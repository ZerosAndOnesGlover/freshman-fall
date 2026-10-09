# ECE 110 · Digital Logic
## Week 4 · Lecture 1 (Wednesday)
### Karnaugh Maps

*“Simplicity is prerequisite for reliability.”* — Edsger W. Dijkstra, "How do we tell truths that might hurt?" (EWD498, 1975)

**Date:** Wednesday 17 February 2027 · 13:00–14:15 · Week 4

**Coursework:** 📊 **Quiz 3** today 13:00–13:10 · 📝 **PS 3** due Thu 18 Feb 13:00 · 📝 **PS 4** released Thu 18 Feb 14:30, due Thu 25 Feb 13:00 · 🔬 **Lab 4** Fri 19 Feb 14:00–15:50

---

**Reading:** Harris & Harris §2.7 | Mano & Ciletti §3.1–3.2
**Quiz 3** — at the start of today's lecture. **Covers Week 3.** Ungraded.

---

## 1. Why Not Just Do Algebra

**Week 1 minimised $\sum m(1,3,5,6,7)$ to $C+AB$ by spotting shared factors.** That worked because the function was small and the factors were visible.

**Two problems.** You must *notice* the opportunity, and there is no signal telling you when to stop. **A K-map fixes both:** the opportunities are visible as adjacent cells, and you stop when every 1 is covered by a maximal group.

---

## 2. Gray Code, and Why the Columns Are In That Order

**A K-map is a truth table drawn so that neighbouring cells differ in exactly one variable.**

**Ordinary binary counting does not do that** — $01 \to 10$ changes both bits. **Gray code does:**

$$00,\ 01,\ 11,\ 10$$

*(Verified: every consecutive pair differs in exactly one bit, and so does the wrap-around pair $10 \to 00$.)*

**The wrap-around matters.** It means **the left and right edges of the map are adjacent**, and so are the top and bottom. **The map is a torus**, not a rectangle, and groups may wrap around the edges.

---

## 3. The Maps

### Two variables

| $A\backslash B$ | 0 | 1 |
|:-:|:-:|:-:|
| **0** | $m_0$ | $m_1$ |
| **1** | $m_2$ | $m_3$ |

### Three variables

| $A\backslash BC$ | 00 | 01 | 11 | 10 |
|:-:|:-:|:-:|:-:|:-:|
| **0** | $m_0$ | $m_1$ | $m_3$ | $m_2$ |
| **1** | $m_4$ | $m_5$ | $m_7$ | $m_6$ |

**Note the column order and that $m_0$ is adjacent to $m_2$** — first column and last column touch.

### Four variables

| $AB\backslash CD$ | 00 | 01 | 11 | 10 |
|:-:|:-:|:-:|:-:|:-:|
| **00** | $m_0$ | $m_1$ | $m_3$ | $m_2$ |
| **01** | $m_4$ | $m_5$ | $m_7$ | $m_6$ |
| **11** | $m_{12}$ | $m_{13}$ | $m_{15}$ | $m_{14}$ |
| **10** | $m_8$ | $m_9$ | $m_{11}$ | $m_{10}$ |

**The four corners $m_0, m_2, m_8, m_{10}$ are mutually adjacent** — both edges wrap.

---

## 4. Grouping

> **Circle groups of $2^k$ adjacent 1s. Each group of size $2^k$ eliminates $k$ variables.**

**Why it works — a group of two:**

$$AB\overline C + ABC = AB(\overline C+C) = AB$$

**The variable that differs across the group cancels.** A group of four cancels two variables, a group of eight cancels three.

### The rules

1. **Groups must be rectangular** and of size $1, 2, 4, 8, 16$ — **never 3, 6 or 12**.
2. **Groups may wrap** around edges and corners.
3. **Groups may overlap.** A 1 covered twice costs nothing — $X+X=X$.
4. **Make every group as large as possible**, then use as few groups as possible.
5. **Every 1 must be covered at least once. No 0 may be covered.**

**Rule 4 is the one that is actually hard**, and rule 3 is the one students distrust — overlapping feels wasteful and is free.

---

## 5. Worked Example

$$F = \sum m(0,1,2,3,4,5,10,11,14,15)$$

| $AB\backslash CD$ | 00 | 01 | 11 | 10 |
|:-:|:-:|:-:|:-:|:-:|
| **00** | **1** | **1** | **1** | **1** |
| **01** | **1** | **1** | 0 | 0 |
| **11** | 0 | 0 | **1** | **1** |
| **10** | 0 | 0 | **1** | **1** |

**Three maximal groups:**

- **The whole top row** ($m_0,m_1,m_3,m_2$) — $A=0, B=0$, so $\overline A\,\overline B$.
- **The left half of rows 00 and 01** ($m_0,m_1,m_4,m_5$) — $A=0, C=0$, so $\overline A\,\overline C$.
- **The right half of rows 11 and 10** ($m_{15},m_{14},m_{11},m_{10}$) — $A=1, C=1$, so $AC$.

$$\boxed{F = \overline A\,\overline B + \overline A\,\overline C + AC} \qquad \textbf{3 terms, 6 literals}$$

*(Verified.)*

### The mistake to avoid

**A student who only ever circles pairs gets:**

$$\overline A\,\overline B\,\overline C + \overline A\,\overline BC + \overline AB\overline C\,\overline D + \overline AB\overline CD + A\overline BC + ABC$$

**6 terms, 20 literals — and it is completely correct.** *(Verified to be the same function.)*

> **Correct is not the same as minimal, and nothing in the answer tells you which you have.**
> **The discipline is: after you have covered every 1, go back and ask whether any group could have
> been bigger.** That question is the whole method.

---

## 6. Reading Zeros Instead

**Group the 0s the same way and you get $\overline F$ as an SOP; complement it with De Morgan to get $F$ as a POS.**

**For the same $F$:**

$$F = (C+\overline A)(A+\overline B+\overline C) \qquad \textbf{2 terms, 5 literals}$$

*(Verified equal to the SOP above.)*

**POS is cheaper here — 5 literals against 6.**

> **Week 1 said neither form always wins. This is the case.** **Do both maps.** It costs two minutes
> and it is the only way to know.

---

## 7. What To Take From This Lecture

1. **A K-map is a truth table in Gray-code order** so neighbours differ in one variable.
2. **The edges wrap** — the map is a torus, and the four corners are adjacent.
3. **A group of $2^k$ cells eliminates $k$ variables**, because the differing variables cancel.
4. **Groups: rectangular, powers of two, may wrap, may overlap.**
5. **Maximal groups first, then fewest groups.**
6. **A correct cover need not be minimal**, and the answer will not tell you — go back and check every group is maximal.
7. **Group the 0s for a POS**, and compare.

---

*Next: Thursday — Minimization, Don't-Cares, and Beyond*
