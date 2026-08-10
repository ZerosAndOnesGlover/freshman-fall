# CS 201 · Week 2 · Summary

**Topic —** x86-64 assembly: registers, addressing modes, arithmetic, flags and control flow, read from real compiler output.
**Lectures —** L07 Registers, Operands and the Two Syntaxes; L08 Arithmetic, and What the Compiler Does Instead of Dividing; L09 Flags, Conditionals and Control Flow.
**Work —** PS 2 (100, due Week 3), Lab 2 (unmarked), Quiz 2 Monday covering Week 1 (unmarked, key in the paper).
**Takeaway —** The instruction set is small and strange, and the compiler is fluent. `lea` is the general adder and touches no memory; `cmp` writes no register; `x/10` compiles to a multiply by 0x66666667 = ⌊2³⁴/10⌋+1 with no division instruction; `x/8` is four instructions where `x>>3` is one, because `/` truncates and `sar` floors; and one unsigned `cmp`+`ja` bounds a range on both sides. A seven-case switch compiled four different ways — arithmetic (10x+10), a `.rodata` value table, a 32-bit-offset jump table, and a comparison chain — chosen by the case values alone.
**Next —** Week 3 — procedures, the stack, and the System V calling convention.
