# ECE 110 · Digital Logic
## Week 2 · Lecture 2 (Thursday)
### Functional Completeness and Gate-Level Design

*“There is not only a close analogy between the operations of the mind in general reasoning and its operations in the particular science of Algebra, but there is to a considerable extent an exact agreement in the laws by which the two classes of operations are conducted.”* — George Boole, *An Investigation of the Laws of Thought* (1854)

**Date:** Thursday 4 February 2027 · 13:00–14:15 · Week 2

**Coursework:** 📝 **PS 1** due today 13:00 · 📝 **PS 2** released today 14:30, due Thu 11 Feb 13:00 · 🔬 **Lab 2** Fri 5 Feb 14:00–15:50 · 📊 **Quiz 2** Wed 10 Feb 13:00–13:10

---

**Reading:** Harris & Harris §2.5 | Mano & Ciletti §3.5
**PS 2** released today, due Thursday of Week 3.

---

## 1. Functional Completeness

> **A set of gates is functionally complete if every Boolean function can be built from it.**

**$\{$AND, OR, NOT$\}$ is complete** — Week 1's canonical SOP is the proof, since every truth table becomes an expression in exactly those three operators.

**The interesting claims are the small sets.**

---

## 2. NAND Alone Is Complete

**It suffices to build AND, OR and NOT**, since those three are already known to be complete.

$$\overline A = A\ \text{NAND}\ A$$

$$AB = \overline{\overline{AB}} = (A\ \text{NAND}\ B)\ \text{NAND}\ (A\ \text{NAND}\ B)$$

$$A+B = \overline{\overline A\,\overline B} = \overline A\ \text{NAND}\ \overline B = (A\ \text{NAND}\ A)\ \text{NAND}\ (B\ \text{NAND}\ B)$$

*(All three verified exhaustively, in Python and independently in a Verilog testbench.)*

**The OR construction is De Morgan directly**: $\overline{\overline A\,\overline B} = A+B$.

| built | NAND gates |
|---|---:|
| NOT | 1 |
| AND | 2 |
| OR | 3 |
| NOR | 4 |
| **XOR** | **4** |

### XOR from NAND, the four-gate build

$$A\oplus B = \overline{\big(A\cdot\overline{AB}\big)\cdot\big(B\cdot\overline{AB}\big)}$$

**With $X = A\ \text{NAND}\ B$ computed once and shared:**

$$A\oplus B = (A\ \text{NAND}\ X)\ \text{NAND}\ (B\ \text{NAND}\ X)$$

*(Verified.)* **Four gates, and the sharing of $X$ is what makes it four rather than five.**

---

## 3. NOR Alone Is Complete Too

$$\overline A = A\ \text{NOR}\ A \qquad A+B = \overline{\overline{A+B}} \qquad AB = \overline A\ \text{NOR}\ \overline B$$

*(All verified.)*

**The constructions are the duals of NAND's**, which is Week 1's duality principle showing up in hardware.

**NOR was historically the primitive** in some technologies — the Apollo Guidance Computer was built from about 5600 NOR gates and nothing else.

---

## 4. A Set That Is *Not* Complete

**$\{$AND, OR$\}$, with no NOT, cannot build every function.**

**Proof.** Call a function **monotone** if changing any input from 0 to 1 never changes the output from 1 to 0.

1. **AND is monotone.** **OR is monotone.** *(Verified.)*
2. **A composition of monotone functions is monotone.** If every input change can only push intermediate values up, the output can only be pushed up.
3. **Therefore every function built from AND and OR alone is monotone.**
4. **NOT is not monotone** — changing its input $0\to1$ changes its output $1\to0$. *(Verified.)*
5. **So NOT cannot be built from AND and OR.** $\blacksquare$

> **This is the course's first impossibility proof, and the distinction matters.** It does not say
> "no construction has been found". It says **no construction exists**, and it takes five lines.
>
> **The same shape of argument** — find a property every member of a class has, exhibit something
> lacking it — is how Week 12 will separate what programmable logic can and cannot do in one pass.

---

## 5. Converting a Design to NAND-Only

**Given a minimised SOP expression, the conversion is mechanical.**

**A two-level AND-OR circuit becomes a two-level NAND-NAND circuit with the same structure.**

$$F = AB + CD \;=\; \overline{\overline{AB+CD}} \;=\; \overline{\overline{AB}\cdot\overline{CD}} \;=\; \big(\overline{AB}\big)\ \text{NAND}\ \big(\overline{CD}\big)$$

**So: replace every AND with a NAND, replace the OR with a NAND, and you are done.** The two added inversions cancel — this is bubble pushing.

> **Any two-level SOP becomes NAND-NAND with the same gate count and the same number of levels.**
> Literal inputs that arrive complemented need an inverter, which is one more NAND each.

**The dual holds:** a two-level POS (OR-AND) becomes NOR-NOR.

---

## 6. What XOR Costs, Three Ways

| technology | XOR | XNOR |
|---|---:|---:|
| **NAND only** | **4** | 5 |
| NOR only | 5 | **4** |
| AND / OR / NOT | 5 | 5 |

*(All four gate counts established by exhaustive search over every construction up to 8 gates — these are true minima, not merely the best anyone has drawn.)*

> **Look at the mirror.** XOR is cheaper in NAND; XNOR is cheaper in NOR, by exactly the same margin.
> **That is Week 1's duality principle, priced in silicon.**

**In transistors, the AND/OR/NOT build is $2(2) + 2(6) + 6 = 22$ against NAND's $4\times4 = 16$.**

> **Same function, same truth table, different cost — and which is cheapest depends on the
> technology, not on the algebra.** Week 1 said neither SOP nor POS always wins; this week says
> neither gate family always wins either. **You compute both.**

---

## 7. What To Take From This Lecture

1. **Functionally complete = can build every Boolean function.**
2. **NAND alone is complete. NOR alone is complete.** Verified constructions for each.
3. **XOR is 4 NAND gates**, and the sharing of $A\ \text{NAND}\ B$ is why.
4. **$\{$AND, OR$\}$ is *not* complete** — the monotonicity proof, in five lines.
5. **AND-OR converts to NAND-NAND mechanically**, same structure, bubbles cancelling.
6. **POS converts to NOR-NOR** by duality.
7. **The cheapest realisation depends on the technology.**

---

*Next: Friday — Lab 2, gates on a breadboard*
