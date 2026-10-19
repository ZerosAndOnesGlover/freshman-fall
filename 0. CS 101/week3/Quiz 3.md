---
assessment: Quiz 3
course: CS 101
component: Quizzes
possible: 10
score: 10
status: graded
started: 2026-10-14
submitted: 2026-10-14
graded: 2026-10-14
source: "QUIZ 3 Week 3 Wednesday.md"
---

# CS 101 · Quiz 3
## Answer Sheet

**Assessment:** `QUIZ 3 Week 3 Wednesday.md`
**Points available:** 10

---

**Q1 (2 pts).**

```python
total = 0
for i in range(1, 6):
    if i % 2 == 0:
        total += i
    else:
        total -= i
print(total)
```

Trace: `i=1` odd → `-1`; `i=2` even → `1`; `i=3` odd → `-2`; `i=4` even → `2`; `i=5` odd → `-3`.

**Output:** `-3`

*Marks: 2 / 2*

---

**Q2 (2 pts). Bug.**

The loop has no bound check: if `lst` contains **no** negative number, `i` reaches `len(lst)` and
`lst[i]` raises `IndexError`.

**Fix:**

```python
i = 0
while i < len(lst) and lst[i] >= 0:
    i += 1
if i < len(lst):
    print(f"First negative at index {i}")
else:
    print("No negative numbers found")
```

*Marks: 2 / 2*

---

**Q3 (2 pts). Invariant.**

"At the start of each iteration, `result` equals the **product of all elements of `lst` that have
been processed so far** — that is, `lst[0] * lst[1] * … * lst[k-1]` where `k` elements have been
processed."

**Invariant + exit → postcondition:** the `for` loop ends when all `len(lst)` elements have been
processed, so `k = len(lst)` and `result` is the product of the entire list — which is exactly what
`print(result)` outputs (here `60`).

*Marks: 2 / 2*

---

**Q4 (2 pts).** `n = 8`:

`8 → 4 → 2 → 1`, which is 3 steps.

**Output:** `3`

The loop computes the length of the **Collatz sequence** (the number of steps for `n` to reach 1).

*Marks: 2 / 2*

---

**Q5 (2 pts).** Sum of multiples of 3 or 5 below 50:

```python
total = 0
for n in range(1, 50):
    if n % 3 == 0 or n % 5 == 0:
        total += n
print(total)   # 543
```

*Marks: 2 / 2*

---

## Grading Summary

| | |
|---|---|
| **Score** | 10 / 10 |
| **Percent** | 100% |
| **Graded** | 2026-10-14 |

**Feedback:**
All correct per the answer key. Q1 traces to `-3`. Q2 names the out-of-range access (`IndexError`) when
there is no negative and fixes it with a bound check plus a "not found" branch. Q3 states the
partial-product invariant and connects the exit condition to the printed product. Q4 gives `3` and
names the Collatz sequence. Q5 sums to `543` with the `or` test.
