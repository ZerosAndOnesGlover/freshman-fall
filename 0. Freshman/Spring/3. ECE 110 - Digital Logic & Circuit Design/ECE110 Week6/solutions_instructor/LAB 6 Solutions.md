# ECE 110 · Digital Logic
## Lab 6 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures from running the lab in Icarus Verilog 12.0 and Python.

---

## Part A — The ALU (35 pts)

### A1 (12), A2 (12), A3 (11)

**Reference implementation:** structural ripple-carry adder from Week 3 full adders; behavioural bitwise units; behavioural output mux; flags from the carries.

**A3 is the part with teeth.** Subtraction **must** reuse the adder via the Week 3 XOR trick — `SUB` driving both the $B$-input XORs and the least significant carry-in.

*Marking A3: 11 for reuse. **A second adder instance, or a behavioural `A - B` in the datapath, caps this part at 5** — the whole point is that the hardware is already there.*

> **$V$ must come from $C_3\oplus C_4$.** A student computing it by comparing against a wider result
> has verified their own assumption rather than built a flag, and loses A2's marks even if the value
> is right.

---

## Part B — All 2048 (25 pts)

### B1 (15)

$$\textbf{2048 cases (8 opcodes × 16 × 16), 0 failures.}$$

*(Measured, Icarus Verilog 12.0; matches the Python model exactly.)*

> ⚠ **The width trap again.** Comparing a 4-bit result against an unmasked `A - B` reports mass
> false failures. **This is the third lab in which the testbench, not the circuit, was the thing that
> broke** — Lab 2's 1-bit loop counter, Lab 3's 240 phantom failures, and now this. **Say so.**

### B2 (10)

$$\textbf{256 signed pairs, 0 failures}$$ for $V$ on the ADD operation, checked with `$signed()`. *(Measured.)*

---

## Part C — Timing (25 pts)

### C1 (10)

**The critical path is an arithmetic operation** — ADD or SUB — **ending at $C_{out}$ (or at $V$, one XOR later).**

**For the 4-bit ripple version: 9 gate delays to $C_{out}$**, plus the output mux. *(Measured in Week 3; unchanged here.)*

**The logic operations are 1 gate deep** and never on the critical path. **This is why the adder is the only part of an ALU anyone optimises.**

### C2 (8)

| $N$ | gate delays | at 20 ps |
|---:|---:|---:|
| 8 | 17 | 0.34 ns |
| 16 | 33 | 0.66 ns |
| 32 | 65 | 1.30 ns |
| 64 | 129 | 2.58 ns |

### C3 (7)

**Ripple at 64 bits: $2.58/0.333 = \mathbf{7.75}$ clock periods — does not fit.**

**Hierarchical CLA at 64 bits: 12 gate delays $= 0.24$ ns $= \mathbf{0.72}$ periods — fits, with about 28% margin.**

*(Both measured.)*

*Marking: 4 ripple with the number, 3 CLA with the margin. **A verdict without the arithmetic earns half.***

---

## Part D — On the Bench (15 pts)

### D1 (10)

One bit slice of the logic unit: 74HC08, 74HC32, 74HC86, 74HC04 feeding a 74HC153 4:1 mux. **All four operations verify.**

### D2 (5)

**4-bit logic unit:** 4 slices — one package each of AND/OR/XOR/NOT (each holds 4 gates) plus two dual-4:1 mux packages. **About 6 packages.**

**32-bit:** 8 packages of each logic type plus 16 mux packages — **roughly 48 packages**, which is the honest reason nobody builds a 32-bit ALU from 74HC parts.

*Marking: 3 + 2. **Accept any reasonable package arithmetic**; the point is the scaling.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 35 |
| B | 25 |
| C | 25 |
| D | 15 |
| **Total** | **100** |

---

## Checkoff Checklist

1. **A3: subtraction reuses the adder**
2. **A2: $V$ comes from the carries**
3. B1 reports 2048 cases, 0 failures
4. B2 reports 256 signed pairs, 0 failures
5. **C1 identifies an arithmetic op as the critical path**
6. **C3 gives 7.75 and 0.72 with a verdict**
7. D2's package arithmetic scales sensibly

---

## Note for the Debrief

**Short, because the midterm is this week. Two points.**

> **You have built the part of a processor that computes** — and it is an adder, four gates and a
> mux. **Nothing in it was invented today.** Weeks 0 and 3 gave you the arithmetic, Week 1 the XOR
> trick, Week 5 the mux. **A large part of engineering is assembly, and noticing that the shift and
> the comparison were already free.**

Then close the arc that has run since Week 2:

> **Week 2 said gate count is area and critical path is speed. Week 3 built something cheap in area
> and unusable in time. Week 4 made things smaller and did nothing for speed. This week you spent
> area to buy speed on purpose: 2× the gates for a 10.8× shorter path**, and that is the difference
> between an adder that fits in a 3 GHz clock period and one that needs 7.7 of them.
>
> **You measured every one of those numbers yourselves.**

Then: **the midterm covers Weeks 0–5, not this week.** Revision guide is in `resources/`.

---

*ECE 110 · Week 6 · Lab 6 Solutions · Instructor Only*
