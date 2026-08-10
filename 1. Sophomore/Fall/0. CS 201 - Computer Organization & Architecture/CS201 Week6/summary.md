# CS 201 · Week 6 · Summary

**Topic —** Virtual memory: the page table, the TLB, demand paging, copy-on-write and replacement.
**Lectures —** L19 Virtual Memory and the Page Table; L20 The TLB and the Cost of Translation; L21 Demand Paging, Copy-on-Write and Replacement.
**Work —** PS 6 (100, due Week 7), Lab 6 (unmarked, sat Tuesday of Week 7), Quiz 6 Monday covering Week 5 (unmarked, key in the paper).
**Takeaway —** Cache residency and TLB reach are separate capacities. 512 pointers held constant at 512 cache lines — 32 KiB, L1-resident throughout — cost 1.24 ns spread over 8 pages and 27.57 ns spread over 8192, a 22× penalty that is pure address translation; the 1.24 ns matches Week 4's independently measured L1 latency of 1.22 ns. Allocation is a promise: `malloc(512 MiB)` grew RSS by 136 KiB, and touching every page produced 131,071 minor faults for 131,072 pages, one each, at ~1900 ns or 6200 cycles apiece. `fork` of a fully resident 256 MiB process took 4.3 ms and copied nothing — the child was born with 14 faults and took exactly 65,536 more, one per page, when it wrote. Huge pages, meanwhile, did nothing at all for a DRAM-bound chase, because translation was not what it was waiting for.
**Next —** Week 7 — I/O and storage, where major faults get their price.
