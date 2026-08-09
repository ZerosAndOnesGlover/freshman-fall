# ECE 110 · Week 3 · Summary

**Topic —** Combinational circuits: half adder, full adder, ripple-carry adder, subtraction and flags.
**Lectures —** L01 Half and Full Adders; L02 The Ripple-Carry Adder and Its Delay.
**Work —** PS 3 (100), Lab 3 (100, build a 4-bit adder and time it), Quiz 2 (Wednesday, covers Week 2, ungraded).
**Takeaway —** A ripple-carry adder is 5N gates and 2N+1 gate delays — both linear, and only one is a problem. At 64 bits that is 320 gates (trivial) and 2.58 ns (7.7 periods of a 3 GHz clock, so unusable). Subtraction costs N XOR gates because XOR is a controlled inverter, and the overflow flag costs one more.
**Next —** Week 4 — Karnaugh maps, and making circuits smaller.
