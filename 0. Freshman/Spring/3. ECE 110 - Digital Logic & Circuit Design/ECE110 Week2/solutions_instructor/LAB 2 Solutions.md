# ECE 110 · Digital Logic
## Lab 2 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** Simulation figures produced by the Python reference below; transistor figures are static-CMOS 2-input counts.

---

> **Revised 2026-09-23.** Verilog is taught in Week 10; this lab's Verilog part is now a Python
> simulation of the same circuit, and the expected counts are unchanged. The reference code below was
> run for this revision (Python 3.14).

## Part A — Gates on the Bench (25 pts)

### A1, A2 (18)

**Standard truth tables**, measured. Marks are for having measured them, not for their content.

*Common wiring faults, in order of frequency: $V_{CC}$/GND swapped or missing (chip warm, outputs dead); LED without its series resistor; DIP switch with no pull-down, so the "0" input is floating rather than low.*

### A3 (7) — the floating input

**Expected observation:** the floating input drifts. The output is **unstable** — it may sit at either level, flicker, or respond to a hand moved near the wire, because the input capacitance is picking up mains hum and body capacitance.

**Tied high through 10 kΩ: stable and correct.**

**Why a floating CMOS input is not a logic 0:** a CMOS input is a **capacitive gate terminal that draws essentially no current**, so nothing pulls it anywhere — it holds whatever charge it happens to have. **It is not "0", it is undefined**, and it can also sit in the forbidden region where both transistors conduct, drawing large current and heating the chip.

*Marking: 3 first observation, 2 second, 2 explanation. **Full marks require "undefined, not low".***

---

## Part B — NAND-Only Rebuilds (30 pts)

| build | expression | NAND gates |
|---|---|---:|
| **NOT** | $A\,\text{NAND}\,A$ | **1** |
| **AND** | $\overline{(A\,\text{NAND}\,B)}$ | **2** |
| **OR** | $\overline A\,\text{NAND}\,\overline B$ | **3** |
| **XOR** | $(A\,\text{NAND}\,X)\,\text{NAND}\,(B\,\text{NAND}\,X)$, $X=A\,\text{NAND}\,B$ | **4** |

**All four verified structurally in the Python simulation: 0 failures over the 4 input combinations.** *(Measured.)*

**B4's shared sub-expression is $X = A\,\text{NAND}\,B$**, wired once and fed to both `g2` and `g3`. **A five-gate build computes it twice.**

*Marking: 8 + 8 + 7 + 7. **For B4, 3 of the 7 are identifying the sharing.** A student with five gates who cannot find the sharing earns 4.*

---

## Part C — Cost, Measured (20 pts)

### C1 (8)

| build | NAND gates | 74HC00 packages | transistors @4/NAND |
|---|---:|---:|---:|
| NOT | 1 | 1 | 4 |
| AND | 2 | 1 | 8 |
| OR | 3 | 1 | 12 |
| XOR | 4 | **1** *(uses all four)* | 16 |

### C2 (6)

| | rebuild | dedicated | verdict |
|---|---:|---:|---|
| NOT | 4 | 2 | more expensive by 2 |
| AND | 8 | 6 | more expensive by 2 |
| OR | 12 | 6 | more expensive by 6 |
| XOR | 16 | 12 | more expensive by 4 |

$$\boxed{\text{Every rebuild costs more. None is cheaper.}}$$

*(Measured.)*

> **The question invites students to look for the cheap cases and there are none.** That is the
> intended surprise, and a student who reports "AND is cheaper" has assumed rather than counted.

*Marking: 6. **Deduct 3 for any claim that some rebuild is cheaper.***

### C3 (6)

**Because transistor count for one isolated gate is not what is being minimised.**

Three reasons, any two for full marks:

1. **Uniformity.** One cell, characterised once, laid out once, verified once. A library with fewer distinct cells is cheaper to design, model and manufacture than one optimised gate by gate.
2. **The inversions cancel in real networks.** The rebuilds above are penalised by a trailing inverter that a *multi-level* circuit absorbs — Week 2's AND-OR → NAND-NAND conversion costs **nothing**, because the added bubbles pair off. **The isolated-gate comparison is the worst case for NAND, not the typical one.**
3. **Regularity suits automation.** Place-and-route and technology mapping are easier over a uniform primitive, which matters far more at scale than 2 transistors per gate.

*Marking: 6. **"It is cheaper" earns 0** — the student has just measured that it is not, and the point of the part is to notice that the obvious answer is contradicted by their own table.*

---

## Part D — The Simulation Cross-Check (25 pts)

### D1 (10)

**Must be built from a `NAND` function only**, wired as on the bench. `return a ^ b` is not a rebuild
and earns 3 of 10.

```python
def NAND(a, b): return 1 - (a & b)
def NOT_(a):    return NAND(a, a)
def AND_(a, b): x = NAND(a, b); return NAND(x, x)
def OR_(a, b):  return NAND(NAND(a, a), NAND(b, b))
def XOR_(a, b): x = NAND(a, b); return NAND(NAND(a, x), NAND(b, x))
```

### D2 (8)

$$\textbf{0 failures over 4 input combinations, all four rebuilds.}$$

*(Run 2026-09-23.)*

### D3 (7)

**All three agree for XOR:** bench measurement, the gate-level simulation, and the truth-table checker from Lab 1.

**On disagreement:** the expected judgement is **trust the bench over the simulation**, because the simulation encodes your intent and the bench encodes what you actually wired — but **first check that the two are testing the same circuit**, since the usual cause is a wiring error rather than a modelling error.

*Marking: 4 for the three verdicts, **3 for the reasoning about which to trust.** Any defensible ordering earns the 3 if it is argued; an unargued preference earns 0.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 30 |
| C | 20 |
| D | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A3 says the floating input is **undefined, not low**
2. **B4 uses 4 gates with $X$ shared**
3. **C2 reports that *every* rebuild is more expensive**
4. C3 does not answer "it is cheaper"
5. **D1 uses `nand` primitives, not `assign`**
6. D2 reports 0 failures
7. D3 argues which tool to trust

---

## Note for the Debrief

> **Last week the algebra said NAND could build anything. Today you built it, and it worked — and it
> cost more transistors every single time.**
>
> **Both facts are true and neither cancels the other.** NAND is universal *and* an isolated NAND
> rebuild is wasteful. **Industry uses NAND anyway, and the reason is not on your transistor table** —
> it is uniformity, and the fact that in a real multi-level circuit the extra inversions cancel
> instead of accumulating.

Then close on the method:

> **You have now checked XOR three ways: by hand on a breadboard, gate by gate in simulation, and as a truth table.** All
> three agreed. **Next week you build something none of you can verify by staring at it** — a 4-bit
> adder, with 512 input combinations — and that is when the habit starts paying for itself.

---

*ECE 110 · Week 2 · Lab 2 Solutions · Instructor Only*
