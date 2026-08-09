# ECE 110 · Week 5 · Summary

**Topic —** The reusable MSI blocks: decoders, encoders, priority encoders, multiplexers, demultiplexers.
**Lectures —** L01 Decoders and Encoders; L02 Multiplexers and Demultiplexers.
**Work —** PS 5 (100), Lab 5 (100, three implementations of one function, compared), Quiz 4 (Wednesday, covers Week 4, ungraded).
**Takeaway —** A decoder's outputs are the minterms, so decoder + OR implements any function straight from the truth table. Better: by Shannon expansion a 2^(k-1):1 mux implements any k-variable function, with 0, 1, x or x' on each data input — a lookup table, which costs the same whatever function is inside it. That is why an FPGA needs no minimisation.
**Next —** Week 6 — the ALU, and the Midterm.
