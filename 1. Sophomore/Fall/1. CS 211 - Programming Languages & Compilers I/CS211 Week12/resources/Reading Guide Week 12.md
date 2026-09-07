# CS 211 · Reading Guide · Week 12
## The Landscape of Programming Languages

**Three deadlines fall on Friday and the final is ten days later.** This guide is short, and everything on it is short. If you read one thing, read Hoare.

---

## Before Tuesday (L25 — design as constraint)

| Source | Why | Pages |
|---|---|---|
| **Hoare (1980), "The Emperor's Old Clothes"** | The Turing Award lecture. **Where he apologises for the null reference** — "my billion-dollar mistake" — and where the two-ways-of-constructing-a-design line comes from. Funny, and forty-five years old. | 10 |
| **Gabriel (1991), "Worse Is Better"** | Why the simpler-to-implement design wins even when it is worse. Uncomfortable, and mostly right. | 6 |
| **Wirth (1995), "A Plea for Lean Software"** | The complaint of someone who watched the industry choose otherwise. | 5 |

---

## Before Thursday (L26 — the landscape)

| Source | Why | Pages |
|---|---|---|
| **Haas et al. (2017)**, "Bringing the Web up to Speed with WebAssembly" | The design paper. **§2–3 is the language; §4 is the formal semantics** — the first mainstream bytecode with one. | 12 |
| **Steele (1998), "Growing a Language"** | A talk that is also a demonstration of its own thesis. Watch it rather than read it; the effect does not survive on paper. | — |
| **Lattner (AOSA ch. 11)** *(revisit)* | Week 11's reading, re-read for §L26.2's argument about targets. | 14 |

---

## If You Want More

- **Sebesta**, *Concepts of Programming Languages* — the standard survey, and a reasonable reference for the history in L25 §5.
- **Van Roy & Haridi**, *Concepts, Techniques, and Models of Computer Programming* — organises languages by what they *add* rather than by paradigm. The best structural account of the landscape.
- **Kernighan & Ritchie**, *The C Programming Language* — read it now, at 270 pages, and notice how much of L25 §5's "cost" column is visible in it.
- **The Rust Book, ch. 4** — ownership, in the language's own words, beside L25 §6.

---

## The One Thing Worth Reading Twice

**Hoare (1980), the section on the null reference.**

Read it, then run:

```bash
./bounds_c ; java Bounds ; python3 bounds.py ; node bounds.js
```

Hoare's point is that he added null **because it was easy to implement**, and that the cost has been paid continuously ever since by everyone else.

The four programs are the same argument in miniature. C's `29291` is easy to implement — no check, no cost. JavaScript's `undefined` is easy too. **Both push the cost onto every future reader of every program written in them**, and Java and Python's per-access check is the alternative bill, paid visibly and in advance.

**That is the whole of L25 in one comparison**, and it is why the lecture's closing question is about failure modes rather than features.

---

## A Note on the Final

**The most efficient revision material in this course is the eleven quiz answer keys**, and they already exist. They cover Weeks 0–10 with worked reasoning, they are written in the register the exam uses, and re-reading them is worth more per hour than any book on this page.

[[CS211 Week12/resources/FINAL EXAM Revision Guide|FINAL EXAM Revision Guide]] says what is on the paper and in what proportion. **Q7 is 30 of 150 marks and is the only part you can fully prepare in advance** — PS 12 is three-quarters of that preparation, which is why it is short.

---

*CS 211 · Week 12 · Reading Guide · © CSE Department*
