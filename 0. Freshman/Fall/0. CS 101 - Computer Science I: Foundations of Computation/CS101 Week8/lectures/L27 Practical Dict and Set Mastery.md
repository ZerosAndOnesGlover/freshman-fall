# CS 101 — Lecture 27 (Week 8, Lecture 3)
## Practical Dictionary and Set Mastery

**Week 8 · Friday**
*"Knowing that dict lookup is O(1) is theory. Knowing WHEN to reach for a dict instead of a list is engineering." — CS 101*

---

## 0. From Mechanism to Mastery

Wednesday gave you the theory of hashing. Thursday gave you the mechanism (collision resolution, resizing). Today is about **fluency** — recognizing the patterns where dict/set transform an algorithm's complexity class, and building the instinct to reach for them automatically.

---

## 1. The Master Pattern: Trading Space for Time

Nearly every "use a dict to speed this up" technique follows the same shape:

```
SLOW (no auxiliary structure):     "for each item, scan everything else"  → O(n²)
FAST (with a dict/set):             "for each item, look up in O(1)"        → O(n)
```

This trade-off — spend O(n) extra memory to build a lookup structure, in exchange for turning repeated O(n) scans into O(1) lookups — is one of the most impactful patterns in all of practical programming. Let's see it applied to real problems.

---

## 2. Pattern 1: Counting — The Frequency Table

You've seen this since Wednesday, but let's generalize it.

```python
def count_frequencies(items):
    """
    Count occurrences of each item. O(n) time, O(k) space (k = unique items).
    """
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts


# Python's standard library has a purpose-built tool for this:
from collections import Counter

def count_frequencies_builtin(items):
    """Same result, using the standard library's Counter class."""
    return Counter(items)


text = "the cat sat on the mat the cat ran".split()
print(count_frequencies(text))
print(count_frequencies_builtin(text))

c = Counter(text)
print(c.most_common(2))    # [('the', 3), ('cat', 2)] — the 2 most frequent items
```

`collections.Counter` is a `dict` subclass specialized for counting — it has `.most_common(n)`, arithmetic operations (`Counter(a) + Counter(b)`), and defaults every missing key to 0 automatically (no `KeyError`, no need for `.get(x, 0)`).

---

## 3. Pattern 2: Grouping — Building an Index

```python
def group_by_length(words):
    """
    Group words by their length.
    Returns dict: {length: [word1, word2, ...]}
    """
    groups = {}
    for word in words:
        key = len(word)
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return groups


# Cleaner using collections.defaultdict:
from collections import defaultdict

def group_by_length_cleaner(words):
    groups = defaultdict(list)   # auto-creates an empty list for any new key!
    for word in words:
        groups[len(word)].append(word)
    return dict(groups)


words = ["cat", "dog", "bird", "ox", "fish", "ant"]
print(group_by_length_cleaner(words))
# {3: ['cat', 'dog', 'ant'], 4: ['bird', 'fish'], 2: ['ox']}
```

`defaultdict(list)` eliminates the "check if key exists, create empty container if not" boilerplate — a factory function (here, `list`) is called automatically the first time any new key is accessed.

---

## 4. Pattern 3: Membership Testing — The Deduplication Speedup

```python
def has_duplicates_slow(lst):
    """O(n²) — the Week 3 approach, without dicts."""
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                return True
    return False


def has_duplicates_fast(lst):
    """O(n) — using a set for O(1) average membership testing."""
    seen = set()
    for item in lst:
        if item in seen:      # O(1) average!
            return True
        seen.add(item)         # O(1) average!
    return False


def remove_duplicates_preserving_order(lst):
    """
    Remove duplicates while preserving first-occurrence order. O(n).
    (Compare to PS7's O(n^2) linked-list version, done without a set!)
    """
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


assert remove_duplicates_preserving_order([1,2,2,3,1,4,3]) == [1,2,3,4]
```

This directly answers PS7's B3(d) footnote: "a set-based version would be O(n)." Here it is.

---

## 5. Pattern 4: The Two-Sum Problem — A Classic Dict Application

**Problem:** given a list of numbers and a target, find two numbers that sum to the target.

```python
def two_sum_slow(nums, target):
    """O(n²) — check every pair."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_fast(nums, target):
    """
    O(n) — for each number, check if its COMPLEMENT has already been seen.

    Key insight: instead of checking all pairs, ask "have I already seen
    the number that would complete a pair with THIS number?"
    """
    seen = {}   # maps value -> index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:      # O(1) average!
            return (seen[complement], i)
        seen[num] = i

    return None


assert two_sum_fast([2, 7, 11, 15], 9) == (0, 1)
assert two_sum_fast([3, 2, 4], 6)       == (1, 2)
assert two_sum_slow([2, 7, 11, 15], 9) == two_sum_fast([2, 7, 11, 15], 9)
```

**This pattern — "have I seen the complement/target/match already?" — generalizes to an enormous class of problems.** Anagram detection, pair-sum problems, "find the missing number," and many technical interview questions all reduce to this shape.

---

## 6. Pattern 5: Anagram Detection, Properly

Recall Week 2's `is_anagram` challenge, which explicitly forbade dictionaries (since they hadn't been covered). Now:

```python
def is_anagram(s1, s2):
    """
    Return True if s1 and s2 are anagrams (same characters, same frequencies).
    O(n) time, using frequency dicts.
    """
    if len(s1) != len(s2):
        return False

    return count_frequencies(s1.lower()) == count_frequencies(s2.lower())


def count_frequencies(s):
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    return counts


assert is_anagram("listen", "silent")  == True
assert is_anagram("hello", "world")     == False
assert is_anagram("Dormitory", "Dirty Room".replace(" ", "")) == True
```

Comparing two dicts (`==`) checks that they have the same keys AND the same values for each key — exactly the anagram condition. This is O(n), versus O(n log n) for a sort-based comparison, or O(n²) for the loop-based Week 2 version.

---

## 7. Pattern 6: Caching / Memoization Revisited

Week 4's memoization used dicts without formally introducing them as a "pattern." Now you understand *why* they're the right tool: O(1) average lookup means checking "have I already computed this?" doesn't slow down as the cache grows.

```python
def fib_memo(n, cache=None):
    if cache is None:
        cache = {}
    if n in cache:            # O(1) average — this is WHY memoization works efficiently!
        return cache[n]
    if n <= 1:
        return n
    cache[n] = fib_memo(n-1, cache) + fib_memo(n-2, cache)
    return cache[n]


# Python's standard library can do this automatically:
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_auto_memo(n):
    if n <= 1:
        return n
    return fib_auto_memo(n-1) + fib_auto_memo(n-2)


import time
t0 = time.perf_counter(); fib_auto_memo(100); t1 = time.perf_counter()
print(f"fib_auto_memo(100) computed in {(t1-t0)*1000:.4f} ms")
```

`functools.lru_cache` is a **decorator** (a preview of Week 9) that automatically memoizes any function's results using a dict internally, keyed on the function's arguments. This is production-grade memoization with zero manual dict management.

---

## 8. The Complete Decision Framework: list vs. set vs. dict

```
Do you need to preserve DUPLICATE values?
    → list (sets and dicts inherently deduplicate keys)

Do you need ORDERED, indexed access (lst[3])?
    → list

Do you need FAST membership testing (`x in collection`) and DON'T need
associated values (just "is x present or not")?
    → set

Do you need to associate EACH unique item with SOME OTHER value
(a mapping, a lookup table, a count, a grouping)?
    → dict

Do you need FAST membership testing AND to preserve insertion order
of first-seen elements specifically?
    → dict (using keys only) — dicts preserve insertion order (Python 3.7+);
      plain sets do NOT guarantee any particular iteration order
```

### Complexity Comparison Table

| Operation | list | set | dict |
|-----------|------|-----|------|
| `x in collection` | O(n) | O(1) average | O(1) average (checks keys) |
| Add an element | O(1) amortized (append) | O(1) average | O(1) average |
| Remove an element | O(n) (must find + shift) | O(1) average | O(1) average |
| Access by position | O(1) (`lst[i]`) | N/A — no positional access | N/A — access by key, not position |
| Preserves duplicates | Yes | No | No (keys unique; values can repeat) |
| Preserves insertion order | Yes (always has) | No guarantee | Yes (Python 3.7+ guarantee) |
| Memory overhead | Lowest | Higher (hash table overhead) | Higher (hash table + value storage) |

---

## 9. Dictionary and Set Comprehensions

Just as list comprehensions (Week 2 preview, formalized here) build lists concisely, Python supports dict and set comprehensions:

```python
# Dict comprehension:
squares = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

word_lengths = {word: len(word) for word in ["cat", "elephant", "ox"]}
# {'cat': 3, 'elephant': 8, 'ox': 2}

# Set comprehension:
unique_lengths = {len(word) for word in ["cat", "dog", "elephant", "ox"]}
# {8, 2, 3}   (order not guaranteed for plain sets)

# Filtering with comprehensions:
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

---

## 10. A Complete Application: Finding the First Non-Repeating Character

```python
def first_non_repeating_char(s):
    """
    Return the first character in s that appears exactly once.
    Return None if every character repeats.

    Two-pass O(n) algorithm:
        Pass 1: count all character frequencies (a dict)
        Pass 2: scan in order, return the first with count == 1

    Examples:
        first_non_repeating_char("swiss")     → 'w'
        first_non_repeating_char("aabbcc")    → None
        first_non_repeating_char("statistics") → 'a'
    """
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1

    for char in s:              # scan in ORIGINAL order — this is why we need 2 passes
        if counts[char] == 1:
            return char

    return None


assert first_non_repeating_char("swiss")      == 'w'
assert first_non_repeating_char("aabbcc")     == None
assert first_non_repeating_char("statistics") == 'a'
```

**Why two passes, not one?** The frequency of a character isn't known until you've seen the ENTIRE string (a character might repeat later). So you must complete counting first (pass 1), then check in original order (pass 2) to find the first that turned out to be unique. This two-pass pattern — "gather full information first, then make a decision using it" — is common whenever a decision depends on GLOBAL information about the input.

---

## 11. When Dict/Set DON'T Help — Know the Limits

**Dict/set do NOT speed up:**
- Finding the maximum/minimum (still O(n) — you must examine every element; there's no hash-based shortcut for "biggest")
- Maintaining sorted order (dicts/sets have no inherent ordering by value; use a sorted structure or re-sort when needed)
- Range queries ("find all values between X and Y") — this needs a sorted structure (like a Binary Search Tree, later weeks) or explicit sorting + binary search (Week 5), NOT a hash table
- Anything requiring positional/indexed access

**The lesson:** dict/set solve the specific problem of "fast lookup by exact key/value match." They are not a universal speedup for every algorithmic problem — recognizing WHICH problems they help with is the actual skill, more important than knowing their internals.

---

## Summary

| Pattern | Problem Shape | Complexity Without Dict | With Dict/Set |
|---------|---------------|--------------------------|----------------|
| Counting | "How many of each?" | O(n²) nested loops | O(n) |
| Grouping | "Bucket items by property" | O(n²) or awkward | O(n) with `defaultdict` |
| Deduplication | "Remove/detect duplicates" | O(n²) | O(n) with `set` |
| Complement search | "Find pair summing to X" | O(n²) | O(n) |
| Anagram check | "Same letters, same counts?" | O(n²) or O(n log n) sort | O(n) |
| Memoization | "Have I computed this before?" | N/A (no caching) | O(1) average per check |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict the output and give the complexity of each call.

```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return (seen[target - n], i)
        seen[n] = i
    return None

print(two_sum([2, 7, 11, 15], 9))
print(two_sum([3, 3], 6))
print(two_sum([3, 2, 4], 6))
print(two_sum([1, 2], 7))
```

**2. (Explain.)** `x in some_list` and `x in some_set` look identical. Give the complexity of each, predict the ratio on a million elements, and state when the list is nonetheless the right choice.

**3. (Build.)** Write `first_non_repeating(s)` returning the first character occurring exactly once, or `None`. Give its complexity, and explain why a two-pass solution beats the obvious nested-loop one.

**4. (Stretch.)** §11 covers when dicts and sets do **not** help. Give three problems where converting to a dict or set makes things worse, and say what to use instead.


### Answers

**1.** `(0, 1)`, `(0, 1)`, `(1, 2)`, `None`. All are **Θ(n) time, Θ(n) space**.

The third is the one worth tracing. At `i = 0`, `seen = {}`, `6 - 3 = 3` is absent, so `seen = {3: 0}`. At `i = 1`, `6 - 2 = 4` is absent, so `seen = {3: 0, 2: 1}`. At `i = 2`, `6 - 4 = 2` **is** present at index 1, so it returns `(1, 2)` — deliberately *not* `(0, 0)`, because 3 + 3 = 6 would require using index 0 twice.

That constraint is enforced by the structure of the loop, not by an explicit check: the complement is looked up **before** the current element is inserted, so `n` can never match itself. Inserting first would break `[3, 2, 4]` and return `(0, 0)`.

The second case shows genuine duplicates still work: at `i = 1` the first `3` is already in `seen`, so `(0, 1)` is correct. Note `seen[n] = i` overwrites on duplicates, keeping the *most recent* index — harmless here since a match is found first, but it is the kind of detail that matters if the problem asks for all pairs.

**2.** `x in list` is **Θ(n)** — a linear scan comparing each element. `x in set` is **Θ(1) average** — one hash, one bucket probe.

**Prediction:** on a million elements, searching for a worst-case (last or absent) element should differ by roughly a factor of a million, modulo constants. Measured with `timeit`, the list takes on the order of ten milliseconds per lookup and the set tens of nanoseconds — a difference of about five orders of magnitude. This is the single largest easy win in the course: converting a list to a set before a membership-heavy loop turns Θ(n·m) into Θ(n + m).

The list is the right choice when:

- **Elements are unhashable** — lists, dicts, or mutable custom objects cannot go in a set.
- **Order or duplicates matter** — a set has neither.
- **The collection is tiny and you check it once.** Building a set costs Θ(n) and allocates; for a five-element collection checked once, that is pure overhead. The break-even is usually a handful of lookups.
- **You need indexing or slicing**, which sets do not support.

The rule of thumb: **if you build a collection to answer "is this in it?" more than once, make it a set.** If it is a literal you check against repeatedly, make it a `frozenset` module constant.

**3.**

```python
from collections import Counter

def first_non_repeating(s):
    counts = Counter(s)
    for ch in s:
        if counts[ch] == 1:
            return ch
    return None

# 'aabbcd' -> 'c'   'aabb' -> None   '' -> None
```

**Θ(n) time, Θ(k) space** for k distinct characters.

The nested-loop version — for each character, scan the whole string counting occurrences — is **Θ(n²)**, because it recomputes from scratch what it already computed for every previous character.

The two-pass version separates **gathering** from **deciding**. Pass one builds the complete frequency table; pass two consults it in O(1) per character. Neither pass needs the other's work repeated, so the total is linear.

The second pass must iterate over **`s`, not over `counts`** — the question asks for the *first* such character in the string. Iterating the dict happens to work in CPython, since dicts preserve insertion order and the counter was built by scanning `s`, but relying on that couples your correctness to how the table was constructed. Iterating `s` states the requirement directly.

This "count everything first, then decide in one pass" shape recurs constantly — anagram grouping, majority elements, sliding windows — and is the concrete form of §1's space-for-time trade.

**4.** **1. Finding the k smallest elements.** A set discards order entirely, so you would have to sort it anyway. Hashing gives you O(1) *equality* lookup and nothing about *ordering* — no "next largest", no range query, no minimum. Use a **heap** (`heapq.nsmallest`, Θ(n log k)) or a sorted list with `bisect`.

**2. Prefix or substring matching** — "all words starting with 'pre'". A hash of `"prefix"` bears no relation to the hash of `"pre"`; hashing deliberately destroys the structure that prefix matching needs. Use a **trie**, or a sorted list plus `bisect` to find the range.

**3. Small collections, or one-shot membership checks.** Building a set is Θ(n) with allocation and hashing per element. For five items checked once, `x in [1,2,3,4,5]` is faster than `x in set([1,2,3,4,5])`, since the latter pays construction to save a scan of five. Use a **list or tuple**.

A fourth worth adding: **unhashable elements**. A list of lists cannot become a set at all, and the workaround — converting each to a tuple — silently changes the element type and costs a copy.

The unifying principle: hashing buys **O(1) exact-match lookup** and pays for it by destroying **order, adjacency, and structure**. When the query is "is this exact thing present?", it is unbeatable. When the query involves *comparison* between elements — smallest, nearest, in-range, sharing a prefix — you need a structure that preserves order, and a hash table is the wrong tool.



---

## Reading

- **Guttag, Ch. 5.4–5.5** — Dictionaries and sets (continued)
- **Python docs — collections module:** https://docs.python.org/3/library/collections.html (Counter, defaultdict, OrderedDict)
- **Python docs — functools.lru_cache:** https://docs.python.org/3/library/functools.html#functools.lru_cache

---

*CS 101 · Week 8 · Lecture 27 (Fri) · © CSE Department*
