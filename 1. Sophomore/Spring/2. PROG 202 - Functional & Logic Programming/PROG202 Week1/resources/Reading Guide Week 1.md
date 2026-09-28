# PROG 202 · Reading Guide · Week 1
## Hutton 3, 4 and 8 — and the chapter to read twice

---

Week 1 is **types**, and Hutton splits the subject across three chapters that are not adjacent.
**Chapter 8 is the important one** and it is the one students skip, because it is numbered later than
the week and looks like it belongs to a different topic.

**Budget two hours.**

| Chapter | Now? | Why |
|---|---|---|
| **3. Types and classes** | **Read, all of it** | §3.1–3.6 is L03 §1–§3. §3.7–3.9 is classes, which is Week 4 — read it anyway, lightly, so `Num a =>` stops being strange |
| **4. Defining functions** | **§4.1–4.4** | Guards, pattern matching, lambdas, sections. L04 §1 |
| 5. List comprehensions | done in Week 0 | |
| 6. Recursion | **Skim now, read in Week 2** | §6.1–6.3 makes Lab 1's two-equation functions feel normal |
| **8. Declaring types and classes** | **Read twice** | **This is the week.** §8.1 `type`, §8.2 `data`, §8.3 newtype, §8.4 recursive types, §8.5–8.6 the tautology checker |
| 12. Monads | no | Not yet. It will not help |

**If you have two hours:** Chapter 8 §8.1–8.4, then Chapter 3, then §4.1–4.4, then Chapter 8 again.

---

## Chapter 8 — the one to read twice

§8.1–8.3 is the `type` / `data` / `newtype` distinction that L03 §2 turns into a table. Hutton is
clearer than the lecture on *why* the three exist; the lecture is clearer on what each one costs.

**Questions to hold while reading:**

1. §8.1's `type` declarations are synonyms. **Hutton says they "cannot be recursive".** Work out why
   not — what would `type Tree = (Int, [Tree])` have to mean? *(The answer is about expansion, and it
   is the same reason C's `#define` cannot recurse.)*
2. §8.2 introduces `data`. Hutton writes `data Shape = Circle Float | Rect Float Float`. **Count the
   values of `Shape`** in terms of the number of `Float`s. Then say why `Circle` and `Rect` are
   functions and `data Bool = False | True`'s constructors are not.
3. §8.3's `newtype Nat = N Int`. **Hutton says the difference from `data` is efficiency.** That is
   right and it undersells it: give the *other* reason, the one L03 §2's table is about, by asking
   what `type Nat = Int` would have allowed.
4. §8.4's recursive types build `Nat`, `List` and `Tree` from nothing. **`data List a = Nil | Cons a
   (List a)` is the real list** with different spelling. Write out `[1,2,3]` in both notations.
5. §8.6's tautology checker is a small interpreter over a `Prop` data type — **it is Project 1 in
   miniature**, and it is the best single exercise in the book. Do it. It takes forty minutes and it
   will make Week 7's deadline much less frightening.

---

## Chapter 3 — read for the two ideas the lecture assumes

1. §3.3's **curried functions**. If `add :: Int -> Int -> Int` is not yet obviously
   `Int -> (Int -> Int)`, stop and fix that before Thursday; Week 2 is unreadable without it.
2. §3.5's **polymorphic types** and §3.6's **overloaded types**. The difference between `length :: [a]
   -> Int` and `sum :: Num a => [a] -> a` is the difference between *any type at all* and *any type
   that can do something*. **The `=>` is the whole distinction** and Quiz 1 Q2 is about it.

**Question:** §3.6 gives `(+) :: Num a => a -> a -> a`. Why can there be no `(+) :: a -> a -> a`? Say
what such a function would have to do for `a = Bool`.

---

## Chapter 4 — §4.4 is the one with the trap

§4.4 covers **lambda expressions** and **sections**. The trap is in the sections:

```
ghci> map (subtract 1) [1,2,3]
ghci> map (- 1) [1,2,3]
```

The second is not what you want. Work out what it is and why, then read
[[PROG202 Week0/resources/Haskell Syntax and Symbols|Haskell Syntax and Symbols]] §5's last paragraph
— **`-` is the one genuinely irregular symbol in the language** and this is the only place it bites.

---

## Real World Haskell

**Chapters 3 and 4**, and Chapter 3 is genuinely good here — it is the same ground as Hutton 8 written
for someone impatient, and its "algebraic data types" section has better *engineering* advice about
when to use a record than Hutton has.

**One thing in Chapter 3 to be careful of.** It presents the `data` / `type` / `newtype` distinction
before it has shown you a reason to care, and its examples use positional constructors where a record
would be clearer. Read L03 §4's measurement first and Chapter 3 second, and its advice will land
differently.

---

## Not This Week

**Chapters 12 and 14 of Hutton, and Chapter 14 of *Real World Haskell*.** Monads. Every student who
has heard the word is tempted in Week 1 and every one of them regrets it. The order in this course is
deliberate: you need folds (Week 2), laziness (Week 3) and type classes (Week 4) before a monad is
anything but an incantation.

---

## What to Actually Do

**Hutton §8.6's tautology checker, by hand, before Wednesday's lab.** Nothing else this week will
teach you as much per minute: it is a data type, a recursive evaluator, a substitution, and an
exhaustive search, in about thirty lines — and it is the same shape as the `Expr` in L04 §4 and the
same shape as Project 1.

---

*PROG 202 · Week 1 · Reading Guide · © CSE Department*
