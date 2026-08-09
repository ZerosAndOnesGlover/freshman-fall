# ECE 110 · Digital Logic
## Problem Set 10 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Every behaviour below was produced by running the code in Icarus Verilog 12.0.

---

## Part A (5 pts each)

**A1 (5).** **Because it describes a structure that exists permanently and all at once, not a sequence of steps.**

**Concrete consequence (any one):** a `for` loop replicates hardware rather than iterating; an `if` without an `else` builds a latch; every `assign` and `always` block is active simultaneously and forever.

**A2 (5).** **`reg` means "assigned by a procedural statement", nothing more.** A `reg` inside `always @(*)` synthesises to plain gates with no storage.

**Storage is decided by the clock** — `always @(posedge clk)` — **not by the keyword.**

**A3 (5).** Structural (gate instances — matching a schematic); dataflow (`assign` — combinational); behavioural (`always` — sequential and FSMs).

**A4 (5).** **A full adder chain of the declared width**, with the carry-out concatenated onto the sum.

**The tool is free to choose the adder architecture** — ripple-carry, carry-lookahead, carry-select — guided by the timing constraints. **Weeks 3 and 6 are exactly what it is choosing between.**

---

## Part B (6 pts each)

**B1 (6).** **A latch**, not a mux. With `en=0` nothing is assigned, so `y` must hold — the tool builds storage.

*(Measured: `y` stayed at 1 after `a` changed to 0.)*

**Not what a designer wants.** Fix with a default assignment or an `else`.

**B2 (6).** **In simulation, an AND gate that only re-evaluates when `a` changes** — so changing `b` does nothing *(measured: `b` 0→1 left `y` at 0)*.

**In synthesis, a proper AND gate**, because gates have no sensitivity list.

**Not what a designer wants, and dangerously so:** the two disagree, and **the simulation is the wrong one.**

**B3 (6).** **Blocking in a clocked block.** `q1 = d` takes effect immediately, so `q2 = q1` sees the *new* value, and so does `q3`.

**Result: all three registers load `d` in the same cycle — three flip-flops behaving as one.**

*(Measured: `111` then `000`, against non-blocking's `xx1 → x10 → 100`.)*

**Not what a designer wants** if a shift register was intended.

**B4 (6).** **A correct 3-stage shift register.** Non-blocking evaluates all right-hand sides before assigning, which is what flip-flops do on an edge. *(Measured: the 1 walks through.)*

**This is what a designer wants.**

**B5 (6).** **A 3-to-1 mux with an inferred latch**, because `sel = 2'b11` assigns nothing.

**Fix: add `default: y = a;`** (or any defined value), or assign a default before the `case`.

*Marking B1–B5: 3 for the hardware, 3 for the judgement. **"It assigns y" earns 0** — the question asks what hardware results.*

---

## Part C (6 pts each)

**C1 (6).**

```verilog
module adder #(parameter N = 4)
  (output [N-1:0] sum, output cout, input [N-1:0] a, b, input cin);
  assign {cout, sum} = a + b + cin;
endmodule
```

**C2 (6).**

```verilog
always @(posedge clk or posedge rst)
  if (rst)      q <= 4'b0;
  else if (load) q <= d;
```

**Reset asynchronous, load synchronous, as specified.** *(Note: no `else` is needed here — this is a clocked block, so holding is what a flip-flop does. **The latch trap applies only to `always @(*)`.**)*

*Marking: **award full marks for omitting the final `else`, and flag it in feedback** — students who add one are not wrong, but should know why it is unnecessary.*

**C3 (6).**

```verilog
always @(posedge clk or posedge rst)
  if (rst)          q <= 4'd0;
  else if (q == 4'd9) q <= 4'd0;
  else              q <= q + 1;
```

**C4 (6).** A `case` on `op` with **all eight branches and a `default`.**

**C5 (6).** The three-block idiom, with `next = state;` as the default in the combinational block.

---

## Part D (5 pts each)

**D1 (5).** Testbench sweeping $16\times16\times2 = 512$ combinations.

**The three traps and their avoidance:**
1. **`integer` loop counters** — a 1-bit `reg` wraps and the loop never terminates *(Week 2)*.
2. **Mask the comparison** — compare `{cout,sum}` against the full-width sum, or mask to $N$ bits *(Week 3: 240 false failures)*.
3. **`!==` rather than `!=`** — a comparison involving `x` yields `x`, which is falsy *(Week 1)*.

*Marking: 2 testbench, **3 for naming all three.***

**D2 (5).** **Simulation only re-evaluates the block when a listed signal changes; synthesis produces a gate, which responds to every input.**

$$\textbf{The simulation is the wrong one.}$$

**And that is what makes it dangerous: the testbench passes and the silicon fails**, with nothing in the verification flow able to detect it.

**D3 (5).** **Because a latch is level-sensitive and transparent** *(Week 7)*. An unintended one in a synchronous design creates a timing path that was never analysed, can pass data through within a clock phase, and is a standard cause of designs that simulate correctly and fail on silicon.

**It is a functional defect, not an aesthetic one.**

**D4 (5).** **The tool performed state assignment and derived the next-state and output equations** — Week 9's $D_1=Q_0\overline X+Q_1\overline{Q_0}X$, $D_0=X$, $Y=Q_1Q_0X$ — **by running minimisation equivalent to Week 4's.**

**It might have chosen a different encoding**, most likely **one-hot**, which uses more flip-flops and less logic — cheaper on an FPGA *(Weeks 5, 9)*. **The behaviour is identical; the gates are not.**

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 30 |
| C | 30 |
| D | 20 |
| **Total** | **100** |

---

## The Five Errors To Expect

1. **B-series:** describing what the code *does* rather than what hardware it *becomes*.
2. **C2:** adding an unnecessary `else` in a clocked block, having over-applied the latch rule.
3. **D2:** saying the two "differ" without stating that the simulation is wrong.
4. **D3:** calling inferred latches untidy rather than a functional defect.
5. **D4:** not knowing the tool may re-encode the states.

---

*ECE 110 · Week 10 · PS 10 Solutions · Instructor Only*
