# Meeting Summary: Core Event Streaming Migration Architecture Review

**Date:** 2026-08-14  
**Participants:** Sarah Lin (Principal Architect), Marcus Vance (Lead Data Engineer), Elena Rostova (Director of Infrastructure), David Chen (Product Security Lead)

---

## 1. Executive Summary

- **Meeting Objective:** Finalize architecture, cost, security gates, and timeline to migrate to managed cloud pub/sub.
- **Key Decisions Made:**
  - Migrate 18-node self-hosted cluster to managed cloud pub/sub.
  - Standardize on Protobuf v3 with schema registry backward-compatibility checks.
  - Enforce CMEK, VPC perimeters, and workload identity federation via Terraform.
  - Schedule: Sept 5 dual-publish, Sept 12 InfoSec audit, Oct 3, 2026 cutover.
- **Strategic Outcomes & Impact:**
  - 28% net savings ($22,700 to $11,800/mo); eliminates 22 hrs/mo maintenance.
  - Eliminates >4-minute rebalance lag; achieves 14ms avg / 26ms p99 at 65,000 QPS.
  - Prevents silent schema drift; payloads shrink 42% vs. JSON.
- **Critical Risks & Blockers:**
  - Sept 12 InfoSec VPC perimeter audit is a hard staging gate.
  - Legacy Python pull-client memory benchmark is unassigned.

---

## 2. Detailed Discussion Record and Action Items

### Topic 1: Messaging Platform Migration

- **Key Points:**
  - 18-node cluster (3 AZs, 5-node quorum) takes 22 hrs/mo for rebalancing, disk saturation, and patching.
  - Peak traffic drives >4-minute rebalance lag, breaching the 30-second downstream inventory SLA.
  - Cloud pub/sub pilot hit 65,000 events/sec at 14ms avg / 26ms p99 multi-region latency.
  - Monthly cost: $22,700 self-hosted ($14,200 infra + $8,500 ops) vs. $11,800 managed (4.2B msgs, 2 KB avg, tiered logging)—28% net savings.
- **Trade-offs & Rationale:** Self-hosted upgrade drops quorum nodes but retains manual partition scaling, hot broker rebalancing, and cross-AZ egress; managed removes ops within SLA/budget.
- **Decision / Status:** Approved migration to managed cloud pub/sub.

### Topic 2: Schema Evolution and Serialization

- **Key Points:**
  - Unstructured JSON causes silent schema drift and downstream parser failures.
  - Protobuf v3 payloads shrink 42% vs. JSON and 15% vs. legacy binary across Go, Java, and TypeScript.
  - Topic-level schema registry enforces backward compatibility, rejecting poison pills at the API boundary.
- **Trade-offs & Rationale:** Rejected legacy binary (analytics precedent) for Protobuf v3's faster polyglot codegen, typed stubs, and smaller wire size.
- **Decision / Status:** Adopt Protobuf v3, central `.proto` Git repo, and CI linting.

### Topic 3: Security, Governance, and Compliance

- **Key Points:**
  - **Encryption:** CMEK via KMS (`us-central1` key ring) on all production topics.
  - **Network:** VPC service perimeters blocking data exfiltration.
  - **Access:** Resource-scoped IAM (`roles/messaging.publisher`, `roles/messaging.subscriber`) via short-lived workload identity federation; static JSON keys banned.
- **Decision / Status:** Automate controls via reusable Terraform modules.

### Topic 4: Migration Timeline and Phasing

- **Key Points:**
  - **Sept 5, 2026:** Deploy staging dual-publish adapter; run 14-day shadow traffic verifying delivery and offsets.
  - **Sept 12, 2026:** Run automated InfoSec VPC security validation scan.
  - **Sept 19 / Oct 3, 2026:** Zero-loss shadow sign-off (Sept 19) gates Oct 3 cutover.
  - Legacy Python consumer streaming pull-client memory benchmark deferred to Monday sprint planning.
- **Decision / Status:** Approved Oct 3, 2026 cutover gated on zero-loss staging validation and InfoSec sign-off.

### Action Items

| Action Item | Assigned To | Deadline | Acceptance Criteria / Target Deliverable |
| :--- | :--- | :--- | :--- |
| Build Terraform module (CMEK, VPC, IAM) | Tom Bradley | 2026-08-28 | Approved module merged in Terraform repo |
| Build staging dual-publish gateway adapter | Marcus Vance | 2026-09-05 | Simultaneous legacy/cloud staging publish |
| Run InfoSec VPC security validation scan | David Chen | 2026-09-12 | Signed InfoSec compliance report |
| Verify 14-day shadow zero-loss benchmark | Sarah Lin | 2026-09-19 | Sign-off confirming SLA and zero loss |
| Benchmark Python consumer pull-client memory | Unassigned | Not Specified | Legacy vs. cloud client resource report |
| Execute production cutover to cloud pub/sub | Marcus Vance | 2026-10-03 | Traffic migrated; broker decommission started |

---

## 3. Five-Sentence Summary

The team approved migrating from an 18-node self-hosted cluster to managed cloud pub/sub by October 3, 2026. The migration eliminates 4-minute rebalance lag, achieves 26ms p99 latency at 65,000 QPS, and cuts net costs 28%. Services will adopt Protobuf v3 with topic-level schema registry validation to stop schema drift. Production requires Terraform-managed CMEK, VPC perimeters, and short-lived workload identity federation tokens. Staging dual-publishing begins September 5, followed by a September 12 InfoSec audit and September 19 zero-loss sign-off.

---

## 4. Action Items for Marcus Vance

Marcus Vance will set up the central `.proto` Git repo with automated CI backward-compatibility linting. By September 5, 2026, he must deploy the staging dual-publishing gateway adapter for 14-day shadow validation of delivery guarantees and offsets. After September 19 zero-loss sign-off and InfoSec approval, he will execute production cutover on October 3, 2026, and start broker decommissioning.
