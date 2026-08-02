# PROG 101 — Midterm 2
## Review Guide and Practice Exam

**Exam:** Week 10, Wednesday · 18:00–19:30 · VNC 100
**Duration:** 90 minutes · **Format:** Written, closed book. One handwritten A4 sheet, one side.
**Covers:** Weeks 6–9 · **Weight:** 12.5% of final grade

---

## Part I — Review Guide

### Weighting

| Area | Week | ~Share |
|---|---|---|
| Dynamic memory, ownership, Valgrind | 6 | 30% |
| Structures, unions, enums, linked lists | 7 | 25% |
| File I/O and the UNIX file model | 8 | 20% |
| Recursion and stack mechanics | 9 | 25% |

**Weeks 0–5 are assumed**, not re-examined. Pointers and arrays appear throughout because everything
here is built on them.

### The Ten Things That Cost Marks

1. **`p = realloc(p, n)`** — on failure you leak the original and lose your only pointer.
2. **Forgetting to free on an error path.** The early `return` between two allocations.
3. **Freeing the container but not its contents.** Valgrind: one *definitely lost* per element.
4. **Assuming `malloc` zeroes.** It does not; `calloc` does.
5. **`while (!feof(f))`** — `feof` becomes true only *after* a failed read, so the last item is
   processed twice.
6. **Not checking `fopen`.** It returns NULL, and `fclose(NULL)` is undefined.
7. **Adding up struct members to get `sizeof`.** Padding makes the total larger.
8. **Type-punning through a union and calling it portable.** It is implementation-defined.
9. **Recursion with no base case, or a base case that cannot be reached.**
10. **Claiming naive `fib` is "slow"** without saying it is exponential — Θ(φⁿ).

### Facts Worth Memorising

| | |
|---|---|
| `malloc` zeroes? | **No.** `calloc` does — and checks `n × size` for overflow |
| `realloc(NULL, n)` | Acts as `malloc` |
| `free(NULL)` | Safe no-op |
| Doubling growth | Amortised **O(1)**; total copying < 2n |
| `struct {char; int; char}` | **12** bytes, not 6 |
| Reordered to `{int; char; char}` | **8** bytes |
| `sizeof(union)` | The **largest** member |
| `enum {RED, GREEN=5, BLUE}` | 0, 5, **6** |
| `fopen` failure | Returns **NULL** |
| `feof` after reading 2 of 2 lines | **1**, only after the failed read |
| `fact(10)` | 3,628,800 |
| Naive `fib(20)` | **21,891** calls = 2·fib(21) − 1 |
| ASan vs Valgrind | ASan **misses uninitialised reads** |

---

## Part II — Practice Exam

**Attempt under exam conditions.** 90 minutes, one side of notes.

**Total: 100 points**

---

### Section A — Short Answer (30 points, 2 each)

**A1.** State two things `calloc` does that `malloc` does not.

**A2.** Why is `p = realloc(p, n);` wrong? State exactly what is lost on failure.

**A3.** Give the value of `free(NULL)` — that is, what happens.

**A4.** For `struct A { char c; int i; char d; };` give `sizeof(struct A)` and explain the gap
between that and the sum of its members.

**A5.** Reorder `struct A`'s members to minimise its size, and give the new size.

**A6.** State `sizeof` for `union U { int i; float f; char b[4]; }` and the rule behind it.

**A7.** Given `enum Colour { RED, GREEN = 5, BLUE };` give all three values.

**A8.** What does `fopen` return on failure, and what is wrong with passing that to `fclose`?

**A9.** Explain in one sentence why `while (!feof(f))` processes the last record twice.

**A10.** State the two things every recursive function needs.

**A11.** How many calls does naive `fib(20)` make? Give the formula.

**A12.** Naive `fib` is exponential. State the base of the exponent.

**A13.** State the growth strategy that gives amortised O(1) append, and the one that gives Θ(n²).

**A14.** Name one class of bug Valgrind detects that AddressSanitizer does not.

**A15.** Give the Valgrind message for a leak, verbatim enough to be recognisable.

&nbsp;

---

### Section B — Code Reading (25 points)

**B1 (7 pts).** What does this print, and how many bytes leak?

```c
char *a = malloc(10);
char *b = malloc(20);
a = b;
free(a);
```

**B2 (6 pts).** Give `sizeof(struct S)` and explain each padding byte.

```c
struct S { char a; double b; char c; short d; };
```

**B3 (6 pts).** This function is intended to count lines. Give the bug and the symptom.

```c
int count(FILE *f) {
    int n = 0; char buf[128];
    while (!feof(f)) { fgets(buf, sizeof buf, f); n++; }
    return n;
}
```

**B4 (6 pts).** Trace `mystery(4)` and state what it computes.

```c
int mystery(int n) { return n <= 1 ? 1 : n * mystery(n - 1); }
```

&nbsp;

---

### Section C — Debugging (25 points)

**C1 (9 pts).** Three defects.

```c
typedef struct { char *name; int age; } Person;

Person *make(const char *name, int age) {
    Person *p = malloc(sizeof p);
    p->name = malloc(strlen(name));
    strcpy(p->name, name);
    p->age = age;
    return p;
}
```

**C2 (8 pts).** Two defects, one of which only appears on an error path.

```c
int process(const char *path) {
    FILE *f = fopen(path, "r");
    char *buf = malloc(1024);
    if (!buf) return -1;
    while (fgets(buf, 1024, f)) puts(buf);
    fclose(f);
    free(buf);
    return 0;
}
```

**C3 (8 pts).** This grows a list. Find the two defects and fix both.

```c
void add(int **arr, size_t *len, size_t *cap, int v) {
    if (*len == *cap) {
        *cap *= 2;
        *arr = realloc(*arr, *cap * sizeof **arr);
    }
    (*arr)[(*len)++] = v;
}
```

&nbsp;

---

### Section D — Implementation (20 points)

**D1 (10 pts).** Write `Person *person_new(const char *name, int age)` and
`void person_free(Person **p)` for `typedef struct { char *name; int age; } Person;`.
State the ownership contract in a comment. Both must be Valgrind-clean.

**D2 (10 pts).** Write a **recursive** `int sum_digits(long n)` returning the sum of the decimal
digits of `|n|`. State your base case and justify that it is reachable for every input, including
`n == 0` and negative values.

---

## Part III — Answer Key

> **Instructor copy.** Every value verified by execution.

### Section A

**A1.** It **zeroes** the memory, and it **checks `n × size` for overflow** — `malloc(n*size)` can
wrap silently.

**A2.** On failure `realloc` returns NULL **and leaves the original block allocated**. Assigning back
overwrites the only pointer to it: the block leaks *and* the data is lost. Use a temporary.

**A3.** A **guaranteed no-op**. It is safe and requires no guard.

**A4.** **12 bytes.** The members sum to 6 (1 + 4 + 1). `int` must be 4-byte aligned, so 3 padding
bytes follow `c`; then 3 more trail `d` so the struct's size is a multiple of its strictest alignment
(4), allowing arrays of it to stay aligned. Verified: `offsetof` gives c=0, i=4, d=8.

**A5.** `struct B { int i; char c; char d; };` → **8 bytes**. Verified: reordering saves 4.
*(General rule: declare members in decreasing size order.)*

**A6.** **4** — a union is at least as large as its **largest** member (and padded to its alignment).

**A7.** RED = **0**, GREEN = **5**, BLUE = **6**. An enumerator without an initialiser is one more
than the previous. Verified.

**A8.** **NULL.** `fclose(NULL)` is **undefined behaviour** — check the return before using it.

**A9.** `feof` becomes true only **after** a read has already failed. The loop therefore performs one
extra iteration in which `fgets` fails, leaving `buf` unchanged, and the previous record is counted
or processed a second time. Verified: after reading 2 of 2 lines, `feof` is 1 only once the third
`fgets` has failed. Test the **read's** return value instead.

**A10.** A **base case** that terminates, and a **recursive case that provably moves toward it**.

**A11.** **21,891.** The formula is **2·fib(n+1) − 1**; fib(21) = 10,946.

**A12.** **φ ≈ 1.618**, the golden ratio — the growth is Θ(φⁿ).

**A13.** **Doubling** gives amortised O(1) (total copying < 2n). **Fixed increment** gives Θ(n²).

**A14.** **Reads of uninitialised memory.** ASan does not detect them; Valgrind reports
`Conditional jump or move depends on uninitialised value(s)`.

**A15.** `N bytes in 1 blocks are definitely lost in loss record 1 of 1`.

---

### Section B

**B1 (7 pts).** Nothing is printed. **10 bytes leak.**

`a = b` overwrites the only pointer to the first block, which becomes unreachable. `free(a)` then
frees the *second* block (since `a` and `b` now alias it). Valgrind reports
`10 bytes in 1 blocks are definitely lost`. Note `b` is also left dangling.

*4 pts for the leak size, 3 for explaining that the surviving `free` released the wrong block.*

**B2 (6 pts).** **24 bytes.**

| Offset | Content |
|---|---|
| 0 | `a` (1 byte) |
| 1–7 | 7 padding — `double` needs 8-byte alignment |
| 8–15 | `b` |
| 16 | `c` |
| 17 | 1 padding — `short` needs 2-byte alignment |
| 18–19 | `d` |
| 20–23 | 4 trailing padding — size must be a multiple of 8 |

*The trailing padding is the part students miss: the struct's size must be a multiple of its
strictest member alignment so that arrays remain aligned.*

**B3 (6 pts).** Two related defects: the loop tests `feof` **before** reading, and `fgets`' return
value is ignored.

On the final iteration `fgets` fails, leaves `buf` untouched, and `n` is incremented anyway — so the
count is **one too high** and the last line's contents would be processed twice if used. Correct
form:

```c
while (fgets(buf, sizeof buf, f)) n++;
```

**B4 (6 pts).** `mystery(4)` = 4 · 3 · 2 · 1 = **24**. It computes **n factorial**. Verified:
`fact(10)` is 3,628,800. The base case `n <= 1` returns 1, which also makes `mystery(0)` return 1 —
correct for 0!.

---

### Section C

**C1 (9 pts).**

- **`malloc(sizeof p)` allocates 8 bytes** — the size of the *pointer*, not the struct. Must be
  `sizeof *p`. This is the exact reason the course teaches `sizeof *p`.
- **`malloc(strlen(name))` is one byte short** — no room for the terminator. `strcpy` then writes
  past the end.
- **Neither allocation is checked.**

```c
Person *make(const char *name, int age)
{
    Person *p = malloc(sizeof *p);
    if (!p) return NULL;
    size_t n = strlen(name) + 1;
    p->name = malloc(n);
    if (!p->name) { free(p); return NULL; }   /* unwind */
    memcpy(p->name, name, n);
    p->age = age;
    return p;
}
```

*3 pts each. The `free(p)` in the second failure branch is worth calling out — it is the error-path
leak from Lecture 2.*

**C2 (8 pts).**

- **`fopen`'s return is never checked.** If it fails, `fgets(…, NULL)` is undefined.
- **The error path leaks `f`.** If `malloc` fails, the function returns −1 with the file still open.

```c
FILE *f = fopen(path, "r");
if (!f) return -1;
char *buf = malloc(1024);
if (!buf) { fclose(f); return -1; }
```

*4 pts each. The second is the one most students miss, and it is the point of the question.*

**C3 (8 pts).**

- **`*cap *= 2` is 0 when the list is empty**, so `realloc(…, 0)` is called and the first write is out
  of bounds. Must be `*cap ? *cap * 2 : 4`.
- **`*arr = realloc(*arr, …)`** — the A2 bug. On failure the original leaks and `*arr` becomes NULL,
  and the very next line dereferences it.

```c
int add(int **arr, size_t *len, size_t *cap, int v)
{
    if (*len == *cap) {
        size_t nc = *cap ? *cap * 2 : 4;
        if (nc > SIZE_MAX / sizeof **arr) return -1;
        int *tmp = realloc(*arr, nc * sizeof **arr);
        if (!tmp) return -1;
        *arr = tmp; *cap = nc;
    }
    (*arr)[(*len)++] = v;
    return 0;
}
```

*Note the function must also gain a return value — a `void` grow cannot report failure. Award 2 bonus
marks within the 8 for spotting that.*

---

### Section D

**D1 (10 pts).**

```c
/* Returns a newly allocated Person, or NULL. CALLER MUST call person_free. */
Person *person_new(const char *name, int age)
{
    Person *p = malloc(sizeof *p);
    if (!p) return NULL;
    size_t n = strlen(name) + 1;
    p->name = malloc(n);
    if (!p->name) { free(p); return NULL; }
    memcpy(p->name, name, n);
    p->age = age;
    return p;
}

/* Frees *p and its contents, then sets *p to NULL. Safe if *p is already NULL. */
void person_free(Person **p)
{
    if (!p || !*p) return;
    free((*p)->name);     /* the owned string FIRST */
    free(*p);             /* then the struct        */
    *p = NULL;
}
```

*Marking: 2 for `sizeof *p`, 2 for `+1` and the copy, 2 for unwinding on the second failure, 2 for
freeing `name` **before** the struct, 2 for the ownership comment and `Person **`.*

**Freeing in the wrong order** — `free(*p)` then `free((*p)->name)` — is a use-after-free. It often
appears to work, which makes it worth naming explicitly.

**D2 (10 pts).**

```c
int sum_digits(long n)
{
    if (n < 0) n = -n;            /* see the caveat below */
    if (n < 10) return (int)n;    /* base case */
    return (int)(n % 10) + sum_digits(n / 10);
}
```

**Base case:** `n < 10`, i.e. a single digit, which returns itself. It handles `n == 0` correctly,
returning 0.

**Reachability:** each recursive call passes `n / 10`, which for `n >= 10` is strictly smaller and
non-negative, so the value decreases monotonically toward the base case and cannot skip it.

**The caveat worth full marks:** `n = -n` is **undefined for `LONG_MIN`**, whose magnitude exceeds
`LONG_MAX` (Week 1's two's-complement asymmetry). A fully correct version takes the remainder before
negating, or works in `unsigned long`:

```c
int sum_digits(long n)
{
    unsigned long m = (n < 0) ? -(unsigned long)n : (unsigned long)n;
    return m < 10 ? (int)m : (int)(m % 10) + sum_digits_u(m / 10);
}
```

*6 pts for a correct recursion with a stated, reachable base case; 4 for handling negatives, of
which 2 require noticing the `LONG_MIN` case.*

---

## Final Advice

**Name the tool.** Several questions ask what Valgrind or ASan reports; a specific message earns more
than "it would catch it".

**Check every allocation and every `fopen`** in code you write, even under time pressure. It is two
lines and it is where the marks are.

**On error paths, free what you already allocated.** C2 and C1 both turn on this.

Good luck.

---

*PROG 101 · Week 10 · Midterm 2 · © CSE Department*
