# ECE 110 · Digital Logic
## Week 11 · Lecture 2 (Thursday)
### ROM and Memory Organisation

---

**Reading:** Harris & Harris §5.5.3–5.5.6 | Mano & Ciletti §7.4–7.5
**PS 11** released today, due Thursday of Week 12.

---

## 1. ROM Is A Circuit You Already Designed

**A read-only memory is a decoder driving a programmable OR plane.**

**That is precisely Week 5's observation**: one decoder shared by many OR gates gives you $m$ functions of the same $n$ inputs cheaply — **and it was noted then that this arrangement is a ROM.**

| ROM | size |
|---|---|
| $n$-bit address, $w$-bit word | $2^n$ decoder lines, $2^n\times w$ programmable bits |

**For $n=10$, $w=8$: 1024 word lines and 8192 stored bits.** *(Verified.)*

### It is also a lookup table

**Address in, stored word out, no computation.** **The same object as Week 5's mux-based logic and next week's FPGA cell** — and, once again, **its cost does not depend on the function stored in it.**

> **Three times now the course has arrived at the lookup table from different directions:** as a
> multiplexer with constants on its data inputs, as a decoder with an OR plane, and next week as an
> FPGA's basic cell. **They are one idea.**

### The variants

| | programmed | erasable |
|---|---|---|
| **Mask ROM** | at manufacture | no |
| **PROM** | once, by the user | no |
| **EPROM** | electrically | UV light |
| **EEPROM / Flash** | electrically | **electrically** |

**Flash is how firmware and SSDs work**, and it is non-volatile — the one row in this week's table that survives a power cut.

---

## 2. The Array

**Memory is not a long row of cells. It is a square.**

**A flat decoder for $2^n$ words needs $2^n$ AND gates.** For a megabit that is over a million gates **to address** a million bits — the decoder would cost more than the storage.

**So split the address in half.** Half selects a **row**; half selects a **column** through a multiplexer.

| words | flat | square | saving |
|---:|---:|---:|---:|
| 1 024 | 1 024 | $32\times32$ → 64 | 16× |
| 65 536 | 65 536 | $256\times256$ → 512 | 128× |
| 1 048 576 | 1 048 576 | $1024\times1024$ → **2 048** | **512×** |

*(Verified.)*

> **The saving grows with size**, which is why every memory ever built is organised this way — and
> why memory chips have a **row address strobe** and a **column address strobe** rather than one wide
> address bus.

---

## 3. Why Sequential Access Is Faster

**Reading a DRAM location has two phases: open the row, then select the column.**

**If the next access is in the *same row*, the row is already open** and only the column select is needed — several times faster.

> **This is the hardware fact underneath every "locality of reference" argument you will meet in CS
> 201**, and underneath the advice to traverse arrays in memory order. **The row buffer is why
> sequential access is fast, and it is a consequence of the square array**, which is itself a
> consequence of the decoder cost above.

---

## 4. Memory Interfaces

**A memory block's ports:**

| | |
|---|---|
| **address** | $n$ lines |
| **data** | $w$ lines, often bidirectional |
| **chip select** | enables this device — from a decoder *(Week 5)* |
| **write enable** | write when asserted, read otherwise |
| **output enable** | drive the data bus, or float |

**Bidirectional data buses need three-state buffers** — a driver that can be electrically disconnected, so many devices can share the wires with exactly one driving at a time.

> **A three-state output is not a third logic value.** It is *no* value — the driver is off. **Two
> devices driving the same bus simultaneously is a short circuit**, which is why the chip-select
> decoding must guarantee that never happens.

---

## 5. Building Bigger Memories

**Wider words:** put chips side by side, sharing address and control, each supplying some bits.

**More words:** stack chips, using a decoder on the high address bits to generate chip selects.

**Both are Week 5's blocks doing the obvious thing** — and this is exactly how a memory module is built from individual devices.

---

## 6. What To Take From This Lecture

1. **A ROM is a decoder plus a programmable OR plane** — Week 5's shared-decoder circuit.
2. **$2^n$ lines, $2^n\times w$ stored bits.**
3. **A ROM is a lookup table**, the third route the course has taken to the same idea.
4. **Flash is the non-volatile one**, and how firmware and SSDs work.
5. **Memories are square** because a flat decoder costs $2^n$ gates — 512× saving at a megabit.
6. **Hence row and column strobes**, and hence sequential access is faster.
7. **Bidirectional buses need three-state buffers**, and a three-state output is *no* value, not a third one.
8. **Wider and deeper memories are built with Week 5's decoders and multiplexers.**

---

*Next: Friday — Lab 11, memory timing and refresh*
