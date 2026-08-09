# ECE 110 · Week 9 · Summary

**Topic —** Finite state machines: the design procedure, state assignment, Mealy and Moore.
**Lectures —** L01 State Diagrams and the Design Procedure; L02 Mealy vs Moore.
**Work —** PS 9 (100), Lab 9 (100, one detector built both ways), Quiz 8 (Wednesday, covers Week 8, ungraded).
**Takeaway —** The state is a compression of the past, and deciding what to keep is the only creative step — for a 1011 detector it is the longest matching prefix, giving four states. Mealy needs fewer states than Moore (4 vs 5) and responds a cycle earlier, but its output can glitch because an input feeds it directly; Moore's cannot. Register a Mealy output and you get both.
**Next —** Week 10 — Verilog, and describing hardware instead of drawing it.
