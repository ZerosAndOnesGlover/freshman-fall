# PROG 101 · Quiz 5
## Week 6, Tuesday — In-Class Assessment

**Date:** Tuesday 3 November 2026 · 10:00–10:10 (start of Week 6, Lecture 1)
**Duration:** 10 minutes · **Format:** Written, closed book
**Covers:** Week 5 — pointers, pointer arithmetic, `const`, NULL

---

### Question 1 (2 points)

`sizeof(char *)` and `sizeof(double *)` are both 8. Give **two** things the pointer's type *does*
control.

&nbsp;

&nbsp;

---

### Question 2 (2 points)

For `int a[10]`, state how many **bytes** each advances, and why they differ:

(a) `a + 1`   (b) `&a + 1`

&nbsp;

&nbsp;

---

### Question 3 (2 points)

```c
void f(int a, int b) { int t = a; a = b; b = t; }
```

State why this cannot swap the caller's variables, and give the corrected signature.

&nbsp;

&nbsp;

---

### Question 4 (2 points)

For each, say whether it compiles:

(a) `const int *p = &x; p = &y;`
(b) `const int *p = &x; *p = 5;`
(c) `int *const p = &x; p = &y;`
(d) `int *const p = &x; *p = 5;`

&nbsp;

&nbsp;

---

### Question 5 (2 points)

```c
int *f(void) { int local = 42; return &local; }
```

Name the defect, and state what GCC actually compiles this function to return.

&nbsp;

&nbsp;

---

**Total: 10 points**

## Answer Key (Instructor Copy)

**1.** What `*p` reads or writes (how many bytes, interpreted how), and how far `p + 1` moves.

**2.** (a) `4` bytes — one `int`; (b) `40` bytes — one whole `int[10]`. `&a` has type `int (*)[10]`, and
pointer arithmetic scales by the pointed-to type.

**3.** `a` and `b` are copies in `f`'s frame. `void swap(int *a, int *b)`, called as `swap(&x, &y)`.

**4.** (a) compiles (b) error: assignment of read-only location (c) error: assignment of read-only variable
(d) compiles.

**5.** Returning the address of a local — dangling. gcc 13 warns (`-Wreturn-local-addr`) and compiles the
function to return **NULL** (verified: the caller prints `(nil)`), so the bug shows up as a null dereference
far from its cause.

*PROG 101 · Week 6 · Quiz 5 · © CSE Department*
