# CS 101 · Reading Guide, Week 12
## Synthesis, Review, and the Path Forward

---

## The Week in One Sentence

The course closes by showing that its eleven topics were one idea applied eleven times — build a
layer, find where it leaks — then maps what was left out and why.

---

## What Is Different About This Week

There is no new technical material and no problem set. Week 12 carries three things instead:

| | |
|---|---|
| **The Final Exam** | Covers Weeks 1–11, 25% of your grade |
| **Project 2 due** | Friday 18 December, 17:00 |
| **Three lectures** | Synthesis (L37), the map of the field (L38), the practice of programming (L39) |

The lectures are not examinable. Attend them anyway — L37 is the most efficient revision session of
the term, because it organises everything you already know into a structure you can actually hold in
your head.

---

## Priorities, In Order

**1. Project 2, if it is not finished.** It is due Friday and it is 5% of your grade. The algorithms
carry hard correctness requirements — get `project2_starter.py` to 15/15 before doing anything else.

**2. The practice exam, under exam conditions.** Three hours, one sheet of notes, no looking at the
key. This is worth more than any amount of re-reading, because it tells you *specifically* where you
are weak instead of leaving you with a general feeling of unpreparedness.

**3. Whatever the practice exam exposed.** Not the topics you enjoy revising.

**4. L37.** Read it once before the exam. The four threads in §2 are the connective tissue the exam's
longer questions test.

---

## How to Revise for This Exam

**Do not re-read lecture notes front to back.** Recognition is not recall, and re-reading produces
the strongest possible illusion of the two being the same.

**Do this instead:**

- **Work the practice exam cold**, then mark yourself honestly against the key
- **Redo problem-set questions you got wrong** the first time — the marked-up copies are the highest
  value revision material you own
- **Explain a topic out loud** without notes. Hash tables, or the halting problem. Where you stall
  is where the gap is
- **Rebuild one thing from scratch** — a hash table, merge sort, `atomic_write`. Twenty minutes of
  this beats two hours of reading

**The one-sheet note strategy.** You are permitted one double-sided handwritten A4 sheet. *Making*
the sheet is the revision; the sheet itself is almost incidental. Put on it what you cannot derive:
the exact constants (n(n−1)/2), the `atomic_write` requirements, the 7-tuple, the exception
hierarchy. Do not waste space on things you can reconstruct.

---

## Exam Topic Weights

| Area | Weeks | ~Share |
|---|---|---|
| Foundations: types, control flow, functions | 1–3 | 15% |
| Recursion | 4 | 10% |
| Searching and sorting | 5 | 15% |
| **Complexity analysis** | 6 | **20%** |
| **Data structures** | 7–8 | **20%** |
| Strings and regex | 9 | 10% |
| Files and exceptions | 10 | 10% |
| Computability | 11 | 10% |

Weeks 6–8 are 40% between them. If revision time is short, that is where it goes.

---

## The Nine Marks Most Commonly Lost

From the review guide, worth reading twice:

1. Confusing "always halts" with "answers correctly"
2. Reducing in the **wrong direction**
3. Quoting Big-O without stating the case
4. Saying "O(1) lookup" without conditions
5. Forgetting `open(path, "w")` truncates **at open**
6. `except` clauses ordered general-before-specific
7. Conflating code points, bytes, and graphemes
8. Claiming a regex can match nested structure
9. Giving a complexity without saying what **n** counts

---

## Reading

**For the exam:** the practice exam, and your own marked problem sets. Nothing else has better
return.

**For L37–L39** (optional, none examinable):

- **Brooks, "No Silver Bullet"** (1986) — essential vs accidental complexity; 15 pages
- **Kernighan & Pike, *The Practice of Programming*** — the best companion to L39
- **Ulrich Drepper, "What Every Programmer Should Know About Memory"** — L38's caching claim, at
  length

**For the holiday**, if you want one thing: pick a small tool you actually use and read its source.
That is L39's real assignment, and it is the fastest way to close the gap between coursework and
practice.

---

## After the Exam

L38 maps where each thread continues. The short version:

- **CS 102** — object-oriented design, next semester
- **CS 210** — testing and software engineering as a discipline
- **CS 230 / CS 250** — the layers below: architecture, then operating systems and concurrency
- **CS 301** — the pumping lemma, the Chomsky hierarchy, P vs NP; Week 11 done properly

And the advice from L38 §5 that is not about courses: **build something nobody assigned**, and
**learn a language that argues with you**.

---

*CS 101 · Week 12 · Reading Guide · © CSE Department*
