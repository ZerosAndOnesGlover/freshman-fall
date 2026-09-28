# PROG 202 · Quiz 1
## Administered: Tuesday, Week 1 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 0** — purity, referential transparency, evaluation by substitution, and GHCi.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room — the point
> is to find out what has not landed while there is still a term left to fix it.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** Define *referential transparency* in one sentence.

&nbsp;

&nbsp;

---

**Q2.** `elem :: Eq a => a -> [a] -> Bool`. How many arguments does `elem` take, and what is the part
before the `=>`?

&nbsp;

&nbsp;

---

**Q3.** In C, adding one line — `calls++`, on a global nothing reads — made `expensive(n) +
expensive(n)` take 0.88 s instead of 0.44 s. What did the compiler lose, and why was losing it
correct?

&nbsp;

&nbsp;

---

**Q4.** `getLine` is referentially transparent. Explain how that can be true when two calls return
different strings.

&nbsp;

&nbsp;

---

**Q5.** After `let xs = map (*2) [1..5]` and then `length xs`, `:sprint xs` shows `xs =
[_,_,_,_,_]`. What did `length` evaluate, and what did it not?

&nbsp;

&nbsp;

---

**Q6.** `print (sum [1..10000000], length [1..10000000])` holds **44 KB**. Naming that list once and
using it twice holds **273 MB**. Why does the name cost 273 MB?

&nbsp;

&nbsp;

---

**Q7.** Give one reason never to quote a timing taken from `runghc`.

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **An expression is referentially transparent when it can be replaced by its value without
changing the meaning of the program.**

*Accept "equals can be substituted for equals". Do not accept "it has no side effects" on its own —
that is a consequence, not the definition.*

---

**Q2.** **Two.** `Eq a` is a **constraint**: a requirement that the caller supply a type that can be
compared. It is not a parameter and you never pass anything for it.

---

**Q3.** **Common subexpression elimination** — running `expensive` once instead of twice. Losing it was
correct because with `calls++` in the body, **two calls are distinguishable from one** by a later read
of `calls`, so collapsing them would change what the program means. GCC cannot know nothing reads it.

*Making `calls` `static` does not win it back, measured. `__attribute__((const))` does — the programmer
promising what the compiler could not prove.*

---

**Q4.** **`getLine` is a value of type `IO String`: a description of an action, not a string.** It is
the same value every time it is mentioned, and may be substituted freely. What differs is what happens
when the runtime **performs** it — and performing is not evaluating. *The recipe is the same recipe;
the cakes differ.*

---

**Q5.** `length` needed to know **how many cons cells there are** and nothing about their contents, so
it forced the **spine** and left every element an unevaluated thunk. **It never looked at a single
number.**

---

**Q6.** **A name must denote one value, so the list has to be kept alive between the two traversals.**
`sum` walks it from the front while `length` still needs the front — ten million cons cells, all live
at once.

*Two marks of credit if you also said that naming it switches off **fusion**, which is why the unnamed
version allocates 53 KB where the named one allocates 640 MB. That is the separate half of the
measurement.*

---

**Q7.** **It measures the interpreter, not your program.** `runghc` was **57× slower** than `ghc -O2`
on the same file (8.5 s against 0.15 s), and `-O0` was 6.9× slower — so a `runghc` timing tells you
nothing about the code you would ship.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1, Q4 | L01 §2 and §6 |
| **Q2** | **L01 §2, and the `=>` row of [[PROG202 Week0/resources/Haskell Syntax and Symbols\|Haskell Syntax and Symbols]]** — today's lecture depends on it |
| Q3 | L01 §3 |
| Q5 | L02 §4 |
| **Q6** | **L02 §6** — Week 3 is this table |
| Q7 | L02 §5 |

**Q2 is the one that matters today.** This lecture spends fifty minutes on types with constraints in
them, and reading `Eq a =>` as an argument makes all of it incomprehensible. If you missed it, fix it
before Thursday.

---

*PROG 202 · Week 1 · Quiz 1 · covers Week 0 · ungraded*
