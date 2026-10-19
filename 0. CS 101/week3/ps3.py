#!/usr/bin/env python3
"""
ps3.py
CS 101 — Problem Set 3: Functions, Scope, and the Call Stack
Due Friday 23 October 2026, 17:00

Student: Adebayo Glover

Every function has a docstring and at least two assert tests.
Weeks 0-3 tools only: assert for preconditions; no dictionaries.
"""

# --- B1: Math Library -----------------------------------------------------------
def clamp(value, lo, hi):
    """Return value restricted to the closed interval [lo, hi]. Requires lo <= hi."""
    assert lo <= hi, "lo must not exceed hi"
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value

assert clamp(5, 0, 10) == 5
assert clamp(-3, 0, 10) == 0
assert clamp(15, 0, 10) == 10

def lerp(a, b, t):
    """Return the point a fraction t of the way from a to b. Requires 0 <= t <= 1."""
    assert 0 <= t <= 1, "t must be in [0, 1]"
    return a + (b - a) * t

assert lerp(0, 10, 0.5) == 5.0
assert lerp(0, 100, 0.25) == 25.0

def normalize(value, src_min, src_max, dst_min=0.0, dst_max=1.0):
    """Rescale value from [src_min, src_max] into [dst_min, dst_max], by calling lerp."""
    t = (value - src_min) / (src_max - src_min)
    return lerp(dst_min, dst_max, t)

assert normalize(75, 0, 100) == 0.75
assert normalize(75, 0, 100, 0, 10) == 7.5
assert normalize(50, 0, 100, 0, 1) == 0.5


# --- B2: Strings ----------------------------------------------------------------
def title_case(text):
    """Return text with each word's first letter upper case and the rest lower case."""
    words = text.split()
    result = []
    for w in words:
        result.append(w[0].upper() + w[1:].lower())
    return " ".join(result)

assert title_case("the quick brown FOX") == "The Quick Brown Fox"
assert title_case("HELLO world") == "Hello World"

def count_substring(text, sub):
    """Count non-overlapping occurrences of sub in text. Requires sub != "" and no .count()."""
    assert sub != "", "sub must not be empty"
    count = 0
    i = 0
    while i <= len(text) - len(sub):
        if text[i:i + len(sub)] == sub:
            count += 1
            i += len(sub)          # skip the whole match so occurrences never overlap
        else:
            i += 1
    return count

assert count_substring("ababab", "ab") == 3
assert count_substring("aaa", "aa") == 1
assert count_substring("abc", "z") == 0


# --- B3: Functions as Values ------------------------------------------------------
def apply_to_all(func, lst):
    """Return a new list holding func(x) for every x in lst."""
    result = []
    for x in lst:
        result.append(func(x))
    return result

assert apply_to_all(str.upper, ["hello", "world"]) == ["HELLO", "WORLD"]
assert apply_to_all(len, ["a", "bb", "ccc"]) == [1, 2, 3]

def keep_if(predicate, lst):
    """Return a new list of the elements x of lst for which predicate(x) is true."""
    result = []
    for x in lst:
        if predicate(x):
            result.append(x)
    return result

assert keep_if(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]) == [2, 4, 6]
assert keep_if(lambda x: x > 0, [-1, 0, 1, 2]) == [1, 2]


# --- B4: Decomposition — Grade Report ---------------------------------------------
assignments = [
    ("Problem Set 1", 87, 100, 0.30),
    ("Problem Set 2", 92, 100, 0.30),
    ("Midterm", 78, 100, 0.25),
    ("Lab Average", 95, 100, 0.10),
    ("Participation", 100, 100, 0.05),
]

def percentage(score, max_score):
    """Return the score as a percentage of max_score."""
    return score / max_score * 100

assert percentage(87, 100) == 87.0
assert percentage(1, 2) == 50.0

def contribution(score, max_score, weight):
    """Return one assignment's weighted contribution (percentage times weight)."""
    return percentage(score, max_score) * weight

assert round(contribution(87, 100, 0.30), 2) == 26.10
assert contribution(100, 100, 0.05) == 5.0

def weighted_average(assignments):
    """Return the sum of the contributions of all the assignments."""
    total = 0
    for name, score, max_score, weight in assignments:
        total += contribution(score, max_score, weight)
    return total

assert round(weighted_average(assignments), 2) == 87.70
assert weighted_average([("x", 50, 100, 1.0)]) == 50.0

def letter_grade(pct):
    """Return the letter grade for a percentage, using the course cutoffs."""
    cutoffs = [(93, "A"), (90, "A-"), (87, "B+"), (83, "B"), (80, "B-"),
               (77, "C+"), (73, "C"), (70, "C-"), (60, "D")]
    for cutoff, letter in cutoffs:
        if pct >= cutoff:
            return letter
    return "F"

assert letter_grade(93) == "A" and letter_grade(92.99) == "A-"
assert letter_grade(87) == "B+" and letter_grade(59.99) == "F"

def print_report(assignments):
    """Print a formatted grade report and the final weighted average and letter grade."""
    print(f"  {'Assignment':<18}{'Score':>6}{'Max':>6}{'Weight':>8}{'Contrib':>9}")
    for name, score, max_score, weight in assignments:
        print(f"  {name:<18}{score:>6}{max_score:>6}{weight:>8.1%}{contribution(score, max_score, weight):>8.2f}%")
    avg = weighted_average(assignments)
    print(f"  Weighted average: {avg:.2f}%   Letter grade: {letter_grade(avg)}")

print_report(assignments)

print("all asserts passed")
