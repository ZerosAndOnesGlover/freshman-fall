# MATH 151 · Alignment Audit and Build Plan
### Authority: `5. Academic Registry/1. Scheduling/Year1 - Freshman/CSE_Year1_Freshman_Curriculum.docx`

*Written before any files were changed. Same procedure as the PROG 101 and MATH 141 realignments.*

---

## 1. The docx curriculum

| Week | docx topic | Built? |
|---|---|---|
| 0 | Logic: propositions, connectives, truth tables, tautologies | ✅ |
| 1 | Predicate logic, quantifiers, logical equivalences | ✅ |
| 2 | Proof techniques: direct, contradiction, contrapositive | ✅ |
| 3 | Proof by induction: weak and strong | ✅ |
| 4 | Sets: operations, power sets, Cartesian products | ✅ |
| 5 | Functions: injective, surjective, bijective; composition, inverse | ⚠️ **drifted** |
| 6 | Relations: reflexive, symmetric, transitive; equivalence classes | ✅ |
| 7 | Counting: permutations, combinations, the multiplication rule | ✅ |
| 8 | **Advanced counting: pigeonhole principle, inclusion–exclusion** | ❌ |
| 9 | **Recurrence relations and generating functions** | ❌ |
| 10 | **Graphs: terminology, representations, paths, connectivity** | ❌ |
| 11 | **Trees, spanning trees, graph algorithms (BFS/DFS)** | ❌ |
| 12 | **Number theory: divisibility, primes, modular arithmetic; review** | ❌ |

**Weeks 0–7 exist and are substantial** (13 files each, ~123,000 words total). **Weeks 8–12 do not
exist at all.**

---

## 2. The one drift found

**`MATH151 Week5/lectures/L17 Pigeonhole Principle.md` is in the wrong week.**

The docx assigns the pigeonhole principle to **Week 8** (Advanced Counting), alongside
inclusion–exclusion. It is currently taught in **Week 5**, whose docx topic is functions only.

`MATH151 Week5/resources/Pigeonhole Patterns Reference.md` has drifted with it.

**Why it happened, and why it is defensible but still wrong:** pigeonhole is classically motivated
by functions — there is no injection from a larger finite set to a smaller one — so placing it
immediately after Week 5's injective/surjective material reads naturally. But the docx is the
authority for this vault, it groups pigeonhole with inclusion–exclusion as *counting* technique, and
Week 8 cannot be built coherently with its headline topic already spent.

### Complication: lecture numbering is global

MATH 151 numbers lectures `L00`–`L23` continuously, three per week, so Week *N* owns
`L(3N)`–`L(3N+2)`. Relocating L17 to Week 8 would break that invariant for every later week.

**Resolution — content moves, slots do not:**

| Action | Detail |
|---|---|
| Pigeonhole *content* → Week 8 | Re-homed and renumbered as **L24**, Week 8's first lecture |
| [[Pigeonhole Patterns Reference]] → Week 8 | Moves to `MATH151 Week8/resources/` |
| Week 5's **L17 slot** is refilled | New lecture on **bijections, cardinality, and counting with functions** — squarely docx Week 5 material, and the honest home for the "no injection into a smaller set" idea that motivated the misplacement |

No written work is discarded and the global numbering invariant survives.

---

## 3. Build plan — Weeks 8 to 12

Each week follows the established MATH 151 shape (13 files):

```
README.md
assignments/PS N <Topic>.md
lab/LAB N <Topic> Workshop.md
lectures/L<n> …  ×3
quiz/QUIZ N <prior week topic>.md
quiz/QUIZ N+1 Preview.md
resources/<Topic> Reference.md  ×2
solutions_instructor/{LAB N, PS N, QUIZ N} Solutions.md
```

| Week | Lectures | Assets |
|---|---|---|
| **8** | L24 Pigeonhole Principle *(re-homed)* · L25 Inclusion–Exclusion · L26 Generalised Pigeonhole and Ramsey Flavour | PS 8, Lab 8, Quiz 8 (Counting), Quiz 9 Preview, 2 references |
| **9** | L27 Recurrence Relations · L28 Solving Linear Recurrences · L29 Generating Functions | PS 9, Lab 9, Quiz 9 (Advanced Counting), Quiz 10 Preview, 2 references |
| **10** | L30 Graph Terminology · L31 Representations and Isomorphism · L32 Paths, Connectivity, Euler and Hamilton | PS 10, Lab 10, Quiz 10 (Recurrences), Quiz 11 Preview, 2 references |
| **11** | L33 Trees and Their Properties · L34 Spanning Trees · L35 BFS and DFS | PS 11, Lab 11, Quiz 11 (Graphs), Quiz 12 Preview, 2 references |
| **12** | L36 Divisibility and Primes · L37 Modular Arithmetic and the GCD · L38 Review and the Road Ahead | PS 12, Lab 12, Quiz 12 (Trees/Graphs), 2 references |

**Quiz convention preserved:** Quiz *N* covers Week *N−1*; each week also ships next week's preview.

---

## 4. Verification discipline

The same rules that governed CS 101, PROG 101 and MATH 141 apply, with one addition specific to
discrete mathematics:

- **Every count is computed, never asserted.** Binomial identities, inclusion–exclusion totals,
  derangement numbers, Catalan numbers, recurrence closed forms — all checked against brute-force
  enumeration in Python for small *n* before being written down.
- **Every graph claim is checked on an explicit graph.** Adjacency matrices, degree sums, BFS/DFS
  orders, spanning-tree counts (Cayley, Matrix-Tree) verified by running them.
- **Every number-theory claim is checked.** GCDs by Euclid, modular inverses, CRT reconstructions,
  primality — all executed.
- Point totals reconciled against each grading table **as the file is assembled**, not afterwards.
- Cross-week references checked against actual week contents before the week is called done.

---

*MATH 151 · Realignment Plan · superseded only by the docx*
