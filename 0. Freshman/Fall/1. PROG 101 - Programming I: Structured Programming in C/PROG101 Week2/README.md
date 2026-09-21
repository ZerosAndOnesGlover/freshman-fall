# PROG 101 · Week 2
## Operators, Expressions, and Control Flow

---

## This Week

Week 1 established what a value *is* — its type, its size, its bit pattern. This week is about what
you can *do* to values, and it splits into two halves that look unrelated and are not.

The first half is operators: the full precedence table, the bitwise operators, and the specific
places where C parses your expression differently from how you read it. The second half is control
flow: `if`, `switch`, and the three loop forms, plus the Böhm–Jacopini result that these are
*sufficient* — any computable control structure can be built from sequence, selection, and iteration.

Between them sits Lecture 2, which is the one students remember. C does not specify the order in
which subexpressions are evaluated, and it declares some expressions to have **no meaning at all**.
`i = i++` is not compiler-dependent; it is undefined, and a compiler may legally assume the line
never runs. Learning to recognise that category — and to reach for `-Wall` and UBSan rather than for
"but it printed the right answer" — is the real content of the week.

| Day | Session | Topic | Duration |
|-----|---------|-------|----------|
| Tue 6 Oct | **Quiz 1** + Lecture 1 | Operators, expressions, and bit manipulation | 50 min |
| Wed 7 Oct | Lecture 2 | Evaluation order and undefined behaviour | 50 min |
| Thu 8 Oct | Lecture 3 | Control flow — `if`, `switch`, `while`, `for` | 50 min |
| Mon 12 Oct, 15:00 (Week 3) | **Lab 2** | Operators, evaluation order, and control flow | 2 hours |

**Problem Set 2** released Friday 9 October, due Friday 16 October, 17:00.

---

## Contents

```
PROG101 Week2/
├── README.md
├── lectures/
│   ├── Lecture 01 Operators Expressions Bits.md
│   ├── Lecture 02 Evaluation Order and Undefined Behaviour.md
│   └── Lecture 03 Control Flow.md
├── assignments/
│   └── Problem Set 2.md
├── lab/
│   └── LAB 2 Operators Evaluation Control Flow.md
├── quizzes/
│   └── QUIZ 1.md
├── resources/
│   └── Week 2 Operator and Control Flow Reference.md
└── solutions_instructor/
    └── LAB 2 Solutions.md
```

---

## Learning Objectives

1. Read any C expression the way the compiler parses it, and place parentheses where precedence is counter-intuitive
2. Use the bitwise operators to set, clear, toggle and test flags in an `unsigned` bitset
3. Distinguish **well-defined**, **unspecified**, **implementation-defined**, and **undefined** behaviour, and classify a given expression
4. State what a sequence point is and identify expressions that violate the modification rule
5. Use `-Wall -Wextra -Werror` and `-fsanitize=undefined` to catch what testing cannot
6. Write and trace `if`, `switch`, `while`, `do-while`, and `for`, including `break` and `continue`
7. Implement a character-driven state machine using `switch` inside a read loop

---

## Key Facts

| | |
|---|---|
| Bitwise binds **looser** than comparison | `a & b == c` parses as `a & (b == c)` |
| `1 << 2 + 3` | is `1 << 5` = **32**, not 7 |
| Division truncates **toward zero** | `-7 / 2 == -3`, and `-7 % 2 == -1` |
| Sign of `%` follows the **dividend** | unlike Python, which floors |
| Always `1u << n` for flags | `1 << 31` is undefined for signed `int` |
| Test a flag with `(p & F) != 0` | `p & F` returns the mask, not `1` |
| `i = i++` | **undefined** — not "compiler-dependent" |
| `-Wall` includes `-Wsequence-point` | which catches exactly that |
| Undocumented `switch` fallthrough | is an **error** under `-Werror` |
| `do-while` | runs its body at least once |
| `getchar()` returns `int` | so `EOF` differs from every valid `char` |

---

## Connections

**Back:** Week 1's integer representation is what makes the bitwise operators meaningful, and what
makes `1 << 31` undefined for a signed type. Week 1's `sizeof` explains why shift counts have limits.

**Forward:** Week 3 turns control flow into *functions*, adding the call stack. The undefined
behaviour vocabulary built here recurs constantly — in Week 4's buffer overflows, Week 5's null and
dangling pointers, Week 6's use-after-free, and Week 10's macro traps. The state machine in Lab 2 is
the same shape as the tokeniser you will write in Week 8 for parsing files.

**Sideways:** CS 101 is covering conditionals and loops in Python this week. The control structures
are the same; the difference is that C lets you write expressions with no defined meaning, and
Python does not.

---

*PROG 101 · Week 2 · © CSE Department*
