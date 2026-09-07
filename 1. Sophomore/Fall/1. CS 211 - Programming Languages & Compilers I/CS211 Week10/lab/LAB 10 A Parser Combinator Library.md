# CS 211 · Lab 10
## A Parser Combinator Library

**Friday of Week 10 · 14:00–15:50 · BH 220 · covers Week 10**
**Unmarked and mandatory.** The TA checks you off in the session. [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second unexcused absence.

**Bring:** a terminal. Everything is in this folder.

> **Project 1 is due next Friday, and so is PS 10.** If your compiler is not yet running under
> `--gc=none`, say so to the TA at the start of this session — that is a better use of the two
> hours than anything below, and nobody will mind.

---

## Setup

```bash
cd "CS211 Week10/lab"
python3 demo.py | head -8
python3 combinators.py | head -6
python3 circuit.py | head -4
```

---

## Part A — Macros (30 min)

**Q1.** Start the REPL and convince yourself that code is data:

```bash
python3 lisp.py -
```

```lisp
(quote (if a b c))
(car (quote (if a b c)))
(cdr (quote (+ 1 2)))
(cons (quote *) (cdr (quote (+ 2 3))))
```

**The last one built a program.** Say in one sentence what homoiconicity means, using that example.

**Q2.** Now the week's result:

```bash
python3 demo.py | sed -n '/2\. a function/,/way out/p'
```

- Report the four lines.
- **Why did the function version raise and the macro version not?** Your answer must say *when* each one's arguments were evaluated.
- Find the section of Week 7 that predicted this. *(It is the one where `Z factgen` still diverged.)*

**Q3.** Write your own macro. In the REPL:

```lisp
(defmacro my-unless (test body) `(if ,test nil ,body))
(my-unless #f 42)
(my-unless #t (boom))
```

Then write `my-and` so that `(my-and #f (boom))` returns `#f` without raising. **Check that a function version cannot.**

**Q4.** Watch expansion happen:

```lisp
(defmacro twice (e) `(begin ,e ,e))
```

- Predict what `(twice (print 1))` prints, then run it.
- Now predict `(twice (boom))`.
- **A macro can evaluate its argument more than once.** Write a macro where that is a bug, and say what a careful macro writer does about it. *(Hint: bind it to a `gensym`'d name first.)*

**Q5.** The capture bug:

```bash
python3 demo.py | sed -n '/5\. variable capture/,$p'
```

- Report `(swap-bad tmp z)` and its expansion.
- **Which two `tmp`s collided?**
- Name the Week 7 section this is, and the function there that `gensym` corresponds to.

---

## Part B — Parser Combinators (35 min)

**Q6.** Run it and read the top:

```bash
python3 combinators.py
```

- `expr` prints as an object. **What is it, and what was Week 2's `expr`?**
- Find the four lines in the source that are the grammar. Write out the three productions they correspond to.

**Q7.** Associativity:

```
10 - 2 - 3  parses as  ('-', ('-', 10, 2), 3)
```

- Which associativity is that, and which is correct for `-`?
- Find `_fold`. **Change it to fold right instead**, re-run, and report what `10 - 2 - 3` now evaluates to.
- **You changed associativity without touching a production.** Say why that is not possible in a hand-written recursive-descent parser.

**Q8.** The trap:

```bash
python3 combinators.py | sed -n '/left recursion/,/reified/p'
```

- Report what happens.
- **Write the rule out** and say exactly why it never terminates.
- This is a Week 2 problem. Name Week 2's fix, and confirm the shipped `expr` uses it.

**Q9.** Now the part that is usually left out of the tutorial. Compare error messages:

```bash
python3 -c "
from combinators import expr
for s in ['1 +', '(1 + 2', '1 + + 2', '1 2']:
    try: expr.parse(s)
    except SyntaxError as e: print(f'  {s:<12} {e}')
"
```

against the hand-written parser:

```bash
cd ../../"CS211 Week6"/lab
echo 'fn f() -> int { return (1 + 2; }' > /tmp/e.cy
python3 tac.py /tmp/e.cy f 2>&1 | grep error:
cd -
```

- Put the two side by side.
- **Which one would you rather get?** Say what the combinator version is missing.
- Explain the *structural* reason — think about what `a | b` has to throw away when `a` fails.

**Q10.** Extend the library. Implement **`chainl1(p, op)`**: parse `p` separated by `op`, folding left-associatively. Then rewrite `term` and `expr` using it and check the tests still pass.

---

## Part C — The Circuit DSL (25 min)

**Q11.** Run it:

```bash
python3 circuit.py
```

- Report the full adder's truth table and confirm it is correct.
- The internal DSL is **five methods**. Find them.
- The gate count is **5**. Work out by hand why it is not 6.

**Q12.** Build something with the internal DSL. In a Python file or the REPL:

```python
from circuit import inputs, show_table, gate_count
a, b = inputs("a b")
# a 2-to-1 mux with select s, then a half adder, then...
```

Build a **2-bit equality comparator** — output 1 when both bits match — and show its truth table.

**Q13.** Now the external one. Write your comparator as a netlist and check it agrees:

```python
from circuit import parse_netlist, show_table
net = parse_netlist("""
  in a0 a1 b0 b1
  ...
""")
```

- **Which of the two was more pleasant to write?** Which would you hand to a hardware engineer?
- Break your netlist deliberately — an undefined wire — and report the error message.

**Q14.** *(Discussion — out loud with your neighbour.)*

You are asked to build a DSL for your team.

- What is the deciding question between internal and external? **It is not elegance.**
- Name a real external DSL you have used, and one thing about its tooling that annoyed you.
- L22 §7's test: *is this read by more than one consumer, or by non-programmers?* Apply it to something you have actually built.

---

## If You Finish Early

**Q15.** Write a Lisp macro `time` that evaluates its body and reports how long it took. **This cannot be a function.** Say why in one sentence.

**Q16.** Add `let` to the Lisp as a macro: `(let ((x 1) (y 2)) body)` expanding to `((lambda (x y) body) 1 2)`. Test it, then check whether it is hygienic — what happens if the body refers to a variable called `lambda`?

**Q17.** In `combinators.py`, add a `commit` combinator that prevents backtracking past a point. Use it in `atom` after `lit('(')` so that `(1 + 2` reports a missing `)` at the right place.

**Q18.** Add constant folding to `circuit.py`: `and(x, 0)` → `0`, `xor(x, x)` → `0`. **Verify the truth table is unchanged.** *(This is PS 10 B4 — starting it here is encouraged.)*

---

## Before You Leave

Show the TA:

1. Your Q2 answer — the four lines, and *when* each version's arguments were evaluated.
2. Your Q5 answer — which two `tmp`s collided.
3. Your Q7 right-folding result, and why a hand-written parser could not do that so easily.
4. Your Q9 side-by-side error comparison, with the structural reason.

---

*CS 211 · Week 10 · Lab 10 · © CSE Department*
