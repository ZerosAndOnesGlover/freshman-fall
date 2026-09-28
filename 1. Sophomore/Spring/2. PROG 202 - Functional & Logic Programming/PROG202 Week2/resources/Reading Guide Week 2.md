# PROG 202 · Reading Guide · Week 2
## Hutton 6 and 7 — and the paper to read next week, not this one

---

Week 2 is **the most transferable week in the course.** `map`, `filter`, `fold` and composition are in
Python, Java, Rust, C++, TypeScript and Swift now, and they arrived there from here. If you take one
week's material into your working life it is this one.

**Budget two hours.** Hutton Chapter 7 is short and dense and worth all of it.

| Chapter | Now? | Why |
|---|---|---|
| **6. Recursion** | **Read §6.1–6.6** | The two-equation shape that Chapter 7 abstracts. §6.6 (`mutual` recursion) is optional |
| **7. Higher-order functions** | **Read, all of it, twice** | **This is the week.** §7.1 basics, §7.3 `foldr`, §7.4 `foldl`, §7.5 composition, §7.6 the church-encoding aside |
| 8 | done in Week 1 | |
| **14. Foldables and friends** | **not yet** | Week 4. Reading it now will make `Foldable t =>` in every `:t` output more confusing, not less |
| **15. Lazy evaluation** | **next week** | Week 3, and read it then rather than now |
| 16. Reasoning about programs | Week 12 | §16.4 proves the universal property L06 §2 states. Look at it if you are curious; it is not this week's |

**If you have two hours:** Chapter 7 end to end, then Chapter 6 §6.1–6.5, then Chapter 7 again.

---

## Chapter 7 — the one to read twice

**Questions to hold while reading:**

1. §7.1 introduces higher-order functions with `twice f x = f (f x)`. **`:t twice`.** Why must the
   argument and result types be the same, and what does that tell you about `twice twice`?
2. §7.3 defines `foldr` and works through `sum`, `product`, `length`, `reverse`. **Hutton's `reverse`
   is a `foldr`.** L06 §5 says appending inside a fold is quadratic. **Is Hutton's `reverse` quadratic?**
   Work it out, then measure it — PS 2 Q2(a) asks for exactly this and the answer is not flattering to
   the book's version.
3. §7.4 introduces `foldl`, and Hutton says it is often "more efficient". **That is true of the machine
   code and false of the memory**, and L06 §3's eight numbers are the evidence. Note what the book does
   *not* mention: `foldl'`. It is in `Data.List`, it is what you almost always want, and a textbook
   that omits it is not wrong so much as out of date.
4. §7.5's `(.)` and the "composition of a list of functions" idiom, `compose = foldr (.) id`.
   **Work out its type by hand before you look.** It is one of the two genuinely useful expressions in
   PS 2 Q1(a).
5. §7.6 encodes numbers and booleans as functions. **Skippable, and read it anyway** — it is the
   clearest ten pages in the book on the idea that a function is a value, and Week 12 refers back to it.

---

## Chapter 6 — for one sentence

Read it for **§6.4**: the four-step recipe for writing a recursive function (name the type, enumerate
the cases, define the simple cases, define the others). It is the best procedural advice in the book
and it works.

**Question:** §6.5 gives `qsort` again, the four-liner. Hutton calls it "quicksort". L06 §6 measures it:
faster than `Data.List.sort` on random input, and **19 seconds for 40,000 already-sorted elements.**
**Find the sentence in §6.5 that would have warned you**, and if there is not one, say what should have
been there.

---

## Real World Haskell

**Chapter 4, "Functional programming"** — and this is the chapter where the book's age matters most.

It is very good on `foldr`/`foldl` *mechanics* and its space-leak discussion is the clearest prose
anywhere on why `foldl` is a problem. **What has changed is the symptom.** The book describes a stack
overflow; on GHC 9.4.7 with default settings you get **619 MB of heap** instead and no exception, and
you have to pass `+RTS -K16m` to see the crash it describes.

**Read it, and then read L06 §3.** The chapter's advice — use `foldl'` — is right. Its account of what
happens if you do not is a description of a compiler from 2008.

> **This is the second of the three places this course contradicts *Real World Haskell*.** The Week 0
> syllabus lists all three. Being able to say *"the book's reasoning is right and its symptom is out of
> date"* is a more useful skill than knowing which book is current, because next year this course's
> notes will be the out-of-date ones.

---

## Not This Week: the Hughes Paper

**Hughes, "Why Functional Programming Matters" (1989)** is assigned reading for **Week 3**, not this
week, and the reason is that its whole argument turns on **laziness** — which you have measured
(`foldr` answering a question about `[1..]`) and not yet been taught.

Read it next week and the `foldr`-on-an-infinite-list result you measured in Lab 2 §5 will be the
paper's central example. Read it this week and it is a list of assertions.

**Its opening paragraph is already quoted at the top of L05**, and you have met the sentence that
matters. That is enough for now.

---

## What to Actually Do

**Write `foldr` out by hand, from memory, twice.** Then `foldl`. Then `foldl'`.

It takes four minutes and it is the difference between the exam question being mechanical and being
impossible. Both the midterm and the final ask you to reduce a fold by hand, and a student who has to
reconstruct the definition first will run out of time.

---

*PROG 202 · Week 2 · Reading Guide · © CSE Department*
