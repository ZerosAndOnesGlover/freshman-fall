# CS 211 · Reading Guide · Week 10
## Domain-Specific Languages and Metaprogramming

**Budget your week around Project 1, not around this guide.** Project 1 and PS 10 are both due Friday of Week 11. If you read one thing this week, make it Bentley — it is four pages and it frames everything else.

---

## Before Tuesday (L21 — macros and homoiconicity)

| Source | Section | Why | Pages |
|---|---|---|---|
| **SICP** | **§4.1.1–4.1.2** | The metacircular evaluator: `eval` and `apply` in a page. **`lisp.py` is this**, and reading them together is the fastest route in. Free at mitpress.mit.edu. | 10 |
| **Graham**, *On Lisp* | **ch. 7** | "Macros." The clearest account of what a macro is and when to reach for one. | 12 |
| **Graham**, *On Lisp* | **ch. 9** | "Variable Capture." Names the failure modes and the standard fixes. **§9.2 is `swap-bad`.** | 10 |

**Skip for now:** anything on `syntax-case`. Hygiene as a *mechanism* is a rabbit hole; hygiene as a *property* is one paragraph in L21 §7 and that is enough this week.

---

## Before Thursday (L22 — DSLs and combinators)

| Source | Section | Why | Pages |
|---|---|---|---|
| **Bentley (1986)** | all | "Little Languages," *CACM* Programming Pearls. **Four pages, and it is the whole argument.** Written before the term "DSL" existed. | 4 |
| **Fowler**, *DSLs* | **ch. 1–4** | The internal/external distinction, done properly, with the trade-offs named. Skim ch. 2's examples. | 30 |
| **Hutton (1992)** | §1–3 | "Higher-Order Functions for Parsing." Where combinators come from; `seq`, `alt` and `many` in their original form. | 10 |
| **Dragon** | **§4.4** (revisit) | Top-down parsing and left recursion — **the reason `bad_expr` fails is here, from Week 2**, unchanged. | 6 |

---

## Papers, If You Want Them

- **Kohlbecker, Friedman, Felleisen & Duba (1986)**, "Hygienic Macro Expansion." The paper that made automatic renaming rigorous.
- **Wadler (1985)**, "How to Replace Failure by a List of Successes." The list-of-successes idea behind backtracking combinators.
- **Ford (2004)**, "Parsing Expression Grammars." PEGs and packrat parsing — what you get if you take combinators seriously and add memoisation.
- **Steele & Sussman (1978)**, "The Art of the Interpreter." Long, and the best thing ever written about why `eval` looks the way it does.

---

## Documentation

- **`doc.rust-lang.org/reference/macros-by-example.html`** — `macro_rules!`, and its hygiene rules stated explicitly. Read this beside L21 §7.
- **`docs.python.org/3/reference/datamodel.html#special-method-names`** — the operator methods that make an internal DSL possible in Python. `circuit.py` uses four of them.
- **The Protocol Buffers language guide** — an external DSL with many consumers, which is L22 §7's test passing.

---

## The One Thing Worth Reading Twice

**Graham, *On Lisp* §9.2, on capture.**

Read it, then run:

```bash
python3 demo.py | sed -n '/5\. variable capture/,$p'
```

`(swap-bad tmp z)` returns `(7 7)` where `(7 100)` was wanted, and the expansion shows `(define tmp tmp)`.

Graham catalogues the ways a macro can capture a caller's name. **What he does not dwell on is that you have already seen this exact failure** — Week 7 §5 measured `(λx y. x) y` producing the identity function instead of a constant function, one beta-step apart, with nothing raised. Same bug, same fix, two settings five weeks apart.

**Noticing that `gensym` and Week 7's `fresh` are the same function is the point of reading both.**

---

## A Note on What This Week Is Really Arguing

The syllabus lists mechanisms — macros, homoiconicity, reflection, ANTLR, protocol buffers, parser combinators — and it would be easy to read the week as a tour.

**It is an argument about cost, and the direction is not the one the tutorials take.**

Nearly every technique here trades *expressive power at the source level* for *quality of diagnosis when something goes wrong*. Macros make the core small and delete the thing the programmer wrote before anything fails. Internal DSLs are free and permanently limited. External DSLs say exactly what you mean and hand you the entire tooling bill. Parser combinators shrink a grammar from 357 lines to 4 and turn `line 1 col 30: expected ')'` into `at '(1 + 2'`.

**None of that is a reason not to use them.** It is a reason to know what you are buying — and to notice that the industrial compilers whose teams understand this material best all hand-write their parsers anyway.

The question L22 §7 ends on is the useful one: *is this description read by more than one consumer, or by people who are not programmers?* **If neither, a library of ordinary functions will serve better and cost far less, and it comes with a debugger.**

---

*CS 211 · Week 10 · Reading Guide · © CSE Department*
