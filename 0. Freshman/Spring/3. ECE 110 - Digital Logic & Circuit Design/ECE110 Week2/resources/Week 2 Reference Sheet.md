# ECE 110 · Digital Logic
## Week 2 · Reference Sheet
### Logic Gates and Functional Completeness

---

## The Seven Gates

| gate | expression | 1 when | CMOS transistors |
|---|---|---|---:|
| NOT | $\overline A$ | input is 0 | **2** |
| NAND | $\overline{AB}$ | not both 1 | **4** |
| NOR | $\overline{A+B}$ | neither is 1 | **4** |
| AND | $AB$ | both 1 | 6 |
| OR | $A+B$ | at least one 1 | 6 |
| XOR | $A\oplus B$ | inputs differ | 12 |
| XNOR | $\overline{A\oplus B}$ | inputs agree | 12 |

$$\text{AND} = \text{NAND} + \text{NOT} = 4+2 = 6 \;>\; \text{NAND}$$

> **CMOS makes inverting gates the cheap primitives.** The algebra's primitives (AND, OR, NOT) are
> not silicon's (NAND, NOR).

---

## The Digital Abstraction

$$V<V_{IL}\Rightarrow 0 \qquad V>V_{IH}\Rightarrow 1 \qquad \text{between} \Rightarrow \textbf{forbidden}$$

$$NM_H = V_{OH}-V_{IH} \qquad NM_L = V_{IL}-V_{OL}$$

**Every gate *restores* the signal**, so noise is discarded rather than accumulated. **That is why digital circuits can be 100 gates deep and analogue chains cannot.**

**A floating CMOS input is undefined, not 0.** It draws no current, so nothing pulls it anywhere; it can also sit in the forbidden region and overheat the chip. **Always tie unused inputs.**

---

## Fan-In, Fan-Out, Delay

- **Fan-in** — inputs per gate. Wide gates stack transistors and are slow; libraries stop near 4.
- **Fan-out** — loads driven by one output. More load, more capacitance, more delay.
- **$t_{pd}$** — input change to stable output.
- **Critical path** — the *longest* path through the circuit. **The circuit's delay is its critical path, not its gate count.**

| $F=ABCD$ | gates | critical path |
|---|---:|---:|
| chain $((AB)C)D$ | 3 | **3** |
| tree $(AB)(CD)$ | 3 | **2** |

> **Gate count is area. Critical path is speed.** Same area, different speed.

---

## Functional Completeness

> **Complete = every Boolean function is realisable from that set alone.**

### Complete

$$\overline A = A\,\text{NAND}\,A \qquad AB = \overline{(A\,\text{NAND}\,B)} \qquad A+B = \overline A\,\text{NAND}\,\overline B$$

**and dually for NOR.** *(all verified in Python and Verilog)*

| built from NAND | gates |
|---|---:|
| NOT | 1 |
| AND | 2 |
| OR | 3 |
| NOR | 4 |
| **XOR** | **4** |

### Not complete — two impossibility proofs

**$\{$AND, OR$\}$: monotonicity.** AND and OR are monotone, composition preserves monotonicity, NOT is not monotone. **So NOT is unbuildable.**

**$\{$NOT, XOR$\}$: affineness.** Both are affine ($c_0\oplus c_1x_1\oplus\cdots$), composition preserves affineness, AND is not affine. **So AND is unbuildable.**

**$\{$XOR, AND$\}$: depends on constants.** With 1 available, $\overline A=A\oplus1$ makes it complete. Without, every composition maps all-zeros to 0, so NOT is unbuildable.

*(all verified)*

> **Both proofs have the same shape: find a property closed under composition, exhibit a target
> lacking it.** That is what an impossibility proof looks like.

---

## Converting to NAND-Only

$$F = AB+CD = \big(\overline{AB}\big)\,\text{NAND}\,\big(\overline{CD}\big)$$

**Any two-level SOP becomes NAND-NAND: replace every AND with NAND, the OR with NAND, done.** Same gate count, same levels — **the conversion is free**, because the added bubbles cancel in pairs.

**Dually, any two-level POS becomes NOR-NOR.** *(both verified)*

---

## Minimum Gate Counts

| | NAND | NOR |
|---|---:|---:|
| XOR | **4** | 5 |
| XNOR | 5 | **4** |
| the other's gate | 4 | 4 |

*(true minima, by exhaustive search over all constructions up to 8 gates)*

> **XOR is cheaper in NAND; XNOR in NOR, by the same margin — Week 1's duality, priced in silicon.**

**XOR transistors:** 4 NAND = **16**; 2 NOT + 2 AND + 1 OR = **22**.

**But an isolated rebuild always loses to a dedicated gate:**

| | rebuild | dedicated |
|---|---:|---:|
| NOT | 4 | 2 |
| AND | 8 | 6 |
| OR | 12 | 6 |
| XOR | 16 | 12 |

*(measured)* **Industry uses NAND anyway** — for library uniformity, and because in multi-level circuits the inversions cancel instead of accumulating.

---

## Common Errors

1. **Leaving a CMOS input floating** and calling it 0.
2. **Adding inverters after an AND-OR → NAND-NAND conversion** that the cancellation already removed.
3. **Building XOR from 5 NANDs** by computing $A\,\text{NAND}\,B$ twice.
4. **Asserting impossibility** instead of proving it with a closed property.
5. **Answering the $\{$XOR, AND$\}$ question without stating the constants assumption.**
6. **Using gate count as a proxy for speed.**

---

*ECE 110 · Week 2 · Reference Sheet*
