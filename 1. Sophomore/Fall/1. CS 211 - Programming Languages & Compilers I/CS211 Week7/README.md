# CS 211 · Programming Languages & Compilers I
## Week 7: Functional Programming — The Lambda Calculus

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** Lab 7, PS 7, and Quiz 7 (Tuesday, covers Week 6).

> **Midterm 2 is on the Tuesday of Week 8 and covers Weeks 4–7 — this week included.** Lab 7 on
> Friday is the last scheduled contact before it, and PS 7 is due the Friday *after* it.

---

### Why This Week Exists

Because your compiler cannot lower a lambda, and has never been able to.

```cyan
let inc = fn(n: int) -> int { return n + 1; };
```

The parser builds a `Lambda` node and has since Week 2. The type checker gives it the type `fn(int) -> int` and has since Week 3. Then `tac.py` raises `NotImplementedError: Lambda`, and `grep -n Lambda tac.py` returns nothing at all.

That is not a missing `elif`. A function value that can be returned, stored and called later must **capture the variables it mentions** — so those variables cannot live in the frame that made them, which means Week 6's heap, which means the collector needs a `SLOTS` entry for a kind of object we have not defined. **Project 1 lists first-class functions as one of its two hardest options for exactly this reason.**

So before writing that code, this week asks what a function *is*. The answer fits in three lines and computes everything computable.

---

### Learning Objectives

By the end of Week 7, you should be able to:

1. Read and write terms under the **three conventions**, and say why currying means every function takes one argument.
2. Perform **beta-reduction** by hand, and identify a term's normal form.
3. Define **alpha-equivalence** and **eta-conversion**, and say what each is a claim about.
4. Implement **capture-avoiding substitution**, and demonstrate what the naive version computes instead.
5. Connect capture to **Week 3's scope rule**, and to hygienic macros.
6. Explain why **no interpreter can decide** whether a term has a normal form.
7. Distinguish **four reduction strategies** on two independent axes, and predict which terminate.
8. Encode **numbers, booleans, pairs and lists**, and explain the single principle behind all four.
9. Read a cost measurement and say why it **tracks the encoding's shape** rather than the data's size.
10. Explain why `zero`, `false` and `nil` are the same term, and what that says about untyped languages.
11. Derive **`Y g = g (Y g)`**, and explain why `Y` diverges under call-by-value while `Z` does not.
12. State why **`if` cannot be a function** in a strict language, and demonstrate it in Python.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L15 Three Constructs and the One That Is Hard.md` | Syntax, currying, beta/alpha/eta, **substitution and what capture costs**, normal forms, undecidability, two strategies that disagree |
| `lectures/L16 Encodings Recursion and Why Y Hangs in Python.md` | Church encodings, **the seven collisions**, `Y`, **the three-way strategy comparison**, `Z`, thunked `if`, de Bruijn, Turing equivalence |
| `assignments/PS 7 A Lambda Calculus Interpreter.md` | Capture, **call-by-need with sharing**, tree encodings, **mutual recursion** |
| `assignments/QUIZ 7 Week 7 Tuesday.md` | **Covers Week 6.** Six questions, key printed below them |
| `lab/LAB 7 Encoding Data in Pure Lambda Calculus.md` | Reduce by hand, build the data, then break `Y` three times |
| `lab/lam.py` | Terms, capture-avoiding substitution (with a `--naive` switch), four strategies, eta |
| `lab/church.py` | Encodings, decoding, and a self-test that **asserts the collision** rather than hiding it |
| `lab/prelude.lam` | Fifty-five definitions, in three constructs |
| `lab/debruijn.py` | The same calculus with the names taken out, and what that costs |
| `lab/strict.py` | All of it in Python — **no import of `lam.py`**, which is the point |
| `resources/Reading Guide Week 7.md` | TAPL ch. 5 · SICP §1.3, §3.5 · Barendregt ch. 2 · Church 1936 |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**`zero`, `false` and `nil` are the same term.**

```
zero = λf x. x       false = λt f. f       nil = λc n. n
alpha-equivalent: True
```

A function that returns `λf x. x` has returned the number zero, and the boolean false, and the empty list, and **there is no fact of the matter about which**. Nothing in the term records an intention, and no function of the term can recover one.

Compare all fifty-five definitions and there are **seven** such pairs — but they are not all the same kind of fact:

| **theorems** — any correct encoding has them | **collisions** — accidents of this encoding |
|---|---|
| `compose == mult` — multiplication *is* composition | `false == zero` |
| `const == true` — selecting the first *is* what true means | `false == nil` |
| `apply == one` — "do it once" *is* "apply it" | `nil == zero` |
| | `id == unit` |

**The untyped calculus cannot tell those two columns apart**, because it cannot see intent. The obvious remedy is a type system, and **Week 8 measures whether that works** — inference over these same terms separates neither column. What does the job is a *declaration*: `int` and `bool` differ not because their representations do — here they do not — but because somebody said so.

*(Found by brute force over 1485 pairs, four lines of code — Lab 7 Q9.)*

---

### Assessment Reminder

**Labs and quizzes carry no weight**, and both are required. **Quiz 7 is sat Tuesday and covers Week 6. Lab 7 is Friday and covers this week.**

Both are tracked in `5. Academic Registry/2. Gradebook/Year2 Sophomore/Fall/_CS 211 Lab and Quiz Record.md`. **PS 7 is a weighted component** and goes in `CS 211.md`.

**PS 7 is released Wednesday and due Friday of Week 8**, as every problem set in this course has been.

**Project 1, assigned in Week 6, is due Week 11.** By the end of this week you should have chosen a feature and written the three test programs that do not compile yet. If you chose first-class functions, L16 §12's closing paragraph is the design you need.

---

### Connections

**Back:** **Capture is Week 3's scope bug** in a language with three constructs — a variable silently rebound to the wrong binder, with no symbol table to prevent it. **Evaluation order is Week 4's `&&` decision**, generalised: `gen_shortcircuit` lowered `&&` to branches for precisely the reason `if` cannot be a function. **Undecidability is why Week 5's analyses approximate** — liveness *may*, dominance *must*, and neither can be exact.

**Sideways:** **`strict.py` imports nothing from this folder.** Every result about evaluation order is a property of Python, not of our interpreter.

**Forward:** **Week 8 takes the collision above as its opening question**, and finds that inferring types does not separate `zero` from `false` — a *declaration* does. It also finds that typing costs exactly one thing, and it is the one thing §7 of L16 needed. **Week 11's closures are this week's substitution, done with environments instead.** **Project 1's hardest option is a direct application of L16 §12.**

---

*CS 211 · Week 7 · © CSE Department*
