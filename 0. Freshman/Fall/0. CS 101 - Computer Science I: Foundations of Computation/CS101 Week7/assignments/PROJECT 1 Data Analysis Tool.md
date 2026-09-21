# CS 101 · Project 1
## Data Analysis Tool

**Assigned:** Friday 13 November 2026, 10:00 · Week 7
**Due:** Friday 27 November 2026, 17:00 · Week 9 — late penalty from 17:01
**Weight:** Half of the 10% Projects component
**Submission:** `weather.py` and `report.md` in `"$CS101/project1"`, committed to the Freshman Fall repo with incremental commits
**Collaboration:** Individual — no partners, no code sharing
**Expected time:** about 8–10 hours over two weeks

---

## Overview

You will write a program that takes a season of messy daily weather records, cleans them, analyses them
with **your own** search, sort and statistics code, finds a streak with a Week 7 data structure, and prints
a report. It brings together Weeks 0–7: strings and conversion, `try`/`except ValueError`, loops,
functions, recursion, searching and sorting, analysis, and stacks/queues.

**What it deliberately does not need:** reading or writing files (Week 10), dictionaries or sets (Week 8),
your own modules. The data is given to you as a list of text lines, exactly as they would appear in a CSV
file, so you do the parsing yourself with `split(",")`.

---

## Part 1: The Data

`project1_starter.py` (this week's `assignments/` folder) begins with `ROWS`, a list of 122 strings: a
header and **121 daily records** from 1 January to 29 April 2024.

```
date,high_temp,low_temp,precipitation,humidity
2024-01-01,37.2,29.0,0.03,70
2024-01-02,39.1,24.4,0.1,55
...
```

The data is **deliberately messy**. Somewhere in it there are:
- empty fields
- fields that are not numbers
- a row with the wrong number of fields
- physically implausible rows (humidity above 100, a low above that day's high)
- a date that appears twice

Your report must say how you handled each kind, and why.

---

## Part 2: Required Features

Copy `project1_starter.py` to `"$CS101/project1/weather.py"` and build on it. One file, many small functions.

### 2.1 Loading and validation

- `parse_row(line)` — return a record `(date, high, low, precipitation, humidity)` as a tuple, or a
  short string naming why the row was rejected (`"missing value"`, `"not a number"`, …). Use the
  `try`/`except ValueError` idiom around the conversions.
- Remove duplicate dates **without a dict or set**: sort the records by date with your merge sort, then
  compare neighbours.
- Print a **data-quality summary**: rows read, rows kept, and each rejected row with its reason.

### 2.2 Statistics (your own code — no `statistics` module)

- For `high` and `low`: mean, median, minimum, maximum, and standard deviation.
- The date of the highest high and of the lowest low.
- The average high for each month: keep a list of twelve `[total, count]` pairs indexed by month number.

### 2.3 Searching and sorting (your own implementations from Week 5)

- Sort the records by `high` with your **merge sort** and print the five hottest days.
- Use your **binary search** (the "first index with value ≥ x" variant, L16 §6) on the sorted list to
  answer "how many days had a high between 60 and 65 inclusive?" — without scanning every record.

### 2.4 A streak with a Week 7 structure

Find the longest run of consecutive records with `high > 70`. Hold the current run in an `ArrayQueue`,
`LinkedQueue` or `collections.deque` (L24) and explain in your report why a queue fits: the run grows at
the back and is cleared when it breaks.

### 2.5 The report

Print one readable report: the quality summary, the statistics, the five hottest days, the range-query
answer, the longest streak, and an ASCII bar chart of the monthly average highs using `█`.

---

## Part 3: Design Requirements

1. **Small functions.** Each does one thing (L12 §1–2). `main()` only calls them in order.
2. **A docstring on every function**, with its cost in terms of `n` where it loops or sorts.
3. **No crash on bad data.** Every conversion that can fail is inside `try`/`except ValueError`.
4. **Recursion once, where it fits** — your merge sort counts.
5. **A real use of a Week 7 structure** — the streak (2.4).
6. **Your own sort and search** for 2.2's median and 2.3. Built-in `sorted()` is not allowed for these.

---

## Part 4: The Written Report (`report.md`, 600–1,000 words)

1. **Design** — how the functions fit together.
2. **Data handling** — each kind of bad row, and what you did about it.
3. **Costs** — the Θ-bound of loading, de-duplicating, sorting, the range query and the streak.
4. **Data structures** — why a queue for the streak, and why sorting is how you find duplicates without a dict.
5. **Findings** — three real observations from the data.
6. **Testing** — how you checked `parse_row` on each kind of bad line.

---

## Grading Rubric

| Component | Weight | Criteria |
|-----------|--------|----------|
| Code organisation | 15% | small single-purpose functions, docstrings with costs |
| Loading and validation | 20% | every bad row caught with the right reason; duplicate removed; summary correct |
| Statistics | 15% | all values correct, own code |
| Search and sort | 15% | own merge sort and binary search used; range query does not scan |
| Streak | 10% | correct run, genuine queue use |
| Printed report | 10% | complete, readable, bar chart |
| Written report | 15% | all six sections, accurate costs |
| **Total** | **100%** | |

---

## Timeline Suggestion

| By | What |
|----|------|
| Tue 17 Nov | `parse_row` and the quality summary |
| Fri 20 Nov | statistics and merge sort |
| Tue 24 Nov | binary-search range query and streak |
| Thu 26 Nov | printed report; draft `report.md` |
| Fri 27 Nov, 17:00 | final checks and submit |

---

## Academic Integrity

You may discuss approaches and Python syntax, and ask TAs for debugging help. You may not share code,
use AI tools to write your implementation, or use `pandas`, `numpy` or `statistics`.

---

*CS 101 · Project 1 · Assigned Friday 13 November, due Friday 27 November 2026, 17:00 · © CSE Department*
