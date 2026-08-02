# CS 101 Quiz 3
## Week 3, Wednesday: In-Class Assessment

**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 2 material: conditionals, while loops, for loops, loop invariants

---

### Question 1 (2 points)

What is the output? Trace carefully.

```python
total = 0
for i in range(1, 6):
    if i % 2 == 0:
        total += i
    else:
        total -= i
print(total)
```

Answer: _______________

Show your trace (briefly):

---

### Question 2 (2 points)

This loop is supposed to find the index of the first negative number in `lst`.
It has a bug. Identify it and write the corrected version.

```python
lst = [4, 7, -3, 2, -1]
i = 0
while lst[i] >= 0:
    i += 1
print(f"First negative at index {i}")
```

Bug: _______________

Fix:
```python


```

---

### Question 3 (2 points)

State the **loop invariant** for this loop:

```python
def product(lst):
    result = 1
    for x in lst:
        result *= x
    return result
```

Invariant (complete the sentence): "At the start of each iteration, `result` equals ..."

Then show that the **invariant + exit condition** proves the function is correct.

---

### Question 4 (2 points)

What does this print? (No trace needed — reason about it.)

```python
def mystery(n):
    count = 0
    while n > 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        count += 1
    return count

print(mystery(8))
```

Answer: _______________

What well-known sequence does `mystery` compute the length of?

---

### Question 5 (2 points)

Write a `for` loop (in Python) that prints the sum of all multiples of 3 or 5 that are less than 50. (This is Project Euler Problem 1, reduced to 50.)

```python



```

Expected answer: 543

---

**Total: 10 points**

---

## Answer Key (Instructor Copy)

**Q1:** Trace:
- i=1: odd → total = 0-1 = -1
- i=2: even → total = -1+2 = 1
- i=3: odd → total = 1-3 = -2
- i=4: even → total = -2+4 = 2
- i=5: odd → total = 2-5 = -3
Output: `-3`

**Q2:** Bug: if `lst` contains no negative numbers, `i` reaches `len(lst)` and `lst[i]` raises `IndexError`.
Fix:
```python
i = 0
while i < len(lst) and lst[i] >= 0:
    i += 1
if i < len(lst):
    print(f"First negative at index {i}")
else:
    print("No negative numbers found")
```

**Q3:**
Invariant: "At the start of each iteration, `result` equals the product of all elements in `lst` that have been processed so far (i.e., `lst[0] * lst[1] * ... * lst[k-1]` where k elements have been seen)."

At exit: k = len(lst), so result = product of all elements = correct return value. ✓

**Q4:** `mystery(8)`:
8 → 4 → 2 → 1 (3 steps)
Output: `3`
This computes the Collatz sequence length.

**Q5:**
```python
total = 0
for n in range(1, 50):
    if n % 3 == 0 or n % 5 == 0:
        total += n
print(total)   # 543
```

---

*CS 101 · Week 3 · Quiz 3 · © CSE Department*
