# CS 102 · Computer Science II: Algorithms and Data Structures
## Course Overview and Syllabus
### Year 1 · Spring · 4 credits

---

## Course Identity

| | |
| --- | --- |
| **Code** | CS 102 |
| **Title** | Computer Science II: Algorithms and Data Structures |
| **Credits** | 4 (3 lecture + 1 lab) |
| **Semester** | Spring, Year 1 |
| **Meeting** | 3 lectures per week + one 2-hour lab section |
| **Prerequisites** | **CS 101, MATH 151** |
| **Languages** | Python 3 (primary), C (for the memory-sensitive work) |
| **Assessment** | **Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%** |

---

## Course Description

CS 102 is where you become a systems thinker. CS 101 gave you the basic vocabulary — algorithms,
complexity, data structures. **CS 102 expands that vocabulary dramatically and teaches you to design
algorithms from scratch.**

You will encounter trees and graphs — the data structures that power the internet, your file system,
your GPS, and every social network on earth. You will learn dynamic programming, the technique
underlying sequence alignment in genomics, speech recognition, and route optimisation.

By the end you will be able to read a problem, identify its structure, choose or design an
appropriate algorithm, implement it correctly in Python or C, **prove its correctness**, and analyse
its time and space complexity. This is the core competency of a computer scientist.

---

## What Makes This Course Different From CS 101

CS 101 asked you to implement algorithms that were described to you. **CS 102 asks you to design
algorithms that nobody has described to you**, and then to prove they work.

The shift is real and most students feel it around Week 4. Three things change:

1. **Correctness must be argued, not tested.** A passing test suite is evidence, not proof. From
   Week 0 you will be asked to state loop invariants and to argue by induction.
2. **The data structure is the algorithm.** Choosing a heap over a sorted list is not an
   implementation detail; it is the difference between $O(n \log n)$ and $O(n^2)$.
3. **There is no single right answer.** Most weeks present two or three algorithms for the same
   problem with different trade-offs, and part of the assessment is defending a choice.

**MATH 151 is a hard prerequisite, not a formality.** Induction, recurrence relations, graph
terminology, and summation manipulation are used from Week 0 without re-teaching.

---

## Weekly Schedule

| Week | Topic | Assessments |
| --- | --- | --- |
| **0** | Review and Course Overview | Lab 0 |
| **1** | Binary Trees and Binary Search Trees | PS 1, Lab 1, Quiz 1 |
| **2** | Balanced BSTs: AVL Trees and Red-Black Trees | PS 2, Lab 2, Quiz 2 |
| **3** | Heaps and Priority Queues | PS 3, Lab 3, Quiz 3 |
| **4** | Graphs I: Representations and Traversals | PS 4, Lab 4, Quiz 4 · *Midterm 1 announced* |
| **5** | Graphs II: Shortest Paths | PS 5, Lab 5, Quiz 5 · **MIDTERM 1** (Weeks 0–4) |
| **6** | Graphs III: Minimum Spanning Trees | PS 6, Lab 6, Quiz 6 |
| **7** | Dynamic Programming I: Principles | PS 7, Lab 7, Quiz 7 · **Project 1 assigned** |
| **8** | Dynamic Programming II: Applications | PS 8, Lab 8, Quiz 8 |
| **9** | Greedy Algorithms | PS 9, Lab 9, Quiz 9 · **Project 1 due** |
| **10** | String Algorithms | PS 10, Lab 10, Quiz 10 · **MIDTERM 2** (Weeks 5–9) |
| **11** | Computational Geometry and Advanced Data Structures | PS 11, Lab 11, Quiz 11 |
| **12** | NP-Completeness and the Limits of Efficiency | Lab 12 · **FINAL EXAM** · **Project 2 due** |

---

## Assessment Breakdown

| Component | Weight | Details |
| --- | --- | --- |
| **Problem Sets (11)** | 35% | PS 1–11, released Friday, due the following Friday. **Lowest 1 dropped.** No problem set in Weeks 0 or 12. |
| **Midterm Exam 1** (Week 5) | 12.5% | 75 minutes. Covers Weeks 0–4. One handwritten sheet, 1 side. |
| **Midterm Exam 2** (Week 10) | 12.5% | 75 minutes. Covers Weeks 5–9. Same rules. |
| **Final Exam** (Week 12) | 20% | Comprehensive, 180 minutes. Two handwritten sheets. |
| **Project 1** (assigned Week 7, due Week 9) | 10% | Substantial implementation with a written analysis. |
| **Project 2** (due Week 12) | 10% | Second project, assigned Week 10. |
| **Total** | **100%** | |

> **These weights come directly from the Year 1 curriculum document**, which specifies *Problem Sets
> 35%, Midterms 25%, Final 20%, Projects 20%*. The only elaboration is the split of Midterms into two
> equal halves and Projects into two equal halves. **No component has been added or removed.**

### Labs and Quizzes Carry No Direct Weight

This is deliberate and it is what the curriculum specifies — the assessment line above sums to 100%
without them.

**They are still required.**

- **Labs (13, Weeks 0–12)** are marked on completion and correctness with an in-lab checkoff. **You
  must satisfactorily complete at least 10 of the 13 labs to pass the course**, regardless of your
  weighted average. A lab is where you find out that your algorithm was wrong.
- **Quizzes (11, Weeks 1–11)** are 15 minutes at the start of Monday's lecture. **Quiz *N* covers
  Week *N−1***, the same convention CS 101 used. They are marked and returned so that you and the
  staff can see where you stand before an exam makes it expensive.

The reason for the gate rather than a weight: **a lab you can skip for a 2% grade cost is a lab you
will skip in the week you are busiest**, which is reliably the week the material is hardest.

---

## Textbooks

**Primary:**

- **Cormen, Leiserson, Rivest & Stein — *Introduction to Algorithms*, 4th ed. (MIT Press, 2022).**
  "CLRS". **Chapters 10–25 are covered directly.** You used Chapters 1–4 in CS 101; this course is
  where the book becomes your daily reference.

**Alternative perspectives, all genuinely useful:**

- **Sedgewick & Wayne — *Algorithms*, 4th ed. (Addison-Wesley, 2011).** Excellent visualisations.
  Examples are in Java, but the book is algorithm-focused and reads fine if you are not.
- **Skiena — *The Algorithm Design Manual*, 3rd ed. (Springer, 2020).** A practising engineer's view.
  The "war stories" of real algorithm application are invaluable and are unlike anything in CLRS.
- **Dasgupta, Papadimitriou & Vazirani — *Algorithms*** (free PDF online). Concise and
  mathematically elegant. The best of the four for theory, and the shortest.

**How to use four books:** you are not expected to read all of them. Read CLRS for the definitive
treatment, and when a chapter does not click, **read the same topic in Dasgupta or Sedgewick before
concluding you do not understand it.** Different expositions fail for different readers, and a
concept that seems impenetrable in one book is often obvious in another.

---

## Languages

**Python 3 is the primary language** for most problem sets and labs — it lets you express an
algorithm without fighting the language.

**C is used where memory layout matters** — heaps as arrays (Week 3), adjacency structures (Week 4),
and anywhere the point is that pointer chasing costs you cache misses. You learned C in PROG 101,
which is a corequisite-level dependency: if you are taking PROG 101 concurrently rather than having
finished it, tell the instructor in Week 0 and the C components will be scaffolded for you.

**On using library implementations:** `heapq`, `sorted`, `dict`, and `collections.deque` are
forbidden **in the week where you are implementing that structure**, and encouraged everywhere else.
The point of Week 3 is to build a heap; the point of Week 5 is to use one to make Dijkstra fast.

---

## Grading Scale

This course uses the **university-wide 13-band scale** defined in [[UNIVERSITY POLICIES]] (Academic
Registry) — A+ 97–100, A 93–96, A− 90–92, B+ 87–89, B 83–86, B− 80–82, C+ 77–79, C 73–76, C− 70–72,
D+ 67–69, D 63–66, D− 60–62, F below 60. The registry copy governs if the two ever differ.

---

## Course Policies

- **Late policy:** 20% deduction per day; no submissions accepted after 3 days late. Projects have a
  separate, stricter policy stated on each project specification.
- **Collaboration:** discussing approaches is encouraged and is how algorithms are actually learned.
  **Writing code or proofs together is not.** The line: you may leave a conversation with an idea in
  your head; you may not leave it with text on your screen. Name your collaborators on every
  submission — this costs you nothing and its absence is what turns a discussion into misconduct.
- **Generative tools:** permitted for explaining concepts and for debugging code you wrote. Not
  permitted for producing solutions. **State any use on the submission.** The reason is narrow and
  practical: this course is graded on whether you can design an algorithm under exam conditions in
  Weeks 5, 10 and 12, and a term of outsourced problem sets produces a predictable result there.
- **Exams:** closed book, closed device. The handwritten-sheet allowance is generous — build it as
  you go rather than the night before, since making it is most of the revision.

---

## Accessibility and Support

Anything you need in order to participate — extended time, a distraction-reduced room, materials in
advance, an alternative lab arrangement — is arranged by emailing the instructor, **without requiring
you to disclose a reason.**

Office hours are posted on the course portal. **Come with a specific question and the thing you
already tried**; that turns a 40-minute session into a 5-minute one and is a skill worth practising
before you need it professionally.

---

## What You Should Be Able to Do by Week 12

1. Implement and reason about binary search trees, AVL trees, heaps, and union-find, and state the invariant each maintains.
2. Choose between adjacency matrix and adjacency list from the density of the graph and the operations required.
3. Implement BFS, DFS, Dijkstra, Bellman-Ford, Prim and Kruskal, and **say precisely which assumption each one needs**.
4. Recognise optimal substructure and overlapping subproblems, define a DP state, and write the recurrence before writing any code.
5. Decide whether a problem admits a greedy solution, and **prove it by exchange argument** when it does.
6. Explain why KMP never moves backward in the text, and derive the failure function.
7. Use the cross product to answer orientation, intersection, and hull questions.
8. State what P and NP are, give a polynomial-time reduction, and explain what a proof of P = NP would destroy.
9. Given an unfamiliar problem: identify its structure, design an algorithm, argue its correctness, implement it, and analyse its complexity — which is the whole course in one sentence.

---

*CS 102 · Course Syllabus · © CSE Department*
