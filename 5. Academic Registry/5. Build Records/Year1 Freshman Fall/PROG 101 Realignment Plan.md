# PROG 101 — Curriculum Realignment Plan

**Decision:** the Year 1 curriculum document (`CSE_Year1_Freshman_Curriculum.docx`) is authoritative.
Built content is redistributed to match its week numbering.

**Why this was needed.** Built Week 1 covered two docx weeks (Types/Memory *and* Operators/Control
Flow). Every later week inherited that compression, so by Week 5 the built course was teaching
File I/O where the curriculum specifies Pointers I — a two-to-three week drift. Built Week 7
(hash tables) is not in the PROG 101 curriculum at all; it duplicates CS 101 Week 8.

---

## Target structure (from the docx)

| Week | Docx topic | Source |
|---|---|---|
| 0 | The C Compilation Model | built W0 — **unchanged** |
| 1 | Types, Variables, and the Memory Model | built W1 L1 + 2 new lectures |
| 2 | Operators, Expressions, and Control Flow | built W1 L2–L3 + 1 new lecture |
| 3 | Functions and Structured Programming | built W2 L1 + built W3 L1 + 1 new |
| 4 | Arrays and Strings | built W2 L2–L3 + 1 new lecture |
| 5 | Pointers I: The Fundamental Abstraction | built W3 L2 + 2 new lectures |
| 6 | Pointers II: Dynamic Memory | built W3 L3 + 2 new lectures |
| 7 | Structures, Unions, and Enumerations | built W4 — **wholesale move** |
| 8 | File I/O and the UNIX File Model | built W5 — **wholesale move** |
| 9 | Recursion in C and Stack Mechanics | built W6 — **wholesale move** |
| 10 | The C Preprocessor and Macros | **build new** |
| 11 | The C Standard Library and System Programming Preview | built W8 (function pointers, `qsort`) + new |
| 12 | Software Engineering in C: Style, Testing, Debugging | **build new** |

---

## Disposition of built Week 7 (hash tables)

Not in the PROG 101 curriculum, and duplicates CS 101 Week 8. **Not deleted** — moved to
`Appendix - Hashtables (not in curriculum)/` so the work is preserved and clearly marked as
off-syllabus. It remains usable as optional/elective material.

---

## Stages

**Stage 1 — wholesale relocations** *(mechanical, unambiguous)*

| From | To |
|---|---|
| `PROG101 Week4` (Structs/Unions/Linked Lists) | `PROG101 Week7` |
| `PROG101 Week5` (File I/O, UNIX model) | `PROG101 Week8` |
| `PROG101 Week6` (Recursion, D&C, Trees) | `PROG101 Week9` |
| `PROG101 Week7` (Hash tables) | `Appendix - Hashtables (not in curriculum)` |
| `PROG101 Week8` (Function pointers — new) | `PROG101 Week11` |

Plus rewriting every prose cross-reference to those weeks, inside PROG 101 **and** the eight
references from CS 101.

**Stage 2 — split weeks** *(content authoring)*

Built W1, W2 and W3 each spanned more than one docx week. Splitting them leaves gaps that must be
filled so every week has three lectures. Prose references to built Weeks 1–3 cannot be remapped
mechanically, because a reference to "Week 1" may mean either new W1 or new W2 depending on
subject; these are resolved by hand during authoring.

**Stage 3 — new weeks**

W10 (Preprocessor and Macros), W11 (Standard Library — absorbs the already-written function-pointer
lectures), W12 (Software Engineering in C).

---

## Assessment weights

The docx and the registry agree, so no change is needed:

> **Labs 20% · Problem Sets 35% · Midterms 25% · Final 20%**

---

## Cross-reference remapping table

For Stage 1. Applies to prose of the form "Week N" inside PROG 101, and "PROG 101 Week N" elsewhere.

| Old week | New week | Subject |
|---|---|---|
| 4 | 7 | structures, unions, enums, linked lists |
| 5 | 8 | file I/O, UNIX file model, serialization |
| 6 | 9 | recursion, divide & conquer, binary trees |
| 7 | — | hash tables (moved to appendix; references need rewording) |

Weeks 0–3 keep their numbers for now; their references are settled in Stage 2.

---

*PROG 101 · Realignment Plan · generated during the Year 1 curriculum audit*

---

## Stage 2 — detailed lecture mapping

Splitting is mostly **redistribution of existing sections**, not new authoring. Each source lecture
is section-rich enough to divide, then expand.

### W1 · Types, Variables, and the Memory Model
Source: old W1 L01 (9 sections, 3547w) — split three ways.

| New | Sections drawn from L01 |
|---|---|
| L01 Types and the Memory Model | §1 What Is a Type, §2 Memory Big Picture, §7 `sizeof`, §8 Declaration/Init/Scope |
| L02 Integer Representation | §3 Fundamental Integer Types, §4 Two's Complement, §5 Integer Overflow |
| L03 Floating-Point and Conversions | §6 Floating-Point, §9 Type Conversions |

### W2 · Operators, Expressions, and Control Flow
Sources: old W1 L02 (Operators) and L03 (Control Flow) move wholesale. One new lecture.

| New | Source |
|---|---|
| L01 Operators and Expressions | old W1 L02 |
| L02 Evaluation Order and Undefined Behaviour | **new** — sequence points, order of evaluation, promotion |
| L03 Control Flow | old W1 L03 |

### W3 · Functions and Structured Programming
Sources: old W2 L01 (Functions/Scope/Callstack) and old W3 L01 (Structured Programming).

| New | Source |
|---|---|
| L01 Functions and Pass-by-Value | old W2 L01 §1–5, §8–9 |
| L02 The Call Stack and Scope | old W2 L01 §6–7, expanded |
| L03 Structured Programming and Multi-File Design | old W3 L01, **minus §4 function pointers** (now W11) |

### W4 · Arrays and Strings
Sources: old W2 L02 (Arrays) and L03 (Strings) move wholesale. One new lecture.

| New | Source |
|---|---|
| L01 Arrays | old W2 L02 |
| L02 Strings in Depth | old W2 L03 |
| L03 Buffer Safety and Bounded String Functions | **new** |

### W5 · Pointers I: The Fundamental Abstraction
Source: old W3 L02 (9 sections, 3313w) — split three ways.

| New | Sections |
|---|---|
| L01 What a Pointer Is | §1, §2, §4 |
| L02 Pointers, Arrays, and Arithmetic | §5, §6 |
| L03 `const`, NULL, and Pointer Errors | §3, §7, §8, §9 |

### W6 · Pointers II: Dynamic Memory
Source: old W3 L03 (8 sections, 2923w) — split three ways.

| New | Sections |
|---|---|
| L01 The Process Memory Map and `malloc` | §1, §2, §3 |
| L02 `realloc`, `free`, and Ownership | §4, §5, §8 |
| L03 Valgrind and Building a Dynamic Array | §6, §7 |

### Assessments

Problem sets, labs and quizzes were written per old week and cover the old groupings. They are
re-scoped to their new weeks as the lectures settle; a lab that spanned two docx weeks is split or
re-anchored to whichever week now owns its material.

