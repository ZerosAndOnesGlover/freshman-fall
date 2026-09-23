# ECE 110 · Digital Logic
## Week 11 · Overview
### Memory Circuits — SRAM, DRAM, ROM

---

**Topic:** where the bits actually live
**Reading:** Harris & Harris §5.5 | Mano & Ciletti §7.1–7.5
**Assessment this week:** PS 11 (released Thu 8 Apr 14:30, due Thu 15 Apr 13:00), Lab 11 (**Fri 9 Apr**, 14:00), **Quiz 10** *(Wed 7 Apr, 13:00 — covers Week 10, ungraded)*

---

## You Already Know How To Store A Bit

**Week 7 gave you the flip-flop, and it works.** It costs about **20 transistors**.

**A gigabit of flip-flops would be 20 billion transistors for the storage alone** — more than most whole processors. **So memory is not built from flip-flops**, and this week is about what it *is* built from, and what each shortcut costs.

---

## The Cost Table That Explains Everything

| cell | transistors/bit | volatile? | needs refresh? |
|---|---:|:-:|:-:|
| **D flip-flop** | ~20 | yes | no |
| **SRAM** (6T) | **6** | yes | no |
| **DRAM** (1T1C) | **1** | yes | **yes** |
| **ROM** (mask) | ~1 | **no** | no |

*(Verified arithmetic.)*

**For one gigabit:**

| | transistors |
|---|---:|
| SRAM | 6 442 450 944 |
| **DRAM** | **1 073 741 824** |

> **DRAM is six times denser than SRAM and about twenty times denser than a flip-flop.** That single
> ratio is why your machine has megabytes of cache and gigabytes of main memory, and it is the whole
> reason the memory hierarchy exists.

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | SRAM and DRAM | Six transistors, or one and a problem |
| **Lecture 2** | Thursday | ROM and Memory Organisation | Decoding, and the array |

---

## SRAM — Week 7's Latch, Shrunk

**Two cross-coupled inverters** — which is Week 7's latch with the NOR gates reduced to the minimum that still holds a bit — **plus two access transistors.** Six in total.

**It holds its value as long as power is applied, needs no refresh, and is fast** (about **1 ns**).

**It is used where speed matters and capacity does not: processor caches and register files.**

---

## DRAM — One Transistor and a Leak

**One transistor and one capacitor.** The bit is *charge on the capacitor*, and the transistor connects it to the bit line.

**The capacitor leaks.** Within milliseconds the charge is gone.

### The refresh arithmetic

**Standard retention is 64 ms, and a typical device has 8192 rows:**

$$\frac{64\text{ ms}}{8192\text{ rows}} = 7.81\ \mu\text{s per row}$$

**Every row must be read and rewritten within that window, forever, or the data evaporates.** At a refresh cycle time of 350 ns:

$$\frac{8192 \times 350\text{ ns}}{64\text{ ms}} = \mathbf{4.5\%} \text{ of the time}$$

*(Verified.)*

> **About one twentieth of DRAM's availability is spent remembering rather than reading.** That is
> the price of the 6× density advantage — and reading a DRAM cell **destroys** it, so every read is
> followed by a write-back.

---

## Organisation — Why Memories Are Square

**A flat decoder for $2^n$ words needs $2^n$ AND gates** *(Week 5)*. For a megabit that is **1 048 576 gates**, which is absurd.

**Split the address: half selects a row, half selects a column.**

| words | flat decoder | square array | saving |
|---:|---:|---:|---:|
| 1 024 | 1 024 | $32\times32$ → 64 | 16× |
| 65 536 | 65 536 | $256\times256$ → 512 | 128× |
| 1 048 576 | 1 048 576 | $1024\times1024$ → **2 048** | **512×** |

*(Verified.)*

**This is why memory chips have a row-address strobe and a column-address strobe**, and why accessing consecutive addresses in the same row is faster than jumping around — **the row is already open.**

---

## ROM Is Week 5's Circuit

**A decoder driving a programmable OR plane** — exactly the "one decoder shared by many OR gates" of Week 5, which was noted then to be a ROM.

**An $n$-bit address by $w$-bit word ROM is $2^n$ decoder lines and $2^n \times w$ programmable bits.** *(Verified.)*

**And it is a lookup table** — the same object as Week 5's mux-based logic and Week 12's FPGA cell.

---

## This Week's Work

1. **Quiz 10** — Wed 7 Apr, covers Week 10. **Ungraded.**
2. **Lab 11** — model the array, compute the refresh budget, build a small ROM.
3. **PS 11** — cell comparison, decoding, refresh arithmetic.

---

*Next: Wednesday — SRAM and DRAM*
