# PROG 202 · Reading Guide · Week 0
## Hutton 1–2, Real World Haskell 1–2, and what to actually do with them

---

The curriculum sets Week 0 as *"Functional Programming Philosophy; Haskell Introduction; GHCi"* and
names three books. **This guide says which parts are Week 0, which are Week 1, and which are
reference material you should know how to find rather than know.**

**Two lectures a week means the reading is not optional here the way it is in a three-lecture
course.** There is no Wednesday session to catch the overflow. Budget **two hours** for this week's
reading; it is genuinely two hours, not the eight that Week 0 of PROG 201 asked for.

---

## Hutton — *Programming in Haskell*, 2nd ed.

| Chapter | Now? | Why |
|---|---|---|
| **1. Introduction** | **Read** | 12 pages. §1.1–1.5 is L01, written better. **§1.7's exercises are the best five minutes of the week** |
| **2. First steps** | **Read** | GHCi, the standard prelude, function application, naming. This is L02 §1 and §3 |
| 3. Types and classes | **Skim §3.1–3.3 only** | Week 1. But skim it now so `Num a =>` is not a shock on Tuesday |
| 4. Defining functions | **§4.1–4.4** | Guards, pattern matching, lambdas. Lab 0 uses all four |
| 5. List comprehensions | **§5.1–5.2** | `Sched.hs` is built out of these. Ten pages |
| 6. Recursion | Week 2 | Read it if you have time — it makes Week 2's folds land better |
| 7. Higher-order functions | Week 2 | **This is Week 2**, and it is the most important chapter in the book |
| 8. Declaring types and classes | Week 1 | |
| 9–11 | Later / never | Worked examples. Good, and not scheduled |
| 12. Monads and more | Weeks 4–6 | Do not read ahead. It will not help and it will discourage you |
| **14. Foldables and friends** | Week 4 | |
| **15. Lazy evaluation** | **Week 3** | Twenty pages, and the week that most needs them |
| 16. Reasoning about programs | Week 12 | The one that makes Curry–Howard land |

**If you have two hours this week:** Chapter 1, then Chapter 2, then §4.1–4.4, then §5.1–5.2.

### Questions to hold while reading Chapter 1

1. §1.1 gives the "summing the integers 1 to n" comparison between C and Haskell that L01 §1 also
   uses. Hutton's point and L01's point are **different**. Say what each is.
2. §1.5 claims functional programs are "easier to reason about". **Find the sentence where he says
   what "reason about" means.** It is a specific technical claim, not a mood, and Week 12 tests it.
3. §1.4's `qsort` is four lines and is the most-quoted Haskell program in existence. It is also
   **not quicksort** — it is not in place and it allocates two new lists per level. Estimate how much
   memory it uses to sort a million elements, then read Week 2's measurement of exactly this.

### Chapter 2 — do it at a prompt, not in a chair

Chapter 2 is the only chapter in the book that is worthless read passively. Have `ghci` open.

**Questions:**

1. §2.3 lists the prelude functions on lists. **`:t` every one of them.** Which three take a function
   as an argument?
2. §2.4 introduces function application by juxtaposition, and the table comparing `f(a,b)` to `f a b`.
   Write down what `f a b` would mean if Haskell used the first convention and you wrote the second.
3. §2.5's naming rules: why must a type start with a capital and a variable with a lower case letter?
   *(There is a real parsing reason, and it is about patterns. Week 1.)*

---

## O'Sullivan, Stewart & Goerzen — *Real World Haskell*

**Chapters 1 and 2, and read them knowing the book is from 2008.**

It is the best book on Haskell *engineering* that exists and it is thirteen years older than the
compiler in BH 215. **Three places where it and this machine disagree**, each flagged in the week it
matters:

| Where | What it says | What GHC 9.4.7 does |
|---|---|---|
| Ch. 2, `ghci` output | `ghci> :type 'a'` etc. — output formatting differs slightly | Cosmetic. Ignore |
| Ch. 14, `Monad` instances | Defines `instance Monad Foo` with only `return` and `>>=` | **Will not compile.** Since GHC 7.10, `Monad` requires `Applicative`, which requires `Functor`. Week 5 §6 |
| Ch. 25, profiling | `-auto-all`, `-caf-all` | Spelled `-fprof-auto` now. Week 3 |

**Chapter 1 is the ten-minute GHCi tour** and it overlaps Hutton Ch. 2 almost exactly. Read whichever
you prefer; do not read both.

**Chapter 2 is "Types and Functions" and it is worth reading even though Week 1 covers the same
ground**, because it is written for someone who already programs and is impatient. Hutton is written
for someone learning to program. You are the first.

---

## Clocksin & Mellish — *Programming in Prolog*

**Not this week.** Week 8. Do not start it now; the two halves of this course do not mix well in a
single head, and the whole point of doing Haskell first is that seven weeks of "no mutation" makes
Prolog's "no functions either" survivable.

If you cannot resist: read **§1.1 only**, three pages, and stop.

---

## The paper for later

**Hughes, J. — *Why Functional Programming Matters* (1989).** Twenty-three pages, read in **Week 3**,
and on the final. Do not read it this week: its whole argument turns on laziness, which you will not
have met, and reading it early turns it into a slogan instead of an argument.

---

## The Thing You Should Actually Do This Week

**Not more reading — more `ghci`.**

Set a twenty-minute timer, open `ghci`, and type `:t` at every function named in Hutton Chapter 2.
When you meet a type you cannot read, look the symbols up in
[[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]], which is the
punctuation reference for this whole course.

**Week 0 is the only week you will have the time for that**, and the students who spend it end the
term able to read a type signature at a glance. That single skill is the difference between Week 5
being hard and Week 5 being impossible.

---

*PROG 202 · Week 0 · Reading Guide · © CSE Department*
