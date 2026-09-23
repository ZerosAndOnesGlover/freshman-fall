# ECE 110 · Digital Logic
## Lab 6 — Solutions and Checkoff Notes
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All figures from running the lab in Python.

---

> **Revised 2026-09-23.** Verilog is taught in Week 10; this lab's Verilog part is now a Python
> simulation of the same circuit, and the expected counts are unchanged. The reference code below was
> run for this revision (Python 3.14).

## Part A — The ALU (35 pts)

### A1 (12), A2 (12), A3 (11)

**Reference implementation:** structural ripple-carry adder from Lab 3's full adders; bitwise units on
single bits; output selection by opcode; flags from the carries.

```python
def alu(op, a, b):                       # a, b: ints 0..15; bits() / val() convert to and from bit lists
    A, B = bits(a), bits(b)
    if op in (0, 1):                     # ADD / SUB share one adder: SUB inverts B and sets carry-in
        s, cout, carries = add4(A, [x ^ op for x in B], op)
        r, C, V = val(s), cout, carries[3] ^ carries[4]
    elif op == 7:                        # A < B (unsigned): no carry out of A + ~B + 1
        s, cout, carries = add4(A, [1 - x for x in B], 1)
        r, C, V = 1 - cout, 0, 0
    else:
        r = val({2: [x & y for x, y in zip(A, B)], 3: [x | y for x, y in zip(A, B)],
                 4: [x ^ y for x, y in zip(A, B)], 5: [1 - x for x in A],
                 6: [0] + A[:3]}[op])
        C, V = (A[3] if op == 6 else 0), 0
    return r, C, V, int(r == 0), (r >> 3) & 1          # result, C, V, Z, N
```

(`add4` here also returns the list of internal carries, so that $V = C_3 \oplus C_4$.)

**A3 is the part with teeth.** Subtraction **must** reuse the adder via the Week 3 XOR trick — `SUB` driving both the $B$-input XORs and the least significant carry-in.

*Marking A3: 11 for reuse. **A second adder, or Python's `a - b` in the datapath, caps this part at 5** — the whole point is that the hardware is already there.*

> **$V$ must come from $C_3\oplus C_4$.** A student computing it by comparing against a wider result
> has verified their own assumption rather than built a flag, and loses A2's marks even if the value
> is right.

---

## Part B — All 2048 (25 pts)

### B1 (15)

$$\textbf{2048 cases (8 opcodes × 16 × 16), 0 failures.}$$

*(Run 2026-09-23.)*

> ⚠ **The width trap again.** Comparing a 4-bit result against an unmasked `a - b` reports mass
> false failures. **This is the second lab in which the test, not the circuit, was the thing that
> broke** — Lab 3's 256 phantom failures, and now this. **Say so.**

### B2 (10)

$$\textbf{256 signed pairs, 0 failures}$$ for $V$ on the ADD operation, checked against true signed sums
(64 of the 256 pairs overflow). *(Run 2026-09-23.)*

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
