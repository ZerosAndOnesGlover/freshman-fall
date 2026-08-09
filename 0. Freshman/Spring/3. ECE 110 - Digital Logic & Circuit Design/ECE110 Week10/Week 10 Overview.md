# ECE 110 · Digital Logic
## Week 10 · Overview
### VHDL/Verilog — Hardware Description Languages

---

**Topic:** how this is written down at scale
**Reading:** Harris & Harris §4.1–4.6 | Mano & Ciletti §3.9, §5.8
**Assessment this week:** PS 10, Lab 10, **Quiz 9** *(Wednesday — covers Week 9, ungraded)*

---

## Why A Language

**You have drawn every circuit in this course by hand. That stops working at about a hundred gates, and a modern chip has billions.**

**A hardware description language lets you write the design as text**, and a **synthesis** tool turns the text into gates — running, among other things, the minimisation of Week 4 and the state encoding of Week 9.

> **You have been using Verilog since Week 1** as a checking tool. This week it becomes the design
> medium, and the emphasis changes completely: **code that simulates correctly and code that
> synthesises correctly are not the same set.**

---

## The Sentence To Keep

> **Verilog is a *description* language, not a programming language.**

**You are not telling the machine what to do in sequence. You are describing a structure that exists all at once**, and the tool builds it.

**Every trap in this week comes from forgetting that.** A `for` loop does not loop — it replicates hardware. An `if` without an `else` does not "do nothing" — **it builds a latch to remember the old value.**

---

## The Two Lectures

| | Day | Topic | The point |
|---|---|---|---|
| **Lecture 1** | Wednesday | Describing Hardware, Not Programming It | Modules, the three styles, `wire` vs `reg` |
| **Lecture 2** | Thursday | Sequential Verilog and the Classic Traps | The three bugs everyone writes once |

---

## Three Styles, One Circuit

| style | looks like | use for |
|---|---|---|
| **structural** | gate instances wired together | matching a schematic exactly |
| **dataflow** | `assign y = (a & b) | c;` | combinational logic |
| **behavioural** | `always @(posedge clk)` | sequential logic, FSMs |

**All three synthesise.** You have written structural Verilog in every lab since Week 2; this week adds the other two.

---

## The Three Traps, Measured

**Each of these was run, and each produced the failure shown.**

### 1. Blocking vs non-blocking

**A three-stage shift register, written both ways:**

| cycle | `<=` non-blocking | `=` blocking |
|:-:|:-:|:-:|
| 0 | `xx1` | `111` |
| 1 | `x10` | `000` |
| 2 | `100` | `000` |

*(Measured.)*

**Non-blocking gives a real shift register — the 1 walks through. Blocking makes all three bits take $d$ in the same cycle**, collapsing three flip-flops into one.

$$\textbf{Rule: } \texttt{<=} \textbf{ in sequential blocks, } \texttt{=} \textbf{ in combinational ones.}$$

### 2. The inferred latch

```verilog
always @(*) if (en) y = sel ? b : a;    // no else
```

**With `en=0` the output *holds its previous value*.** *(Measured: `y` stayed at 1 even after its inputs changed.)*

**You asked for a mux and got a latch** — and Week 7 explained why an unintended latch is a serious problem.

**Fix: assign a default before the `if`.**

### 3. The incomplete sensitivity list

```verilog
always @(a) y = a & b;    // b is missing
```

**Simulation obeys the list: changing `b` does nothing.** *(Measured.)* **Synthesis ignores the list and builds a proper AND gate.**

> **The chip and the simulation then disagree**, which is the worst class of bug in the subject:
> your testbench passes and the hardware is wrong. **Always write `always @(*)`.**

---

## This Week's Work

1. **Quiz 9** — Wednesday, covers Week 9. **Ungraded.**
2. **Lab 10** — write it, simulate it, then compare against the real chips.
3. **PS 10** — combinational and sequential description, and finding the traps.

---

*Next: Wednesday — Describing Hardware, Not Programming It*
