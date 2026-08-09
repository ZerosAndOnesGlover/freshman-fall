# PROG 102 · Week 1 · Summary

**Topic —** Operator overloading and the Rule of Three
**Lectures —** L04 Operator Overloading; L05 Copy Semantics and the Rule of Three; L06 The Copy-and-Swap Idiom.
**Work —** PS 1 (a Vector3D class), Lab 1 (debugging copy semantics), Quiz 1.
**Takeaway —** If you write one of destructor, copy constructor or copy assignment, you need all three — the compiler's default is a shallow copy, and a shallow copy of an owning pointer is a double free.
**Next —** Week 2 — templates.
