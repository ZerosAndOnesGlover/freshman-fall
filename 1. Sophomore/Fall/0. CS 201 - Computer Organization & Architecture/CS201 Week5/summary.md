# CS 201 · Week 5 · Summary

**Topic —** Pipelining, hazards, branch prediction, out-of-order execution, SIMD and Amdahl's Law.
**Lectures —** L16 The Pipeline and Its Hazards; L17 Branch Prediction and Out-of-Order Execution; L18 SIMD and Amdahl's Law.
**Work —** **MIDTERM 1 Monday 18:00, Weeks 0–4, 100 points, 12.5%.** PS 5 (100, due Week 6), Lab 5 (unmarked), Quiz 5 Monday covering Week 4 (unmarked, key in the paper).
**Takeaway —** A program is limited by one resource at a time, and each technique only helps if it is the right one. Four accumulator chains ran exactly 4.00× faster than one and eight ran 7.25×, as the limit moved from dependency latency to issue throughput. Sorting an array made an identical loop 8.03× faster — but only after `-fno-if-conversion`, because GCC had already emitted `cmovg` and the famous demonstration measured 1.02×; branchless turns out to lose 2× to a correctly predicted branch while winning 8× on an unpredictable one. The same AVX2 loop gave 4.51× at 16 KiB per array and 1.07× at 16 MiB, identical instructions throughout, because the second is waiting for DRAM. Amdahl prices the disappointment: 4.5× on 40% of runtime is 1.45× overall.
**Next —** Week 6 — virtual memory, page tables and the TLB.
