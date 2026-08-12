# CS 211 · Quiz 4
## Administered: Tuesday, Week 4 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 3** — symbol tables, scope, type checking, and Hindley-Milner inference.

**Instructions:** Closed notes. 10 minutes.

> **Not marked, no weight.** The key is printed below. Sit it closed-book, then mark it yourself.
>
> **Midterm 1 is tomorrow evening** and covers Weeks 0–3. Treat this quiz as your last calibration.

---

**Q1.** Give one program that the *parser* accepts and the *type checker* rejects.

&nbsp;

---

**Q2.** How does shadowing arise from `Scope.lookup`, given that nothing implements it?

&nbsp;

---

**Q3.** Why can a Cyan function be called before it is declared, when a local cannot be used before it is declared?

&nbsp;

---

**Q4.** The type checker reports `line 4 col 5`. Where did that position come from, and why could it not be recovered later?

&nbsp;

---

**Q5.** What is the occurs check for? Give the expression that needs it.

&nbsp;

---

**Q6.** `let f = \x->x in if f true then f 1 else 2` type-checks. The same expression with `f` lambda-bound does not. Name the rule.

&nbsp;

---

**Q7.** GHC rejects `1 + True` with `No instance for (Num Bool)` rather than a unification failure. What does that tell you about the type of `1` in Haskell?

&nbsp;

---

\pagebreak

---

## Answer Key — mark your own before leaving

**Q1.** Any of L07 §5's eighteen. `let x = 1 + true;` is the canonical one — every token is legal, the grammar is satisfied, and `+` has no rule for `int` and `bool`.

---

**Q2.** **`lookup` walks outward from the innermost scope and returns on the first match.** Shadowing is what "stop at the first match" means when scopes are nested — there is no shadowing code anywhere.

---

**Q3.** **The checker makes three passes over the top level** — structs, then function signatures, then bodies. All signatures are in the table before any body is checked. **Statements inside a body get one pass, in order**, so a local genuinely is not there yet.

---

**Q4.** **From the token the parser consumed when it built that node**, copied onto the AST node at construction.

**It cannot be recovered later because the token list no longer exists** by the time the checker runs — the checker receives only the tree. Information not copied at that moment is gone.

---

**Q5.** **To make unification terminate.** `\x -> x x` requires $t_0 = t_0 \to t_1$, and without the check the algorithm builds a cyclic type and loops forever.

---

**Q6.** **Let-polymorphism** — HM **generalises at `let`** but not at lambda. A `let`-bound variable's free type variables become universally quantified, and each use instantiates them freshly; a lambda-bound variable has one monomorphic type.

*Note the trap: `let id = \x->x in id (id 1)` works in* both *forms, because both uses are at `int -> int` and no polymorphism is needed.*

---

**Q7.** **`1` is not `Int`.** It has type `Num a => a` — any type with a `Num` instance. GHC unified `a` with `Bool` **successfully**, then failed on the *constraint* `Num Bool`.

**Haskell is HM plus type classes**, and this is the seam. Week 8.

---

### If you got fewer than 5

**Re-read L07 §3–§4 and L08 §6 tonight.** Q3, Q4 and Q6 are all live midterm material, and Q6's trap is the one most likely to appear in a form that punishes reciting the rule without checking it applies.

---

*CS 211 · Quiz 4 · Covers Week 3 · Unmarked*
