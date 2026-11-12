# Presentation Summary: Distributed Vector Search Engine Architecture Keynote

**Date:** 2026-09-18  
**Presenter(s):** Dr. Aris Thorne (Distinguished Systems Engineer)

---

## Chronological Presentation Summary

### 1. Introduction & Slide 1: The Billion-Vector Memory Wall

- HyperIndex v4 scales billion-vector similarity search while halving memory usage.
- Cluster grew over 18 months from 120M embeddings to 1.4B 1536D FP32 vectors (Slide 1 left chart).
- Uncompressed FP32 HNSW graphs consumed 11.2 TB DRAM across 180 high-memory nodes.
- At 18,000 peak QPS, GC pauses and cross-node scatter-gather drove 142 ms p99 latency vs. 30 ms SLA.

### 2. Slide 2: Two-Tier Hybrid Storage & RabitQ Quantization

- **Tier 1 (L3 / DRAM):** Asymmetric binary quantization with corrective scalar residuals compresses 1536D vectors, cutting memory 64% to 4.0 TB across 64 nodes.
- **Tier 2 (Local NVMe SSDs):** Full-precision FP16 vectors stored in 16 KB aligned blocks (Slide 2 bottom diagram).
- **Query flow:** Traverse Tier 1 graph for top 250 candidate IDs, then issue one batched `io_uring` NVMe read for full-precision rescoring.

### 3. Slide 3: Zero-Copy Kernel Bypass & SIMD Distance Kernels

- NVMe rescoring profiling showed Linux page cache copies consumed 38% of CPU cycles.
- Direct async `io_uring` queues and pre-pinned hugepage ring buffers bypass the page cache (Slide 3 pipeline diagram).
- Custom AVX-512 SIMD inner-product kernel scores exact cosine distances on 250 candidates at 1.8B comparisons/sec/core.

### 4. Slide 4: Dynamic Predicate Pushdown During Graph Traversal

- Post-filtering fails on selective metadata filters (e.g., 1% match on tenant ID or date range), yielding near-empty results.
- Adaptive query planner evaluates filter cardinality via Roaring Bitmaps pre-traversal (Slide 4 diagram):
  - **>15% selectivity:** Evaluates Roaring Bitmap inline during HNSW graph hops.
  - **<2% selectivity:** Switches to bitmap-driven brute-force scan over quantized vectors (100% completeness, zero recall loss).

### 5. Slide 5: Production Telemetry & Live Benchmark Readout

- Live `us-east` canary telemetry on 1.4B vectors at 20,000 concurrent QPS:
  - **Recall (top-left):** `Recall@10` at 98.4% vs. exact k-NN ground truth.
  - **Latency (center histogram):** 4.8 ms p50 and 16.2 ms p99 (-88% vs. legacy v3).
  - **Cost:** Shrinking 180 to 64 nodes cuts compute and memory spend by $1.14M/year.
