# PROG 101 · Quiz 4
## Week 5, Tuesday — In-Class Assessment

**Date:** Tuesday 27 October 2026 · 10:00–10:10 (start of Week 5, Lecture 1)
**Duration:** 10 minutes · **Format:** Written, closed book
**Covers:** Week 4 — arrays, strings, buffer safety

---

### Question 1 (2 points)

For `int a[10]` declared in `main`, state `sizeof a`. Then state what `sizeof a` gives inside
`void f(int a[10])`, and name the mechanism responsible.

&nbsp;

&nbsp;

---

### Question 2 (2 points)

For `char s[] = "Hi!";` give `sizeof s` and `strlen(s)`, and explain in one sentence why they differ.

&nbsp;

&nbsp;

---

### Question 3 (2 points)

`strncpy(dst, src, n)` is often described as "safe `strcpy`". Give the **two** distinct ways this is
misleading.

&nbsp;

&nbsp;

---

### Question 4 (2 points)

```c
int n = snprintf(dst, cap, "%s", src);
```

(a) What does `n` hold?

(b) Write the correct test for truncation, and say why a cast is needed.

&nbsp;

&nbsp;

---

### Question 5 (2 points)

Name **one** function from `<string.h>` that must never be used and why, and give its replacement.

&nbsp;

&nbsp;

---

**Total: 10 points**

## Answer Key (Instructor Copy)

Checked with gcc 13.3 on x86-64.

**1.** `40` in `main`; `8` inside `f` — the parameter `int a[10]` is adjusted to `int *a`
(**array-to-pointer decay**), so `sizeof` measures the pointer.

**2.** `sizeof s` is `4`, `strlen(s)` is `3`: the array holds the terminating `'\0'`, which `strlen` does not count.

**3.** It does not terminate `dst` when `src` is `n` bytes or longer, and it zero-pads all the way to `n` when
`src` is short (wasted work, and it hides the length).

**4.** (a) the length the full output **would** have had, not counting the terminator — e.g. `snprintf` of
`"Hello"` into 4 bytes returns `5` and stores `"Hel"`. (b) `if (n < 0 || n >= (int)cap)` means truncated or failed;
the cast avoids comparing a signed `int` with an unsigned `size_t`, where a negative `n` would become huge.

**5.** `gets` (no length limit; removed in C11) → `fgets`; or `strcpy`/`strcat`/`sprintf` → `snprintf`.

*PROG 101 · Week 5 · Quiz 4 · © CSE Department*
