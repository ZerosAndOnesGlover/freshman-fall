# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 10: String Algorithms

**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PS 10** (released Friday, due Friday of Week 11), Lab 10, **Quiz 10 —
which covers Week 9**.
**MIDTERM 2 is this week**, 75 minutes, covering Weeks 5–9. See `resources/MIDTERM 2 Revision Guide.md`.
**PROJECT 2 is assigned this week** and due Friday of Week 12 — **10% of the course**.

---

### Why This Week Exists

Finding a pattern in text is the operation you have used most and thought about least. The obvious
algorithm is quadratic in the worst case, and the fixes are among the few genuinely surprising
algorithms in this course.

But the week's real subject is **what stays fixed and what varies**. Every algorithm here answers the
same question and makes a different bet about that:

| what is fixed | what varies | algorithm |
| --- | --- | --- |
| nothing | text and pattern | naive, Boyer–Moore |
| the pattern | the text (a stream) | **KMP** |
| many patterns | one pass over the text | **Rabin–Karp** |
| the **text** | thousands of queries | **suffix array** |

**No algorithm dominates.** Identifying which column your problem sits in is the skill, and PS 10 Part
D is entirely that question.

### Learning Objectives

By the end of Week 10, you should be able to:

1. Construct the worst case for naive matching, and say why it does not occur in ordinary text.
2. Define the failure function as a statement about **borders**, and compute it in $\Theta(m)$.
3. Implement KMP, and **prove it $\Theta(n+m)$** by a potential argument.
4. Implement a rolling hash, and say what the verification step protects against.
5. Explain why Rabin–Karp's complexity depends on **a parameter you choose**.
6. Implement Boyer–Moore's bad-character rule, including the guard, and say what the alphabet size
   does to its performance.
7. Build a suffix array and an LCP array, and use them for search, longest repeated substring, and
   distinct-substring counting.
8. Choose between preprocessing the pattern and preprocessing the text, given a query count.

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L31 Naive Matching and KMP.md` | Borders, the failure function, and the amortised proof |
| `lectures/L32 Rabin-Karp and Boyer-Moore.md` | Hashing and skipping, and what each depends on |
| `lectures/L33 Suffix Arrays and Applications.md` | Preprocessing the text; LCP arrays and what they buy |
| `assignments/PS 10 String Matching.md` | 100 points, due Friday of Week 11 |
| `assignments/QUIZ 10 Week 10 Monday.md` | 20 points, formative — **covers Week 9** |
| `assignments/PROJECT 2 A Search Engine.md` | **10% of the course**, due Friday of Week 12 |
| `lab/LAB 10 Building a Plagiarism Detector.md` | Fingerprinting, and why the parameter is the system |
| `resources/Reading Guide Week 10.md` | CLRS §32.1–32.4, plus Sedgewick for what CLRS omits |
| `resources/MIDTERM 2 Revision Guide.md` | Format, examinable material, fifteen reproducible proofs |
| `solutions_instructor/` | PS 10 and Lab 10 solutions — instructor only |

### The Three Ideas Most Likely to Be Missed

**1. KMP's guarantee is worth more than its speed.** On ordinary text Boyer–Moore is several times
faster — measured, **0.144** comparisons per text character on a 26-letter alphabet against KMP's
**1.04** — and Python's `str.find` uses neither. KMP is the right answer for repetitive input, for
**streams you cannot rewind**, and when you need a bound rather than good behaviour.

**2. Boyer–Moore's advantage belongs to the alphabet, not the algorithm.** At 26 letters it examines
one character in seven. On a **binary** alphabet it does **1.490** comparisons per character — *worse
than KMP*. Same code, same pattern length, opposite verdict.

**3. Rabin–Karp's complexity depends on a parameter you choose.** With modulus $2^{61}-1$: **0**
spurious hits over 20,000 windows. With modulus 101: **214**, each costing an $O(m)$ verification, and
a worst case of $\Theta(nm)$. Not the input, not the machine — the prime.

### The Reference That Was Wrong

PS 10 C4 asks for the longest repeated substring via the LCP array, and for a brute-force reference to
check it against. **The obvious reference is wrong.**

`str.count` counts **non-overlapping** occurrences, so `"aaa".count("aa")` is 1 — but `aa` genuinely
repeats in `aaa`, at positions 0 and 1, overlapping. A reference built that way disagrees with the LCP
method on about **22%** of random strings, and **the LCP method is the one that is right**.

This is the second time this term that a *verification* has been the broken component — the first was
PS 4's circular check of the parenthesis theorem. **"My two implementations disagree" does not tell you
which to fix.**

### A Note on the Measurements

**Counts are deterministic** — every comparison count, spurious-hit count, suffix array and LCP array.
`banana` has $\mathrm{SA} = [5,3,1,0,4,2]$ and $\mathrm{LCP} = [0,1,3,0,0,2]$ on any correct
implementation.

**Timings are not**, and one of them is worth flagging: sorting the suffixes directly is
$\Theta(n^2\log n)$ and **beats** prefix doubling until about $n = 10{,}000$, because `sorted` runs in C.
That is the sixth instance of the pattern this term.

### Connections

**Back:** KMP's amortised proof is the third of its kind, after **Week 3**'s linear `BUILD-HEAP` and
**Week 6**'s union-find — an expensive step that cannot be expensive often. Rabin–Karp's rolling hash
is what makes Lab 10's fingerprinting linear. Suffix arrays feed **Week 9**'s Huffman through the
Burrows–Wheeler transform, and Project 2 uses **Week 3**'s bounded heap, **Week 7**'s edit distance and
**Week 9**'s compression.

**Forward:** **Week 11** turns to computational geometry and to segment trees, which decompose an
interval the way Week 8's interval DP did. **Week 12** asks which problems admit no efficient algorithm
— and several of the first NP-complete problems you meet are about strings. **Project 2** is due
Friday of Week 12, the same day as the final exam week begins.

---

*CS 102 · Week 10 · © CSE Department*
