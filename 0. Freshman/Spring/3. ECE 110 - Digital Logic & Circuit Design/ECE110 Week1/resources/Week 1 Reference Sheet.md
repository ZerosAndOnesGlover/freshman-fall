# ECE 110 · Digital Logic
## Week 1 · Reference Sheet
### Boolean Algebra

---

## Operators

| | written | note |
|---|---|---|
| **AND** | $AB$, $A\cdot B$ | |
| **OR** | $A+B$ | **inclusive**: $1+1=1$ |
| **NOT** | $\overline A$, $A'$ | |
| **XOR** | $A\oplus B$ | 1 iff the inputs differ |

---

## The Laws

| | | |
|---|---|---|
| **Identity** | $A+0=A$ | $A\cdot1=A$ |
| **Null** | $A+1=1$ | $A\cdot0=0$ |
| **Idempotence** | $A+A=A$ | $A\cdot A=A$ |
| **Complement** | $A+\overline A=1$ | $A\overline A=0$ |
| **Involution** | $\overline{\overline A}=A$ | |
| **Commutative** | $A+B=B+A$ | $AB=BA$ |
| **Associative** | $(A{+}B){+}C = A{+}(B{+}C)$ | $(AB)C=A(BC)$ |
| **Distributive** | $A(B{+}C)=AB{+}AC$ | $A{+}BC=(A{+}B)(A{+}C)$ |
| **Absorption** | $A+AB=A$ | $A(A+B)=A$ |
| **De Morgan** | $\overline{AB}=\overline A+\overline B$ | $\overline{A+B}=\overline A\,\overline B$ |
| **Consensus** | $AB+\overline AC+BC = AB+\overline AC$ | |

*(all verified exhaustively, in Python and independently in Verilog — 15/15, zero failures)*

### The two that are not arithmetic

$$A+BC=(A+B)(A+C) \qquad\qquad A+AB = A$$

**At $A{=}1,B{=}1,C{=}0$:** Boolean gives $1=1$; arithmetic gives $1$ vs $\mathbf{2}$.

### XOR

$$A\oplus B = A\overline B+\overline AB \qquad A\oplus0=A \qquad A\oplus1=\overline A \qquad A\oplus A=0 \qquad A\oplus\overline A=1$$

$$\boxed{\overline A\oplus\overline B = A\oplus B} \qquad \boxed{\overline{A\oplus B} = A\oplus\overline B}$$

> **Complementing one input inverts XOR; complementing both leaves it alone.** *(verified)* This is
> the controlled-inverter behind Week 6's ALU.

**XOR is associative**: $A\oplus(B\oplus C) = (A\oplus B)\oplus C$. *(verified)*

---

## Duality

> **The dual of a valid identity is valid.** Swap $+\leftrightarrow\cdot$ and $0\leftrightarrow1$;
> **leave variables and complements alone.**

**So you need remember only half the table.**

**Duality is a claim about which identities are true — not a transformation you may apply to one side of an equation.** Complementing variables is a *different* operation and confusing the two is the standard error.

---

## De Morgan in Practice

$$\overline{AB}\ne\overline A\,\overline B \qquad\text{(check at } A{=}1,B{=}0\text{: } 1 \text{ vs } 0)$$

**To complement any expression:** complement every variable, swap every $+$ with $\cdot$.

$$\overline{A\overline B+\overline AC} = (\overline A+B)(A+\overline C) \qquad\textbf{(verified)}$$

**Bubble pushing** is the schematic form: a NAND is simultaneously AND-with-inverted-output and OR-with-inverted-inputs. **This is why NAND is universal** *(Week 2)*.

---

## Canonical Forms

| | built from | variable complemented when its bit is |
|---|---|---|
| **Minterm** ($\sum m$) | the **1** rows | **0** |
| **Maxterm** ($\prod M$) | the **0** rows | **1** |

**Opposite rules — this is the most common slip.**

### Worked: $F=\sum m(1,3,5,6,7)$

$$\text{canonical SOP} = \overline A\,\overline BC+\overline ABC+A\overline BC+AB\overline C+ABC \quad\text{(5 terms, 15 literals)}$$

$$\boxed{F = C+AB} \quad\text{(2 terms, 3 literals)} \qquad F=(A+C)(B+C) \quad\text{(2 terms, 4 literals)}$$

*(all verified equivalent)*

### Cost, under 2-input gates with shared inverters

| form | NOT | AND | OR | total |
|---|---:|---:|---:|---:|
| canonical SOP | 3 | 10 | 4 | **17** |
| minimal $C+AB$ | 0 | 1 | 1 | **2** |

$$\textbf{17} \to \textbf{2 gates } (8.5\times) \quad\text{while literals fell only } 5\times$$

> **Minimisation removed the inverters too**, so the gate saving beats the literal saving.
> **Literals are a proxy for cost; gates are closer to it.**

**Neither SOP nor POS is always cheaper** — for $\sum m(0,2,5,7)$ both are 4 literals. **Compute both.**

---

## How Big Is The Space

$$\text{Boolean functions of } n \text{ variables} = 2^{2^n}$$

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| functions | 4 | 16 | 256 | 65 536 | $4.29\times10^9$ | $1.84\times10^{19}$ |

**At $n=6$ there are more functions than distinct 64-bit integers.** *(verified)* **Hence method, not cleverness** — Week 4.

---

## Common Errors

1. **Reading $+$ as arithmetic.** $1+1=1$.
2. **$\overline{AB} = \overline A\,\overline B$.** Break the bar, *change the operator*.
3. **Complementing variables when forming a dual.**
4. **Applying consensus where absorption applies** — check which theorem fits.
5. **Complementing maxterms on 0.** Minterms complement on 0; maxterms on 1.
6. **Unnamed steps in an algebraic proof.**
7. **Assuming SOP is always cheaper than POS.**

---

*ECE 110 · Week 1 · Reference Sheet*
