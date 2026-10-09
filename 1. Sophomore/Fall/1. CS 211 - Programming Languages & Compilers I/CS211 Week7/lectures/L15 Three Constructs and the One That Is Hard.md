# CS 211 · Programming Languages & Compilers I
## Week 7 · Lecture 1 of 2
### Three Constructs, and the One That Is Hard

*“Scheme programming language demonstrates that a very small number of rules for forming expressions, with few restrictions on how they are composed, suffice to form a practical and efficient programming language that is flexible enough to support most of the major programming paradigms in use today.”* — Gerald Jay Sussman, on receiving the Taylor L. Booth Education Award

---

**Reading:** Pierce, *TAPL* ch. 5 · Barendregt ch. 2–3 · SICP §1.3 · **Next:** L16, encodings, recursion, and evaluation order

**Coursework:** 📊 **Quiz 7** today · 📝 **PS 7** released Wed this week, due Fri of Week 8 17:00 · 📝 **PS 6** due Fri this week 17:00 · 🔬 **Lab 7** Fri this week 14:00–15:50 · 📘 **Midterm 2** Tue of Week 8 20:00–21:15

---

## 1. Your Compiler Has Been Parsing These Since Week 2

Week 6 opened by grepping for `free` and finding that `alloc` had been a promise since Week 4. Do the same thing again, with a different word.

```cyan
fn twice() -> int {
  let inc = fn(n: int) -> int { return n + 1; };
  return apply(inc, 41);
}
```

The parser accepts it — `parser.py:380` builds a `Lambda` node, and has since Week 2. The type checker accepts it — `typecheck.py:298` gives it the type `fn(int) -> int`, and has since Week 3. Then:

```
$ python3 tac.py lam.cy twice
```

```
  File "tac.py", line 212, in gen_expr
    raise NotImplementedError(k)
NotImplementedError: Lambda
```

**Two phases understand anonymous functions and the third has never been asked to emit one.** `grep -n Lambda tac.py` returns nothing at all.

That is not an oversight, and it is why this week exists. Lowering a lambda is not one more `elif` branch. A function value that can be returned, stored, and called later has to capture the variables it mentions — which means those variables cannot live in the stack frame that created them, which means Week 6's heap, which means the collector needs a `SLOTS` entry for a kind of object we have not defined. **Project 1 lists "first-class functions" as one of the two hardest features on its menu for exactly this reason.**

So before writing that code, this week asks what a function *is*. The answer turns out to be short enough to fit on one line, and strong enough to compute anything computable.

---

## 2. The Whole Language

```
    x           a variable
    λx. e       an abstraction — the function of x whose body is e
    e₁ e₂       an application — e₁ applied to e₂
```

That is the entire grammar. There are:

- **no numbers** — no integer literals, no arithmetic
- **no booleans**, no `if`, no comparison
- **no data structures** — no arrays, no structs, no lists
- **no assignment**, no mutation, no statements
- **no recursion** — a function cannot name itself, because *nothing* has a name
- **no types**
- **no heap**, no stack, no memory model of any kind

Week 6 spent two lectures on what to do about memory. **This language does not have any, and is Turing-complete anyway.**

Three conventions make it readable, and all three are standard:

| convention | meaning |
|---|---|
| application associates **left** | `f a b` is `(f a) b` |
| abstraction bodies extend **right** | `λx. f x` is `λx. (f x)`, never `(λx. f) x` |
| `λx y. e` abbreviates `λx. λy. e` | **currying** — every function takes exactly one argument |

That last one is not sugar in a small way. It is the reason this calculus needs no notion of "a function of two arguments": a two-argument function is a one-argument function that returns a one-argument function. `lam.py`'s parser implements it in three lines, and every multi-argument function you have written in any language is this underneath.

---

## 3. Reduction: The Only Rule

There is one computational rule, **beta-reduction**:

$$(\lambda x.\, e)\; a \;\longrightarrow\; e[x := a]$$

Apply a function to an argument by substituting the argument for the parameter in the body. That is all computation is here.

```
$ python3 lam.py '(\x. x) y'
; ---- normal form in 1 beta-reductions ----
  y
```

A term with no reducible application anywhere is in **normal form** — it is finished. `lam.py` reduces until it reaches one:

```
$ python3 lam.py '(\x y. x) a b'
; ---- normal form in 2 beta-reductions ----
  a
```

Two steps, because `(λx y. x) a b` is `((λx. λy. x) a) b`: the first step consumes `a`, leaving `λy. a`, and the second consumes `b`.

**Alpha-equivalence** is the other half of the setup. `λx. x` and `λy. y` are the same function; the name of a bound variable is not data. `lam.py` provides `alpha_eq` for exactly this, because any test comparing printed forms would call them different.

**Eta-conversion** is the third: `λx. f x` and `f` behave identically on every argument, so they are the same function.

```
$ python3 lam.py '\x. f x' --eta
  f
```

That is not a curiosity — it is a real compiler transformation under the name **eta-reduction**, and it is why a wrapper function that only forwards its argument costs nothing after optimisation. §7 of L16 shows it doing something much less decorative.

---

## 4. Substitution Is the Hard Part

Everything above took three paragraphs. Now the function that implements it.

Substitution has three cases and two of them are trivial:

```python
if isinstance(t, Var):
    return s if t.name == x else t
if isinstance(t, App):
    return App(subst(t.fn, ...), subst(t.arg, ...))
```

The third case is `Abs`, and it is where every implementation of this calculus goes wrong at least once.

Substituting into the body of a binder moves the replacement term **underneath that binder**. If the replacement has a free variable whose name matches the binder's parameter, that variable stops referring to whatever it referred to outside, and starts referring to the parameter.

It has been **captured**.

---

## 5. What Capture Costs, Measured

`lam.py` ships a `--naive` switch that disables capture avoidance and does nothing else. One term, one beta-step, both ways:

```
$ python3 lam.py '(\x y. x) y'
; ---- normal form in 1 beta-reductions ----
  λy0. y
  betas=1 substs=3 renames=1 max_size=5
```

```
$ python3 lam.py '(\x y. x) y' --naive
; ---- normal form in 1 beta-reductions ----
  λy. y
  betas=1 substs=2 renames=0 max_size=5
```

Read what those two terms are.

| | result | what it is |
|---|---|---|
| correct | `λy0. y` | **a constant function** — ignores its argument, returns the outer `y` |
| naive | `λy. y` | **the identity function** — returns its argument |

**Those are not similar functions. They are opposite functions**, and one beta-step separates them.

The naive result is a perfectly well-formed term. Nothing raises. Nothing warns. It reduces, it prints, it has a normal form, and every downstream computation proceeds happily on an answer that is not the one the program asked for.

> **This is the fourth time this term, and the pattern has not changed.** Week 4's folder turned
> `-301` into `-401`. Week 5's dead-code pass deleted a live `load`. Week 6's root set freed an
> object the next instruction wrote through. Each was a silent wrong answer produced by code that
> looked reasonable, and each was found by *running the thing and reading the output* rather than
> by the compiler complaining.

The fix is to rename the binder before descending:

```python
fs = free_vars(s)
if t.param in fs:
    if stats:
        stats.renames += 1
    new = fresh(t.param, fs | free_vars(t.body) | {x})
    body = subst(t.body, t.param, Var(new), stats, naive)
    return Abs(new, subst(body, x, s, stats, naive))
```

`λy0` in the correct output is that rename. The binder was renamed so that the incoming free `y` could pass underneath it without colliding.

---

## 6. Capture Is Week 3's Bug, in a Language With Three Constructs

Look at what capture actually is: **a variable silently rebound to the wrong binder.**

That is scope. It is precisely the failure Week 3's symbol table was built to prevent — `L07 Symbol Tables, Scope, and the First Phase That Says No` spent a lecture on chained scopes so that an inner declaration would shadow an outer one *deliberately* and never by accident.

Here there is no symbol table, no chain, and no phase that says no. There are three constructs. **And the bug is still there**, which is the most useful thing this lecture can tell you about it:

> **Capture is not an artefact of complicated languages.** It is the minimum price of having
> binders and substitution at all. Every language with local variables and any form of inlining
> has this problem, and the ones that appear not to have solved it somewhere you cannot see.

C's preprocessor is the standard example of *not* solving it. `#define SWAP(a,b) { int t=a; a=b; b=t; }` invoked as `SWAP(x,t)` captures `t`, and the result compiles cleanly and swaps the wrong things. That macro system substitutes without renaming — it is `--naive`, shipped, in a language with three billion lines of deployed code. Scheme's `syntax-rules` and Rust's `macro_rules!` are called **hygienic** macro systems, and the hygiene they mean is exactly this renaming.

---

## 7. How Often Does It Actually Fire?

Here the measurement disagrees with the usual motivation, so it is worth taking seriously.

Capture avoidance is normally introduced as expensive — you must compute `free_vars` of the replacement on every abstraction. So measure it, across the whole prelude:

| term | betas | substs | **renames** | renames per beta |
|---|---|---|---|---|
| `mult three four` | 9 | 86 | **0** | 0.00 |
| `pred five` | 56 | 2067 | **0** | 0.00 |
| `eq three three` | 180 | 6135 | **0** | 0.00 |
| `exp two five` | 64 | 818 | 21 | 0.33 |
| `fact three` | 1525 | 66213 | 174 | 0.11 |
| `fact four` | 10384 | 595158 | 543 | 0.05 |
| `factV five` | 368 | 7372 | **0** | 0.00 |

**Renaming almost never fires.** Four of the seven terms never rename once, and the worst case is one rename per three reductions.

Now look at the column next to it. `fact four` performs 10,384 beta-reductions and **595,158 substitution visits** — fifty-seven nodes entered per reduction. *That* is where the time goes, and it has nothing to do with capture.

> **The textbook motivation for de Bruijn indices is that renaming is expensive. On this workload
> it is not.** The real argument for them is the one §5 made: renaming is a **correctness** hazard
> whose failure is silent. L16 §9 measures what removing it costs, and the answer is not what the
> motivation predicts either.

---

## 8. Normal Forms, and the Term That Has None

Not every term finishes.

```
omega = (λx. x x) (λx. x x)
```

Beta-reduce it: substitute `λx. x x` for `x` in `x x`, giving `(λx. x x) (λx. x x)`. **The same term.** It reduces to itself, in one step, forever.

```
$ python3 lam.py --defs prelude.lam omega --limit 50
; ---- DIVERGED after 50 steps: step limit ----
```

`omega` is the smallest term with no normal form, and it is four characters of actual content. Two facts follow, and the second is the one people skip.

**First:** the lambda calculus can express non-termination without a loop keyword, a `goto`, or recursion. Self-application is enough.

**Second, and read the message carefully:**

```
  NOTE: this does not prove there is no normal form. That question is undecidable.
```

`lam.py` reports that *it stopped looking*, and nothing more. Deciding whether an arbitrary term has a normal form is **undecidable** — it is the halting problem in different notation. An interpreter cannot tell you a term diverges; it can only tell you it has not finished yet.

That is why `Diverged` carries a reason:

```python
raise Diverged(t, n, f"term grew to {sz} nodes")
```

"I stopped after 10,000 steps" and "the term reached 400,000 nodes and is still expanding" are different pieces of evidence about the same undecidable question, and the second is much more informative. Neither is a proof.

---

## 9. Two Ways to Reduce, and They Do Not Agree

`omega` diverges under any strategy. The interesting case is a term where the *strategy decides*.

```
(λx y. y) omega one
```

The function ignores its first argument. Does the argument have to terminate anyway?

```
$ python3 lam.py --defs prelude.lam '(\x y. y) omega one' --strategy normal
; ---- normal form in 2 beta-reductions ----
  λf x. f x

$ python3 lam.py --defs prelude.lam '(\x y. y) omega one' --strategy applicative
; ---- DIVERGED after 20000 steps ----
```

**Same term. One strategy answers in two steps; the other never answers.**

- **Normal order** reduces the **leftmost-outermost** redex — the function is applied before its arguments are evaluated, so an unused argument is never touched.
- **Applicative order** reduces the **leftmost-innermost** redex — arguments are reduced to normal form before the function is applied, so `omega` is evaluated whether or not anyone wants it.

There is a theorem here, and it is the reason normal order has its name:

> **Standardisation theorem.** If a term has a normal form, normal-order reduction will find it.

No strategy can do better than that, and applicative order demonstrably does worse. Which raises an obvious question — why does any real language use applicative order?

**Every mainstream language uses it.** C, Java, Python, Rust, Go, Swift, OCaml: all evaluate arguments before the call. They have all chosen the strategy that provably fails on terms where the other succeeds.

L16 §6 measures why, and the answer is that normal order pays for its completeness in a currency this lecture has not mentioned yet.

---

## 10. What to Take From This

1. **Your parser and type checker have handled anonymous functions since Weeks 2 and 3**; `tac.py` has never been asked to emit one, because a function value has to capture its environment, and that means the heap.
2. **Three constructs.** No numbers, no booleans, no data, no recursion, no types, no memory — and Turing-complete.
3. **Currying is why every function takes one argument.** A two-argument function is a function returning a function, and always was.
4. **Beta-reduction is the only rule.** Alpha says names of bound variables do not matter; eta says a forwarding wrapper is the thing it forwards to.
5. **Substitution is the hard part, and its failure is silent.** `(λx y. x) y` gives a constant function correctly and **the identity function** naively — opposite functions, one step apart, no error.
6. **Capture is Week 3's scope bug in a language with three constructs.** It is the price of binders, not of complexity, and C's preprocessor pays it in production.
7. **Renaming fires rarely** — 0 for most terms here — so the case for de Bruijn indices is correctness, not speed. The measurement contradicts the usual motivation.
8. **`omega` has no normal form**, and no interpreter can tell you that; it can only report that it stopped looking. Undecidability is not an abstraction, it is why the error message is worded that way.
9. **Evaluation order changes whether a program terminates**, not merely how fast it runs — and every language you use has picked the strategy that fails.

**Next:** how three constructs get you numbers, booleans, lists and recursion — and why the Y combinator hangs in Python.

---

*CS 211 · Week 7 · Lecture 15 · © CSE Department*
