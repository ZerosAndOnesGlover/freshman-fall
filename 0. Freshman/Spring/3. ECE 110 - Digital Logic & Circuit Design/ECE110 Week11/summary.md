# ECE 110 · Week 11 · Summary

**Topic —** Memory circuits: SRAM, DRAM, ROM, and how arrays are organised.
**Lectures —** L01 SRAM and DRAM; L02 ROM and Memory Organisation.
**Work —** PS 11 (100), Lab 11 (100, cost model, refresh budget, and a diode-matrix ROM), Quiz 10 (Wednesday, covers Week 10, ungraded).
**Takeaway —** A flip-flop costs ~20 transistors, SRAM 6, DRAM 1 — so memory is not built from flip-flops, and the 6× DRAM density advantage is paid for with refresh: 8192 rows in a 64 ms window is one row every 7.81 μs, about 4.5% of the device's time. That overhead *rises* with row count (35.8% at 65,536 rows). Memories are square because a flat decoder for 2²⁰ words needs a million gates where a square array needs 2,048.
**Next —** Week 12 — programmable logic, and the final.
