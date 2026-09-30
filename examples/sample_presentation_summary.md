# Presentation Summary: Next-Generation Vector Search Engine Architecture Keynote

**Date:** 2026-09-18  
**Presenter(s):** Dr. Aris Thorne (Distinguished Systems Engineer)

---

## Chronological Presentation Summary

### 1. Introduction and Slide 1: The Billion-Vector Memory Wall

- **Presenter:** Dr. Aris Thorne
- **What Was Presented & Said:** Dr. Thorne introduced the architectural keynote on HyperIndex v4, a distributed vector search engine designed to scale billion-vector similarity search while reducing memory usage. Presenting Slide 1 ("The Billion-Vector Memory Wall") and referencing its left chart, he detailed that over the prior 18 months the enterprise search cluster expanded from 120 million embeddings to 1.4 billion 1536-dimensional floating-point vectors. Storing uncompressed FP32 HNSW graphs in DRAM consumed 11.2 terabytes of cluster memory across 180 high-memory nodes. Under peak query loads of 18,000 queries per second (QPS), garbage collection pauses and cross-node scatter-gather fan-out caused p99 query latency to reach 142 milliseconds, exceeding the 30-millisecond search tier target.

### 2. Slide 2: Two-Tier Hybrid Storage and RabitQ Quantization

- **Presenter:** Dr. Aris Thorne
- **What Was Presented & Said:** Presenting Slide 2 ("Two-Tier Hybrid Storage and RabitQ Quantization"), Dr. Thorne explained the redesigned two-tier hybrid storage engine built to reduce memory consumption without sacrificing recall:
  1. *Tier 1 (CPU L3 Cache and DRAM):* Compresses 1536-dimensional vectors using asymmetric binary quantization with corrective scalar residuals, reducing the in-memory footprint by 64% to 4.0 terabytes across 64 nodes.
  2. *Tier 2 (Local NVMe SSDs):* Shown at the bottom of the Slide 2 diagram, full-precision FP16 vectors are stored on local NVMe solid-state drives in 16-kilobyte aligned blocks.
  3. *Query Execution Flow:* The engine traverses the compressed in-memory graph to select the top 250 candidate IDs, then executes a single batched `io_uring` NVMe read to rescore only those 250 candidates in full precision.

### 3. Slide 3: Zero-Copy Kernel Bypass and SIMD Distance Kernels

- **Presenter:** Dr. Aris Thorne
- **What Was Presented & Said:** Presenting Slide 3 ("Zero-Copy Kernel Bypass and SIMD Distance Kernels"), Dr. Thorne noted that profiling the NVMe rescoring stage revealed standard Linux page cache copies consumed 38% of CPU cycles. Referencing the pipeline diagram on Slide 3, he described bypassing the Linux kernel page cache using direct asynchronous `io_uring` submission queues paired with pre-pinned hugepage ring buffers. Once the 250 full-precision candidate vectors load into the ring buffer, a custom AVX-512 SIMD inner-product kernel calculates exact cosine distances at a sustained rate of 1.8 billion vector comparisons per second per core.

### 4. Slide 4: Dynamic Predicate Pushdown During Graph Traversal

- **Presenter:** Dr. Aris Thorne
- **What Was Presented & Said:** Presenting Slide 4 ("Dynamic Predicate Pushdown During Graph Traversal"), Dr. Thorne addressed the post-filtering problem in vector databases, where filtering after a top-K vector search yields nearly empty results when a tenant ID or date range filter matches only 1% of documents. He walked through the adaptive bitmap pushdown engine shown on Slide 4, which evaluates metadata filter cardinality prior to graph traversal using Roaring Bitmaps:
  - *Selectivity Above 15%:* The engine evaluates the Roaring Bitmap inline during HNSW graph hops.
  - *Selectivity Below 2%:* The engine switches to a bitmap-driven brute-force scan over the quantized vectors, maintaining 100% filter completeness with zero recall degradation.

### 5. Slide 5: Production Telemetry and Live Benchmark Readout

- **Presenter:** Dr. Aris Thorne
- **What Was Presented & Said:** Concluding on Slide 5 ("Production Telemetry and Live Benchmark Readout"), Dr. Thorne displayed a live Grafana dashboard from the `us-east` canary cluster operating on the 1.4-billion vector dataset at 20,000 concurrent QPS and reported three benchmark outcomes:
  - *Recall Accuracy (Top-Left Panel):* `Recall@10` measured 98.4% relative to exact k-NN ground truth.
  - *Latency Reduction (Center Panel Histogram):* Median p50 latency measured 4.8 milliseconds and p99 tail latency measured 16.2 milliseconds, representing an 88% reduction in p99 latency compared to the legacy v3 cluster.
  - *Infrastructure Cost Savings:* Reducing cluster size from 180 nodes to 64 nodes lowered annual compute and memory costs by $1.14 million per year.
