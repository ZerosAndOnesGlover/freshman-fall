# CS 211 · Programming Languages & Compilers I
## Week 12: The Landscape of Programming Languages

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 101, CS 102, MATH 151
**Assessment for this course (overall):** Problem Sets 30%, Projects 25%, Midterms 25%, Final 20%
**This week's deliverables:** **PROJECT 2 (Friday 17:00)**, PS 11 and PS 12 (both Friday), Lab 12.

> ## The last teaching week.
>
> **Friday carries three deadlines**: Project 2 (12.5%), PS 11 and PS 12. Project 2 is worth more
> than both problem sets combined, and **the lowest problem set is dropped**. PS 12 is written to
> take an evening, and three of its four parts are direct preparation for the final's Q7.
>
> **No quiz this week** — Quiz 11 in Week 11 was the last.
>
> **Final exam: Tuesday 16 December, 09:00–11:30, VNC 100.** Comprehensive, Weeks 0–12, 20%.

---

### Why This Week Exists

Because Week 7 proved that every general-purpose language computes exactly the same functions, and so the interesting question was never expressiveness.

Twelve weeks have been finding out where the differences actually are. **A language design is a set of decisions about what to make impossible**, and every one of them buys something and costs something — costs this course has spent the term measuring.

This week collects them, adds the historical context, and asks the question the whole term has been circling: **how do you judge a language?**

---

### Learning Objectives

By the end of Week 12, you should be able to:

1. Explain why **expressiveness is not the axis**, and name the result that settles it.
2. Distinguish **memory safety** from **diagnostic safety**, with an example of each failure.
3. Read a cross-language benchmark critically, and identify **warm-up artefacts**.
4. Trace a language's **central decision** through four consequences.
5. State **Rust's ownership rules**, and say which one also eliminates data races.
6. Describe what **converged** in the multiparadigm trend, and what did not.
7. Explain what **WebAssembly** is, what it guarantees, and what it still lacks.
8. Name where compilers are going: diagnostics, incrementality, language servers, verification.
9. Identify this course's **through-lines** — fixed points, soundness, silent failure.
10. **Judge a language** by its failure mode when you are wrong.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L25 Language Design Is a Study in Constraints]] | The safety, performance and expressiveness axes **measured**; what each language made impossible; Rust; three design principles and their critics |
| [[L26 The Landscape and What Comes Next]] | The multiparadigm convergence, **WebAssembly**, where compilers are going, and what this course was |
| [[FINAL EXAM]] | **The paper.** 150 marks, Weeks 0–12 |
| [[PROJECT 2 A Compiler With Optimisation]] | **Due Friday, 12.5%.** Extends Project 1; demoed in Lab 12 |
| `assignments/PS 11 …` *(Week 11)* · [[CS211 Week12/assignments/PS 12 Synthesis\|PS 12 Synthesis]] | Both due Friday. PS 12 is short and is Q7 preparation |
| [[LAB 12 Lightning Talks]] | Project 2 demos, then five minutes on a language of your choice |
| `lab/bounds.c` · `Bounds.java` · `bounds.py` · `bounds.js` | **One question, four answers** |
| `lab/bench.c` · `Bench.java` · `bench.py` · `bench.js` | The same algorithm, four languages, two input sizes |
| [[CS211 Week12/resources/FINAL EXAM Revision Guide\|FINAL EXAM Revision Guide]] | What is on it, in what proportion, and a three-evening plan |
| [[CS211 Week12/resources/Reading Guide Week 12\|Reading Guide Week 12]] | Hoare 1980 · Gabriel 1991 · Haas et al. 2017 · Steele 1998 |
| `solutions_instructor/` | Instructor only — including the exam mark scheme |

---

### The One Thing to Take From This Week

**Ask a language what it does when you are wrong.**

```
int a[4] = {10, 20, 30, 40};   read a[7]
```

| | answer |
|---|---|
| **C** | **a number that varies between runs** — undefined behaviour, no diagnostic, program continued |
| **Java** | `ArrayIndexOutOfBoundsException: Index 7 out of bounds for length 4` |
| **Python** | `IndexError: list index out of range` |
| **JavaScript** | **`undefined`** — no error at all |

**Four different answers, and each is a decision.**

C is unsafe: the bug corrupts memory. **JavaScript is memory-safe and *diagnostically* unsafe** — nothing is corrupted, nothing is reported, and the mistake becomes a *value* that travels into your arithmetic and surfaces later as `NaN`. Java and Python are both safe, at a compare-and-branch on every access.

> **"Safe" is at least two properties, and when someone says a language is safe you should ask
> which they mean.** This course spent twelve weeks on failures that were silent — a folder that
> returned `−401`, a collector that freed a live object and printed the right answer, a compiler
> that emitted `jmp .L6`. **The languages that would have caught them are the ones that made the
> corresponding mistake impossible**, not the ones that discouraged it.

---

### Assessment Reminder

**No quiz this week.** Labs remain required; **Lab 12 is demo day and your Project 2 demo happens there.**

**Project 2 (12.5%) is due Friday 17:00** and is recorded in [[CS 211]]. **PS 11 and PS 12 are both due Friday**, and the Problem Sets component drops your lowest mark.

**The final exam is Tuesday 16 December, 09:00–11:30, VNC 100** — comprehensive, 150 marks, 20% of the course. One handwritten A4 sheet, **both sides**, permitted.

---

### Connections

**Back:** **everything.** Week 7's Church–Turing result is why expressiveness is not the axis. Week 9's undefined behaviour is why C prints `29291`. Week 11's JIT is why Java's ratio to C changes with input size. Week 6's collector and Week 8's ownership discussion are what Rust's rules replace. Week 11's target table is why WebAssembly is in this lecture at all.

**Sideways:** **CS 201 Week 12** closes its own loop the same week; the two courses met at the ISA and at the memory hierarchy.

**Forward:** **the final exam**, and then Year 3. `L26 §5` lists what to read next depending on which part of this you liked — and the honest recommendation is to finish a small language of your own, because **you already have one**.

---

*CS 211 · Week 12 · © CSE Department*
