# PROG 101 · Midterm 1
## Review Guide and Practice Exam

**Exam:** Wednesday 4 November 2026 · 18:00–19:30 · VNC 100 (Week 6)
**Duration:** 90 minutes · **Format:** Written, closed book. One handwritten A4 sheet, one side.
**Covers:** Weeks 0–5 · **Weight:** 12.5% of final grade

---

## Part I — Review Guide

### Weighting

| Area | Weeks | ~Share |
|---|---|---|
| Compilation model and toolchain | 0 | 8% |
| Types, integers, floating point | 1 | 20% |
| Operators, evaluation order, control flow | 2 | 15% |
| Functions, the call stack, scope | 3 | 17% |
| Arrays and strings | 4 | 20% |
| Pointers | 5 | 20% |

### The Ten Things That Cost Marks Every Year

1. **Saying "signed overflow wraps."** It is **undefined behaviour**. The compiler may delete your
   check entirely.
2. **Forgetting integer promotion.** `char + char` is computed as `int`.
3. **Comparing signed with unsigned.** `-1 < 1u` is **false**.
4. **Claiming `strncpy` is safe.** It does not null-terminate, and it pads the whole buffer.
5. **Giving `sizeof` on an array parameter as the array size.** It is the pointer size.
6. **Confusing `&a` with `&a[0]`.** Same address, different types — `&a + 1` jumps the whole array.
7. **Writing `p = realloc(p, n)`.** *(Week 6 material, but the habit starts here.)*
8. **Assuming argument evaluation order.** It is **unspecified**.
9. **Confusing scope with lifetime.** A `static` local has narrow scope and program lifetime.
10. **Giving a complexity without saying what n counts.**

### Facts Worth Memorising

| | |
|---|---|
| `sizeof` char/short/int/long | 1 / 2 / 4 / 8 |
| `INT_MAX` | 2147483647 |
| Unsigned overflow | **Defined** (modular) |
| Signed overflow | **Undefined** |
| `-7 / 2`, `-7 % 2` | **−3**, **−1** (truncates toward zero; sign follows dividend) |
| `0.1 + 0.2 == 0.3` | **false** |
| Exact integers in `double` / `float` | 2⁵³ / 2²⁴ |
| `(int)3.99`, `(int)-3.99` | **3**, **−3** (truncates, never rounds) |
| `sizeof(int a[10])` in scope vs parameter | **40** vs **8** |
| `a+1` vs `&a+1` for `int a[10]` | **+4** vs **+40** bytes |
| All object pointers | **8 bytes** |
| `p2 - p1` | Element **count**, not bytes |
| Guaranteed evaluation order | `&&`, `\|\|`, `?:`, `,` — nothing else |

---

## Part II — Practice Exam

**Attempt under exam conditions before reading Part III.** 90 minutes, one side of notes.

**Total: 100 points**

---

### Section A — Short Answer (30 points, 2 each)

**A1.** State the four stages of the C compilation pipeline, and which one `#include` belongs to.

**A2.** `UINT_MAX + 1u` and `INT_MAX + 1` differ fundamentally. State each result or status.

**A3.** Give the value and type of `sizeof(c1 + c2)` where both are `char`. Name the mechanism.

**A4.** Is `-1 < 1u` true or false? Explain in one sentence.

**A5.** State `-7 / 2` and `-7 % 2` in C, and which operand's sign the remainder follows.

**A6.** Is `0.1 + 0.2 == 0.3`? Give the reason in one sentence.

**A7.** Give the largest integer exactly representable in a `double`, and in a `float`.

**A8.** State the value of `(int)-3.99` and say whether C rounds or truncates.

**A9.** Name the **four** operators with a guaranteed evaluation order.

**A10.** What does `sizeof(f())` do to `f`? Explain.

**A11.** For `int a[10]` declared in `main`, give `sizeof a`. Then give it inside `void g(int a[10])`.

**A12.** State how many bytes `a + 1` and `&a + 1` advance for `int a[10]`.

**A13.** Give two distinct reasons `strncpy` is not "safe `strcpy`".

**A14.** For `int n = snprintf(dst, cap, ...)`, what does `n` hold, and what is the truncation test?

**A15.** Name three things a pointer's *type* controls, given that all object pointers are 8 bytes.

&nbsp;

---

### Section B — Code Reading (25 points)

**B1 (6 pts).** Give the output and explain.

```c
int i = 5;
printf("%d %d\n", i++, i++);
```

**B2 (6 pts).** Give the output.

```c
void c(void){ printf("c "); }
void b(void){ printf("b "); c(); printf("B "); }
void a(void){ printf("a "); b(); printf("A "); }
int main(void){ a(); printf("done\n"); return 0; }
```

State the maximum number of stack frames alive at once.

**B3 (6 pts).** What does this print? Explain both numbers.

```c
int a[5] = {1, 2, 3};
printf("%d %zu\n", a[3], sizeof a / sizeof a[0]);
```

**B4 (7 pts).** For each, say whether it compiles:

```c
const int *p = &x;  p = &y;      /* (a) */
const int *p = &x;  *p = 5;      /* (b) */
int *const q = &x;  q = &y;      /* (c) */
int *const q = &x;  *q = 5;      /* (d) */
```

&nbsp;

---

### Section C — Debugging (25 points)

**C1 (9 pts).** Three defects. Name each, say what happens at runtime, and fix it.

```c
int *build(int n)
{
    int a[n];
    for (int i = 0; i <= n; i++) a[i] = i;
    return a;
}
```

**C2 (8 pts).** Two defects.

```c
void greet(const char *name)
{
    char buf[16];
    strcpy(buf, "Hello, ");
    strcat(buf, name);
    printf("%s\n", buf);
}
```

**C3 (8 pts).** This loop is intended to walk backwards and prints the right answer. Explain why it
is nonetheless undefined, and rewrite it correctly.

```c
for (size_t i = n - 1; i >= 0; i--) process(a[i]);
```

&nbsp;

---

### Section D — Implementation (20 points)

**D1 (10 pts).** Write `void min_max(const int *a, size_t n, int *lo, int *hi)` setting `*lo` and
`*hi`. State what you do when `n == 0` and why.

**D2 (10 pts).** Write `int safe_copy(char *dst, size_t cap, const char *src)` returning 0 on
success and −1 if `src` would not fit. `dst` must be a valid string on **every** path, including
failure and `cap == 0`.

---

## Part III — Answer Key

> **Instructor copy.** Every value below was verified by execution.

### Section A

**A1.** Preprocess → compile → assemble → link. `#include` is **preprocessing**.

**A2.** `UINT_MAX + 1u` is **0** — unsigned arithmetic is modular and **defined**. `INT_MAX + 1` is
**undefined behaviour**; the compiler may assume it cannot happen and optimise accordingly. *(1 pt
each; the word "undefined" is required for the second.)*

**A3.** **4**, type `int`. **Integer promotion** — arithmetic never happens in a type narrower than
`int`. Verified: `char 100 + char 100` gives 200, not overflow.

**A4.** **False.** With one signed and one unsigned operand of equal rank, the signed converts to
unsigned; `-1` becomes 4294967295.

**A5.** `-7 / 2` is **−3**; `-7 % 2` is **−1**. The remainder follows the **dividend**. *(Python
differs — it follows the divisor.)*

**A6.** **No.** 0.1 and 0.2 have no exact binary representation, so the sum is 0.30000000000000004
while the nearest double to 0.3 is slightly smaller.

**A7.** `double`: **2⁵³** = 9,007,199,254,740,992. `float`: **2²⁴** = 16,777,216.

**A8.** **−3**. C **truncates toward zero**; it does not round. `(int)3.99` is likewise 3.

**A9.** `&&`, `||`, `?:`, and the comma operator `,`.

**A10.** **Nothing — `f` is not called.** `sizeof` does not evaluate its operand; it needs only the
type, known at compile time. Verified.

**A11.** **40** in `main`; **8** inside `g`, because the parameter has decayed to `int *`.

**A12.** `a + 1` advances **4** bytes; `&a + 1` advances **40** — `&a` has type `int (*)[10]`.

**A13.** (i) It does **not null-terminate** when the source is at least `n` long. (ii) It **pads the
entire buffer** with zeros, making it O(buffer size) rather than O(strlen).

**A14.** `n` holds the length `snprintf` **wanted** to write, not what it wrote. Truncation test:
`n >= (int)cap` — and the cast is required, since `cap` is unsigned.

**A15.** (i) How many bytes a dereference touches; (ii) how far `p + 1` moves; (iii) what assignments
the compiler permits.

---

### Section B

**B1 (6 pts).** **The question has no defined answer, and that is the answer.**

`i++` appears twice with no sequence point between, so `i` is modified twice — **undefined
behaviour**. Two separate errors are possible in reasoning about it: assuming a left-to-right
argument order (which is *unspecified*) and assuming the increments are sequenced at all (they are
not). GCC warns `-Wsequence-point`.

*Award 6 only for identifying UB. A specific numeric answer with confident reasoning earns 2.*

**B2 (6 pts).** Output: **`a b c B A done`**. Maximum frames alive: **4** — `main`, `a`, `b`, `c`,
all live while `c` runs. Verified.

**B3 (6 pts).** Prints **`0 5`** (verified). An array initialiser with fewer values than elements sets the
rest to zero, so `a[3]` is `0`; `sizeof a / sizeof a[0]` is `20 / 4 = 5` because `a` here is the array itself,
not a decayed pointer. *(2026-09-21: replaced a `SQUARE(x)` macro-trap question — function-like macros are Week 10.)*

**B4 (7 pts).** (a) **compiles** — the pointer is not const. (b) **rejected** — the target is const
through `p`. (c) **rejected** — the pointer is const. (d) **compiles** — only the pointer is const.
All four verified against the compiler. *(1 pt each, 3 for a correct statement of the rule.)*

---

### Section C

**C1 (9 pts).**

- **`return a;` returns the address of a local array.** The frame dies at return; the pointer
  dangles. GCC: `-Wreturn-local-addr`. Verified: GCC compiles such functions to **return NULL**.
- **`i <= n` writes one past the end** — `a[n]` is out of bounds.
- **`int a[n]` is a VLA on the stack.** A large `n` overflows the 8 MB stack, and its lifetime ends
  with the function regardless.

Fix: allocate on the heap and document the ownership, or take a caller-supplied buffer:

```c
int build(int *out, size_t n) { for (size_t i = 0; i < n; i++) out[i] = (int)i; return 0; }
```

**C2 (8 pts).**

- **`strcpy` and `strcat` are unbounded.** `"Hello, "` is 7 characters; any `name` of 9 or more
  overflows the 16-byte buffer.
- **No length is available** — `buf` is local so `sizeof buf` works here, but the code never uses it.

Fix: `snprintf(buf, sizeof buf, "Hello, %s", name);` — one call, bounded, terminated, and truncation
detectable from the return value.

**C3 (8 pts).** `size_t` is **unsigned**, so `i >= 0` is **always true**. When `i` reaches 0 and
decrements, it wraps to `SIZE_MAX` and the loop reads far out of bounds. Worse, if `n == 0` then
`n - 1` is `SIZE_MAX` before the loop even starts.

```c
for (size_t i = n; i-- > 0; ) process(a[i]);
```

Test-then-decrement: the body sees `n-1 … 0`, and with `n == 0` the loop never runs.

*Full marks require noting the `n == 0` case as well as the wrap.*

---

### Section D

**D1 (10 pts).**

```c
void min_max(const int *a, size_t n, int *lo, int *hi)
{
    if (n == 0) return;                 /* leave *lo and *hi untouched */
    *lo = *hi = a[0];
    for (size_t i = 1; i < n; i++) {
        if (a[i] < *lo) *lo = a[i];
        if (a[i] > *hi) *hi = a[i];
    }
}
```

**The `n == 0` decision must be stated and defended.** Leaving the outputs untouched is correct and
must be documented so callers know to initialise them; writing `INT_MAX`/`INT_MIN` is also
defensible if documented. Reading `a[0]` unconditionally is an out-of-bounds read and loses 4.

*3 pts for `const` on the input and non-const outputs; 4 for correct logic; 3 for the `n == 0`
decision with justification.*

**D2 (10 pts).**

```c
int safe_copy(char *dst, size_t cap, const char *src)
{
    if (cap == 0) return -1;                    /* no room even for a terminator */
    int n = snprintf(dst, cap, "%s", src);
    if (n < 0 || (size_t)n >= cap) {
        dst[cap - 1] = '\0';                    /* keep it a valid string */
        return -1;
    }
    return 0;
}
```

*Marking:* 3 for using `snprintf` at all; 3 for the correct truncation test **with the cast**; 2 for
the `cap == 0` guard; 2 for leaving `dst` terminated on the failure path. Any use of `strcpy` or
`strncpy` without an explicit terminator caps this at 3.

---

## Final Advice

**Show your reasoning.** Most questions award more for the argument than the answer.

**Say "undefined behaviour" when it applies** — B1 and C1 both turn on it, and a confident numeric
answer where the standard gives none is the most expensive mistake available.

**State the case.** Best, average, worst; signed or unsigned; in scope or as a parameter.

Good luck.

---

*PROG 101 · Week 6 · Midterm 1 · © CSE Department*
