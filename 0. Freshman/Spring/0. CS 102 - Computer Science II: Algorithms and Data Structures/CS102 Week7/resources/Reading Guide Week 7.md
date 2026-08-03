# CS 102 · Reading Guide, Week 7
## Dynamic Programming I

---

## Required

**CLRS, 4th ed. — Chapter 14, §14.1–14.4** (Dynamic Programming), about 35 pages.

- §14.1 rod cutting — the introduction, and the best one in the book
- §14.2 matrix chain multiplication — **skim for now**, it is Week 8's material
- §14.3 **elements of dynamic programming** — the most important section this week
- §14.4 longest common subsequence

Knapsack is Problem 14-2; edit distance is Problem 14-5. Both are set on PS 7.

Also useful:

- **Skiena §10** — the practitioner's view of DP, and unusually good on *how to find the state*, which
  is the part textbooks skip.
- **Kleinberg & Tardos, Chapter 6** — if your library has it, the best DP chapter in print. §6.6 on
  sequence alignment and §6.7 on Hirschberg's linear-space algorithm are exactly Project 1.

---

## Read §14.3 Twice

Chapter 14 works four examples, and it is tempting to read them as four recipes. **§14.3 is where the
chapter says what they have in common**, and it is the only part that transfers to a problem you have
not seen.

The two conditions it names — **optimal substructure** and **overlapping subproblems** — are what you
should be testing any new problem against. Note that CLRS is careful to give a problem *without*
optimal substructure (longest simple path, §14.3) and to explain why. That example is worth more than
any of the four that work.

---

## How to Read It

**§14.1 (rod cutting, 12 pages).** Long because it introduces everything: the naive recursion, the
exponential blow-up, memoisation, tabulation, the subproblem graph, and reconstructing a solution.
**The subproblem-graph picture (Figure 14.4) is the one to keep** — it makes "overlapping subproblems"
concrete, and it is the object Lab 7 Part D measures.

**§14.2 (matrix chain, 10 pages).** Skim. Come back in Week 8, when it is the main event.

**§14.3 (elements of DP, 8 pages).** Read properly, then read again after doing PS 7 Part E. The
subsection on **subproblem graphs** explains why the running time is (number of states) × (work per
state), which is the only complexity formula you need this week.

**§14.4 (LCS, 8 pages).** The clean worked example. CLRS builds a separate table of arrows for the
traceback; storing arrows is unnecessary — you can recompute the direction from the values, as
Lecture 23 does — but the arrow table makes the picture clearer, which is why Lab 7 asks for it.

---

## Guiding Questions

Three of these are on MIDTERM 2.

1. §14.3: state both conditions for DP to apply. For each, give a problem that **fails** that
   condition and say what technique applies instead.

2. §14.1: the naive rod-cutting recursion is exponential. What exactly is the redundancy — which
   subproblem is solved most often, and how many times?

3. §14.3: the running time is (number of subproblems) × (work per subproblem). Apply that formula to
   LCS and to 0/1 knapsack, and say what "number of subproblems" is in each.

4. Memoisation and tabulation have the same asymptotic complexity. Name **two** situations where one
   is clearly preferable, and give the reason in each case.

5. §14.4: the LCS recurrence takes a match greedily when the last characters agree. **Why is that
   safe?** (The argument is an exchange argument — the same device as Week 6's cut property.)

6. 0/1 knapsack runs in $\Theta(nW)$, and the problem is NP-complete. Reconcile these.

7. Bellman–Ford (Week 5) is a dynamic program. What are its subproblems, and how many are there?

---

## Common Misreadings

**"DP means filling a table."** DP means not recomputing. The table is one mechanism; a dictionary and
a recursion is another, and for sparse state spaces it does dramatically less work — measured at
**1,242× fewer subproblems** on one knapsack instance in Lecture 22 §5.

**"Memoisation and tabulation are the same thing, so pick either."** They compute the same *values*
and generally not the same *set* of them. See above. They also differ on recursion depth, on how easy
the space optimisation is, and on constant factors — measured at about 6× on Fibonacci.

**"$\Theta(nW)$ is polynomial."** It is polynomial in $W$, and $W$ is exponential in the input size —
the input contains $W$ written in $\log_2 W$ bits. Add one bit and the running time doubles. This is
**pseudo-polynomial**, and it is the single most misunderstood claim in the chapter.

**"LCS and edit distance are the same problem."** They coincide only when substitution is disallowed:
$D_{\text{indel}} = |a| + |b| - 2\,\mathrm{LCS}$. With substitution the answers differ — `abcd` to
`dcba` has indel distance 6 and edit distance 4.

**"A subsequence is a substring."** A substring is contiguous; a subsequence is not. `ACE` is a
subsequence of `ABCDE` and not a substring. The two problems have different recurrences and different
answers.

**"The DP gives the answer."** The DP gives the *value*. Recovering the actual solution needs the
table and a traceback, and if you rolled the table down to two rows to save space, **you cannot** —
which is precisely the problem Hirschberg's algorithm solves and Project 1 asks you to implement.

---

## If You Have Extra Time

**Hirschberg's algorithm** — linear-space LCS *with* recovery, by divide-and-conquer. Kleinberg &
Tardos §6.7 is the clearest treatment. It is Project 1 Part 3, and it is the most elegant single
algorithm in this course: $\Theta(nm)$ time and $\Theta(\min(n,m))$ space, measured at **139× less
memory for 1.18× the time**.

**The Hunt–Szymanski algorithm.** Real `diff` implementations do not use the $\Theta(nm)$ table. When
the files are similar the number of matching line *pairs* is small, and Hunt–Szymanski runs in
$O((r + n)\log n)$ where $r$ is that number. Understanding why it beats the textbook algorithm on real
input, and loses on adversarial input, is a good exercise in reading a bound properly.

**Myers' diff algorithm** (1986) is what `git` actually uses — an $O(ND)$ method where $D$ is the size
of the edit script, so it is fast exactly when the files are similar. The paper is readable and short.

**The four-Russians trick** speeds up edit distance by a $\log$ factor using precomputed blocks. It is
also a reasonable place to first meet the idea that you can precompute answers for all small inputs.

---

*CS 102 · Week 7 · Reading Guide · © CSE Department*
