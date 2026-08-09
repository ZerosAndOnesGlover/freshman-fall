# ECE 110 · Week 7 · Summary

**Topic —** Latches and flip-flops: SR, gated D, master–slave D, JK, T — and timing.
**Lectures —** L01 Latches and the Forbidden State; L02 Flip-Flops and Timing.
**Work —** PS 7 (100), Lab 7 (100, build a latch and catch it racing), Quiz 6 (Wednesday, covers Week 6, ungraded).
**Takeaway —** Memory requires feedback, and feedback costs determinism: leaving the SR latch's forbidden state is a race whose outcome is decided by gate speed, not by the inputs. You fix a race by making the bad input unreachable (the gated D latch), then fix transparency with a master–slave edge-triggered flip-flop. JK redefines the forbidden combination as toggle, and its excitation table's don't-cares are why JK designs minimise better.
**Next —** Week 8 — registers, counters, and shift registers.
