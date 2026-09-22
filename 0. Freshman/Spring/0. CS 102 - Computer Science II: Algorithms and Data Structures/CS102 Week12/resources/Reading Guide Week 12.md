# CS 102 · Reading Guide, Week 12
## NP-Completeness and the Limits of Efficiency

---

## Required

**CLRS, 4th ed. — Chapter 34** (NP-Completeness), §34.1–34.5, about 60 pages.
**CLRS, 4th ed. — Chapter 35** (Approximation Algorithms), §35.1–35.3 and §35.5.

- §34.1 polynomial time
- §34.2 **polynomial-time verification** — the definition of NP, and the one people get wrong
- §34.3 NP-completeness and reducibility, including Cook–Levin
- §34.4 NP-completeness proofs
- §34.5 five worked NP-complete problems — **read at least vertex cover**
- §35.1 vertex cover, §35.2 TSP, §35.3 set cover, §35.5 subset-sum

> **The FINAL EXAM is Wednesday 21 April and is comprehensive**, and **PROJECT 2 and PS 11 are due Friday 16 April**.
> Chapter 34 is long. If you read three sections, read **§34.2, §34.3's statement of Cook–Levin, and
> §35.1**.

Also useful:

- **Garey & Johnson, *Computers and Intractability* (1979)** — the catalogue. Still the standard
  reference, and its appendix of several hundred NP-complete problems is genuinely the thing you reach
  for in practice.
- **Sipser, *Introduction to the Theory of Computation*, Ch. 7** — a cleaner treatment of the theory
  than CLRS, if you want the theory rather than the algorithms.
- **Aaronson, "P =? NP" (2017 survey)** — readable, and the best account of *why* the question is hard
  to settle.

---

## Read §34.2 Twice

**NP does not mean "non-polynomial".** It means *nondeterministic polynomial time*, and the working
definition is:

> A problem is in NP if every **yes** instance has a short certificate that can be **checked** in
> polynomial time.

Almost every misunderstanding of this topic traces back to that sentence. Note what it does *not* say:
it says nothing about finding the certificate, and nothing about **no** instances.

CLRS is careful about the second point, and it is worth pausing on. Nothing in the definition gives a
short proof that a formula is *un*satisfiable. That asymmetry is why **co-NP** exists as a separate
class, and it has a practical consequence you can see: a SAT solver reporting "satisfiable" hands you
an assignment you can verify in a second; one reporting "unsatisfiable" is asking to be trusted.

---

## How to Read It

**§34.1 (10 pages).** Encodings and what "polynomial in the input size" means. **Read the discussion of
encodings** — it is where Week 7's pseudo-polynomial knapsack gets its explanation. A number written in
binary has length $\log W$, and that single fact is the whole of it.

**§34.2 (10 pages).** Verification, certificates, and the definition of NP. The most important section.

**§34.3 (14 pages).** Reducibility and NP-completeness, ending with Cook–Levin. **Read the definition
of $\le_p$ and the statement of the theorem carefully; skim the proof.** The proof is a landmark and it
is explicitly not examinable.

**§34.4 (6 pages).** How to prove a new problem NP-complete: show it is in NP, then reduce a known
NP-complete problem **to** it. **The direction is the content of this section**, and getting it
backwards is the classic error.

**§34.5 (16 pages).** Clique, vertex cover, Hamiltonian cycle, TSP, subset sum. Read the vertex cover
reduction in full — it is the clearest gadget construction in the chapter and the model for the rest.

**Chapter 35.** Read §35.1 and §35.2 properly; both proofs are three lines and both are examinable.
§35.5's PTAS for subset-sum is the answer to "can we do arbitrarily well?" and is worth the twenty
minutes.

---

## Guiding Questions

Three of these are on the final.

1. State the definition of NP precisely. Then give the certificate, and its checking time, for TSP,
   vertex cover, and subset sum.

2. Why is $P \subseteq NP$ immediate? What would it take to show the containment is strict?

3. §34.4: to prove $B$ is NP-complete you reduce a known-hard $A$ **to** $B$. Explain in one sentence
   why the other direction proves nothing.

4. Week 7's knapsack runs in $\Theta(nW)$ and knapsack is NP-complete. Reconcile these, using §34.1's
   discussion of encodings.

5. Four problems in this course are NP-complete in general and easy under a restriction you
   implemented. Name them and the restriction in each case.

6. §35.2: the MST tour is a 2-approximation for **metric** TSP. Which of the three proof steps uses the
   triangle inequality, and what is known about approximating general TSP?

7. Knapsack has a PTAS; max clique has essentially no approximation. Both are NP-complete. **What does
   NP-completeness therefore not tell you?**

---

## Common Misreadings

**"NP means non-polynomial."** It means nondeterministic polynomial. Every problem in P is also in NP.

**"NP-complete means unsolvable."** It means no *polynomial* algorithm is known and one would imply
P = NP. Held–Karp solves TSP exactly; it takes 14.8 seconds at $n = 20$ and about two years at
$n = 40$. That is intractable, not impossible. **Undecidable** — the halting problem — is the stronger
condition, and it is not what this week is about.

**"NP-hard and NP-complete are the same."** NP-complete requires membership in NP as well as hardness.
The *optimisation* version of TSP is NP-hard and not known to be in NP, because "this tour is optimal"
has no obvious short certificate.

**"To prove my problem is hard, reduce it to SAT."** Backwards. That shows your problem is *no harder*
than SAT, which is true of everything in NP. Reduce **from** a known-hard problem **to** yours.

**"If P ≠ NP then NP-complete problems can't be approximated."** Unrelated. Knapsack is NP-complete and
admits an arbitrarily good approximation; max clique is NP-complete and admits essentially none.
**NP-completeness is about exact solution and says nothing about approximation.**

**"A heuristic that beats the approximation algorithm is better."** 2-opt averaged 0.5% above optimal
and found the exact answer 84% of the time; the MST 2-approximation averaged 11% above. **2-opt has no
guarantee at all.** What you can say about the first is "it was good on my sample"; about the second,
"it will never be worse than 2× on any input".

**"The 2-approximation for TSP always works."** Only with the triangle inequality. Measured on
non-metric instances the worst ratio reached **4.0** and the bound was violated 42 times in 2,000. And
for general TSP, **no** constant-factor approximation exists unless P = NP.

---

## If You Have Extra Time

**Christofides' algorithm.** 1.5-approximation for metric TSP — MST plus a minimum-weight perfect
matching on the odd-degree vertices, then an Euler tour with shortcuts. It held the record for
**forty-five years**, and the 2020 improvement was by about $10^{-36}$. Understanding why the matching
step is the right idea is a good afternoon.

**The PCP theorem and inapproximability.** The results saying "no better approximation is possible
unless P = NP" come from a characterisation of NP in terms of probabilistically checkable proofs. It is
one of the deepest results in the field and the statement alone is worth knowing.

**Modern SAT solvers.** SAT is the canonical NP-complete problem and industrial solvers routinely
handle instances with millions of variables — through conflict-driven clause learning, which is a
beautiful piece of engineering. **Worst-case hardness does not mean your instances are hard**, and SAT
solvers are the best illustration in computing.

**Parameterised complexity.** A finer-grained theory: vertex cover is solvable in $O(2^k n)$ where $k$
is the cover's size, so it is tractable whenever the answer is small even though the problem is
NP-complete. It is often the right lens when your instances have structure.

**The Clay Millennium Prize.** One million dollars, unclaimed since 2000. You are now equipped to
understand the problem statement, which is more than most people with an opinion about it.

---

*CS 102 · Week 12 · Reading Guide · © CSE Department*
