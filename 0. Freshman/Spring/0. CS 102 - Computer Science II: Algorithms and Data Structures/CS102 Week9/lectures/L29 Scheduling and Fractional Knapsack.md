# CS 102 · Computer Science II
## Lecture 29: Scheduling and Fractional Knapsack

---

## 1. Three Problems, Three Exchange Arguments

Lecture 28 gave the template. This lecture applies it three times, and the point of doing three is that
**the sorting key changes completely with the objective** — the same set of jobs is scheduled in a
different order depending on what you are minimising, and only the proof tells you which.

---

## 2. Minimising Total Completion Time

**Problem.** $n$ jobs with durations $d_1 \dots d_n$, one machine. A job's **completion time** is when
it finishes. Minimise the sum of completion times — equivalently, the average time a job waits.

**Rule: shortest processing time first.**

*(Verified against exhaustive permutation search on 2,000 random instances. **Suboptimal on 0.**)*

### The exchange argument, in two lines

Suppose an optimal schedule runs job $A$ immediately before job $B$ with $d_A > d_B$. Swap them.

Every other job's completion time is unchanged — the pair occupies the same total interval. Within the
pair, one job now finishes earlier and one later, and the sum changes by $d_B - d_A < 0$. **The swap
strictly improves it**, so no optimal schedule has a longer job before a shorter one. $\square$

That is the entire proof. It is worth noticing *why* it is so short: swapping **adjacent** elements
changes almost nothing, so the accounting is trivial. **Adjacent exchange is the technique to reach for
first**, and it works whenever the objective is a sum over positions.

### Why it matters

If a job's duration is 1 second and another's is 1 hour, running the hour first makes the short job
wait an hour. Running the short job first costs the long one one second. **The asymmetry is the whole
result**, and it is why queueing systems favour short tasks — and why they need separate protection
against starvation, which is a policy question rather than an algorithmic one.

---

## 3. Minimising Maximum Lateness

**Problem.** Each job has a duration $d_i$ and a **deadline** $t_i$. If it finishes at time $f_i$, its
lateness is $\max(0, f_i - t_i)$. Minimise the **maximum** lateness.

The objective changed. Does the rule?

| rule | suboptimal on |
| --- | --- |
| **earliest deadline first** | **0 of 2,000** |
| shortest duration first | **1,233 of 2,000** |
| smallest slack ($t_i - d_i$) first | 508 of 2,000 |

*(Verified against exhaustive permutation search.)*

**The rule that was optimal in §2 is now wrong 62% of the time.** Same jobs, same machine, different
objective — and "shortest first" has gone from provably optimal to worse than a coin flip.

Note also that **smallest slack** — which sounds like the sophisticated choice, and is a real
scheduling heuristic — is wrong on a quarter of instances.

### The proof

**Earliest deadline first** is optimal. Again by adjacent exchange.

Suppose an optimal schedule has $A$ immediately before $B$ with $t_A > t_B$ — an *inversion*. Swap
them. Only $A$ and $B$ change completion time; every other job is unaffected.

- $B$ now finishes **earlier**, so its lateness cannot increase.
- $A$ now finishes when $B$ used to, at time $f$. Its new lateness is $f - t_A$, which is **less than**
  $f - t_B$, which was $B$'s lateness before the swap.

So the new maximum over the pair is at most the old maximum, and nothing else moved. The swap does not
increase the objective. Repeating removes every inversion — and a schedule with no inversions is
earliest-deadline order. $\square$

**The "$A$'s new lateness is less than $B$'s old lateness" step is the entire argument.** It is where
$t_A > t_B$ is used, and without that hypothesis it is false.

> **Idle time.** The proof also assumes no gaps in the schedule. Inserting idle time can never help
> when all jobs are available at time 0, which is worth one sentence in a full write-up and is the
> detail most people omit.

---

## 4. Fractional Knapsack

**Problem.** As 0/1 knapsack, but items may be **divided**: take any fraction of an item and receive
that fraction of its value.

**Rule: sort by value-to-weight ratio, take greedily, split the last item to fill the bag exactly.**

```python
def fractional_knapsack(W, items):
    total = 0.0
    for w, v in sorted(items, key=lambda it: -it[1]/it[0]):
        if W <= 0: break
        take = min(w, W)
        total += v * take / w
        W -= take
    return total
```

$\Theta(n\log n)$, dominated by the sort. *(Verified: the fractional optimum was $\ge$ the 0/1 optimum
on all 2,000 random instances — as it must be, since every 0/1 solution is a legal fractional one.)*

### Why it works, and 0/1 does not

*Exchange argument.* Suppose an optimal solution takes some of item $j$ while item $i$ with a strictly
higher ratio is not fully taken. Move a small amount $\varepsilon$ of weight from $j$ to $i$. The
weight is unchanged and the value changes by $\varepsilon(v_i/w_i - v_j/w_j) > 0$ — an improvement,
contradicting optimality. $\square$

**The word doing the work is "a small amount".** You can always move $\varepsilon$ of weight, because
items are divisible, so the bag is always exactly full and no capacity is wasted.

In 0/1 knapsack you cannot. Taking the best-ratio item may leave capacity that nothing fits into, and
the exchange is unavailable:

| $W$ | items (weight, value) | greedy by ratio | true optimum |
| --- | --- | --- | --- |
| 50 | $(10,60), (20,100), (30,120)$ | 160 | **220** |
| 100 | $(1,2), (100,100)$ | **2** | **100** |

*(Verified. The second row is the worst case made obvious: greedy takes the tiny item with ratio 2 and
then cannot fit the item worth 100.)*

Over 2,000 random 0/1 instances, greedy-by-ratio is **suboptimal on 11%**, with a worst observed
greedy/optimal ratio of **0.412**. And the second example above shows the ratio can be made
**arbitrarily bad** — scale the numbers and greedy achieves 2 where the optimum is $10^6$.

> **One word — "fractional" — changes a $\Theta(n\log n)$ greedy algorithm into an NP-complete
> problem.** That is the sharpest illustration in the course of how much a problem statement matters,
> and it is worth sitting with. The algorithms look almost identical; one is provably optimal and the
> other has no approximation guarantee at all.

---

## 5. A Summary Worth Memorising

| objective | sort by | proof |
| --- | --- | --- |
| most activities scheduled | **earliest finish time** | leaves the most room |
| minimum total completion time | **shortest duration** | adjacent swap changes the sum by $d_B - d_A$ |
| minimum maximum lateness | **earliest deadline** | adjacent swap: $A$'s new lateness $<$ $B$'s old |
| maximum value, divisible | **value/weight ratio** | move $\varepsilon$ of weight to the better ratio |
| maximum value, indivisible | *nothing works* | NP-complete — use DP (Week 7) |

**Four problems that all sort a list and take a prefix, with four different keys.** Choosing the key
correctly is the algorithm; the code is the same either way.

---

## 6. What to Do

- Read CLRS §15.1–15.3. §15.3 (Huffman) is next lecture.
- **PS 9** proves two of these and breaks two more.
- **PROJECT 1 is due Friday.** Do not start it now.
- Next lecture: Huffman coding — a greedy algorithm whose exchange argument is subtler than these
  three, and which is inside every JPEG, MP3 and zip file you have ever opened.

---

*CS 102 · Week 9 · Lecture 29 · © CSE Department*
