# PROG 202 · Midterm Examination
## Thursday 5 March, 18:00–19:15 · VNC 100 · 75 minutes · 100 marks · 15% of the course

**Name:** _________________________________ **Student ID:** ___________

---

**Covers Weeks 0–5.** Purity and referential transparency; types and algebraic data types; higher-order
functions and folds; lazy evaluation; type classes; monads.

**Closed book.** No notes, no devices. **One A4 sheet of your own handwritten notes is permitted, one side**
— bring it; writing it is the best revision exercise available and you may keep it.

**Answer all questions.** Marks are shown. **Budget roughly 45 seconds per mark.**

> **How this paper is marked.**
>
> **Where a question asks for a number, the number is one you measured**, and this course's figures are in
> the lecture notes. An answer that gives the right *mechanism* with a wrong number keeps most of the
> marks; an answer that gives a number with no mechanism keeps almost none.
>
> **Two questions ask you to disagree with something.** A defended position that contradicts the lectures
> scores full marks. Reciting the lecture's own position without defending it does not.
>
> **Code need not compile.** It must be unambiguous. Write types when you are unsure whether it is.

---

## Section A — Short Answers (30 marks)

**A1. [4]** Define *referential transparency* in one sentence. Then say whether `getLine` has it, and why
your answer is consistent with two calls returning different strings.

**A2. [4]** Define *weak head normal form*. Then: after `let p = (1+1, 2+2)` and `p `seq` ()`, what does
`:sprint p` show, and why?

**A3. [5]** `Session` was `(String, String, String, Int, Int)` in Week 0. **Of the 120 orderings of its five
fields, how many type-check, and where does that number come from?** After the Week 1 redesign it is 2 — say
which ordering is the wrong one and why it survives.

**A4. [4]** `elem :: Eq a => a -> [a] -> Bool`. How many arguments does `elem` take? What does the compiler
supply that you did not write, and at which point?

**A5. [4]** State the rule for choosing between `foldl'` and `foldr`. Your rule must mention the **operator**,
not the list, and you must give one operator for each side.

**A6. [5]** `length ('x', 5)` is `1`. `maximum ("hello", 3)` is `3`. `maximum (Left "x")` **throws**, while
`length (Left "x")` is `0`. **Explain all four from one fact about `Foldable`.**

**A7. [4]** `do { x <- m; y <- n x; pure (x, y) }` — desugar it into `>>=` and lambdas. Then say what `<-`
actually is.

---

## Section B — Applied Judgement (40 marks)

**B1. Where the memory went [14]**

A colleague has written the mean of a list in one pass, because two passes would retain the list:

```haskell
mean :: [Int] -> Double
mean xs = let (s, c) = foldl' step (0, 0) xs in fromIntegral s / fromIntegral c
  where step (s, c) x = (s + x, c + 1)
```

At *n* = 10⁷ and `-O0` it holds **727 MB**.

**(a) [5]** `foldl'` is the strict fold. **Explain the leak precisely**, using the phrase *weak head normal
form*, and say how many thunk chains are built and how long each is.

**(b) [4]** Give **two** fixes, in code. Say which you would ship and why.

**(c) [5]** The colleague replies: *"At `-O2` it is 44 KB, so there is no bug."* **Answer them.** Your answer
must name the compiler pass responsible, and give **one case from this course where the same optimisation
does not save you** — with its measurement.

---

**B2. What the types left open [12]**

Week 1 redesigned `Session` so that one wrong field ordering still type-checks, and closed it like this:

```haskell
mkSession :: Course -> Kind -> Day -> Minutes -> Minutes -> Either String Session
mkSession c k d s e
  | s >= e    = Left (…)
  | otherwise = Right (Session c k d s e)
```

**(a) [4]** `mkSession`'s type does one thing that a `Bool`-returning validator would not. Say what, and why
it matters to the caller.

**(b) [4]** **`mkSession` is worthless on its own.** Say what else is required, give the one line of code
that supplies it, and state what a caller can do if it is absent. *(One sentence each.)*

**(c) [4]** Week 4's `Monoid Stats` used `mempty = Stats 0 0 0`, where the third field is a **maximum**.
**That is lawful only because of `mkSession`.** Explain the connection, and say what you would have to write
instead if `mkSession` did not exist.

---

**B3. Reading a fold [14]**

**(a) [4]** Evaluate by hand, showing the bracketing: `foldr (-) 0 [1,2,3]` and `foldl (-) 0 [1,2,3]`.

**(b) [5]** `foldr (\x acc -> x > 5 || acc) False [1..]` returns `True`. The same question written with
`foldl'` **never terminates.** Explain, in terms of which element is the **outermost** application in each
fold.

**(c) [5]** Summing `[1..10⁷]`: at `-O2`, `foldl` is **44 KB** and `foldr` is **130 MB**. At `-O0`, `foldl`
is **619 MB** and `foldr` is **446 MB**. **The ranking reverses.** Explain both columns, and say why no
optimisation level rescues `foldr` here. **Your answer must say what is being held in each case, and they are
not the same thing.**

---

## Section C — Longer Answers (30 marks)

**Answer TWO of the three.** 15 marks each. Half a page each is enough; a page is plenty.

---

**C1. Write `State` from scratch.**

Give the `newtype`, all three instances in the required order, and `get`, `put`, `evalState`, `execState`.

Then: **annotate your `>>=` with what each of its steps does**, and say which of the three instances `do`
notation actually calls.

---

**C2. "Laziness is a feature, and the space cost is the price of it."**

**Argue for or against**, using at least **three** measurements from this course. Your answer must include
at least one case where laziness bought something that strictness could not, and at least one case where the
cost was not visible in the source text.

**A defended "against" scores full marks.**

---

**C3. "A type class is just an interface."**

**Answer it.** Give at least **three** ways the two differ, and for each say what it lets you write that
the other does not. One of your three must involve a function whose class variable appears **only in its
return type**.

Then say what *coherence* is, and name the cost this course showed you paying for it.

---

## Given facts

You are not expected to have memorised figures, but these are the ones this paper's questions refer to, so
that no mark depends on recall:

| | |
|---|---|
| `Session` orderings | 120 tried · **12** accepted by the tuple (11 wrong) · **2** by the Week 1 record · 1 by a newtype per field |
| `sched` | 17 sessions · 1,070 contact minutes · 0 clashes · 2 lunch collisions |
| Summing `[1..10⁷]`, residency | `-O2`: `foldr` 130 MB, `foldl` 44 KB, `foldl'` 44 KB · `-O0`: `foldr` 446 MB, `foldl` 619 MB, `foldl'` 44 KB |
| One-pass mean, *n* = 10⁷ | lazy pair **727 MB** at `-O0`, 44 KB at `-O2` · strict fields 110 KB allocated at `-O2` |
| Two-pass mean | 245 MB at `-O0` **and** 289 MB at `-O2` |
| `Data.Map` as a counter | `Lazy` **107 MB**, `Strict` 44 KB — **both at `-O2`** |
| `acc ++ [x]` in a fold | 22.57 s against 0.01 s at *n* = 40,000 |
| Dictionary passing | 2.9 s against 2.2 s with `SPECIALISE`; **0.07 s** with `NOINLINE` also removed |
| `State`, *n* = 3×10⁶, `-O0` | `Lazy`+`modify` 308 MB · `Lazy`+`modify'` **398 MB** · `Strict`+`modify` 167 MB · `Strict`+`modify'` **44 KB** |
| `runghc` against `-O2` | 8.5 s against 0.15 s — **57×** |

---

**End of paper.** 100 marks: Section A 30, Section B 40, Section C 30.

---

*PROG 202 · Week 6 · Midterm · Thursday 5 March, 18:00–19:15 · © CSE Department*
