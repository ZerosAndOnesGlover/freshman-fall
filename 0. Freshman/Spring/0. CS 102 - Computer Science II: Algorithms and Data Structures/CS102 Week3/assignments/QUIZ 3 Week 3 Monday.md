# CS 102 · Quiz 3

**Week 3, Monday, first 15 minutes of lecture · 20 points**
**Covers Week 2** — rotations, AVL trees, and red-black trees. **Not** this week's material.

Closed book. No calculator required — every number here is exact.
Height counts **edges**; a leaf has height 0 and the empty tree has height $-1$.
Balance factor is $\mathrm{bf}(v) = h(v.\text{left}) - h(v.\text{right})$.

---

**Q1.** *(4)* For the tree

```
        50
       /  \
     30    70
    /  \
  20    40
  /
10
```

- **(a)** Give $\mathrm{bf}(50)$, $\mathrm{bf}(30)$, and $\mathrm{bf}(20)$.
- **(b)** Is this a valid AVL tree? If not, name the **lowest** violating node.
- **(c)** Which of the four cases is it — LL, RR, LR, or RL — and which rotation repairs it?

---

**Q2.** *(3)* Apply your answer to Q1(c). Draw the resulting tree and confirm it is a valid AVL tree.

State the one property the rotation is guaranteed to preserve, and how you would check it in a single
line of code.

---

**Q3.** *(4)* Insert $30, 10, 20$ into an empty AVL tree in that order.

- **(a)** Name the case.
- **(b)** A classmate applies a single `rotate_right` at the root. Give the tree they get and its
  root's balance factor.
- **(c)** In one sentence, say why one rotation cannot work here.

---

**Q4.** *(3)* Let $N(h)$ be the **minimum** number of nodes in an AVL tree of height $h$.

- **(a)** Write the recurrence, with its two base cases.
- **(b)** Give $N(4)$.

---

**Q5.** *(4)* Each tree below is either a valid red-black tree or violates **exactly one** property.
For each, say **valid**, or name the violated property and the node responsible. `R` = red, `B` =
black; `NIL` leaves are omitted.

```
A:            20B                B:            20B               C:        10B
             /   \                            /   \                       /   \
          10R     30B                      10R     30B                  5B     20B
         /   \                            /   \                        /
       5B     15B                       5R     15B                   3B
                                       /  \
                                     3B    7B
```

---

**Q6.** *(2)* An AVL **insertion** triggers at most one rebalance event. An AVL **deletion** can
trigger one at every level.

State in one sentence what is true after an insertion's rotation that is **not** true after a
deletion's.

---

*20 points total. Solutions posted after Wednesday's lecture.*

*CS 102 · Week 3 · Quiz 3 · © CSE Department*
