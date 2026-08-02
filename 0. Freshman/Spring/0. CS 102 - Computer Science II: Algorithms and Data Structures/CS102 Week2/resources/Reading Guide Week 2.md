# CS 102 — Reading Guide, Week 2
## Balanced Binary Search Trees

---

## Required

**CLRS, 4th ed. — Chapter 13, §13.1–13.4** (Red-Black Trees)
**CLRS, 4th ed. — §18.1** (B-tree definition only)

A warning about the primary text: **CLRS does not cover AVL trees in the main chapters.** They appear
as Problem 13-3 at the end of Chapter 13. Chapter 13 is nonetheless the right reading, because §13.2
is the definitive treatment of rotations and the argument in §13.1 is the model for the one you will
reproduce.

For AVL specifically:

- **Sedgewick & Wayne, *Algorithms* 4th ed., §3.3** — balanced search trees, excellent diagrams.
  Their presentation is of left-leaning red-black trees, so read it for the *rotation mechanics* and
  the pictures rather than for the invariant.
- **Weiss, *Data Structures and Algorithm Analysis*, Chapter 4** — the standard AVL treatment, with
  the $N(h)$ recurrence worked out in full. If your library has it, this is the best single source
  for Lecture 08.

---

## How to Read Chapter 13

**§13.1 (properties, 6 pages).** Read the five properties, then read the proof of Lemma 13.1 — the
$h \le 2\log_2(n+1)$ bound — twice. **The two-step structure of that proof is the thing to take
away**: bound the node count from below using black-height, then bound black-height from below using
the no-two-reds rule. Lecture 09 uses exactly this shape.

**§13.2 (rotations, 4 pages).** Short and essential. Confirm for yourself that Figure 13.2's before
and after have the same inorder sequence. The code here is the code you will write.

**§13.3 (insertion, 10 pages).** The three cases and their mirror images. **Read for the idea, not
for memorisation** — you are not examined on red-black insertion code. The idea worth having is that
the fix-up loop moves a "violation" up the tree until it can be discharged.

**§13.4 (deletion, 10 pages).** The hardest section in the chapter. Read it once, slowly, and do not
be discouraged. **The one fact to retain is that it terminates after at most three rotations**, and
why that is the property libraries want.

**§18.1 (B-trees, 6 pages).** Read only the definition and the height bound. Skip §18.2–18.3.

---

## Guiding Questions

Answer these as you read. They are not submitted, and three of them are on the midterm.

1. §13.2: a rotation is $O(1)$. Which quantities does it change, and which does it leave alone?
   Why does the pointer count not depend on subtree size?

2. §13.1, Lemma 13.1: where exactly is property 4 (no red with a red child) used? What would the
   bound become if the tree merely satisfied properties 1, 2, 3, and 5?

3. Both AVL and red-black trees are $O(\log n)$ tall. **Which constant is smaller, and by how much?**
   Reconcile your answer with the measurements in Lecture 09 §3.

4. §13.3: why does the fix-up loop terminate? What is the quantity that decreases?

5. AVL insertion needs at most one rebalance; AVL deletion may need one per level. **Locate the exact
   step in the argument where the two cases diverge.**

6. §18.1: a B-tree node holds up to $2t-1$ keys. What sets $t$ in practice, and what happens to the
   height if you halve it?

7. Lecture 09 measured `SortedList` beating a hand-written AVL tree by 16× while having worse
   asymptotic complexity. **Is that a criticism of asymptotic analysis?** Argue both sides in a
   paragraph, then commit to one.

---

## Optional

- **Adelson-Velsky & Landis (1962)**, *An algorithm for the organisation of information* — the
  original AVL paper, three pages, translated from Russian. Worth reading purely to see how compact
  the original statement of a now-standard result can be.
- **Sedgewick, *Left-Leaning Red-Black Trees* (2008)** — a simplification of red-black insertion to
  about 30 lines, along with an argument about why the standard presentation is harder than it needs
  to be. Read after you have suffered through §13.3.
- **Bayer & McCreight (1972)**, the original B-tree paper. Section 1's discussion of the cost model is
  still the clearest statement of why disk changes everything.

---

## Common Misreadings

**"An AVL tree is balanced, so it is nearly perfect."** It is within a factor of 1.44 of perfect in
the *worst* case. That is a strong guarantee, not a claim of near-perfection.

**"Red-black trees rotate less than AVL trees."** True for deletion; **false for insertion on sorted
input**, where Lecture 09 measures the two within 0.02% of each other. Check which operation a claim
like this is about.

**"Rotations are expensive because they move subtrees."** They re-parent subtrees. Nothing inside
$A$, $B$, or $C$ is read or written. This is why a rotation is $O(1)$ and not $O(\text{size})$.

**"CLRS covers AVL trees."** It does not, except as an end-of-chapter problem. If you are looking for
the AVL height proof in Chapter 13, you will not find it — see Weiss, or Lecture 08 §3.

---

*CS 102 · Week 2 · Reading Guide · © CSE Department*
