#!/usr/bin/env python3
"""
sorting_counts.py — CS 101 Lab 5 (Tuesday 3 November 2026)
Each sort returns (sorted_copy, comparisons, swaps), as in L17 §7.
"""
import random


def selection_sort(lst):
    # TODO: return (sorted_copy, comparisons, swaps)
    pass



def insertion_sort(lst):
    # TODO: return (sorted_copy, comparisons, swaps)
    pass



def bubble_sort(lst):
    # TODO: return (sorted_copy, comparisons, swaps)
    pass



def merge_sort(lst):
    """Returns (sorted_copy, comparisons, 0): merge sort moves items but never swaps."""
    # TODO: return (sorted_copy, comparisons, swaps)
    pass



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

    # Part 2 runs once Part 1 passes
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
