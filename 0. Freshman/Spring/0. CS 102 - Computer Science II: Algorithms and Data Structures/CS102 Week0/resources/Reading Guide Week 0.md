# CS 102 · Week 0 Reading Guide
## Review and Course Overview

**Assigned:** CLRS Chapters 1–4 (review). Roughly 90 pages, most of which you have seen.

---

## How to Read a Review Assignment

You covered most of CLRS 1–4 in CS 101. The temptation is to skip it. **Read it faster instead**, and
read it with a different question in mind.

In CS 101 you read these chapters asking *what does this algorithm do?* Read them now asking **why is
it presented in this order?** CLRS opens with insertion sort and a loop invariant, moves to
divide-and-conquer and merge sort, then to asymptotic notation, then to recurrences. That is not
arbitrary: it is exactly the toolkit needed before any interesting algorithm can be discussed, and it
is the same sequence Lectures 01–03 followed this week.

---

## Required

### CLRS Chapter 1 — The Role of Algorithms in Computing
*Skim. 15 minutes.*

Sets up the idea that algorithms are a technology with measurable properties. The one section worth
slowing down for is the comparison of insertion sort and merge sort on machines of different speeds
— **the point being that the faster machine running the worse algorithm loses**, which is Lecture
01's §4 in miniature.

### CLRS Chapter 2 — Getting Started
*Read properly. This is the most important chapter this week.*

Insertion sort, **loop invariants**, and merge sort. Section 2.1's invariant proof is the template
Lecture 03 followed, and the one your Week 1 problem set will expect you to imitate.

> **Guiding question:** CLRS proves insertion sort correct with a loop invariant having three parts —
> initialisation, maintenance, termination. **Which of the three would still hold if the algorithm
> were wrong?** Answering this tells you which part is actually doing the work.

### CLRS Chapter 3 — Characterizing Running Times
*Read the definitions carefully; skim the examples.*

Formal $O$, $\Omega$, $\Theta$, plus $o$ and $\omega$. **The formal definitions matter this term** in
a way they did not in CS 101 — you will be asked to show a bound is tight, which is a claim about
$\Theta$ and cannot be established by an $O$ argument.

> **Guiding question:** Write down a function $f(n)$ that is $O(n^2)$ but **not** $\Theta(n^2)$, and
> one that is $\Theta(n^2)$ but not $O(n)$. If you cannot produce both in two minutes, reread §3.1.

### CLRS Chapter 4 — Divide-and-Conquer
*Read §4.3–4.5 (substitution, recursion trees, the master method). §4.6's proof is optional.*

The three recurrence-solving techniques from Lecture 02 §5.

> **Guiding question:** The master method has three cases and a gap — recurrences it cannot solve.
> **Find one.** ($T(n) = 2T(n/2) + n\log n$ is a good place to start; work out why it falls between
> Case 2 and Case 3.)

---

## Optional but Recommended

### Skiena, *The Algorithm Design Manual*, Chapter 1
Skiena opens with two "war stories" about real problems where the obvious algorithm was catastrophic.
Twenty minutes, and it does more than any lecture to explain why step 2 of the design process
(identify the structure) is where the value is.

### Dasgupta, Papadimitriou & Vazirani, Chapter 0
Nine pages. The single best short treatment of "why asymptotic notation" that exists. **If CLRS
Chapter 3 did not land, read this before rereading CLRS.**

---

## Verify Lecture 01's Table Yourself

Lecture 01 claimed specific runtimes for different complexity classes. **Do not take them on trust** —
this is a course about verifying claims, and it would be odd to begin by believing one.

```python
import math

for n in [10, 100, 1000, 10**6]:
    print(n, round(n*math.log2(n)), n**2)

ops = 1e9                      # operations per second
yr  = 365.25*24*3600
print("n=1e6, n log n :", 10**6*math.log2(10**6)/ops, "s")
print("n=1e6, n^2     :", (10**6)**2/ops/60, "min")
print("n=1e9, n^2     :", (10**9)**2/ops/yr, "years")
print("2^100 at 1e9/s :", 2**100/ops/yr, "years")
```

The last line is the one worth staring at. **It is about $4\times10^{13}$ years** — roughly 2,900
times the age of the universe — and running it on a machine a *billion* times faster still leaves
about 40,000 years. That is the difference Week 12 is about.

---

## Before Week 1

- [ ] CLRS 1–4 read
- [ ] Lab 0 complete
- [ ] Lecture 03's five exercises attempted — **Quiz 1 draws directly on them**
- [ ] You can state a loop invariant without looking at an example

**There is no problem set this week.** PS 1 is released in Week 1. Use the slack; it is the last of
it until the midterm.
