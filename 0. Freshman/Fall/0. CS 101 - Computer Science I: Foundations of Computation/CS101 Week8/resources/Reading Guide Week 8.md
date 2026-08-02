# CS 101 — Week 8 Reading Guide & Resources
## Data Structures II: Hash Tables and Sets

---

## Required Reading

### Guttag — Introduction to Computation and Programming Using Python

**Chapter 5.4–5.5 — Dictionaries and Sets** (if covered in your edition)
- Basic dict/set syntax and operations
- Common use patterns

### CLRS — Introduction to Algorithms (Primary reference this week)

**Chapter 11 — Hash Tables**
- §11.1 — Direct-address tables (the "ideal" case with no collisions — useful conceptual baseline)
- §11.2 — Hash tables (chaining, formal analysis of expected search time)
- §11.3 — Hash functions (what makes a hash function "good"; division method, multiplication method)
- §11.4 — Open addressing (linear probing, quadratic probing, double hashing)

This is the definitive formal treatment — read it after lecture to deepen the mathematical analysis of expected-case performance.

### Python Documentation

- **collections module:** https://docs.python.org/3/library/collections.html — `Counter`, `defaultdict`, `OrderedDict`
- **Data model — hashing:** https://docs.python.org/3/reference/datamodel.html#object.__hash__

---

## Focused REPL / Experimentation Sessions

### Session A: Feeling Hash Determinism and Randomization (15 min)

```python
# Within ONE Python session, hash() is deterministic:
print(hash("apple"))
print(hash("apple"))   # SAME value

# But restart Python (or open a new terminal) and run again —
# you'll get a DIFFERENT value! This is hash randomization (security feature).

# Small integers hash to themselves:
print(hash(42))     # 42
print(hash(0))       # 0
print(hash(-1))      # -2  (a special case in CPython, NOT -1! Why? -1 is reserved
                      #      internally as an error signal in C, so CPython avoids it.)

# Tuples hash based on their CONTENTS:
print(hash((1, 2, 3)))
print(hash((1, 2, 3)))   # same tuple contents -> same hash, even different tuple objects
a = (1, 2, 3)
b = (1, 2, 3)
print(a is b)              # False — different objects (usually)
print(hash(a) == hash(b))  # True — same contents, same hash (REQUIRED by the contract)
```

### Session B: Measuring Dict/Set Speedup Directly (15 min)

```python
import time

n = 100_000
data_list = list(range(n))
data_set  = set(data_list)
data_dict = {x: True for x in data_list}

targets = [0, n // 2, n - 1, -1]   # first, middle, last, absent

for target in targets:
    t0 = time.perf_counter()
    result_list = target in data_list
    t1 = time.perf_counter()

    t0b = time.perf_counter()
    result_set = target in data_set
    t1b = time.perf_counter()

    print(f"target={target:>8}: list={((t1-t0)*1e6):9.2f}μs  set={((t1b-t0b)*1e6):7.4f}μs  "
          f"speedup={((t1-t0)/(t1b-t0b) if t1b>t0b else float('inf')):8.0f}x")

# Notice: list's time DEPENDS heavily on where the target is (0 is instant,
# -1/absent requires scanning everything). Set's time is roughly CONSTANT
# regardless of where (or whether) the target is — this IS the O(1) average
# behavior made visible.
```

### Session C: Building the Complement-Search Pattern From Scratch (15 min)

```python
# Work through the "have I seen the complement" pattern on paper first,
# then verify in the REPL.

def two_sum(nums, target):
    seen = {}   # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None

# Trace by hand: nums = [2, 7, 11, 15], target = 9
# i=0, num=2, complement=7, seen={} -> 7 not in seen -> seen={2:0}
# i=1, num=7, complement=2, seen={2:0} -> 2 IS in seen! -> return (0, 1)

print(two_sum([2, 7, 11, 15], 9))   # (0, 1)

# Now apply the SAME pattern to a different problem: "does the list contain
# two elements that differ by exactly k?"
def has_pair_with_difference(nums, k):
    seen = set()
    for num in nums:
        if (num - k) in seen or (num + k) in seen:
            return True
        seen.add(num)
    return False

print(has_pair_with_difference([1, 5, 3, 9], 4))   # True (5-1=4, or 9-5=4)
print(has_pair_with_difference([1, 2, 3], 10))      # False
```

---

## Conceptual Exercises (Paper and Pencil)

**Exercise 1:** A hash table has 16 buckets and uses chaining. After inserting 20 elements (assume perfectly uniform distribution across buckets), what is the average chain length? What is the load factor?

**Exercise 2:** Explain why `hash(3.0) == hash(3)` is True in Python, even though `3.0` is a float and `3` is an int. (Hint: think about the `__eq__`/`__hash__` contract — `3.0 == 3` is True in Python, so what does the contract REQUIRE about their hashes?)

**Exercise 3:** You are designing a hash table for a system that will ONLY ever store English words (never removed once inserted). Would you choose chaining or open addressing? Justify using this week's load-factor performance data — does the "no removal" constraint change your reasoning about tombstones?

**Exercise 4:** A student writes:
```python
class Config:
    def __init__(self, settings_dict):
        self.settings = settings_dict   # a dict — mutable!

    def __hash__(self):
        return hash(tuple(sorted(self.settings.items())))
```
They then use `Config` objects as dictionary keys. Explain the danger in this design, even though `__hash__` is defined and technically "works" at first. (Hint: think about what happens if `self.settings` is mutated AFTER the object has been used as a key.)

---

## Complexity Reference Card

```
DICT / SET (Python's hash table implementation)
──────────────────────────────────────────────────
d[key]                    O(1) average, O(n) worst case
d[key] = value             O(1) average, O(1) amortized (resize occasionally)
key in d                   O(1) average
del d[key]                 O(1) average
len(d)                     O(1)
d.get(key, default)        O(1) average
d.keys() / .values() / .items()   O(1) to CREATE the view; O(n) to iterate fully

set operations (a, b are sets of size n, m):
a | b   (union)             O(n + m)
a & b   (intersection)      O(min(n, m))
a - b   (difference)        O(n)
a.issubset(b)               O(n)

HASH TABLE INTERNALS
──────────────────────
Chaining:
    average case:   O(1 + load_factor)
    worst case:      O(n)  (all keys collide)
Open addressing:
    average case:   O(1 / (1 - load_factor))  — degrades faster as load factor → 1
    worst case:      O(n)

Resize (amortized): O(1) per insertion, same structure as PS6's DynamicArray
```

---

## Common Mistakes This Week

**Mistake 1: Using a mutable object as a dict key or set member**
```python
d = {[1,2]: "value"}   # TypeError: unhashable type: 'list'
```
Use a tuple, frozenset, or an immutable custom class instead.

**Mistake 2: Defining `__eq__` without `__hash__`**
```python
class Foo:
    def __eq__(self, other):
        return ...
    # No __hash__! Python sets __hash__ = None automatically, making Foo unhashable.
```
If you override `__eq__`, you MUST also define `__hash__` if you want instances to work in sets/dicts.

**Mistake 3: Hashing based on mutable state**
```python
class Config:
    def __hash__(self):
        return hash(tuple(self.settings.items()))   # if self.settings is later mutated,
                                                       # this hash becomes STALE and WRONG
```
Only hash based on data that is guaranteed never to change during the object's lifetime.

**Mistake 4: Assuming dict/set have a meaningful sort order**
```python
s = {3, 1, 4, 1, 5}
print(s)   # order is an implementation detail, NOT sorted, NOT insertion order for sets!
```
Only Python's `dict` (3.7+) guarantees insertion-order iteration. Plain `set` does NOT guarantee any particular order.

**Mistake 5: Reaching for a dict/set when the problem doesn't actually need one**
```python
# If you need the MAXIMUM, a dict doesn't help — you still need O(n):
max_val = max(data)   # O(n) regardless of data structure
```
Dict/set solve "fast exact-match lookup." They do not speed up order-based queries (max, min, range, sorted position) — those need sorted structures instead.

---

## Week 8 Self-Test

1. Why must equal objects have equal hashes? What breaks if this contract is violated?
2. What is a collision? Why is it mathematically unavoidable (name the principle)?
3. Compare chaining and open addressing: which handles high load factor more gracefully? Which has better memory/cache characteristics?
4. What is a tombstone, and why is it necessary for correct deletion in open addressing?
5. What is "load factor"? How does Python's dict keep it bounded?
6. Explain the amortized O(1) argument for hash table insertion, connecting it to Week 6/PS6's dynamic array analysis.
7. Give the "complement lookup" pattern in one sentence, and name two problems it solves.
8. Why is `hash([1,2,3])` an error but `hash((1,2,3))` is not?
9. Name two operations dict/set do NOT speed up, and explain why.
10. What does `defaultdict(list)` do differently from a plain `dict` when you access a missing key?

*(Answers: 1. so the hash table can reliably find items later — a corrupted lookup structure otherwise. 2. two different keys hashing to the same bucket; pigeonhole principle. 3. chaining degrades more gracefully; open addressing has better cache locality/lower memory overhead. 4. a "deleted" marker distinct from "never used," preserving probe sequences for later searches. 5. count/size; automatic resizing (doubling) when a threshold is exceeded. 6. resizes happen exponentially rarely, so total resize cost amortizes to O(1) per insertion, same as PS6's DynamicArray.append(). 7. "for each item, check if its complement/target has already been seen"; two-sum, pair-with-difference-k. 8. lists are mutable (hash could become stale); tuples are immutable. 9. finding max/min, range queries, sorted order — dict/set have no ordering machinery. 10. it auto-creates an empty list (or whatever factory you specify) instead of raising KeyError.)*

---

## Preview: Week 9

Week 9 covers **Strings and Regular Expressions** — going far deeper into string processing than Week 1's introduction, including pattern matching, regex syntax, and efficient string algorithms (e.g., substring search beyond the naive approach).

**Project 1 is also due this Friday (end of Week 9)** — make sure your data analysis tool is fully complete, tested, and your written report is polished well before the deadline.

Before Wednesday of Week 9, think about: how would you check if a string contains a specific pattern that isn't just an exact substring — for example, "any sequence of digits" or "an email-like structure"? Plain string methods (`.find()`, `in`) can't express this — regular expressions can.

---

*CS 101 · Week 8 · Reading Guide · © CSE Department*
