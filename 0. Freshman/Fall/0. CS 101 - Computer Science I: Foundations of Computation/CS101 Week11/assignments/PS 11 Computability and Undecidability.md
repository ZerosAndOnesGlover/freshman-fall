# CS 101 · Problem Set 11
## Computability and Undecidability

**Released:** Friday 11 December 2026, 10:00 (after L36) · Week 11
**Due:** Friday 18 December 2026, 17:00 · Week 12 — late penalty from 17:01
**Submission:** `ps11.py` and your answer sheet in `"$CS101/week11"`, committed to the Freshman Fall repo.
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: cut from about four hours to three. Lab 11, on Tuesday 15 December, writes the
doubling-budget recogniser (Exercise 5.3), so A3(b) and B3 left this set. The 7-tuple recall A1(a) and
the binary-increment machine were removed too.)*

---

## Overview

This set is half proof, half construction. Part A asks you to reason about what machines can and
cannot do; Part B asks you to build machines and write reductions as code.

Written answers go in this file. Code goes in `ps11.py`, scaffolded by `ps11_starter.py`.

> **⚠️ This is the last problem set before the final.** Part A's reduction proofs are the most
> likely exam material in the course. Do them properly rather than quickly.

**A note on proofs.** A reduction proof is not a paragraph of intuition. It must: state the
assumption, exhibit the construction, argue **both** directions of the equivalence, and conclude.
Missing either direction is missing half the proof, and is marked accordingly.

---

## Part A: Written Questions (62 points)

### A1: Models and Their Limits (8 points)

(a) A student proposes a "Turing machine with two heads on one tape" and claims it is strictly more
powerful. Explain why the claim is wrong, and state what such a machine *does* buy you. *(4 pts)*

(b) Give one language that a finite automaton can recognise and one it cannot, and state the single
structural property that separates them. *(4 pts)*

&nbsp;

### A2: The Church–Turing Thesis (10 points)

(a) State the thesis. *(2 pts)*

(b) Explain why it is not a theorem and cannot be proved. *(4 pts)*

(c) Your colleague says: "Quantum computers can solve problems classical computers can't, so the
Church–Turing thesis is dead." Identify the specific confusion, and state what a genuine refutation
would have to look like. *(4 pts)*

&nbsp;

### A3: Decidable, Recognisable, Neither (10 points)

(a) Define **decidable** and **recognisable**, making the difference between them explicit. *(4 pts)*

(b) A language L is decidable **iff** both L and its complement are recognisable. Explain the
intuition behind this in your own words — you do not need a formal proof. *(6 pts)*

*Hint for (b): if you had a recogniser for each, what could you do with both of them at once?*

&nbsp;

### A4: The Halting Problem (16 points)

(a) Reproduce the proof that HALT is undecidable. Give the `paradox` construction and argue both
cases. *(8 pts)*

(b) Explain why the proof requires running `paradox` on **itself**, and what fails if you run it on
some other function instead. *(4 pts)*

(c) Explain the connection to Cantor's diagonalization: what plays the role of the table, what plays
the role of the diagonal, and what plays the role of the flipped element? *(4 pts)*

&nbsp;

### A5: Reduction (18 points)

For each, give a **full reduction proof** from HALT. State the assumption, give the construction,
argue both directions, conclude.

(a) **ALWAYS-CRASHES** = { ⟨M, w⟩ : M raises an exception when run on w }. *(9 pts)*

(b) **EMPTY** = { ⟨M⟩ : M accepts no input at all }. *(9 pts)*

*For (b), be careful about direction — you must build a halting decider out of an `is_empty`
decider, not the other way round.*

&nbsp;

---

## Part B: Code (38 points)

Implement in `ps11.py`, scaffolded by `ps11_starter.py`. Run `python3 ps11_starter.py` to check.
**7 automated tests.**

### B1: A Non-Regular Language (18 points)

Implement `equal_zeros_ones()`: a TM accepting strings over `{0,1}` with an **equal number** of `0`s
and `1`s, **in any order**. So `"0011"`, `"0101"`, `"1100"`, `"011010"` and `""` are accepted;
`"001"`, `"110"`, `"0"` are rejected.

This is harder than `aⁿbⁿ` because the symbols interleave. The cross-off strategy still works, but
you must handle two problems:

- After crossing off a pair you need to return to the left end — and with a one-way-infinite tape,
  **moving left from position 0 silently keeps you at position 0**, so you cannot detect the left end
  by bumping into it. Use a **sentinel**: mark the leftmost cell with a distinct symbol.
- When you cross off a `0`, the matching `1` may be anywhere to the right. Argue to yourself why it
  can never be to the *left*.

*(3 pts of the 18 are for a comment in your code stating the sentinel invariant.)*

### B2: A Reduction, as Code (12 points)

Implement `build_prints_hello_wrapper(f, x, log)`, returning a zero-argument `wrapper` such that
calling `wrapper()` appends `"hello"` to `log` **if and only if** `f(x)` halts.

This is L36 §2's reduction written in Python. Three lines.

In your written answers, explain in two sentences why this construction shows PRINTS-HELLO is
undecidable — and be explicit about which problem is assumed solvable and which is concluded
impossible.

### B3: Classification (8 points)

Fill in `CLASSIFICATIONS` with `"decidable"` or `"undecidable"` for all six questions. Then, **in
this file**, justify each in one sentence, naming either Rice's theorem, a resource bound, or
"syntactic". *(The dict is 4 pts; the justifications are 4 pts.)*

&nbsp;

---

## Submission

Submit:

- This file with Part A and the B2/B3 written justifications completed
- `ps11.py` with all three parts implemented

**Checklist:**

- [ ] `python3 ps11_starter.py` reports **7/7**
- [ ] Both reduction proofs in A5 argue **both directions**
- [ ] B1's sentinel invariant is stated in a code comment
- [ ] B3's six justifications each name a specific reason
- [ ] No `__pycache__` in your submission

**Marking note:** in Part A, a correct conclusion reached by a wrong or incomplete argument earns at
most half marks. This is a proof-based set — the reasoning *is* the answer.

---

*CS 101 · Week 11 · Problem Set 11 · © CSE Department*
