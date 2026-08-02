# MATH 151 — Hasse Diagram Reference
## Week 6: Partial Orders and Diagram Construction

---

## Construction Checklist

To draw a Hasse diagram for poset $(A,\preceq)$:

1. **List all elements** of $A$ as nodes.
2. **Find all covering relations:** $a\lessdot b$ means $a\prec b$ and no $c$ exists with $a\prec c\prec b$.
3. **Position nodes:** if $a\prec b$, place $b$ physically higher than $a$.
4. **Draw edges** only for covering relations — a straight line, NO arrowhead.
5. **Never draw:** self-loops, edges for non-covering relations (these are implied by transitively following lines upward).

---

## Worked Example 1 — Divisors of 12

$A=\{1,2,3,4,6,12\}$, order = divisibility.

**Step 1 — Find all divisibility pairs:**
$1\mid2,1\mid3,1\mid4,1\mid6,1\mid12$
$2\mid4,2\mid6,2\mid12$
$3\mid6,3\mid12$
$4\mid12$
$6\mid12$

**Step 2 — Remove non-covering pairs (those with an intermediate):**
$1\mid4$: intermediate 2 exists ($1\mid2\mid4$) → NOT a covering relation, remove.
$1\mid6$: intermediate 2 or 3 exists → remove.
$1\mid12$: intermediate 2,3,4,6 exist → remove.
$2\mid12$: intermediate 4 or 6 exists → remove.
$3\mid12$: intermediate 6 exists → remove.

**Remaining covering relations:**
$1\lessdot2,\ 1\lessdot3,\ 2\lessdot4,\ 2\lessdot6,\ 3\lessdot6,\ 4\lessdot12,\ 6\lessdot12$

**Step 3 — Diagram (levels by "depth"):**

```
Level 3:         12
                 /  \
Level 2:        4    6
                |   / |
Level 1:        2 /   3
                 \/   /
                 /\  /
Level 0:          1
```

Cleaner ASCII rendering:
```
       12
      /  \
     4    6
     |   /|
     |  / |
     2 /  3
     \ /  /
      \  /
       1
```
(In-class: this is drawn properly on a whiteboard with clean line routing; 1 connects up to both 2 and 3; 2 connects up to 4 and 6; 3 connects up to 6; both 4 and 6 connect up to 12.)

---

## Worked Example 2 — Power Set of {a,b,c}

$A=\mathcal{P}(\{a,b,c\})$, order = $\subseteq$.

**Elements by size:**
- Size 0: $\emptyset$
- Size 1: $\{a\},\{b\},\{c\}$
- Size 2: $\{a,b\},\{a,c\},\{b,c\}$
- Size 3: $\{a,b,c\}$

**Covering relations:** every set of size $k$ is covered by exactly the sets of size $k+1$ obtained by adding one element.

$$\emptyset\lessdot\{a\},\ \emptyset\lessdot\{b\},\ \emptyset\lessdot\{c\}$$
$$\{a\}\lessdot\{a,b\},\ \{a\}\lessdot\{a,c\},\ \{b\}\lessdot\{a,b\},\ \{b\}\lessdot\{b,c\},\ \{c\}\lessdot\{a,c\},\ \{c\}\lessdot\{b,c\}$$
$$\{a,b\}\lessdot\{a,b,c\},\ \{a,c\}\lessdot\{a,b,c\},\ \{b,c\}\lessdot\{a,b,c\}$$

**Structure:** this is the classic "cube" — 8 vertices, 12 edges, exactly the vertex-edge structure of a 3-dimensional cube graph. Each level corresponds to subset size, matching row $k$ of Pascal's Triangle: $\binom{3}{0}=1,\binom{3}{1}=3,\binom{3}{2}=3,\binom{3}{3}=1$ (preview of Week 7!).

```
            {a,b,c}
           /   |   \
      {a,b}  {a,c}  {b,c}
        |  \  / \  /  |
        |   \/   \/   |
        |   /\   /\   |
       {a}    {b}    {c}
          \    |    /
           \   |   /
              ∅
```

---

## Worked Example 3 — A Non-Divisibility Poset (String Prefix Order)

Consider short strings ordered by "is a prefix of": $A=\{\epsilon, a, ab, abc, b, ba\}$ (where $\epsilon$ is empty string).

**Covering relations:**
$\epsilon\lessdot a,\ \epsilon\lessdot b$
$a\lessdot ab$
$ab\lessdot abc$
$b\lessdot ba$

**Structure:** two separate "chains" growing from $\epsilon$ — this poset is NOT connected as a single chain; $a$ and $b$ are incomparable, and everything descending from $a$ is incomparable with everything descending from $b$ (except through $\epsilon$).

```
abc      ba
 |        |
ab        b
 |       /
 a      /
  \    /
   \  /
    ε
```

---

## Reading Facts Off a Hasse Diagram

Given a completed Hasse diagram:

| To find... | Look for... |
|---|---|
| $a\preceq b$ | An upward path (following edges upward) from $a$ to $b$ |
| Maximal elements | Nodes with nothing directly above (top of any upward path) |
| Minimal elements | Nodes with nothing directly below (bottom of any upward path) |
| Maximum | A single node reachable upward FROM every other node (only exists if diagram has one "top") |
| Minimum | A single node from which every other node is reachable upward (only exists if diagram has one "bottom") |
| A chain | Any set of nodes lying along a single upward path |
| An antichain | Any set of nodes with no upward paths between any pair (often a single "level") |

---

## Common Diagram Mistakes

| Mistake | Why Wrong |
|---|---|
| Drawing an edge for every $\preceq$ pair, not just covers | Redundant — transitivity is implied; diagram becomes unreadable |
| Adding arrowheads | Unnecessary — the vertical position (up = greater) already encodes direction |
| Drawing self-loops | Reflexivity is always implied for a poset; never draw them |
| Placing incomparable elements at different heights arbitrarily | Should reflect only genuine order relationships; incomparable elements can be drawn at the same or different heights, but no edge implies no order relation between them |
| Missing a covering relation because "it's implied by a longer path" | Only remove edges that are implied by ANOTHER DIRECT path through an intermediate element in the poset — verify carefully |

---

## Topological Sort from a Hasse Diagram — Algorithm

1. Identify all minimal elements (bottom of the diagram, or more precisely: no incoming covering edges from below).
2. Pick any one; output it; remove it (and its edges) from the diagram.
3. Repeat: some element becomes minimal after removal (possibly newly exposed); pick any minimal element.
4. Continue until diagram is empty.

**Multiple valid outputs exist whenever multiple minimal elements are available at some step** — this is exactly why several different topological sorts can satisfy the same partial order.
