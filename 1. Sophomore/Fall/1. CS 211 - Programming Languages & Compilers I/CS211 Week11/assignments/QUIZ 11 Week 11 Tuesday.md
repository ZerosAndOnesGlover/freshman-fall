# CS 211 · Quiz 11

**Sat:** Tuesday of **Week 11**, first 10 minutes of lecture · TH 205
**Covers:** **Week 10** — metaprogramming and domain-specific languages
**Unmarked.** Recorded in [[_CS 211 Lab and Quiz Record]].

**This is the last quiz of the term.** The answer key is printed below the questions.

> **Project 1 is due Friday at 17:00**, and PS 10 with it. Ten minutes here is well spent; the
> rest of the week belongs to the project.

---

## Questions

**1.** *(2 min)* `unless` is defined twice:

```lisp
(define unless-fn  (lambda (test body) (if test nil body)))
(defmacro unless-mac (test body) `(if ,test nil ,body))
```

`(unless-fn #t (boom))` raises; `(unless-mac #t (boom))` returns `nil`.

**Explain the difference**, and name the Week 7 result this is.

---

**2.** *(2 min)* `(cons (quote *) (cdr (quote (+ 2 3))))` evaluates to `(* 2 3)`.

Say what that demonstrates, name it, and say what it lets a macro be.

---

**3.** *(2 min)* This macro is wrong:

```lisp
(defmacro swap-bad (a b)
  `(begin (define tmp ,a) (set! ,a ,b) (set! ,b tmp)))
```

`(swap-bad tmp z)` returns `(7 7)` where `(7 100)` was expected.

**Name the bug**, give the Week 7 section it first appeared in, and name the fix.

---

**4.** *(1 min)* Distinguish an **internal** DSL from an **external** one, and give one thing each can do that the other cannot.

---

**5.** *(2 min)* Parser combinators express the arithmetic grammar in **4 lines**; Week 2's hand-written parser is 357.

Give **two** things the combinator version is worse at, and explain the second one structurally.

---

**6.** *(1 min)* `bad_expr := bad_expr '+' NUMBER | NUMBER` produces a `RecursionError`.

Say why, and say what that tells you about the relationship between parser combinators and Week 2's recursive descent.

---
---

## Answer Key

**1.** **A function's arguments are evaluated before it is entered**, so `(boom)` ran before `unless-fn` could discard it. **A macro receives its arguments as unevaluated syntax** and runs at expansion time, so the branch it does not want is never evaluated.

The Week 7 result is **§10**: in a strict language `if` cannot be an ordinary function, which is why `(Z factgen) three` diverged under call-by-value — `if` evaluated both branches, including the recursive one. Week 7's fix was thunks at the *caller*; a macro fixes it at the *definition*.

---

**2.** It builds **a program out of a program**, using `cons` and `cdr` — ordinary list operations.

That is **homoiconicity**: a Lisp program *is* a Lisp list.

It lets a macro be **an ordinary function from lists to lists**, written in the same language, with no special mechanism. *(And it is why the whole front end is about thirty lines — the syntax is the data structure, which is the fortnight Weeks 1–2 spent that Lisp declines to.)*

---

**3.** **Variable capture.** The macro introduces `tmp`, and the caller's variable is also called `tmp`, so the expansion is `(define tmp tmp)` — the macro clobbers the value it was supposed to save. No error; a plausible wrong answer.

It first appeared in **Week 7 §5**: `(λx y. x) y` gives a constant function correctly and **the identity** under naive substitution, one beta-step apart.

The fix is **`gensym`** — a name nothing else is using — which **is Week 7's `fresh`** under another name. A macro system that does this automatically is **hygienic**.

---

**4.** An **internal** DSL is embedded in a host language using its existing syntax — operator overloading, method chaining, macros. An **external** DSL has its own syntax, parser and file format.

**Internal can:** reuse the host's tooling entirely — debugger, line numbers, editor, package manager — for free.
**External can:** use notation the host's grammar forbids. `nand(a, b)` has to be `~(a & b)` in an internal Python DSL, because you may not add an operator.

*(Accept the reverse framing. The deciding question is **who reads it**.)*

---

**5.** Any two of: **error messages**, **left recursion**, performance, debuggability.

**The error messages, structurally:** alternation **backtracks**. When `a | b` tries `a` and it fails, everything `a` learned — including how far it got — is discarded before `b` is tried. When both fail, the only position still available is where the whole alternation *started*. So the combinator reports `expected number or ')' at '(1 + 2'` — pointing at the beginning of the input — where the hand-written parser reports `line 1 col 30: expected PUNCT ')', found PUNCT ';'`.

**This is why clang, rustc and GHC all hand-write their parsers**, despite those teams knowing exactly what a combinator is: they are optimising for the diagnostic, which is what users interact with.

---

**6.** A left-recursive rule **calls itself as its first action, before consuming any input**, so the recursion never reaches a base case.

It tells you that **parser combinators are recursive descent with the call graph reified** — the grammar became a value, but the parsing strategy did not change, so every limitation of top-down parsing is inherited exactly. Week 2's fix (rewrite the recursion to the right, recover associativity in a fold) is still the fix.

---

## How You Did

**6 correct** — you are ready for the last two weeks.
**4–5** — reread the section you missed; all of it is on the final.
**0–3** — L21 and L22, but **after** Project 1 is submitted.

**This is the last quiz.** Between them, Quizzes 1–11 cover Weeks 0–10, with worked answers — they are the most efficient revision material for the final, and they already exist.

---

*CS 211 · Week 11 · Quiz 11 · © CSE Department*
