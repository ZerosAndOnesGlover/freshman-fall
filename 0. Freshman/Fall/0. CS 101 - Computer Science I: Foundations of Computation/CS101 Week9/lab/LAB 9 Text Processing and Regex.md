# CS 101 · Lab 9
## Text Processing: Measuring the Concatenation Trap, Search Cost, and Regex Behaviour

**Date:** Tuesday 1 December 2026 · 15:00–16:50 · Lab Section (Week 10) — covers Week 9 (L28–L30)
*Duration: 2 hours · 100 points via TA checkoff, part of the Labs component (10%)*

---

## Objectives

1. Measure the string concatenation trap and defeat CPython's optimisation that hides it
2. Implement naive substring search and compare it empirically against the built-in
3. Build and test regular expressions, including named groups and validation
4. Demonstrate catastrophic backtracking (ReDoS) with real timings
5. Establish where regex stops being the right tool

---

## Setup

```bash
mkdir -p "$CS101/week9" && cd "$CS101/week9"        # set in ~/.bashrc -- see Lab 0
# copy text_lab_starter.py here
python3 --version      # 3.10+
```

---

## Part 1: The Concatenation Trap (20 minutes)

### Exercise 1.1 — The misleading benchmark

```python
import timeit
for n in (2000, 8000, 32000):
    t_cat  = timeit.timeit("s=''\nfor c in src: s+=c", setup=f"src='x'*{n}", number=3)/3
    t_join = timeit.timeit("''.join(src)",             setup=f"src='x'*{n}", number=3)/3
    print(f"n={n:>6}  concat {t_cat*1000:8.3f} ms   join {t_join*1000:7.4f} ms   ratio {t_cat/t_join:5.0f}x")
```

**Record the ratios.** You should find concat is only a few times slower — *not* quadratically
slower. Write down what you would conclude if you stopped here.

### Exercise 1.2 — Defeating the optimisation

CPython resizes a string in place when its reference count is 1. Keep a live alias and that
optimisation cannot fire:

```python
for n in (2000, 8000, 32000):
    t = timeit.timeit("""
s = ''
keep = []
for c in src:
    s += c
    keep.append(s)
""", setup=f"src='x'*{n}", number=1)
    print(f"n={n:>6}  with live alias: {t*1000:9.3f} ms")
```

**Record in `LAB 9 Text Processing and Regex.md`:**

1. The three timings from 1.1 and the three from 1.2.
2. For 1.2, compute the ratio between successive timings. What complexity class does that imply?
3. In one paragraph: what does this tell you about trusting microbenchmarks?

---

## Part 2: Substring Search (25 minutes)

### Exercise 2.1 — Implement and instrument

```python
def naive_search(haystack, needle):
    n, m = len(haystack), len(needle)
    if m == 0:
        return 0, 0                      # empty needle matches at 0
    comparisons = 0
    for i in range(n - m + 1):           # every alignment
        j = 0
        while j < m:
            comparisons += 1             # count EVERY character comparison
            if haystack[i + j] != needle[j]:
                break
            j += 1
        if j == m:
            return i, comparisons
    return -1, comparisons
```

Verify the index agrees with `str.find` on all four cases:

```python
for hay, ned in [("hello world", "world"), ("aaaa", "aab"), ("abc", ""), ("abc", "abc")]:
    idx, comps = naive_search(hay, ned)
    print(f"{hay!r:14} {ned!r:8} -> idx={idx:>3} comps={comps:>3}  builtin={hay.find(ned):>3}"
          f"  {'OK' if idx == hay.find(ned) else 'MISMATCH'}")
```

The empty-needle case is the one people omit — `str.find` returns 0, and yours must agree.

### Exercise 2.2 — The adversarial input

```python
import timeit
for n in (2000, 8000, 32000):
    hay, ned = "a" * n, "a" * 50 + "b"
    _, comps = naive_search(hay, ned)
    t_naive   = timeit.timeit(lambda: naive_search(hay, ned), number=1)
    t_builtin = timeit.timeit(lambda: hay.find(ned),          number=1)
    print(f"n={n:>6}  comps={comps:>9,}  formula={(n-50)*51:>9,}"
          f"  naive={t_naive*1000:7.2f} ms  find={t_builtin*1e6:7.1f} us")
```

Run it on a haystack of `n` a's against a needle of 50 a's followed by `b`:

| n | Your comparisons | `(n−k)(k+1)` | Naive time | `str.find` time |
|---|---|---|---|---|
| 2,000 | | | | |
| 8,000 | | | | |
| 32,000 | | | | |

**Record:** does your comparison count match the formula exactly? What is the speed ratio between
your implementation and the built-in at n = 32,000?

### Exercise 2.3 — Why the built-in wins

In two or three sentences, explain what information a failed match provides that the naive
algorithm discards, and name one algorithm that exploits it.

---

## Part 3: Regular Expressions (30 minutes)

### Exercise 3.1 — Core behaviour

Predict, then run:

```python
re.findall(r"<.+>",  "<a><b>")
re.findall(r"<.+?>", "<a><b>")
re.match(r"world", "hello world")
re.search(r"world", "hello world")
re.fullmatch(r"\w+", "hello world")
re.split(r"[,;]\s*", "a, b; c")
re.sub(r"\s+", " ", "a   b \t c")
re.findall(r"\b(\w+) \1\b", "the the quick fox fox")
```

Record any prediction you got wrong and why.

### Exercise 3.2 — Build a log parser

Write a verbose, anchored, named-group pattern for lines like:

```
2026-07-26 11:02:33 ERROR disk full
```

It must extract `date`, `time`, `level`, `message`, and **skip** malformed lines rather than
raising. Test against a file containing at least two malformed lines.

### Exercise 3.3 — Validation, done correctly

Write `valid_email` with `fullmatch`. Then deliberately rewrite it with `search` and find an input
the `search` version wrongly accepts. **Record that input** — it is the point of the exercise.

---

## Part 4: Catastrophic Backtracking (20 minutes)

```python
import re, time
bad = re.compile(r"^(a+)+$")
for n in (18, 20, 22, 24):
    s = "a"*n + "!"
    t0 = time.perf_counter(); bad.search(s); el = time.perf_counter() - t0
    print(f"  {n} a's: {el*1000:9.2f} ms")

good = re.compile(r"^a+$")
t0 = time.perf_counter(); good.search("a"*100000 + "!")
print(f"  safe pattern on 100000 a's: {(time.perf_counter()-t0)*1000:.3f} ms")
```

**⚠️ Do not go above n = 26** unless you enjoy killing processes.

**Record:**

1. The four timings, plus the ratio between successive ones.
2. Why the ratio is what it is — what is the engine actually doing?
3. Why `^a+$` is immune.
4. The name of this attack class, and one real-world incident caused by it.

---

## Part 5: Where Regex Stops Working (10 minutes)

```python
re.sub(r"<.*?>", "", '<a href="x">link</a>')        # observe
re.sub(r"<.*?>", "", '<a href="a>b">link</a>')      # observe
```

**Record:** the two outputs, an explanation of the second, and a statement of the general boundary
in terms of language classes. Name the correct tool for HTML.

---

## Part 6: Commit and Reflection (5 minutes)

```bash
git add . && git commit -m "Week 9 Lab: text processing, search cost, regex, ReDoS"
```

### Reflection in `LAB 9 Text Processing and Regex.md`:

1. Which measurement surprised you most, and what did you believe beforehand?
2. Part 1 showed a benchmark that hid the behaviour it was measuring. How would you guard against
   that in future?
3. Give one task from your own experience where regex would be the right tool, and one where it
   would be tempting but wrong.

---

## TA Checkoff Criteria

| Part | Points | Show your TA |
|---|---|---|
| 1 | 20 | Both benchmarks run; the quadratic ratio identified from 1.2 |
| 2 | 20 | `naive_search` agrees with `str.find` on all four cases; formula confirmed |
| 3 | 25 | Log parser works and skips malformed lines; the `search`-accepts-garbage input found |
| 4 | 20 | Four timings recorded; exponential growth explained; attack named |
| 5 | 15 | The HTML failure reproduced and explained in terms of language classes |
| **Total** | **100** | Reflection answered and work committed (required) |

---

*CS 101 · Week 9 · Lab 9 · Tuesday 1 December 2026 · © CSE Department*
