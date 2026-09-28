# PROG 202 · Quiz 2
## Administered: Tuesday, Week 2 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 1** — types as sets, algebraic data types, pattern matching, exhaustiveness, inference.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** How many values does `Bool -> Maybe Bool` have? Show the arithmetic.

&nbsp;

&nbsp;

---

**Q2.** What does `type Session = (String, String, Int)` check that a tuple of that shape does not?

&nbsp;

&nbsp;

---

**Q3.** Of the 120 orderings of Week 0's five `Session` fields, **twelve** type-check. Where does the
twelve come from?

&nbsp;

&nbsp;

---

**Q4.** GHC names the missing case for `Kind` (`SEM`) and gives up with an ellipsis for `String`. Why?

&nbsp;

&nbsp;

---

**Q5.** Name one way to crash a program that `-Wall` on this GHC gives **no warning** about at all.

&nbsp;

&nbsp;

---

**Q6.** `mkSession` checks that a session ends after it starts. Why is that guarantee worthless without
the module's export list?

&nbsp;

&nbsp;

---

**Q7.** `deriving Ord` on `data Day = Mon | Tue | Wed | Thu | Fri` makes `Mon < Tue` true. Where did
that ordering come from?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **Nine.** `|a -> b| = |b|^|a|`, so `|Maybe Bool| ^ |Bool|` = **3² = 9**.

*Not 6. A function chooses a result for **each** argument, so it exponentiates; it does not multiply.*

---

**Q2.** **Nothing.** `type` declares a *synonym*: every tuple of that shape **is** a `Session` and every
`Session` **is** that tuple. It is documentation with a keyword in front of it. `newtype` and `data`
make new types; `type` does not.

---

**Q3.** **3! × 2! = 12.** Any permutation that keeps the three `String`s among the string positions and
the two `Int`s among the integer positions is indistinguishable to the type. One of the twelve is
right, so **eleven wrong orderings compile.**

---

**Q4.** Because **`Kind` has four values and the compiler knows all four**, so the uncovered set is a
finite list it can print. `String` is infinite, so the uncovered set can only be described by patterns
over characters — GHC emits four such clauses and then stops, because there is no end to them.

**This is a fact about the types, not about GHC's cleverness.** No compiler can enumerate the complement
of three string literals in an infinite set.

---

**Q5.** Either of:

- **A partial record selector** — `why (Pending 1)` gives `No match in record selector why`. There is no
  `-Wincomplete-record-selectors` on GHC 9.4.7 at all.
- **`head []`** — `Prelude.head: empty list`. `-Wx-partial` is not recognised here either.

*`-Wall` **does** catch the incomplete `case` and the incomplete `let Just x = …`. Those two it does
not.*

---

**Q6.** **Because the export list is the only thing that makes `mkSession` the *only* way to build a
`Session`.** Export `Session (..)` instead of `Session` and any caller can use the raw constructor:
measured, `./break` then prints `PROG 202 LEC Tue 12:15-11:00` and exits 0. **A validation function is a
convention until a module boundary makes it a guarantee.**

---

**Q7.** **Declaration order** — `deriving Ord` compares constructors in the order they appear in the
`data` declaration. Nobody wrote a comparison. It is what you want for `Day` and a bug for a type whose
constructors you happened to list in some other order.

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| **Q1** | **L03 §1** — the counting is today's tool, not a curiosity |
| Q2, Q3 | L03 §2 and §4 |
| Q4 | L04 §2 |
| Q5 | L04 §2's aside, and L03 §2 |
| **Q6** | **L04 §3** — this is Lab 1's thesis |
| Q7 | L03 §6 |

**Q1 is the one that matters today.** This lecture is about functions as values, and if
`|a -> b| = |b|^|a|` is not obvious then `map`'s type will not be either.

---

*PROG 202 · Week 2 · Quiz 2 · covers Week 1 · ungraded*
