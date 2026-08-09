# ECE 110 · Digital Logic
## Lab 10: Verilog — Simulate, Then Compare With the Hardware
### Week 10 Lab Session

---

**Duration:** 2 hours (Friday 14:00–15:50, MEC 110)
**Format:** Pairs. **Both partners submit their own report.**
**Graded on:** completion + correctness — **100 points**
**Tools:** Icarus Verilog. Breadboard from Week 9 still assembled for Part D.

---

## Overview

**You will write, deliberately break, and then fix the three bugs that every Verilog beginner writes exactly once.**

Then you will describe Week 9's state machine in fifteen lines and confirm it matches the one you built from gates.

> **Parts A–C are about *seeing* the traps rather than being told about them.** Run each broken
> version before fixing it, and record what it actually did.

---

## Part A — Blocking vs Non-Blocking (25 pts)

**A1 (10 pts).** Write **two** 3-stage shift registers, identical except that one uses `<=` and the other `=`:

```verilog
always @(posedge clk) begin
  q[0] <= d; q[1] <= q[0]; q[2] <= q[1];   // and the = version
end
```

**A2 (10 pts).** Drive both from the same clock and the same `d`. Send a single 1 followed by zeros, and **tabulate `q` for both over 6 cycles.**

**A3 (5 pts).** **Explain the difference** in terms of when each assignment takes effect, and state the rule.

---

## Part B — The Inferred Latch (25 pts)

**B1 (10 pts).** Write this and simulate it:

```verilog
always @(*) if (en) y = sel ? b : a;
```

**Set `en=1` and observe `y`. Then set `en=0` and change `a`.** Record what `y` does.

**B2 (8 pts).** **What hardware did you get, and what did you ask for?**

**B3 (7 pts).** Fix it two different ways — a default assignment, and an explicit `else`. **Confirm both behave identically**, and say which you prefer for a `case` with many branches.

---

## Part C — The Sensitivity List (20 pts)

**C1 (8 pts).** Write `always @(a) y = a & b;` and a correct `always @(*)` version. Drive both and **record where they differ.**

**C2 (6 pts).** **Which of the two matches the hardware a synthesis tool would build?**

**C3 (6 pts).** **Why is this the worst of the three traps?** Two sentences.

---

## Part D — The Real Design (30 pts)

**D1 (12 pts).** Write the overlapping `1011` **Mealy** detector using the three-block idiom — state register, next-state `case`, output assignment.

**No hand-derived equations.**

**D2 (10 pts).** Testbench it against a reference over at least 2000 random cycles. **Report cycles and failures.**

> ⚠ **Pulse your reset.** `reg rst = 1;` never produces a `posedge`, so the state stays `x`
> *(Week 9)*.

**D3 (8 pts).** Compare with the gate-level machine you built in Lab 9:

- **Does it behave identically on `1011011011`?**
- **You wrote no equations. What did the tool derive that you derived by hand in Week 9?**
- **Which is shorter to write, and which is easier to check by hand?**

---

## Marking Summary

| Part | Points |
|---|---|
| A — blocking vs non-blocking | 25 |
| B — the inferred latch | 25 |
| C — the sensitivity list | 20 |
| D — the real design | 30 |
| **Total** | **100** |

---

## Submission

Your code — **both the broken and fixed versions** — your recorded tables, and your answers.

> **The broken versions are marked.** Deleting them loses the marks; the point of the lab is the
> evidence.

---

*ECE 110 · Week 10 · Lab 10*
