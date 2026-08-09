# ECE 110 · Week 10 · Summary

**Topic —** Verilog: describing hardware rather than programming it, and the three classic traps.
**Lectures —** L01 Describing Hardware, Not Programming It; L02 Sequential Verilog and the Classic Traps.
**Work —** PS 10 (100), Lab 10 (100, write and break the three traps), Quiz 9 (Wednesday, covers Week 9, ungraded).
**Takeaway —** Verilog describes a structure that exists all at once. Measured: blocking assignment collapses a 3-stage shift register into one (111 → 000 instead of 001 → 010 → 100); an `if` without an `else` in `always @(*)` builds a latch that holds its output after the inputs change; and an incomplete sensitivity list makes simulation and silicon disagree — the simulation being the wrong one. Writing an FSM as a `case` statement makes the tool derive the equations Week 9 derived by hand.
**Next —** Week 11 — memory: SRAM, DRAM, ROM.
