# CS 201 · Week 1 · Summary

**Topic —** Integers, undefined behaviour, IEEE 754, and why floating-point addition is not associative.
**Lectures —** L04 Integers, Overflow and Undefined Behaviour; L05 IEEE 754 — Anatomy of a Float; L06 Why Floating-Point Addition Is Not Associative.
**Work —** PS 1 (100, due Week 2), Lab 1 (unmarked), Quiz 1 Monday covering Week 0 (unmarked, key in the paper).
**Takeaway —** Finite representations lose information silently, and the compiler is complicit. `x + 1 > x` on signed ints compiles to `mov eax,0x1` — the check is deleted, not wrapped. Summing 1/i over 10⁷ terms in float is 7.7% wrong because 79% of the terms are absorbed, starting exactly at i = 2²¹ where 1/i equals half an ULP. Reversing the loop is 139× better, Kahan is 1.7 million× better, and `-ffast-math` deletes Kahan entirely. All measured.
**Next —** Week 2 — x86-64 assembly, the instruction set properly.
