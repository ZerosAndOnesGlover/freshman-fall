# CS 211 · Problem Set 7
## A Lambda Calculus Interpreter

---

**Released:** Week 7, Wednesday · **Due:** Week 8, Friday 17:00
**100 points · counts toward the Problem Sets component (30% of the final grade)**

**Submit:** `lam.py` and any new modules (runnable end to end), your `.lam` files, and `ps7.md` (written answers, tables, traces). Written answers inside code comments will not be marked.

> **Midterm 2 is on the Tuesday of Week 8 and covers Weeks 4–7** — this week included. This problem
> set is due on the Friday *after* it. **Parts A, C and D are the best revision available for the
> Week 7 portion of that exam**, so doing them before Tuesday rather than after is worth more than
> the marks are.

Start from the Week 7 lab folder. `lam.py`, `church.py` and `prelude.lam` are given to you complete.

---

## Part A — Substitution and Capture (20 points)

**A1.** *(4)* For each term, list the **free** variables and the **bound** variables, and say which binder each bound occurrence belongs to.

```
λx. x y            (λx. x) (λy. y x)          λx. (λx. x) x          λf. (λx. f (x x)) (λx. f (x x))
```

The third one is the interesting one. **Say precisely which `x` the final `x` refers to**, and name the rule that decides it.

**A2.** *(6)* Reproduce L15 §5:

```
$ python3 lam.py '(\x y. x) y'
$ python3 lam.py '(\x y. x) y' --naive
```

- Give both results and say, in one sentence each, **what function each one is**.
- Now construct a *different* term, not of the form `(λx y. x) y`, on which `--naive` and the correct substitution differ. Show both outputs.
- **Construct a term on which they agree but for which `--naive` still performs no rename**, and explain why agreement here is luck rather than correctness.

**A3.** *(6)* `subst`'s `Abs` case has three branches: the parameter equals `x`, the parameter is free in `s`, and neither.

- State what each branch is for, in one sentence.
- **Delete the first branch** (the `t.param == x` early return) and find a term whose result changes. If you believe none exists, prove it — the claim is that the branch is a *performance* optimisation and not a correctness requirement, and it is either true or it is not.
- Restore it. Then break the third branch instead, by always renaming. Does anything change? What does that tell you about what the second branch is actually checking?

**A4.** *(4)* `fresh` generates names using a global counter.

- Two reductions of the *same* term, in the same process, produce different variable names. Show this.
- **Why does that not make the results wrong?** Name the relation under which they are equal, and show it holds using a function from `lam.py`.
- Give one concrete reason a compiler would nevertheless want the names to be deterministic.

---

## Part B — Reduction Strategies (22 points)

**B1.** *(5)* `lam.py` ships four strategies. For each, say in one sentence what redex it picks, and whether it reduces under a lambda.

Then fill in this table by running them, and explain every difference:

| term | `normal` | `cbn` | `applicative` | `cbv` |
|---|---|---|---|---|
| `(\x y. y) omega one` | | | | |
| `(\x. x x) (\x. x x)` | | | | |
| `\x. (\y. y) z` | | | | |

**The third row separates the four strategies into two pairs.** Say which pairs and why.

**B2.** *(5)* L16 §8 reports that normal order takes 10,384 beta-reductions for `fact four` and call-by-value takes 552.

- Reproduce both numbers.
- **Explain the gap mechanically.** Your answer must name the term that gets duplicated and say how many times.
- Normal order is *guaranteed* to find a normal form if one exists, and call-by-value is not. Explain in two sentences why that guarantee did not help here.

**B3.** *(12)* **Implement call-by-need.**

Call-by-name has normal order's termination behaviour and its duplication problem. Call-by-need fixes the duplication by **sharing**: an argument is wrapped in a mutable cell, reduced at most once, and the result remembered.

- Add a `Thunk` node holding a term and a `done` flag.
- Implement `whnf` (weak head normal form) that forces a thunk at most once and overwrites it with the result.
- Implement a `force_all` that normalises fully, so results can be decoded.

Then report, for `fact one` through `fact four`:

| n | normal order betas | call-by-need betas | thunk forces |
|---|---|---|---|

- **State the saving at n = 4 as a ratio.**
- Confirm that call-by-need still terminates on `(\x y. y) omega one` — that is, that you have kept normal order's behaviour and not accidentally built call-by-value.
- In two sentences: this is the difference between Haskell and a call-by-name language. **Is call-by-need a semantic change or an implementation technique?** Defend your answer.

---

## Part C — Encodings (22 points)

**C1.** *(4)* Using only `prelude.lam`'s definitions, write terms for:

- `double` — `λn. add n n`, but define it in terms of `mult` and check the beta counts of both. Which is cheaper, and why?
- `iseven` — true when a numeral is even.
- `max` — the larger of two numerals.

Test each on at least three inputs and give the beta counts.

**C2.** *(6)* `pred three` costs 36 beta-reductions; `mult three four` costs 9.

- Explain the asymmetry from the encoding, not from arithmetic.
- Measure `pred n` for n = 1…6 and give the growth.
- **`sub` is defined as `λm n. n pred m`.** Predict the cost of `sub six two` before running it, from your `pred` measurements, then run it. Report both numbers and account for any difference.

**C3.** *(6)* L16 §5 shows that `zero`, `false` and `nil` are the same term.

- Verify it with `alpha_eq`.
- **Find every alpha-equivalent pair** among the prelude's definitions. Brute force over all of them is the expected method — it is four lines and about 1500 comparisons. Report the complete list; **there are more than three pairs.**
- **Classify each pair as a *theorem* or a *collision*.** A theorem is a pair that any correct encoding would reproduce, because the two things genuinely are the same operation. A collision is a pair that happens to share a shape and would come apart under a different encoding. Justify each classification in one sentence.
- For the *collisions* only: write a term whose value is one of the two meanings and which a reader would plausibly misinterpret. Say what a type system would have to know to keep them apart — and why it does not need to keep the *theorems* apart.

**C4.** *(6)* **Encode binary trees.** A tree is either a leaf carrying a numeral, or a node with two subtrees.

- Give `leaf`, `node`, and `foldtree` following the same principle as `cons`/`nil` — *a datum is the function that uses it*.
- Define `treesum` and `depth` using `foldtree`.
- Test on a tree of at least five leaves and report the beta counts.
- **Your `leaf` and `node` must be distinguishable.** Show that they are, or explain what goes wrong and fix it. *(This is C3's problem, arriving in code you wrote.)*

---

## Part D — Recursion and Evaluation Order (24 points)

**D1.** *(6)* Reproduce the three-attempt result of L16 §10:

```
$ python3 lam.py --defs prelude.lam '(Y factgen) three' --strategy cbv --max-size 5000
$ python3 lam.py --defs prelude.lam '(Z factgen) three' --strategy cbv --max-size 5000
$ python3 lam.py --defs prelude.lam --church 'factV three' --strategy cbv
```

- Report all three.
- **Y diverges in 44 steps and Z survives 3911. Explain the difference**, and then explain why 3911 is still a failure.
- Name the single feature of `if` that causes attempt 2 to fail, and state it as a general rule about strict languages.

**D2.** *(6)* Verify that `Z` eta-reduces to `Y`, using `eta_reduce` and `alpha_eq`.

- Show the three terms.
- **Two terms that are the same function have different termination behaviour.** Say precisely what "the same function" means such that this is not a contradiction.
- Give a line of Python and a line of JavaScript that are eta-expansions performed for exactly this reason.

**D3.** *(12)* **Mutual recursion.** Define `iseven'` and `isodd'` so that each calls the other:

```
iseven' n  =  if (iszero n) true  (isodd'  (pred n))
isodd'  n  =  if (iszero n) false (iseven' (pred n))
```

Neither can use `Y` directly, because `Y` gives a fixed point of *one* function.

- **Work out how to do it** and implement it in `prelude.lam`. *(There is more than one route. The pair-based one — take the fixed point of a function on pairs, then project — is the standard one and is the one to reach for if you are stuck.)*
- Test both on n = 0…6 and report the results and beta counts.
- Make them work under **call-by-value** as well. Say what you had to change and why.
- In two sentences: OCaml writes `let rec f = ... and g = ...`, and the `and` is doing what your construction does. **What does the compiler have to build?**

---

## Part E — Written (12 points)

**E1.** *(6)* L16 §12 measures that de Bruijn indices produce **identical beta counts** and cost 5–74× more per step.

- State the two things de Bruijn indices genuinely buy.
- The per-step cost comes from `shift`. Explain what it does and why every beta-reduction needs two of them.
- **The speed advantage de Bruijn is usually credited with comes from a different change.** Name it, and say in three sentences how it avoids the problem. *(Your Cyan compiler will need this for Project 1 if you chose first-class functions.)*

**E2.** *(6)* The simply-typed lambda calculus — next week's subject — has the property that **every well-typed term has a normal form.** No term diverges.

- `omega = (λx. x x) (λx. x x)` must therefore be untypeable. **Show why**, by attempting to assign a type to `x` in `λx. x x` and finding the contradiction.
- `Y` contains `x x` too. So a typed language cannot have `Y`. **How does OCaml have recursion, then?** Answer in two sentences.
- Adding non-termination back to a total language is a design decision with a cost. Name one thing you can no longer do to programs in the language once `Y` is available. *(Week 5 did it constantly.)*

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14.2). **Beta counts are deterministic; timings are not.**

| Measurement | Value |
| --- | --- |
| `(\x y. x) y` correct / `--naive` | `λy0. y` / **`λy. y`** |
| `mult three four` | 12, in 9 betas |
| `pred three` | 2, in **36** betas |
| `sub six two` | 4, in 126 betas |
| `eq four four` | true, in 272 betas |
| `exp two five` | 32, in 64 betas, 21 renames |
| `fact three` (normal order) | 6, in 1525 betas |
| `fact four` (normal order) | 24, in **10384** betas |
| `factV four` (call-by-value) | 24, in 263 + 289 betas |
| `(Y factgen) three` under `cbv` | **diverges, 44 steps** |
| `(Z factgen) three` under `cbv` | **diverges, 3911 steps** |
| `factV three` under `cbv` | 6, in 175 + 64 betas |
| `eta_reduce(Z)` vs `Y` | **alpha-equivalent** |
| `zero`, `false`, `nil` | **the same term** |

Call-by-need, for Part B3 (reference implementation):

| n | normal order | call-by-value | call-by-need | forces |
|---|---|---|---|---|
| 1 | 45 | 53 | 45 | 32 |
| 2 | 248 | 119 | **94** | 68 |
| 3 | 1525 | 239 | **177** | 131 |
| 4 | 10384 | 552 | **384** | 292 |
| 5 | >60000 | 1864 | **1237** | — |
| 6 | >60000 | 9539 | **6210** | — |

**Your call-by-need counts need not match these exactly** — they depend on where you place thunks. What must hold: the results are correct, the counts are far below normal order's, and the ratio grows with n. **If your counts match normal order's, you have not shared anything.**

---

## A Note on Parts A3, C3 and D3

Each asks you to look for something whose existence is not guaranteed by the question.

A3 asks whether a branch is load-bearing. C3 asks you to find a collision that "there is at least one" of. D3 asks you to work out a construction rather than implement a stated one.

**A careful negative result is worth full marks and a fabricated positive one is worth zero** — the same rule as PS 5 and for the same reason. In A3 in particular, "I deleted the branch, ran every test in `church.py`, and nothing changed; here is the argument that nothing can" is a complete answer and a better one than a vague claim that something might.

**On C3 specifically:** brute-forcing all 49 definitions pairwise is 1176 comparisons and about four lines of Python. That is the expected method. Do not hand-inspect them.

---

*CS 211 · Week 7 · Problem Set 7 · © CSE Department*
