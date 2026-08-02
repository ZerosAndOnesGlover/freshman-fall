# CS 101 · Week 11
## Computability: What Cannot Be Computed

---

## Overview

The course's turning point. Weeks 6–10 asked how *efficiently* problems can be solved. Week 11 asks
whether they can be solved **at all**, and proves that some cannot — a claim about every program
that will ever be written, not about our current cleverness.

The week also pays off a debt from Week 9: L30's claim that no regular expression can parse HTML was
stated as a theorem and deferred. L34 proves the model-level version on day one.

---

## Contents

```
CS101 Week11/
├── lectures/
│   ├── L34 Models of Computation.md
│   ├── L35 Decidability and the Halting Problem.md
│   └── L36 Reduction and the Landscape of Undecidability.md
├── assignments/
│   ├── QUIZ 11 Week 11 Wednesday.md
│   ├── PS 11 Computability and Undecidability.md
│   └── ps11_starter.py
├── lab/
│   ├── LAB 11 Building a Turing Machine.md
│   └── tm_lab_starter.py
├── resources/
│   └── Reading Guide Week 11.md
└── solutions_instructor/
    ├── QUIZ 11 Solutions.md
    ├── LAB 11 Solutions.md
    ├── PS 11 Solutions.md
    ├── tm_lab_solution.py
    └── ps11_solution.py
```

> **Note:** Week 11 is the first week with instructor keys for *all three* assessments (quiz,
> problem set, lab). Weeks 9 and 10 currently have lab solutions only — see "Known gaps" below.

---

## Schedule

| Day | Session | Topic |
|---|---|---|
| Tue | L34 | Models of computation; finite automata and their ceiling; the Turing machine; Church–Turing; universality |
| Wed | Quiz 11 + L35 | Decidable vs recognisable; **the halting problem**; diagonalization; sound/complete/total |
| Thu | Lab 11 | Build a Turing machine simulator; meet the halting problem experimentally |
| Fri | L36 | Reduction; the landscape of undecidable problems; Rice's theorem; what it means for real tools |

**Quiz 11** (Wednesday, 10 min) covers **Week 10** — files, exceptions, atomic writes.
**PS 11** released Friday, due Friday of Week 12.

---

## Learning Objectives

By the end of Week 11 you should be able to:

1. State the formal definition of a Turing machine and build one for a given language
2. Explain the Church–Turing thesis, why it is not a theorem, and what would refute it
3. Distinguish **decidable** from **recognisable**, and give an example separating them
4. Reproduce the halting-problem proof, including both cases of the contradiction
5. Explain the proof as diagonalization, and identify the table, diagonal, and flip
6. Construct a reduction from HALT to a new problem — **in the correct direction**
7. Apply Rice's theorem to classify a behavioural question as undecidable
8. Explain why real static analysers work despite the theorem, naming which of
   sound/complete/total each one drops

---

## Key Results

| Result | Statement |
|---|---|
| **Finite automata ⊊ Turing machines** | No FA recognises `aⁿbⁿ`; a TM does |
| **Church–Turing thesis** | Every model of effective computation coincides with TMs |
| **Universality** | One machine simulates all machines — the stored-program computer |
| **Halting problem** | HALT is undecidable (Turing, 1936) |
| **HALT is recognisable** | Just run it — proves *yes*, never proves *no* |
| **Reduction** | A ≤ B and A undecidable ⟹ B undecidable |
| **Rice's theorem** | Every non-trivial semantic property is undecidable |

---

## Verification

All code and claims in this week's materials were verified by execution:

- The Turing machine simulator and all example machines (unary increment, even-parity, `aⁿbⁿ`,
  ends-in-0, equal 0s and 1s, binary increment) run and produce the documented traces
- `aⁿbⁿ` on `"aabb"` takes exactly the 13 steps shown in L34 §3 and Lab 11 Ex 4.4
- `binary_increment` verified on all of n = 0..31
- Step-count growth for `aⁿbⁿ` verified quadratic with closed form **2n² + 2n + 1** (checked n=1..12)
- Σ(3) = 6 and S(3) = 21 verified by exhaustive search — and confirmed to be achieved by
  **different machines** (6-ones champion halts in 13 steps; 21-step champion writes 4 ones)
- `tm_lab_starter.py` → 0/11; `tm_lab_solution.py` → **11/11**
- `ps11_starter.py` → 0/11; `ps11_solution.py` → **11/11**

---

## A Note on Where Solutions Live

Weeks 9 and 10 embed their instructor keys **inside** the quiz and problem-set files, under an
"Answer Key (Instructor Copy)" heading. Week 11 instead keeps them as separate files in
`solutions_instructor/`, so that the student-facing documents can be distributed as-is.

Both conventions are in use across the course and both are complete — no assessment is missing a
key. Week 11's split is the safer default for anything handed out electronically.

---

## Connections

**Back:**
- **L30 (Week 9)** — "regex cannot parse nested structure" is proved at model level in L34 §2
- **Week 7** — "tests show the presence of bugs, not their absence" is L35 §5's semi-decidability
- **Week 6** — Big-O is *complexity*; this week is *computability*. L34 §4 keeps them apart
- **L01** — the von Neumann architecture is universality, which L34 §5 explains

**Forward:**
- **CS 301** — the pumping lemma, the Chomsky hierarchy, P vs NP
- **CS 220** — why parsers layer regex under grammars
- **Week 12** — synthesis, final review, Project 2

---

*CS 101 · Week 11 · © CSE Department*
