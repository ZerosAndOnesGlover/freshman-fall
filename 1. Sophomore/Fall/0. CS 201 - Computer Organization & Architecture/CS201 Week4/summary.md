# CS 201 · Week 4 · Summary

**Topic —** The memory hierarchy, cache organisation, and locality as the programmer's only lever.
**Lectures —** L13 The Memory Hierarchy, Measured; L14 Cache Organisation — Lines, Sets and Ways; L15 Locality as Leverage.
**Work —** PS 4 (100, due Week 5), Lab 4 (unmarked), Quiz 4 Monday covering Week 3 (unmarked, key in the paper). **Midterm 1 next week, Weeks 0–4.**
**Takeaway —** Diagnose the level before choosing the intervention. A pointer chase found this machine's cache sizes with nothing but a stopwatch — cliffs at 32 KiB, 256 KiB and 6 MiB, at 4/12/41/438 cycles, so DRAM costs ~107 L1 hits. Swapping two loop lines was worth 30×. Blocking the transpose gave 3.29× — but its L1 miss rate got *worse* (41.5% → 42.5%) and the last-level rate collapsed (41.5% → 13.5%), because in the naive version every L1 miss went all the way to DRAM. At N=512, where everything fits in L3, blocking did nothing and the LLd counts matched to four significant figures; that null result is what makes the first one credible. Padding a 512×512 column traversal — the textbook conflict fix — moved the miss rate 1.3 points and ran marginally slower, because the problem was spatial locality, not conflict.
**Next —** Week 5 — pipelining and instruction-level parallelism, plus Midterm 1.
