# PROG 102 · Week 5 · Summary

**Topic —** RAII, smart pointers, and move semantics
**Lectures —** L16 RAII and unique_ptr; L17 shared_ptr, weak_ptr and the Cost of Sharing; L18 Move Semantics.
**Work —** PS 5 (from raw pointers to smart pointers), Lab 5 (leak detection with AddressSanitizer), Quiz 5.
**Takeaway —** RAII makes ownership a type rather than a comment. `shared_ptr` is not free — it is atomic refcounting, and two of them in a cycle never release anything.
**Next —** Week 6 — implementing containers.
