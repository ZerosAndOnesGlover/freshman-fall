# CS 211 · Problem Set 0 · Solutions
## Instructor Only

---

> **Every count in this document was produced by `lab/cfg_count.py`** and every arithmetic result by
> Python 3.14.2. Where a student's grammar differs from the model answer but passes the same
> verification, **mark it correct** — Q4(c) in particular has several right answers.

---

## Q1: Derivations and Trees (20)

### (a) [6] Leftmost derivation of `x = a + b * c`

```
S ⇒ A
  ⇒ IDENT = E                 (A ::= IDENT "=" E)
  ⇒ x = E
  ⇒ x = E + T                 (E ::= E "+" T)
  ⇒ x = T + T                 (E ::= T)
  ⇒ x = F + T
  ⇒ x = IDENT + T
  ⇒ x = a + T
  ⇒ x = a + T * F             (T ::= T "*" F)
  ⇒ x = a + F * F
  ⇒ x = a + IDENT * F
  ⇒ x = a + b * F
  ⇒ x = a + b * IDENT
  ⇒ x = a + b * c
```

**Mark scheme:** 6 for a complete correct sequence. **−2** if any step expands a non-leftmost non-terminal. **−1** per missing intermediate line. Accept collapsing `F ⇒ IDENT ⇒ a` into one step if done consistently.

### (b) [4] Rightmost derivation

```
S ⇒ A ⇒ IDENT = E
  ⇒ IDENT = E + T
  ⇒ IDENT = E + T * F
  ⇒ IDENT = E + T * IDENT     (rightmost first)
  ⇒ IDENT = E + T * c
  ⇒ IDENT = E + F * c
  ⇒ IDENT = E + b * c
  ⇒ IDENT = T + b * c
  ⇒ IDENT = F + b * c
  ⇒ IDENT = a + b * c
  ⇒ x = a + b * c
```

**Mark scheme:** 4 for correct rightmost order. The common error is producing the leftmost sequence again with the lines shuffled — check that each step really expands the rightmost non-terminal.

### (c) [4] The parse tree

```
S
└── A
    ├── IDENT(x)
    ├── "="
    └── E
        ├── E
        │   └── T
        │       └── F
        │           └── IDENT(a)
        ├── "+"
        └── T
            ├── T
            │   └── F
            │       └── IDENT(b)
            ├── "*"
            └── F
                └── IDENT(c)
```

**Node count: 17.** Ten non-terminals (`S`, `A`, two `E`, three `T`, three `F`) and seven terminals (`x`, `=`, `a`, `+`, `b`, `*`, `c`).

*Verified: the grammar gives this string exactly one parse tree.*

**Mark scheme:** 3 for a correct tree shape, 1 for the count. Accept 10 (non-terminals only) **if the student states that convention** — the question says "counting every non-terminal and every terminal", so an unstated 10 loses the mark.

### (d) [6] The AST

```
Assign
├── Var(x)
└── Add
    ├── Var(a)
    └── Mul
        ├── Var(b)
        └── Var(c)
```

**7 nodes.** Discarded: $17 - 7 = 10$, which is $10/17 = \mathbf{58.8\%}$ of the parse tree.

**What the discarded nodes were for:** they encoded *precedence and associativity during parsing* — the `E`/`T`/`F` ladder is the machinery that forced `Mul` under `Add`. Once the tree has that shape the ladder has done its job, and the shape itself now carries the information.

**Mark scheme:** 3 tree, 1 count, 2 for the explanation. The explanation must say the nodes did work *during* parsing — "they are just noise" earns 0 of the 2.

---

## Q2: Ambiguity by Hand (22)

### (a) [5] All parse trees for `9 - 5 - 2`

**Two trees** *(verified: count = 2)*.

```
      E                          E
    / | \                      / | \
   E  -  E                    E  -  E
  /|\     \                  /      /|\
 E - E     2                9      E - E
 |   |                             |   |
 9   5                             5   2

   ((9-5)-2)                    (9-(5-2))
```

**Mark scheme:** 5 for both trees correctly drawn. **−3** for only one. Drawing three or more means the student has confused derivation order with tree shape — worth a comment.

### (b) [5] Evaluate each

$((9-5)-2) = 4 - 2 = \mathbf{2}$
$(9-(5-2)) = 9 - 3 = \mathbf{6}$

**They disagree.** What the grammar has failed to specify is **associativity** — it says `-` is a binary operator between two expressions, and says nothing about how to group a chain of them. **Until that is fixed the grammar does not define a language**, because a program in it has more than one meaning.

**Mark scheme:** 2 for the two values, 3 for naming associativity as the missing specification. "It's ambiguous" alone earns 1 of the 3 — the question asks *what* was left unspecified.

### (c) [6] Left-associative

```bnf
E ::= E "-" T | T
T ::= NUM
```

**Left recursion on `E`** means the left operand may itself be a subtraction while the right may not, forcing `((9-5)-2)`. **Evaluates to 2.**

### (d) [6] Right-associative

```bnf
E ::= T "-" E | T
T ::= NUM
```

**Evaluates to 6.**

**Is there a language with right-associative subtraction?** In common use, **no** — and the reason is that left-associativity is what matches the reading order of ordinary arithmetic notation, which predates every programming language. Accept either an honest "none in common use, because arithmetic convention is older than programming languages" **or** a correct counter-example from an unusual language. **What must not appear** is a claim that some mainstream language (C, Python, Java, Haskell) has right-associative `-`; that is simply false and costs all 6.

*Worth mentioning in review:* right-associativity is normal for **exponentiation** (`2**3**2` = 512 in Python) and for `=` in C (`a = b = c`). So the concept is not exotic — it is subtraction specifically where left is universal.

**Mark scheme:** 3 for the grammar, 1 for the value, 2 for the language argument.

---

## Q3: Counting Without Counting (14)

### (a) [6] The recurrence

$$T(k) = \sum_{i=1}^{k-1} T(i) \cdot T(k-i), \qquad T(1) = 1$$

**Reasoning to expect:** the root `+` splits the $k$ operands into a non-empty left group of $i$ and a non-empty right group of $k-i$. Each grouping is independent, so the counts multiply; the groupings are disjoint, so they add.

**Mark scheme:** 4 for the sum, 1 for the base case, 1 for the multiply-then-add justification. **−2** if the sum runs $i = 1$ to $k$ (allowing an empty side).

### (b) [4] $T(7)$ by hand

$$T(7) = 1{\cdot}42 + 1{\cdot}14 + 2{\cdot}5 + 5{\cdot}2 + 14{\cdot}1 + 42{\cdot}1 = 42+14+10+10+14+42 = \mathbf{132}$$

using $T(1..6) = 1, 1, 2, 5, 14, 42$.

**Mark scheme:** 4 for 132 with the arithmetic shown. **2** for 132 with no working.

### (c) [4] Thirty operands

$$T(30) = C_{29} = 1{,}002{,}242{,}216{,}651{,}368 \approx \mathbf{10^{15}}$$

*(Exact value verified. The approximation $4^{29}/(29^{1.5}\sqrt{\pi}) = 1.04 \times 10^{15}$ agrees to within 4%.)*

**Accept anything from $10^{14}$ to $10^{16}$.** The question asks for an order of magnitude.

**The comment:** a parser that enumerated parse trees would need $10^{15}$ of them for one ordinary line of arithmetic — at a nanosecond each that is **eleven days**. **Enumeration is not a strategy.** A real parser commits to one tree using a disambiguated grammar and never materialises the others; this is exactly why §5 of L02 fixes the grammar rather than filtering the output.

**Mark scheme:** 2 for the magnitude, 2 for a comment that draws the right conclusion — that ambiguity must be removed *before* parsing, not resolved after.

---

## Q4: The Ambiguity Checker (24)

### (a) [8] Grammar One is ambiguous

**Shortest ambiguous string: `[ n , n , ]`, with 2 parse trees.** And `[ n , n , n , ]` gives **5**.

*(Verified. Note that `[ n , n ]` and `[ n , ]` each give 1 — students who test only those will report "no ambiguity found" and should be pushed to test longer strings with a trailing comma.)*

**Where the derivations diverge.** The culprit is `items ::= items "," items`, which is the Catalan-style rule from L02 §4 — it lets `n , n` be split either way — **combined with** `items ::= items ","` which supplies the trailing comma. For `[ n , n , ]`:

- **Tree 1:** `items → items ","` where the inner `items → items "," items → n , n`
- **Tree 2:** `items → items "," items` where the right `items → items ","`… absorbing the final comma into the right branch instead of the outer rule.

**Mark scheme:** 3 for finding an ambiguous string, 2 for the count of 5, 3 for locating the divergence in `items ::= items "," items`. A student who blames only the trailing-comma rule has half the answer — the self-referential rule is what supplies the second tree.

### (b) [8] Grammar Two is unambiguous and still wrong

```
[ n , n , ]   -> 1
[ n , , n ]   -> 1      <-- and this string should not be in the language at all
```

**The defect: Grammar Two accepts `[ n , , n ]`** — a list with an empty slot — and gives it exactly one parse tree. The `items ::= items ","` rule can fire in the *middle* of the list, not just at the end, and the grammar has no way to say "only at the end".

**Why the checker could not have told you.** The counter answers "how many trees?", and the answer here is 1, which is what a correct grammar also gives. **A count of 1 says the grammar is unambiguous; it says nothing about whether the language it generates is the language you wanted.** Checking that requires you to supply strings that *should* be rejected — which is why the question, and Lab 0 Part 4, always give a negative test list alongside the positive one.

**Mark scheme:** 3 for identifying `[ n , , n ]` as wrongly accepted, 2 for locating the cause in `items ::= items ","` firing mid-list, 3 for the point about the checker's blind spot. **This last part is the question** — a student who only reports the counts gets 5.

### (c) [8] A grammar with neither defect

**Model answer:**

```python
LIST_FIXED = {
    'L':     [('[', ']'), ('[', 'items', ']')],
    'items': [('elems',), ('elems', ',')],
    'elems': [('elems', ',', 'e'), ('e',)],
    'e':     [('n',)],
}
```

**The idea:** `elems` is a strictly comma-*separated* list — unambiguous because it is left-recursive with a single terminal element on the right. `items` then wraps it and permits **exactly one** optional trailing comma, in the one place it can legally appear.

Verified output:

```
  1  [ ]                 0  [ , ]
  1  [ n ]               0  [ , n ]
  1  [ n , ]             0  [ n , , n ]
  1  [ n , n ]           0  [ n n ]
  1  [ n , n , ]
  1  [ n , n , n , ]
```

**Other correct answers exist** — e.g. splitting on whether a trailing comma is present at the `L` level. **Mark any grammar that passes all ten checks as fully correct**; the marks are for the verification, not for matching this shape.

**Mark scheme:** 5 for a grammar passing all ten, 3 for pasting the actual output. **A grammar that passes the six positives but accepts one negative earns at most 4** — that is precisely the Grammar Two failure the question just taught.

---

## Q5: Design Under Constraint (20)

### (a) [6] C's arithmetic

With `a = 1, b = 5, c = 3`:

1. `a < b` → `1 < 5` → **`1`** (C has no `bool`; relational operators yield `int` `0` or `1`)
2. `1 < c` → `1 < 3` → **`1`**

So `a < b < c` prints `1`. *(Verified: gcc 13.3.0 prints `1`, and warns `comparisons like 'X<=Y<=Z' do not have their mathematical meaning [-Wparentheses]`.)*

**Why a reader calls it wrong:** the reader reads `a < b < c` as the mathematical claim $1 < 5 < 3$, which is false. **C's answer is not a bug** — it follows from `<` being left-associative and returning an `int` that is then a valid operand for another `<`. The wrongness is in the gap between what the notation means to a human and what the grammar means by it.

**Mark scheme:** 3 for the arithmetic, 3 for locating the problem in the notation/semantics gap rather than calling C broken.

### (b) [6] Python's real desugaring

**The naive version is wrong:**

```python
a < b and b < c          # for f() < g() < h():
f() < g() and g() < h()  # calls g() TWICE
```

*(Verified: call order is `f, g, g, h` for the naive version, but `f, g, h` for real Python.)*

**Python evaluates each operand exactly once**, so the desugaring must bind the middle operand first:

```python
tmp1 = f()
tmp2 = g()
result = tmp1 < tmp2
if result:
    result = tmp2 < h()
```

**Why the naive version is wrong** is not just efficiency — `g()` may have side effects, or may return a different value the second time. **The chain is defined in terms of the *values*, evaluated once, left to right, with short-circuiting.**

**Mark scheme:** 2 for spotting the double evaluation, 2 for a correct single-evaluation desugaring, 2 for saying *why* it matters (side effects / non-determinism, not merely speed). A student who says only "it's slower" gets 4 of 6.

### (c) [8] The argument

**There is no required answer.** All three positions are defensible, and the marks are entirely for whether the cost is named concretely.

| Position | A good argument names… |
|---|---|
| **C** | uniformity — one rule for all binary operators, no special cases in the grammar, and a warning already exists. **Cost:** a silently wrong result in code that reads correctly. |
| **Python** | it gives the answer the notation promises. **Cost:** a special production, an operand evaluated in a way that does not follow from the general rule, and a construct that behaves unlike every other binary operator in the language. |
| **Cyan** | no wrong answer is *expressible*; the error is caught at parse time with no analysis. **Cost:** `a < b && b < c` is more verbose, and a programmer coming from Python finds a familiar, correct-in-their-language construct rejected. |

**Full marks require a concrete situation**, not a general claim. Examples that earn it:

- *For C:* a range check `if (0 <= i < n)` compiles, always passes, and the bounds bug ships.
- *For Python:* someone writes `a < b < c` expecting C semantics and gets a different answer, or a code generator emitting comparison chains has to special-case them.
- *For Cyan:* a mathematical formula transcribed from a paper must be manually rewritten, and the rewrite is where a typo enters.

**Mark scheme:** 3 for a clearly stated position, 5 for the cost. **A student who argues their choice has no downside earns at most 3** — the entire point of the question, and of habit 2 in the syllabus, is that there is always a cost.

---

## Mark Distribution

| Question | Points | Common failure |
|---|---:|---|
| Q1 | 20 | Rightmost derivation written as a shuffled leftmost |
| Q2 | 22 | Claiming a mainstream language has right-associative `-` |
| Q3 | 14 | Recurrence summing $i=1..k$, allowing an empty side |
| Q4 | 24 | Reporting counts for (b) without seeing the blind spot |
| Q5 | 20 | Arguing a position has no cost |
| **Total** | **100** | |

**If the cohort average on Q4(b) is below 60%**, spend five minutes of Week 1's Tuesday lecture on it before starting the lexer — the idea that verification tools answer only the question you asked recurs in Week 2 with bison's conflict reports, and it is worth landing properly the first time.

---

*CS 211 · PS 0 Solutions · Instructor Only*
