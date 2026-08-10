# CS 201 · Week 3 · Summary

**Topic —** Procedures: `call`/`ret`, the stack frame, the System V ABI, alignment, the red zone, and recursion in hand-written assembly.
**Lectures —** L10 `call`, `ret` and the Stack Frame; L11 The System V AMD64 Calling Convention; L12 Alignment, the Red Zone and Recursion.
**Work —** PS 3 (100, due Week 4), Lab 3 (unmarked), Quiz 3 Monday covering Week 2 (unmarked, key in the paper). **Midterm 1 announced — Week 5, covering Weeks 0–4.**
**Takeaway —** `ret` pops eight bytes and jumps to them with no validation, which is both why separately compiled code interoperates and why stack smashing works. Overwriting a return address in GDB gave `SIGSEGV at 0x00000000deadbeef`; pointing it at `main` re-entered `main`. Everything else is convention: `fib`'s `push rbx` exists only because `rax` cannot survive the second `call`, and its 48-byte frame accounts exactly as 8 + 8 + 8 + 24. Misalignment, though, is usually silent — removing the alignment `sub` from a recursive fib still returned fib(30) correctly, because a misaligned `rsp` faults only when the callee happens to execute an aligned SSE instruction.
**Next —** Week 4 — the memory hierarchy, where the time actually goes.
