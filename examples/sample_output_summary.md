# Meeting Summary: Core Event Streaming Migration Architecture Review

**Date:** 2026-08-14  
**Participants:** Sarah Lin (Principal Architect), Marcus Vance (Lead Data Engineer), Elena Rostova (Director of Infrastructure), David Chen (Product Security Lead)

---

## 1. Executive Summary

- **Meeting Objective:** Finalize architecture, cost, security gates, and timeline for cloud pub/sub migration.
- **Key Decisions Made:**
  - Migrate 18-node self-hosted cluster to managed cloud pub/sub.
  - Standardize on Protobuf v3 with schema registry backward-compatibility checks.
  - Enforce CMEK, VPC perimeters, and workload identity federation via Terraform.
  - Schedule: Sept 5 dual-publish, Sept 12 InfoSec audit, Oct 3, 2026 cutover.
- **Strategic Outcomes & Impact:**
  - Cuts net cost 28% ($22,700 to $11,800/mo) and saves 22 hrs/mo ops.
  - Cuts >4-min rebalance lag to 14ms avg / 26ms p99 at 65,000 QPS.
  - Stops silent schema drift; shrinks payloads 42% vs. JSON.
- **Critical Risks & Blockers:**
  - Sept 12 InfoSec VPC perimeter audit is a hard staging gate.
  - Legacy Python pull-client memory benchmark is unassigned.

---

## 2. Detailed Discussion Record and Action Items

### Topic 1: Messaging Platform Migration

- **Key Points:**
  - 18-node cluster (3 AZs, 5-node quorum) takes 22 hrs/mo for rebalancing, disk saturation, and patching.
  - Peak campaigns cause >4-min rebalance lag, breaching the 30s inventory SLA.
  - Cloud pub/sub pilot hit 65,000 events/sec at 14ms avg / 26ms p99 multi-region latency.
  - Monthly cost: $22,700 self-hosted ($14,200 infra + $8,500 ops) vs. $11,800 managed (4.2B msgs, 2 KB avg, tiered logging) -- 28% net savings.
- **Trade-offs & Rationale:** Self-hosted upgrade drops quorum nodes but keeps manual scaling, hot rebalancing, and cross-AZ egress; managed removes ops within SLA/budget.
- **Decision / Status:** Approved migration to managed cloud pub/sub.

### Topic 2: Schema Evolution and Serialization

- **Key Points:**
  - Unstructured JSON causes silent schema drift and downstream parser failures.
  - Protobuf v3 payloads shrink 42% vs. JSON and 15% vs. legacy binary across Go, Java, and TypeScript.
  - Topic-level schema registry enforces backward compatibility, rejecting poison pills at API boundary.
- **Trade-offs & Rationale:** Chosen over legacy binary (analytics precedent) for faster polyglot codegen, typed stubs, and smaller payloads.
- **Decision / Status:** Adopt Protobuf v3, central `.proto` Git repo, and CI linting.

### Topic 3: Security, Governance, and Compliance

- **Key Points:**
  - **Encryption:** CMEK via KMS (`us-central1` key ring) on all production topics.
  - **Network:** VPC service perimeters blocking data exfiltration.
  - **Access:** Resource-scoped IAM (`roles/messaging.publisher`, `roles/messaging.subscriber`) via short-lived workload identity federation; static JSON keys banned.
- **Decision / Status:** Automate controls via reusable Terraform modules.

### Topic 4: Migration Timeline and Phasing

- **Key Points:**
  - **Sept 5, 2026:** Deploy staging dual-publish adapter; run 14-day shadow delivery/offset check.
  - **Sept 12, 2026:** Run automated InfoSec VPC security scan.
  - **Sept 19 / Oct 3, 2026:** Zero-loss shadow sign-off (Sept 19) gates Oct 3 cutover.
  - Python consumer pull-client memory benchmark deferred to Monday sprint planning.
- **Decision / Status:** Approved Oct 3, 2026 cutover gated on zero-loss staging and InfoSec sign-off.

### Action Items

| Action Item | Assigned To | Deadline | Acceptance Criteria / Target Deliverable |
| :--- | :--- | :--- | :--- |
| Build Terraform module (CMEK, VPC, IAM) | Tom Bradley | 2026-08-28 | Approved module merged in repo |
| Build staging dual-publish gateway adapter | Marcus Vance | 2026-09-05 | Simultaneous legacy/cloud staging publish |
| Run InfoSec VPC security validation scan | David Chen | 2026-09-12 | Signed InfoSec compliance report |
| Verify 14-day shadow zero-loss benchmark | Sarah Lin | 2026-09-19 | SLA and zero-loss sign-off |
| Benchmark Python consumer pull-client memory | Unassigned | Not Specified | Client memory comparison report |
| Execute production cutover to cloud pub/sub | Marcus Vance | 2026-10-03 | Traffic migrated; decommission started |
