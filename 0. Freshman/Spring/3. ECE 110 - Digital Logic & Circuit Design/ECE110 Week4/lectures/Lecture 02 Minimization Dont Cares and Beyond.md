# ECE 110 · Digital Logic
## Week 4 · Lecture 2 (Thursday)
### Minimization, Don't-Cares, and Beyond

**Date:** Thursday 11 February 2027 · 13:00–14:15 · Week 4

---

**Reading:** Harris & Harris §2.7.3 | Mano & Ciletti §3.3–3.4
**PS 4** released today, due Thursday of Week 5.

---

## 1. The Vocabulary Minimisation Actually Uses

**Yesterday you circled groups. Today those circles get names, because the names turn a knack into a procedure.**

| term | meaning |
|---|---|
| **implicant** | any product term that implies $F$ — any legal group |
| **prime implicant** | a group that **cannot be made larger** |
| **essential prime implicant** | a prime implicant that is **the only one covering some minterm** |

> **The minimal cover always consists of prime implicants** — a non-maximal group can always be
> enlarged for free. **And every essential prime implicant must appear in every minimal cover**,
> because the minterm only it covers has to be covered somehow.

**That gives a procedure rather than a knack.**

---

## 2. The Procedure

1. **Find every prime implicant** — every group that cannot grow.
2. **Find the essential ones** — for each minterm, if exactly one prime implicant covers it, that implicant is essential.
3. **Take all essentials.**
4. **Cover whatever minterms remain**, using as few of the remaining prime implicants as possible.

---

## 3. Worked Example

$$F = \sum m(0,1,2,5,6,7,8,9,10,14)$$

| $AB\backslash CD$ | 00 | 01 | 11 | 10 |
|:-:|:-:|:-:|:-:|:-:|
| **00** | **1** | **1** | 0 | **1** |
| **01** | 0 | **1** | **1** | **1** |
| **11** | 0 | 0 | 0 | **1** |
| **10** | **1** | **1** | 0 | **1** |

### Step 1 — the prime implicants

$$\overline B\,\overline C,\quad \overline B\,\overline D,\quad C\overline D,\quad \overline ABC,\quad \overline ABD,\quad \overline A\,\overline CD$$

*(Six, found exhaustively.)*

### Step 2 — which are essential

$$\boxed{\overline B\,\overline C \quad\text{and}\quad C\overline D}$$

*(Verified: $m_0$ and $m_9$ are covered only by $\overline B\,\overline C$; $m_{14}$ only by $C\overline D$.)*

### Step 3–4 — cover the remainder

**The two essentials cover $m_0,m_1,m_2,m_6,m_8,m_9,m_{10},m_{14}$.**

$$\textbf{Left over: } m_5, m_7$$

**One prime implicant covers both — $\overline ABD$.**

$$\boxed{F = \overline B\,\overline C + C\overline D + \overline ABD} \qquad \textbf{3 terms, 7 literals}$$

*(Verified minimal.)*

> **Notice that $\overline B\,\overline D$, $\overline ABC$ and $\overline A\,\overline CD$ are all
> prime implicants and none appears in the answer.** Being maximal is necessary and not sufficient —
> **step 4 is a covering problem, and it is where a genuine choice can exist.**

---

## 4. Don't-Cares

**Some inputs cannot occur.** A BCD digit uses $0000$–$1001$; the six codes $1010$–$1111$ are **impossible**.

**The output on an impossible input is unconstrained.** Mark it $\times$, and **treat it as 1 or 0 — whichever makes your groups bigger.**

### Worked: "is this BCD digit $\ge 5$?"

**1 on $m_5,m_6,m_7,m_8,m_9$; $\times$ on $m_{10}\ldots m_{15}$.**

| | expression | literals |
|---|---|---:|
| **using the don't-cares** | $A + BC + BD$ | **5** |
| treating them as 0 | $\overline ABC + \overline ABD + A\overline B\,\overline C$ | 9 |

*(Both verified — and the don't-care version gives the specified output on **every input that can actually occur**.)*

**Nearly half the literals, for free.**

> **The don't-care version outputs 1 for the input $1111$.** That is not a bug: $1111$ is not a BCD
> digit, so no correct circuit is defined there. **But if your assumption is wrong — if that code
> *can* appear — the circuit is now wrong in a way the map will never show you.**
>
> **A don't-care is a claim about the world, not about the algebra.** Write down why each one is
> impossible.

---

## 5. Where Maps Stop

**Maps are comfortable to 4 variables, awkward at 5, unusable past 6.** The reason is human: you cannot see adjacency in more than three dimensions on paper.

**Beyond that, the systematic method is Quine–McCluskey** — exactly the same two steps, done as a table:

1. **Merge terms differing in one bit, repeatedly, until nothing merges.** What remains is the prime implicants.
2. **Solve the covering problem** with a chart.

**It is mechanical, so a machine can run it** — which is what a logic synthesis tool does, and why Week 12's FPGA flow requires no human to minimise anything.

> **It is also expensive.** The covering problem in step 2 is NP-hard in general, so real tools use
> heuristics past a certain size and **do not guarantee a true minimum.** Your four-variable map does.

---

## 6. What Minimisation Is Actually For

**Fewer literals means fewer gate inputs; fewer terms means fewer gates.** From Week 1: $\sum m(1,3,5,6,7)$ went 17 gates → 2.

**But recall Week 3.** The ripple-carry adder's problem was **not** gate count — it was the critical path, and no amount of minimisation would have fixed it.

> **Minimisation reduces area, and reduces delay only incidentally.** It is the right tool for "this
> costs too much" and the wrong tool for "this is too slow". **Week 6 is the other tool.**

---

## 7. What To Take From This Lecture

1. **Prime implicant = a group that cannot grow.** The minimal cover uses only these.
2. **Essential = the sole cover of some minterm.** Every minimal cover contains all of them.
3. **Procedure: all primes → essentials → cover the rest.**
4. **Being prime is not enough** — step 4 is a real covering problem.
5. **Don't-cares are free literals**, and are **a claim about the world**. Justify each one.
6. **Maps stop at ~4–6 variables; Quine–McCluskey scales**, and real tools stop guaranteeing minimality.
7. **Minimisation buys area, not speed.**

---

*Next: Friday — Lab 4, your minimisation against a machine's*
