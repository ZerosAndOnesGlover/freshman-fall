# ECE 110 · Digital Logic
## Lab 10 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every table below was produced by running the code in Icarus Verilog 12.0.

---

## Part A — Blocking vs Non-Blocking (25 pts)

### A1 (10), A2 (10)

**Single 1 followed by zeros:**

| cycle | `d` | `<=` non-blocking | `=` blocking |
|:-:|:-:|:-:|:-:|
| 0 | 1 | `xx1` | `111` |
| 1 | 0 | `x10` | `000` |
| 2 | 0 | `100` | `000` |
| 3 | 0 | `000` | `000` |

*(Measured.)*

**The `x`s in the non-blocking column are correct and expected** — the upper stages have not been loaded yet. **A student who "fixes" them with an `initial` block has removed evidence.**

### A3 (5)

**Non-blocking evaluates every right-hand side first, then performs all the assignments together** — which is exactly what a bank of flip-flops does on a clock edge.

**Blocking takes effect immediately**, so `q[1] = q[0]` reads the value just written, and `q[2] = q[1]` likewise. **All three stages load `d` in the same cycle.**

$$\texttt{<=} \text{ sequential} \qquad \texttt{=} \text{ combinational}$$

*Marking: 5. **The explanation must be about *when* the assignment takes effect.***

---

## Part B — The Inferred Latch (25 pts)

### B1 (10)

| $a$ | $b$ | $sel$ | $en$ | $y$ |
|:-:|:-:|:-:|:-:|:-:|
| 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | **0** | **1** ← held |
| **0** | 0 | 0 | 0 | **1** ← still held |

*(Measured — the output did not follow its input.)*

### B2 (8)

**Asked for: a multiplexer.** **Got: a multiplexer plus a latch**, because nothing is assigned when `en=0`, so `y` must retain its old value.

### B3 (7)

**Both fixes give `y=0` when `en=0`, and both behave identically.** *(Verified.)*

**For a `case` with many branches, the default-assignment form is preferred** — one line covers every unlisted branch, whereas an `else` on each `if` must be repeated and is easy to miss.

---

## Part C — The Sensitivity List (20 pts)

### C1 (8)

| $a$ | $b$ | `always @(a)` | `always @(*)` |
|:-:|:-:|:-:|:-:|
| 1 | 0 | 0 | 0 |
| 1 | **1** | **0** | **1** |

*(Measured — changing `b` alone had no effect on the incomplete version.)*

### C2 (6)

**`always @(*)`.** **Synthesis ignores the sensitivity list entirely** and builds an AND gate, which responds to both inputs. **The incomplete version's *simulation* is what does not match the hardware.**

### C3 (6)

**Because the failure is invisible to verification.** The other two traps produce wrong behaviour in simulation, so a testbench catches them. **This one produces wrong behaviour only in the chip** — the testbench passes, and nothing in the flow reports a problem.

*Marking: 6. **Full marks require the point that the testbench passes.***

---

## Part D — The Real Design (30 pts)

### D1 (12)

**Three-block idiom** with `next = state;` as the default. **No hand-derived equations.**

### D2 (10)

$$\textbf{2000+ cycles, 0 failures.}$$

*(Measured — 4000 cycles in the reference run.)*

> ⚠ **The reset bug again.** `reg rst = 1;` with `always @(posedge ... or posedge rst)` never fires,
> leaving the state `xx`. **Expect a handful of submissions reporting failures only in the first
> cycles with `x` in the output.** That is the symptom; the fix is to pulse the reset.

### D3 (8)

**Identical behaviour on `1011011011`: both give `0001001001`.** *(Verified.)*

**What the tool derived:** the state assignment and the next-state and output equations — Week 9's $D_1 = Q_0\overline X + Q_1\overline{Q_0}X$, $D_0 = X$, $Y = Q_1Q_0X$ — **by running a minimisation equivalent to Week 4's.**

**Shorter to write: the Verilog, decisively.** **Easier to check by hand: the gate-level version**, because you can trace two flip-flops and five literals, whereas the Verilog's actual gates are whatever the tool chose and may not be those equations at all.

*Marking: 3 + 3 + 2. **The last point — that the tool's output may differ from your hand derivation — is the one worth having.***

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 25 |
| C | 20 |
| D | 30 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **Both broken and fixed versions submitted**
2. A2's table shows `111`/`000` for blocking
3. A3 explains *when* assignments take effect
4. **B1 shows `y` held after its input changed**
5. B3 prefers the default form for many-branch `case`
6. **C3 says the testbench passes**
7. D2 reports cycles and failures
8. **D3 notes the tool's gates may differ from the hand derivation**

---

## Note for the Debrief

**Open on Part C, because it is the one that should frighten them.**

> **Two of today's three bugs showed up in simulation, so a testbench would catch them.** The third
> did not. **The incomplete sensitivity list simulates wrongly and synthesises correctly** — your
> testbench passes, and the chip is a different circuit from the one you verified.
>
> **There is nothing in your verification flow that can find that.** The fix is one character:
> `always @(*)`.

Then the week's real content:

> **In Part D you wrote fifteen lines and got the machine you spent Week 9 deriving by hand.** The
> tool did the state assignment, the K-maps and the minimisation — **and it may well have picked a
> different encoding from yours, with entirely different gates.**
>
> **That is not a reason to regret Week 9.** It is the reason Week 9 came first: **you can read what
> the tool produced, judge whether it is sensible, and know what to do when it is not.** Someone who
> has only ever written the `case` statement cannot.

Then set up Week 11:

> **You have described logic. Next week: where the bits actually live** — and you will find that the
> memory cell you meet on Monday is Week 7's latch, shrunk until almost nothing is left of it.

---

*ECE 110 · Week 10 · Lab 10 Solutions · Instructor Only*
