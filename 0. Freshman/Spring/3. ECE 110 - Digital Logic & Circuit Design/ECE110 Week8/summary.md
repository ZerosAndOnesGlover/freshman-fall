# ECE 110 · Week 8 · Summary

**Topic —** Registers, shift registers, ring counters, and the two kinds of counter.
**Lectures —** L01 Registers and Shift Registers; L02 Counters — Ripple and Synchronous.
**Work —** PS 8 (100), Lab 8 (100, build both counters and catch the transients on a scope), Quiz 7 (Wednesday, covers Week 7, ungraded).
**Takeaway —** A ripple counter costs zero gates and has two flaws: it settles in N·t_cq, and its bits change in sequence so it passes through states that were never intended — 011 → 010 → 000 → 100, meaning a decoder watching it glitches. A synchronous counter toggles bit k when all lower bits are 1, has no transient states and logarithmic delay, and pays for it in toggle logic. Week 3's trade, in sequential clothing.
**Next —** Week 9 — finite state machines, Mealy and Moore.
