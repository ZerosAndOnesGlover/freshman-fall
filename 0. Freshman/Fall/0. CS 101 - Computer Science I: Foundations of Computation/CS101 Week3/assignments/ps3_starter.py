#!/usr/bin/env python3
"""
ps3.py
CS 101 — Problem Set 3: Functions, Scope, and the Call Stack

Student: ____________________________
Date: ______________________________

Honor pledge: I wrote this code myself and understand every line.
Signed: ____________________________
"""

import math
import time


# ══════════════════════════════════════════════════════════════════════════════
# B1: Mathematical Functions Library
# ══════════════════════════════════════════════════════════════════════════════

def clamp(value, lo, hi):
    """
    Restrict value to the closed interval [lo, hi].

    Args:
        value: the number to clamp
        lo:    lower bound
        hi:    upper bound (must be >= lo)

    Returns:
        lo if value < lo; hi if value > hi; value otherwise

    Raises:
        ValueError if lo > hi

    Examples:
        clamp(5, 0, 10)   → 5
        clamp(-3, 0, 10)  → 0
        clamp(15, 0, 10)  → 10
    """
    if lo > hi:
        raise ValueError(f"lo={lo} must be <= hi={hi}")
    # TODO
    pass


assert clamp(5, 0, 10) == 5,  f"clamp mid: {clamp(5,0,10)}"
assert clamp(-3, 0, 10) == 0, f"clamp low: {clamp(-3,0,10)}"
assert clamp(15, 0, 10) == 10, f"clamp high: {clamp(15,0,10)}"


def lerp(a, b, t):
    """
    Linearly interpolate between a and b by fraction t.
    t=0.0 returns a; t=1.0 returns b; t=0.5 returns the midpoint.

    Args:
        a (float): start value
        b (float): end value
        t (float): interpolation fraction, must be in [0.0, 1.0]

    Returns:
        float: a + (b - a) * t

    Raises:
        ValueError if t < 0 or t > 1

    Examples:
        lerp(0, 10, 0.5)   → 5.0
        lerp(0, 100, 0.25) → 25.0
        lerp(10, 20, 0.0)  → 10.0
    """
    if not (0.0 <= t <= 1.0):
        raise ValueError(f"t={t} must be in [0.0, 1.0]")
    # TODO
    pass


assert lerp(0, 10, 0.5) == 5.0
assert lerp(0, 100, 0.25) == 25.0


def normalize(value, src_min, src_max, dst_min=0.0, dst_max=1.0):
    """
    Rescale value from [src_min, src_max] to [dst_min, dst_max].
    Uses lerp internally.

    Examples:
        normalize(75, 0, 100)          → 0.75
        normalize(75, 0, 100, 0, 10)   → 7.5
        normalize(50, 0, 200, -1, 1)   → 0.0
    """
    # TODO: compute t = where value falls in [src_min, src_max], then lerp
    pass


assert normalize(75, 0, 100) == 0.75
assert normalize(75, 0, 100, 0, 10) == 7.5


def smooth_step(t):
    """
    Smooth interpolation curve: 3t² - 2t³.
    Has zero derivative (slope) at t=0 and t=1 — useful for animations.

    Args:
        t (float): value in [0.0, 1.0]

    Returns:
        float: 3*t**2 - 2*t**3

    Examples:
        smooth_step(0.0) → 0.0
        smooth_step(0.5) → 0.5
        smooth_step(1.0) → 1.0
    """
    # TODO
    pass


assert smooth_step(0.0) == 0.0
assert smooth_step(1.0) == 1.0
assert abs(smooth_step(0.5) - 0.5) < 1e-9


def map_range(value, src_min, src_max, dst_min, dst_max):
    """
    Map value from [src_min, src_max] to [dst_min, dst_max],
    clamping the result to [dst_min, dst_max].

    Examples:
        map_range(50, 0, 100, 0, 255)    → 127.5
        map_range(150, 0, 100, 0, 255)   → 255   (clamped)
        map_range(-10, 0, 100, 0, 255)   → 0     (clamped)
    """
    # TODO: normalize, then lerp, then clamp
    pass


assert map_range(50, 0, 100, 0, 255) == 127.5
assert map_range(150, 0, 100, 0, 255) == 255


def moving_average(data, window):
    """
    Compute the moving average of data with the given window size.
    Returns a list of length len(data) - window + 1.

    Args:
        data   (list of float): the input data
        window (int):           window size, must be >= 1 and <= len(data)

    Returns:
        list of float: moving averages

    Examples:
        moving_average([1, 2, 3, 4, 5], 3) → [2.0, 3.0, 4.0]
        moving_average([1, 2, 3], 1)        → [1.0, 2.0, 3.0]
        moving_average([1, 2, 3], 3)        → [2.0]
    """
    assert 1 <= window <= len(data), f"window={window} out of range"
    # TODO: for loop; each window is data[i:i+window]
    pass


assert moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
assert moving_average([1, 2, 3], 3) == [2.0]


# ══════════════════════════════════════════════════════════════════════════════
# B2: String Processing Functions
# ══════════════════════════════════════════════════════════════════════════════

def title_case(text):
    """
    Convert text to title case without using str.title().
    Each word: first letter uppercase, rest lowercase.

    Examples:
        title_case("the quick brown FOX") → "The Quick Brown Fox"
        title_case("")                    → ""
    """
    words = text.split()
    # TODO: capitalize each word: word[0].upper() + word[1:].lower()
    pass


assert title_case("the quick brown FOX") == "The Quick Brown Fox"
assert title_case("") == ""


def wrap_text(text, width):
    """
    Wrap text at word boundaries so no line exceeds width characters.
    Returns a list of lines.
    Words longer than width appear alone on their own line.

    Examples:
        wrap_text("The quick brown fox", 10) → ["The quick", "brown fox"]
        wrap_text("superlongword hi", 5)     → ["superlongword", "hi"]
    """
    words = text.split()
    if not words:
        return []
    lines  = []
    current = words[0]
    # TODO: for each subsequent word:
    #   if adding it (with a space) keeps the line <= width: add it
    #   else: append current line to lines, start new current = word
    # After loop: append final current line
    pass


assert wrap_text("The quick brown fox", 10) == ["The quick", "brown fox"]
assert wrap_text("a", 10) == ["a"]


def justify_line(text, width):
    """
    Pad spaces between words so the line is exactly width characters.
    Extra spaces are distributed left-to-right.
    If only one word (or text already >= width), left-align (no change).

    Examples:
        justify_line("Hello world", 20) → "Hello          world"
        justify_line("one two three", 17) → "one   two   three"
    """
    words = text.split()
    if len(words) <= 1:
        return text.ljust(width)
    gaps = len(words) - 1
    total_spaces = width - sum(len(w) for w in words)
    # TODO: distribute total_spaces across gaps
    # base = total_spaces // gaps; extra = total_spaces % gaps
    # first 'extra' gaps get base+1 spaces, rest get base spaces
    pass


assert len(justify_line("Hello world", 20)) == 20
assert justify_line("Hello world", 20).startswith("Hello")
assert justify_line("Hello world", 20).endswith("world")


def count_substring(text, sub):
    """
    Count non-overlapping occurrences of sub in text.
    Do NOT use str.count().

    Examples:
        count_substring("ababab", "ab")  → 3
        count_substring("aaa", "aa")     → 1  (non-overlapping)
        count_substring("hello", "xyz")  → 0
    """
    if not sub:
        return 0
    count = 0
    i = 0
    # TODO: while loop: search for sub starting at i
    #   if found at position j: count += 1; i = j + len(sub)
    #   else: break
    pass


assert count_substring("ababab", "ab") == 3
assert count_substring("aaa", "aa") == 1
assert count_substring("hello", "xyz") == 0


def compress(text):
    """
    Compress runs of 3+ identical characters to "count:char".
    Runs of 1 or 2 are left unchanged.

    Examples:
        compress("aaabbbccccdd") → "3:a3:b4:cdd"

        Wait — let's be precise:
        "aaa"   → "3:a"
        "bb"    → "bb"   (only 2 — unchanged)
        "cccc"  → "4:c"
        "dd"    → "dd"   (only 2 — unchanged)
        So: compress("aaabbbccccdd") → "3:abbb4:cdd"

        Hmm — "bbb" is 3 b's → "3:b". Let's recheck:
        "aaa"  (3) → "3:a"
        "bbb"  (3) → "3:b"
        "cccc" (4) → "4:c"
        "dd"   (2) → "dd"
        → "3:a3:b4:cdd"

        compress("hello")  → "hello"    (no run of 3+)
        compress("aaaa")   → "4:a"
        compress("")       → ""
    """
    if not text:
        return ""
    result = ""
    i = 0
    # TODO: walk text with while loop
    # Count run length for each character
    # If run >= 3: append f"{count}:{char}"
    # Else: append char * count
    pass


assert compress("aaabbbccccdd") == "3:a3:b4:cdd"
assert compress("hello") == "hello"
assert compress("aaaa") == "4:a"
assert compress("") == ""


# ══════════════════════════════════════════════════════════════════════════════
# B3: Higher-Order Functions
# ══════════════════════════════════════════════════════════════════════════════

def apply_to_all(func, lst):
    """
    Return a new list with func applied to each element of lst.

    Examples:
        apply_to_all(str.upper, ["hello", "world"]) → ["HELLO", "WORLD"]
        apply_to_all(lambda x: x**2, [1, 2, 3])    → [1, 4, 9]
    """
    # TODO
    pass


assert apply_to_all(str.upper, ["hello", "world"]) == ["HELLO", "WORLD"]
assert apply_to_all(lambda x: x**2, [1, 2, 3]) == [1, 4, 9]


def keep_if(predicate, lst):
    """
    Return a new list containing only elements where predicate(element) is True.

    Examples:
        keep_if(lambda x: x % 2 == 0, [1,2,3,4,5,6]) → [2, 4, 6]
        keep_if(str.isupper, ["Hello", "WORLD", "hi"]) → ["WORLD"]
    """
    # TODO
    pass


assert keep_if(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]) == [2, 4, 6]


def reduce_with(func, lst, initial):
    """
    Combine all elements of lst using func, starting from initial.
    reduce_with(f, [a,b,c], init) = f(f(f(init, a), b), c)

    Examples:
        reduce_with(lambda a, b: a + b, [1,2,3,4], 0) → 10
        reduce_with(lambda a, b: a * b, [1,2,3,4], 1) → 24
        reduce_with(lambda a, b: a + b, [], 0)         → 0
    """
    # TODO
    pass


assert reduce_with(lambda a, b: a + b, [1, 2, 3, 4], 0) == 10
assert reduce_with(lambda a, b: a * b, [1, 2, 3, 4], 1) == 24
assert reduce_with(lambda a, b: a + b, [], 0) == 0


def compose(f, g):
    """
    Return a new function h such that h(x) = f(g(x)).

    Examples:
        double_then_square = compose(lambda x: x**2, lambda x: x*2)
        double_then_square(3) → 36   (3*2=6, 6**2=36)
    """
    # TODO: return a lambda or nested function
    pass


double_then_square = compose(lambda x: x**2, lambda x: x * 2)
assert double_then_square(3) == 36
assert double_then_square(5) == 100


def memoize(func):
    """
    Return a new function that caches results of func.
    The first call with argument x computes func(x) and stores it.
    Subsequent calls with the same x return the cached result immediately.

    Demonstrate with a slow function that the second call is fast.

    Hint: store results in a dict (cache) inside the closure.
    """
    cache = {}

    def memoized(x):
        # TODO: if x in cache, return cache[x]
        # else: compute func(x), store in cache[x], return it
        pass

    return memoized


# Demonstration:
def slow_square(x):
    time.sleep(0.05)   # simulate slow computation
    return x * x

fast_square = memoize(slow_square)
t0 = time.time(); fast_square(10); t1 = time.time()
t2 = time.time(); fast_square(10); t3 = time.time()
assert fast_square(10) == 100
assert (t3 - t2) < (t1 - t0) * 0.1, "Memoized call should be much faster"
print("✓ memoize (second call was faster)")


# ══════════════════════════════════════════════════════════════════════════════
# B4: Grade Calculator
# ══════════════════════════════════════════════════════════════════════════════

def percentage(score, max_score):
    """Return score as a percentage of max_score (0–100 scale)."""
    # TODO
    pass

def weighted_score(score, max_score, weight):
    """Return the weighted contribution: percentage * weight."""
    # TODO
    pass

def weighted_average(assignments):
    """
    Return the overall weighted percentage for a list of
    (name, score, max_score, weight) tuples.
    """
    # TODO: sum weighted_score for each assignment
    pass

def letter_grade(pct):
    """
    Convert a percentage to a letter grade.
    A: 93+, A-: 90+, B+: 87+, B: 83+, B-: 80+,
    C+: 77+, C: 73+, C-: 70+, D: 60+, F: below 60
    """
    # TODO: if/elif chain
    pass

def grade_points(letter):
    """
    Return GPA points for a letter grade.
    A=4.0, A-=3.7, B+=3.3, B=3.0, B-=2.7,
    C+=2.3, C=2.0, C-=1.7, D=1.0, F=0.0
    """
    scale = {
        "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7, "D": 1.0, "F": 0.0,
    }
    return scale.get(letter, 0.0)

def format_assignment_row(name, score, max_score, weight, contribution):
    """
    Return a single formatted row for the report table.
    Columns: name (left, 22 chars), score (right, 5), max (right, 4),
             weight% (right, 7), contribution% (right, 8)
    """
    # TODO: f-string with fixed widths
    pass

def print_grade_report(assignments):
    """
    Print the complete formatted grade report.
    This is the only function in B4 that may call print().
    """
    avg    = weighted_average(assignments)
    grade  = letter_grade(avg)
    gpa    = grade_points(grade)

    border = "═" * 56
    div    = "─" * 56

    print(border)
    print("  GRADE REPORT")
    print(border)
    print(f"  {'Assignment':<22} {'Score':>5} {'Max':>4} {'Weight':>7} {'Contrib':>8}")
    print(f"  {div}")

    for name, score, max_score, weight in assignments:
        contrib = weighted_score(score, max_score, weight)
        row = format_assignment_row(name, score, max_score, weight * 100, contrib * 100)
        print(f"  {row}")

    print(f"  {div}")
    print(f"  {'Weighted Average:':<42} {avg:>7.2f}%")
    print(f"  {'Letter Grade:':<42} {grade:>8}")
    print(f"  {'GPA Points:':<42} {gpa:>8.1f}")
    print(border)


# Quick sanity tests:
assert abs(percentage(87, 100) - 87.0) < 1e-9
assert letter_grade(87.7) == "B+"
assert grade_points("B+") == 3.3

# Demonstration:
_sample_assignments = [
    ("Problem Set 1",  87,  100, 0.30),
    ("Problem Set 2",  92,  100, 0.30),
    ("Midterm",        78,  100, 0.25),
    ("Lab Average",    95,  100, 0.10),
    ("Participation", 100,  100, 0.05),
]
print_grade_report(_sample_assignments)


# ══════════════════════════════════════════════════════════════════════════════
# B5: Recursive Functions
# ══════════════════════════════════════════════════════════════════════════════

def power(base, exp):
    """
    Compute base**exp for non-negative integer exp, recursively.

    Base case:    power(base, 0) = 1
    Inductive step: power(base, exp) = base * power(base, exp - 1)

    Why correct: by induction, power(base, k) = base^k for all k >= 0.
    """
    assert isinstance(exp, int) and exp >= 0
    # TODO
    pass


assert power(2, 0)  == 1
assert power(2, 10) == 1024
assert power(3, 4)  == 81


def gcd_recursive(a, b):
    """
    Compute gcd(a, b) using the Euclidean algorithm, recursively.

    Base case:    gcd(a, 0) = a
    Inductive step: gcd(a, b) = gcd(b, a % b)

    Correctness: gcd(a, b) = gcd(b, a%b) because any common divisor of
    a and b also divides a%b = a - (a//b)*b, and vice versa.
    """
    # TODO
    pass


assert gcd_recursive(48, 18) == 6
assert gcd_recursive(7, 13)  == 1
assert gcd_recursive(0, 5)   == 5


def flatten(lst):
    """
    Return a flat list of all non-list elements, recursively.

    Base case:    empty list → []
    Inductive step: if lst[0] is a list → flatten(lst[0]) + flatten(lst[1:])
                    else                → [lst[0]] + flatten(lst[1:])

    Examples:
        flatten([1, [2, [3, 4]], 5]) → [1, 2, 3, 4, 5]
        flatten([])                  → []
        flatten([[[1]]])             → [1]
    """
    # TODO
    pass


assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
assert flatten([]) == []
assert flatten([[[1]]]) == [1]


def binary_to_int(binary_str):
    """
    Convert a binary string to its integer value, recursively.

    Base case:    single character → int(char)
    Inductive step: binary_to_int(s) =
                    binary_to_int(s[:-1]) * 2 + int(s[-1])

    Examples:
        binary_to_int("0")   → 0
        binary_to_int("1")   → 1
        binary_to_int("101") → 5
        binary_to_int("1111") → 15
    """
    assert all(c in "01" for c in binary_str), "Not a binary string"
    # TODO
    pass


assert binary_to_int("0")    == 0
assert binary_to_int("1")    == 1
assert binary_to_int("101")  == 5
assert binary_to_int("1111") == 15


def merge_sorted(lst1, lst2):
    """
    Merge two sorted lists into one sorted list, recursively.

    Base cases:   either list is empty → return the other
    Inductive step: compare first elements; take the smaller and
                    recurse on the remainder.

    Examples:
        merge_sorted([1, 3, 5], [2, 4, 6]) → [1, 2, 3, 4, 5, 6]
        merge_sorted([], [1, 2])            → [1, 2]
        merge_sorted([1], [])               → [1]
    """
    # TODO
    pass


assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
assert merge_sorted([], [1, 2]) == [1, 2]
assert merge_sorted([5], [1, 2, 3]) == [1, 2, 3, 5]


# ══════════════════════════════════════════════════════════════════════════════
# B6: Closures and Function Factories
# ══════════════════════════════════════════════════════════════════════════════

def make_counter(start=0, step=1):
    """
    Return a function that yields start, start+step, start+2*step, ...
    Each call advances by step.

    Examples:
        c = make_counter(10, 5)
        c() → 10
        c() → 15
        c() → 20

        c2 = make_counter()   # defaults: start=0, step=1
        c2() → 0
        c2() → 1
    """
    # Hint: store current value in a list (mutable container) to work
    # around the nonlocal requirement: current = [start]
    # then each call: val = current[0]; current[0] += step; return val
    current = [start]

    def counter():
        # TODO
        pass

    return counter


c = make_counter(10, 5)
assert c() == 10
assert c() == 15
assert c() == 20
c2 = make_counter()
assert c2() == 0
assert c2() == 1
print("✓ make_counter")


def make_validator(min_val, max_val, allow_none=False):
    """
    Return a validate(x) function that returns True if x is in [min_val, max_val],
    or (if allow_none=True) if x is None.

    Examples:
        validate_age = make_validator(0, 150)
        validate_age(25)   → True
        validate_age(-1)   → False
        validate_age(None) → False

        validate_opt = make_validator(0, 100, allow_none=True)
        validate_opt(None) → True
        validate_opt(50)   → True
    """
    def validate(x):
        # TODO
        pass
    return validate


validate_age = make_validator(0, 150)
assert validate_age(25)   == True
assert validate_age(-1)   == False
assert validate_age(None) == False
validate_opt = make_validator(0, 100, allow_none=True)
assert validate_opt(None) == True
assert validate_opt(50)   == True
print("✓ make_validator")


def make_pipeline(*funcs):
    """
    Return a function that applies funcs in sequence,
    passing each output as input to the next.

    Examples:
        process = make_pipeline(str.strip, str.lower, str.split)
        process("  Hello World  ") → ['hello', 'world']

        double_then_negate = make_pipeline(lambda x: x*2, lambda x: -x)
        double_then_negate(5) → -10
    """
    def pipeline(x):
        # TODO: apply each func in funcs to the running result
        pass
    return pipeline


process = make_pipeline(str.strip, str.lower, str.split)
assert process("  Hello World  ") == ['hello', 'world']
double_then_negate = make_pipeline(lambda x: x * 2, lambda x: -x)
assert double_then_negate(5) == -10
print("✓ make_pipeline")


def once(func):
    """
    Return a wrapper that calls func at most once.
    Subsequent calls return the first result without calling func again.

    Examples:
        call_count = [0]
        def counted():
            call_count[0] += 1
            return 42

        guarded = once(counted)
        guarded()   → 42  (counted called)
        guarded()   → 42  (counted NOT called again)
        assert call_count[0] == 1
    """
    # Hint: store [has_been_called, result] in a mutable container
    state = [False, None]

    def wrapper(*args, **kwargs):
        # TODO
        pass

    return wrapper


call_count = [0]
def _counted():
    call_count[0] += 1
    return 42

guarded = once(_counted)
assert guarded() == 42
assert guarded() == 42
assert call_count[0] == 1, f"func called {call_count[0]} times, expected 1"
print("✓ once")


# ══════════════════════════════════════════════════════════════════════════════
# B7: Polynomial Calculator
# ══════════════════════════════════════════════════════════════════════════════

def poly_eval(coeffs, x):
    """
    Evaluate polynomial at x.
    coeffs[i] is the coefficient of x^i.

    poly_eval([2, -3, 1], 2) = 2 - 3*2 + 1*4 = 2 - 6 + 4 = 0

    Use Horner's method for efficiency:
    a0 + x*(a1 + x*(a2 + x*a3))
    But a straightforward loop is fine for correctness.
    """
    # TODO
    pass


assert poly_eval([2, -3, 1], 2) == 0   # x^2 - 3x + 2 at x=2: 4-6+2=0
assert poly_eval([1], 100) == 1        # constant polynomial
assert poly_eval([0, 1], 5) == 5       # y = x at x=5


def poly_add(p, q):
    """
    Add two polynomials. Result length = max(len(p), len(q)).
    poly_add([1, 2], [3, 0, 1]) → [4, 2, 1]
    """
    length = max(len(p), len(q))
    # TODO: for each index i up to length:
    # result[i] = (p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0)
    pass


assert poly_add([1, 2], [3, 0, 1]) == [4, 2, 1]
assert poly_add([1], [0, 1])       == [1, 1]


def poly_scale(p, scalar):
    """
    Multiply polynomial by a scalar.
    poly_scale([1, 2, 3], 2) → [2, 4, 6]
    """
    # TODO
    pass


assert poly_scale([1, 2, 3], 2) == [2, 4, 6]
assert poly_scale([1, 2], 0)    == [0, 0]


def poly_multiply(p, q):
    """
    Multiply two polynomials.
    Result degree = len(p) + len(q) - 2.
    poly_multiply([1, 1], [1, 1]) → [1, 2, 1]   ((1+x)^2 = 1 + 2x + x^2)

    Method: result[i+j] += p[i] * q[j] for all i, j
    """
    if not p or not q:
        return []
    result = [0] * (len(p) + len(q) - 1)
    # TODO: nested for loops
    pass


assert poly_multiply([1, 1], [1, 1]) == [1, 2, 1]
assert poly_multiply([1, 0, 1], [1, 1]) == [1, 1, 1, 1]  # (1+x^2)(1+x)


def poly_derivative(p):
    """
    Compute the derivative of p.
    If p = [a0, a1, a2, a3, ...], then p' = [a1, 2*a2, 3*a3, ...]

    poly_derivative([2, -3, 1]) → [-3, 2]   (derivative of 2 - 3x + x^2 is -3 + 2x)
    poly_derivative([5])        → []         (derivative of constant is zero)
    """
    if len(p) <= 1:
        return []
    # TODO: result[i] = (i+1) * p[i+1] for i in range(len(p)-1)
    pass


assert poly_derivative([2, -3, 1]) == [-3, 2]
assert poly_derivative([5])        == []
assert poly_derivative([0, 0, 1])  == [0, 2]   # derivative of x^2 is 2x


def poly_to_string(coeffs):
    """
    Return a human-readable string for the polynomial.

    Rules:
    - Skip zero terms
    - x^1 is written as "x" (not "x^1")
    - x^0 is written as just the number
    - Negative coefficients use " - " instead of " + -"
    - Coefficient of 1 or -1 for x^n (n>0) is omitted (write "x" not "1x")
    - Use Unicode superscripts: ² ³ ⁴ ⁵ ... for exponents >= 2

    Examples:
        poly_to_string([2, -3, 1])    → "2 - 3x + x²"
        poly_to_string([0, 1])        → "x"
        poly_to_string([5])           → "5"
        poly_to_string([1, 0, -1])    → "1 - x²"
    """
    superscripts = {2:"²", 3:"³", 4:"⁴", 5:"⁵", 6:"⁶", 7:"⁷", 8:"⁸", 9:"⁹"}

    def format_term(coeff, degree):
        """Format a single term."""
        if coeff == 0:
            return None
        if degree == 0:
            return str(coeff)
        # build x part
        x_part = "x" + superscripts.get(degree, f"^{degree}") if degree >= 2 else "x"
        if abs(coeff) == 1:
            return ("-" if coeff < 0 else "") + x_part
        return f"{coeff}{x_part}"

    # TODO: build list of non-None terms, join with " + " / " - "
    # Start from highest degree (reversed enumeration)
    # Handle sign carefully for the join
    pass


assert poly_to_string([5])           == "5"
assert poly_to_string([0, 1])        == "x"
assert poly_to_string([2, -3, 1])    == "2 - 3x + x²"
print("✓ poly_to_string")


def poly_roots_newton(coeffs, initial_guess, tolerance=1e-8, max_iter=100):
    """
    Find a root of the polynomial near initial_guess using Newton-Raphson.

    Newton-Raphson: x_new = x - p(x) / p'(x)
    Stop when |p(x)| < tolerance or after max_iter iterations.

    Args:
        coeffs (list): polynomial coefficients
        initial_guess (float): starting point
        tolerance (float): convergence threshold on |p(x)|
        max_iter (int): maximum iterations

    Returns:
        float: approximate root, or None if convergence failed

    Examples:
        # x^2 - 3x + 2 = (x-1)(x-2): roots at 1 and 2
        poly_roots_newton([2, -3, 1], 2.5)  → ≈ 2.0
        poly_roots_newton([2, -3, 1], 0.5)  → ≈ 1.0
    """
    deriv = poly_derivative(coeffs)
    x = float(initial_guess)

    for _ in range(max_iter):
        fx  = poly_eval(coeffs, x)
        if abs(fx) < tolerance:
            return x
        dfx = poly_eval(deriv, x)
        if dfx == 0:
            return None   # derivative is zero — can't continue
        x = x - fx / dfx

    return None   # did not converge


root = poly_roots_newton([2, -3, 1], 2.5)
assert root is not None and abs(root - 2.0) < 1e-6, f"root near 2: {root}"
root2 = poly_roots_newton([2, -3, 1], 0.5)
assert root2 is not None and abs(root2 - 1.0) < 1e-6, f"root near 1: {root2}"
print("✓ poly_roots_newton")


# ══════════════════════════════════════════════════════════════════════════════
# Final summary
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("All ps3.py assertions passed at import time.")
    print("Run individual sections to see output.")
    print("=" * 50)
