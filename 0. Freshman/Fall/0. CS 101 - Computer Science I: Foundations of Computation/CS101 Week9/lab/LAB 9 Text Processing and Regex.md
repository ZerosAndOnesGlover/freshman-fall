# CS 101: Lab 9
## Text Processing: Measuring the Concatenation Trap, Search Cost, and Regex Behaviour

**Duration:** 3 hours | **Graded:** TA checkoff on completion and correctness

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
mkdir -p cs101/week9 && cd cs101/week9
# copy text_lab_starter.py here
python3 --version      # 3.10+
```

---

## Part 1: The Concatenation Trap (35 minutes)

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

## Part 2: Substring Search (40 minutes)

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

## Part 3: Regular Expressions (50 minutes)

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

## Part 4: Catastrophic Backtracking (30 minutes)

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

## Part 5: Where Regex Stops Working (15 minutes)

```python
re.sub(r"<.*?>", "", '<a href="x">link</a>')        # observe
re.sub(r"<.*?>", "", '<a href="a>b">link</a>')      # observe
```

**Record:** the two outputs, an explanation of the second, and a statement of the general boundary
in terms of language classes. Name the correct tool for HTML.

---

## Part 6: Building a Concordance (30 minutes)

A **concordance** maps each word to the lines on which it appears — the core of every search index,
and a direct application of L27's grouping pattern to text.

### Exercise 6.1 — Build it

```python
import re, unicodedata
from collections import defaultdict, Counter

def normalise(w):
    return unicodedata.normalize("NFC", w).casefold()

def concordance(text):
    """Map each normalised word -> sorted list of line numbers where it appears."""
    index = defaultdict(list)
    for lineno, line in enumerate(text.splitlines(), start=1):
        for word in re.findall(r"[\w']+", line):
            index[normalise(word)].append(lineno)
    return index
```

Test on:

```python
text = """The quick brown fox jumps over the lazy dog.
The dog barks; the fox runs. A quick fox!"""
```

Expected — words appearing on more than one line:

| Word | Lines | Occurrences |
|---|---|---|
| `the` | 1, 2 | 4 |
| `fox` | 1, 2 | 3 |
| `quick` | 1, 2 | 2 |
| `dog` | 1, 2 | 2 |

Note `The`, `the`, and `the` all collapse to one entry — that is the normalisation doing its job.

### Exercise 6.2 — n-grams

```python
def ngrams(text, n):
    """Counter of every contiguous n-word sequence."""
    words = [normalise(w) for w in re.findall(r"[\w']+", text)]
    return Counter(tuple(words[i:i+n]) for i in range(len(words) - n + 1))
```

On the sample text: **18 words yield 17 bigrams**. Confirm that, and state the general relationship
between word count and n-gram count. What is the complexity of `ngrams` in terms of the word count?

### Exercise 6.3 — One more regex limit

Splitting text into sentences looks like a regex job:

```python
re.split(r"(?<=[.!?])\s+", "A dog. A cat.")
# ['A dog.', 'A cat.']                    <- correct

re.split(r"(?<=[.!?])\s+", "Dr. Smith went home. He slept.")
# ['Dr.', 'Smith went home.', 'He slept.'] <- WRONG: three sentences, should be two
```

**Record:** why the second fails, and why patching it with a list of abbreviations is not a general
fix. What would you use instead for real text?

*(The `(?<=...)` construct is a **lookbehind** — it asserts what precedes the match position
without consuming it, so the punctuation stays attached to the sentence.)*

---

## Part 7: Commit and Reflection (10 minutes)

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

- [ ] Part 1: both benchmarks run; the quadratic ratio identified from 1.2
- [ ] Part 2: `naive_search` agrees with `str.find` on all four cases; formula confirmed
- [ ] Part 3: log parser works and skips malformed lines; the `search`-accepts-garbage input found
- [ ] Part 4: four timings recorded; exponential growth explained; attack named
- [ ] Part 5: the HTML failure reproduced and explained in terms of language classes
- [ ] Part 6: concordance built and verified; bigram count confirmed; sentence-split limit explained
- [ ] Reflection complete

---

## Bonus Challenges

1. Implement **Boyer–Moore–Horspool** search and compare its comparison count against naive on the
   adversarial input. When is it *worse* than naive?
2. Write a regex that validates an IPv4 address — all four octets in 0–255, no leading zeros. This
   is harder than it looks; state how many characters your pattern needs.
3. Time `re.compile`d patterns against inline `re.search` in a loop of 100,000 iterations. Is the
   difference what you expected? Investigate `re`'s internal cache.
