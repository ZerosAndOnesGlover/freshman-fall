# CS 102 · Lab 10 — Solutions and Checkoff Notes
## Building a Plagiarism Detector

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**This is midterm week and Project 2 has just been assigned.** Students will be stretched. The coding
is genuinely small — Part A is fifteen lines — so protect the time for Parts B and D, which is where
the content is.

**The one thing to insist on is the vocabulary size.** The specification says 3,000 words with Zipf
weights. A student who uses a 20-word vocabulary will find unrelated documents scoring **0.57** and
will conclude the method does not work. That is a real result about their corpus and it destroys the
rest of the lab, so check A3's numbers before they proceed.

*(This is not a hypothetical failure mode — it is what the reference implementation did on the first
attempt, and the lab is designed around avoiding it.)*

---

## Part A — Fingerprinting (12)

### A1 (3), A2 (3)

**Containment is the better measure when the documents differ greatly in length.** Jaccard divides by
the union, so a short passage copied into a long document scores low even though *all* of the short
document was copied. Containment$(A, X) = |A \cap X|/|A|$ asks "what fraction of A appears in X",
which is the question an accusation actually rests on.

### A3 (6) — deterministic

Four documents of 600 words over a 3,000-word Zipf vocabulary. At $k = 25$, document A has **3,575**
distinct $k$-grams.

*Mark the vocabulary size and the Zipf weighting, not the exact counts — those depend on the
generator. If unrelated documents score above 0.05 at $k = 20$, the corpus is wrong.*

---

## Part B — Choosing $k$ (12)

### B1 (6) — deterministic

| $k$ | identical | 20% changed | 30% chunk | unrelated |
| --- | --- | --- | --- | --- |
| 5 | 1.000 | 0.663 | 0.390 | **0.284** |
| 10 | 1.000 | 0.487 | 0.202 | 0.063 |
| 20 | 1.000 | 0.310 | 0.148 | **0.001** |
| 40 | 1.000 | **0.157** | 0.146 | 0.000 |

### B2 (4) — the assessed question

| $k$ | 5 | 10 | **20** | 40 |
| --- | --- | --- | --- | --- |
| separation | 0.106 | 0.140 | **0.148** | 0.146 |

*(Computed from unrounded scores. Subtracting the rounded table entries above gives values differing
by up to 0.001 — accept either.)*

Best at $k = 20$, with $k = 40$ close behind.

Expected explanations:

- **Small $k$**: there are only $\sigma^k$ possible $k$-grams and any two English documents share huge
  numbers of short ones by chance. At $k=5$, unrelated documents score **0.284** — overlapping with
  the 0.390 of a genuine 30% copy, so no threshold separates them.
- **Large $k$**: a $k$-gram survives only if $k$ consecutive characters are untouched. One changed word
  destroys every $k$-gram overlapping it, so at $k=40$ the 20%-edited document falls to **0.157** —
  indistinguishable from a genuine partial copy at 0.146.

*4 requires **both** directions. One direction is 2. A student who says "k=20 is best" with no
mechanism gets 1.*

### B3 (2) — deterministic, at $k = 25$

| comparison | Jaccard | containment |
| --- | --- | --- |
| identical | 1.000 | 1.000 |
| 20% changed | 0.257 | 0.409 |
| 30% chunk | 0.147 | 0.296 |
| unrelated | 0.000 | 0.000 |

Expected: **containment**, because it answers "how much of this document appears in that one" and is
not diluted by the accused document's length. A student padding a copied passage with original text
lowers Jaccard and leaves containment untouched.

---

## Part C — Winnowing (8)

### C1 (4) — deterministic

Document A: **3,575** $k$-grams → **801** fingerprints, **22%**.

### C2 (4) — deterministic

| comparison | winnowed | full |
| --- | --- | --- |
| identical | 1.000 | 1.000 |
| 20% changed | 0.246 | 0.257 |
| 30% chunk | 0.147 | 0.147 |
| unrelated | 0.000 | 0.000 |

Expected answer to "why does the minimum preserve matches":

If two documents share a substring of length at least $k + w - 1$, that substring contains at least $w$
consecutive $k$-grams, so it contains **a complete window** — and both documents compute the minimum of
that same window, selecting the **same** hash. The choice depends only on the hash values in the
window, not on position, so both documents select it independently.

**That is the guarantee**: any shared passage long enough to contain a full window is certain to
produce at least one shared fingerprint. Shorter shared passages may be missed, which is the price.

*4 requires the "same window, same minimum, chosen independently" argument. "It keeps a representative
sample" is 1 — that is true of random sampling too, and random sampling has no guarantee.*

---

## Part D — Judgement (8)

### D1 (3)

**High score without plagiarism** — any two of:

- both students used the same **template, boilerplate or starter code**;
- both quote the same **source material** — a specification, a textbook passage, standard library
  documentation;
- the assignment is narrow enough that correct solutions **converge**, which is common in a first
  programming course;
- both used the same **generated or auto-formatted** output.

**Low score despite plagiarism**: the student **paraphrased** — renamed variables, reordered
independent statements, changed formatting — which destroys $k$-grams while preserving the structure a
human would recognise instantly.

*The paraphrase case is the important half. Award 1 of 3 if it is missing.*

### D2 (3)

| normalisation | defeats | new false positives |
| --- | --- | --- |
| lowercasing | capitalisation changes | documents differing only in case now identical |
| stripping whitespace/punctuation | reformatting, re-indentation | code and prose with different structure collide |
| replacing identifiers with a placeholder | systematic renaming | **any two programs with the same shape** — which for a first-year exercise may be most of the cohort |

The third is the one to draw out: it defeats the most common evasion and produces the most false
positives, and that trade is a policy decision rather than a technical one.

### D3 (2)

$\binom{300}{2} = \mathbf{44{,}850}$ comparisons.

Expected change: **invert the index.** Build a map from fingerprint to the set of documents containing
it, then only compare document pairs that share at least one fingerprint — most pairs share none and
are never compared. Winnowing makes this cheaper still by shrinking the index by ~78%.

*Accept LSH/minhash as a stronger answer. Reject "use multiprocessing" — the question asks about the
design, and 44,850 comparisons is not a compute problem, it is a needless-work problem.*

---

## Checkoff Checklist

1. Vocabulary is **3,000 words with Zipf weights** — check before anything else.
2. Unrelated documents score **~0.001 at $k = 20$**. If not, the corpus is wrong.
3. B2 explains **both** failure directions.
4. C2's explanation is the shared-window argument, not "it samples".
5. D1 includes the paraphrase case.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 12 |
| B | 12 |
| C | 8 |
| D | 8 |
| **Total** | **40** |

Labs are pass/fail for progression: **10 of 13 required.** This is Lab 10 of 13 — a student who has
missed three has now used their allowance and must complete Labs 11 and 12. **Tell them individually
this week**, not in Week 12.

---

## Note for the Week 11 Lecture

Part D is the last time this course asks what an algorithm's output *means* rather than what it costs,
and it is worth two minutes on Monday.

The detector is correct, fast, and produces a number. **The number is not evidence.** Two students with
the same specification and the same textbook will share long passages legitimately; a plagiarist who
paraphrases scores low. What the tool produces is a **ranked list of pairs for a human to read**, and a
system that treats the score as a verdict is worse than no system, because it is wrong with an air of
authority.

That generalises past this lab. **Week 12** ends the course on approximation algorithms — methods whose
whole contract is "the answer is within a factor of 2 and I can prove it" — and the habit of asking
what a number licenses you to conclude is exactly what makes those usable.

---

*CS 102 · Week 10 · Lab 10 Solutions · © CSE Department*
