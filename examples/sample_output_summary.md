# Meeting Summary: Enterprise Event Streaming Migration Architecture Review

**Date:** 2026-08-14  
**Participants:** Sarah Lin (Principal Architect), Marcus Vance (Lead Data Engineer), Elena Rostova (Director of Infrastructure), David Chen (Product Security Lead)

---

## 1. Executive Summary

- **Meeting Objective:** Finalize the architectural, financial, security, and scheduling plans for migrating the enterprise event streaming infrastructure from self-hosted message broker clusters on virtual compute instances to a managed cloud publish-subscribe platform.
- **Key Decisions Made:**
  - Approved full platform migration from the self-hosted broker to the managed cloud messaging platform.
  - Standardized on Protocol Buffers version 3 (Protobuf) for message serialization and schema enforcement, deprecating unvalidated JSON payloads.
  - Mandated schema registry enforcement at the topic boundary with strict backward compatibility rules.
  - Enforced Customer-Managed Encryption Keys (CMEK), Virtual Private Cloud (VPC) service perimeters, and short-lived identity federation policies across all production messaging resources.
  - Approved target timeline: Dual-publishing in staging by September 5, 2026; InfoSec audit complete by September 12, 2026; production cutover scheduled for October 3, 2026.
- **Strategic Outcomes & Impact:**
  - Reduces net messaging infrastructure and operational costs by 28%, eliminating approximately 22 hours per month of manual broker maintenance and partition rebalancing management.
  - Resolves consumer rebalance lag spikes (previously exceeding 4 minutes during peak traffic), achieving sub-26 millisecond p99 publish latency at 65,000 QPS.
  - Eliminates silent schema drift across polyglot microservices via centralized schema validation and automated CI tooling.
- **Critical Risks & Blockers:**
  - InfoSec compliance approval is a hard gate prior to staging sign-off, requiring complete VPC perimeter validation by September 12, 2026.
  - Memory footprint impact on legacy Python consumer workers using streaming pull clients remains unbenchmarked and unassigned.

---

## 2. Detailed Discussion Record and Action Items

### Topic 1: Messaging Platform Migration Evaluation

- **Discussion Details (What Was Said):** The organization currently operates an 18-node broker cluster across three Availability Zones with a 5-node coordination quorum. The platform team incurs 22 hours per month managing partition rebalancing storms, disk saturation, and rolling patching. Under peak marketing load, consumer group rebalance lag exceeds 4 minutes, violating the 30-second downstream inventory update SLA. The data engineering team evaluated two primary options:
  1. *Upgrading Self-Hosted Broker Software:* Eliminates coordination nodes but retains manual partition rebalancing, broker sizing overhead, and cross-AZ data egress expenses.
  2. *Managed Cloud Messaging Platform:* Fully managed autoscaling messaging service. Pilot benchmarking demonstrated sustained throughput of 65,000 events per second, average publish latency of 14 milliseconds, and p99 latency of 26 milliseconds on multi-region topics.
  3. *Financial Comparison:* Self-hosting costs $14,200 per month in compute/storage plus $8,500 in engineering overhead ($22,700 total). The managed cloud messaging service is projected at $11,800 per month for 4.2 billion monthly messages (2 KB average payload), representing a 28% net financial savings.
- **Points Raised and Rationale:** Upgrading the self-hosted software was rejected because it failed to resolve the core operational pain points around partition scaling and manual node maintenance. The managed cloud messaging platform was selected because it eliminates cluster operational overhead entirely while satisfying all latency and throughput requirements within budget.
- **Key Conclusions:** The team unanimously approved transitioning the entire messaging tier to the managed cloud publish-subscribe platform.

### Topic 2: Schema Evolution and Serialization Standard

- **Discussion Details (What Was Said):** Existing downstream services consume unstructured JSON payloads. This lack of contract enforcement causes schema drift and unhandled parser exceptions in production. The team evaluated legacy binary schema formats versus Protocol Buffers version 3 (Protobuf):
  1. *Legacy Binary Format:* Supported by historical analytics pipelines, but requires complex schema registry coordination across microservices.
  2. *Protobuf v3:* Provides strongly typed code generation across Go, Java, and TypeScript microservices. Payloads are 42% smaller than JSON and 15% smaller than legacy binary schemas, minimizing network overhead.
- **Points Raised and Rationale:** Although the legacy format had historical precedent, Protobuf v3 was selected due to superior polyglot service compatibility, smaller serialization footprint, and direct integration with the central schema registry. Schema validation will occur directly at the topic boundary to reject malformed messages before ingestion.
- **Key Conclusions:** Adopt Protobuf v3 across all event producers. Centralize schema definitions in a dedicated repository with automated CI linting and enforce backward compatibility at the API boundary.

### Topic 3: Security, Governance, and Compliance Controls

- **Discussion Details (What Was Said):** Migrating production event streams requires strict alignment with enterprise InfoSec compliance, data privacy, and identity governance policies. David Chen established three mandatory security requirements:
  1. *Encryption:* Customer-Managed Encryption Keys (CMEK) via Key Management Service (KMS) using the existing `us-central1` key ring for all production topics.
  2. *Network Isolation:* VPC service perimeters surrounding all messaging resources to block exfiltration paths.
  3. *Access Management:* Granular IAM roles (`roles/messaging.publisher`, `roles/messaging.subscriber`) bound to specific resource URIs via short-lived workload identity federation tokens. Long-lived service account JSON keys are strictly prohibited.
- **Points Raised and Rationale:** Security controls must be implemented upstream in infrastructure-as-code to prevent configuration drift and guarantee compliance before data ingestion begins.
- **Key Conclusions:** All infrastructure will be deployed via reusable Terraform modules incorporating CMEK and VPC security policies.

### Topic 4: Migration Timeline and Phasing

- **Discussion Details (What Was Said):** Transitioning to the cloud platform requires zero data loss and uninterrupted operation of downstream business systems. The migration proceeds in three distinct phases:
  1. *Dual-Publishing & Staging Validation:* An adapter in the event gateway will publish simultaneously to the legacy broker and cloud messaging platform in staging starting September 5, 2026. Shadow traffic will run for two weeks to validate message ordering, delivery guarantees, and consumer offsets.
  2. *Security Audit:* Automated InfoSec scanning of VPC perimeters will execute prior to September 12, 2026.
  3. *Production Cutover:* If staging shadow tests demonstrate zero data loss by September 19, 2026, production cutover will occur over the weekend of October 3, 2026.
- **Points Raised and Rationale:** Dual-publishing provides a safe verification window to benchmark latency and verify consumer correctness under real traffic patterns without risking production data integrity.
- **Key Conclusions:** The team agreed to the October 3, 2026 production cutover target date contingent on staging validation and InfoSec sign-off.

### Action Items

| Action Item | Assigned To | Deadline | Acceptance Criteria / Target Deliverable |
| :--- | :--- | :--- | :--- |
| Develop reusable Terraform module for cloud messaging with CMEK and IAM hardening | Tom Bradley | 2026-08-28 | Terraform module submitted and approved in repository |
| Implement dual-publishing adapter in core event gateway | Marcus Vance | 2026-09-05 | Gateway publishing simultaneously to legacy broker and cloud platform in staging |
| Conduct automated security validation scan on VPC perimeters | David Chen | 2026-09-12 | InfoSec compliance report signed and published |
| Verify shadow traffic zero data loss benchmark | Sarah Lin | 2026-09-19 | Sign-off report confirming SLA and zero loss over 14-day staging run |
| Benchmark memory footprint on legacy Python consumer workers with streaming pull client | Unassigned | Not Specified | Resource utilization report comparing legacy vs cloud messaging client overhead |
| Execute production cutover to cloud messaging platform | Marcus Vance | 2026-10-03 | Production traffic routed to cloud platform; legacy broker decommission plan initiated |

---

## 3. Five-Sentence Summary

The enterprise architecture team finalized plans to decommission their self-hosted message broker cluster and migrate all event streaming workloads to a managed cloud publish-subscribe platform by October 3, 2026. This migration resolves chronic consumer rebalancing lag, improves p99 latency to under 26 milliseconds at 65,000 QPS, and yields a 28 percent net infrastructure cost reduction. The organization standardized on Protocol Buffers version 3 with schema registry enforcement at the topic boundary to eliminate downstream schema drift. Production rollout is gated on mandatory InfoSec controls, including Customer-Managed Encryption Keys, Virtual Private Cloud service perimeters, and short-lived identity federation tokens. Staging dual-publishing will launch on September 5, 2026, followed by an InfoSec compliance audit on September 12, 2026, prior to final production cutover.
