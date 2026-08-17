# CS 211 · Week 5 · Summary

**Topic —** Optimization: live-variable analysis, dominators and natural loops, loop-invariant code motion, induction variables, register allocation by graph colouring, instruction selection, peephole, the pass pipeline and LTO.
**Lectures —** L11 Liveness, Loops, and Loop-Invariant Code Motion; L12 Register Allocation, Instruction Selection, and the Pipeline.
**Work —** PS 5 (100), Lab 5 (unmarked, Friday), Quiz 5 (unmarked, Tuesday, covers Week 4).
**Takeaway —** The rule governing code motion is not about loops: LLVM hoists `k * 2 + 1` out of a loop it might never enter, and refuses to hoist `100 / k` from the same loop, because the multiply cannot trap and the division can. Loop rotation is how a compiler buys the hoist without the bet — it optimises nothing itself, it restructures the CFG so the guard exists. Measured alongside: Week 4's dead-code pass silently deletes a live `load` (8 → 6 instructions on three lines of Cyan), Chaitin's heuristic is *optimal* on `scale` at k=7 exactly matching peak simultaneous liveness, and `-O2` emits 3.8× more instructions than `-O1` while running 1.6× faster.
**Next —** Week 6 — memory management and garbage collection, because `alloc` produces a pointer and nothing in the pipeline ever frees it. Project 1 assigned.
