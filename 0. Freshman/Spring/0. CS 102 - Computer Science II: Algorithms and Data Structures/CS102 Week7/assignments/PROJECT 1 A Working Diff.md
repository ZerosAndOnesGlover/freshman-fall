# CS 102 · Project 1
## A Working `diff`

**Assigned:** Week 7 · **Due:** Friday, Week 9, 23:59
**10% of the final grade** — the largest single piece of work this term.

**Submit:** a repository or archive containing
`mydiff.py` (a runnable command-line tool), `align.py` (the algorithms), `test_mydiff.py` (your
tests), and `REPORT.md` (2,500 words maximum).

---

## The Brief

Build a working `diff`: a program that takes two text files and prints the minimal set of line
insertions and deletions that turns the first into the second.

This is Lecture 23's LCS, applied to lines instead of characters. The algorithm is a dozen lines. **The
project is everything around it** — making it correct, making it fast enough, making it usable, and
being able to say what it costs and why.

You are not permitted to use `difflib`, or any library that computes sequence alignment. `sys`,
`argparse`, `time`, `tracemalloc` and the standard data structures are all fine.

---

## Part 1 — The Core Tool (30 marks)

**1.1** *(10)* `lcs(a, b)` over lists of lines, returning the length and one longest common
subsequence, with the $\Theta(nm)$ table and a traceback.

**1.2** *(10)* `diff(a, b)` producing a list of `(tag, line)` pairs with tags `' '`, `'-'`, `'+'`.

Two properties **must** hold, and your tests must check both on random inputs:

- keeping the `' '` and `'+'` lines reconstructs $b$ exactly;
- keeping the `' '` and `'-'` lines reconstructs $a$ exactly.

**1.3** *(10)* A command-line tool: `python mydiff.py FILE1 FILE2`, printing a **unified-style** diff
with `@@` hunk headers and three lines of context, and exiting 0 when the files match and 1 when they
differ (the convention real `diff` uses).

Handle sensibly: empty files, identical files, files with no trailing newline, and files where one is
empty.

---

## Part 2 — Making It Fast Enough (25 marks)

The $\Theta(nm)$ table is unusable on real files. Two standard fixes, both required.

**2.1** *(10)* **Trim common prefixes and suffixes** before running the DP. Real edits touch a small
part of a file, so this alone often reduces the problem by orders of magnitude.

Measure it: generate a 5,000-line file, change 10 lines in the middle, and report the DP problem size
with and without trimming.

**2.2** *(10)* **Hash the lines to integers** once, and run the DP on integers rather than strings.
This is standard advice: comparing machine words should beat comparing strings.

**Measure it** at $n = m = 2{,}000$, and then measure it again with lines that share a 1,000-character
common prefix.

Report both, and **explain what you find.** Two of these ten marks are for the implementation; the
other eight are for the explanation, and the expected answer is not "it made it faster".

Then answer separately: **what breaks if two different lines hash equal**, and what do you do about
it?

> This part is deliberately not a win. Reporting a speedup you did not measure is worse than
> reporting none.

**2.3** *(5)* Report timings for your final tool on line counts
$n = m \in \{500,\ 1000,\ 2000,\ 4000\}$ with 5% of lines changed. Give the doubling ratios and name
the complexity class they indicate.

---

## Part 3 — Linear Space (25 marks)

The full table at $n = m = 50{,}000$ needs $2.5\times10^9$ cells. **Hirschberg's algorithm** recovers
the actual subsequence in $\Theta(nm)$ time and $\Theta(\min(n,m))$ space.

**3.1** *(5)* `lcs_row(a, b)` — the final row of the LCS table in linear space.

**3.2** *(15)* `hirschberg(a, b)` — a full LCS in linear space. The method:

- if either input is empty, return empty; if $a$ has one line, return it if present in $b$;
- otherwise split $a$ at its midpoint;
- compute the last LCS row of $a_{\text{left}}$ vs $b$, and of **reversed** $a_{\text{right}}$ vs
  **reversed** $b$;
- find the split point $k$ of $b$ maximising the sum of the two rows;
- recurse on $(a_{\text{left}}, b[:k])$ and $(a_{\text{right}}, b[k:])$ and concatenate.

**3.3** *(5)* Verify against your Part 1 LCS on at least 300 random pairs — same length, and a genuine
common subsequence of both. Then measure **peak memory** for both at $n = m \in \{200, 500, 1000\}$,
and the **time** cost of the saving.

---

## Part 4 — The Report (20 marks)

`REPORT.md`, **2,500 words maximum**. Marks are for judgement, not length.

**4.1** *(5)* **The algorithm.** State the recurrence, its base cases, and why the greedy match in the
equal-characters case is safe. One page.

**4.2** *(5)* **The measurements.** Your tables from Parts 2 and 3, each with a sentence saying what it
shows. Include your machine and Python version.

**4.3** *(6)* **The design decisions.** For each, say what you chose and why:

- a line-based diff has no *substitution* operation, so a changed line appears as a delete plus an
  insert. Should it? What would change if you added substitution?
- when several LCSs have the same length, yours picks one. Which, and is it the one a human would
  prefer?
- your hashing in 2.2 introduces a possible collision. Argue that your handling is correct, or state
  precisely the conditions under which your tool is wrong.

**4.4** *(4)* **The limits.** Give an input class on which your tool performs badly, with a
measurement. Say what you would do about it if this were going into production.

---

## Marking

| Part | Marks | Focus |
| --- | --- | --- |
| 1 | 30 | A correct, usable tool |
| 2 | 25 | Making it fast, and measuring that you did |
| 3 | 25 | Linear-space recovery |
| 4 | 20 | Judgement, stated in writing |
| **Total** | **100** | scaled to 10% of the course |

**Correctness gates the rest.** A tool that fails the Part 1.2 round-trip properties cannot score above
40 overall, however good the report — a diff that does not reproduce the target file is not a diff.

---

## Reference Numbers

From the machine these notes were prepared on (Python 3.14, x86-64 Linux). Yours will differ; the
**shape** should not.

**Part 3.3 — peak memory**, random sequences over a 4-letter alphabet:

| $n = m$ | full table | Hirschberg | ratio |
| --- | --- | --- | --- |
| 200 | 329 KiB | 12 KiB | 28.6× |
| 500 | 2,139 KiB | 29 KiB | 72.8× |
| 1,000 | **11,695 KiB** | **84 KiB** | **139.6×** |

**Part 3.3 — time cost of that saving:**

| $n = m$ | full table | Hirschberg | ratio |
| --- | --- | --- | --- |
| 200 | 5.1 ms | 6.9 ms | 1.34× |
| 400 | 23.1 ms | 28.0 ms | 1.21× |
| 800 | 104.7 ms | 123.0 ms | 1.18× |

**Two rows, one conclusion: Hirschberg costs about 20% more time and saves two orders of magnitude of
space, and the ratio improves with $n$.** If your time ratio is far worse than this, you are probably
recomputing rows you already have.

**Part 2.1 — trimming**, a 5,000-line file with 10 lines changed in the middle:

| | problem size |
| --- | --- |
| untrimmed | 5,000 × 5,000 = **25,000,000** cells |
| common prefix / suffix found | 2,400 / 2,590 lines |
| trimmed | 10 × 10 = **100** cells |
| reduction | **250,000×** |

**Part 2.2 — hashing**, $n = m = 1{,}200$, varying how much of each line is a shared prefix:

| shared prefix | strings | integers | speedup |
| --- | --- | --- | --- |
| 0 chars | 146.4 ms | 138.9 ms | 1.05× |
| 40 chars | 146.2 ms | 141.3 ms | 1.03× |
| 200 chars | 153.8 ms | 138.8 ms | 1.11× |
| 1,000 chars | 168.3 ms | 142.2 ms | **1.18×** |

**Part 2.3 — scaling**, 5% of lines changed, integers:

| $n$ | time | doubling ratio |
| --- | --- | --- |
| 500 | 22.9 ms | — |
| 1,000 | 101.9 ms | 4.44 |
| 2,000 | 438.6 ms | 4.31 |
| 4,000 | 1,771.9 ms | **4.04** |

Ratio 4 per doubling is $\Theta(n^2)$ — as expected, since trimming does nothing when the changes are
spread through the file.

**A worked example** your tool should reproduce:

```
A: the quick brown fox / jumps over / the lazy dog / end
B: the quick brown fox / leaps over / the lazy dog / the end

  the quick brown fox
 -jumps over
 +leaps over
  the lazy dog
 -end
 +the end
```

---

## Practical Notes

**Start Part 1 this week.** It is two hours' work and everything else depends on it. Parts 2 and 3 are
where the time goes, and Part 3 is where students who left it late lose marks.

**Test against real `diff`.** Your output format need not match GNU `diff` byte for byte, but the
*set* of changed lines should agree. Disagreement is a bug in one of you, and it will not be `diff`.

**Version control your work.** This is a two-week project and the failure mode is a broken working
copy at 22:00 on the due date.

**Collaboration.** Discussing approaches is encouraged; sharing code is not. The report must be
entirely your own, and it is where most of the discrimination between submissions happens.

**Late work** follows the standard course policy in the syllabus.

---

## Why This Project

`diff` is the piece of infrastructure you use most and think about least. Every code review, every
merge, every `git log -p` is this algorithm.

It is also the honest version of what Week 7 teaches. The recurrence takes a lecture; making it work
on a 50,000-line file takes prefix trimming, hashing, and a divide-and-conquer trick that most people
never learn — and none of that is visible from the recurrence. **The gap between "I can write the DP"
and "I have a tool someone would use" is the whole of this project**, and it is a fair sample of what
the rest of the degree is like.

---

*CS 102 · Project 1 · © CSE Department*
