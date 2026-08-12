# CS 211 · Week 4 · Summary

**Topic —** Intermediate representation: three-address code, basic blocks and the control-flow graph, SSA and φ-functions, dataflow analysis, and constant folding.
**Lectures —** L09 Three-Address Code and the Control-Flow Graph; L10 SSA, φ-Functions, and Dataflow Analysis.
**Work —** **MIDTERM 1** (Wednesday, 75 marks, 12.5%, covers Weeks 0–3), PS 4 (100), Lab 4 (unmarked, Friday), Quiz 4 (unmarked, Tuesday, covers Week 3).
**Takeaway —** An optimisation that produces a different answer is a wrong compiler, not a slow one: changing the folder's `/` from Cyan's truncating division to Python's floor division makes `-7/2*100 + -7%2` fold to `-401` instead of `-301`, silently, with every test that avoids negative division still passing. Measured alongside: our CFG for `gcd` matches clang's block for block, and `mem2reg` turns 23 instructions into 11, replacing all eleven memory operations with two φ-nodes.
**Next —** Week 5 — loop-invariant code motion, induction variables, and register allocation by graph colouring, built on the liveness analysis this week's dead-code pass was missing.
