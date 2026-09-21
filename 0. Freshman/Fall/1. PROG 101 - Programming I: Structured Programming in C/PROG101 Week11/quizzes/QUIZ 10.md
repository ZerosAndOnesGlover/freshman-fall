# PROG 101 · Quiz 10
## Week 11, Tuesday — In-Class Assessment

**Duration:** 10 minutes · **Format:** Written, closed book
**Date:** Tuesday 8 December 2026 · 10:00–10:10 (start of Week 11, Lecture 1)
**Covers:** Week 10 — the preprocessor and macros

---

### Question 1 (2 points)

`#define SQUARE(x) x * x`. Give the value of `SQUARE(2 + 3)` and of `100 / SQUARE(5)`, and state the
**two distinct** fixes needed.

&nbsp;

&nbsp;

---

### Question 2 (2 points)

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
int i = 5;
int m = MAX(i++, 3);
```

State the final value of `i`, name the defect, and explain why parentheses cannot fix it.

&nbsp;

&nbsp;

---

### Question 3 (2 points)

Why must a multi-statement macro be wrapped in `do { ... } while (0)`? State what breaks without it,
and why a bare `{ ... }` block is not enough.

&nbsp;

&nbsp;

---

### Question 4 (2 points)

Given `#define VERSION 42`, state what `STR(VERSION)` and `XSTR(VERSION)` produce, where
`#define STR(x) #x` and `#define XSTR(x) STR(x)`. Explain the difference.

&nbsp;

&nbsp;

---

### Question 5 (2 points)

Name **one** thing that belongs in a header and **one** that must not, and say what goes wrong when
the second is put there anyway — including at which pipeline stage it fails.

&nbsp;

&nbsp;

---

**Total: 10 points**

*PROG 101 · Week 11 · Quiz 10 · © CSE Department*
