# PROG 101 · Week 2
## LAB 2 Solutions — INSTRUCTOR ONLY

**Total: 20 points.** Every output below was produced by compiling and running the code with
`gcc -Wall -Wextra -Werror -pedantic -std=c11`.

---

## Part 1: Precedence and What the Compiler Sees (5 pts)

### 1A — verified output, `a = 6, b = 3, c = 2` *(2 pts)*

| # | Expression | Value | How C parsed it |
|---|---|---|---|
| 1 | `a & b == c` | `0` | `a & (b == c)` → `6 & 0` |
| 2 | `(a & b) == c` | `1` | `(6 & 3) == 2` → `2 == 2` |
| 3 | `1 << 2 + 3` | `32` | `1 << (2 + 3)` → `1 << 5` |
| 4 | `(1 << 2) + 3` | `7` | `4 + 3` |
| 5 | `a + b % c` | `7` | `a + (b % c)` → `6 + 1` |
| 6 | `~5` | `-6` | two's complement: `~x == -x - 1` |
| 7 | `5 ^ 3` | `6` | `0101 ^ 0011 = 0110` |

**Lines 1 and 2 are the pair that matters.** They differ (`0` vs `1`) purely because of precedence:
`==` binds **tighter** than `&`. Students who predicted both the same have found the exact bug this
part exists to teach.

*Marking: 2 pts for the table complete with parenthesisations. Values alone: 1 pt.*

### 1B — the warnings *(2 pts)*

Lines 1 and 3 warn:

```
warning: suggest parentheses around comparison in operand of '&' [-Wparentheses]
warning: suggest parentheses around '+' inside '<<' [-Wparentheses]
```

**The general rule:** GCC warns where the precedence is **widely misremembered**, not everywhere
precedence matters.

`a + b % c` is equally precedence-dependent and draws no warning, because `%` binding tighter than
`+` matches ordinary arithmetic — nobody is surprised by it.

But `&` binding *looser* than `==`, and `+` binding *tighter* than `<<`, are historical accidents of
C's grammar that contradict most people's intuition. Those are the ones GCC flags.

*Full marks require the "surprising vs unsurprising" distinction, not just "it warns on two of
them." Award 1 for identifying the lines without the rule.*

### 1C — division and remainder *(1 pt)*

| Expression | Value |
|---|---|
| `-7 / 2` | `-3` |
| `-7 % 2` | `-1` |
| `7 / -2` | `-3` |
| `7 % -2` | `1` |

**C99 rule:** integer division **truncates toward zero**, and the sign of `a % b` follows the sign of
**`a`** (the dividend), not `b`.

Identity check, `(a/b)*b + a%b == a`:

| | |
|---|---|
| `(-3)(2) + (-1) = -7` ✓ | `(-3)(-2) + 1 = 7` ✓ |

*This differs from Python, where `-7 // 2 == -4` and `-7 % 2 == 1` (floored division). Students
coming from CS 101 will get these wrong; it is worth 60 seconds in review.*

---

## Part 2: Undefined Behaviour, Caught (5 pts)

### 2A — the sequence point classic *(2 pts)*

```
ub.c:4:7: warning: operation on 'i' may be undefined [-Wsequence-point]
    4 |     i = i++;
      |     ~~^~~~~
```

The flag is **`-Wsequence-point`**, and it is **included in `-Wall`** — students do not need to add
it explicitly.

**Sequence point:** a point in execution at which all side effects of previous evaluations are
complete and none of the following have started. C forbids modifying an object **more than once**
between sequence points, and forbids reading it except to compute the value to be stored.

`i = i++` writes `i` twice (once by `++`, once by `=`) with no sequence point between. The standard
does not say which wins — it says the program has **no meaning at all**.

*Common wrong answer: "it depends on the compiler." That describes *unspecified* behaviour. Undefined
behaviour permits the compiler to assume the line never executes. Deduct 0.5.*

### 2B — signed overflow *(1 pt)*

Normal build printed `-2147483648`. Under `-fsanitize=undefined`:

```
ovf.c:5:5: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

*It still printed the wrapped value afterwards — UBSan reports and continues by default. Students
should note that the plausible-looking output was produced by a program with no defined behaviour.*

### 2C — shifting too far *(1 pt)*

```
ovf.c:7:22: runtime error: left shift of 1 by 31 places cannot be represented in type 'int'
```

`int` is 32 bits with 31 value bits plus a sign bit. `1 << 31` would set the sign bit, and for a
**signed** type C11 §6.5.7 leaves that undefined.

**The one-character fix:** `1u << 31`. An `unsigned int` has 32 value bits and no sign bit, and its
shifts are defined modulo 2³². *This is exactly why Problem Set 2's permission flags are written
`1u << n`.*

### 2D — why "it worked" proves nothing *(1 pt)*

Expected answer: undefined behaviour imposes **no** requirement on the implementation, so producing
the expected output is one permitted outcome among all outcomes — it is not evidence of correctness.
A test can only demonstrate that UB did not manifest *on this compiler, at this optimisation level,
on this input*; changing any of the three can change the result, and optimisers routinely do so
because they are entitled to assume UB never happens.

The two tools: **the compiler's own warnings** (`-Wall -Wextra -Werror`, which caught 2A statically)
and **UndefinedBehaviorSanitizer** (`-fsanitize=undefined`, which caught 2B and 2C at run time).

---

## Part 3: Control Flow (6 pts)

### 3A — fallthrough *(3 pts)*

**1. Verified output:**

```
n=1: one two three
n=2: two three
n=3: three
n=4: four
n=5: other
```

The `case 1` arm has no `break`, so control falls into `case 2` and then `case 3`, stopping at its
`break`. *(1 pt)*

**2. With `-Wall -Wextra -Werror` it does not compile:**

```
error: this statement may fall through [-Werror=implicit-fallthrough=]
   11 |         case 1: printf("one ");
      |                 ^~~~~~~~~~~~~~
note: here
   12 |         case 2: printf("two ");
cc1: all warnings being treated as errors
```

Two errors, one per falling-through arm. *(1 pt)*

**3. The fix — document the intent, don't change the logic:** *(1 pt)*

```c
case 1: printf("one "); /* fall through */
case 2: printf("two "); /* fall through */
case 3: printf("three "); break;
```

GCC recognises a `/* fall through */` comment (and the C23 `[[fallthrough]]` attribute, or GCC's
`__attribute__((fallthrough))`). Output is unchanged; the build now passes.

**The pedagogical point:** the warning does not object to fallthrough — it objects to fallthrough
you did not *say* you meant. Note that the empty chain `case 'a': case 'e':` never warns, because
there is no statement to fall through.

### 3B — loop trace, `x = 27` *(2 pts)*

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

**Final: `steps = 111`.** *(Verified.)*

*27 is chosen because it climbs to 9232 before descending — students who assume the sequence falls
monotonically discover otherwise by iteration 4.*

### 3C — `do-while` *(1 pt)*

```c
int k = 100, iter = 0;
do { iter++; } while (k < 10);
printf("%d\n", iter);   /* prints 1 */
```

The condition is false on entry, yet the body ran once — verified output `1`.

**When you want it:** whenever the loop must run at least once to *produce* the value the condition
tests. Input validation is the standard case — you must read before you can check what was read.

---

## Part 4: State Machine (4 pts)

Reference implementation:

```c
#include <stdio.h>

#define OUT_OF_WORD 0
#define IN_WORD     1

static int is_space(int c) { return c == ' ' || c == '\t' || c == '\n'; }

int main(void) {
    int st = OUT_OF_WORD;
    long words = 0, chars = 0, lines = 0;
    int c;

    while ((c = getchar()) != EOF) {
        chars++;
        if (c == '\n') lines++;

        switch (st) {
            case OUT_OF_WORD:
                if (!is_space(c)) { st = IN_WORD; words++; }
                break;
            case IN_WORD:
                if (is_space(c)) st = OUT_OF_WORD;
                break;
        }
    }

    printf("%ld %ld %ld\n", lines, words, chars);
    return 0;
}
```

**Verified against `wc`:**

| Input | Mine | `wc` |
|---|---|---|
| `hello world\n` | `1 2 12` | `1 2 12` ✓ |
| empty | `0 0 0` | `0 0 0` ✓ |
| `   \n` | `1 0 4` | `1 0 4` ✓ |
| `a\n\n\nb\n` | `4 2 6` | `4 2 6` ✓ |
| a 42-line source file | `42 234 1428` | `42 234 1428` ✓ |

**The one design decision worth marking:** `words++` happens on the **transition** into `IN_WORD`,
not on every non-space character. Counting inside the `IN_WORD` state instead is the standard bug
and yields a character count rather than a word count.

*`int c` — not `char c` — is required: `getchar()` returns `int` so that `EOF` is distinguishable
from every valid character. A student using `char` may pass all five tests and still be wrong; check
the declaration, not just the output.*

---

## Marking Summary

| Part | Points | Watch for |
|---|---|---|
| 1 | 5 | 1A lines 1 vs 2 must differ; 1B needs the "surprising precedence" rule |
| 2 | 5 | 2A must define *sequence point*, not just say "compiler-dependent" |
| 3 | 6 | 3A.3 must preserve output; 3B trace must show the climb to 142 |
| 4 | 4 | `words++` on transition; `int c` not `char c` |
| **Total** | **20** | |

---

*PROG 101 · Week 2 · Lab 2 Solutions · Instructor copy — do not distribute*
