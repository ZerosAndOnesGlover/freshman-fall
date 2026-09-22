# CS 102 · Quiz 8

**Date:** Monday 15 March 2027 · 09:00–09:15 (start of L25) · Week 8 · 20 points
**Covers Week 7** — optimal substructure, memoisation, LCS, edit distance, knapsack. **Not** this
week's material.

Closed book. Every number here is exact.

---

**Q1.** *(3)* State the **two** conditions a problem must satisfy for dynamic programming to apply.

For each, name a problem that fails it, and say what technique applies to that problem instead.

---

**Q2.** *(4)* Fill in the LCS table for $a = $ `ABC`, $b = $ `BAC` and give the LCS length.

Then give **two distinct** longest common subsequences, and say what that tells you about the
uniqueness of the answer versus the uniqueness of the length.

---

**Q3.** *(3)* Write the edit-distance recurrence, **including the base cases**.

Say in one sentence what goes wrong if the base cases are all set to 0.

---

**Q4.** *(4)* 0/1 knapsack runs in $\Theta(nW)$.

- **(a)** *(2)* Explain why this is **not** polynomial in the input size.
- **(b)** *(2)* By what factor does the running time change if you add one bit to $W$?

---

**Q5.** *(3)* In the space-optimised knapsack, the inner loop over capacity runs **downwards**.

Someone changes it to run upwards. Their code does not crash and returns plausible numbers.

**What problem does their code now solve?**

---

**Q6.** *(3)* Memoisation and tabulation have the same asymptotic complexity.

Give **one** situation where memoisation does dramatically less work, and **one** where tabulation is
the only option that works at all.

---

*20 points total. Solutions posted after Wednesday's lecture.*

*CS 102 · Week 8 · Quiz 8 · © CSE Department*
