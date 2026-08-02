# PROG 101 · Quiz 11
## Week 12, Tuesday — In-Class Assessment

**Duration:** 10 minutes · **Format:** Written, closed book
**Covers:** Week 11 — function pointers and generic programming

---

### Question 1 (2 points)

State the difference between `int *f(int);` and `int (*p)(int);`.

&nbsp;

&nbsp;

---

### Question 2 (2 points)

```c
int cmp(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
```

Name the defect, give an input pair that triggers it, and state the correct idiom.

&nbsp;

&nbsp;

---

### Question 3 (2 points)

`qsort` takes four parameters. Three exist to replace information destroyed by `void *`. Name them
and say what each replaces.

&nbsp;

&nbsp;

---

### Question 4 (2 points)

An array of `char *` is sorted with `qsort`. What is the static type of the pointer the comparator
receives, and how do you obtain the string from it?

&nbsp;

&nbsp;

---

### Question 5 (2 points)

A function pointer captures nothing. State what C uses instead, and one concrete problem you would
face without it.

&nbsp;

&nbsp;

---

**Total: 10 points**

*PROG 101 · Week 12 · Quiz 11 · © CSE Department*
