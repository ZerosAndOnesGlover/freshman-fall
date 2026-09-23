# ECE 110 · Digital Logic
## Lab 3 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures produced by running the lab in Python.

---

> **Revised 2026-09-23.** Verilog is taught in Week 10; this lab's Verilog part is now a Python
> simulation of the same circuit, and the expected counts are unchanged. The reference code below was
> run for this revision (Python 3.14).

## Part A — One Full Adder (25 pts)

### A1 (10), A2 (10)

**Half adder:** $S=A\oplus B$, $C=AB$ — 2 gates.
**Full adder:** two half adders plus an OR — **5 gates** (2 XOR, 2 AND, 1 OR).

**All 8 rows satisfy $S+2C_{out} = A+B+C_{in}$.** *(Verified.)*

### A3 (5)

**One 74HC86, one 74HC08, one 74HC32** — three packages for one full adder, using 2 of 4 XORs, 2 of 4 ANDs and 1 of 4 ORs.

> **Worth pointing out on the bench:** a single full adder wastes most of three packages. **Four full
> adders fit in the same three packages** (8 XOR needs two 74HC86s, so four packages total for the
> 4-bit adder) — which is why students should wire Part B before tearing down Part A.

*Marking: 5. **Package count, not just gate count**, is what is being asked.*

---

## Part B — Four Bits (25 pts)

### B1 (12), B2 (8)

| $A$ | $B$ | $C_{in}$ | result |
|---|---|---|---|
| 0011 | 0101 | 0 | **01000** |
| 1111 | 0001 | 0 | **10000** |
| 1010 | 0101 | 0 | **01111** |
| 1111 | 1111 | 1 | **11111** |

*(All verified.)*

**Row 2 is the full-ripple case** — the carry crosses all four stages.

### B3 (5)

$$\frac{4}{512} = 0.0078 = \mathbf{0.78\%}$$

**What passing them entitles you to conclude: that the adder is not broken in those four ways.**

**Nothing more.** It does not establish correctness — 508 combinations are untested, and a wiring fault affecting only, say, bit 2's carry when $A_2=B_2=0$ would pass all four of these.

*Marking: 2 fraction, **3 for the epistemics.** "It probably works" earns 1; the answer must say what has and has not been established.*

---

## Part C — All 512, In Simulation (25 pts)

### C1 (12)

**Must be structural** — gate functions composed into half adders, full adders and the chain. **An adder
that returns `a + b + cin` internally earns 3 of 12**: it tests Python's adder, not the student's.

```python
def XOR(a, b): return a ^ b
def AND(a, b): return a & b
def OR(a, b):  return a | b
def half(a, b):     return XOR(a, b), AND(a, b)
def full(a, b, c):
    s1, c1 = half(a, b); s, c2 = half(s1, c); return s, OR(c1, c2)
def add4(a, b, cin):                 # a, b: lists of 4 bits, least significant first
    s, c = [], cin
    for i in range(4):
        si, c = full(a[i], b[i], c); s.append(si)
    return s, c
```

### C2 (8)

$$\textbf{512 cases, 0 failures}$$ comparing `cout*16 + sum` against `a + b + cin`. *(Run 2026-09-23.)*

> ⚠ **The width trap in the lab text is real.** Comparing the 4-bit `sum` alone against the unmasked
> `a + b + cin` reports **256 failures out of 512** — every case whose total reaches 16 — on a circuit
> that is entirely correct. **The test is what is wrong**, not the circuit.
>
> **This is the single most valuable thing in the lab.** Expect it in submissions, and when a student
> reports mass failures, have them check the comparison width *before* they rewire anything.

### C3 (5)

**All four bench rows appear in the 512 with identical results.** *(Verified.)*

*Marking: 5. **The confirmation must be explicit**, not assumed.*

---

## Part D — Timing (25 pts)

### D1 (10)

**One unit per gate**, inputs at $t=0$:

| output | arrives |
|---|---:|
| $S_0$ | 2 |
| $C_1$ | 3 |
| $S_1$ | 4 |
| $C_2$ | 5 |
| $S_2$ | 6 |
| $C_3$ | 7 |
| $S_3$ | **8** |
| $C_{out}$ | **9** |

*(Measured.)*

$$\textbf{Critical path} = \mathbf{9} \text{ gate delays, ending at } C_{out}.$$

### D2 (8)

**Stage 0's carry needs 3** (its inputs must clear the first XOR before the AND-OR). **Each further stage adds 2** ($C_{in}\to C_{out}$ skips the first XOR). **The final sum bit adds 1** after its carry arrives.

$$t = 3 + 2(N-1) = 2N+1$$

| $N$ | predicted | measured |
|---:|---:|---:|
| 2 | 5 | **5** |
| 3 | 7 | **7** |
| 4 | 9 | **9** |

*(Verified — and the formula also holds at $N = 8, 16, 32, 64$.)*

### D3 (7)

| $N$ | gates | delays | at 20 ps |
|---:|---:|---:|---:|
| 8 | 40 | 17 | 0.34 ns |
| 16 | 80 | 33 | 0.66 ns |
| 32 | 160 | 65 | 1.30 ns |
| **64** | **320** | **129** | **2.58 ns** |

*(Measured.)*

$$\frac{2.58\text{ ns}}{0.333\text{ ns}} = \mathbf{7.7 \text{ clock periods}}$$

**So: no.** A 64-bit ripple-carry adder cannot be used in a 3 GHz processor — **one addition would take nearly eight cycles**, and the adder is on the critical path of almost every instruction.

*Marking: 4 table, **3 for the 7.7 and a plain verdict.** A student who tabulates the nanoseconds but does not divide by the clock period earns 4 of 7 — the comparison is the answer.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 25 |
| B | 25 |
| C | 25 |
| D | 25 |
| **Total** | **100** |

---

## Checkoff Checklist

1. A2 checks $S+2C_{out}$ on all 8 rows
2. **B3 says 0.78% and states what it does *not* establish**
3. **C1 is structural, not `assign a+b`**
4. C2 reports 512 cases, 0 failures
5. C3 confirms bench and simulation agree
6. **D1 gives 9 gate delays with $C_{out}$ on the critical path**
7. D2 derives $2N+1$ and checks it at three widths
8. **D3 divides by the clock period and gives a verdict**

---

## Note for the Debrief

**Two things to close on, and the second is the important one.**

> **Your bench test passed four cases out of 512 — 0.78%.** The simulation passed all of them.
> **Neither of those is "I checked it".** The first is a smoke test and the second is a proof, and
> knowing which you have is most of engineering judgement.

Then the real lesson:

> **An unmasked comparison reports 256 failures out of 512 on this circuit, which is completely
> correct.** The comparison was 4 bits wide on one side and unbounded on the other.
>
> **The answer was that the *test* was broken** — not the design. **When your checker fires, suspect
> the checker first.**

Then set up Week 6:

> **You built something correct today and measured that it is unusable at 64 bits — 7.7 clock
> periods for one addition.** The gates are cheap; the *dependency chain* is not.
>
> **Week 4 teaches you to make circuits smaller. Week 6 teaches you to make this one faster**, by
> computing every carry at once instead of passing it along. **You now know why that is worth doing.**

---

*ECE 110 · Week 3 · Lab 3 Solutions · Instructor Only*
