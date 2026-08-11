# CS 211 · Lab 0 · Solutions and Checkoff Notes
## Instructor Only

---

**Lab 0 is unmarked.** The TA checks the five parts off in the session. These notes exist so the checkoff is consistent and so the TA knows which failures are interesting and which are typos.

> **Every count below was produced by `lab/cfg_count.py`.** If a student's number disagrees, run
> theirs — the tool is the authority, and twice in a session the student will be right about
> something the notes did not anticipate.

---

## Part 1 — The Toolchain (20 min)

### Expected output

Every one of `python3 gcc flex bison ghc clang opt lli swipl java` must print a version.

**On BH 220 machines all ten are present.** On personal machines the usual failures, in order of frequency:

| Symptom | Cause | Fix |
|---|---|---|
| `opt`, `lli` missing but `clang` present | Ubuntu ships them versioned | Use `opt-18` / `lli-18`, or `sudo apt install llvm-18-tools`. **Note it — Week 4's commands need the suffix.** |
| `ghc` missing | Not pulled in by `clang` | `sudo apt install ghc` |
| `swipl` missing | `swi-prolog-nox` is the headless package | `sudo apt install swi-prolog-nox` |
| `sqlite3` missing | Rare; it is usually preinstalled | `sudo apt install sqlite3` |

**A student on macOS or WSL is fine** provided all ten report versions. Do not spend lab time on platform differences; send them to the Help Desk and let them do Parts 2–5, which need only `python3`.

### Q1 — Ranking the four paradigms

All four print `Ada, Grace`. *(Python 3.14.2 and SQLite 3.45.1 confirmed on the reference machine; the Prolog goal is the one line to re-check the first time a lab machine is reimaged.)*

**Expected ranking, most method supplied to least:**

1. **Imperative** — loop, mutable accumulator, iteration order, sort call. *Gives up:* nothing, which is the point; you control everything and are responsible for everything.
2. **Functional** — the transformation, but no loop and no accumulator. *Gives up:* control over evaluation order and intermediate storage.
3. **Logic** — facts and a rule; the search strategy is the engine's. *Gives up:* control over the search, which can make performance hard to predict.
4. **Declarative (SQL)** — the shape of the answer only. *Gives up:* everything about execution — scan versus index, join order, parallelism.

**Accept a swap of 2 and 3.** The argument for logic being *less* specified than functional is reasonable — a Prolog rule does not say how to search — and a student who defends that ordering has understood the question better than one who matched this list by luck.

**The mark of a good answer** is the *exchange* clause, not the ranking. "SQL gives up execution control" is worth more than a correct order with no reasons.

---

## Part 2 — Derivations by Hand (20 min)

Grammar: `E ::= E "+" T | T` · `T ::= T "*" F | F` · `F ::= n | "(" E ")"`. String: **`n * n + n`**.

### Q2 — Leftmost

```
E ⇒ E + T ⇒ T + T ⇒ T * F + T ⇒ F * F + T ⇒ n * F + T
  ⇒ n * n + T ⇒ n * n + F ⇒ n * n + n
```

### Q3 — Rightmost

```
E ⇒ E + T ⇒ E + F ⇒ E + n ⇒ T + n ⇒ T * F + n
  ⇒ T * n + n ⇒ F * n + n ⇒ n * n + n
```

**The common error** is writing the leftmost sequence with the lines reordered. Check each step actually expands the rightmost non-terminal — in the rightmost derivation, `E + T` becomes `E + F` *before* the left `E` is touched at all.

### Q4 — The parse tree

```
E
├── E
│   └── T
│       ├── T
│       │   └── F
│       │       └── n
│       ├── "*"
│       └── F
│           └── n
├── "+"
└── T
    └── F
        └── n
```

**13 nodes** — eight non-terminals (two `E`, three `T`, three `F`) and five terminals.

*Verified: this string has exactly one parse tree under the stratified grammar, and two under the ambiguous one.*

**Why both derivations give the same tree:** a derivation is a *linearisation* of the tree — a choice of the order in which to visit nodes while expanding. Leftmost and rightmost are two traversal orders of one structure. **The tree is the object; the derivation is a walk over it.**

Accept any phrasing that identifies the derivation as an ordering artefact.

### Q5 — The AST

```
Add
├── Mul
│   ├── n
│   └── n
└── n
```

**5 nodes**, down from 13. **Eight nodes discarded, 62%.**

**The point to make at checkoff:** the `E`/`T`/`F` ladder existed to *force* `Mul` beneath `Add`. Having done that, it is redundant — the tree shape now encodes the precedence, so the nodes that produced the shape can go. Students who describe the discarded nodes as "useless" have missed this; they were essential, and then they were finished.

---

## Part 3 — Watching Ambiguity Explode (20 min)

### Q6 — Catalan counts and ratios

| Operands | Trees |
|---:|---:|
| 3 | 2 |
| 6 | 42 |
| 9 | 1,430 |
| 12 | 58,786 |

Successive ratios: `2.0, 2.5, 2.8, 3.0, 3.14, 3.25, 3.33, 3.40, 3.45, 3.50`

**Approaching 4, but slowly** — at twelve operands it has only reached 3.5. The limit is 4 because $C_k \sim 4^k / (k^{1.5}\sqrt{\pi})$, and the $k^{1.5}$ term drags the ratio below 4 for small $k$. **Accept "it looks like it is heading to 4 but has not got there"** — that is the correct observation. A student who says "the ratio is 4" has not looked at the numbers.

### Q7 — Do the two grammars generate the same language?

**They do**, and no string distinguishes them. A correct answer names the *kind* of string that would have disproved it: **one accepted by one grammar and rejected by the other**, i.e. a count of 0 on one side and non-zero on the other.

**The important observation:** the five rejected strings are evidence, not proof. Proof requires an argument about the grammars, not a finite test suite. **A student who says "I tested twenty strings and found none, so they are equal" should be pushed** — that is induction from examples, and Q4 of PS 0 is built on exactly this trap.

### Q8 — Why `( n + n ) * n` has one tree even under the ambiguous grammar

The ambiguity in `E ::= E "+" E | E "*" E` comes from the parser being free to choose where the *top-level* operator sits. Parentheses remove that freedom: `( n + n )` can only be derived through `F ::= "(" E ")"`, which forces the addition into a subtree before the `*` is ever considered. **There is exactly one place the `*` can go.**

**Good phrasing to look for:** the parentheses are the programmer overriding the grammar's choice, so there is no choice left to be ambiguous about.

### Q9 — Three operators

**`n + n * n ^ n` has 5 parse trees.** *(Verified.)*

**Most students predict 4 or 6.** The right reasoning: with three binary operators and four operands the count is $C_3 = 5$ — the operators' identities are irrelevant, because the ambiguous grammar treats them all identically. **That is the insight worth drawing out:** adding a third operator did not add a third kind of ambiguity, it just added another operand position, and the count depends only on how many.

Check the student wrote a prediction *before* running. The point of the question is the surprise.

---

## Part 4 — Fixing an Ambiguous Grammar (25 min)

### Q10 — The ambiguous boolean grammar

```
t or f and t   -> 2
not t and f    -> 2
```

*(Verified.)* Both exceed 1, as required.

### Q11 / Q12 — Model answer

```python
BOOL_FIXED = {
    'B': [('B', 'or', 'C'), ('C',)],      # or  — lowest, left-assoc
    'C': [('C', 'and', 'N'), ('N',)],     # and — tighter, left-assoc
    'N': [('not', 'N'), ('P',)],          # not — tighter still, prefix
    'P': [('t',), ('f',), ('(', 'B', ')')],
}
```

**All sixteen checks pass** *(verified)*:

```
1  t                  1  not not t              0  t or
1  not t              1  ( t or f ) and t       0  or t
1  t or f             1  not ( t or f )         0  t t
1  t and f                                      0  not
1  t or f and t                                 0  ( t
1  not t and f                                  0  t and and f
1  t or f or t or f
```

**Accept any grammar passing all sixteen.** Variable names will differ. The structural requirements are: three levels in the order `or` < `and` < `not`, left recursion on the two binary levels, and a `P` level holding the atoms and the parenthesised form.

**Common failures at checkoff:**

| Symptom | Cause |
|---|---|
| `not not t` returns 0 | `N ::= "not" P` instead of `N ::= "not" N` — cannot nest |
| `( t or f ) and t` returns 0 | The parenthesised rule was put at the wrong level, or omitted |
| Everything returns 0 | Terminal spelled differently in the grammar than in the test string — e.g. `'not'` vs `'!'` |
| `t or f and t` returns 2 | Only two levels; `and` and `or` share one |

### Q13 — Why a prefix operator cannot be left-recursive

**`N ::= N "not"` would put the operator *after* its operand**, which is not what `not t` looks like. Left recursion means the recursive reference comes first and the operator follows it — that is the shape of an *infix* or *postfix* operator. A prefix operator has its keyword first, so the recursion must follow it: `N ::= "not" N`.

Accept any answer that connects recursion position to operator position. **Do not accept** "because it would loop forever" — `E ::= E "+" T` is left-recursive and does not loop; the grammar is fine, and only a naive top-down *parser* would loop, which is Week 2's problem.

---

## Part 5 — Extending Cyan (25 min)

### Q14 / Q15 — Model answer

`**` goes **between `mul_expr` and `unary`** — a new level, tighter than `*`, looser than unary. Right-associativity comes from **right** recursion:

```python
'mul':  [('mul', 'mulop', 'pw'), ('pw',)],    # mul_expr ::= mul_expr ("*"|"/"|"%") pow_expr | pow_expr
'pw':   [('un', 'pow', 'pw'), ('un',)],       # pow_expr ::= unary "**" pow_expr | unary
'un':   [('-', 'un'), ('!', 'un'), ('post',)],
```

**All six test expressions return exactly 1** *(verified)*:

```
1  n mulop n pow n            1  ( n pow n ) pow n
1  n pow n pow n              1  n addop n pow n mulop n
1  n pow n mulop n            1  - n pow n
```

**The right-recursion is the whole question.** A student who writes `'pw': [('pw','pow','un'), ('un',)]` gets a grammar that passes all six counts — it is unambiguous — but is **left**-associative, so `2 ** 3 ** 2` would be 64 rather than 512. **The counter cannot catch this.** Ask them to say which grouping their grammar produces; that is the checkoff, not the count.

> This is the Q4(b) lesson from PS 0 arriving early: **passing the ambiguity check does not mean the
> grammar is the one you wanted.** If a student hits it here, it is worth two minutes.

### Q16 — Where unary minus sits

**The model grammar above parses `- n ** n` as `(-n) ** n`**, because `pw ::= un "**" pw` takes a `un` on the left, and `un ::= "-" un` has already absorbed the minus.

**Python disagrees:**

```
$ python3 -c "print(-2 ** 2)"
-4
```

**Python gives `-4`, i.e. `-(2 ** 2)`** — exponentiation binds *tighter* than unary minus on its left. `(-2) ** 2` would be `4`.

To match Python, unary minus must sit **above** `**`:

```python
'mul':  [('mul', 'mulop', 'un2'), ('un2',)],
'un2':  [('-', 'un2'), ('!', 'un2'), ('pw2',)],
'pw2':  [('post', 'pow', 'un2'), ('post',)],   # right operand may carry a minus
```

*(Verified: this variant gives 1 for all six expressions plus `- n pow - n`.)*

**Neither is wrong**, and the marks — this being unmarked, the *checkoff* — are for the student noticing which one they built and being able to say so. Arguments to accept:

- **For Python's choice:** it matches mathematical notation, where $-x^2$ means $-(x^2)$.
- **For the other:** it is more uniform — every prefix operator binds tighter than every infix one, with no exception to remember.

**A student who has not checked which one their grammar produces has not finished Part 5**, even if all six counts are 1.

---

## Early Finish — The Dangling Else

```
 1  if e s
 2  if e if e s else s
 3  if e if e if e s else s else s
 1  if e if e s else s else s
```

*(Verified.)*

**The count is linear in the number of `if`s, not Catalan** — and that surprises people who expect the §4 explosion. The reason: each `else` can attach to any of the enclosing unmatched `if`s, so the count is the number of *attachments*, not the number of bracketings.

Braced, Cyan-style:

```
 1  if e { s }
 1  if e { if e { s } else { s } }
 1  if e { if e { s } } else { s }
```

**All 1.** The braces make the attachment explicit, so there is nothing left to choose.

---

## Checkoff Summary

| Part | Minimum to pass |
|---|---|
| **1** | Ten tools reporting versions; four paradigm programs run; Q1 has exchange clauses, not just a ranking |
| **2** | Two derivations differing in order, one tree, one AST, node counts stated |
| **3** | Catalan numbers recorded; Q9 prediction written *before* running |
| **4** | `BOOL_FIXED` passing all sixteen, demonstrated live |
| **5** | Six counts at 1, **and** the student can say whether their `**` is left- or right-associative and how `- n ** n` groups |

**If a student is short on time, cut Part 3's Q7.** Do not cut Part 5 Q16 — it is the only place in Week 0 where the limits of the verification tool are visible, and Week 2 depends on that lesson landing.

---

*CS 211 · Lab 0 Solutions · Instructor Only*
