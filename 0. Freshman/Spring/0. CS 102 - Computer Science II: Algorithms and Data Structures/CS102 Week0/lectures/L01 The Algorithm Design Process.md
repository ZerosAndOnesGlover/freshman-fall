# CS 102 — Computer Science II
## Lecture 01: The Algorithm Design Process

---

## 1. What Changes in This Course

CS 101 handed you algorithms and asked you to implement them. Binary search was described, then you
wrote it. Merge sort was described, then you wrote it.

**CS 102 will hand you problems and ask you to produce algorithms.** That is a different activity,
and it is worth naming the difference precisely, because students who do not name it tend to conclude
around Week 4 that they have become worse at programming. They have not. They have started doing
something harder.

The difference is not that the code is longer — most of what you write this term is under sixty
lines. It is that **the code is the last step**, and by the time you reach it the interesting work is
finished.

---

## 2. The Process

Every algorithm you design this term goes through the same six steps. They are not a ritual; each one
catches a specific class of mistake, and skipping one has a predictable consequence.

### Step 1 — Understand the problem

State the input, the output, and the constraint precisely enough that someone could disagree with
your statement.

This sounds trivial. It is where most wrong answers begin. "Find the shortest path" is not a problem
statement — shortest by number of edges or by total weight? May weights be negative? Is the graph
directed? Is it connected? **Each of those answers selects a different algorithm**, and three of them
make the obvious algorithm silently wrong rather than slow.

> **Discipline:** write the input and output types before anything else. If you cannot, you do not
> yet know what you are solving.

### Step 2 — Identify the structure

Ask what shape the problem has. This is the step that turns an unfamiliar problem into a familiar
one, and it is the skill this course is really teaching.

| If the problem has… | Consider… | Weeks |
| --- | --- | --- |
| A sorted or orderable domain | Binary search, BSTs, balanced trees | 1–2 |
| Repeated "give me the smallest/largest" | Heaps, priority queues | 3 |
| Entities with pairwise relationships | Graphs | 4–6 |
| Optimal solutions built from optimal sub-solutions, reused | Dynamic programming | 7–8 |
| Optimal solutions built from optimal sub-solutions, *not* reused | Greedy | 9 |
| Self-similarity within a sequence | String algorithms | 10 |
| Orientation, containment, proximity in the plane | Computational geometry | 11 |

**Notice the DP/greedy row.** Both need optimal substructure. What separates them is whether
subproblems overlap — and getting that wrong is the single most common error in Weeks 7–9.

### Step 3 — Design

Now choose or invent the algorithm. Write it as prose or pseudocode first.

**Not as code.** Code forces you to decide things — variable types, iteration order, off-by-ones —
that are irrelevant to whether the idea is correct, and deciding them early makes you reluctant to
throw the idea away when it turns out to be wrong.

### Step 4 — Prove it

State why it is correct. For iterative algorithms this usually means a **loop invariant**; for
recursive ones, **induction**. Lecture 03 covers both.

A proof is not decoration. It is the only thing that distinguishes "I could not find a case where it
fails" from "it does not fail."

### Step 5 — Implement

*Now* write the code. If steps 1–4 were done, this is transcription.

### Step 6 — Analyse

Time and space, as a function of the input size, in the worst case — and where relevant the average
and amortised cases too.

---

## 3. Why the Order Matters

Consider a concrete failure. A student is asked: *given a list of $n$ integers, find the $k$ largest.*

**Skipping step 2**, they reach for the familiar and sort the whole list, then take the last $k$.
That is $O(n \log n)$ and it is correct. It is also doing far more work than the problem requires —
it produces a total order on all $n$ elements when the question only asked which $k$ are biggest.

Having identified the structure as "repeated give-me-the-largest", a heap gives $O(n + k \log n)$,
and a size-$k$ min-heap gives $O(n \log k)$ — which for $k = 10$ and $n = 10^9$ is the difference
between a job you run and a job you abandon.

**Neither solution is more cleverly coded than the other.** The difference was made entirely at
step 2, before anything was written.

---

## 4. What "Efficient" Means Here

Throughout this course, **efficient means polynomial in the size of the input**, and we will care
intensely about which polynomial.

Some scale, to make the abstraction concrete. Assume $10^9$ elementary operations per second:

| $n$ | $n \log_2 n$ | $n^2$ | $n^3$ | $2^n$ |
| --- | --- | --- | --- | --- |
| $10$ | $33$ | $100$ | $1{,}000$ | $1{,}024$ |
| $100$ | $664$ | $10^4$ | $10^6$ | $\approx 1.27\times10^{30}$ |
| $1{,}000$ | $\approx 10^4$ | $10^6$ | $10^9$ | — |
| $10^6$ | $\approx 2\times10^7$ | $10^{12}$ | — | — |

*(Computed, not estimated — see `Reading Guide Week 0.md` for the script.)*

At $n = 10^6$: an $O(n \log n)$ algorithm finishes in about **0.02 seconds**; an $O(n^2)$ algorithm
takes about **17 minutes**. At $n = 10^9$ the $O(n\log n)$ algorithm takes about **30 seconds** and
the $O(n^2)$ one takes roughly **30 years**.

**This is why we do not say "computers are fast enough."** The gap between complexity classes grows
without bound, so hardware improvements move the boundary of the feasible by a constant factor while
the input sizes people actually care about grow faster than that.

For $2^n$ the picture is different in kind. At $n = 100$ the machine above needs $2^{100} \approx
1.27\times10^{30}$ operations — about $4\times10^{13}$ years, or roughly **2,900 times the age of the
universe.**

And notice what buying a faster computer does here. Speed it up by a factor of a *billion*, to
$10^{18}$ operations per second, and the same problem still takes about **40,000 years**. A
billion-fold hardware improvement moved $n=100$ from hopeless to hopeless.

**That is the difference between polynomial and exponential**, and it is why the distinction is worth
a whole week. For a polynomial algorithm, a faster machine raises the size of problem you can handle.
For an exponential one, it adds a constant to it. **Week 12 is about the problems for which we know
nothing better.**

---

## 5. The Roadmap

The course has four movements.

**Weeks 1–3 — Structures that maintain order.** Binary search trees, then the balancing that makes
their worst case respectable, then heaps. The recurring theme: *an invariant, maintained cheaply on
every update, buys you a guarantee on every query.*

**Weeks 4–6 — Graphs.** The most general structure in the course, and the one that most real problems
turn out to be. Traversal, then shortest paths, then minimum spanning trees. The recurring theme:
*a greedy choice justified by a structural property.*

**Weeks 7–9 — Algorithm design paradigms.** Dynamic programming, then greedy, treated as general
techniques rather than as specific algorithms. This is the intellectual centre of the course.

**Weeks 10–12 — Specialised domains and the limits.** Strings, geometry, and finally the theory of
what cannot be done efficiently at all.

**Weeks 5 and 9 are the two hardest.** Week 5 is where three shortest-path algorithms must be held
apart by their assumptions rather than their code, and Week 9 is where "prove your greedy algorithm
is optimal" stops being a formality.

---

## 6. A Warning About Familiarity

You have met some of this material before — Fibonacci, binary search, merge sort. It will be
tempting to skim those parts.

Do not. **They are reintroduced because they are about to be used as examples of something more
general**, and the general point is invisible if you only remember the specific case. Fibonacci in
Week 7 is not a revision exercise; it is the smallest possible demonstration of overlapping
subproblems, and the whole of dynamic programming is built on noticing what happens there.

---

## 7. What to Do This Week

- Read CLRS Chapters 1–4. You have seen most of it; read it anyway, faster.
- Complete **Lab 0**: implement and benchmark three sorts from CS 101. It exists to reconnect your
  hands to the material and to make the $n \log n$ versus $n^2$ gap something you have *measured*
  rather than been told.
- There is no problem set this week and no quiz. **Quiz 1, in Week 1, covers this week.**

---

*CS 102 · Week 0 · Lecture 01 · © CSE Department*
