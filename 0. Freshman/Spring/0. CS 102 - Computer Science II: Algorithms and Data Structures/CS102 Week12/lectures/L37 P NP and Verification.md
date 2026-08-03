# CS 102 · Computer Science II
## Lecture 37: P, NP, and Verification

---

## 1. A Different Kind of Question

For twelve weeks the question has been *what is the best algorithm for this problem*. This week asks a
question one level up: **for which problems is there no good algorithm at all?**

That is not a question about your cleverness. It is a question about the problem, and the theory that
answers it — begun by Cook and Levin in 1971 — is one of the genuine intellectual achievements of the
subject.

Start with what "no good algorithm" would mean, concretely. Exact TSP by Held–Karp, measured:

| $n$ | operations $\approx 2^n n^2$ | time |
| --- | --- | --- |
| 8 | 16,384 | 0.001 s |
| 12 | 589,824 | 0.022 s |
| 16 | 16,777,216 | 0.590 s |
| 20 | 419,430,400 | **14.8 s** |

*(Verified.)* Extrapolating the same code:

| $n$ | estimated time |
| --- | --- |
| 25 | ≈ 12 minutes |
| 30 | ≈ **9.5 hours** |
| 40 | ≈ **2 years** |

**Forty cities.** Not forty thousand. And Held–Karp is the *best known exact algorithm* — from 1962,
and still unbeaten in the exponent.

**Buying a faster computer does not help.** A machine a thousand times faster moves $n = 40$ to
$n = 49$ — **nine more cities.** That is the difference between exponential and polynomial growth, and it is why this week
exists.

---

## 2. Decision Problems

The theory is stated for **decision problems** — questions with a yes/no answer.

| optimisation version | decision version |
| --- | --- |
| find the shortest tour | *is there a tour of length $\le k$?* |
| find the smallest vertex cover | *is there a cover of size $\le k$?* |
| find the largest clique | *is there a clique of size $\ge k$?* |

This looks like a restriction and is not: **if you can answer the decision version quickly, you can
solve the optimisation version quickly** by binary searching on $k$, at a cost of a $\log$ factor. The
two are equivalent for our purposes, and decision problems are much easier to reason about.

---

## 3. P and NP

> **P** is the class of decision problems solvable in polynomial time — $O(n^k)$ for some constant $k$.

Everything in this course until Week 7's knapsack is in P: sorting, shortest paths, MSTs, string
matching, convex hulls.

> **NP** is the class of decision problems whose **yes** answers can be *verified* in polynomial time,
> given a suitable certificate.

Read that carefully, because it is the definition people get wrong.

**NP is not "non-polynomial".** It stands for *nondeterministic polynomial time*. A problem is in NP if,
whenever the answer is yes, there is a short proof that can be checked quickly.

| problem | certificate for "yes" | checking it |
| --- | --- | --- |
| Is there a tour of length $\le k$? | the tour | add up $n$ edges |
| Is this formula satisfiable? | the assignment | evaluate the formula |
| Is there a cover of size $\le k$? | the vertex set | check every edge |
| Is $n$ composite? | a factor | one division |

**Finding the certificate may be hard. Checking it is easy.** That asymmetry is the entire subject.

### The obvious containment

$$P \subseteq NP$$

If you can *solve* a problem in polynomial time you can verify it in polynomial time — ignore the
certificate and solve it. The question is whether the containment is strict.

### And the one that is not obvious

**NP does not obviously contain the complement.** Nothing in the definition gives a short certificate
for a **no** answer. "There is no tour shorter than $k$" is not obviously checkable — you would have to
rule out every tour. The class of problems with short *disproofs* is called **co-NP**, and whether
NP = co-NP is another open question.

> **The asymmetry is real and it matters practically.** A SAT solver that says "satisfiable" hands you
> an assignment you can check in a second. One that says "unsatisfiable" is asking you to trust it —
> which is why proof-producing solvers are a research area of their own.

---

## 4. P vs NP

$$\text{Is } P = NP\,?$$

Does every problem whose solutions can be *checked* quickly also admit solutions that can be *found*
quickly?

Almost everyone believes **no**. Nobody can prove it. It is one of the seven Clay Millennium Prize
Problems, and the prize has stood since 2000.

### What "yes" would mean

If P = NP, then for every problem where a solution is recognisable, a solution is findable — at the
same cost. The consequences are not incremental:

- **Cryptography largely collapses.** RSA rests on factoring being hard; much of modern crypto rests on
  problems in NP. If P = NP, breaking a key is as easy as checking one.
- **Optimisation becomes routine.** Scheduling, routing, protein folding, circuit layout — all of them
  are searches for a certificate that is easy to verify.
- **Mathematics changes.** Finding a proof of bounded length becomes as easy as checking one, which
  arguably automates a large part of the discipline.

**That last consequence is the strongest informal argument that P ≠ NP.** As Scott Aaronson puts it,
if P = NP then anyone able to appreciate a symphony is Mozart. The world does not look like that.

### Why it is hard to prove

To show P ≠ NP you must prove that **no** polynomial algorithm exists for some NP problem — a statement
about every algorithm that could ever be written. Two major barriers (relativisation and natural
proofs) are known to rule out whole families of proof techniques, including most of what we have.

**You are not expected to have an opinion about the proof.** You are expected to know what the question
says, why it matters, and — the practical part — what to do when your problem turns out to be on the
wrong side of it.

---

## 5. What This Means for You

You will not be asked to resolve P vs NP. You will regularly be asked to write an algorithm for a
problem that turns out to be NP-complete, and the value of this week is knowing **what to do next**.

The wrong response is to keep looking for a polynomial algorithm. The right responses:

1. **Prove it is NP-complete** (Lecture 38) so you can stop looking and say why.
2. **Exploit structure.** Your instances may not be general. Longest path is NP-complete on a graph and
   linear on a DAG (Week 5); independent set is NP-complete on a graph and linear on a tree (Week 8).
3. **Accept exponential, but a good exponential.** Held–Karp handles $n = 20$; modern SAT solvers
   routinely handle instances with millions of variables, despite the worst case.
4. **Accept a bound on the answer instead** — approximation algorithms, Lecture 39.
5. **Accept a bound on the input.** Knapsack is NP-complete and $\Theta(nW)$ solves it when $W$ is
   small (Week 7).

**Each of those is a decision about which guarantee to give up**, and making it deliberately is the
professional skill this week teaches.

---

## 6. What to Do

- Read CLRS §34.1 (polynomial time) and §34.2 (verification). These two sections are the whole of this
  lecture, stated carefully.
- **There is no problem set this week.** **PROJECT 2 and PS 11 are both due Friday**, and the **FINAL
  EXAM** is this week.
- **Lab 12** implements the TSP approximation from Lecture 39.
- Next lecture: reductions — how to prove a problem is hard by relating it to one already known to be.

---

*CS 102 · Week 12 · Lecture 37 · © CSE Department*
