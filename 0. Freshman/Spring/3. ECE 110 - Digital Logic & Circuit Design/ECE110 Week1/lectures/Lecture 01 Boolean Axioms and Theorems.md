# ECE 110 · Digital Logic
## Week 1 · Lecture 1 (Wednesday)
### Boolean Axioms and Theorems

*“To deduce the laws of the symbols of Logic from a consideration of those operations of the mind which are implied in the strict use of language as an instrument of reasoning.”* — George Boole, *An Investigation of the Laws of Thought* (1854), stating his aim

**Date:** Wednesday 27 January 2027 · 13:00–14:15 · Week 1

**Coursework:** 📝 **PS 0** due Thu 28 Jan 13:00 · 📝 **PS 1** released Thu 28 Jan 14:30, due Thu 4 Feb 13:00 · 🔬 **Lab 1** Fri 29 Jan 14:00–15:50

---

**Reading:** Harris & Harris §2.1–2.3 | Mano & Ciletti §2.1–2.4
**PS 1** released tomorrow. **No quiz this week** — Quiz 1 is next Wednesday and covers this week.

---

## 1. Two Values, Three Operators

**A Boolean variable takes one of two values.** Write them $0$ and $1$; the hardware will call them low and high, and Week 2 will call them volts.

**Three operators, and everything else is built from them:**

| operator | written | reads | $0$ result |
|---|---|---|---|
| **AND** | $AB$, $A\cdot B$, $A\wedge B$ | "A and B" | unless both are 1 |
| **OR** | $A+B$, $A\vee B$ | "A or B" | only when both are 0 |
| **NOT** | $\overline A$, $A'$, $\lnot A$ | "not A" | when $A=1$ |

**OR is inclusive.** $1+1 = 1$, not 2. **This is where the notation first lies to you**, and it is worth saying out loud: the symbols $+$ and $\cdot$ were borrowed from arithmetic because the *shapes* of some laws match. **The values are not numbers and there is no carrying.**

---

## 2. The Axioms

**Everything below follows from these.** They are stated in pairs, and the pairing is not decoration — see §5.

| | | |
|---|---|---|
| **Identity** | $A+0=A$ | $A\cdot 1 = A$ |
| **Null / domination** | $A+1=1$ | $A\cdot 0 = 0$ |
| **Idempotence** | $A+A=A$ | $A\cdot A = A$ |
| **Complement** | $A+\overline A = 1$ | $A\cdot\overline A = 0$ |
| **Involution** | $\overline{\overline A} = A$ | |
| **Commutative** | $A+B = B+A$ | $AB = BA$ |
| **Associative** | $(A+B)+C = A+(B+C)$ | $(AB)C = A(BC)$ |
| **Distributive** | $A(B+C) = AB+AC$ | $A+BC = (A+B)(A+C)$ |
| **Absorption** | $A+AB = A$ | $A(A+B) = A$ |

**All eighteen verified exhaustively** — by a Verilog simulation over every input assignment, and independently by a symbolic solver. *(Agreement between two unrelated tools is the standard this course holds itself to; see Lab 1.)*

---

## 3. The One That Is Not Arithmetic

$$\boxed{A + BC = (A+B)(A+C)}$$

**Read that again if it looked ordinary.** In arithmetic, $a + bc \ne (a+b)(a+c)$ in general:

| $A$ | $B$ | $C$ | Boolean $A+BC$ | Boolean $(A{+}B)(A{+}C)$ | arithmetic $a{+}bc$ | arithmetic $(a{+}b)(a{+}c)$ |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | 1 | 0 | 1 | 1 | 1 | **2** |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 | 1 | 1 | **2** |

*(Verified.)*

> **The Boolean columns agree on all eight rows. The arithmetic columns do not.** OR distributes over
> AND *and* AND distributes over OR — a symmetry ordinary algebra does not have, and the source of
> most of the simplifications you will find.

**Absorption is the same surprise in miniature:** $A + AB = A$ regardless of $B$. In arithmetic $a+ab \ne a$ unless $b=0$.

---

## 4. Proving a Theorem

**Two methods. Use both until one becomes reliable.**

### By truth table — always works, never elegant

$2^n$ rows, evaluate both sides, compare. **For $n\le4$ this is the honest answer** and it is what Lab 1 automates.

### By algebra — shorter, and easier to get wrong

**Prove absorption $A+AB=A$:**

$$A + AB = A\cdot1 + AB = A(1+B) = A\cdot 1 = A$$

*Identity, distributive, null, identity.* **Name the law at every step.** A chain of unjustified rewrites is not a proof and is marked as though it were wrong, because in this algebra your intuition is exactly the thing on trial.

---

## 5. Duality

**Every identity in §2 came in a pair, and the pairing is a theorem.**

> **The dual of a valid Boolean identity is a valid Boolean identity.**
> **Form it by swapping $+ \leftrightarrow \cdot$ and $0 \leftrightarrow 1$**, leaving variables and
> complements alone.

$$A+0=A \quad\xrightarrow{\ \text{dual}\ }\quad A\cdot1 = A$$
$$A+AB = A \quad\xrightarrow{\ \text{dual}\ }\quad A(A+B) = A$$

**So you only ever have to remember half the table.**

> **Duality is not the same as complementing.** The dual of an *expression* is not equal to that
> expression — $A+0$ and $A\cdot1$ are both equal to $A$ here only because both are identities.
> **Duality is a statement about which identities are true, not a transformation you may apply
> mid-proof.** Applying it to one side of an equation is the most common way students produce a
> confident wrong answer on this material.

---

## 6. The Consensus Theorem

$$\boxed{AB + \overline A C + BC = AB + \overline A C}$$

**The third term is redundant.** *(Verified: both sides produce the truth table `[0,1,0,1,0,0,1,1]` over $ABC = 000\ldots111$.)*

**Why:** for $BC$ to matter, both $B$ and $C$ must be 1. If also $A=1$ then $AB$ already covers it; if $A=0$ then $\overline A C$ already covers it. **There is no remaining case**, so $BC$ contributes nothing.

**Proof:**

$$AB+\overline AC+BC = AB+\overline AC+BC(A+\overline A) = AB+\overline AC+ABC+\overline ABC$$
$$= AB(1+C) + \overline AC(1+B) = AB+\overline AC$$

> **Why it matters.** A redundant term is redundant gates — real area, real power, real delay. And
> this is precisely the term a Karnaugh map deletes in Week 4, so meeting it algebraically first
> makes the map's answer explicable rather than magical.

---

## 7. What To Take From This Lecture

1. **Two values, three operators.** OR is inclusive; $1+1=1$.
2. **The symbols are borrowed from arithmetic; the rules are not.**
3. **$A+BC = (A+B)(A+C)$** — true here, false in arithmetic. Absorption likewise.
4. **Name the law at every step** of an algebraic proof.
5. **Duality halves what you must memorise**, and is a claim about identities — not a licence to transform one side.
6. **Consensus: $AB+\overline AC+BC = AB+\overline AC$.** Redundant terms cost gates.

---

*Next: Thursday — De Morgan, Duality, and Canonical Forms*
