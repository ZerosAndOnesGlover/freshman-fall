# CS 211 · Quiz 8

**Sat:** Tuesday of **Week 8**, first 10 minutes of lecture · TH 205
**Covers:** **Week 7** — the lambda calculus: substitution, reduction strategies, encodings, fixed points
**Unmarked.** Recorded in [[_CS 211 Lab and Quiz Record]].

**The answer key is printed below the questions.** Do not look at it until you have written something for all six.

> **Midterm 2 is this evening, 20:00–21:15, and Week 7 is a quarter of it.** This quiz is deliberately
> placed on the morning of the exam. Sit it properly, mark it against the key, and you have a list of
> what to revise with eight hours to do it.

---

## Questions

**1.** *(2 min)* Reduce to normal form, showing every step:

```
(λx y. y x) a (λz. z)
```

---

**2.** *(2 min)* `(λx y. x) y` reduces in one step to `λy′. y` with capture-avoiding substitution, and to `λy. y` without it.

Say what **function** each result is — not what it looks like. Then name the Week 3 concept this is an instance of.

---

**3.** *(2 min)* `(λx y. y) omega one` returns a value under normal order and never terminates under applicative order.

Explain the difference in one sentence. Then say which of the two strategies **every mainstream language** uses, and name one consequence you have seen in Python.

---

**4.** *(1 min)* `Y g` reduces to `g (Y g)`.

Under call-by-value it diverges. Name the subterm that is evaluated over and over, and say why `g` is never entered.

---

**5.** *(2 min)* `Z` is `Y` with one eta-expansion, and `eta_reduce(Z)` is alpha-equivalent to `Y`.

Yet `Z` terminates under call-by-value and `Y` does not. **Two terms that are the same function behave differently.** State precisely what "the same function" is a claim about, so that this is not a contradiction.

---

**6.** *(1 min)* In the Church encoding, `zero`, `false` and `nil` are the same term, and `mult` and `compose` are also the same term.

**Those are two different kinds of fact.** Say what the difference is.

---
---

## Answer Key

**1.**

```
(λx y. y x) a (λz. z)
→  (λy. y a) (λz. z)
→  (λz. z) a
→  a
```

Three beta-reductions; the normal form is **`a`**.

*Application is left-associative, so the term is `((λx y. y x) a) (λz. z)` and the first step consumes `a` alone. Reducing the argument first reaches the same answer — the calculus is confluent — so any correct order scores full marks.*

---

**2.** `λy′. y` is a **constant function**: it ignores its argument and returns the outer free `y`. `λy. y` is **the identity function**: it returns its argument.

Those are opposite functions, one beta-step apart, with no error reported either way.

The Week 3 concept is **lexical scoping** — an occurrence binds to the nearest enclosing binder of that name. Capture is that rule being broken silently, which is exactly what the symbol table in `L07` existed to prevent.

*Full marks require describing the two by **behaviour**. "One has a prime on it" is not an answer.*

---

**3.** **Normal order reduces the leftmost-outermost redex** — the function is applied before its arguments are evaluated, so an argument that is never used is never touched. **Applicative order reduces arguments first**, so `omega` is evaluated whether or not anyone wants it.

**Every mainstream language uses applicative order** — C, Java, Python, Rust, Go, Swift, OCaml.

The consequence in Python: `False and bottom()` returns `False`, but the same logic written as a function, `and_fn(False, bottom())`, diverges. **Short-circuiting is not a property of `and`; it is a property of not being a function.** *(Equally acceptable: `1 if True else bottom()` works because `if` is a keyword; `const(1, bottom())` does not.)*

---

**4.** The repeatedly evaluated subterm is **`x x`**.

`Y g` is `(λx. g (x x)) (λx. g (x x))`. Under call-by-value the **argument** must be reduced to a value before the application happens — and reducing `x x` produces `g (x x)` again, which contains another `x x`. The unfolding never finishes, so `g` is never entered and the base case is never consulted.

*Measured: 44 steps to the size limit.*

---

**5.** **"The same function" is an extensional claim: for every argument, both produce the same result.**

It says nothing about *when* the result is produced, how many reductions it takes, or whether a particular evaluation strategy reaches it at all. So two extensionally equal terms can differ in termination behaviour under a given strategy without any contradiction.

**Eta-conversion preserves meaning and destroys timing**, and that is exactly why eta-expansion — `lambda: expr` in Python, `() => expr` in JavaScript — is the standard way to delay evaluation in a strict language.

---

**6.** **`zero == false == nil` is a *collision*. `mult == compose` is a *theorem*.**

- A **theorem** is a pair any correct encoding would reproduce, because the two operations genuinely coincide: multiplying Church numerals *is* composing functions, since doing something m×n times is doing-it-n-times done m times. Confusing them cannot produce a wrong answer.
- A **collision** is an accident of *this* encoding — three unrelated meanings that all happen to need "take the second alternative". A different encoding of numerals separates `zero` from `false` immediately.

*The prelude contains seven alpha-equivalent pairs: three theorems (`const`/`true`, `apply`/`one`, `compose`/`mult`) and four collisions.*

---

## How You Did

**6 correct** — you are ready for this evening.
**4–5** — reread the section you missed. **You have the whole day.**
**0–3** — Week 7 is 15 of the 75 marks tonight. Read L15 §5 and L16 §7–10 this afternoon, in that order, and reduce three terms by hand.

**Question 5 is the one that discriminates**, and a version of it is on the paper. If you could not answer it, the fix is one idea rather than a topic: *extensional equality is a claim about results only*. Ten minutes with L16 §9 is enough.

---

*CS 211 · Week 8 · Quiz 8 · © CSE Department*
