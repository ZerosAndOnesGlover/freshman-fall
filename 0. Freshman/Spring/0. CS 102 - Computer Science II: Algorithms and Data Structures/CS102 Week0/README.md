# CS 102 · Computer Science II — Algorithms and Data Structures
## Week 0: Review and Course Overview

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, MATH 151
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverable:** Lab 0. **No problem set and no quiz** — Quiz 1, in Week 1, covers this week.

---

### Why This Week Exists

To make the change of gear explicit before it catches anyone by surprise.

CS 101 handed you algorithms and asked you to implement them. **CS 102 hands you problems and asks
you to produce algorithms** — and then to prove they work. That is a different activity, and students
who have not been told so tend to conclude around Week 4 that they have got worse at programming.
They have not. They have started doing something harder.

This week re-establishes the three tools the rest of the course assumes: the **design process**,
**asymptotic analysis** sharpened past where CS 101 left it, and **correctness proofs** — loop
invariants and induction — which is the genuinely new skill.

### Learning Objectives

By the end of Week 0, you should be able to:

1. State the six steps of the algorithm design process and say what each one catches.
2. Explain why identifying a problem's *structure* matters more than coding skill, using the $k$-largest example.
3. Distinguish $O$, $\Omega$ and $\Theta$, and say why "merge sort is $O(n^2)$" is true and useless.
4. Distinguish worst, average and amortised case, and explain why amortised is **not** a probabilistic claim.
5. Solve a recurrence with the master theorem — **and recognise when it does not apply**.
6. State and prove a loop invariant in three parts, including termination.
7. Prove a recursive algorithm correct by strong induction, and say why ordinary induction is insufficient for divide-and-conquer.
8. Explain from measured data why $\Theta(n^2)$ and $\Theta(n\log n)$ diverge, and what asymptotic analysis hides.

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L01 The Algorithm Design Process.md` | The six steps, why order matters, the roadmap, and what "efficient" means |
| `lectures/L02 Complexity Analysis Reviewed.md` | $O/\Omega/\Theta$, the three cases, loops, recurrences, space, and what the model hides |
| `lectures/L03 Correctness Loop Invariants and Induction.md` | Why testing is not proof; worked invariants; induction; five exercises |
| `lab/LAB 0 Sorting Benchmarks.md` | Implement three sorts, verify them, measure the gap yourself |
| `resources/Course Overview Syllabus.md` | **Read this in full in Week 0** — assessment, policies, the lab gate |
| `resources/Reading Guide Week 0.md` | CLRS 1–4 with guiding questions, plus a script to check Lecture 01's numbers |
| `solutions_instructor/LAB 0 Solutions.md` | Instructor only |

### The One Thing to Take From This Week

**A proof is not decoration.** It is the only thing that distinguishes *"I could not find a case where
it fails"* from *"it does not fail."*

From Week 7 you will design algorithms nobody has handed you, with no reference implementation to
compare against. The proof is what will stand between you and a plausible algorithm that is wrong.
Lecture 03's exercises are the beginning of that skill and are worth more than their length suggests.

### Assessment Reminder

Labs and quizzes carry **no direct weight** — the curriculum's assessment line sums to 100% without
them. They are still required: **at least 10 of 13 labs must be completed satisfactorily to pass the
course**, and **Quiz *N* covers Week *N−1***. The reasoning is in the syllabus, and it is short: a lab
you can skip for a 2% grade cost is a lab you will skip in the week you are busiest, which is
reliably the week the material is hardest.

### Connections

**Back:** CS 101 supplies the sorts, the searches, and the Big-O basics. **MATH 151 is a hard
prerequisite** — induction, recurrences, summations and graph terminology are used from here on
without re-teaching.

**Forward:** Lecture 03's invariants are used in every single week that follows. Lecture 02's
amortised analysis is what makes union-find work in Week 6. The complexity table in Lecture 01 §4 is
the setup for Week 12's question about what happens when no polynomial algorithm exists at all.

---

*CS 102 · Week 0 · © CSE Department*
