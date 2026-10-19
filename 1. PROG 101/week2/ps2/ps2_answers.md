# PROG 101 · Week 2 · Problem Set 2 — Written Answers

**Name:** Adebayo Glover · **Set:** Problem Set 2 (Operators, Evaluation Order, and Control Flow)
**Build:** `gcc 15.2.0`, `gcc -Wall -Wextra -Werror -pedantic -std=c11`. Every output below is real.

---

## Problem 1 — Bit Manipulation  (`flags.c`)

The permission set lives in one `unsigned int`, with bits defined as

```c
#define PERM_READ  (1u << 0)
#define PERM_WRITE (1u << 1)
#define PERM_EXEC  (1u << 2)
```

### 1.1 / 1.2 — Output (matches the expected values)

```
set READ     -> 1
set EXEC     -> 5
clear READ   -> 4
toggle WRITE -> 6
test WRITE   -> 1
test READ    -> 0
bits set     -> 2
as rwx       -> -wx
```

* **Set** READ: `p = p | PERM_READ` → `0 | 1 = 1`.
* **Set** EXEC: `p = p | PERM_EXEC` → `1 | 4 = 5`.
* **Clear** READ: `p = p & ~PERM_READ` → `5 & ~1 = 5 & 0xFFFFFFFE = 4`.
* **Toggle** WRITE: `p = p ^ PERM_WRITE` → `4 ^ 2 = 6`.

After each step `p` is **1, 5, 4, 6** — exactly as expected. Membership is reported as `!= 0`, so the
tests print **exactly `0` or `1`** (`test WRITE -> 1`, `test READ -> 0`), *not* the masked value.

Set bits are counted by shifting `p` right (`for (rest = p; rest; rest >>= 1) count += rest & 1u;`) →
**2**. Printed as letters, bit 2 set + bit 1 set + bit 0 clear gives **`-wx`**.

### 1.3 — Why `1u << n` and not `1 << n`

`1` is a **signed** `int`. Shifting it so that a `1` lands in the sign bit — as `1 << 31` does on a
32-bit `int` — is **undefined behaviour** in C11 §6.5.7; the compiler may do anything. `1u` is an
**unsigned** `int`, which has 32 value bits and no sign bit, and its shifts are defined modulo 2³².
So `1u << n` is well defined for every `n` in `0..31`, while `1 << 31` is a latent UB bug. (This is the
same reason Lab 2's Part 2C needs `1u << 31`.) Since permissions are unsigned flags, `1u << n` is both
correct and portable.

---

## Problem 2 — Undefined and Unspecified Behaviour  (25 pts)

| # | Expression | Category | Justification |
|---|---|---|---|
| (a) | `i = i++;` | **Undefined** | Two unsequenced modifications of `i` (the `++` and the `=`) with no sequence point between them. |
| (b) | `f() + g();` order | **Unspecified** | The order in which the operands of `+` are evaluated is unspecified: either order is allowed. |
| (c) | `INT_MAX + 1` | **Undefined** | Signed integer overflow has no defined result; the compiler may assume it never happens. |
| (d) | `-1 >> 1` | **Implementation-defined** | Right-shifting a negative value is left to the implementation, which must document its choice. |

**Evidence:**

* **(a)** gcc emits, verbatim:
  ```
  seq.c:2:30: warning: operation on 'i' may be undefined [-Wsequence-point]
  ```
  and the program then prints `5` — but that value is meaningless: the standard gives the line **no
  definition at all**. (Note it is *undefined*, not merely "compiler-dependent" — that would be
  unspecified.)

* **(b)** The standard does not fix the evaluation order of `+`'s operands, so `f` or `g` may run first.
  Both are conforming; a program must not depend on which.

* **(c)** Under `-fsanitize=undefined`:
  ```
  ovf.c:3:34: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
  ```
  (the normal build still printed `-2147483648`, but with no guarantee).

* **(d)** `-1 >> 1` prints **`-1`** on gcc/x86-64 — an **arithmetic** shift (the sign bit is replicated).
  That is gcc's documented, implementation-defined choice; a logical shift (giving a large positive
  value) would be equally conforming.

---

## Problem 3 — `for` and `while`  (30 pts)

### 3.1 — Equivalent `while` rewrite (20 pts)

Original:

```c
for (int i = 0; i < n; i++) { if (i % 3 == 0) continue; total += i; }
```

Equivalent `while`:

```c
int i = 0;
while (i < n) {
    if (i % 3 == 0) { i++; continue; }   /* the increment must happen BEFORE continue */
    total += i;
    i++;
}
```

Verified: with `n = 10` both forms produce `total = 27` (indices 1,2,4,5,7,8).

### 3.2 — The one case where they differ (10 pts)

They are **not equivalent when the body uses `continue`**. In a `for` loop the increment `i++` runs
*after the body and after any `continue`*, whereas a naive `while` rewrite puts the increment only at
the end of the body — so a `continue` skips it. On the very first iteration (`i = 0`, `0 % 3 == 0`)
control jumps back to the test with `i` still `0`, and the loop **never terminates**. The fix is to
duplicate the increment immediately before every `continue` (as in 3.1), restoring the `for` loop's
guarantee that the increment always runs.

---

*PROG 101 · Week 2 · Problem Set 2 · Adebayo Glover*
