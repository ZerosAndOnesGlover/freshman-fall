# CS 102 · Reading Guide, Week 10
## String Algorithms

---

## Required

**CLRS, 4th ed. — Chapter 32, §32.1–32.5** (String Matching; §32.5 is suffix arrays).

- §32.1 the naive algorithm
- §32.2 Rabin–Karp
- §32.3 matching with finite automata — **optional**, but it is the cleanest way to see *why* KMP works
- §32.4 the Knuth–Morris–Pratt algorithm

**Boyer–Moore is not in CLRS. Suffix arrays are §32.5, new in the 4th edition.** Also use:

- **Sedgewick & Wayne §5.3** — substring search, with the best treatment of Boyer–Moore available at
  this level;
- **Sedgewick & Wayne §6.3** — suffix arrays, including the LCP array;
- **Gusfield, *Algorithms on Strings, Trees and Sequences*** — the reference work if your library has
  it. Chapters 1–3 cover this week properly.

> **MIDTERM 2 is this week and covers Weeks 5–9 — none of this material.** Read the midterm guide
> first. This chapter can wait until after the paper; PS 10 is not released until Friday.

---

## Read §32.4 for the Idea, Not the Code

CLRS's KMP is correct and its presentation is **1-indexed**, which makes the failure function's
indices differ from the lectures by one. You have converted between indexing conventions twice already
(Week 3's heaps, Week 5's CLRS graphs); do it here deliberately rather than by trusting your eye.

**The thing to extract is the definition of the failure function**, not the loop:

> $f[i]$ is the length of the longest proper prefix of $p[0 \dots i]$ that is also a suffix of it.

Everything else — the construction, the search loop, the complexity — follows from that sentence. If
you can state it precisely you can rederive the algorithm; if you memorise the loop you will not.

**§32.3 is worth the detour.** It builds a finite automaton whose states are "how much of the pattern
have I matched", and KMP is that automaton with the transitions computed lazily instead of stored. The
automaton view makes the correctness obvious in a way the pointer manipulation does not.

---

## How to Read It

**§32.1 (2 pages).** The naive algorithm and its $\Theta((n-m+1)m)$ bound. Note that CLRS is careful to
say this is a *worst case* and that the algorithm is fine in practice — a distinction most summaries
drop.

**§32.2 (7 pages).** Rabin–Karp. The rolling-hash recurrence is the content. Pay attention to the
discussion of **spurious hits**: the running time is $O(n) + O(m \cdot v)$ where $v$ is the number of
false matches, and $v$ depends on your modulus, not on the input.

**§32.4 (8 pages).** KMP. The amortised analysis of the `while` loop (Lemma 32.5) is the same potential
argument as Week 3's `BUILD-HEAP` and Week 6's union-find. **Read it as the third instance of a pattern
you know**, not as a new trick.

---

## Guiding Questions

Three of these are on the final.

1. §32.1: the naive algorithm is $\Theta(nm)$ worst case and fast in practice. What property must a
   (text, pattern) pair have to hit the worst case? Construct one.

2. §32.4: state the failure function's definition. Then explain why `k = f[k-1]` is the right fallback
   — *why is the longest border of a border also a border?*

3. §32.4: the inner `while` loop can run $\Theta(m)$ times in one iteration. Why is the algorithm still
   $\Theta(n)$? Name the quantity that makes the potential argument work.

4. §32.2: what exactly does the `t[i:i+m] == p` verification protect against, and what is the
   algorithm's worst-case complexity without it?

5. Rabin–Karp is rarely the best way to find *one* pattern. Give the situation where it beats every
   other algorithm in this chapter, and say why.

6. Boyer–Moore can be sublinear — it examines fewer than $n$ characters. Which algorithm property
   allows that, and which input property is required?

7. A suffix array costs $O(n\log n)$ to build and $O(m\log n)$ per query; KMP costs $\Theta(n+m)$ per
   query with no preprocessing. **At how many queries does the suffix array win?**

---

## Common Misreadings

**"KMP is the fastest string matcher."** It has the best *worst-case* guarantee. On ordinary text
Boyer–Moore is several times faster — measured, **0.144** character comparisons per text character on a
26-letter alphabet against KMP's ~1.04 — and Python's own `str.find` uses neither.

**"Boyer–Moore is always sublinear."** Only with a reasonably large alphabet. On a binary alphabet it
does **1.490** comparisons per character, **worse than KMP**. The advantage is a property of the
alphabet, not of the algorithm.

**"Rabin–Karp is $O(n+m)$."** Expected, and only with a good modulus. Measured with modulus 101 there
were **214** spurious hits over 20,000 windows, each costing an $O(m)$ verification; the worst case is
$\Theta(nm)$. This is the only algorithm in the course whose complexity depends on **a parameter you
choose**.

**"The hash comparison in Rabin–Karp finds the matches."** It finds *candidates*. The string comparison
is what makes the algorithm correct, and removing it turns a matcher into a heuristic.

**"A suffix array is a suffix tree."** A suffix array is $n$ integers, $\Theta(n)$ space with a small
constant. A suffix tree answers some queries faster and costs 10–20 bytes per character in practice,
which is why suffix arrays largely replaced them.

**"Sorting the suffixes directly is too slow."** Asymptotically $\Theta(n^2\log n)$, and measured, it
**beats** prefix doubling until about $n = 10{,}000$ in CPython. Same pattern as Weeks 2, 3, 6 and 8.

**"The longest repeated substring can't overlap itself."** It can. `ana` occurs at positions 1 and 3 of
`banana`. A brute-force reference written with `str.count` — which counts non-overlapping occurrences —
gets this wrong on about **22%** of random strings — 1,100 of 5,000 pooled over ten samples — and **it
is the reference that is wrong, not the LCP method.**

---

## If You Have Extra Time

**The Z-algorithm.** For each position, the length of the longest substring starting there that is also
a prefix of the whole string. Computable in $\Theta(n)$, and it solves string matching by running on
`p + '\0' + t`. Many people find it easier to derive from scratch than KMP, and it is the standard tool
in competitive programming. It also computes the failure function as a by-product.

**Aho–Corasick.** KMP generalised to **many patterns at once**: build a trie of the patterns, add
failure links between trie nodes, and match all of them in one $\Theta(n)$ pass. It is what `fgrep`
and most intrusion-detection systems use, and it is the right answer to Lecture 32's "many patterns"
case when the patterns have different lengths.

**The Burrows–Wheeler transform and the FM-index.** A permutation of the text read off the suffix
array, which makes the text *more compressible* and remains searchable. `bzip2` uses the first half;
`bwa` and `bowtie` use the second to index a 3-billion-character genome in less space than the genome
itself. **It connects this week directly to Week 9's Huffman**, which is BWT's last stage.

**Suffix automata and suffix trees.** Ukkonen's linear-time suffix tree construction is a famous piece
of work and a famous difficulty; read it only when you have time to do it properly.

---

*CS 102 · Week 10 · Reading Guide · © CSE Department*
