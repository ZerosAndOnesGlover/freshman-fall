# CS 211 · Problem Set 10
## A Circuit DSL and Its Simulator

---

**Released:** Week 10, Wednesday · **Due:** Week 11, Friday 17:00
**100 points · counts toward the Problem Sets component (30% of the final grade)**

**Submit:** `circuit.py`, `combinators.py`, `lisp.py` (your versions, runnable end to end) and `ps10.md` (written answers, tables, traces).

> ## ⚠ This is due the same day as Project 1.
>
> **Friday of Week 11, 17:00 — both of them.** Project 1 is worth 12.5% of the course and this
> problem set is worth roughly 2.3%. **If you have to choose, choose the project**, and take the
> dropped-problem-set allowance on this one: the Problem Sets component drops your lowest mark.
>
> That allowance exists for weeks exactly like this one. **Plan for it now rather than discovering
> it at 16:00 on the 21st.** Parts A and D are the cheapest marks here if you want partial credit.

---

## Part A — Macros (20 points)

**A1.** *(5)* Run `python3 demo.py` and report demonstrations 2 and 5.

- Give the four results from the `unless-fn` / `unless-mac` comparison.
- **State in one sentence why the function version raised** — your answer must refer to *when* arguments are evaluated.
- Connect it to Week 7: name the section and the term that diverged for the same reason.

**A2.** *(5)* Write three macros that cannot be functions in a strict language, and demonstrate each:

- `my-and` — short-circuiting conjunction, variadic.
- `my-or` — short-circuiting disjunction, variadic.
- `cond` — a multi-way conditional, `(cond (test1 body1) (test2 body2) (else body))`.

For each, show a call where the function version would evaluate something it must not, using `boom`.

**A3.** *(5)* Reproduce the capture bug in `swap-bad`, then:

- Show the expansion, and say exactly which two `tmp`s collided.
- **Write a *different* capturing macro** — not a swap — where the capture produces a wrong answer rather than an error. Show the expansion and the wrong result.
- Fix yours with `gensym` and show the corrected expansion.

**A4.** *(5)* `lisp.py`'s macros are **unhygienic**.

- A macro can also capture in the *other* direction: it can refer to a name the *caller* has shadowed. Construct such a case — a macro whose body uses `+`, called in a scope where the caller has rebound `+` — and show what happens.
- **`gensym` does not fix this one.** Say why, and name what would. *(Scheme's `syntax-rules` handles both directions; find out what it tracks.)*

---

## Part B — The Circuit DSL (40 points)

`circuit.py` gives you an internal DSL (operator overloading), an external DSL (a netlist parser), a levelised simulator, and a full adder that works in both.

**B1.** *(8)* **Extend the internal DSL.**

- Add `nand`, `nor` and `mux` as functions over `Node`.
- Build a **4-bit ripple-carry adder** from your full adder. Report the gate count and verify at least six input pairs against Python's arithmetic.
- Report `gate_count` for the 4-bit adder. **Explain why it is not four times the full adder's five.**

**B2.** *(8)* **Extend the external DSL.**

- Add syntax for a *module*: a named, reusable sub-circuit with inputs and outputs, instantiable by name.
- Rewrite the 4-bit adder as a netlist using your module syntax.
- Report the error message your parser gives for three malformed netlists: an undefined wire, an arity mismatch, and a syntax error. **Then say honestly how good those messages are** compared with Week 2's `parser.py`, and what it would take to close the gap.

**B3.** *(10)* **Sequential logic.**

The simulator assumes a **DAG**. A latch does not have one — its output feeds back to its input.

- Add a `reg` (D flip-flop) primitive: it holds a value and updates on a clock edge.
- Change the simulator to evaluate a circuit **over time**: given inputs per cycle, produce outputs per cycle.
- Build a 4-bit counter and show ten cycles.
- **Say precisely what broke in the old evaluator** when you introduced feedback, and what you replaced it with.

**B4.** *(8)* **Optimise a circuit.**

You have a representation and a simulator, so you have a compiler.

- Implement **constant folding**: `and(x, 0)` → `0`, `or(x, 1)` → `1`, `xor(x, x)` → `0`, and so on.
- Implement **common subexpression elimination** so that structurally identical gates become one node.
- Report gate counts before and after for at least three circuits, one of which should improve substantially.
- **Verify the optimised circuit has the same truth table as the original** — exhaustively for small circuits. Say what you would do if it had 40 inputs.

**B5.** *(6)* **A measurement.**

- Time the simulator on a circuit with at least 16 inputs. Report the cost of a full truth table.
- The memo in `evaluate` matters. **Remove it** and re-measure on a deep circuit with sharing. Report the difference and explain it.
- What is the complexity of `evaluate` with and without the memo, in terms of circuit depth?

---

## Part C — Parser Combinators (24 points)

**C1.** *(6)* Reproduce the left-recursion failure in `combinators.py` and report it.

- **State the general rule** about which grammars a top-down parser cannot handle.
- Rewrite `bad_expr` so that it parses the same *language* and terminates. Show that it does.
- Explain why your rewrite still produces **left-associative** trees.

**C2.** *(8)* **Improve the error messages.**

`combinators.py` reports `expected number or ')' at '(1 + 2'` where Week 2's parser reports `line 1 col 30: expected PUNCT ')', found PUNCT ';'`.

- Track **line and column** through the parser and report them.
- Implement a **`commit`** (or `cut`) combinator: once a branch has consumed a distinguishing token, do not backtrack past it, and report the failure from inside that branch.
- Re-run the four failing inputs and report the new messages.
- **How close did you get to the hand-written parser?** Be honest, and say what remains.

**C3.** *(6)* **Build a combinator that is not in the file.**

Choose two of: `chainl1` (left-associative binary operators, folding built in), `between(open, p, close)`, `optional(p)`, `not_followed_by(p)`, or `sep_end_by`. Implement them, and rewrite part of the arithmetic grammar using them so it is shorter.

**C4.** *(4)* Combinators build the grammar at run time.

- Write a function that takes a **list of operator precedence levels** and *generates* the corresponding expression grammar.
- Use it to build a parser for an expression language with four precedence levels, and demonstrate it.
- **Say what this is that Week 2's parser could not be.** One sentence.

---

## Part D — Written (16 points)

**D1.** *(6)* You are asked to design a configuration language for a build system.

- Give one argument for an internal DSL and one for an external DSL, specific to this case.
- **Say which you would choose and why.** Name the deciding factor, and it should not be elegance.
- Name a real build system that made each choice, and say what it cost them.

**D2.** *(5)* L22 §5 claims clang, rustc and GHC all hand-write their parsers despite knowing what combinators are.

- Give the reason.
- **Is it a good reason?** Argue either way, engaging with the measured trade — 4 lines against 357, and the error messages in the table.
- Name one class of tool where you would use combinators without hesitation.

**D3.** *(5)* Macro systems keep being reinvented: the C preprocessor, C++ templates, Java annotation processors, Rust proc-macros, Go generate.

- Say what all of them are working around, in one sentence.
- Two of those five are **hygienic**. Name them and say what hygiene means.
- C++ templates are Turing-complete *by accident*. Say what practical consequence that had, and name the feature added later to fix it.

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14.2).

| Measurement | Value |
| --- | --- |
| `(unless-fn #t (boom))` | **ERROR: boom was evaluated** |
| `(unless-mac #t (boom))` | `nil` |
| `while` macro, `(< i 5)` summing | total = **10** |
| `(unless-mac #t (boom))` expands to | `(if #t nil (boom))` |
| `(swap-bad tmp z)` | **`(7 7)`**, expected `(7 100)` |
| its expansion | `(begin (define tmp tmp) (set! tmp z) (set! z tmp))` |
| `(swap tmp z)` with `gensym` | `(7 100)` |
| full adder, internal DSL | 5 gates (2 xor, 2 and, 1 or) |
| internal and external truth tables | **identical** |
| `combinators.py` arithmetic grammar | **4 lines** |
| Week 2/6 `parser.py` | 357 non-comment lines |
| `10 - 2 - 3` parses as | `('-', ('-', 10, 2), 3)` |
| left-recursive `bad_expr` | **RecursionError** |
| combinator error, `(1 + 2` | `expected number or ')' at '(1 + 2'` |
| hand-written error, same shape | `line 1 col 30: expected PUNCT ')', found PUNCT ';'` |

---

## A Note on Scope

**This problem set is larger than it needs to be, deliberately**, so that you can choose where to spend the time you have.

If you are short — and in the week Project 1 is due, you will be — **A1, A3, C1 and D1 are the cheapest complete answers**, and B3 and B4 are the most expensive. A submission consisting of Parts A, C and D, done properly, with a note saying you prioritised the project, is a perfectly respectable outcome and will not be marked down for the missing part beyond the marks themselves.

**What will be marked down is a Part B that claims a working sequential simulator without a ten-cycle trace**, or a B4 that claims an optimisation without a truth-table check. As every week: a careful partial result beats a confident claim.

---

*CS 211 · Week 10 · Problem Set 10 · © CSE Department*
