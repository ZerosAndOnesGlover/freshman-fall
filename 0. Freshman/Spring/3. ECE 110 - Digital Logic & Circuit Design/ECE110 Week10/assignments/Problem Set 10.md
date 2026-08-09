# ECE 110 · Digital Logic
## Problem Set 10
### Topic: Verilog — Combinational and Sequential Description
**Released:** Thursday, Week 10 · **Due:** Thursday, Week 11 at the start of class

---

> **For every code fragment, say what hardware it becomes.** "It assigns y" is not an answer;
> "an AND gate" is.
>
> **All design code must be synthesisable.** If you cannot name the gates, do not write it.

---

## Part A — The Model (5 pts each)

**A1.** **Why is Verilog a description language rather than a programming language?** Give one concrete consequence.

**A2.** What does `reg` actually mean? **What decides whether you get a flip-flop?**

**A3.** Name the three description styles, with a one-line example of each and when to use it.

**A4.** `assign {cout, sum} = a + b + cin;` — **what hardware does this build**, and what is the tool free to choose?

---

## Part B — Reading Code (6 pts each)

**For each, say what hardware results and whether it is what a designer would want.**

**B1.**
```verilog
always @(*) if (en) y = d;
```

**B2.**
```verilog
always @(a) y = a & b;
```

**B3.**
```verilog
always @(posedge clk) begin
  q1 = d; q2 = q1; q3 = q2;
end
```

**B4.**
```verilog
always @(posedge clk) begin
  q1 <= d; q2 <= q1; q3 <= q2;
end
```

**B5.**
```verilog
always @(*) begin
  case (sel)
    2'b00: y = a;
    2'b01: y = b;
    2'b10: y = c;
  endcase
end
```

---

## Part C — Writing Code (6 pts each)

**C1.** A parameterised $N$-bit adder with carry-in and carry-out.

**C2.** A 4-bit register with synchronous load enable and asynchronous reset.

**C3.** A 4-bit synchronous counter with a mod-10 wrap.

**C4.** The 8-operation ALU of Week 6, using a `case`.

**C5.** The overlapping `1011` Mealy detector of Week 9, using the three-block idiom.

---

## Part D — Verification and Synthesis (5 pts each)

**D1.** Write a testbench for C1 at $N=4$ sweeping all 512 input combinations. **Name the three testbench traps this course has already hit and say how you avoided each.**

**D2.** **Why does an incomplete sensitivity list make simulation and silicon disagree?** Which one is wrong?

**D3.** **Why are inferred latches serious rather than merely untidy?** Refer to Week 7.

**D4.** You wrote C5 without deriving any equations. **What did the synthesis tool do that you did by hand in Week 9, and what might it have chosen differently?**

---

## Marking Summary

| Part | Problems | Points |
|---|---|---|
| A — the model | 4 × 5 | 20 |
| B — reading code | 5 × 6 | 30 |
| C — writing code | 5 × 6 | 30 |
| D — verification and synthesis | 4 × 5 | 20 |
| **Total** | | **100** |

---

*ECE 110 · Problem Set 10 · due Thursday of Week 11*
