# CS 211 · Week 3 · Reading Guide
## Two books, and the one chapter worth reading slowly

---

**Set reading:** Aho et al., **§2.7** (symbol tables), **§5.1–5.2** (attribute grammars), **§6.5** (type checking).
**Also set:** Pierce, *TAPL*, **Chapter 22** (type reconstruction). **This is the one to read slowly.**
**Optional:** Appel, **Chapter 5**. A working symbol-table implementation, which the Dragon does not really give you.

**Dragon before Tuesday, TAPL 22 after Thursday.** L08 gives you the algorithm operationally; TAPL gives it to you properly, and the second reading lands much better with the first in place.

---

## Why TAPL Is Different

The Dragon Book is a *compiler engineering* text. **TAPL is a mathematics text about type systems**, and it is the first genuinely formal reading in this course.

It states type systems as **inference rules**:

$$\frac{\Gamma \vdash e_1 : T_1 \to T_2 \qquad \Gamma \vdash e_2 : T_1}{\Gamma \vdash e_1\, e_2 : T_2}$$

Read that as: *"if, in context $\Gamma$, $e_1$ has a function type and $e_2$ has its argument type, then the application has the result type."* **Premises above the line, conclusion below.**

> **This notation is worth twenty minutes of discomfort.** It is how every type system in the
> literature is specified, it is what Week 8 is written in, and the entire Cyan type checker is
> about fifteen such rules — `check_binary` in `typecheck.py` is three of them in Python. **Once you
> can read the rules, the implementation is transcription.**

---

## Section by Section

| § | What to take from it |
|---|---|
| **Dragon 2.7** | Symbol tables, and scope as a chain of tables. §2.7.1 is `Scope.lookup` from L07 §3 |
| **Dragon 5.1** | **Synthesised and inherited attributes.** Types are synthesised — computed bottom-up from children. Scope is inherited — passed down from parents. **Your `check_expr` does both and you may not have noticed** |
| **Dragon 5.2** | Evaluation orders for attributes; dependency graphs. Skim |
| **Dragon 6.5** | **Type checking.** §6.5.2 on type conversions is the section Cyan deliberately has nothing corresponding to |
| **TAPL 22.1** | Type variables and substitution. Short and essential |
| **TAPL 22.2–22.3** | **Constraint generation.** This is L08 §2 — walking the tree emitting equations |
| **TAPL 22.4** | **Unification.** The algorithm, with the occurs check and a termination proof |
| **TAPL 22.5** | **Principal types.** The theorem from L08 §5, stated and proved |
| **TAPL 22.6–22.7** | Let-polymorphism, and why lambda-bound variables are not generalised. **L08 §6** |
| **TAPL 22.8** | Implementation notes |

---

## The Three Things Worth Slow Reading

**Dragon §5.1's attribute distinction.** *Synthesised* attributes flow up the tree; *inherited* attributes flow down. **Your type checker is an attribute grammar you wrote without knowing the term** — `check_expr(e, scope)` takes an inherited attribute (`scope`) and returns a synthesised one (the type). Seeing that makes Week 4's IR generation, which is the same shape again, much less mysterious.

**TAPL §22.4's unification.** The Dragon Book does not cover unification at all. **This is the only place you will read it properly**, and the termination argument — why the occurs check is necessary and sufficient — is the part to get.

**TAPL §22.6 on let-polymorphism.** Pierce is careful about exactly which variables get generalised and why. **Lab 3 Q14's trap is a case Pierce's rules handle correctly and most informal explanations do not.**

---

## What Neither Book Emphasises Enough

**That error message quality is a language design constraint.** Both books treat type checking as a decision procedure — does this program type-check, yes or no. **In practice the *no* comes with a message, and where that message points is most of what users experience of your type system.** L08 §7 gives that as Cyan's main reason for requiring annotations, and neither book will tell you so.

**That Haskell is not Hindley-Milner.** TAPL Chapter 22 presents HM cleanly. **Real Haskell is HM plus type classes**, and the seam shows the moment you type `1 + True` and get `No instance for (Num Bool)` rather than a unification failure. **Chapter 22 does not cover classes**; TAPL Chapter 23 does System F, and classes proper are Week 8's material.

---

## Questions to Read Against

**On Dragon §2.7 and §5.1**

1. §2.7 chains symbol tables for nested scopes. **What is the cost of a lookup** in terms of nesting depth, and when would that matter?
2. Classify each as synthesised or inherited: the type of an expression; the scope a statement is checked in; whether a function has a `return` on every path.
3. §5.1's attribute grammars can express type checking. **Can they express "declared before use"?** Answer carefully — think about what an inherited attribute can carry.

**On Dragon §6.5**

4. §6.5.2 covers implicit conversions and a *widening* hierarchy. **Cyan has none.** Write the two lines you would add to `check_binary` to allow `int` where `bool` is expected, and then say what breaks.
5. The book gives a rule for array indexing requiring an integer subscript. **Cyan's error for `a[true]` names a column.** What does the book's formulation leave out that a real compiler must add?

**On TAPL 22**

6. §22.3 generates constraints; §22.4 solves them. **Does the order of constraint generation affect the solution?** Justify from the properties of unification.
7. §22.4's occurs check makes unification terminate. **Give the expression from L08 §3 that needs it**, and say what the algorithm does without it.
8. §22.5's principal type theorem says there is a most general type. **Why does that make `hm.py` and GHC agreeing on six expressions unsurprising** rather than a coincidence?
9. §22.6 generalises at `let` but not at lambda. **Give the expression from Lab 3 Q14 that distinguishes them**, and one that does not despite looking like it should.

---

## Two Things to Check on Your Own Machine

**1. That GHC agrees with your inference.**

```bash
cat > t.hs <<'EOF'
i     = \x -> x
twice = \f -> \x -> f (f x)
comp  = \f -> \g -> \x -> f (g x)
EOF
for n in i twice comp; do echo ":t $n" | ghci -v0 t.hs; done
```

**Compare against `hm.py`.** The variable names differ; the *structure* must not.

**2. The seam.**

```bash
echo 'bad = 1 + True' > e.hs && ghc -fno-code e.hs 2>&1 | head -4
```

**`No instance for (Num Bool)`** — not `couldn't match Int with Bool`. **Ask yourself what type GHC thinks `1` has**, and keep the answer for Week 8.

---

*Next week's reading is Dragon Ch. 6 in full plus §8.4–8.5, and the LLVM Language Reference's first few sections. **Midterm 1 sits in Week 4** and covers Weeks 0–3 — the revision guide arrives with Week 4's materials.*
