# CS 102 · Project 2
## A Search Engine

**Assigned:** Monday 29 March 2027, 09:00 (at L31) · Week 10
**Due:** Friday 16 April 2027, 17:00 · Week 12 — late penalty from 17:01
**10% of the final grade**

**Submit:** a repository or archive containing `index.py`, `search.py`, `mysearch.py` (a runnable
command-line tool), `test_search.py`, and `REPORT.md` (2,500 words maximum).

## What this project uses

Week 3's bounded heap for top-$k$ (L12 §4), Week 7's edit distance (L23), Week 10's suffix array and
its binary-search query (L33), and the merge step of merge sort (CS 101) for intersecting sorted
lists. The inverted index is a `dict` of lists (CS 101 Week 8), and it is defined below. The
command-line lines you need are the two from Project 1.

**Not needed and not expected:** TF–IDF weighting, phrase queries, postings compression, `zlib`, or
any tokeniser beyond lower-casing and splitting on spaces.

---

## The Brief

Build a search engine over a document corpus: index it once, then answer queries fast.

Project 1 was one algorithm made production-ready. **This one is an assembly** — it uses Week 10's
suffix array, Week 7's edit distance and Week 3's heaps, and the work is in making them fit together
and in measuring what each contributes.

No search or indexing libraries. `heapq`, `bisect`, `collections`, `random`, `time` and the standard
data structures are all fine.

---

## Part 1 — The Corpus and the Inverted Index (30 marks)

**1.1** *(5)* `build_corpus(n_docs=2000, seed=11)` generating reproducible documents: `random.seed(seed)`
once, then for each document an id, a title and a body of a few hundred words drawn with
`random.choices(words, weights=w)` from a vocabulary of at least 3,000 words with Zipf-like weights
$w_i = 1/(i+1)$ — the call Lab 9 used to build its corpus. Specify your vocabulary in the report so your
figures can be checked. A uniform corpus will make every later measurement meaningless.

**1.2** *(15)* An **inverted index**: a `dict` from each term to the **sorted list** of document ids
containing it, together with the number of times the term occurs in each of those documents.

Report: vocabulary size, total postings (the sum of all list lengths), and the index's size in memory
against the corpus's, measured with `sys.getsizeof` as in Lecture 13 §4.

**1.3** *(10)* Boolean queries — `AND`, `OR`, `NOT` — over the postings lists.

**`AND` must merge two sorted lists in linear time**, the way merge sort's merge walks two lists —
not by converting to sets. Report the query time for a common-term pair and a rare-term pair, and
explain the difference.

---

## Part 2 — Ranking (15 marks)

**2.1** *(10)* Score each matching document by the **total number of occurrences** of the query terms in
it, and return the top $k$ using a **bounded heap of size $k$** — Week 3 Lecture 12 §4 — not by sorting
all scores. Report the difference in work for $k = 10$ over 2,000 documents.

**2.2** *(5)* Give a query for which this ranking is clearly wrong, and explain why in two sentences.

---

## Part 3 — Substring and Fuzzy Search (30 marks)

**3.1** *(12)* A **suffix array** over the concatenated corpus, supporting substring queries that are
**not** word-aligned.

Report construction time and index size, and give a query the inverted index cannot answer but this
can.

**3.2** *(12)* **Fuzzy search**: given a misspelled query term, return vocabulary terms within edit
distance $\le 2$.

The obvious implementation compares against every vocabulary term. **Make it faster** — a length
filter and a first-character bucket are enough — and report the speedup and the number of candidates
eliminated.

**3.3** *(6)* Verify that your fuzzy search returns exactly the terms a brute-force scan returns, on at
least 200 queries. Report mismatches.

---

## Part 4 — The Report (25 marks)

`REPORT.md`, **2,500 words maximum**.

**4.1** *(5)* **The design.** One diagram or structured list showing what is built at index time and
what happens per query, with the complexity of each stage.

**4.2** *(8)* **The measurements.** Every table from Parts 1–3, each with a sentence saying what it
shows. Include your machine and Python version.

**4.3** *(7)* **The decisions.** For each, what you chose and why:

- an inverted index cannot answer substring queries and a suffix array cannot count terms per
  document. **You built both.** When would you ship only one?
- your fuzzy search has a threshold of 2. What breaks at 1, and at 3?
- your ranking ignores document length. Show a query where that gives a bad result, and say what you
  would do about it.

**4.4** *(5)* **The limits.** Give a query class your engine handles badly, with a measurement. Say
what you would change if the corpus were 10,000× larger.

---

## Marking

| Part | Marks | Focus |
| --- | --- | --- |
| 1 | 30 | The index and boolean retrieval |
| 2 | 15 | Ranking, and top-$k$ without sorting |
| 3 | 30 | Substring and fuzzy search |
| 4 | 25 | Judgement, in writing |
| **Total** | **100** | scaled to 10% of the course |

**Correctness gates the rest.** If Part 1.3's boolean queries return wrong document sets, the project
cannot score above 40 however good the report — everything above is built on the index.

---

## Practical Notes

**Start Part 1 this week.** It is an evening's work and Parts 2–3 sit on top of it. The failure mode
for this project is students who begin in Week 12.

**Verify against brute force everywhere.** Every part of this project has a slow obviously-correct
version: scan every document, compare every term, sort every score. Write those first and keep them as
test oracles — they are the only thing that will tell you your fast version is right.

**Measure what you claim.** The report is 25 marks and most of them are for tables with a sentence
attached. A claim of "much faster" without a number scores nothing.

**Reuse your own code.** Week 3's bounded heap, Week 7's edit distance and PS 10's suffix array are all
yours already. Say in the report which parts you reused.

**Collaboration.** Discussing approaches is encouraged; sharing code is not. The report must be
entirely your own.

---

## Why This Project

Every part of it is a data structure you have already met, chosen for a property you have already
proved. What is new is that **the parts constrain each other**: the inverted index makes counting and
ranking easy and substring search impossible; the suffix array does the reverse.

That is the difference between a course and a system. In a problem set the question tells you which
structure to use. Here **the question is which structure to use**, and Part 4.3 is where you have to
defend it.

---

*CS 102 · Project 2 · © CSE Department*
