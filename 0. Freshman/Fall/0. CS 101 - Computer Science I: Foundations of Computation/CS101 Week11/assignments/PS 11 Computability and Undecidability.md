# CS 101 · Problem Set 11
## Computability and Undecidability

**Released:** Friday 11 December 2026, 10:00 (after L36) · Week 11
**Due:** Friday 18 December 2026, 17:00 · Week 12 — late penalty from 17:01
**Submission:** `ps11.py` and your answer sheet in `"$CS101/week11"`, committed to the Freshman Fall repo.
**Total:** 100 points · **Expected time:** about 4 hours

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

## Part A: Written Questions (52 points)

### A1: Models and Their Limits (10 points)

(a) State the formal definition of a Turing machine as a 7-tuple, and say in one sentence what each
component does. *(4 pts)*

(b) A student proposes a "Turing machine with two heads on one tape" and claims it is strictly more
powerful. Explain why the claim is wrong, and state what such a machine *does* buy you. *(3 pts)*

(c) Give one language that a finite automaton can recognise and one it cannot, and state the single
structural property that separates them. *(3 pts)*

&nbsp;

### A2: The Church–Turing Thesis (8 points)

(a) State the thesis. *(2 pts)*

(b) Explain why it is not a theorem and cannot be proved. *(3 pts)*

(c) Your colleague says: "Quantum computers can solve problems classical computers can't, so the
Church–Turing thesis is dead." Identify the specific confusion, and state what a genuine refutation
would have to look like. *(3 pts)*

&nbsp;

### A3: Decidable, Recognisable, Neither (10 points)

(a) Define **decidable** and **recognisable**, making the difference between them explicit. *(3 pts)*

(b) HALT is recognisable but not decidable. Give the recogniser in three lines of Python and state
precisely which property it lacks. *(3 pts)*

(c) A language L is decidable **iff** both L and its complement are recognisable. Explain the
intuition behind this in your own words — you do not need a formal proof. *(4 pts)*

*Hint for (c): if you had a recogniser for each, what could you do with both of them at once?*

&nbsp;

### A4: The Halting Problem (12 points)

(a) Reproduce the proof that HALT is undecidable. Give the `paradox` construction and argue both
cases. *(6 pts)*

(b) Explain why the proof requires running `paradox` on **itself**, and what fails if you run it on
some other function instead. *(3 pts)*

(c) Explain the connection to Cantor's diagonalization: what plays the role of the table, what plays
the role of the diagonal, and what plays the role of the flipped element? *(3 pts)*

&nbsp;

### A5: Reduction (12 points)

For each, give a **full reduction proof** from HALT. State the assumption, give the construction,
argue both directions, conclude.

(a) **ALWAYS-CRASHES** = { ⟨M, w⟩ : M raises an exception when run on w }. *(6 pts)*

(b) **EMPTY** = { ⟨M⟩ : M accepts no input at all }. *(6 pts)*

*For (b), be careful about direction — you must build a halting decider out of an `is_empty`
decider, not the other way round.*

&nbsp;

---

## Part B: Code (48 points)

Implement in `ps11.py`, scaffolded by `ps11_starter.py`. Run `python3 ps11_starter.py` to check.
**11 automated tests.**

### B1: A Non-Regular Language (12 points)

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

*(2 pts of the 12 are for a comment in your code stating the sentinel invariant.)*

### B2: Binary Increment (14 points)

Implement `binary_increment()`: add 1 to a binary number written most-significant-bit first.
`"0"` → `"1"`, `"1"` → `"10"`, `"1011"` → `"1100"`, `"111"` → `"1000"`.

The carry is the easy part. The hard part is **overflow**: when the carry propagates off the left
end, the answer is one digit longer than the input, and there is no cell to the left of position 0
to put it in.

You will need to **shift the entire tape right by one cell**. The standard technique is a pair of
states that "carry" a digit: the machine writes the digit it is carrying into the current cell,
picks up the digit that was there, and moves right. Work out on paper what `"111"` should do at each
step before coding.

*Tested on all of n = 0..31.*

### B3: The Recogniser (8 points)

Implement `recognise_halt(machine, tape_input, start_budget=1)` using a **doubling budget**.

It must be **sound**: never return `True` for a machine that does not halt, never return `False` for
one that does. It is permitted not to terminate — that is the point.

In your written answers, state which of sound/complete/total it lacks and on which inputs.

### B4: A Reduction, as Code (8 points)

Implement `build_prints_hello_wrapper(f, x, log)`, returning a zero-argument `wrapper` such that
calling `wrapper()` appends `"hello"` to `log` **if and only if** `f(x)` halts.

This is L36 §2's reduction written in Python. Three lines.

In your written answers, explain in two sentences why this construction shows PRINTS-HELLO is
undecidable — and be explicit about which problem is assumed solvable and which is concluded
impossible.

### B5: Classification (6 points)

Fill in `CLASSIFICATIONS` with `"decidable"` or `"undecidable"` for all six questions. Then, **in
this file**, justify each in one sentence, naming either Rice's theorem, a resource bound, or
"syntactic". *(The dict is 3 pts; the justifications are 3 pts.)*

&nbsp;

---

## Submission

Submit:

- This file with Part A and the B3/B4/B5 written justifications completed
- `ps11.py` with all five functions implemented

**Checklist:**

- [ ] `python3 ps11_starter.py` reports **11/11**
- [ ] Both reduction proofs in A5 argue **both directions**
- [ ] B1's sentinel invariant is stated in a code comment
- [ ] B5's six justifications each name a specific reason
- [ ] No `__pycache__` in your submission

**Marking note:** in Part A, a correct conclusion reached by a wrong or incomplete argument earns at
most half marks. This is a proof-based set — the reasoning *is* the answer.

---

*CS 101 · Week 11 · Problem Set 11 · © CSE Department*
