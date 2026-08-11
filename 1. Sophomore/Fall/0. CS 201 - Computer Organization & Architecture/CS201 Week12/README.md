# CS 201 · Computer Organization & Architecture
## Week 12: Architecture Frontiers and Synthesis

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** **PROJECT 2 due Friday (10%)**, PS 12 (due Friday), Lab 12 *(demo day, this week's lab)*. **No quiz — Quiz 11 in Week 11 was the last.**

> **This is the last teaching week.** The final exam (Weeks 0–12, comprehensive, 20%) follows in finals
> week — see `resources/FINAL EXAM Revision Guide.md`. Project 2 is demoed in Lab 12 and submitted Friday.

---

### Why This Week Exists

Because a course that spent twelve weeks descending into one machine should end by climbing back out — seeing where that machine is going, and seeing the whole of it at once.

**L37 is the frontier:** RISC-V, TPUs, FPGAs, quantum and neuromorphic chips — all answers to the question Week 0 opened with. The general-purpose free lunch ended in 2005, and the field's response was to build a hundred *specialised* machines, each spending its transistors on one workload. **You can now read why each exists, because you understand the general machine it specialises away from.**

**L38 is the synthesis:** one ordinary function containing every week of the course, the abstraction hierarchy revealed as the syllabus, and the latency ladder as the single artefact worth keeping. **L39 is the road ahead** — where this holds up the rest of the degree, and the two things (the speed of light, the cost of data movement) that will outlast every hardware generation you will work through.

---

### Learning Objectives

By the end of Week 12, you should be able to:

1. Contrast RISC-V with CISC using a real compiled example, and explain why more instructions can be the better trade.
2. Explain why RISC-V being *open* is an architectural advantage.
3. Place CPU, GPU, TPU, FPGA and ASIC on the generality-vs-efficiency axis.
4. Explain what a TPU discards from a general core and why it can.
5. Describe quantum and neuromorphic computing as different *models*, and their honest uncertainty.
6. **Trace the whole course through a single ordinary program.**
7. State the latency ladder's ratios and why they outlast the numbers.
8. Name the ideas that recurred across the course and where each appeared.
9. Explain why the course's ordering was necessary (security and frontiers needed the whole machine).

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L37 Architecture Frontiers.md` | RISC-V, TPUs, FPGAs, quantum, neuromorphic — the generality-efficiency axis |
| `lectures/L38 The Whole Machine — Synthesis.md` | One function, every week; the layers; the latency ladder; the recurring ideas |
| `lectures/L39 The Road Ahead.md` | Where CS 201 holds up the degree, and what to keep |
| `assignments/PROJECT 2 Pipelined CPU Simulator with a Cache.md` | **10%, due Friday.** The capstone — extend Project 1 with a pipeline and cache |
| `assignments/PS 12 Synthesis.md` | RISC-V, domain-specific chips, and the whole machine in one program |
| `lab/LAB 12 Demo Day.md` | Demo Project 2, watch others, look back |
| `resources/FINAL EXAM Revision Guide.md` | Weeks 0–12, the two pages, the plan |
| `resources/CS 201 Reference Sheet.md` | The whole course on one page — the artefact to keep |
| `resources/Course Retrospective.md` | **Read after the final, not before** |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**You understand the specialised machines because you understand the general one.**

A TPU discards the caches (Week 4) and branch predictors (Week 5) a CPU spends heavily on — and you can say *why it can*: neural-network computation is regular, branchless matrix multiplies, so those features buy nothing and the transistors go to arithmetic instead. **That sentence was impossible in Week 1 and is obvious now**, and it is the whole point of ending here.

The frontier moves along one axis — **generality against efficiency** — and every machine on it, from the CPU to the ASIC, is Week 0's lesson at the level of silicon: **every transistor spent on flexibility is a transistor not spent on the workload.** "The architecture reflects the workload" is the whole story, and you have the vocabulary to read the next chapter of it.

---

### Assessment Reminder

**No quiz this week** — Quiz 11 (Week 11) was the last. **Labs remain required**; Lab 12 is demo day, and your Project 2 demo is graded there.

**Project 2 (10%) is due Friday** and demoed in Lab 12 — the cycle-accurate pipelined CPU simulator with a cache, extending Project 1. **PS 12 (synthesis) is also due Friday** and is deliberately short.

**The final exam is comprehensive (Weeks 0–12, 20%, 150 minutes, two handwritten pages).** The revision guide and the one-page reference sheet in `resources/` are your two most useful documents. **Read the Course Retrospective only after the exam** — it is not revision.

---

### Connections

**Back:** **all of it.** L38 traces every week through one function; L37's specialised machines each specialise away from something you learned (the TPU from Weeks 4–5, the FPGA from ECE 110's gates, RISC-V from Week 2's decode). **Week 0's abstraction-cost thesis is L37's generality-efficiency axis.**

**Forward:** **the whole degree.** PROG 201 assumed this course all semester; CS 202 implements it next; ECE 311, CS 341, CS 302, CS 321, CS 331 and MATH 341 each build on a specific week. **CS 201 is the foundation those courses were waiting for** — L39 lays this out.

---

*CS 201 · Week 12 · © CSE Department*
