# PROG 202 · Functional & Logic Programming
## Week 1: Types, Algebraic Data Types, and Pattern Matching

**Credits:** 3 (2 lecture + 1 lab) · **Prerequisites:** PROG 102, CS 211
**Assessment for this course (overall):** Problem Sets 40%, Projects 30%, Midterm 15%, Final 15%
**This week's deliverables:** PS 1, and **Quiz 1 on Tuesday** — the first graded-adjacent work of the
term. **There is no lab session this week**; Lab 1 is sat on the Wednesday of Week 2.

---

### Why This Week Exists

Because Week 0's `Session` was a lie, and it is measurable.

`type Session = (String, String, String, Int, Int)` — three strings in a row, then two `Int`s. **Of
the 120 ways to order those five fields, twelve type-check, and eleven of them are wrong.** That is
not an estimate; L03 §4 generates all 120 orderings, compiles every one, and counts.

This week takes the eleven down to **one**, and the interesting part is why it is not zero. Sum types
kill the typos. Newtypes kill the confusions. Records make the code readable. And then `start` and
`end` are both `Minutes`, so **one wrong ordering remains, and no type can close it** — that one needs
a smart constructor, which needs a module boundary to mean anything at all.

**The skill being taught is not `data` syntax.** It is knowing which defect each tool catches, and
noticing when the tools have run out.

---

### Learning Objectives

By the end of Week 1, you should be able to:

1. **Count the values of a type**, and state the three rules: products multiply, sums add, functions
   exponentiate.
2. Declare a sum type, a product type, and a type that is both, and say which of `type`, `newtype`
   and `data` you want and what each costs.
3. **Say what `type` checks.** *(Nothing.)*
4. Use `Maybe` and `Either` as the ordinary data types they are, and explain how `Maybe` replaces null.
5. **Write a pattern for a shape and a guard for a value**, and say which of the two a given question
   needs.
6. Read GHC's exhaustiveness warning, and **explain why it can name the missing case for a finite type
   and cannot for `String`.**
7. Name two ways to crash that `-Wall` on this GHC does **not** warn about, and give the design change
   that prevents each.
8. **Design a type so that a meaningless combination of fields cannot be written**, and apply the test:
   can you write down a value a reviewer would call impossible?
9. Write a smart constructor, and **say why it is worthless without an export list.**
10. Explain what type inference does — fresh variables, constraints, unification — and what *principal
    type* means.
11. **Say what a type signature buys**, with the evidence: without one, GHC blamed the literal `150`
    for a mistake four lines away in another function.
12. Declare a recursive data type, write an evaluator over it, and recognise that you have just started
    Project 1.

---

### New Syntax and Symbols This Week

Week 0's ten are assumed. Full reference:
[[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]].

| Symbol | Said out loud | Means |
|---|---|---|
| `data T = A \| B` | **"data"**, `\|` is **"or"** | A new type with two constructors. `\|` separates alternatives |
| `newtype T = T X` | **"newtype"** | A new type wrapping exactly one field. **Erased at compile time** — free |
| `type T = X` | **"type synonym"** | *Not* a new type. An abbreviation, checked for nothing |
| `deriving (…)` | **"deriving"** | Ask GHC to write the instances. `Eq Ord Show Enum Bounded` this week |
| `T { f = v }` | **record syntax** | Construction or update by field name. `s { day = Wed }` is a **new** value |
| `T { f = p }` | **record pattern** | Match a record, bind one field, ignore the rest |
| `x@p` | **"as-pattern"** | Bind the whole value to `x` *and* match it against `p` |
| `case e of …` | **"case"** | Pattern match in the middle of an expression |
| `\| g = e` | **"guard"**, "such that" | A boolean condition on an equation's clause. `otherwise` is a library `True` |
| `minBound`, `maxBound` | — | From `Bounded`. `[minBound .. maxBound]` is **every value of a finite type** |
| `Module (T)` vs `Module (T (..))` | — | Export the **type** alone, or the type **and its constructors**. §5 of the lab is this one character |

**Two namespace facts that cause real confusion.** `data Session = Session …` declares *two* things
called `Session` — a type and a constructor — and they live in separate namespaces, which is why an
export list can let one through and not the other. And **a record accessor is an ordinary function**,
`course :: Session -> Course`, not a member-access syntax, which is why `map course ts` works.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L03 Types Algebraic Data Types and Inference]] | Types as sets, and the arithmetic; `data`/`newtype`/`type`; `Maybe` and `Either`; **the 120-ordering measurement — 11 wrong accepted, then 1**; Hindley–Milner; **a signature as a firewall, and the literal `150`** |
| [[L04 Pattern Matching and Unrepresentable States]] | Every pattern form; guards against patterns; **exhaustiveness: `SEM` named for `Kind`, an ellipsis for `String`**; two crashes `-Wall` misses here; making bad states unrepresentable; the smart constructor and the module boundary; `Expr` and `eval` |
| [[LAB 1 Algebraic Data Types and Exhaustive Matching]] | Rewrite `sched`'s types, then find the hole and close it. **Wednesday of Week 2, 13:00–14:50** |
| `lab/Sched.hs`, `Main.hs`, `Break.hs`, `Makefile` | Eight TODOs, a driver you do not edit, and **a file that must fail to compile** |
| [[PROG202 Week1/assignments/Problem Set 1\|Problem Set 1]] | Five questions, fifteen parts, 100 points, about three hours, due **Friday of Week 2** |
| [[PROG202 Week1/assignments/QUIZ 1 Week 1 Tuesday\|QUIZ 1]] | Ten minutes, Tuesday, covers **Week 0**. Prints its own key |
| [[PROG202 Week1/resources/Reading Guide Week 1\|Reading Guide Week 1]] | Hutton 3, 4 and **8 — the chapter to read twice**; and §8.6's tautology checker, which is Project 1 in miniature |
| `resources/orderings.py` | The 120-ordering experiment, all three designs. Really does run `ghc` 360 times |
| `resources/exhaustive.hs` | The same function over `Kind` and over `String`, each missing a case |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**Types do not catch bugs. Types make bugs unwriteable — and then stop.**

The measurement is the argument. Eleven wrong field orderings compiled happily in Week 0. After this
week's redesign, **one** does: `start` and `end` exchanged, because they are both `Minutes`. No amount
of further type cleverness closes it that anyone sustains — the version that does
(`orderings.py strict`) makes `start a < end b` **fail to compile**, so you add a conversion, and the
protection you paid for is gone.

So the last hole is closed by a **value** check in a smart constructor. And a smart constructor is a
*convention* rather than a *guarantee* until the module exports it **instead of** the real constructor:
change one character, `Session` to `Session (..)`, and `./break` cheerfully prints a session running
from 12:15 to 11:00 and exits 0.

**The hierarchy, in order of what each can promise:** a distinct type stops the wrong kind of thing; a
sum type stops an impossible combination; `-Wall` stops a forgotten case, *if the type is finite*; a
smart constructor stops a bad value; **and only a module boundary makes that last one true.**

That final clause is the part everybody leaves out, and it is what Lab 1 §5 exists to prove.

---

### Assessment Reminder

**Labs and quizzes carry no weight.** The curriculum's assessment line sums to 100% without them.

They are still required. **The lab is checked off by the TA in the session**, and a second unexcused
absence costs a letter grade. **Quiz *N* covers Week *N−1***, runs ten minutes at the start of
**Tuesday's** lecture in Weeks 1–11, and prints its own answer key.

> **There is no lab in Week 1.** Lab 0 was sat on the Friday that closed the ten-day Week 0, and
> **Lab 1 is sat on the Wednesday of Week 2** — this course's labs lag a full week from here on,
> because the lab is Wednesday and the lectures are Tuesday and Thursday.
>
> **Quiz 1, on the Tuesday of this week, is the first one.** It covers Week 0 and it is ten minutes.

Both are tracked in [[_PROG 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0's `Session` is the thing this week deletes**, and Week 0's `weekdays` list is
replaced by `[minBound .. maxBound]` — a list that could disagree with the data, replaced by something
there is nothing to disagree with. L03 §5's firewall measurement is Lab 0 §2(c) with the numbers
attached.

**Sideways:** **CS 211 last term described the algorithm this week relies on.** Its Week 3 lecture on
Hindley–Milner is the theory; L03 §5 is what it feels like when it reports an error in the wrong place.
**CS 212 this term is the same argument about tests:** its rule that 95% coverage with a 30% mutation
score is worse than 75% with 75% is L04 §3's point — what matters is not how much you checked but
whether the bad case was possible.

**Forward:** **Week 2 takes the recursion out** of everything you wrote today — `pairs`, the
comprehensions, `sum (map duration ts)` are all the same three shapes of loop, and Week 2 names them.
**Week 6 explains `traverse id`**, which Lab 1 makes you use and asks you to guess at; keep the guess.
**And `Expr`/`eval` in L04 §4 is Project 1's first commit** — due Friday of Week 7, and every week from
here adds one constructor and one equation.

---

*PROG 202 · Week 1 · © CSE Department*
