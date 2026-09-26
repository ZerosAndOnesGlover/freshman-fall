# PROG 101 · Problem Set 5 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: the set now has three problems: old 1C → Problem 1 (25), old Problem 2 without
`reverse_ptr`, `remove_negatives`, `partition_even_odd` and `is_palindrome_ptr` → Problem 2 (30: `longest_run`,
`find_word_bounds`, `two_sum_sorted`), old Problem 4 without `p_rotate` → Problem 3 (45). Answers for the removed
items below can be ignored.)*

## Answer Key (Instructor Copy)

### Problem 1 — Pointer Mechanics (15 pts)

**1A Prediction Table (5 pts).** Verified output, in order:

| Expression | Value | Note |
|---|---|---|
| `*p` | `20` | `p` aims at `b` |
| `*q` | `10` | `q` aims at `a` |
| `*p + *q` | `30` | 20 + 10 |
| `*p * *q` | `200` | 20 × 10. The space in `* *q` is **required** — `**q` would lex as a single token |
| `*(p) + 1` | `21` | dereference *then* add; contrast `*(p + 1)`, which reads the next `int` — out of bounds here |
| `*(&b)` | `20` | `*` and `&` cancel |
| `b` after `*p = 99` | `99` | writing through the pointer mutates `b` itself |
| `*p` after | `99` | same object |
| `*p` after `p = &c` | `30` | now aims at `c` |
| `b` after | `99` | **unchanged** — repointing `p` does not touch what it previously referenced |
| `*q` after `q = p` | `30` | both aim at `c` |
| `p == q` | `1` | same address |
| `*p == *q` | `1` | same value (trivially, same object) |

*Grading: 5 pts across 16 lines — roughly 0.3 each, rounded in the student's favour. The two conceptually load-bearing rows are `b` after `p = &c` (repointing ≠ mutating) and `*(p) + 1` vs `*(p + 1)`. A student who gets those two right and slips elsewhere should still score ≥ 4.*
*`printf("%p", …)` **must** cast to `void *` — passing an `int *` is UB for `%p`. The prompt already does this correctly; flag any student who removes the cast.*

**1B Pointer Arithmetic (5 pts).** Verified on x86-64:

| Type | `+1` advances | `sizeof` |
|---|---|---|
| `char *` | 1 byte | 1 |
| `short *` | 2 bytes | 2 |
| `int *` | 4 bytes | 4 |
| `double *` | 8 bytes | 8 |

1. Pointer arithmetic is in **units of the pointed-to type**, not bytes — `p + 1` means "the next object of this type", so the byte step is `sizeof(*p)`. This is what makes `arr[i]` ≡ `*(arr + i)` work uniformly for every element type.
2. The compiler knows the size **statically**, from the pointer's declared type; it multiplies the index by `sizeof` at compile time. This is also why arithmetic on `void *` is not permitted by the standard (gcc allows it as an extension, treating it as size 1).

*The `(char*)(xp+1) - (char*)xp` idiom in the prompt is the correct way to measure this: subtracting two `char *` yields a byte count. Subtracting the original typed pointers would give `1` for every type — worth pointing out, as a student may "simplify" it and lose the whole result.*

**1C Pointer to Pointer (5 pts).**
*Expected: `int **pp = &p;` gives `*pp` ≡ `p` (an `int *`) and `**pp` ≡ the `int`. Assigning `*pp = &c` **repoints `p` itself** — that is the whole reason double pointers exist: to let a callee modify the caller's pointer. Grade on whether the student connects this to the practical case (a function that allocates and must hand the pointer back, e.g. `void alloc_it(int **out)`), not merely on tracing arrows.*

---

### Problem 2 — Pointer-Based Data Manipulation (25 pts)

*Where "pointer-only" is required, indexing with `arr[i]` should cost marks only if the spec explicitly forbade it; otherwise treat `*(arr+i)` and `arr[i]` as identical (they are, by definition).*
*Probe the classic reversal bug: a two-pointer reverse with `while (lo <= hi)` swaps the middle element with itself on odd lengths — harmless — but `while (lo < hi)` is correct and clearer. Neither is wrong; a loop that runs `lo != hi` **is** wrong for even lengths (the pointers cross without ever being equal, running off both ends). Test with both an odd- and even-length array.*

---

### Problem 3 — `const` Correctness (15 pts)

```c
const int *p1;              /* 1. repoint yes, modify target no  */
int *const p2 = &v;         /* 2. repoint no,  modify target yes */
const int *const p3 = &v;   /* 3. neither                        */

int  total(const int *a, size_t n);      /* 4. promises not to modify */
void fill(char *out, size_t cap);        /* 5. must NOT be const      */
```

**(a) `const char *s` — 4 pts.** `s++` **compiles**; `s[0] = 'x'` is **rejected**. The `const` is
leftmost so it qualifies the `char` being pointed at, not the pointer. Moving the pointer changes no
`char`, so it is permitted.

**(b) `char *const s` — 4 pts.** Exactly reversed: `s++` is **rejected**, `s[0] = 'x'` **compiles**.
The `const` sits right of the `*`, so it qualifies the pointer itself.

*Verified: all four cases compile-checked; the results match the table above.*

The rule to state: **`const` qualifies whatever is immediately to its left, unless it is leftmost, in
which case it qualifies what is immediately to its right.**

**(c) — 4 pts.** `const` constrains **access through that particular pointer**, not the object.
`p` promises *"I will not modify anything through p"*; it says nothing about `v`, which is an
ordinary non-const `int` and may be assigned by name. It is a compile-time promise about **a route**,
not runtime protection of storage.

Students who answer "because `v` is not const" have the right conclusion; award full marks only if
they identify that the qualification attaches to the access path.

**(d) — 3 pts.** Any one of:

- **It widens what callers may pass.** A caller holding a `const int *` cannot pass it to a function
  taking `int *`; the `const` version accepts both.
- **It documents the contract in the type**, where it cannot go stale the way a comment can.
- **It enables optimisation** in some cases, by telling the compiler the callee will not write
  through that pointer.

*Reject "it stops me making mistakes"* — the question explicitly excludes that.

---

### Problem 4 — Pointer-Only Utilities (25 pts)

```c
size_t p_strlen(const char *s)
{ const char *p = s; while (*p) p++; return (size_t)(p - s); }

void p_reverse(int *a, size_t n)
{
    if (n < 2) return;
    int *l = a, *r = a + n - 1;
    while (l < r) { int t = *l; *l = *r; *r = t; l++; r--; }
}

int *p_find(int *a, size_t n, int target)
{
    for (int *p = a; p != a + n; p++) if (*p == target) return p;
    return NULL;
}

size_t p_count_between(const int *a, size_t n, int lo, int hi)
{
    size_t c = 0;
    for (const int *p = a; p != a + n; p++) if (*p >= lo && *p <= hi) c++;
    return c;
}

size_t p_remove_negatives(int *a, size_t n)
{
    int *w = a;
    for (int *r = a; r != a + n; r++) if (*r >= 0) *w++ = *r;
    return (size_t)(w - a);
}

void p_rotate(int *a, size_t n, size_t k)
{
    if (n == 0) return;
    k %= n;
    if (k == 0) return;
    p_reverse(a, k);
    p_reverse(a + k, n - k);
    p_reverse(a, n);
}
```

**Verified: 16 checks passing, Valgrind clean** — including `n = 0`, `n = 1`, even and odd lengths,
all-kept and none-kept removals, and `k > n`. (2026-09-21: `p_count_if`/`p_filter` took
function-pointer predicates — Week 11 — and were replaced; checked: `{5,-1,3,-7,0,8}` gives
`p_count_between(…,0,5) = 3` and `p_remove_negatives` → `5 3 0 8`, length 4.)

**Marking notes.**

- **`p_rotate` is where the marks separate.** The three-reversal algorithm is O(n) time and O(1)
  space. A solution using a temporary array is O(n) space and loses 3 of the 6; a repeated
  rotate-by-one is O(n·k) and loses 4.
- **`k %= n` before anything else** handles `k > n`. Verified: `k = 7` on `n = 5` gives the same
  result as `k = 2`. Omitting it reads out of bounds.
- **`n == 0` must be guarded before `k %= n`** — otherwise it is a division by zero, which is
  undefined behaviour in the very line meant to make the function safe. This is the same shape as
  Week 6's `size != 0` guard before `SIZE_MAX / size`.
- **`p_remove_negatives` must be one pass** with a write cursor trailing a read cursor. Removing elements one
  at a time with a shift is Θ(n²) — cap at 3 of 6 and name the cost.
- **`p != a + n` rather than `p < a + n`.** Both work for arrays; `!=` is the convention that
  generalises. Do not deduct for `<`.
- **Any `[]` in a function body** costs that function's marks, as stated in the problem.

---

### Problem 5 — Reading a Pointer Bug (20 pts)

*4 points each: 1 for naming, 1 for the runtime consequence, 1 for the tool, 1 for the fix.*

| | Defect | At runtime | Caught by | Fix |
|---|---|---|---|---|
| **(a)** | Returning the address of a local | The frame dies at return; the pointer dangles | `-Wreturn-local-addr` | Return by value, or take a caller-supplied `int *out` |
| **(b)** | Unbounded `strcpy` into an 8-byte buffer | Overflows `buf` when `s` is longer; corrupts adjacent stack | ASan; `-Wstringop-overflow` sometimes | `snprintf(buf, sizeof buf, "%s", s)` |
| **(c)** | `i <= n` off-by-one | Reads `a[n]`, one past the end | ASan / Valgrind | `i < n` |
| **(d)** | Uninitialised pointer dereferenced | Writes 5 to an arbitrary address | `-Wmaybe-uninitialized` (**at `-O1`+ only**) | Initialise before use |
| **(e)** | `strchr` result not checked for NULL | `*p` dereferences NULL when `'x'` is absent | Valgrind; static analysis | `if (!p) return -1;` before dereferencing |

**Marking notes.**

- **(a)** GCC compiles this to `return NULL` under optimisation — verified. A student who says "you
  get a stale address" has the common misconception; award the mark but correct it, because the point
  is that UB is a *compiler* phenomenon, not a hardware one.
- **(d)** The tool answer must note that `-Wmaybe-uninitialized` reports **nothing at `-O0`**.
  Verified. A bare "the compiler warns" is worth half.
- **(b)** Accept `strlcpy` or a manual bounded copy as the fix. Do **not** accept `strncpy` without
  an explicit terminator assignment, since `strncpy` does not null-terminate when the source fills
  the buffer.
- **(e)** Also accept restructuring to avoid `strchr` entirely. The mark is for recognising the
  unchecked return, which is the single most common C crash.

---

*PROG 101 · Week 5 · Problem Set 5 · © CSE Department*
