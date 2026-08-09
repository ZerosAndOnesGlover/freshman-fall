# ECE 110 · Digital Logic
## Problem Set 2 — Solutions
### INSTRUCTOR / TA COPY — not for distribution

---

**Total: 100 points.** All constructions verified exhaustively in Python and Verilog; all minimum gate counts established by exhaustive search.

---

## Part A (5 pts each)

**A1 (5).** Standard tables. NAND is 1 except at $(1,1)$; NOR is 1 only at $(0,0)$; XOR is 1 when inputs differ; XNOR when they agree.

**A2 (5).** Each gate **restores** the signal: any input inside a valid range produces an output comfortably inside a valid range, so noise picked up on a wire is removed rather than passed on. An analogue amplifier passes its input through faithfully **including the noise**, and amplifies it, so error accumulates along the chain. **Digital circuits are deep because every stage discards the deviation.**

*Marking: 5. **The word "restore" or an equivalent must appear.***

**A3 (5).** $NM_H = V_{OH}-V_{IH} = 2.4-2.0 = \boxed{0.4\text{ V}}$; $NM_L = V_{IL}-V_{OL} = 0.8-0.4 = \boxed{0.4\text{ V}}$.

**A4 (5).** CMOS builds a gate as a PMOS pull-up and an NMOS pull-down, and **the natural output is the complement** of the pull-down's condition. NAND is therefore one 4-transistor stage; **AND is a NAND followed by an inverter**, $4+2=6$.

**Rule: inverting gates (NAND, NOR, NOT) are the cheap primitives; non-inverting ones cost an extra inverter.**

---

## Part B (6 pts each)

**B1 (6).**

$$\overline A = A\,\text{NAND}\,A \ (1) \qquad AB = \overline{(A\,\text{NAND}\,B)} \ (2) \qquad A+B = \overline A\,\text{NAND}\,\overline B \ (3)$$

*(All verified.)*

**B2 (6).** The duals:

$$\overline A = A\,\text{NOR}\,A \ (1) \qquad A+B = \overline{(A\,\text{NOR}\,B)} \ (2) \qquad AB = \overline A\,\text{NOR}\,\overline B \ (3)$$

**B3 (6).**

$$F = AB+CD = \overline{\overline{AB+CD}} = \overline{\overline{AB}\cdot\overline{CD}} = \big(\overline{AB}\big)\,\text{NAND}\,\big(\overline{CD}\big)$$

**So: every AND becomes a NAND, the OR becomes a NAND, and the two added inversions cancel.** *(Verified over all 16 assignments.)*

**Gate count is unchanged at 3**, and the level count is unchanged at 2. **The conversion is free.**

**B4 (6).** Dually, $G = (A+B)(C+D) = \big(\overline{A+B}\big)\,\text{NOR}\,\big(\overline{C+D}\big)$ — three NOR gates, two levels. *(Verified.)*

**B5 (6).** With $X = A\,\text{NAND}\,B$ **computed once and shared**:

$$A\oplus B = (A\,\text{NAND}\,X)\,\text{NAND}\,(B\,\text{NAND}\,X) \qquad \textbf{4 gates}$$

*(Verified. Exhaustive search confirms 4 is the true minimum.)*

**The naive $A\overline B+\overline AB$ route costs 9 NAND gates:** 2 inverters, 2 ANDs at 2 each, 1 OR at 3.

$$\boxed{9 \to 4 \text{ by sharing one sub-expression}}$$

*Marking: 3 construction, 2 identifying $X$ as shared, 1 the naive count. **The sharing is the point** — a student who draws 4 gates but cannot say why it is not 5 earns 4 of 6.*

---

## Part C (5 pts each)

**C1 (5).** **A set of gates is functionally complete if every Boolean function of any number of variables can be realised using only gates from that set.**

**C2 (5).** Build NOT, AND and OR from NAND (B1), then invoke that $\{$AND, OR, NOT$\}$ is complete — which Week 1's canonical SOP establishes, since every truth table becomes an expression in exactly those operators. $\blacksquare$

*Marking: 3 constructions, **2 for the appeal to canonical SOP.** A student who builds the three gates and stops has not finished the proof.*

**C3 (5).** **Monotonicity.**

1. Call $f$ monotone if flipping an input $0\to1$ never flips the output $1\to0$.
2. **AND and OR are monotone** *(verified)*; a composition of monotone functions is monotone.
3. So every function over $\{$AND, OR$\}$ is monotone.
4. **NOT is not monotone** *(verified)*.
5. Therefore NOT is not constructible. $\blacksquare$

*Marking: 5. **An answer of the form "there is no way to invert" earns 1.** The property-exhibiting structure is the whole exercise.*

**C4 (5).** **No.**

**NOT and XOR are both *affine*** — expressible as $c_0 \oplus c_1x_1\oplus\cdots\oplus c_nx_n$ — **and a composition of affine functions is affine.** *(Verified: NOT and XOR are affine, and 200 randomly generated circuits over $\{$NOT, XOR$\}$ were all affine.)*

**AND is not affine** *(verified)*, so it cannot be built. $\blacksquare$

> **This is the second impossibility proof of the course and it has exactly the shape of the first:**
> find a property closed under composition, show the target lacks it. **Monotonicity killed
> $\{$AND, OR$\}$; affineness kills $\{$NOT, XOR$\}$.**

**C5 (5).** **It depends on whether the constant 1 is available.**

- **With constants: yes.** $\overline A = A\oplus1$ *(verified)*, giving NOT, and $\{$AND, NOT$\}$ is complete. *(This is the Reed–Muller basis.)*
- **Without constants: no.** Both AND and XOR output 0 when all inputs are 0, so **every composition maps all-zeros to 0** — but $\text{NOT}(0)=1$. $\blacksquare$

*Marking: 2 for each case, **1 for identifying that the availability of constants is the distinguishing assumption.** A student who answers only "yes" or only "no" earns 2.*

---

## Part D (5 pts each)

**D1 (5).**

| gate | NOT | NAND2 | NOR2 | AND2 | OR2 | XOR2 |
|---|---:|---:|---:|---:|---:|---:|
| transistors | 2 | 4 | 4 | 6 | 6 | 12 |

**D2 (5).**

| build | transistors |
|---|---:|
| 4 × NAND | $4\times4 = \mathbf{16}$ |
| 2 NOT + 2 AND + 1 OR | $2(2)+2(6)+6 = \mathbf{22}$ |

$$\textbf{NAND wins by 6 transistors, about 27\%.}$$

**D3 (5).**

| | NAND | NOR |
|---|---:|---:|
| XOR | **4** | 5 |
| XNOR | 5 | **4** |

*(All four are true minima, established by exhaustive search over constructions up to 8 gates.)*

**The symmetry is duality:** NAND and NOR are duals, XOR and XNOR are duals, so the cost table is symmetric under swapping both.

**D4 (5).**

| structure | gates | critical path |
|---|---:|---:|
| chain $((AB)C)D$ | 3 | **3 gate delays** |
| tree $(AB)(CD)$ | 3 | **2 gate delays** |

**D5 (5).** **Gate count and delay are different costs and they do not track each other.** Two circuits computing the same function with identical area can differ in speed by 50%.

> **Gate count is area. Critical path is speed.** Optimising one does not optimise the other, and a
> real design states which it is optimising. **This is the same lesson as Week 1's literals-versus-gates
> table, one level down.**

*Marking: 5. **Full marks require naming both as separate costs**, not merely observing that the delays differ.*

---

## Marking Summary

| Part | Points |
|---|---|
| A | 20 |
| B | 30 |
| C | 25 |
| D | 25 |
| **Total** | **100** |

---

## The Five Errors To Expect

1. **B3:** converting AND-OR to NAND-NAND and then *adding* inverters that the cancellation already removed.
2. **B5:** drawing 5 gates because $A\,\text{NAND}\,B$ was computed twice.
3. **C3/C4:** asserting impossibility instead of proving it via a closed property.
4. **C5:** answering without noticing the constants assumption.
5. **D5:** observing that delays differ but not naming area and speed as distinct costs.

---

*ECE 110 · Week 2 · PS 2 Solutions · Instructor Only*
