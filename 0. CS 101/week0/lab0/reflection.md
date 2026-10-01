# CS 101 · Lab 0 · Reflection

**Student:** Adebayo Glover
**Date:** 1 October 2026

---

## 1. Type System

**Where Python's unlimited integers are necessary: cryptography.** RSA works with integers that are
2048 bits or longer, and it multiplies and takes remainders of them. Every digit has to be exact. A
32-bit C `int` overflows past 2,147,483,647 and a 64-bit one past about 9.2 × 10¹⁸. In the REPL,
`2 ** 100` gave `1267650600228229401496703205376`, which no fixed-size C integer can hold, and
Python stored it without complaint. Exact factorials and counting problems in combinatorics
(`50!` has 65 digits) need unlimited integers for the same reason.

**Where C's fixed-size integers are better: performance-critical and memory-limited programs**,
such as firmware on a microcontroller, a graphics buffer of millions of pixels, or a game physics
loop. A C `int` is always exactly 4 bytes and the CPU adds two of them in one instruction. A Python
`int` is an object with its own header, it grows as the number grows, and every operation has to
check how big the number is first. When the values are known to be small, fixed-size integers give
predictable memory use and much faster arithmetic. They also match hardware registers and file
formats that are defined bit by bit.

## 2. Float Imprecision

A `float` stores a number in **binary**, with a 53-bit fraction. Most decimal fractions have no exact
binary form. 0.1 is 1/10, and since 10 = 2 × 5, the factor of 5 makes the binary expansion repeat
forever: 0.000110011001100… It gets cut off and rounded, the same way 1/3 = 0.333… has to be cut off
in decimal. The value actually stored for `0.1` is

```
0.1000000000000000055511151231257827021181583404541015625
```

and the stored values for `0.2` and `0.3` are also slightly off. When `0.1 + 0.2` is computed, the two
small errors add up, and the result is rounded to `0.30000000000000004`. That is a different float
from the one closest to `0.3`, so `0.1 + 0.2 == 0.3` is `False`.

**Consequence for financial software.** Every amount like $0.10 would be slightly wrong, and over
millions of transactions the errors add up. Totals could be off by cents, an account that should hold
exactly $0.30 would fail an `== 0.30` check, and two systems that add the same items in a different
order could get different totals, so the books would not balance. Money should be stored as an
integer number of cents (`30` instead of `0.30`), or with Python's `decimal.Decimal`, which works in
base 10.

## 3. Modulo Surprises

Python's `%` always gives a result with the same sign as the divisor. For `n % 7` that means the
answer is always one of 0, 1, …, 6, even when `n` is negative. Those are exactly the valid day
numbers.

Number the days Monday = 0 … Sunday = 6. The day N days after day `d` is `(d + N) % 7`. The formula
also works for going **backwards**. Today is Thursday (`d = 3`). Ten days ago was
`(3 - 10) % 7 = -7 % 7 = 0`, Monday, which is correct. For a Wednesday (`d = 2`), ten days ago gives
`(2 - 10) % 7 = -8 % 7 = 6`, Sunday, which is also correct.

In C or Java, `-8 % 7` is `-1`. That is not a day of the week, and using it as an array index would be
a bug. So the C version needs an extra correction, `((d + N) % 7 + 7) % 7`. Python's rule removes
that special case. The same is true for anything that wraps around: hours on a clock, positions in a
circular buffer, or letters in a Caesar cipher.

## 4. Git

Many small commits are better than one big "Complete lab 0" commit for these reasons:

- **Readable history.** `git log --oneline` then tells the story of the work, for example *Add
  temperature conversion formula*, then *Add absolute zero*. One big commit just says that
  something changed.
- **Easier to undo.** If one change turns out to be wrong, `git revert` can undo that one commit and
  keep everything else. When unrelated changes share a commit, they can only be undone together.
- **Easier to find bugs.** If a bug appears, `git bisect` can binary-search the history to find the
  commit that caused it. Bisect lands on a commit, so a small commit points almost straight at the
  broken line, while a big one leaves a lot of code to look through.
- **Easier to review.** A teammate or TA can check a 10-line commit with one purpose properly.
  A 500-line commit gets skimmed.
- **Less work lost.** Each commit is a safe checkpoint. If I break something while experimenting, I
  can go back to the last good state instead of losing an afternoon's work.
