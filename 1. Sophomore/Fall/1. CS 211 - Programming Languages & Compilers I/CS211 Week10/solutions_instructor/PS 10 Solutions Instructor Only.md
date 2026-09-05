# CS 211 · Problem Set 10 — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** Verified against the Week 10 lab code on Python 3.14.2.

> **Mark this one with the calendar in mind.** PS 10 and Project 1 fall on the same Friday, and
> the brief explicitly tells students to prioritise the project and take the dropped-PS allowance.
> **A submission of Parts A, C and D with a note explaining the choice is a fully respectable
> outcome** and should be marked on what is there, not on what is missing.

---

## Part A — Macros (20)

**A1.** *(5)* The four lines as in the Lab 10 solutions. The function raised because **its arguments were evaluated before it was entered**. Week 7 **§10**, where `(Z factgen) three` diverged for the same reason.

**A2.** *(5)* Any correct macros. Reference shapes:

```lisp
(defmacro my-and (. cs) (if (null? cs) #t
  (if (null? (cdr cs)) (car cs) `(if ,(car cs) (my-and ,@(cdr cs)) #f))))
(defmacro my-or  (. cs) ...)
(defmacro cond (. clauses) ...)
```

**Require a `boom` demonstration for each** — the point is the short-circuit, not the syntax.

**A3.** *(5)* `(swap-bad tmp z)` → `(7 7)`; expansion `(begin (define tmp tmp) (set! tmp z) (set! z tmp))`; the macro's `tmp` and the caller's collided.

The second macro must produce a **wrong answer rather than an error** — the usual shape is a macro with an accumulator or counter variable, called in a scope where that name is live.

**A4.** *(5 — the discriminating question)*

Verified:

```lisp
(defmacro double (x) `(+ ,x ,x))
(double 5)                                          => 10
((lambda (+) (double 5)) (lambda (a b) (* a b)))    => 25
```

The macro's `+` resolved to **the caller's** binding, so `double` multiplied.

**`gensym` does not fix this** because the problem is not the macro *introducing* a name — it is the macro *referring* to a free name that the caller has rebound. `gensym` gives fresh names for the macro's own bindings and does nothing about its references.

**What would fix it:** hygiene in the other direction — resolving a macro's free identifiers **in the macro's definition environment** rather than the use site. Scheme's `syntax-rules`/`syntax-case` track that by attaching the definition environment to each piece of syntax; Racket calls the result a *syntax object*.

*Full marks require distinguishing the two directions. Most answers will get the demonstration and stop; the second half is the mark.*

---

## Part B — The Circuit DSL (40)

**B1.** *(8)* Ripple-carry adder from four full adders.

**Gate count is not 4 × 5 = 20** — a full adder is 5 gates but the four instances share nothing with each other, so 20 is right *if* built independently. **The interesting answer is that it depends on how they built it**: reusing one `Node` graph across bit positions is wrong (the bits differ), so 20 is expected. Credit any student who explains *why* sharing does not apply here — that is the tree/DAG distinction used correctly in the negative direction.

*If a student reports fewer than 20 and cannot explain it, they have accidentally shared nodes between bit positions and their adder is wrong. Check the truth table.*

**B2.** *(8)* Module syntax; any reasonable design. **The marked half is the honest comparison of error messages** against `parser.py`'s `line N col M: expected X, found Y`. Expect: no line numbers, position at the start of the expression. Closing the gap needs position tracking through the parser plus a commit combinator — which is C2.

**B3.** *(10 — the hardest part)*

**What breaks:** `evaluate` recurses through `inputs` and terminates because the circuit is a **DAG**. Feedback makes it a cyclic graph, so the recursion does not terminate — the memo turns an infinite recursion into a wrong answer or a `RecursionError` depending on where the cycle closes.

**The replacement** is a two-phase update over time: hold each register's current value, evaluate all combinational logic from `(inputs + register outputs)`, then commit all register inputs simultaneously at the clock edge. **Simultaneity is the point** — updating registers one at a time gives a shift-register bug that looks almost right.

A 4-bit counter should show 0,1,2,…,9 over ten cycles.

**B4.** *(8)* Constant folding and CSE. **The verification is the mark**: an optimised circuit must be checked against the original exhaustively for small input counts. For 40 inputs, exhaustive is 2⁴⁰ — the answer is random testing plus, ideally, a **SAT check of the miter circuit** (XOR the two outputs and ask whether it can ever be 1). Credit anyone who reaches equivalence checking; it is the professional answer and it is Week 8's Curry-Howard idea in industrial form.

**B5.** *(6)* Removing the memo makes `evaluate` **exponential in circuit depth** on a shared graph — each node re-evaluates all its inputs, and a diamond doubles the work per level. With the memo it is **linear in the number of gates**. Require an actual measurement showing the blow-up.

---

## Part C — Parser Combinators (24)

**C1.** *(6)* `RecursionError`. **The rule:** a top-down parser cannot handle a grammar where a non-terminal can derive itself as its own leftmost symbol without consuming input.

The rewrite is `NUMBER ('+' NUMBER)*` folded left — **and the fold is why it is still left-associative**, which is the third bullet and the one students skip.

**C2.** *(8)* Position tracking plus a `commit`/`cut`. Expect real but partial improvement: `(1 + 2` reporting a missing `)` at the right column is achievable; matching `expected PUNCT ')', found PUNCT ';'` exactly needs the parser to know token *kinds*, which this one does not have.

**Full marks require the honest assessment at the end.** A student claiming parity with the hand-written parser has almost certainly not tested the cases where alternation nests.

**C3.** *(6)* Any two combinators, correctly implemented, with the grammar rewritten and tests still passing.

**C4.** *(4)* A function taking a precedence table and returning a parser:

```python
def expression(atom, levels):
    p = atom
    for ops in levels:
        p = chainl1(p, alt(*[lit(o) for o in ops]))
    return p
```

**What it is that Week 2's parser could not be: a *value* computed at run time.** A hand-written parser's precedence is fixed in the shape of its call graph; this one is data, so a language could read its operator table from a config file — which is what Haskell's `infixl` declarations and Prolog's `op/3` actually do.

---

## Part D — Written (16)

**D1.** *(6)* Any coherent choice. **The deciding factor must not be elegance** — acceptable answers are: who writes the config (non-programmers → external), how many tools consume it (many → external), and how much tooling budget exists (little → internal).

Real examples: **Bazel/Buck chose internal** (Starlark, a Python subset) and pay for it in a language that looks like Python and is not, confusing everyone. **Make chose external** and pays for it in tab-significant syntax and famously poor diagnostics. **CMake chose external** and pays for it continuously. Accept any with a stated cost.

**D2.** *(5)* The reason is **error messages** — L22 §5's table, and users interact with diagnostics far more than with grammars.

**Both conclusions are defensible.** For hand-writing: diagnostics are the product for a compiler. Against: the combinator version can be given good errors with commit points, and 4 lines against 357 is an enormous maintenance difference.

Combinators without hesitation: **a config file parser, a log format, a one-off data import, an internal tool** — anywhere the input is machine-generated or the user is you.

**D3.** *(5)* All five are **working around the absence of homoiconicity** — the source is not already a data structure of the language, so each bolts on a second representation.

**Hygienic: Rust's `macro_rules!` and (by design) `syntax-rules`** in Scheme. Of the five listed, `macro_rules!` is the hygienic one; proc-macros are hygiene-capable but let you opt out. Hygiene means macro-introduced names cannot collide with the caller's.

**C++ templates:** Turing-completeness was **discovered, not designed** (Veldhuizen, 1994), and the practical consequence is that template metaprogramming errors are the output of an *unintended interpreter* — pages of instantiation traces. The retrofit is **`constexpr`** (C++11) and **`consteval`** (C++20): ordinary code, run at compile time, with ordinary error messages.

---

## Overall

**Expected distribution:** A and C should be high. **B3 and B4 are where the marks separate**, and both will be thin in a week when Project 1 is due — which is expected and is why the drop exists.

**Two failure modes:**

1. **B4 without a verification step.** An optimisation asserted, not checked. This is precisely Weeks 4–5's lesson and should be marked accordingly.
2. **C2 claiming parity with the hand-written parser.** Ask for the nested-alternation cases.

---

*CS 211 · Week 10 · PS 10 Solutions · © CSE Department*
