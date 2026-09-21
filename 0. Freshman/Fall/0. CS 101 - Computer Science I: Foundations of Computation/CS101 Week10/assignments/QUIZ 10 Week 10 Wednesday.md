# CS 101 · Quiz 10
## Week 10, Wednesday — In-Class Assessment

**Date:** Wednesday 2 December 2026 · 09:00–09:10 (start of L31) · Week 10
**Duration:** 10 minutes (first 10 minutes of Wednesday lecture)
**Format:** Written — closed book, closed notes
**Covers:** Week 9 material: strings, encoding, search cost, regular expressions

---

### Question 1 (2 points)

`len("café")` is 4 but `len("café".encode("utf-8"))` is 5. Explain in one sentence. Then state
`len("👋🏽")` and why.

&nbsp;

&nbsp;

---

### Question 2 (2 points)

Building a string with `s += c` inside a loop over `n` characters is Θ(n²).

(a) State the total number of character copies performed.

(b) A student benchmarks it and measures only a ~5× penalty, concluding it is linear. Name the
CPython behaviour responsible.

&nbsp;

&nbsp;

---

### Question 3 (2 points)

State the difference between `re.match`, `re.search`, and `re.fullmatch`. Which must be used to
**validate** a field, and give one input that the wrong choice would wrongly accept for a 4-digit
PIN.

&nbsp;

&nbsp;

---

### Question 4 (2 points)

`re.findall(r"<.+>", "<a><b>")` returns **one** match, not two.

(a) Why?

(b) Give the one-character fix.

&nbsp;

&nbsp;

---

### Question 5 (2 points)

Naive substring search is Θ(n·m) in the worst case.

(a) Describe the input shape that triggers the worst case.

(b) Name one thing a *failed* match tells you that the naive algorithm throws away.

&nbsp;

&nbsp;

---

**Total: 10 points**

---

### Answer Key (Instructor Copy — Do Not Distribute)

**1.** A `str` is a sequence of **Unicode code points**; UTF-8 is a **variable-width** encoding, and
`é` requires two bytes. `len("👋🏽")` is **2** — a base emoji plus a skin-tone modifier, two code
points rendering as one glyph. 1 pt each. Accept "characters vs bytes" for the first mark only if
the variable-width point is made.

**2.** (a) `1 + 2 + … + n = n(n+1)/2` copies. (b) CPython **resizes the string in place when its
reference count is 1**, which the naive loop happens to satisfy. Accept "an in-place optimisation
when nothing else references the string." Do **not** accept "the interpreter caches strings."

**3.** `match` anchors at the start; `search` matches anywhere; `fullmatch` requires the **entire**
string. **`fullmatch` validates.** Wrongly accepted input for `search(r"\d{4}", …)`: any string
*containing* four digits — `"12345"`, `"abc1234"`, `"drop table; 1234"`. 1 pt for the three-way
distinction, 1 pt for `fullmatch` **plus** a concrete bad input.

**4.** (a) `.+` is **greedy** — it consumes to the end of the string, then backtracks only as far as
the **last** `>`, so one match spans both tags. (b) `<.+?>` — the `?` makes the quantifier lazy.
1 pt each.

**5.** (a) A needle that **almost matches everywhere**: a haystack of repeated characters and a
needle repeating then differing, e.g. `"aaa…ab"` searched in `"aaaa…a"`. Each alignment compares
`m` characters before failing. (b) A failed match reveals **what the characters were** up to the
point of failure, so many subsequent alignments can be ruled out without comparison — the idea
behind KMP, Boyer–Moore, and the two-way algorithm CPython actually uses. 1 pt each.

*Common wrong answer on 5(a):* "a very long haystack." Length alone does not trigger the worst case;
the *structure* does.
