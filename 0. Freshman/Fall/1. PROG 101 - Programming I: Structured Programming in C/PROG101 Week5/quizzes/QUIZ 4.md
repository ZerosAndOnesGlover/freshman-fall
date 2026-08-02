# PROG 101 — Quiz 4
## Week 5, Tuesday — In-Class Assessment

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

`&a` and `&a[0]` print the same address. State how many bytes `a + 1` and `&a + 1` advance for
`int a[10]`, and explain the difference in one sentence.

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

*PROG 101 · Week 5 · Quiz 4 · © CSE Department*
