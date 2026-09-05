# CS 211 · Programming Languages & Compilers I
## Week 10 · Lecture 1 of 2
### Code as Data, and the Macro That Is `if`

---

**Reading:** SICP §4.1 · Graham, *On Lisp* ch. 7–8 · Kohlbecker et al. (1986) on hygiene · **Next:** L22, DSLs, combinators, and what they cost

---

## 1. A Question Week 7 Left Unfinished

Week 7 proved a rule and Week 7 measured it:

> **In a strict language, `if` cannot be an ordinary function**, because a function's arguments are
> evaluated before it is entered, and a conditional's entire job is to decline to evaluate one of
> its branches.

The consequence was concrete. `(Z factgen) three` diverged under call-by-value after 3911 steps — not because the fixed-point combinator was wrong, but because `if` was a function and evaluated *both* branches, including the recursive one. The fix was thunks: `lazyif`, and `(λu. …)` around each branch.

That is one way out, and it is the way a *functional* language takes. There is another, and it does not require the caller to wrap anything.

**Make the thing that is not a function.**

---

## 2. What a Macro Is

A **macro** is not a function. Two differences, and everything follows from them:

| | function | macro |
|---|---|---|
| runs at | **run time** | **expansion time**, before evaluation |
| receives | the **values** of its arguments | the **unevaluated syntax** of its arguments |
| returns | a value | **a program**, which is then evaluated |

In `lisp.py` the two implementations are identical:

```python
class Lambda:
    __slots__ = ('params', 'body', 'env')

class Macro:
    """Identical to `Lambda` in every respect except **when** it runs and
    whether its arguments were evaluated first."""
    __slots__ = ('params', 'body', 'env')
```

Same three fields. The difference is one line in the evaluator:

```python
if isinstance(m, Macro):
    # THE line. The arguments go in UNEVALUATED -- as the syntax the
    # programmer wrote, not as the values it would produce.
    local = Env(m.params, form[1:], m.env)
    return eval_seq(m.body, local), True
```

`form[1:]` is the raw argument forms. A function call would have evaluated them first.

---

## 3. The Measurement

`unless`, defined twice, as identically as the two mechanisms allow:

```lisp
(define unless-fn  (lambda (test body) (if test nil body)))
(defmacro unless-mac (test body) `(if ,test nil ,body))
```

`boom` is a primitive that raises if it is ever evaluated.

```
$ python3 demo.py
  (unless-fn #t (boom))      => ERROR: boom was evaluated
  (unless-mac #t (boom))     => nil

  (unless-fn #f 42)          => 42
  (unless-mac #f 42)         => 42
```

**The function evaluated the branch it was about to discard.** Both definitions say "if the test holds, return nothing; otherwise return the body" — and only one of them can be written as a function without changing how callers write their code.

That is Week 7 §10's result, and this is the other way out of it. Week 7's fix put the burden on the *caller*, who had to wrap every branch in `(λu. …)`. A macro puts it on the *definition*, once, and callers write ordinary-looking code.

> **`if` is a special form in the evaluator because it has to be. `unless` is not**, and it does
> not have to be — a macro is enough. **The line between "language feature" and "library code"
> moved**, and that is what this week is about.

---

## 4. Why This Works in Lisp: Code Is Data

The macro above built a program with a backquote. It could do that because in Lisp there is nothing else a program *could* be:

```
  (quote (if a b c))                     => (if a b c)
  (car (quote (if a b c)))               => if
  (length (quote (if a b c)))            => 4
  (cons (quote *) (cdr (quote (+ 2 3)))) => (* 2 3)
```

Read the last line. It took a program, `(+ 2 3)`, dropped its head with `cdr`, stuck `*` on the front with `cons`, and **produced a different program** — using the same two list operations you would use on a shopping list.

**A Lisp program is a Lisp list.** That is **homoiconicity**, and it is why a macro is not a special mechanism: it is an ordinary function from lists to lists, written in the same language, using the same operations.

Note what follows for the front end:

```python
def read(src):
    """Text -> nested Python lists. **This is the whole front end.**"""
```

About thirty lines. **Weeks 1 and 2 spent a fortnight on lexing and parsing** — DFAs, LL(1), FIRST/FOLLOW, LR items, shift-reduce conflicts. Lisp's syntax is the data structure, so there is almost nothing to parse. The parentheses everybody complains about are the price of that, paid once, in exchange for macros being trivial.

*(This is a design trade, not a free lunch. L22 §2 is the other side of it.)*

---

## 5. Adding a Loop to the Language

If `unless` can be library code, so can control flow. Here is `while`, in six lines, with no change to the evaluator:

```lisp
(defmacro while (test . body)
  `(begin
     (define loop-fn
       (lambda () (if ,test (begin ,@body (loop-fn)) nil)))
     (loop-fn)))
```

```
  (while (< i 5) (set! total (+ total i)) (set! i (+ i 1)))
  total   => 10
```

Correct — 0+1+2+3+4. **A user added a loop to the language**, in a file, without touching `lisp.py`.

Two details in that macro are worth naming.

**`(test . body)` is a rest parameter** — a loop body is an arbitrary number of forms, so the macro must accept any number. *(The first version of `Env` did not support this and bound `.` as a parameter name, which spliced the body wrongly and produced `unbound symbol: set!`. Rest parameters are not a convenience here; without them `while` cannot be written.)*

**`,@body` is unquote-splicing** — it drops the forms *into* the surrounding list rather than nesting them. `,` inserts one thing; `,@` inserts several.

---

## 6. And Then It Is Gone

Ask what the evaluator actually sees:

```
  (unless-mac #t (boom))          expands to  (if #t nil (boom))
  (unless-mac (> x 3) (print x))  expands to  (if (> x 3) nil (print x))
```

**No macro survives into the evaluated program.** Expansion happens once, before anything runs; what executes is ordinary code built out of primitives.

You have seen this shape before, twice.

- **Week 8's dictionary passing.** `member : Eq a => a -> List a -> Bool` elaborated to `member : DictEq a -> a -> List a -> Bool`. The `=>` became a `->`, and nothing type-class-shaped survived into the compiled program.
- **Week 6's `let`-desugaring** and Week 7's `λx y. e`. Currying is not implemented in the evaluator; it is expanded away by the parser.

> **This is the standard shape of a language feature that is not really a language feature.**
> Something rich at the source level, an expansion pass, and a small core underneath that never
> hears about it. The trade is always the same: **the core stays small and the error messages get
> worse**, because by the time anything goes wrong the thing the programmer wrote is gone.

---

## 7. Capture: Week 7's Bug, Shipped

Here is a `swap` macro. It needs a temporary.

```lisp
(defmacro swap-bad (a b)
  `(begin (define tmp ,a) (set! ,a ,b) (set! ,b tmp)))
```

It works:

```
  (swap-bad x y)      => (2 1)     correct
```

Now the caller happens to have a variable of their own called `tmp`:

```
  (swap-bad tmp z)    => (7 7)     expected (7 100)
  expands to  (begin (define tmp tmp) (set! tmp z) (set! z tmp))
```

**Look at the expansion.** `(define tmp tmp)` — the macro's temporary and the caller's variable are the same name, so the macro clobbered the value it was supposed to be saving. No error. A plausible wrong answer.

**This is variable capture**, and you have met it before under exactly that name.

Week 7 §5 measured it in `subst`: `(λx y. x) y` gives a *constant function* correctly and **the identity function** naively, one beta-step apart, with nothing raised. Week 7 §6 then said this:

> C's preprocessor is the standard example of *not* solving it. `#define SWAP(a,b) { int t=a; a=b; b=t; }`
> invoked as `SWAP(x,t)` captures `t`, and the result compiles cleanly and swaps the wrong things.

**That is the program above.** Week 7 described it; Week 10 runs it.

The fix is the same fix:

```lisp
(defmacro swap (a b)
  (define g (gensym))
  `(begin (define ,g ,a) (set! ,a ,b) (set! ,b ,g)))
```

```
  (swap tmp z)   => (7 100)   correct
  expands to  (begin (define g1 tmp) (set! tmp z) (set! z g1))
```

**`gensym` is `fresh`** — Week 7's function for inventing a name nothing else is using, under a different name, solving the same problem for the same reason.

> A macro system that does this **automatically**, so that a macro's names can never collide with a
> caller's, is called **hygienic**. Scheme's `syntax-rules` and Rust's `macro_rules!` are hygienic;
> Common Lisp's `defmacro` and C's preprocessor are not, and in those you call `gensym` by hand or
> ship the bug.
>
> **Hygiene is not a nicety. It is the difference between a macro system that composes and one
> where every macro is a trap for the next person's variable names.**

---

## 8. What to Take From This

1. **Week 7 said `if` cannot be a function. A macro can be**, because it runs at expansion time on unevaluated syntax.
2. **`Macro` and `Lambda` are the same three fields.** The difference is *when* it runs and whether the arguments were evaluated — one line in the evaluator.
3. **Measured:** `(unless-fn #t (boom))` raises and `(unless-mac #t (boom))` returns `nil`. Same idea, two mechanisms, one of them wrong for this job.
4. **A Lisp program is a Lisp list.** `(cons '* (cdr '(+ 2 3)))` builds a program out of a program with `cons` and `cdr`.
5. **The whole front end is thirty lines**, because the syntax *is* the data structure — the fortnight Weeks 1–2 spent on parsing is the price Lisp declines to pay, and parentheses are the bill.
6. **`while` is six lines of library code**, and it needed rest parameters and unquote-splicing to be writable at all.
7. **No macro survives expansion.** Same shape as Week 8's dictionaries and Week 7's currying: rich surface, expansion pass, small core.
8. **Capture is Week 7's bug in a new setting** — `(define tmp tmp)`, wrong answer, no error — and `gensym` is Week 7's `fresh`.
9. **Hygienic macro systems do that renaming for you.** C's preprocessor does not, which is why `SWAP` is famous.

**Next:** what happens when you use this to build a *language* rather than a control structure — internal against external DSLs, parser combinators, and the cost nobody advertises.

---

*CS 211 · Week 10 · Lecture 21 · © CSE Department*
