# PROG 102 · Final Exam · Revision Guide
## Comprehensive — Weeks 0–12

**Sat Thursday 22 April 2027, 14:00–16:30 (finals week) · 150 minutes · 15% of the course grade**
**Closed book, closed device. Two handwritten sheets of A4.**

---

## What Is Examinable

**Everything.** Lectures 00–39, Problem Sets 0–11, Labs 0–12, and both projects.

**Weighted toward Weeks 5–12**, because Midterms 1 and 2 already assessed Weeks 0–9 and the final's job
is the whole arc. **Weeks 10, 11 and 12 have never been examined** and are systematically
under-revised.

### The Shape of the Paper

| Section | Marks | What it asks |
| --- | --- | --- |
| **A — Short answer** | 30 | 12 questions. Definitions, one-line explanations, "what does this print" |
| **B — Code reading** | 40 | What does this do; what is wrong with it; what does the compiler say |
| **C — Code writing** | 40 | Write a class, an operation, or a fix. **Drawn from Project 2's material** |
| **D — Explain a measurement** | 25 | Two tables. What they show, and what they do not |
| **E — Design judgement** | 15 | An open question with no single right answer |
| **Total** | **150** | |

**A mark a minute.** The paper is written to be finishable in about 135 minutes. If you are short of
time, you have been over-writing.

---

## Section C Comes From Project 2

**Explicitly.** If you built Project 2 properly you have written every class Section C can ask for.

Likely: a container operation with a stated guarantee; an iterator satisfying `iterator_traits`; the
Rule of Five for a resource-owning class; a thread-safe operation with a condition variable; a
`constexpr` function.

**Building Project 2 *is* the revision for Section C.** That is why the syllabus said not to treat it
as a 5% throwaway.

---

## Section D: The Measurements

**Two tables, 25 marks.** Do not memorise numbers — the table is given. **Memorise what each
demonstrates and what it does not.**

| Measurement | Shows | And does not show |
| --- | --- | --- |
| Member fn ≡ free fn assembly (W0) | A method is a function with a hidden `this` | Anything about cost |
| 100 templates ≡ 100 hand-written classes, 43,993 B (W2) | "Template bloat" is misattributed | That instantiation is free |
| vector 178× / list 128× (W3) | The complexity table omits the search | That either container is better |
| `std::sort` 2× `qsort` (W3) | Inlining beats an uninlinable call | A better algorithm |
| Virtual ≈ 2 ns, 3 attempts (W4) | Dispatch is cheap; benchmarks lie | That it is free — it blocks optimization |
| `-O2` 2.20× vs `-O3` 2.23× (W4) | Blocked vectorization is real | …and did **not** explain the gap |
| `unique_ptr` leaks nothing on throw (W5) | RAII is correctness, not tidiness | That it costs nothing (landing pads) |
| Cycle: 80 B, no destructors (W5) | Refcounting cannot collect cycles | A `shared_ptr` defect |
| Lying iterator: 8.6 → 194 ms (W6) | A dishonest category is $O(n^2\log n)$ | Anything — **it sorted correctly** |
| 500k fine, 1M segfault (W6) | Recursion depth from input data | A leak — no sanitizer sees it |
| Decorator $2^n$ vs $n$, 0.58 ns (W7) | The trade is one-sided | Much at n = 3 |
| `std::function` 296 vs 160 ms (W8) | Type erasure blocks inlining | That the lambda differs — same lambda |
| Exceptions: free in time, 240 vs 88 B (W9) | "Zero-cost" is about time | Space, or the ~1.68 µs throw |
| basic 2→4, strong 2→2 (W9) | Guarantees are testable | Anything until you sweep **every** failure point |
| `-O0` 1.1M vs `-O2` 4M/4M/3M (W10) | The optimizer shrinks the race window | That `-O2` fixed it |
| `shared_ptr` 5.9 → 17 → 57 ns (W10) | Two effects: path switch, then contention | One effect |
| lambda 0.61 / fn ptr 1.50 / `std::function` 2.18 ns (W11) | One indirection vs two | The fraction of a real program |
| SBO threshold **16 bytes** (W11) | A hidden allocation boundary | A portable number |
| **L1 1.5 ns → RAM 138 ns** (W12) | ~90×, from location alone | Which your program is in |
| **vector-random ≈ list** (W12) | It is the **access order** | That containers do not matter |
| False sharing 14.7× (W12) | Coherence works on lines, not variables | Anything about shared data — it wasn't |

**A full-mark Section D answer states what the number is evidence for, names one thing it is not
evidence for, and — where relevant — says what the denominator is.**

---

## Section E: Design Judgement

**15 marks, no single right answer.** Likely shapes:

- *"A colleague proposes X. Argue for and against."*
- *"Choose a container/pattern/mechanism for this situation and defend it."*
- *"This code works. Should it be changed?"*

**You are marked on the argument.** A well-defended position we disagree with scores full marks; an
undefended one we agree with does not.

**Practice:** PS 7 D3, PS 8 D1–D2, Lab 7 D2 and Lab 12 Part C are all this question in miniature.

---

## The Arc — What Each Week Was For

| Week | The one thing |
| --- | --- |
| **0** | A method is a function with a hidden `this` |
| **1** | The compiler writes functions for you, and its copy is sometimes wrong |
| **2** | A template is a code generator; the cost is compile time, not runtime |
| **3** | Algorithms and containers are separated by iterators |
| **4** | Polymorphism at run time costs one indirection — and blocks optimization |
| **5** | Ownership is a **type**, not a comment |
| **6** | An honest interface refuses what it cannot do efficiently |
| **7** | A pattern solves *change*; name the change |
| **8** | A pattern is a workaround for what the language cannot say |
| **9** | "Exception-safe" is four specific promises; pick one and test it |
| **10** | A passing run is not evidence |
| **11** | A ratio without a denominator is not an answer |
| **12** | It is the access order, not the container |

**If you can say each of those in a sentence and give the measurement behind it, you are ready.**

---

## Building the Two Sheets

Two sides of A4, handwritten. **Making them is most of the revision.**

**Sheet 1 — mechanisms:**

- the five special members, and when each is suppressed
- the Rule of Three / Five / Zero, and when Zero does not apply
- the five `iterator_traits` typedefs and the four categories
- vtable layout; the virtual destructor rule
- the three exception guarantees and the strong recipe
- `noexcept`: where it is load-bearing
- the smart-pointer preference order

**Sheet 2 — numbers and judgement:**

- the memory hierarchy, roughly: **L1 ~1.5 ns, RAM ~140 ns, cache line 64 B**
- `sizeof` facts: empty class 1, first virtual +8, `unique_ptr` 8, `shared_ptr` 16
- the benchmarking traps table (L38 §6)
- the two GoF principles
- the container decision procedure (L11 §8)

**Not worth the space:** exact benchmark figures (Section D gives you the table) and anything derivable.

---

## Practice Strategy

**Two weeks out:** the lecture exercises you skipped. They are the paper's source material.

**One week out:** **finish Project 2.** It is Section C.

**Three days out:** write the sheets. Then a timed 90 minutes on Weeks 10–12, which no exam has touched.

**The day before:** read the arc table above and the Course Retrospective. Stop.

---

## Practicalities

- **150 minutes**, written to be finishable in about 135.
- **Section C is marked on ideas, not syntax.** Missing `#include`s cost nothing. A missing `virtual`
  destructor, a missing `noexcept` on a swap, or an `operator[]` that returns by value cost plenty.
- **Section D: show your reasoning.** A number with no argument earns little; an argument with an
  arithmetic slip earns most of the marks.
- **Section E: commit to a position.** "It depends" with no decision earns nothing; "it depends on X,
  and here X is true, so Y" earns everything.
- Anything you need — extra time, a separate room — is arranged by emailing the instructor, **without
  giving a reason.** Do it now.

---

*PROG 102 · Week 12 · Final Exam Revision Guide · © CSE Department*
