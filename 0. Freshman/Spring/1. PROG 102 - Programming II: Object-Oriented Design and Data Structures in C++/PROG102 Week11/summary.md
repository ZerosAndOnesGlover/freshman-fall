# PROG 102 · Week 11 · Summary

**Topic —** Lambdas, type erasure, and modern C++
**Lectures —** L34 Lambdas and Closures; L35 std::function and Type Erasure; L36 constexpr and Modern Features.
**Work —** PS 11 (imperative to functional), Lab 11 (profiling lambda overhead), Quiz 11, **Project 2** assigned (a data structure library).
**Takeaway —** A lambda is a compiler-generated class with `operator()`, so it inlines to nothing — `std::function` erases the type and costs an indirection. Knowing which you have is knowing what you pay.
**Next —** Week 12 — testing, profiling, and systems design.
