# CS 211 · Programming Languages & Compilers I
## Week 7 · Lecture 2 of 2
### Encodings, Recursion, and Why Y Hangs in Python

*“Although my own previous enthusiasm has been for syntactically rich languages like the Algol family, I now see clearly and concretely the force of Minsky's 1970 Turing lecture, in which he argued that Lisp's uniformity of structure and power of self reference gave the programmer capabilities whose content was well worth the sacrifice of visual form.”* — Robert W. Floyd, "The Paradigms of Programming" (Turing Award lecture, 1978)

---

**Reading:** Pierce, *TAPL* ch. 5.2 · Barendregt ch. 6 · SICP §1.3, §3.5 · **Next:** L17, types

**Coursework:** 📝 **PS 6** due Fri this week 17:00 · 🔬 **Lab 7** Fri this week 14:00–15:50 · 📊 **Quiz 8** Tue of Week 8 · 📘 **Midterm 2** Tue of Week 8 20:00–21:15 · 📝 **PS 8** released Wed of Week 8, due Fri of Week 9 17:00

---

## 1. The Trick, Stated Once

L15 left a language with no numbers, no booleans, no data structures and no recursion. This lecture builds all four, and there is only one idea:

> **A datum is encoded as the function that uses it.**

A number is not a quantity — it is *the operation of doing something n times*. A boolean is not a bit — it is *the choice between two alternatives*. A pair is not a box with two slots — it is *a function waiting to be told what to do with two things*.

Once you see it, every encoding writes itself. `prelude.lam` has fifty-five definitions and not one of them is clever; they are all this sentence.

---

## 2. Numbers

```
zero  = λf x. x
one   = λf x. f x
two   = λf x. f (f x)
three = λf x. f (f (f x))
```

`three f x` is `f (f (f x))` — apply `f` three times. The numeral **is** its own for-loop.

Arithmetic follows directly from that reading:

```
succ = λn f x. f (n f x)          # do it n times, then once more
add  = λm n f x. m f (n f x)      # do it n times, then m times
mult = λm n f. m (n f)            # do (do it n times) m times
exp  = λm n. n m                  # apply the numeral n to the numeral m
```

`mult` is function composition and `exp` is one application. They are the shortest definitions here.

```
$ python3 lam.py --defs prelude.lam --church 'mult three four'
; ---- normal form in 9 beta-reductions ----
  λf x. f (f (f (f (f (f (f (f (f (f (f (f x)))))))))))
  betas=9 substs=86 renames=0 max_size=45
  decodes to: 12
```

Twelve applications of `f`. Multiplication, in a language with no numbers.

---

## 3. What Arithmetic Costs, and Why It Is Not What You Expect

| term | result | betas | substs | peak size |
|---|---|---|---|---|
| `succ five` | 6 | 3 | 32 | 24 |
| `add three four` | 7 | 6 | 65 | 35 |
| **`mult three four`** | 12 | **9** | 86 | 45 |
| `mult five six` | 30 | 13 | 172 | 93 |
| `exp two five` | 32 | 64 | 818 | 104 |
| **`pred three`** | 2 | **36** | 874 | 227 |
| `pred five` | 4 | 56 | 2067 | 383 |
| `sub six two` | 4 | 126 | 6542 | 521 |
| `eq four four` | true | 272 | 11969 | 722 |

**`pred three` costs four times what `mult three four` costs.** Subtracting one is far more expensive than multiplying, and `sub six two` costs fourteen times a multiplication.

The reason is in the encoding, not in the arithmetic. A numeral can only count **forward** — it applies `f` some number of times, and there is no way to run that backwards. Kleene's predecessor therefore walks forward from the beginning, carrying a pair that lags one step behind, and takes the shadow at the end:

```
shift = λp. pair (snd p) (succ (snd p))
pred  = λn. fst (n shift (pair zero zero))
```

```
(0,0) → (0,1) → (1,2) → (2,3) → ...
```

> **Cost here tracks the shape of the encoding, not the size of the numbers.** That is not a
> property of the lambda calculus; it is a property of *every* representation choice. Week 4
> chose three-address code and got cheap dataflow analysis and expensive aliasing. Week 6 chose
> `Ref` as a distinct class and got precise collection and the ability to move objects. Choosing
> "a number is its own for-loop" makes multiplication free and subtraction quadratic-ish. **The
> representation is the performance model.**

---

## 4. Booleans, and Why `if` Falls Out for Free

A boolean is the choice between two alternatives:

```
true  = λt f. t
false = λt f. f
if    = λp a b. p a b
```

`if` does nothing at all. It hands the two branches to the condition and lets the condition pick, because *picking is what a boolean is*. The definition is pure ceremony — `if p a b` and `p a b` are the same term.

The logical operators are equally direct:

```
not = λp. p false true
and = λp q. p q p
or  = λp q. p p q
```

`and p q` is "if p then q else p". Read it as a choice and it is obvious; read it as boolean algebra and it looks like a trick.

---

## 5. One Term, Three Meanings

Now run the self-test in `church.py` and read the top of the output.

```
$ python3 church.py
; ---- three names, one term ----
  zero = λf x. x    false = λt f. f    nil = λc n. n
  alpha-equivalent: True
```

**`zero`, `false` and `nil` are the same term.** Not similar — `alpha_eq` says identical, and the printed forms differ only in the names of bound variables, which L15 §3 established carry no information.

So a computation that returns `λf x. x` has returned the number zero, and the boolean false, and the empty list, and **there is no fact of the matter about which**. Nothing in the term records an intention. The decoder says so:

```
  ok   iszero three             = 0 (numeral) or False (boolean)
  ok   not true                 = 0 (numeral) or False (boolean)
  ok   leq three two            = 0 (numeral) or False (boolean)
```

That is what **untyped** means, stated concretely. It is not that the language omits type annotations; it is that `add true nil` is a perfectly good term which reduces to something, and no stage of the system will ever object.

### The bug in the test harness, which is the better story

The first version of `church.py` reported **23/23 passed**, including every boolean row. It was wrong, and the reason is worth the detour.

`decode` returned a plain `0` for `λf x. x`, the test expected `False`, and the comparison was `got == want`. In Python, `bool` is a subclass of `int` and **`0 == False` is `True`**. Every boolean test passed by accident, and the collision the tests existed to characterise was invisible.

The fix is one line:

```python
ok = type(got) is type(want) and got == want
```

Seven rows then failed, which is how the collision was found at all.

> **A test harness whose notion of equality is looser than the property under test cannot detect
> a violation of that property.** The tests were not weak on the interesting cases — they were
> weak *precisely* on them, and they reported green. This is the same failure as Week 5's printer
> that misreported a def and Week 6's peak-RSS benchmark that could not see retention: **the
> instrument agreed with the bug.**

---

## 6. Pairs, Lists, and the Fold

A pair is a function waiting to be told what to do with two things:

```
pair = λa b f. f a b
fst  = λp. p (λa b. a)
snd  = λp. p (λa b. b)
```

`fst` passes `true` in disguise; `snd` passes `false`. Selection *is* a boolean.

A list is its own fold:

```
nil    = λc n. n
cons   = λh t c n. c h (t c n)
sum    = λl. l add zero
length = λl. l (λh t. succ t) zero
```

`cons h t` is the function that, given what to do with a head and tail (`c`) and what to do with the empty list (`n`), does it. So `sum` is the list applied to `add` and `zero` — the list runs the fold on itself.

```
  ok   cons one (cons two (cons three nil))   -> [1, 2, 3]
  ok   sum (cons one (cons two (cons three nil))) -> 6 (33 betas)
  ok   length (cons one (cons two nil))       -> 2 (21 betas)
```

Note `nil = λc n. n` is the same term as `false` and `zero` again. **The collision in §5 is not an accident of two encodings; it is what happens when three different notions of "the empty/zero/negative case" all mean "take the second alternative".**

### And it is not the only one

Compare all fifty-five definitions pairwise — 1485 comparisons, four lines of code — and the prelude turns out to contain **seven** alpha-equivalent pairs:

| | | the shared term |
|---|---|---|
| `id` | `unit` | `λx. x` |
| `const` | `true` | `λx y. x` |
| `apply` | `one` | `λf x. f x` |
| **`compose`** | **`mult`** | **`λf g x. f (g x)`** |
| `false` | `nil` | `λt f. f` |
| `false` | `zero` | `λt f. f` |
| `nil` | `zero` | `λc n. n` |

Read the middle row. **Multiplication of Church numerals and composition of functions are the same term** — not analogous, not related, *the same term*. §2 said "do (do it n times) m times" and that sentence is the definition of composition; the encoding makes multiplication *be* composition rather than merely resemble it.

Likewise `const == true`: a function that ignores its second argument and the boolean that selects its first are one term. §6 said `fst` passes `true` in disguise — it would have been equally true to say it passes `const`.

> **These are not all the same kind of fact, and telling them apart is the point.** `compose == mult`
> and `const == true` are **theorems**: they say something true about what multiplication and
> selection *are*, and any correct encoding would reproduce them. `false == zero` is a
> **collision**: two unrelated meanings that happen to need the same shape, and a different
> encoding of numerals would separate them.
>
> The untyped calculus cannot tell you which is which, because it cannot see the intent. **You
> might expect a type system to fix that. Week 8 measures whether it does, and the answer is not
> the one to guess** — `int` and `bool` end up different types not because their representations
> differ, and not because anything was inferred, but because somebody *declared* them so.

---

## 7. Recursion, Without Names

Everything so far avoided the hard one. `fact` needs to call `fact`, and **nothing in this language has a name.** The definitions in `prelude.lam` are abbreviations that `lam.py` expands before reduction begins; they are not part of the calculus, and a definition cannot refer to itself.

The move is to make the recursive call an **argument**:

```
factgen = λr n. if (iszero n) one (mult n (r (pred n)))
```

`factgen` is not factorial. It is a function that, *given factorial*, returns factorial. What we need is a value `F` with `factgen F = F` — a **fixed point**.

```
Y = λf. (λx. f (x x)) (λx. f (x x))
```

Apply `Y` to `g` and reduce once: `(λx. g (x x)) (λx. g (x x))` → `g ((λx. g (x x)) (λx. g (x x)))` = `g (Y g)`. So

$$Y\,g \;=\; g\,(Y\,g)$$

`Y g` unfolds into `g` applied to another copy of itself, on demand, forever. That is recursion, built from self-application, in a language with no names.

```
$ python3 lam.py --defs prelude.lam --church 'fact three'
; ---- normal form in 1525 beta-reductions ----
  λf x. f (f (f (f (f (f x)))))
  betas=1525 substs=66213 renames=174 max_size=2689
  decodes to: 6
```

**Six.** Factorial, with no recursion, no names, no numbers and no conditionals.

---

## 8. Normal Order Is Complete, and Grossly Inefficient

L15 §9 ended with a puzzle: normal order provably finds a normal form whenever one exists, and every real language uses the strategy that provably does not. Here is the missing currency.

`fact` under normal order, against the same computation under call-by-value — and against a third strategy introduced in a moment. Beta-reductions to the answer:

| n | normal order | call-by-value | **call-by-need** | result |
|---|---|---|---|---|
| 1 | 45 | 53 | 45 | 1 |
| 2 | 248 | 119 | **94** | 2 |
| 3 | 1525 | 239 | **177** | 6 |
| 4 | **10384** | 552 | **384** | 24 |
| 5 | *gave up at 60000* | 1864 | **1237** | 120 |
| 6 | *gave up at 60000* | 9539 | **6210** | 720 |

Normal order took 10.90 s at n = 4 and 94.62 s at n = 5 without finishing; call-by-value took 0.11 s and 0.45 s. **At n = 4 that is nineteen times fewer reductions and ninety-nine times faster.**

The cause is duplication. Normal order substitutes an *unevaluated* argument into the body, and if the body mentions its parameter three times, the argument is reduced three times. Call-by-value reduces it once and substitutes the result — which is why it wins, and also why it diverges on `(λx y. y) omega one`, where the argument should never have been reduced at all.

**The third column is the resolution, and it is not a compromise.**

**Call-by-need** takes normal order's rule — never reduce an argument until it is needed — and adds *sharing*: the argument is wrapped in a mutable cell, reduced at most once if it is ever needed, and the result written back. It therefore:

- **terminates exactly where normal order terminates**, because it still never reduces an unneeded argument; and
- **beats call-by-value at every n ≥ 2**, because it never reduces a needed argument twice either.

> **Laziness in a real language is normal order plus a memo table, and the memo table is the whole
> engineering contribution.** Haskell is call-by-need. The theory said normal order was the
> complete strategy and the measurements said it was unusable; sharing is what reconciles them,
> and it is an *implementation* technique that changes no result — only how many times each
> result is computed.

*(PS 7 Part B3 asks you to build it. It is about thirty-five lines.)*

---

## 9. Why Y Hangs in Python

Now the result this lecture is named for.

```
$ python3 lam.py --defs prelude.lam '(Y factgen) three' --strategy cbv --max-size 5000
; ---- DIVERGED after 44 steps: term grew to 5059 nodes ----
  the term is EXPANDING: 5059 nodes and still growing
```

**Forty-four steps.** Under call-by-value, `Y g` = `(λx. g (x x)) (λx. g (x x))` must reduce its argument `(x x)` before applying `g` — and reducing `(x x)` produces `g (x x)` again. The unfolding never reaches `factgen`, so the base case is never consulted.

The standard repair is the **Z combinator**:

```
Z = λf. (λx. f (λv. x x v)) (λx. f (λv. x x v))
```

`λv. x x v` is an *abstraction*, and under call-by-value an abstraction is a **value** — the evaluator does not look inside it. The unfolding stops until the recursive call is actually made.

And notice what Z is:

```
$ python3 -c "
from lam import load, eta_reduce, show, alpha_eq
e = load('prelude.lam')
print('  Y      =', show(e['Y']))
print('  Z      =', show(e['Z']))
print('  eta(Z) =', show(eta_reduce(e['Z'])))
print('  eta(Z) is alpha-equivalent to Y?', alpha_eq(eta_reduce(e['Z']), e['Y']))
"
```

```
  Y      = λf. (λx. f (x x)) (λx. f (x x))
  Z      = λf. (λx. f (λv. x x v)) (λx. f (λv. x x v))
  eta(Z) = λf. (λx. f (x x)) (λx. f (x x))
  eta(Z) is alpha-equivalent to Y? True
```

**Z eta-reduces to Y.** They are the same function extensionally — L15 §3 said `λx. f x` and `f` behave identically on every argument — and they have completely different termination behaviour under call-by-value.

> **Eta-conversion preserves meaning and destroys timing.** That is not a paradox; it is the
> precise statement that "the same function" is a claim about *results*, and evaluation order is
> a claim about *when*. Eta-expansion is the standard way to delay evaluation in a strict
> language, and every `() => expr` in JavaScript and `lambda: expr` in Python is this.

---

## 10. Z Is Not Enough, and the Reason Is `if`

Run Z and it still diverges:

```
$ python3 lam.py --defs prelude.lam '(Z factgen) three' --strategy cbv --max-size 5000
; ---- DIVERGED after 3911 steps: term grew to 5011 nodes ----
```

Better — 3911 steps instead of 44 — and still wrong.

**The problem is no longer the fixed-point combinator. It is `if`.** §4 defined `if = λp a b. p a b`: an ordinary function of three arguments. Under call-by-value, *all three arguments are evaluated before it is applied* — including `mult n (r (pred n))`, the recursive branch, on every call, including when `n` is zero.

No fixed-point combinator can fix that, because the recursion is not what is unfolding. The conditional is.

The fix is to pass the branches as **thunks** and force the chosen one:

```
unit     = λu. u
lazyif   = λp a b. p a b unit
factgenV = λr n. lazyif (iszero n) (λu. one) (λu. mult n (r (pred n)))
```

```
$ python3 lam.py --defs prelude.lam --church 'factV three' --strategy cbv
; ---- value in 175 beta-reductions ----
  ...
  the value is not yet a numeral; normalising it took a further 64 beta-reductions
  λf x. f (f (f (f (f (f x)))))
  decodes to: 6
```

Note what call-by-value returned: a **value**, not a numeral. Its body is unreduced, because a function body has not "happened" until the function is called. Turning it into six visible applications of `f` took 64 further reductions — and that is not the collector's work or the compiler's, it is **what printing is**. A REPL that shows you `6` has forced a computation the evaluator deliberately did not perform.

Three attempts, one table:

| | call-by-value result |
|---|---|
| `Y` + `if` as a function | **diverges**, 44 steps |
| `Z` + `if` as a function | **diverges**, 3911 steps |
| **`Z` + thunked branches** | **6**, in 175 + 64 beta-reductions |

> **This is why `if` is a keyword and not a library function, in every strict language ever
> shipped.** C, Java, Python, Rust and Go all make the conditional part of the *grammar*,
> evaluated by the compiler rather than by the calling convention — because a function cannot
> decline to evaluate its arguments, and a conditional's entire job is to decline.

---

## 11. All of It, in Python

None of §9 or §10 is an artefact of our interpreter.

```
$ python3 strict.py
  const(1, bottom())             = RecursionError
    The function never uses its second argument. Python evaluated it anyway.
  1 if True else bottom()        = 1
  const(1, lambda: bottom())     = 1

  False and bottom()             = False
  and_fn(False, bottom())        = RecursionError
    The identical logic, written as a function, diverges.

  Y(factgen)                     = RecursionError  <- before it was ever applied to 5
  Z(factgen)(5)                  = 120
  Z(factgen)(n) for n = 0..9     = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
  Z(fibgen)(n)  for n = 0..9     = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

Four things there are worth stating plainly.

1. **`const(1, bottom())` diverges** — Python evaluated an argument the function never reads.
2. **`False and bottom()` returns `False`, and `and_fn(False, bottom())` diverges.** Identical logic. Short-circuiting is not a property of `and`; **it is a property of not being a function.**
3. **`Y(factgen)` raises before it is ever applied to a number.** The combinator, in Python, verbatim from `prelude.lam`, diverging for the reason §9 gives.
4. **`Z(factgen)(5)` is 120**, and `Z(fibgen)` produces the Fibonacci numbers, with **no function anywhere referring to itself by name.**

---

## 12. Taking the Names Out

L15 §7 measured that capture avoidance rarely fires, which undercuts the usual argument for de Bruijn indices. Here is the honest version of that argument.

A bound variable's name carries no information, so do not store it — store how many binders out its own binder is:

```
  \x. x        ->  (λ. 0)
  \x y. x      ->  (λ. (λ. 1))
  two          ->  (λ. (λ. (1 (1 0))))
  add          ->  (λ. (λ. (λ. (λ. ((3 1) ((2 1) 0))))))
```

Two things become true immediately:

- **Alpha-equivalence is structural equality.** `alpha_eq` is replaced by `==`.
- **Capture cannot happen**, because there is no name to capture. `subst_db` has no `fresh`, no `free_vars`, and no rename branch. L15 §5's hazard is *gone*, not handled.

```
  (λx y. x) == (λa b. a) as trees?  True
  (λx y. x) == (λa b. b) as trees?  False
  (λx y. x) y  ->  nameless (λ. y)   named λx. y
```

And the cost:

| term | result | betas named | betas db | named visits | nameless visits |
|---|---|---|---|---|---|
| `mult three four` | 12 | 9 | **9** | 86 | 416 |
| `exp two five` | 32 | 64 | **64** | 818 | 7509 |
| `pred five` | 4 | 56 | **56** | 2067 | 61917 |
| `fact three` | 6 | 1525 | **1525** | 66213 | 4911712 |
| `factV five` | 120 | 368 | **368** | 7372 | 206447 |

**The beta counts agree exactly** — both representations perform the same reductions. And the naive nameless version is **five to seventy-four times more expensive per step**, because every beta-reduction needs two extra full traversals to shift indices.

> **De Bruijn indices do not make substitution faster. They make capture impossible.** The hazard
> did not vanish — it changed shape, from "a variable silently rebound" into "an index off by
> one", and an off-by-one shows up on the first test while capture shows up in production. That
> is the trade, and it is worth making.
>
> The *speed* win that de Bruijn is usually credited with comes from a different change
> altogether: stop substituting. Real implementations carry an **environment** and build
> **closures**, so the argument is never copied into the body at all. That is next term's
> material, and it is what your Cyan compiler will need in Project 1.

---

## 13. Turing Equivalence, and Why It Matters Here

Church (1936) and Turing (1937) proposed two definitions of "effectively computable" — the lambda calculus and the Turing machine — and proved them equivalent. Anything one can compute, so can the other.

The **Church–Turing thesis** is the claim that this shared notion is *the* notion of computability. It is not a theorem; there is nothing to prove it against. It is a claim that every formalism anyone has proposed since — general recursive functions, register machines, cellular automata, your Cyan compiler — has turned out to define the same set of functions.

Two consequences that matter for this course.

**Expressiveness is not the interesting axis.** Every general-purpose language computes exactly the same functions. When you argue that one is more powerful than another you are never talking about computability — you are talking about how much has to be said, how much can be checked before it runs, and what the compiler can do with what you wrote. That is the real subject of this course, and Week 12 is entirely about it.

**Undecidability is inherited.** L15 §8 said no interpreter can decide whether a term has a normal form. By the equivalence, that is the halting problem, and it means your compiler cannot decide whether an arbitrary program terminates, whether two functions are equal, or whether a piece of code is reachable. **Every static analysis you have written this term is an approximation, and had to be.** Week 5's liveness was a *may* analysis and Week 5's dominance a *must* analysis for this reason — one over-approximates, one under-approximates, and neither can be exact.

---

## 14. What to Take From This

1. **A datum is the function that uses it.** Numbers are for-loops, booleans are choices, pairs are functions awaiting instructions, lists are their own folds.
2. **Cost tracks the encoding's shape**, not the size of the data: `pred three` costs 4× `mult three four`, because numerals only count forward.
3. **`zero`, `false` and `nil` are the same term.** That is what "untyped" means, and it is why Week 8 exists.
4. **A test harness looser than the property under test reports green.** `0 == False` hid the collision on exactly the cases that mattered.
5. **`Y g = g (Y g)`** gives recursion with no names, and `fact three` = 6 in 1525 reductions.
6. **Normal order is complete and grossly inefficient** — 19× more reductions and 99× slower at n=4, because it duplicates unevaluated arguments. Call-by-need is normal order plus sharing.
7. **Y diverges under call-by-value in 44 steps**; Z survives 3911 and still diverges; only thunked branches work.
8. **`eta(Z) == Y`, verified.** Eta-conversion preserves meaning and destroys timing.
9. **`if` is a keyword because a function cannot decline to evaluate its arguments** — and short-circuiting is a property of not being a function, demonstrated in Python.
10. **De Bruijn indices make capture impossible and each step more expensive.** Identical beta counts, 5–74× the per-step cost; the speed comes from environments, not indices.
11. **Everything computable is computable here.** So expressiveness is never the argument, and undecidability is why every analysis you have written is an approximation.

**Next week the terms stop being untyped.** §5's collision is the problem, and a type system is the answer — along with the discovery that the typed lambda calculus loses exactly one thing, and it is the one thing §7 needed.

---

*CS 211 · Week 7 · Lecture 16 · © CSE Department*
