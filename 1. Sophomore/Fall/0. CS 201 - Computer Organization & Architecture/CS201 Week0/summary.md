# CS 201 · Week 0 · Summary

**Topic —** The abstraction hierarchy from transistors to programs, the fetch-decode-execute cycle, and why performance stopped being free.
**Lectures —** L01 The Abstraction Hierarchy; L02 Von Neumann and the Fetch-Decode-Execute Cycle; L03 Moore's Law and the Shape of x86-64.
**Work —** PS 0 (100), Lab 0 (unmarked, checked off in session). **No quiz** — Quiz 1 in Week 1 covers this week.
**Takeaway —** The machine does not run your source. GCC folded a hundred-million-iteration loop into `movabs rdx,0x11c3793adb7080` at compile time — measured, alongside Python at 12.06 s against C's 0.258 s for the same sum. Read the disassembly, not the C.
**Next —** Week 1 — data representation, and why IEEE 754 addition is not associative.
