# CS 211 · Problem Set 12
## Synthesis: Language Design Trade-offs

---

**Released:** Week 12, Wednesday · **Due:** Week 12, Friday 17:00 *(last teaching week)*
**100 points · counts toward the Problem Sets component (30% of the final grade)**

**Submit:** `ps12.md` only. **No code is required.**

> **This is deliberately short.** Project 2 and PS 11 are due the same day, the final exam is ten
> days later, and the Problem Sets component **drops your lowest mark**. PS 12 is written to be
> completed in an evening — and to be worth doing, because **three of its four parts are direct
> preparation for the final's Q7**, which is 30 of 150 marks.

---

## Part A — Measure the Trade-offs Yourself (30 points)

The programs are in `CS211 Week12/lab`. Run them; do not take the lecture's numbers.

**A1.** *(10)* Run all four `bounds` programs and report what each does with `a[7]`.

- Give the four answers.
- **Rank them from safest to least safe**, and defend the ranking. *(There is a real argument about where JavaScript belongs, and either position scores full marks if argued.)*
- For **each**, name what the behaviour costs: at run time, at compile time, or in bugs that escape.

**A2.** *(10)* Run the four `bench` programs at `fib(30)` and `fib(32)` and report the eight timings.

- Compute each language's ratio to C at both sizes.
- **Java's ratio changes substantially. Explain why**, and name the two earlier weeks where you saw the same effect.
- In two sentences: what would you require of anyone who told you "language X is N times slower than C"?

**A3.** *(10)* Count the non-blank source lines of the four `bench` programs.

- Report them against the `fib(32)` timings.
- The ordering looks inverse. **Give one reason the measurement is confounded**, and one reason the apparent relationship is not simple causation.
- Propose a *better* measurement of expressiveness than line count, and say what it would cost to run.

---

## Part B — One Decision, Many Consequences (25 points)

**B1.** *(10)* Pick **one** language from L25 §5 and trace its central decision through **four** consequences, at least two of which this course measured.

*(Example shape, which you may not reuse: C chose to trust the programmer → no bounds check → `a[7]` is undefined → the optimiser may delete a racy loop → memory-safety CVEs dominate the NVD.)*

**B2.** *(8)* Rust claims the safety/performance trade was false.

- State the three ownership rules.
- **One rule does double duty.** Name it, and say what it eliminates besides use-after-free — and why that follows.
- Name **two** costs, at least one of which is not about performance.

**B3.** *(7)* Hoare called null his "billion-dollar mistake".

- State what makes it a *language design* mistake rather than a library one.
- Name the modern replacement and the property that makes it work.
- **Week 8 measured something relevant here.** Say what, and why an inferred type alone would not have been enough.

---

## Part C — The Through-Lines (25 points)

**C1.** *(10)* **Fixed-point iteration appears at least six times** in this course.

- Name **five**, with the week and what was being computed.
- State the shared structure: what is iterated, what the termination condition is, and what guarantees termination.
- One of them converges to a *greatest* fixed point rather than a least. Which, and why?

**C2.** *(8)* **Sound and incomplete** appears at least five times.

- Name **four**, with the week.
- For each, say what is *rejected or retained* that need not have been.
- State the single reason all of them must approximate. It is one sentence and it is from Week 7.

**C3.** *(7)* **Silent failure** appears every week.

- Choose **three** and give the *mechanism of invisibility* for each — what was seen and what was not.
- Name **two instruments that agreed with a bug**, and say what each was really measuring.

---

## Part D — Judgement (20 points)

**D1.** *(10)* Choose a language you have used that is **not** covered in L25 §5 — Go, Kotlin, Swift, Zig, Haskell, Erlang, TypeScript, Julia, anything.

Answer L25 §8's six questions for it. Be specific: "safe" and "fast" are not answers.

**D2.** *(10)* You are designing a language for **one** of: an embedded controller with 32 KB of RAM; a data-analysis notebook; a browser-based game engine; a payments ledger.

- Pick one and name your **three** central decisions.
- For each, say what it makes impossible and **who pays**.
- Name **one** decision you would make that you personally dislike, and explain why the domain requires it.

---

## Reference Numbers

Measured on the machine these notes were prepared on (gcc 13.3.0, OpenJDK 25.0.3, node v22, CPython 3.14.2).

| | `a[7]` | `fib(30)` | `fib(32)` | lines |
|---|---|---|---|---|
| **C** | *a varying number*, no diagnostic | 0.004 s | 0.028 s | 18 |
| **Java** | `ArrayIndexOutOfBoundsException` | 0.025 s | 0.037 s | 10 |
| **JavaScript** | `undefined`, no error | 0.037 s | 0.075 s | 6 |
| **Python** | `IndexError` | 0.353 s | 0.551 s | 5 |

Ratio to C: **6.3× / 9.3× / 88×** at `fib(30)`; **1.3× / 2.7× / 20×** at `fib(32)`.

---

## A Note on What This Is For

**Parts B, C and D are the final's Q7 in a different order**, and that is deliberate rather than lazy. Q7 is 30 marks, it is the part students run out of time for, and it is the only part of the paper you can genuinely prepare in advance.

**Write these answers as though they were exam answers** — three sentences with a figure, not three pages — and you will have done the revision and the problem set at once.

**As every week: a careful answer that disagrees with the lectures scores full marks. A confident answer with no evidence scores very little.**

---

*CS 211 · Week 12 · Problem Set 12 · © CSE Department*
