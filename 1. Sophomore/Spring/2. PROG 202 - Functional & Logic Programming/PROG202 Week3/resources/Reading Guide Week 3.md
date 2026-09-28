# PROG 202 · Reading Guide · Week 3
## Hughes's paper — the one piece of reading this course insists on

---

**This week has one required reading and it is not a textbook chapter.**

**Hughes, J. — *Why Functional Programming Matters* (1989).** Twenty-three pages. **Read all of it, this
week, and it is on the final.**

Everything else is optional. That is deliberate: the paper is the best single thing written about why
this course exists, and Week 3 is the only week where you have both the vocabulary to read it and the
measurements to argue with it.

---

## Why now and not Week 0

The paper's argument has two halves, and you have just measured the second.

**§3, "Gluing Functions Together", is Week 2** — higher-order functions let you take a program apart at
places an imperative program has no seams. You built that in Lab 2.

**§5, "Gluing Programs Together", is this week** — laziness lets a producer and a consumer be separate
programs, with the consumer deciding how much of the producer runs. `sqrts` never decides when to stop
and `within 1e-12` never knows how the approximations were made, and **six approximations were computed
out of infinitely many.**

Read in Week 0, that section is an assertion. Read now, it is a description of something you have run.

---

## How to read it

| Section | How |
|---|---|
| **§1–2** Introduction, modularity | **Closely.** §2's "new kinds of glue" is the thesis, and the sentence quoted at the top of L05 is its centre |
| §3 Gluing functions together | Skim — it is Week 2, and you have done the exercises |
| §4 Higher-order functions | Read. His `foldr`-based `reduce` is Week 2's `foldr` with 1989 spelling |
| **§5 Gluing programs together** | **Closely, twice.** This is L08 |
| **§6** The game-tree example | **Read it.** It is the pay-off and the only part that is hard. Budget forty minutes |
| §7 Conclusion | Read |

**A note on the notation.** The paper is written in **Miranda**, Haskell's immediate ancestor, so:
`listof *` is `[a]`, `reduce` is `foldr`, `++` and `.` mean what they mean here, and function definitions
use the same equations. **Nothing needs translating except the type syntax.**

---

## The four questions to hold

1. **§2 claims that better glue means better modularity.** He gives no evidence in §2 — the evidence is
   §§3–6. **After reading §6, decide whether he made the case**, and be able to say which of the two
   glues did more of the work in the game-tree example.
2. **§5's separation of `sqrts` from `within` is the paper's cleanest example. Is laziness *necessary*
   for it?** Python's generators, C#'s `IEnumerable`, Rust's `Iterator` and a callback all separate
   production from consumption. **What, exactly, would you give up with each?** *(This is a final-exam
   question. Bring a real answer, not "they're the same".)*
3. **Written in 1989 to argue functional programming deserved attention.** Which of his claims are now
   simply true of every mainstream language, and which are still only true here? Week 12 asks this
   again.
4. **§6's alpha-beta pruning works because the tree is lazy.** L08 §5 lists what laziness costs. **Apply
   that list to §6's program**: where would its space behaviour be hard to predict, and how would you
   find out?

---

## Optional, and worth it if you have time

**Hutton §15, "Lazy evaluation"** — twenty pages, and it is the textbook version of L07. §15.7's
*strict application* covers `$!` and §15.8 is the space-leak discussion. **If any of L07 did not land,
this is the place to go**, and it is better than the lecture on the evaluation-order rules.

**Melissa O'Neill, "The Genuine Sieve of Eratosthenes" (*JFP* 19(1), 2009)** — nine pages on the
`primes` two-liner from L08 §4, and the source of the priority-queue version in `resources/sieve.hs`.
Not required. It is the best short paper on "elegant, correct, and the wrong algorithm" there is.

---

## Not This Week

**Hutton §12 and §14.** Monads and `Foldable`. Week 4 starts `Foldable` and Week 5 starts monads, and
reading ahead here genuinely hurts — `Foldable` makes sense once you have type classes, and not before.

---

## What to Actually Do

**Read §5, then run `resources/infinite.hs`, then read §5 again.** Twenty minutes, and it is the closest
this course comes to a reading assignment that pays off immediately.

Then, before Thursday's lecture, **write down in one sentence what you think laziness is *for*.** L08
finishes with a table of what it costs, and the sentence you wrote is what you should weigh against it.

---

*PROG 202 · Week 3 · Reading Guide · © CSE Department*
