# CS 101 · Week 5
## LAB 5 Solutions: INSTRUCTOR ONLY

> Lab sat Tuesday 3 November 2026. **All code below was executed; the tables are real output.**
> The random rows vary from run to run; the sorted and reversed rows are exact.

---

## Part 1 — Reference `sorting_counts.py` (30)

```python
#!/usr/bin/env python3
"""
sorting_counts.py — CS 101 Lab 5 (Tuesday 3 November 2026)
Each sort returns (sorted_copy, comparisons, swaps), as in L17 §7.
"""
import random


def selection_sort(lst):
    a = lst[:]
    comparisons = swaps = 0
    for i in range(len(a)):
        smallest = i
        for j in range(i + 1, len(a)):
            comparisons += 1
            if a[j] < a[smallest]:
                smallest = j
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]
            swaps += 1
    return a, comparisons, swaps


def insertion_sort(lst):
    a = lst[:]
    comparisons = swaps = 0
    for i in range(1, len(a)):
        j = i
        while j > 0:
            comparisons += 1
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                swaps += 1
                j -= 1
            else:
                break
    return a, comparisons, swaps


def bubble_sort(lst):
    a = lst[:]
    comparisons = swaps = 0
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for j in range(end):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:          # early exit (L17 §3)
            break
    return a, comparisons, swaps


def merge_sort(lst):
    """Returns (sorted_copy, comparisons, 0): merge sort moves items but never swaps."""
    if len(lst) <= 1:
        return lst[:], 0, 0
    mid = len(lst) // 2
    left, c1, _ = merge_sort(lst[:mid])
    right, c2, _ = merge_sort(lst[mid:])
    result = []
    comparisons = c1 + c2
    i = j = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:], comparisons, 0


ALGORITHMS = [("selection", selection_sort), ("insertion", insertion_sort),
              ("bubble", bubble_sort), ("merge", merge_sort)]

if __name__ == "__main__":
    # Part 1: correctness
    tests = [[], [1], [2, 1], [3, 1, 2], [5, 5, 1, 5], [4, 3, 2, 1], [1, 2, 3, 4]]
    for name, sort in ALGORITHMS:
        for t in tests:
            assert sort(t)[0] == sorted(t), (name, t)
        for _ in range(100):
            data = [random.randint(-50, 50) for _ in range(30)]
            assert sort(data)[0] == sorted(data), name
    print("Part 1: all four sorts correct")

    # Part 2: comparisons as n doubles, on sorted / reversed / random input
    print(f"\n{'n':>5} {'input':>9}" + "".join(f"{name:>11}" for name, _ in ALGORITHMS))
    for n in [100, 200, 400, 800]:
        inputs = [("sorted", list(range(n))), ("reversed", list(range(n, 0, -1))),
                  ("random", [random.randint(0, 10 * n) for _ in range(n)])]
        for label, data in inputs:
            row = f"{n:>5} {label:>9}"
            for name, sort in ALGORITHMS:
                row += f"{sort(data)[1]:>11}"
            print(row)

    # Part 3: swaps on reversed input
    n = 100
    data = list(range(n, 0, -1))
    print(f"\nswaps on reversed n={n}: " + ", ".join(f"{name} {sort(data)[2]}" for name, sort in ALGORITHMS[:3]))
```

## Part 2 — Growth (35)

```
    n     input  selection  insertion     bubble      merge
  100    sorted       4950         99         99        316
  100  reversed       4950       4950       4950        356
  100    random       4950       2587       4944        543
  200    sorted      19900        199        199        732
  200  reversed      19900      19900      19900        812
  200    random      19900      10568      19600       1298
  400    sorted      79800        399        399       1664
  400  reversed      79800      79800      79800       1824
  400    random      79800      43008      79097       2962
  800    sorted     319600        799        799       3728
  800  reversed     319600     319600     319600       4048
  800    random     319600     152267     319464       6731
```

1. Selection sort: always `n(n−1)/2` (4950 at 100). 2. `n − 1`: each inner loop stops after one
failed comparison (insertion) / one pass with no swaps (bubble). 3. Selection, and insertion/bubble on
reversed or random input, grow ×4 per doubling; merge sort by a bit more than ×2 (the extra `log₂ n`
factor); the sorted-input rows for insertion/bubble ×2. Random insertion is about half of reversed —
on average each item moves halfway. 4. Merge sort splits and merges regardless of order; on sorted input
each merge ends when the left half runs out, which halves the comparisons but cannot skip the work.

*Up to 8 for the table, 27 for the four answers — each must cite numbers from the table.*

## Part 3 — Swaps (15)

`selection 50, insertion 4950, bubble 4950` on reversed `n = 100`. Selection sort's first pass swaps
`100` with `1`, which also puts `1` in place; each swap fixes **two** positions, so the second half of the
passes find `smallest == i` and swap nothing: `n/2`. When moving a record is expensive, selection sort's
≤ `n − 1` swaps beat the quadratic swaps of the others.

## Part 4 — Stability (20)

Selection sort: pass 1 finds `(1, "Cal")` at index 2 and swaps it with index 0 →
`[(1,"Cal"), (2,"Bob"), (2,"Ann")]` — **Bob now before Ann: unstable**. Insertion sort: `(2,"Bob")` is
not less than `(2,"Ann")` by grade, stays; `(1,"Cal")` moves left past both →
`[(1,"Cal"), (2,"Ann"), (2,"Bob")]` — **stable**. Rule: insertion sort only swaps **adjacent** items
that are strictly out of order, so equal keys never pass each other; selection sort's long-distance
swap can jump an item over its equal.

---

*CS 101 · Week 5 · Lab 5 Solutions · Instructor only*
