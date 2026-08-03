# CS 102 · Lab 10
## Building a Plagiarism Detector

**Week 10 · 2-hour lab session · 40 points**
**Deliverable:** `lab10.py` and `RESULTS.md`. In-lab checkoff by your TA.

> **Labs carry no direct weight** in CS 102, but **you must satisfactorily complete at least 10 of
> the 13 labs to pass the course.** See the syllabus.
> **MIDTERM 2 is this week. PROJECT 2 is assigned this week.**

---

## Purpose

Plagiarism detection is document fingerprinting: hash every $k$-character substring, compare the sets.
The algorithm is Week 10's rolling hash and about fifteen lines.

**Everything that matters is the choice of $k$**, and Part B makes you find it by measurement. Too
small and unrelated documents look similar; too large and a few word changes destroy the signal. There
is a window in between, and it is not where most people guess.

---

## Part A — Fingerprinting (12 pts)

**A1.** *(3)* `kgrams(s, k)` returning every length-$k$ substring, and `fingerprint(s, k)` returning
the **set** of their hashes. Use `hashlib.blake2b(..., digest_size=8)`.

**A2.** *(3)* `jaccard(a, b)` $= |a \cap b| / |a \cup b|$ and `containment(a, b)` $= |a \cap b| / |a|$.

State in one sentence when containment is the better measure.

**A3.** *(6)* Build four documents from a **3,000-word** vocabulary with Zipf-like frequencies
(weight $1/(i+1)$ for the $i$-th word), each 600 words:

- **A** — the reference, seed 1;
- **B** — unrelated, seed 2;
- **C** — identical to A;
- **D** — A with **20%** of its words replaced at random (seed 7);
- **E** — B with the **first 180 words of A** spliced into the middle.

Report each document's length and the number of distinct $k$-grams at $k = 25$.

> The vocabulary size matters. With a 20-word vocabulary, unrelated documents score above 0.5 and the
> detector is useless — Part B shows why.

---

## Part B — Choosing $k$ (12 pts)

**B1.** *(6)* For $k \in \{5, 10, 20, 40\}$, report the Jaccard similarity of A against each of C, D,
E and B — a four-by-four table.

**B2.** *(4)* Define **separation** = (score for E, the 30% copy) − (score for B, unrelated).

Report it for each $k$ and identify the best. Then explain **both** failure directions in one sentence
each:

- why small $k$ makes unrelated documents look similar;
- why large $k$ makes the 20%-edited document look unrelated.

**B3.** *(2)* At your chosen $k$, report Jaccard **and** containment for all four comparisons.

Say which you would use to accuse a student, and why.

---

## Part C — Winnowing (8 pts)

Storing every $k$-gram hash is $\Theta(n)$ per document. **Winnowing** keeps only some: slide a window
of $w$ consecutive hashes and keep the **minimum** of each window.

**C1.** *(4)* `winnow(s, k, w)`. Report, at $k = 25$ and $w = 8$, how many fingerprints it keeps for
document A, as a count and a percentage of the unwinnowed set.

**C2.** *(4)* Repeat B3 with winnowed fingerprints. Report the four Jaccard scores alongside the
unwinnowed ones.

Then answer: **the scores barely change while the index shrinks by nearly 80%.** Why does taking a
minimum preserve matches — what property must two documents' winnowed sets share if they contain a
common substring longer than $k + w$?

---

## Part D — Judgement (8 pts)

**D1.** *(3)* Your detector reports a Jaccard score. A student is accused on the basis of it.

Give **two** distinct ways a high score can arise without plagiarism, and **one** way plagiarism can
produce a low score.

**D2.** *(3)* Real systems normalise before fingerprinting — lowercase, strip whitespace and
punctuation, and sometimes replace identifiers with a placeholder.

Say what each normalisation defeats, and what new false positives each creates.

**D3.** *(2)* Your detector compares two documents. A cohort of 300 submissions needs all pairs.

State the number of comparisons, and one thing you would change about the design to make that feasible.

---

## Submission

- `lab10.py` — runnable end to end, producing every table.
- `RESULTS.md` — the tables and answers. **Include your machine and Python version.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 12 | Fingerprinting, and a corpus that can discriminate |
| B | 12 | Choosing $k$ by measurement |
| C | 8 | Winnowing, and why it preserves matches |
| D | 8 | What the number does and does not mean |
| **Total** | **40** | |

---

## Reference Numbers

3,000-word Zipf vocabulary, 600-word documents, seeds as specified. Python 3.14 on x86-64 Linux.
**Deterministic** given the same generator.

**B1 — Jaccard similarity of A against each document**

| $k$ | identical | 20% changed | 30% chunk | unrelated | **separation** |
| --- | --- | --- | --- | --- | --- |
| 5 | 1.000 | 0.663 | 0.390 | 0.284 | 0.106 |
| 10 | 1.000 | 0.487 | 0.202 | 0.063 | 0.140 |
| **20** | 1.000 | 0.310 | 0.148 | **0.001** | **0.148** |
| 40 | 1.000 | **0.157** | 0.146 | 0.000 | 0.146 |

*(Separation is computed from unrounded scores; subtracting the rounded columns differs by up to
0.001.)*

**Read the two end rows.** At $k=5$ unrelated documents score **0.284** — the detector cannot
distinguish them from a real 30% copy at 0.390. At $k=40$ the 20%-edited document has collapsed to
**0.157**, barely above a genuine copy.

**B3 — at $k = 25$**

| comparison | Jaccard | containment |
| --- | --- | --- |
| identical | 1.000 | 1.000 |
| 20% words changed | 0.257 | 0.409 |
| 30% chunk copied | 0.147 | 0.296 |
| unrelated | **0.000** | **0.000** |

**C1 / C2 — winnowing, $k = 25$, $w = 8$**

Document A: **3,575** $k$-grams → **801** fingerprints (**22%**).

| comparison | Jaccard, winnowed | Jaccard, full |
| --- | --- | --- |
| identical | 1.000 | 1.000 |
| 20% words changed | 0.246 | 0.257 |
| 30% chunk copied | 0.147 | 0.147 |
| unrelated | 0.000 | 0.000 |

---

## A Note on What This Lab Is Really Testing

The algorithm is fifteen lines and there is nothing to get wrong in it. **Part B is the lab.**

A detector with $k = 5$ gives unrelated documents a similarity of 0.284 and a genuine partial copy
0.390. Those distributions overlap, and a threshold placed anywhere between them accuses innocent
students and misses guilty ones. **The algorithm is correct and the system does not work**, and the
only way to find that out is to run it against a case you know the answer to.

At $k = 20$ unrelated documents score **0.001**. Same algorithm, same code, one parameter.

**Part D is the other half.** The output is a number, and a number is not evidence. Two students given
the same assignment, the same textbook and the same standard library will share long passages
legitimately; a plagiarist who paraphrases will score low. **A detector produces candidates for a human
to examine**, and a system that treats its score as a verdict is worse than no system, because it is
wrong with an air of authority.

That distinction — between an algorithm's output and a decision — is the last thing this course has to
say about applying any of it.

---

*CS 102 · Week 10 · Lab 10 · © CSE Department*
