# CS 211 · Lab 7
## Encoding Data in Pure Lambda Calculus

**Friday of Week 7 · 14:00–15:50 · BH 220 · covers Week 7**
**Unmarked and mandatory.** The TA checks you off in the session. `COURSE POLICIES.md` costs you a letter grade after a second unexcused absence.

**Bring:** a terminal. Everything is in this folder.

> **Lab 7 covers Week 7.** Both lectures have already happened. Part C assumes you know what a
> fixed-point combinator is.
>
> **Midterm 2 is on Tuesday of Week 8 and covers Weeks 4–7.** This lab is the last scheduled
> contact before it.

---

## Setup

```bash
cd "CS211 Week7/lab"
python3 lam.py '(\x. x) y'         # should print `y` in 1 beta-reduction
python3 church.py | tail -3        # should end with 24/24 passed
```

If either fails, get the TA now rather than at 15:30.

---

## Part A — Reading Terms (20 min)

**Q1.** Without running anything, write down the normal form of each:

```
(\x. x) (\y. y)
(\x y. x) a b
(\x y. y) a b
(\f. f (f a)) (\x. x)
(\x. x x) (\x. x)
```

Then check with `python3 lam.py '...'`. **Report any you got wrong and why.**

**Q2.** These two differ by one pair of parentheses:

```bash
python3 lam.py '\x. f x'
python3 lam.py '(\x. f) x'
```

Explain the difference in terms of the two grammar conventions from L15 §2. **Which convention does each one exercise?**

**Q3.** Run the capture demonstration:

```bash
python3 lam.py '(\x y. x) y'
python3 lam.py '(\x y. x) y' --naive
```

- Write down both results.
- **In one sentence each, say what function each result is.** Not what it looks like — what it does when applied to an argument.
- Apply both to a fresh variable `z` and confirm your answer:
  ```bash
  python3 lam.py '((\x y. x) y) z'
  python3 lam.py '((\x y. x) y) z' --naive
  ```

**Q4.** Watch a reduction happen:

```bash
python3 lam.py --defs prelude.lam 'mult two three' --trace
```

- How many steps?
- **Find the step where the term is largest.** Terms do not shrink monotonically; say what got bigger and why.

---

## Part B — Building Data (35 min)

**Q5.** Church numerals are for-loops. Confirm:

```bash
python3 lam.py --defs prelude.lam --church 'three'
python3 lam.py --defs prelude.lam --church 'succ three'
python3 lam.py --defs prelude.lam --church 'add two three'
python3 lam.py --defs prelude.lam --church 'mult three four'
```

Record the beta counts. Then **predict** the count for `mult four three` before running it, and run it.

`mult three four` and `mult four three` both give 12. **They do not cost the same.** Report both counts, and explain the difference from the definition `mult = λm n f. m (n f)` — which argument's magnitude drives the cost, and why?

**Q6.** Now the expensive one:

```bash
python3 lam.py --defs prelude.lam --church 'pred three'
python3 lam.py --defs prelude.lam --church 'pred five'
```

- `pred three` costs **36** beta-reductions and `mult three four` costs **9**.
- **Explain why subtracting one is four times harder than multiplying**, using the definition of `pred` in `prelude.lam`.
- Draw the sequence of pairs the reduction walks through for `pred three`.

**Q7.** Booleans:

```bash
python3 lam.py --defs prelude.lam --church 'and true false'
python3 lam.py --defs prelude.lam --church 'if true one zero'
python3 lam.py --defs prelude.lam --church 'if false one zero'
```

`if = λp a b. p a b` does nothing at all. **Say what is actually doing the choosing**, in one sentence.

**Q8.** Now the result the week turns on:

```bash
python3 church.py | head -8
```

- `zero`, `false` and `nil` are the **same term**. Confirm it.
- Write down what `λf x. x` means. Then write down what else it means. Then a third thing.
- **A function returns `λf x. x`. What has it returned?** Answer honestly.

**Q9.** Find the rest of them. Write four lines of Python:

```python
from lam import load, alpha_eq, show
from itertools import combinations
e = load('prelude.lam')
for a, b in combinations(sorted(e), 2):
    if alpha_eq(e[a], e[b]):
        print(f"{a:<9} == {b:<9}  {show(e[a])}")
```

- There are **seven** pairs. List them.
- **`compose == mult`.** Sit with that one for a moment. Is it a coincidence?
- **`const == true`.** Same question.
- Sort the seven into *theorems* (any correct encoding would have them) and *collisions* (an accident of this encoding). **The split is not even.** *(This is PS 7 C3 — starting it here is encouraged.)*

**Q10.** Pairs and lists:

```bash
python3 lam.py --defs prelude.lam --church 'fst (pair one two)'
python3 lam.py --defs prelude.lam --church 'sum (cons one (cons two (cons three nil)))'
python3 lam.py --defs prelude.lam --church 'length (cons one (cons two nil))'
```

`fst = λp. p (λa b. a)`. That inner term is `true` under another name. **Explain why selecting from a pair and choosing between branches are the same operation.**

---

## Part C — Recursion (35 min)

**Q11.** Nothing in this language has a name, so nothing can call itself. Run factorial anyway:

```bash
python3 lam.py --defs prelude.lam --church 'fact three'
```

- Report the beta count.
- Look at `factgen` in `prelude.lam`. **It is not factorial.** Say what it is.
- `Y g` reduces to `g (Y g)`. Verify by hand: reduce `Y g` one step and write down what you get.

**Q12.** Now break it:

```bash
python3 lam.py --defs prelude.lam '(Y factgen) three' --strategy cbv --max-size 5000
```

- It diverges after **44 steps**. Why does call-by-value never reach `factgen`'s base case?
- Which subterm is being evaluated over and over?

**Q13.** Try the standard repair:

```bash
python3 lam.py --defs prelude.lam '(Z factgen) three' --strategy cbv --max-size 5000
```

- Still diverges — but after **3911** steps rather than 44. **Something improved. What?**
- And something did not. `factgen` uses `if`, which is an ordinary function. **Under call-by-value, how many of `if`'s three arguments get evaluated?**
- Say why no choice of fixed-point combinator could fix this.

**Q14.** The actual fix:

```bash
python3 lam.py --defs prelude.lam --church 'factV three' --strategy cbv
```

- Compare `factgenV` with `factgen` in `prelude.lam`. **What is different?**
- The output says the result is a *value*, and that turning it into a numeral took 64 further reductions. **What is a value, and why is printing a computation?**
- State the rule this establishes about `if` in strict languages. It should be one sentence and should not mention lambda calculus.

**Q15.** `Z` is `Y` with something added:

```bash
python3 -c "
from lam import load, eta_reduce, show, alpha_eq
e = load('prelude.lam')
print('Y      =', show(e['Y']))
print('Z      =', show(e['Z']))
print('eta(Z) =', show(eta_reduce(e['Z'])))
print('same?  ', alpha_eq(eta_reduce(e['Z']), e['Y']))
"
```

**Z eta-reduces to Y.** Two terms that are the same function, one of which terminates. Explain, in one sentence, what "the same function" is a claim about — such that this is not a contradiction.

**Q16.** All of it, in a language you use:

```bash
python3 strict.py
```

- `False and bottom()` returns `False`. `and_fn(False, bottom())` crashes. **Same logic.** What is the difference?
- `Y(factgen)` raises before it is ever applied to a number. Match this against Q12.
- `Z(factgen)(5)` is 120, with **no function referring to itself by name**. Find the line that does the work.

---

## If You Finish Early

**Q17.** Encode subtraction that saturates at zero (it already does — `pred zero` is `zero`). Now encode a **signed** integer as a pair of numerals `(positive, negative)`, and define addition and negation on it. What is the normalisation problem, and how would you fix it?

**Q18.** Run `python3 debruijn.py`. The beta counts for named and nameless reduction are **identical** and the per-step cost is 5–74× higher. Explain both halves.

**Q19.** Write a term that reduces to itself in **two** steps rather than one, so it cycles without growing. *(`omega` does it in one.)*

**Q20.** Measure the rename rate — renames per beta-reduction — across the prelude's arithmetic. **Every term with a nonzero rate is an `exp`**; `exp three three` is the worst at 0.46, and `mult`, `add`, `pred` and `sub` are all exactly zero.

**Why does exponentiation force renaming when nothing else does?** Look at what `exp = λm n. n m` does with its arguments that no other definition does.

---

## Before You Leave

Show the TA:

1. Your Q3 answer — both results, and what each function *does*.
2. Your Q8 answer — what `λf x. x` has returned.
3. Your Q9 list of seven pairs, sorted into theorems and collisions.
4. Your Q12–Q14 sequence: 44 steps, 3911 steps, and what finally worked.

---

*CS 211 · Week 7 · Lab 7 · © CSE Department*
