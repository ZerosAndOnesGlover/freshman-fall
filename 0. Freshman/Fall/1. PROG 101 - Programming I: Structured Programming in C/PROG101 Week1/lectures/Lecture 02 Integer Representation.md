# PROG 101 · Programming I: Structured Programming in C
## Week 1 · Lecture 2: Integer Representation

**Date:** Wednesday 30 September 2026 · 10:00–10:50 · Week 1

---

## Lecture Goals

By the end of this lecture you can:

- State the size and range of every standard integer type, and explain why C does not fix them
- Explain two's complement, and why it makes the hardware simpler
- Predict what happens on overflow — and say why signed and unsigned differ *fundamentally*
- Recognise the signed/unsigned comparison trap before it costs you a day

---

## 1. The Fundamental Integer Types

Lecture 1 established that a type tells the compiler how many bytes an object occupies and how to interpret them. For integers, C specifies **minimum** ranges, not exact sizes.

Measured on this machine:

| Type | Bytes | Range |
|---|---|---|
| `char` | 1 | −128 … 127 |
| `short` | 2 | −32,768 … 32,767 |
| `int` | 4 | −2,147,483,648 … 2,147,483,647 |
| `long` | 8 | −9,223,372,036,854,775,808 … 9,223,372,036,854,775,807 |
| `long long` | 8 | same as `long` here |
| `unsigned int` | 4 | 0 … 4,294,967,295 |

**Read that table as a measurement, not a definition.** The standard guarantees only:

```
sizeof(char) == 1  ≤  sizeof(short)  ≤  sizeof(int)  ≤  sizeof(long)  ≤  sizeof(long long)
```

with minimum ranges of ±32,767 for `int` and ±2,147,483,647 for `long`. A 16-bit embedded compiler where `int` is 2 bytes is fully conforming. Code that assumes `int` is 32 bits is not portable, and that assumption is the single most common portability bug in C.

> **`char` is a third integer type.** It is neither `signed char` nor `unsigned char` — it is its own type whose signedness is **implementation-defined**. It is signed here (verified:
> `CHAR_MIN == -128`), but unsigned on ARM by default. When you need a byte, write `unsigned char`.
> When you need a small number, write `signed char`. Bare `char` is for characters.

### When you need exact sizes

```c
#include <stdint.h>

int32_t  x;    /* exactly 32 bits, signed      */
uint8_t  b;    /* exactly 8 bits, unsigned     */
int64_t  big;  /* exactly 64 bits, signed      */
size_t   n;    /* big enough for any object size */
```

Use these whenever the width matters — file formats, network protocols, hardware registers. Use plain `int` for loop counters and ordinary arithmetic, where the natural machine word is what you want.

`size_t` deserves special mention: it is **unsigned**, it is the type of `sizeof`, and it is what
every standard library length function returns. That it is unsigned is the source of §5's trap.

---

## 2. Two's Complement

How does a fixed pattern of bits represent a negative number?

C11 permitted three encodings; **C23 mandates two's complement**, and every machine you will meet uses it. Here is the rule:

> To negate a number: **invert every bit, then add 1.**

Verified bit patterns for `int8_t`:

| Value | Hex    | Binary     |
| ----- | ------ | ---------- |
| 0     | `0x00` | `00000000` |
| 1     | `0x01` | `00000001` |
| 127   | `0x7F` | `01111111` |
| −1    | `0xFF` | `11111111` |
| −128  | `0x80` | `10000000` |

Two things to notice, both consequences of the rule:

**−1 is all ones.** Invert `00000001` to get `11111110`, add 1 to get `11111111`. This is why
`~0` is `−1`, and why a "set all bits" idiom often appears as `-1` in C code.

**The top bit indicates sign** — but it is not a separate sign bit. It is simply the most significant
bit of a normal binary number that happens to have negative place value. For 8 bits, the value is:

```
−128·b₇ + 64·b₆ + 32·b₅ + 16·b₄ + 8·b₃ + 4·b₂ + 2·b₁ + 1·b₀
```

Check `11111111`: −128+64+32+16+8+4+2+1 = **−1**. ✓

### Why hardware designers chose it

**One circuit does both addition and subtraction.** In two's complement, `a − b` is exactly
`a + (−b)` computed with the *same* adder, with no special case. The alternatives (sign-magnitude, ones' complement) need separate subtraction logic and — worse — have **two representations of zero**, so an equality test needs a special case.

Two's complement has exactly one zero, and comparison for equality is a plain bit comparison.

### The asymmetry

Verified:

```
INT_MIN = -2147483648, INT_MAX = 2147483647
|INT_MIN| = 2147483648  >  INT_MAX = 2147483647
```

There is **one more negative number than positive.** With 32 bits there are 2³² patterns; one is
zero, leaving an odd count to split.

The practical consequence bites:

```c
int x = INT_MIN;
int y = -x;        /* UNDEFINED BEHAVIOUR: +2147483648 is not representable */
int z = abs(x);    /* same problem -- abs(INT_MIN) is UB */
```

`-INT_MIN` cannot be represented. Any code that negates or takes the absolute value of a
possibly-`INT_MIN` value has a latent bug, and it is a real one that has caused security
vulnerabilities in parsers that negate an attacker-supplied integer.

---

## 3. Overflow: The Signed/Unsigned Divide

This is the most important distinction in the lecture.

### Unsigned overflow is defined

```c
unsigned int u = UINT_MAX;
printf("%u\n", u + 1u);      /* verified: prints 0 */
```

Unsigned arithmetic is **modular**: results are reduced mod 2ⁿ. This is guaranteed by the standard,
completely portable, and safe to rely on. It is how hash functions, checksums, and pseudo-random
generators are written.

### Signed overflow is undefined behaviour

```c
int i = INT_MAX;
int j = i + 1;               /* UNDEFINED BEHAVIOUR */
```

Not "wraps to `INT_MIN`". Not "implementation-defined". **Undefined** — the standard imposes no
requirements at all, and the compiler may assume it never happens.

That last clause is what surprises people. Consider:

```c
if (x + 1 < x) { /* overflow check */ }
```

Since signed overflow cannot happen in a valid program, the compiler may reason that `x + 1 < x` is always false and **delete the check entirely**. This is not hypothetical; GCC and Clang both do it at `-O2`. The "safety check" vanishes, and the bug it was guarding against ships.

**Correct overflow checks test *before* overflowing:**

```c
if (x > INT_MAX - 1) { /* adding 1 would overflow */ }
```

Or use the compiler builtins, which are exact and branch-free:

```c
int result;
if (__builtin_add_overflow(a, b, &result)) { /* handle overflow */ }
```

> **Catch it while learning.** Build with `-fsanitize=undefined`. UBSan reports signed overflow at
> the exact line:

> ```
> runtime error: signed integer overflow: 2147483647 - -2 cannot be represented in type 'int'
> ```

---

## 4. Integer Promotion

Before arithmetic, C promotes small types. Verified:

```c
char a = 100, b = 100;
printf("%d\n", a + b);        /* 200 -- NOT overflow */
printf("%zu\n", sizeof(a+b)); /* 4 -- the result is an int */
```

`char` and `short` operands are converted to `int` before the operation. So `a + b` is computed as `int` arithmetic and 200 fits comfortably. The result only truncates if you **store it back**:

```c
char c = a + b;    /* NOW it truncates: 200 doesn't fit in a signed char */
```

The rule: **arithmetic never happens in a type narrower than `int`.** This is why `sizeof(a+b)` is 4,
not 1, and it catches people who expect C to compute in the declared type.

---

## 5. The Signed/Unsigned Comparison Trap

Verified, and this one costs real debugging hours:

```c
int          si = -1;
unsigned int ui = 1;
if (si < ui) { /* ... */ }     /* prints FALSE */
```

**−1 is not less than 1.** When a signed and an unsigned operand of the same rank meet, the *signed*
one converts to unsigned. `-1` becomes `4294967295`, which is emphatically not less than 1.

The classic form:

```c
for (size_t i = n - 1; i >= 0; i--)   /* INFINITE LOOP */
    process(a[i]);
```

`size_t` is unsigned, so `i >= 0` is **always true**. When `i` is 0 and decrements, it wraps to
`SIZE_MAX` and the loop reads far out of bounds. Worse, if `n` is 0 then `n - 1` is `SIZE_MAX` before the loop even starts.

Correct downward loops over an unsigned index:

```c
for (size_t i = n; i-- > 0; )        /* idiomatic: test then decrement */
    process(a[i]);
```

This reads oddly at first. `i-- > 0` tests the current value then decrements, so the body sees
`n-1, n-2, …, 0` and the loop ends when the test sees 0. It is correct even when `n == 0`.

> **The compiler will tell you.** GCC's `-Wsign-compare` (included in `-Wall -Wextra`) flags exactly
> this:

> ```
> warning: comparison of integer expressions of different signedness: 'int' and 'unsigned int'
> ```
>
> Under the course's `-Werror` it is a hard error. This is precisely why we mandate those flags.

---

## 6. Division and Modulo Signs

C's rules here differ from Python's, and mixing them up produces off-by-one bugs. Verified:

```
-7 / 2 = -3      (truncates toward ZERO, not toward -infinity)
-7 % 2 = -1      (sign follows the DIVIDEND)
 7 % -2 = 1
```

The invariant C guarantees:

```
a == (a / b) * b + a % b
```

Verified for `a = -7, b = 2`: `(-3)·2 + (-1) = -7`. ✓

**Python chooses differently**: it floors the division, so `-7 // 2` is `-4` and `-7 % 2` is `1` —
the sign follows the *divisor*. Both languages preserve the same identity; they just pick different
rounding. When you port code between them, every `%` on possibly-negative values needs checking.

The practical consequence: **`x % 2 == 1` is not a valid odd-number test in C**, because for negative odd `x` the result is `−1`. Use `x % 2 != 0`.

---

## 7. Summary

| Idea | Takeaway |
|---|---|
| Integer sizes | Minimums guaranteed, exact sizes are not — `int` is not always 32 bits |
| `char` | A third type; signedness is implementation-defined |
| `<stdint.h>` | `int32_t`, `uint8_t` when width matters; `size_t` for sizes |
| Two's complement | Invert and add 1; one adder does both operations; one zero |
| −1 is all ones | Which is why `~0 == -1` |
| The asymmetry | One more negative than positive; `-INT_MIN` is UB |
| **Unsigned overflow** | **Defined** — modular, portable, safe to rely on |
| **Signed overflow** | **Undefined** — the compiler may delete your check |
| Integer promotion | Arithmetic never happens narrower than `int` |
| Signed vs unsigned compare | Signed converts to unsigned; `-1 < 1u` is **false** |
| `i >= 0` on `size_t` | Always true — the classic infinite loop |
| `-7 % 2` | `-1` in C (sign of dividend); `1` in Python |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** For an 8-bit `signed char`, give the binary and decimal result of each:
(a) `127 + 1`  (b) `-128 - 1`  (c) `~0`  (d) `-1 >> 1` (arithmetic shift)

**2. (Explain.)** Why is `if (x + 1 < x)` not a valid overflow check for signed `x`, and what does
the compiler do with it?

**3. (Fix.)** Two bugs. Find and fix both.

```c
for (size_t i = strlen(s) - 1; i >= 0; i--)
    if (s[i] == ' ') s[i] = '_';
```

**4. (Stretch.)** Write `int safe_add(int a, int b, int *out)` returning 0 on success and −1 if the
addition would overflow, **without ever performing the overflowing addition**.

### Answers

**1.**

| | Binary | Decimal | Note |
|---|---|---|---|
| **(a)** `127 + 1` | `01111111 + 1 = 10000000` | **−128** | Wraps. As a *signed* type this is UB in C, though the bit pattern is what the hardware produces |
| **(b)** `-128 - 1` | `10000000 − 1 = 01111111` | **127** | Wraps the other way; also UB |
| **(c)** `~0` | `00000000 → 11111111` | **−1** | The all-ones pattern |
| **(d)** `-1 >> 1` | `11111111 → 11111111` | **−1** | Arithmetic shift replicates the sign bit, so −1 shifts to −1 forever |

*(d) is worth dwelling on:* right-shifting a negative value is implementation-defined in C — most
compilers do an arithmetic shift, preserving the sign, but the standard does not require it. Shift
unsigned values when you want defined bit behaviour.

**2.** Because signed overflow is **undefined behaviour**, and the compiler is permitted to assume
undefined behaviour never occurs in a correct program.

If `x + 1` never overflows — which the compiler may assume — then `x + 1` is always strictly greater
than `x`, so `x + 1 < x` is **always false**. The optimiser therefore replaces the whole condition
with `false` and **deletes the branch**.

GCC and Clang both do this at `-O2`. The check compiles to nothing, and the overflow it was meant to
catch happens unguarded. This is the single clearest demonstration that UB is not "whatever the
hardware does" — the *compiler*, not the CPU, is what breaks your code.

The fix is to test the precondition instead: `if (x > INT_MAX - 1)`, which involves no overflow.

**3.** Both bugs come from `size_t` being unsigned.

- **`i >= 0` is always true.** After `i` reaches 0 it decrements to `SIZE_MAX` (about 1.8×10¹⁹) and
  the loop keeps going, reading wildly out of bounds.
- **`strlen(s) - 1` underflows when `s` is empty.** `strlen("")` is 0, so `0 - 1` is `SIZE_MAX`, and
  the very first `s[i]` is a massive out-of-bounds read — before the loop body has done anything.

```c
for (size_t i = strlen(s); i-- > 0; )
    if (s[i] == ' ') s[i] = '_';
```

This handles both: the test happens before the decrement, so the body sees `len-1` down to `0`, and
when `len` is 0 the test `0 > 0` fails immediately and the loop never runs.

*Also acceptable:* use a signed index with an explicit cast, or iterate forward. Reject "change
`>= 0` to `> 0`" — that silently skips index 0.

**4.**

```c
int safe_add(int a, int b, int *out)
{
    if (b > 0 && a > INT_MAX - b) return -1;   /* would exceed INT_MAX */
    if (b < 0 && a < INT_MIN - b) return -1;   /* would fall below INT_MIN */
    *out = a + b;
    return 0;
}
```

**Why both branches are needed.** Overflow can happen in either direction, and the test differs:

- When `b > 0`, the sum grows, so the danger is exceeding `INT_MAX`. The condition `a > INT_MAX - b`
  is safe to evaluate because `b > 0` means `INT_MAX - b` cannot overflow.
- When `b < 0`, the sum shrinks, so the danger is `INT_MIN`. Again `INT_MIN - b` is safe because
  subtracting a negative moves *up*, away from `INT_MIN`.
- When `b == 0` neither branch fires and the addition is trivially safe.

**Every arithmetic operation in the checks is itself non-overflowing** — that is the whole point.
Writing `if (a + b > INT_MAX)` would perform the very overflow it claims to detect, and the compiler
would optimise it away exactly as in Exercise 2.

*Also full marks* for the builtin, which is what production code should use:

```c
if (__builtin_add_overflow(a, b, out)) return -1;
return 0;
```

It is exact, branch-free on most targets, and available in GCC and Clang — but it is not standard C,
so the portable version above is worth being able to write.

---

## Reading

- **K&R, §2.2, §2.9** — data types and bitwise operators
- **`<limits.h>`** — read it on your system: `/usr/include/limits.h`
- **C11 §6.3.1.1** — integer promotions; **§6.3.1.8** — the usual arithmetic conversions
- **Regehr, "A Guide to Undefined Behavior in C and C++"** — Part 1 covers integer overflow

---

*PROG 101 · Week 1 · Lecture 2 · © CSE Department*
