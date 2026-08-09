# ECE 110 · Digital Logic
## Problem Set 11
### Topic: Memory Circuits — SRAM, DRAM, ROM
**Released:** Thursday, Week 11 · **Due:** Thursday, Week 12 at the start of class

---

> **Show the arithmetic.** Most of this problem set is counting, and the counts are the point.

---

## Part A — Cells (5 pts each)

**A1.** Give the transistor count per bit for a D flip-flop, an SRAM cell and a DRAM cell. **Why is memory not built from flip-flops?**

**A2.** Draw the 6T SRAM cell. **Which part of it did you meet in Week 7?**

**A3.** How is an SRAM cell written? **Why is transistor sizing a design constraint here?**

**A4.** Draw the 1T1C DRAM cell and state what physically holds the bit.

---

## Part B — DRAM's Three Complications (6 pts each)

**B1.** **Why is a DRAM read destructive**, and what must the chip do about it?

**B2.** A device has **8192 rows** and a **64 ms** retention time. **How often must a row be refreshed?**

**B3.** With a refresh cycle time of **350 ns**, **what fraction of the time is spent refreshing?** Show the arithmetic.

**B4.** **What does that fraction buy?** Compare a 1 Gib SRAM and a 1 Gib DRAM in transistors.

**B5.** Week 2 said every gate restores its signal so noise never accumulates. **Explain why a DRAM cell is the exception**, and what maintains the digital abstraction there.

---

## Part C — Organisation (6 pts each)

**C1.** How many AND gates does a flat decoder for $2^{20}$ words need?

**C2.** Organised as a square array, how many decoder gates are needed instead? **State the saving.**

**C3.** Tabulate flat versus square for $2^{10}$, $2^{16}$ and $2^{20}$ words. **Does the advantage grow or shrink with size?**

**C4.** **Why do memory chips have separate row and column address strobes?**

**C5.** **Why is accessing consecutive addresses faster than random access?** Connect this to the array structure.

---

## Part D — ROM and Interfaces (5 pts each)

**D1.** **A ROM is which Week 5 circuit?** Give the decoder line count and the stored-bit count for a 10-bit address, 8-bit word ROM.

**D2.** Name the four ROM variants and say which is non-volatile and electrically erasable.

**D3.** **What is a three-state output, and why is it not a third logic value?** What happens if two devices drive a bus at once?

**D4.** Show how to build a $1\text{K}\times8$ memory from $1\text{K}\times4$ devices, and a $2\text{K}\times8$ from $1\text{K}\times8$ devices. **Which Week 5 block does each need?**

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — cells | 4 × 5 | 20 |
| B — DRAM's complications | 5 × 6 | 30 |
| C — organisation | 5 × 6 | 30 |
| D — ROM and interfaces | 4 × 5 | 20 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 11 · due Thursday of Week 12*
