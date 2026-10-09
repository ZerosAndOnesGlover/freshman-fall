# CS 102 · Reading Guide, Week 9
## Greedy Algorithms

---

## Required

**CLRS, 4th ed. — Chapter 15, §15.1–15.3**, about 25 pages.

- §15.1 activity selection
- §15.2 **elements of the greedy strategy** — the section that matters
- §15.3 Huffman codes

Matroids (CLRS 3rd ed. §16.4; the 4th edition replaced that section with §15.4, offline caching) are optional, hard, and genuinely illuminating if you have the time; see below.

Also useful:

- **Kleinberg & Tardos, Chapter 4** — the best treatment of greedy correctness in print. Their
  taxonomy of proof techniques ("greedy stays ahead" versus "exchange argument") is clearer than
  CLRS's and is worth reading even if you read nothing else.
- **Skiena §1.4 and §5** — good on the psychology of greedy: why wrong rules feel right.

**MIDTERM 2 is in Week 10** and covers Weeks 5–9. **PROJECT 1 is due Friday of this week.** If reading
must be cut, read §15.2 and §15.3 and leave §15.1 to the lecture notes.

---

## Read §15.2 Twice

Chapter 15 works three examples, and the temptation is to memorise three rules. **§15.2 is the section
that says what a greedy algorithm needs**, and it is the only part that helps with a problem you have
not seen.

The two conditions are the **greedy-choice property** and **optimal substructure**. Note what CLRS is
careful about and most summaries are not:

> The greedy-choice property says there is **an** optimal solution beginning with the greedy choice —
> not that every optimal solution does, and not that the greedy choice is obviously right.

That weaker statement is what the exchange argument establishes, and it is all you need.

§15.2 also contains the comparison with dynamic programming, using 0/1 versus fractional knapsack. That
one-word difference is the sharpest example in the chapter and it is examinable.

---

## How to Read It

**§15.1 (activity selection, 8 pages).** CLRS develops it first as a DP and then shows the greedy rule
is better. **Read the DP version even though you will never use it** — the point is that greedy is a
*restriction* of DP that happens to be safe here, which is exactly what §15.2 formalises.

**§15.2 (elements, 6 pages).** The two properties, the comparison with DP, and the knapsack example.
Read it twice.

**§15.3 (Huffman, 8 pages).** The algorithm is a page; the rest is the optimality proof, in two lemmas.
**Lemma 15.2 is the greedy-choice property** — the two least frequent symbols may be taken as deepest
siblings — and its proof is a single swap whose cost change is a product of two terms with opposite
signs. **Lemma 15.3 is optimal substructure.** Together they are the whole theorem.

---

## Guiding Questions

Three of these are on MIDTERM 2.

1. §15.2: state both conditions. Which one does dynamic programming *also* need, and which is unique
   to greedy?

2. §15.1: CLRS solves activity selection by DP before doing it greedily. What does the greedy version
   throw away, and why is throwing it away safe here?

3. Fractional knapsack is greedy-solvable and 0/1 knapsack is NP-complete. **Point at the exact step
   of the exchange argument that fails** when items are indivisible.

4. §15.3, Lemma 15.2: write down the cost change from swapping $x$ with a deepest leaf. Why is that
   expression necessarily $\le 0$?

5. Huffman's average code length satisfies $H \le \bar\ell < H+1$. Construct a distribution where the
   overhead is close to 1, and say what kind of coder does better.

6. You have seen three greedy algorithms fail this term: Dijkstra with negative weights (2.3% of
   instances), coin change on $[1,5,6,9]$ (42% of targets), and fewest-conflicts activity selection
   (needed 43,000 trials to break). **What single methodological conclusion do all three support?**

7. Give a problem where greedy and DP both work, and say which you would ship and why.

---

## Common Misreadings

**"Greedy means taking the biggest thing."** It means committing to a locally optimal choice by
*some* rule. The rule differs per problem, and choosing it is the algorithm — Lecture 29 has four
problems that all sort a list and take a prefix, with four different keys.

**"If greedy gives the right answer on my tests, it works."** The fewest-conflicts rule for activity
selection is optimal on **2,000** random instances and is not optimal. The smallest counterexample has
ten intervals and took about 43,000 randomised trials to find.

**"The greedy choice must be in every optimal solution."** Only *some* optimal solution needs to
contain it. Requiring "every" would make most exchange arguments fail — with ties there are usually
several optima and the greedy choice is in only some of them.

**"Huffman is the best possible compression."** It is the best possible **prefix-free code assigning a
whole number of bits per symbol, treating symbols as independent**. Every clause is load-bearing.
Arithmetic coding beats it by dropping the integer constraint; LZ77 beats it by dropping independence —
measured, `zlib` is **1.95×** smaller than Huffman alone on the Lab 9 corpus.

**"Compression always makes files smaller."** It cannot. There is no injection from $2^n$ strings into
fewer than $2^n$ strings, so any lossless compressor makes some inputs longer. Measured: `"hello
world"` with its code table goes from 11 bytes to 20.

**"Greedy is just a heuristic."** When the greedy-choice property holds, greedy is **exactly optimal**,
not approximately. When it does not, greedy may have no guarantee at all — 0/1 knapsack by ratio can
achieve an arbitrarily small fraction of the optimum. **There is no middle ground supplied by the
paradigm itself**; guarantees for the failing case come from approximation analysis, which is Week 12.

---

## If You Have Extra Time

**Matroids (CLRS 3rd ed. §16.4).** The abstract structure that explains *why* greedy works when it does. A matroid
is a set system closed downwards with an exchange property, and **greedy is optimal on a weighted
matroid** — full stop. Kruskal's algorithm is the greedy algorithm on the graphic matroid, which is
why Week 6 worked. It is the closest thing to a general theory of greedy correctness and it is
beautiful.

Note the limits: activity selection and Huffman are **not** matroid problems, so matroids explain a
large family and not all of it.

**"Greedy stays ahead."** The other standard proof style: instead of exchanging into an optimal
solution, show by induction that after $k$ choices greedy's partial solution is at least as good as any
other's. For activity selection it is often cleaner than the exchange argument. Kleinberg & Tardos §4.1
does it properly.

**Canonical coin systems.** Deciding whether a coin system is canonical is a genuinely subtle problem —
there is a polynomial-time test (Pearson, 2005), and it is not obvious. Worth knowing that "does greedy
work here?" is itself a nontrivial computational question.

**Arithmetic and range coding.** How to beat the one-bit-per-symbol floor. The idea — encode the whole
message as a single number in $[0,1)$ — is elegant, and it is what actually ships in modern codecs.

---

*CS 102 · Week 9 · Reading Guide · © CSE Department*
