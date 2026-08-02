# CS 101 — Project 1
## Data Analysis Tool

**Assigned:** Friday, Week 7
**Due:** Friday, Week 9 at 11:59 PM
**Weight:** 5% of final grade (half of the 10% Projects grade)
**Submission:** A zip file containing all source code, a `README.md`, and a written report (`report.md`)
**Collaboration:** Individual project — no partners, no code sharing

---

## Overview

You will build a **command-line data analysis tool** that reads a dataset from a CSV file, performs statistical analysis, detects patterns, and produces a formatted report — entirely using the skills from Weeks 0–7: types, control flow, functions, recursion, algorithms (searching/sorting), complexity analysis, and now, data structures (stacks, queues, linked lists).

This is not a toy exercise. This project is intentionally designed to require you to **synthesize** nearly everything covered so far, the way a real engineering task would.

---

## Learning Objectives

By completing this project, you will demonstrate the ability to:
- Decompose a non-trivial problem into well-designed, single-responsibility functions
- Read and parse real-world (messy) data from a file
- Apply your own searching and sorting implementations to real data, and justify their use
- Use appropriate data structures (from Week 7) where they provide a genuine advantage
- Perform statistical analysis without relying on external libraries (no `pandas`, no `numpy`)
- Write clear specifications (docstrings) and test your code systematically
- Communicate your design decisions in written form (the report)

---

## Part 1: The Dataset

You will analyze a CSV file of **daily temperature records** for a city over one year (365 or 366 rows). A sample dataset (`weather_data.csv`) is provided in the `resources/` folder of this project package. Each row has:

```
date,high_temp,low_temp,precipitation,humidity
2024-01-01,42.5,28.3,0.0,65
2024-01-02,38.1,25.7,0.15,72
2024-01-03,-5.2,-12.8,0.02,58
...
```

**Important — the data is deliberately messy.** It contains:
- Missing values (empty fields)
- A few malformed rows (wrong number of columns, non-numeric values where numbers are expected)
- Duplicate date entries (same date appears twice, possibly with different values)
- Values that are technically parseable but physically implausible (e.g., humidity > 100%, or a low_temp higher than the same row's high_temp) — you must detect and flag these, not silently accept them

**Part of the assignment is deciding how to handle this messiness** — your report must justify your approach (skip the row? use a placeholder? interpolate?).

---

## Part 2: Required Features

Your tool must implement the following. Organize your code into clearly separated modules/functions — do NOT write one giant script.

### 2.1 — Data Loading and Validation (Required)

- `load_data(filepath)` — read the CSV, parse each row into a structured record (you may use a simple class, a named tuple, or a dictionary — your choice, justify it in the report)
- `validate_record(record)` — return True if the record is well-formed and physically plausible; False otherwise
- Produce a **data quality report**: how many rows were read, how many were valid, how many were rejected and why (categorize: missing fields, malformed numbers, implausible values, duplicates)

### 2.2 — Statistical Analysis (Required)

Using **only your own implementations** (no `statistics` module, no `numpy`):

- Mean, median, mode, min, max, range, standard deviation for `high_temp`, `low_temp`, `precipitation`, and `humidity`
- The date of the highest recorded `high_temp` and the lowest recorded `low_temp`
- Month-by-month averages for each metric (you'll need to parse the date and group by month)

### 2.3 — Searching and Sorting (Required — must use YOUR implementations)

- Implement and use **your own binary search** (from Week 5) to answer queries like "find all days where high_temp was between X and Y" — this requires sorting first
- Implement and use **your own merge sort or quicksort** (from Week 5) to sort records by any field (e.g., "show the 10 hottest days of the year")
- Your report must state the Big-O complexity of each operation you perform on the dataset, in terms of n (number of records)

### 2.4 — Streak Detection Using a Stack or Queue (Required — must use Week 7 structures)

Implement at least ONE of the following, using an appropriate Week 7 data structure (Stack, Queue, or Deque — not just a plain list doing the same job):

- **Longest heat streak:** the longest consecutive run of days where `high_temp` exceeded some threshold (e.g., 90°F). Use a stack or running-window technique to track streak boundaries efficiently.
- **Sliding window analysis:** for a given window size k (e.g., 7 days), compute the maximum `high_temp` in every k-day window across the year, using a `deque` to maintain a monotonic window in O(n) total time (not O(nk)) — this is the "sliding window maximum" problem previewed in PS7's challenge section.

Choose ONE; document your choice and why the data structure you picked is appropriate (not just "a list would also work" — explain the genuine advantage).

### 2.5 — Report Generation (Required)

Produce a formatted, readable text report (printed to console AND saved to a file `analysis_report.txt`) containing:
- The data quality summary (from 2.1)
- All statistics (from 2.2)
- At least 3 interesting findings from your searching/sorting/streak analysis (from 2.3/2.4)
- A simple ASCII visualization of SOMETHING (e.g., a bar chart of monthly average temperatures using `█` characters, similar to techniques from earlier problem sets)

---

## Part 3: Design Requirements (Non-Negotiable)

These reflect the engineering discipline built across Weeks 0–7:

1. **No monolithic functions.** Every function should do one identifiable thing (Week 3, Single Responsibility Principle).
2. **Every function has a docstring** stating purpose, args, returns, and (where relevant) time complexity.
3. **No unhandled crashes on malformed input.** Your program must never raise an uncaught exception when given the messy dataset — validate and handle gracefully (preview of Week 10, but basic `try/except` for file/parsing errors is fair game now; ask if unsure).
4. **You must use recursion at least once**, somewhere genuinely appropriate (not forced) — document where and why in your report.
5. **You must use at least one of: Stack, Queue, or Deque** from Week 7 in a way that provides genuine benefit over a plain list (not cosmetic).
6. **Your own sorting and searching implementations must be used** — not Python's built-in `sorted()` — for the core analysis operations in 2.3. (You MAY use built-ins for incidental, non-analytical purposes, like sorting a small list of category names for display — use judgment and document choices.)

---

## Part 4: The Written Report (`report.md`)

Your report (1,000–1,500 words) must include:

1. **Design Overview** — how you organized your code, and why
2. **Data Handling Decisions** — how you validated/cleaned the messy data, and your justification
3. **Complexity Analysis** — for each major operation (loading, sorting, searching, streak detection), state and justify the Big-O
4. **Data Structure Justification** — which Week 7 structure(s) you used, where, and why they were the right choice over a plain list
5. **Recursion Usage** — where you used recursion and why it was appropriate there
6. **Interesting Findings** — at least 3 genuine observations from your analysis of the actual dataset
7. **What You Would Do Differently** — with more time/tools (e.g., "with dictionaries from Week 8, I could have done X faster")
8. **Testing Summary** — how you tested your code, and what edge cases you specifically checked

---

## Grading Rubric

| Component | Weight | Criteria |
|-----------|--------|----------|
| **Architecture & code organisation** | 15% | Logical modules, clear separation of concerns, no monolithic file; functions do one thing |
| Data loading & validation | 15% | Correctly handles all forms of messiness; produces accurate quality report |
| Statistical analysis | 15% | All statistics correct, computed without banned libraries |
| Search & sort usage | 15% | Uses own implementations correctly; correct complexity claims |
| Stack/Queue/Deque application | 15% | Genuine, justified use; correct implementation |
| Report generation | 10% | Clear, complete, correctly formatted output (console + file) |
| Written report | 15% | All 8 sections present, thoughtful, technically accurate |
| **Total** | **100%** | |

*(Note: the percentage breakdown above reflects THIS project's internal grading. Refer to the course syllabus for how Project 1 contributes to your overall course grade — 5% of the final grade, per the Assessment Breakdown.)*

---

## Submission Checklist

- [ ] All source code (`.py` files), organized into logical modules
- [ ] `README.md` — brief instructions on how to run your tool
- [ ] `report.md` — the full written report (1,000–1,500 words)
- [ ] `analysis_report.txt` — a sample output of your generated report, checked in for grading convenience
- [ ] Test file(s) demonstrating your validation logic against the messy dataset
- [ ] Everything zipped into a single submission file
- [ ] All code committed to Git with meaningful commit messages showing incremental progress (not one giant commit the night before)

---

## Timeline Suggestion

| By when | What |
|---------|------|
| End of Week 7 | Read the dataset, write `load_data` and `validate_record`, produce the data quality report |
| End of Week 8 | Implement all statistics, integrate your own sort/search from Week 5 |
| Mid Week 9 | Implement the streak/window detection using a Week 7 structure |
| 2 days before due | Full report generation working end-to-end; begin writing `report.md` |
| Due date | Final polish, testing edge cases, submit |

**Do not start this the night before.** The scope is deliberately broad enough that last-minute work will be visibly rushed in both code quality and the written report.

---

## Academic Integrity Note

This is an individual project. You may:
- Discuss general approaches and Python syntax questions with classmates
- Ask TAs and the professor for help debugging

You may NOT:
- Share code with another student
- Use AI tools to generate your implementation
- Use `pandas`, `numpy`, or the `statistics` module for the required analysis (the entire point is implementing these yourself, using what you've learned)

If you are unsure whether something is permitted, ask before doing it.

---

*CS 101 · Project 1 · Assigned Week 7, Due Week 9 · © CSE Department*
