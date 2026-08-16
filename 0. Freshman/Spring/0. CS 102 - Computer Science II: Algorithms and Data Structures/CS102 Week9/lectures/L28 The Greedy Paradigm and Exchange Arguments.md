# CS 102 · Computer Science II
## Lecture 28: The Greedy Paradigm and Exchange Arguments

**Date:** Monday 15 March 2027 · 09:00–09:50 · Week 9

---

## 1. The Opposite of Last Week

Dynamic programming considers every option at every step and remembers the results. A **greedy**
algorithm makes one choice, commits to it, and never reconsiders.

```
while the problem is not solved:
    make the choice that looks best right now
```

No table, no subproblems, usually one sort and one pass — $\Theta(n\log n)$ where the DP was
$\Theta(n^2)$ or worse. **When greedy works it is strictly better.**

The difficulty is the "when". You have already seen it fail:

> **Week 8**, coin change with denominations $[1, 5, 6, 9]$. Greedy takes the largest coin that fits.
> For $T = 11$ it takes $9 + 1 + 1 = $ **three coins**; the optimum is $5 + 6 = $ **two**. Greedy is
> wrong for **84 of the first 199 targets** — 42% of them.

And it is right on every real currency, because currencies are designed so that it is.

**Nothing in the code distinguishes the two cases.** The algorithm is four lines either way. So this
week is not about writing greedy algorithms — it is about **proving** them, and the proof is the
deliverable.

---

## 2. What Has to Be True

Two properties, and the first is the one that does the work.

### The greedy-choice property

> **There is an optimal solution that begins with the greedy choice.**

Note the phrasing carefully. Not "the greedy choice is in every optimal solution", and not "the greedy
choice is obviously right" — just that **some** optimal solution agrees with it. That is enough,
because you can then repeat the argument on what remains.

### Optimal substructure

Once the greedy choice is fixed, what remains is a smaller instance of the same problem, and it must be
solved optimally. This is the same condition as Week 7's, and greedy needs it too.

**DP needs optimal substructure. Greedy needs optimal substructure *and* the greedy-choice property.**
That extra requirement is exactly what you must prove, and exactly what coin change on $[1,5,6,9]$
lacks.

---

## 3. The Exchange Argument

The standard proof technique, and you have met it twice already — **Week 6**'s cut property and
**Week 5**'s Dijkstra correctness are both this shape.

> **Template.** Let $G$ be the greedy solution and $O$ any optimal solution.
> 1. Find the **first place** where they differ.
> 2. Show you can **modify $O$** to agree with greedy there, **without making it worse**.
> 3. The modified $O'$ is still optimal and agrees with greedy one step further.
> 4. Repeat. After finitely many exchanges $O$ has become $G$, so $G$ is optimal. $\square$

The whole content is step 2. Steps 1, 3 and 4 are bookkeeping and look the same in every proof.

**"Without making it worse" is doing the work, and it is what fails for coin change.** Exchanging a
9-coin for a 6-coin in an optimal solution for $T = 11$ does make things worse — and no argument can
patch that, because the claim is false.

---

## 4. Activity Selection

**Problem.** Given activities with start and finish times, select the largest set that do not overlap.

There are several plausible greedy rules. Only one of them is right, and finding out which is the point
of the exercise.

| rule | suboptimal on |
| --- | --- |
| **earliest finish time** | **0 of 2,000** |
| shortest duration | 28 of 2,000 |
| earliest start time | 201 of 2,000 |
| fewest conflicts | **0 of 2,000** |

*(Verified against exhaustive search on 2,000 random instances.)*

Two of the four rules are wrong, and their counterexamples are small:

```
shortest duration:  (0,5) (4,6) (5,10)   picks 1 — the short middle one blocks both others
                                          optimal 2:  (0,5) and (5,10)

earliest start:     (0,10) (1,2) (3,4)   picks 1 — the long one blocks everything
                                          optimal 2:  (1,2) and (3,4)
```

*(Verified.)*

### The fourth rule is the interesting one

**"Fewest conflicts" was optimal on all 2,000 random instances — and it is not optimal.**

Finding a counterexample took **42,936 randomised trials**, searching instances of 6 to 11 intervals.
Here is one:

$$(0,4)\ (1,4)\ (2,6)\ (3,5)\ (4,7)\ (6,9)\ (8,10)\ (9,12)\ (9,13)\ (11,14)$$

Fewest-conflicts selects **3**; the optimum is **4**. *(Verified. Removing any single interval destroys
the counterexample, and an exhaustive search finds none with 6 intervals or fewer.)*

> **This is the lecture in one example.** A heuristic passed 2,000 random tests, needed ten intervals
> and forty thousand attempts to break, and is still wrong. **Testing cannot establish the
> greedy-choice property.** Only a proof can — and for this rule there is none, because the claim is
> false.

### Proving earliest-finish-time correct

*Greedy-choice property.* Let $a_1$ be the activity finishing earliest, and let $O$ be an optimal
solution whose first activity is $a_k \ne a_1$. Since $a_1$ finishes no later than $a_k$, replacing
$a_k$ by $a_1$ in $O$ cannot create an overlap with anything that came after $a_k$ — everything in $O$
after $a_k$ starts at or after $a_k$'s finish, which is at or after $a_1$'s. So $O' = O - a_k + a_1$ is
feasible and the same size. $\square$

**One exchange, three lines.** Then induct on the remaining activities that start after $a_1$ finishes.

The intuition worth keeping: **finishing earliest leaves the most room for everything else**, and
"leaves the most room" is exactly what the exchange formalises.

---

## 5. Greedy Against DP

| | greedy | dynamic programming |
| --- | --- | --- |
| choices | one, never revisited | all, remembered |
| typical cost | $\Theta(n\log n)$ | $\Theta(n^2)$ or worse |
| space | $O(1)$–$O(n)$ | the table |
| needs | greedy-choice **+** optimal substructure | optimal substructure |
| correctness | **must be proved** | follows from the recurrence |
| failure mode | **silent** and input-dependent | usually none |

The last row is the one to remember. A DP that is set up correctly is correct. **A greedy algorithm can
be wrong on 42% of inputs and look identical to a correct one.**

### The same problem, both ways

| problem | greedy | why |
| --- | --- | --- |
| **fractional** knapsack | **optimal** | you can always fill the bag exactly (Lecture 29) |
| **0/1** knapsack | **wrong** — suboptimal on 11% of random instances | an item is indivisible; taking the best ratio can waste capacity |
| coin change, $[1,2,5,10,20,50,100,200]$ | optimal | the system is *canonical* |
| coin change, $[1,5,6,9]$ | **wrong** on 42% of targets | it is not |
| shortest path, non-negative | optimal (Dijkstra) | Week 5's proof |
| shortest path, negative edges | **wrong** on 2.3% of instances | Week 5 §4 |
| MST | optimal (Prim, Kruskal) | the cut property |

**Two adjacent rows, one word of difference in the problem statement, and opposite answers.** That is
why the proof is the work.

---

## 6. How to Approach a Greedy Problem

1. **Guess a rule.** Sort by something and take what fits.
2. **Try to break it.** Small cases first, then randomised search against a brute-force reference. This
   is fast and it eliminates most wrong rules in minutes.
3. **If it survives, prove it** by an exchange argument. Not "it seems right" — write step 2 of §3 out.
4. **If you cannot prove it, assume it is wrong.** The fewest-conflicts rule survived 2,000 tests.

**Step 2 does not replace step 3**, and this lecture's whole design is to make that concrete. Step 2 is
how you avoid wasting an afternoon proving something false; step 3 is the only thing that establishes
correctness.

---

## 7. What to Do

- Read CLRS §15.1 (activity selection) and §15.2 (elements of the greedy strategy). §15.2 is the
  section that matters — it is the greedy analogue of Week 7's §14.3.
- **PS 9** asks you to break three greedy rules and prove one.
- **PROJECT 1 is due Friday.** It is 10% of the course.
- **Quiz 9 covers Week 8.**
- Next lecture: scheduling and fractional knapsack — three more exchange arguments, one of which is
  two lines.

---

*CS 102 · Week 9 · Lecture 28 · © CSE Department*
