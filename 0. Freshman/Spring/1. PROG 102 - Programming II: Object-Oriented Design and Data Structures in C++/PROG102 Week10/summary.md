# PROG 102 · Week 10 · Summary

**Topic —** Concurrency: threads, mutexes, and atomics
**Lectures —** L31 Threads and Races; L32 Mutexes, Deadlock and Condition Variables; L33 Atomics and Thread-Safe Data Structures.
**Work —** PS 10 (a thread-safe bounded queue), Lab 10 (finding races with ThreadSanitizer), Quiz 10, **Midterm 2** (Weeks 5–9, 12.5%).
**Takeaway —** A data race is undefined behaviour that usually looks like it works. ThreadSanitizer finds what testing does not, because the bug is in the interleavings you did not happen to run.
**Next —** Week 11 — lambdas and modern C++.
