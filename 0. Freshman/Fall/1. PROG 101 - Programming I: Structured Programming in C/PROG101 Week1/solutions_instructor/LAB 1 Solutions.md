# PROG 101 — Week 1
## LAB 1 Solutions — INSTRUCTOR ONLY

> **Every implementation below compiles under `gcc -Wall -Wextra -Werror -std=c11` and runs clean
> under `-fsanitize=address,undefined`.** Where the lab requires it, Valgrind output is quoted
> verbatim. Reject any submission that does not build warning-free — `-Werror` is not negotiable in
> this course.

---

## Part 1A — `sizeof` Table (verified output)

```
char=1 short=2 int=4 long=8 longlong=8 float=4 double=8 ptr=8
INT_MAX=2147483647 INT_MIN=-2147483648 UINT_MAX=4294967295 CHAR_MIN=-128
```

`CHAR_MIN = -128` shows plain `char` is **signed** on x86-64 Linux. It is *unsigned* on ARM, which
is why `char` is a third type distinct from both `signed char` and `unsigned char`, and why you
should write `unsigned char` whenever you mean a byte.

## Part 1B — Two's Complement

Key facts students must demonstrate:

- `~x == -x - 1` exactly. So `~5 == -6`, and `~0 == -1`.
- `INT_MIN` has a single set bit: `10000000 00000000 00000000 00000000`.
- **`-INT_MIN` overflows** — `+2147483648` is not representable. The range is asymmetric.
- `INT_MAX + 1` is **undefined behaviour**, not a wrap to `INT_MIN`. Demonstrate with
  `-fsanitize=undefined`, which reports it at runtime. *Unsigned* overflow is defined to wrap.

---

## Part 2 — `bitlib` Reference Implementation

All functions verified; every assert passes under `-fsanitize=address,undefined`.

```c
uint32_t bit_set(uint32_t x, int n)    { return x |  (1u << n); }   /* OR sets   */
uint32_t bit_clear(uint32_t x, int n)  { return x & ~(1u << n); }   /* AND-NOT clears */
uint32_t bit_toggle(uint32_t x, int n) { return x ^  (1u << n); }   /* XOR flips */
int      bit_test(uint32_t x, int n)   { return (int)((x >> n) & 1u); }

/* Kernighan: n &= n-1 clears the lowest set bit. Loops once per SET bit. */
int bit_count(uint32_t x) { int c = 0; while (x) { x &= x - 1u; c++; } return c; }

/* One set bit <=> x & (x-1) == 0. The x != 0 term excludes zero. */
int bit_is_power_of_2(uint32_t x) { return x != 0 && (x & (x - 1u)) == 0; }

/* Parallel reversal: swap adjacent 1s, then 2s, 4s, 8s, then the halves. */
uint32_t bit_reverse(uint32_t x) {
    x = ((x & 0x55555555u) << 1)  | ((x & 0xAAAAAAAAu) >> 1);
    x = ((x & 0x33333333u) << 2)  | ((x & 0xCCCCCCCCu) >> 2);
    x = ((x & 0x0F0F0F0Fu) << 4)  | ((x & 0xF0F0F0F0u) >> 4);
    x = ((x & 0x00FF00FFu) << 8)  | ((x & 0xFF00FF00u) >> 8);
    return (x << 16) | (x >> 16);
}

uint32_t bit_extract(uint32_t x, int high, int low) {
    int width = high - low + 1;
    uint32_t mask = (width == 32) ? 0xFFFFFFFFu : ((1u << width) - 1u);
    return (x >> low) & mask;
}

uint32_t bit_set_field(uint32_t x, int high, int low, uint32_t value) {
    int width = high - low + 1;
    uint32_t mask = (width == 32) ? 0xFFFFFFFFu : ((1u << width) - 1u);
    return (x & ~(mask << low)) | ((value & mask) << low);
}

uint32_t bit_byteswap(uint32_t x) {
    return ((x & 0x000000FFu) << 24) | ((x & 0x0000FF00u) << 8)
         | ((x & 0x00FF0000u) >> 8)  | ((x & 0xFF000000u) >> 24);
}
```

Verified results:

```
bit_reverse(0x00000001) = 0x80000000
bit_reverse(0x12345678) = 0x1E6A2C48        (and reversing twice restores it)
bit_extract(0b11010110, 5, 2) = 0x5          matches the spec
bit_set_field(0xFF00FF00, 11, 8, 0xA) = 0xFF00FA00
bit_byteswap(0x12345678) = 0x78563412
```

### The three traps to grade for

1. **`1u << 32` is undefined behaviour.** `bit_extract(x, 31, 0)` has width 32, and the natural mask
   `(1u << width) - 1` invokes UB — shifting by ≥ the operand width is undefined, and on x86 the
   shift count is taken mod 32, so `1u << 32` silently yields `1` and the mask becomes `0`. The
   function then returns 0 for a full-width extract. **The `width == 32` guard is mandatory**, and
   `-fsanitize=undefined` catches its absence. This is the single most commonly missed case.
2. **`1u`, not `1`.** `1 << 31` on a signed `int` is undefined behaviour; `1u << 31` is fine. Check
   every shift literal.
3. **`bit_is_power_of_2(0)` must be 0.** `0 & (0-1)` is `0`, so the naive expression wrongly reports
   zero as a power of two. The `x != 0` term is not decoration.

`bit_count` via Kernighan's trick loops once per *set* bit, so it is O(popcount) rather than O(32).
Accept a 32-iteration loop, but mention `__builtin_popcount` (one instruction on modern CPUs) and
C23's `stdc_count_ones`.

---

## Part 3 — Loop Tracing

**3A.** Grade the *table*, not just the final value. A trace that shows only the answer proves
nothing; the per-iteration state is the deliverable.

**3B — Debug the Loop.** The recurring bugs:

| Symptom | Cause |
|---|---|
| Off by one at the end | `<=` where `<` belongs, or `n` vs `n-1` |
| Infinite loop | `continue` placed *before* the increment, so the counter never advances |
| Loop body never runs | Condition false on entry — check the initialiser |
| Wrong total | Accumulator initialised to the wrong identity (0 for sums, **1** for products) |

The product-initialised-to-zero bug is worth naming explicitly: zero is the absorbing element for
multiplication, so the result is pinned at 0 forever.

**3C — Loops from Spec.** Require a stated invariant for each. The pattern:

```c
/* Invariant: at the top of each iteration, sum == the total of a[0..i-1]. */
long sum = 0;
for (size_t i = 0; i < n; i++) sum += a[i];
/* Exit: i == n, so sum == total of a[0..n-1].  QED */
```

Note `long sum`, not `int` — summing many `int`s overflows, and signed overflow is UB.

---

## Marking Scheme

Points follow the allocation printed on the handout. Within each part:

- **Correctness (≈50%).** Passes the required test cases *and* the edge cases listed above.
- **Memory discipline (≈30%).** No leaks, no invalid reads/writes, every `malloc` checked, every
  owner documented. For labs with a Valgrind requirement this is pass/fail: **0 errors, 0 leaks.**
- **Method (≈20%).** Required technique actually used, bounds asserted, `const` applied where the
  function only reads.

**Automatic deductions, regardless of output:**
- Any compiler warning under `-Wall -Wextra`.
- Unchecked `malloc`/`realloc` return.
- `realloc` result assigned directly back to the original pointer (leaks the block on failure).
- A buffer function that can leave its output unterminated.

**Carry-through.** One wrong helper used consistently downstream costs marks once.

---

*PROG 101 · Week 1 · Lab Solutions · Instructor Copy · © CSE Department*
