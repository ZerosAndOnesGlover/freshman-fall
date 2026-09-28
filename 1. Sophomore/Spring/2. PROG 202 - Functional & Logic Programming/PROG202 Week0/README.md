# PROG 202 · Functional & Logic Programming
## Week 0: Purity, Haskell, and GHCi

**Credits:** 3 (2 lecture + 1 lab) · **Prerequisites:** PROG 102, CS 211
**Assessment for this course (overall):** Problem Sets 40%, Projects 30%, Midterm 15%, Final 15%
**This week's deliverables:** Lab 0 and PS 0. **No quiz** — Quiz 1, in Week 1, covers this week.

> **Week 0 is ten days long**, running Jan 12 to Jan 23. It absorbs orientation and add/drop, and
> Week 1 — when graded work begins — opens Jan 26. You get both lectures and the lab.
>
> **This course has two lectures a week, not three.** Tuesday and Thursday, 11:00–12:15, TH 205.
> Same contact minutes as CS 202 or CS 212; half as many sessions, each half again as long. There is
> no Wednesday lecture to catch anything in — Wednesday is the lab.

---

### Why This Week Exists

Because you have spent two years learning to change things, and the next seven weeks are in a
language where nothing changes.

**PROG 202 is about the two things a program can be when it is not a list of instructions.** Haskell
is an expression to be evaluated; Prolog, from Week 8, is a set of facts to be searched. Neither has
an assignment statement, and the interesting question is not how you cope without one — it is **what
the language gets in exchange.**

This week answers that concretely and with numbers. Purity buys the compiler an optimisation it
cannot otherwise have: measured here, GCC loses common-subexpression elimination to a single
`calls++` and pays **0.44 seconds** for it, while GHC cannot lose it because the line is unwritable.
And purity costs something too, which you also measure: **naming a list you traverse twice costs
273 MB where writing it out twice costs 44 KB.**

It also installs the three habits the rest of the term assumes: **`:t` before you guess, `:sprint`
when you are confused about evaluation, and `+RTS -s` before you believe a performance claim.**

---

### Learning Objectives

By the end of Week 0, you should be able to:

1. State referential transparency precisely, and decide whether a given expression has it — including
   the case that surprises everyone, `getLine`.
2. **Say what purity buys a compiler**, with the measurement: 0.44 s against 0.88 s, and the one line
   of C that made the difference.
3. Explain why immutability is affordable, from the measured cost of a persistent insert: **1.86×
   for a map 1,000× larger**.
4. Read a type signature aloud, and say how many arguments a function with a `=>` in its type takes.
5. **Name the ten symbols** `::` `->` `=>` `=` `_` `:` `++` `.` `$` `<-` and say what each does.
6. Reduce an expression by substitution, by hand, in call-by-value and call-by-name order, and say
   which count call-by-need achieves.
7. Use `:t`, `:i`, `:sprint` and `:set +s` without looking them up.
8. **Read `:sprint` output**: say what `xs = [_,_,_,_,_]` means and what forced it.
9. Compile with `-Wall -O2`, and say why a type signature is a firewall rather than a comment.
10. **Use `+RTS -s`**, and distinguish *allocated* from *maximum residency* — they answer different
    questions and Week 3 depends on the difference.
11. Say why `runghc` timings are worthless, with the ratio: **57×**.
12. Write a small program over a list of tuples, and say what is wrong with the type you used.

---

### New Syntax and Symbols This Week

**Every new language in this course gets its punctuation taught explicitly**, because you cannot look
up a symbol whose name you do not know.
[[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]] is the full
reference for Haskell and it is required reading this week. What Week 0 actually uses:

| Symbol | Said out loud | Means |
|---|---|---|
| `::` | **"has type"** | `x :: Int`. Not C++'s scope operator |
| `->` | **"to"** | `Int -> Bool`, a function type. Right-associative |
| `=>` | **"such that"** | A *constraint*, not an argument. `Eq a => a -> [a] -> Bool` takes **two** arguments |
| `=` | **"is defined as"** | An equation. **Never assignment** |
| `_` | **"wildcard"** | Matches anything, binds nothing |
| `:` | **"cons"** | `1 : [2,3]`. The only list constructor |
| `++` | **"append"** | O(n) in its left argument |
| `.` | **"compose"** | `(f . g) x` = `f (g x)`, right to left |
| `$` | **"apply"** | Lowest precedence. Exists to delete brackets |
| `\x -> e` | **"lambda"** | The `\` is meant to look like a λ |
| `[ e \| x <- xs, p ]` | **"list comprehension"** | `<-` here is **"drawn from"** |
| `<-` (in `do`) | **"bind"** | Perform an action, name its result. **Not assignment** |
| `--`, `{- -}` | — | Line and block comment. `--` needs a space if a symbol follows |
| `where`, `let … in` | — | Local definitions, to an *equation* and to an *expression* respectively |

**Indentation is syntax.** A block's items all start in the same column; further right continues the
previous item; further left ends the block. Tabs are a mistake and `-Wall` says so.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L01 Purity and What It Buys]] | Referential transparency; **CSE measured at 0.44 s vs 0.88 s in C**; persistent insert at **1.86× for 1,000× the data**; the aliasing bug with no Haskell translation; `IO` as a type |
| [[L02 GHCi Types and Evaluation by Substitution]] | The shape of a program; substitution by hand; `:t` `:i` `:sprint` `:set +s`; **`runghc` 57× slower than `-O2`**; **44 KB against 273 MB**, and the difference between retention and fusion |
| [[LAB 0 GHCi and the Shape of a Haskell Program]] | GHCi as a laboratory, `<<loop>>`, and `sched`. **Friday of Week 0, 13:00–14:50** |
| `lab/Shape.hs`, `lab/Sched.hs`, `lab/Makefile` | Fifteen lines of program anatomy, the term's running example, and the build |
| [[PROG202 Week0/assignments/Problem Set 0\|Problem Set 0]] | Five questions, fifteen parts, 100 points, about three hours, due **Friday of Week 1** |
| [[PROG202 Week0/resources/Course Overview Syllabus\|Course Overview Syllabus]] | **Read this in full in Week 0** — assessment, the lab lag, and ten deviations including the one about QuickCheck |
| [[PROG202 Week0/resources/Haskell Syntax and Symbols\|Haskell Syntax and Symbols]] | **The punctuation reference for the whole course.** Keep it open for three weeks |
| [[PROG202 Week0/resources/Reading Guide Week 0\|Reading Guide Week 0]] | Which of Hutton 1–5 is this week, and the three places *Real World Haskell* disagrees with GHC 9.4.7 |
| `resources/cse.c`, `cse.hs`, `share2.hs`, `persist.hs`, `primes.hs`, `alias.py`, `loopx.hs` | Every program whose numbers appear above |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**A name is not free.**

In every language you have used, giving a value a name is the cheapest thing you can do, and
computing something twice is the expensive thing. This week both halves reverse.

`sum [1..10⁷]` twice over costs **44 KB**. The *same computation*, with the list named once and used
twice, costs **273 MB** — and it costs that at `-O0` and at `-O2` alike, because the cost is
**retention**: a name must denote one value, so the whole list has to stay alive between the two
traversals. Worse, naming it also switches off the optimisation that would have deleted the list
entirely, which is why the unnamed version allocates 53 KB where the named one allocates 640 MB.

**This is not a wart and it is not an argument against laziness.** It is what happens when *how much
memory a program uses* stops being visible in its source text. C shows you: an array of ten million
`int` is forty megabytes, and the declaration says so. Haskell does not, and `+RTS -s` is the
instrument that does instead.

Week 3 is titled *Lazy Evaluation*. It is really about this paragraph.

---

### Assessment Reminder

**Labs and quizzes carry no weight.** The curriculum's assessment line sums to 100% without them, and
no percentage has been invented to fill the gap.

They are still required. **The lab is checked off by the TA in the session**, and a second unexcused
absence costs a letter grade. **Quiz *N* covers Week *N−1***, runs ten minutes at the start of
**Tuesday's** lecture in Weeks 1–11, and prints its own answer key.

> **This course's lab lags a full week, because the lab is on Wednesday and the lectures are Tuesday
> and Thursday.** Lab *N* covers Week *N* and is sat on the **Wednesday of Week *N+1***. Lab 0 is the
> exception: it is sat on the **Friday that closes the ten-day Week 0**, at **13:00–14:50** — this
> course's ordinary lab time on an unusual day, after CS 202's Week 0 lab has vacated the morning.
> **There is no lab in Week 1.**
>
> **CS 202 lags too, on Tuesdays.** Read each course's own header rather than carrying a habit
> between them.

Both are tracked in [[_PROG 202 Lab and Quiz Record]].

---

### Connections

**Back:** **PROG 102 is assumed and not re-taught** — you can write and debug a recursive function
without help, and that is the only thing this week needs. **CS 211 supplies the vocabulary**: you
already know what an abstract syntax tree is and that a type system is a checkable set of rules.
This course is where those rules become a *logic you can compute in*, and Week 1's type inference is
the algorithm CS 211 described and did not implement.

**Sideways:** **CS 212 runs alongside and wants the same thing from a different direction.** Its
argument that 95% line coverage with a 30% mutation score is worse than 75% with 75% is Week 11's
argument about properties versus examples, made about tests rather than about specifications. And
its `confirm_booking` — 487 lines, cyclomatic complexity 94 — is L01 §7's "separate the computation
from the effect" as a cautionary tale.

**Forward:** **Week 3 is this week's last table, explained.** **Week 8 changes languages** and the
punctuation reference starts again from nothing. **CS 331 (AI) next year is Weeks 8–10 continued** —
unification and constraint propagation are its first month — and **CS 321 (Databases)** is Prolog's
semantics with a different syntax, since Datalog is Prolog without function symbols.

---

*PROG 202 · Week 0 · © CSE Department*
