# CS 211 · Lab 10 — Solutions
## Instructor Only

**Do not distribute.** All output verified against the Week 10 lab code on Python 3.14.2.

---

## Running the Lab

**Budget:** A 30, B 35, C 25 = 90 minutes against 110, leaving room for Q15–Q18.

**Say this at the start:** Project 1 and PS 10 are both due next Friday, and **anyone whose compiler is not running should spend this session on that instead.** Mean it — a student who fixes their code generator here is better served than one who writes a `chainl1`. Check them off either way.

**Three predictable stalls.**

**Q1 needs the REPL.** `python3 lisp.py -`. Some students will type into `demo.py` and get nothing.

**Q4's second half is the interesting one** and is easy to skip. `(twice (boom))` raises; the point is that a macro may evaluate its argument *more than once*, which is a distinct hazard from capture and is fixed the same way — bind to a `gensym` first.

**Q9 is where the lab lands.** Do not let them rush it. The intended reaction to the two error messages side by side is discomfort, and the follow-up — *why do clang and rustc hand-write their parsers?* — should come from the room.

---

## Part A — Macros

**Q1.** `(quote (if a b c))` → `(if a b c)`; `(car ...)` → `if`; `(cdr '(+ 1 2))` → `(1 2)`; `(cons '* (cdr '(+ 2 3)))` → `(* 2 3)`.

**Homoiconicity:** a program in the language *is* a data structure of the language, so `cons` and `cdr` — ordinary list operations — build and take apart programs.

**Q2.**

```
  (unless-fn #t (boom))   => ERROR: boom was evaluated
  (unless-mac #t (boom))  => nil
  (unless-fn #f 42)       => 42
  (unless-mac #f 42)      => 42
```

**A function's arguments are evaluated before it is entered**, so `(boom)` ran before `unless-fn` could decide it was not needed. A macro's arguments arrive **unevaluated**, as syntax.

The Week 7 section is **§10** — `(Z factgen) three` diverging under call-by-value after 3911 steps because `if` was a function and evaluated both branches.

**Q3.** `(defmacro my-and (a b) `(if ,a ,b #f))` — accept any correct shape.

A function version cannot short-circuit: `(and-fn #f (boom))` evaluates `(boom)` on the way in. *(Week 9's `strict.py` measured exactly this in Python: `False and bottom()` returns `False`, `and_fn(False, bottom())` raises.)*

**Q4.** `(twice (print 1))` prints `1` **twice**. `(twice (boom))` raises.

**The hazard is multiple evaluation**, distinct from capture: an argument with a side effect, or an expensive one, happens once per occurrence in the expansion. The fix is to bind it once:

```lisp
(defmacro twice (e)
  (define g (gensym))
  `(begin (define ,g ,e) ,g ,g))
```

*Credit any student who spots that this is why C macros are written `#define MAX(a,b) ((a)>(b)?(a):(b))` and still evaluate an argument twice.*

**Q5.** `(swap-bad tmp z)` → `(7 7)`, expected `(7 100)`. Expands to `(begin (define tmp tmp) (set! tmp z) (set! z tmp))`.

**The macro's `tmp` and the caller's `tmp`** collided — the macro's temporary shadowed the variable it was meant to be saving.

Week 7 **§5**, and `gensym` corresponds to **`fresh`** in `lam.py`'s `subst`.

---

## Part B — Parser Combinators

**Q6.** `expr` is a **`Parser` object** — a value, built at import time from `seq`, `alt` and `many`. Week 2's `expr` was a **function in a call graph**, which a program cannot inspect.

The four lines are `NUMBER`, `atom`, `term`, `expr`, corresponding to:

```
expr := term (('+'|'-') term)*
term := atom (('*'|'/') atom)*
atom := NUMBER | '(' expr ')'
```

**Q7.** `('-', ('-', 10, 2), 3)` is **left-associative**, which is correct for `-`.

Folding right instead makes `10 - 2 - 3` evaluate to **11** (10 − (2 − 3)), which is wrong for subtraction — and that is the point: **associativity is a property of the fold, not of the grammar.**

In a hand-written recursive-descent parser associativity is encoded in the *recursion structure* — a right-associative operator recurses on the right, a left-associative one loops — so changing it means restructuring the functions.

**Q8.** `RecursionError`.

`bad_expr := bad_expr '+' NUMBER | NUMBER` calls `bad_expr` as its **first action**, before consuming any input, so the recursion never reaches a base case and never terminates.

Week 2's fix: **eliminate the left recursion** — rewrite as `NUMBER ('+' NUMBER)*` and recover associativity in a fold. The shipped `expr` does exactly that.

**Q9.**

| input | hand-written | combinator |
|---|---|---|
| `(1 + 2` | `line 1 col 30: expected PUNCT ')', found PUNCT ';'` | `expected number or ')' at '(1 + 2'` |
| `1 +` | `line 1 col 28: unexpected ';'` | `trailing input at '+'` |

The combinator version has **no line, no column, and the wrong position** — it points at the start of the input.

**The structural reason:** `a | b` **backtracks**. When `a` fails, the alternation discards everything `a` learned — including how far it got — and tries `b` from the original position. When both fail, the only position it still has is the one it started from. Good errors require *committing* to a branch once a distinguishing token is seen, which is what `try`/`cut` does in every serious combinator library.

**Q10.** `chainl1`:

```python
def chainl1(p, op):
    return seq(p, many(seq(op, p))) >> _fold
```

`term = chainl1(atom, lit('*') | lit('/'))`, `expr = chainl1(term, lit('+') | lit('-'))`. All tests should still pass.

---

## Part C — The Circuit DSL

**Q11.** Truth table as printed; sum = a⊕b⊕cin and cout = majority(a,b,cin). Both correct.

The five methods are `__and__`, `__or__`, `__xor__`, `__invert__` on `Node`, plus `Node.__init__`.

**Gate count is 5, not 6, because `sum` and `cout` share `(xor a b)`** — one gate with two consumers. Counting it once per output gives 6 and is wrong.

**Q12.** Any correct comparator. `eq0 = ~(a0 ^ b0)`, `eq1 = ~(a1 ^ b1)`, `out = eq0 & eq1`. Truth table: 1 on the four matching rows.

**Q13.** Netlist form using `nand`/`nor`/`not` as named gates. **Most students find the netlist more pleasant to write and much clearer to hand over** — which is L22 §3's point.

Undefined wire gives `SyntaxError: undefined wire: <name>` — **no line number**, which is the same weakness as Q9 and worth naming again.

**Q14.** *(Discussion.)* The deciding question is **who reads it** — is the description consumed by more than one tool, or written by people who are not programmers? If neither, a library of ordinary functions costs far less and comes with a debugger.

---

## If You Finish Early

**Q15.** `(defmacro time (e) `(begin (define t0 (now)) ,e ...))` — accept any shape. **It cannot be a function** because a function receives the *value* of `e`, computed before the timer could start.

**Q16.** `let` as a macro is straightforward. It is **not hygienic here**: the expansion introduces a `lambda` binding, so a body referring to names the macro introduces can collide. Accept any demonstration.

**Q17.** A `commit` that raises rather than returning `Err` past a chosen point. Expect partial success — getting `(1 + 2` to report at the right place is achievable; getting full line/column tracking is PS 10 C2 and more work.

**Q18.** Constant folding with a truth-table check. **Insist on the check** — an optimisation asserted without verification is exactly what Weeks 4 and 5 were about.

---

*CS 211 · Week 10 · Lab 10 Solutions · © CSE Department*
