# PROG 101 · Lab 2 — Operators, Evaluation Order, and Control Flow

**Name:** Adebayo Glover · **Lab:** Week 2 Lab 2
**Build:** `gcc 15.2.0`. Clean programs: `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`.
Demonstrative files (Parts 1A, 2): same flags **without** `-Werror`, plus `-fsanitize=undefined`
(their warnings / UB are the exercise). Every value below is real output.

---

## Part 1 — Precedence and What the Compiler Sees (5 pts)

### 1A — The parenthesis gallery (`precedence.c`)

`a = 6, b = 3, c = 2`. Predictions written before running:

| # | Expression | Predicted | Actual | How C parsed it |
|---|---|---|---|---|
| 1 | `a & b == c` | 0 | **0** | `a & (b == c)` → `6 & 0` (`==` binds tighter than `&`) |
| 2 | `(a & b) == c` | 1 | **1** | `(6 & 3) == 2` → `2 == 2` |
| 3 | `1 << 2 + 3` | 32 | **32** | `1 << (2 + 3)` → `1 << 5` (`+` binds tighter than `<<`) |
| 4 | `(1 << 2) + 3` | 7 | **7** | `4 + 3` |
| 5 | `a + b % c` | 7 | **7** | `a + (b % c)` → `6 + 1` |
| 6 | `~5` | −6 | **−6** | `~x == −x − 1` |
| 7 | `5 ^ 3` | 6 | **6** | `0101 ^ 0011 = 0110` |

**Lines 1 and 2 are the pair that matters:** they differ (`0` vs `1`) purely because `==` binds
*tighter* than `&`, so the same-looking expressions parse differently.

### 1B — The compiler was trying to tell you (2 pts)

The two lines that warn under `-Wall -Wextra` are **line 1** and **line 3**:

```
precedence.c:11:26: warning: suggest parentheses around comparison in operand of '&' [-Wparentheses]
precedence.c:13:22: warning: suggest parentheses around '+' inside '<<' [-Wparentheses]
```

It warns on these but **not** on `a + b % c`, because gcc warns where precedence is **widely
misremembered**, not everywhere it matters. `%` binding tighter than `+` matches ordinary arithmetic
(nobody is surprised), but `==` binding tighter than `&`, and `+` binding tighter than `<<`, are
historical accidents of C's grammar that contradict most people's intuition. Line 2 (the explicit
version) draws no warning either — the parentheses disambiguate it.

### 1C — Integer division and remainder (1 pt)

| Expression | Value |
|---|---|
| `-7 / 2` | **−3** |
| `-7 % 2` | **−1** |
| `7 / -2` | **−3** |
| `7 % -2` | **1** |

**C99+ rule:** integer division **truncates toward zero**, and the sign of `a % b` follows the sign of
the **dividend `a`** (not `b`). Identity `(a/b)*b + a%b == a`:

* `(-3)(2) + (-1) = -7` ✓
* `(-3)(-2) + (1) = 7` ✓

(This differs from Python, where `-7 // 2 == -4` and `-7 % 2 == 1` — floored division.)

---

## Part 2 — Undefined Behaviour, Caught (5 pts)

### 2A — The sequence point classic (`ub.c`) (2 pts)

Verbatim warning from `gcc -Wall -Wextra`:

```
ub.c:9:7: warning: operation on 'i' may be undefined [-Wsequence-point]
    9 |     i = i++;
      |     ~~^~~~~
```

The flag is **`-Wsequence-point`**, included in `-Wall`. The program then prints `5`, but that value is
meaningless.

**Sequence point:** a point in execution where all side effects of previous evaluations are complete
and none of the following have started. Between two sequence points C forbids modifying an object more
than once, and forbids reading it except to compute the value to be stored. `i = i++` writes `i`
**twice** (once by `++`, once by `=`) with no sequence point between them, so the standard gives the
line **no meaning at all** — this is *undefined*, not merely "compiler-dependent" (which would be
*unspecified*).

### 2B — Signed overflow (`overflow.c`) (1 pt)

Normal build prints `-2147483648`. Under `-fsanitize=undefined`:

```
overflow.c:9:5: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
-2147483648
```

UBSan reports and **continues**; the wrapped value still printed — but the program had no defined
behaviour at that point.

### 2C — Shifting too far (`shift.c`) (1 pt)

Under `-fsanitize=undefined`:

```
shift.c:9:22: runtime error: left shift of 1 by 31 places cannot be represented in type 'int'
-2147483648
```

A 32-bit `int` has 31 value bits plus a sign bit; `1 << 31` would set the sign bit, which C11 §6.5.7
leaves **undefined** for a signed type. **The one-character fix:** `1u << 31`. An `unsigned int` has 32
value bits and no sign bit, so the shift is defined modulo 2³².

### 2D — Why "it worked" proves nothing (1 pt)

Undefined behaviour imposes **no** requirement on the implementation, so printing the "expected" value
is merely one permitted outcome among all outcomes — it is not evidence of correctness. A test only
shows that UB did not manifest *on this compiler, at this optimisation level, on this input*; changing
any one of the three can change the result, and optimisers routinely do because they are entitled to
assume UB never happens. The two tools from this lab that find it: **the compiler's warnings**
(`-Wall -Wextra -Werror`, which caught 2A statically) and **UndefinedBehaviorSanitizer**
(`-fsanitize=undefined`, which caught 2B and 2C at run time).

---

## Part 3 — Control Flow (6 pts)

### 3A — Fall-through (`fallthrough.c`)

**1. Verified output:**

```
n=1: one two three
n=2: two three
n=3: three
n=4: four
n=5: other
```

`case 1` has no `break`, so control falls into `case 2` then `case 3`, stopping at `case 3`'s `break`.

**2. With `-Wall -Wextra -Werror` it does not compile** (two errors, one per falling-through arm):

```
error: this statement may fall through [-Werror=implicit-fallthrough=]
    6 |             case 1: printf("one ");
      |                     ^~~~~~~~~~~~~~
note: here
    7 |             case 2: printf("two ");
```

**3. The fix — declare the intent, do not change the logic:** add a `/* fall through */` comment on each
falling-through arm (gcc recognises it; C23 uses `[[fallthrough]]`). The output is unchanged and the
`-Werror` build now passes. The warning does not object to fall-through itself — only to fall-through
you did not *say* you meant.

### 3B — Loop trace (`collatz.c`, `x = 27`) (2 pts)

| Iter | `x` before | `x % 2` | `x` after |
|---|---|---|---|
| 1 | 27 | odd | 82 |
| 2 | 82 | even | 41 |
| 3 | 41 | odd | 124 |
| 4 | 124 | even | 62 |
| 5 | 62 | even | 31 |
| 6 | 31 | odd | 94 |
| 7 | 94 | even | 47 |
| 8 | 47 | odd | 142 |

**Final: `steps = 111`** (verified by running).

### 3C — `do-while` is not `while` (`dowhile.c`) (1 pt)

```
int k = 100, iter = 0;
do { iter++; } while (k < 10);
printf("%d\n", iter);   /* prints 1 */
```

The condition `k < 10` is false on entry, yet the body ran once — verified output `1`. You want this
whenever the loop must run **at least once to produce the value the condition then tests** — the
standard case is input validation: you must read a value before you can check it.

---

## Part 4 — A State Machine from `switch` and a Loop (4 pts)

`wordcount.c` reads `stdin` with `getchar()` and uses an explicit two-state machine (`OUT_OF_WORD` /
`IN_WORD`) driven by a `switch`. `words++` happens **on the transition into `IN_WORD`**, not on every
non-space character (the standard bug, which counts characters instead of words). `c` is an `int`, not
a `char`, so `EOF` stays distinguishable from every valid character.

Verified against `wc`:

| Input | Mine (`lines words chars`) | `wc` |
|---|---|---|
| `hello world\n` | `1 2 12` | `1 2 12` ✓ |
| empty | `0 0 0` | `0 0 0` ✓ |
| `   \n` | `1 0 4` | `1 0 4` ✓ |
| `a\n\n\nb\n` | `4 2 6` | `4 2 6` ✓ |

---

## Marking self-check

| Part | Points | Criteria |
|---|---|---|
| 1: precedence predicted, verified, warnings explained | 5 | all seven expressions; both warnings identified |
| 2: UB provoked and caught with tools | 5 | all four parts; sanitizer output pasted |
| 3: control flow traced and fallthrough fixed | 6 | trace table correct; `-Werror` build passes |
| 4: word-count state machine | 4 | all four test cases match `wc` |

---

*PROG 101 · Week 2 · Lab 2 · Adebayo Glover*
