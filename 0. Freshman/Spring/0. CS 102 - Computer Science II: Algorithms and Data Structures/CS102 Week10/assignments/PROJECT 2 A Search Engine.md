# CS 102 · Project 2
## A Search Engine

**Assigned:** Week 10 · **Due:** Friday, Week 12, 23:59
**10% of the final grade**

**Submit:** a repository or archive containing `index.py`, `search.py`, `mysearch.py` (a runnable
command-line tool), `test_search.py`, and `REPORT.md` (3,000 words maximum).

---

## The Brief

Build a search engine over a document corpus: index it once, then answer queries fast.

Project 1 was one algorithm made production-ready. **This one is an assembly** — it uses Week 10's
indexing, Week 7's edit distance, Week 3's heaps, and Week 9's compression, and the work is in making
them fit together and in measuring what each contributes.

No search or indexing libraries. `heapq`, `bisect`, `collections`, `math`, `zlib` and the standard
data structures are all fine.

---

## Part 1 — The Corpus and the Inverted Index (25 marks)

**1.1** *(5)* `build_corpus(n_docs=2000, seed=11)` generating reproducible documents. Specify your
generator precisely in the report so your figures can be checked.

Each document needs an id, a title and a body of a few hundred words, with a **Zipf-like** word
distribution — real text has a few very common words and a long tail, and a uniform corpus will make
every later measurement meaningless.

**1.2** *(12)* An **inverted index**: a map from term to the sorted list of document ids containing
it, plus the within-document term frequency.

Report: vocabulary size, total postings, and the index's size in memory against the corpus's.

**1.3** *(8)* Boolean queries — `AND`, `OR`, `NOT` — over the postings lists.

**`AND` must merge two sorted lists in linear time**, not intersect sets. Report the query time for a
common-term pair and a rare-term pair, and explain the difference.

---

## Part 2 — Ranking (20 marks)

**2.1** *(10)* **TF–IDF** scoring: rank matching documents by
$\sum_{t \in q} \mathrm{tf}(t,d)\cdot\log\frac{N}{\mathrm{df}(t)}$.

Return the top $k$ using a **bounded heap of size $k$** — Week 3 Lecture 12 §4 — not by sorting all
scores. Report the difference in work for $k = 10$ over 2,000 documents.

**2.2** *(6)* **Phrase queries** — `"exact phrase"` — using positional postings.

**2.3** *(4)* Explain in the report why IDF is a logarithm. What goes wrong with $N/\mathrm{df}$ alone?

---

## Part 3 — Substring and Fuzzy Search (25 marks)

**3.1** *(10)* A **suffix array** over the concatenated corpus, supporting substring queries that are
**not** word-aligned.

Report construction time and index size, and give a query the inverted index cannot answer but this
can.

**3.2** *(10)* **Fuzzy search**: given a misspelled query term, return vocabulary terms within edit
distance $\le 2$.

The obvious implementation compares against every vocabulary term. **Make it faster** — a length
filter and a first-character bucket are enough — and report the speedup and the number of candidates
eliminated.

**3.3** *(5)* Verify that your fuzzy search returns exactly the terms a brute-force scan returns, on at
least 200 queries. Report mismatches.

---

## Part 4 — Compression (10 marks)

**4.1** *(6)* Postings lists are sorted integers. Apply **delta encoding** — store gaps rather than
absolute ids — then **variable-byte encoding**.

Report the index size before and after, and the compression ratio.

**4.2** *(4)* Compare against `zlib.compress` on the raw postings. Report both, and explain in two
sentences why a general-purpose compressor is or is not better here.

---

## Part 5 — The Report (20 marks)

`REPORT.md`, **3,000 words maximum**.

**5.1** *(4)* **The design.** One diagram or structured list showing what is built at index time and
what happens per query, with the complexity of each stage.

**5.2** *(6)* **The measurements.** Every table from Parts 1–4, each with a sentence saying what it
shows. Include your machine and Python version.

**5.3** *(6)* **The decisions.** For each, what you chose and why:

- an inverted index cannot answer substring queries and a suffix array cannot rank by term frequency.
  **You built both.** When would you ship only one?
- your fuzzy search has a threshold of 2. What breaks at 1, and at 3?
- your ranking ignores document length. Show a query where that gives a bad result, and say what you
  would do about it.

**5.4** *(4)* **The limits.** Give a query class your engine handles badly, with a measurement. Say
what you would change if the corpus were 10,000× larger.

---

## Marking

| Part | Marks | Focus |
| --- | --- | --- |
| 1 | 25 | The index and boolean retrieval |
| 2 | 20 | Ranking, and top-$k$ without sorting |
| 3 | 25 | Substring and fuzzy search |
| 4 | 10 | Postings compression |
| 5 | 20 | Judgement, in writing |
| **Total** | **100** | scaled to 10% of the course |

**Correctness gates the rest.** If Part 1.3's boolean queries return wrong document sets, the project
cannot score above 40 however good the report — everything above is built on the index.

---

## Practical Notes

**Start Part 1 this week.** It is an evening's work and Parts 2–4 all sit on top of it. The failure
mode for this project is students who begin in Week 12.

**Verify against brute force everywhere.** Every part of this project has a slow obviously-correct
version: scan every document, compare every term, sort every score. Write those first and keep them as
test oracles — they are the only thing that will tell you your fast version is right.

**Measure what you claim.** The report is 20 marks and most of them are for tables with a sentence
attached. A claim of "much faster" without a number scores nothing.

**Reuse your own code.** Week 3's bounded heap, Week 7's edit distance, and Week 9's compression are
all yours already. Say in the report which parts you reused.

**Collaboration.** Discussing approaches is encouraged; sharing code is not. The report must be
entirely your own.

---

## Why This Project

Every part of it is a data structure you have already met, chosen for a property you have already
proved. What is new is that **the parts constrain each other**: the inverted index makes ranking easy
and substring search impossible; the suffix array does the reverse; compressing the postings makes them
smaller and the merge slower.

That is the difference between a course and a system. In a problem set the question tells you which
structure to use. Here **the question is which structure to use**, and Part 5.3 is where you have to
defend it.

---

*CS 102 · Project 2 · © CSE Department*
