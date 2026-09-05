# CS 211 · Problem Set 12 — Solutions and Mark Scheme
## Instructor Only

**Do not distribute.** Measured on the reference machine (gcc 13.3.0 -O2, OpenJDK 25.0.3, node v22.22.1, CPython 3.14.2, x86-64).

> **Mark generously on argument and strictly on evidence.** PS 12 is due the same Friday as
> Project 2 and PS 11, the lowest problem set is dropped, and its real purpose is Q7 preparation.
> **A short, well-evidenced answer is the target**; length is not.

---

## Part A — Measure the Trade-offs Yourself (30)

**A1.** *(10 — 3 the four answers, 4 the ranking, 3 the costs)*

| | `a[7]` |
|---|---|
| C | **a number that differs between runs** (29291, 30915, …), no diagnostic, program continued |
| Java | `ArrayIndexOutOfBoundsException: Index 7 out of bounds for length 4` |
| Python | `IndexError: list index out of range` |
| JavaScript | `undefined`, no error |

**The ranking is the marked part, and JavaScript is genuinely contestable.**

- **Java/Python safest** — loud, immediate, at the point of the mistake.
- **C least safe on memory** — reads another object's storage; undefined behaviour.
- **JavaScript is the argument.** Memory-safe (nothing corrupted) but **diagnostically unsafe**: the mistake becomes a *value* and propagates, surfacing much later as `NaN` or a wrong result.

***Every student's C value will differ*** — it is whatever is on the stack. A student who notices that, and says it is the point rather than a problem, has understood undefined behaviour better than one who reproduces 29291.

**Accept JS placed second or third with a real argument.** Reject an unargued ordering. The best answers distinguish *memory* safety from *diagnostic* safety explicitly.

Costs: C pays nothing at run time and pays in escaped bugs; Java/Python pay a compare-and-branch per access; JS pays nothing at run time and pays the most in debugging time.

**A2.** *(10 — 4 timings, 4 the Java explanation, 2 the requirement)*

| | fib(30) | ratio | fib(32) | ratio |
|---|---|---|---|---|
| C | 0.004 | 1× | 0.028 | 1× |
| Java | 0.025 | 6.3× | 0.037 | **1.3×** |
| JS | 0.037 | 9.3× | 0.075 | 2.7× |
| Python | 0.353 | 88× | 0.551 | 20× |

**Java's ratio changes because the JIT warms up** — at `fib(30)` most of the measurement is interpretation plus C2 compiling; at `fib(32)` the compiled code dominates.

**The two earlier weeks:** **Week 11 §L24.4** (a JIT pays in startup and buys information) and **Week 9 §7** (`Hoist.java` terminated interpreted and hung once C2 compiled the loop).

**What to require of an "N times slower" claim:** the workload, the input size, the runtime version, and whether warm-up was excluded. *(Accept "and whether it is a library call in disguise".)*

*Student timings will differ; the **direction and the crossing** must reproduce. Do not mark on absolute figures.*

**A3.** *(10 — 3 the table, 4 the two objections, 3 the proposal)*

18 / 10 / 6 / 5 lines against 0.028 / 0.037 / 0.075 / 0.551 s.

**Confound:** C's count is inflated by `#include`s and explicit timing code that Python gets in one import — a fairer count narrows the gap considerably. *(Accept: line count is not a measure of anything; a one-liner can be unreadable.)*

**Not simple causation:** Python is not slow *because* it is short. **It is short and slow for the same reason** — values carry their types at run time, so the programmer does not write them and the interpreter must check them. One decision, two consequences.

Better measures: tokens rather than lines; a larger, realistic program; time-to-first-correct-solution across programmers (expensive, and the only one that measures what "expressive" is supposed to mean). **Full marks require naming what the proposal would cost to run.**

---

## Part B — One Decision, Many Consequences (25)

**B1.** *(10)* Any language, four consequences, at least two measured in this course. Award 2 per consequence, 2 for the decision being genuinely *central* rather than incidental.

*Strong answers for Python: dynamic typing → no annotations to write → 20× slower → the GIL is tractable because the interpreter is already the bottleneck → Week 9's racy counter got the right answer by accident.*

**B2.** *(8 — 2 rules, 4 the double duty, 2 costs)*

One owner; a borrow must not outlive its referent; **many shared borrows or one mutable borrow, never both**.

**The third does double duty.** A data race requires two threads touching one location with at least one writing — and "one mutable borrow, or many shared" is exactly a prohibition on that. **The rule that eliminates use-after-free eliminates data races too**, which is what "fearless concurrency" means.

Costs (need one non-performance): rejects correct programs (sound and incomplete — a doubly-linked list); `Rc<RefCell<T>>` cycles still leak, as Week 6 §8 requires; **the cost moved to the programmer**, as design time and a learning cliff.

**B3.** *(7 — 3 why a language mistake, 2 the replacement, 2 the Week 8 link)*

It is a **language** mistake because null inhabits *every* reference type: there is no way to say "this cannot be absent", so the type system cannot help and every dereference is a potential fault.

Replacement: **`Option`/`Maybe`** — absence is a *separate constructor of a distinct type*, so the compiler forces a case analysis before use.

**The Week 8 link:** inference alone does not do this. `zero`, `false` and `nil` all inferred to `∀a b. a → b → b` — **a principal type is computed from the term and adds nothing the term did not contain.** What separates them is a **nominal declaration**, which is exactly what `data Option a = None | Some a` is.

*That last point is the discriminating one and the reason this question exists.*

---

## Part C — The Through-Lines (25)

**C1.** *(10 — 5 for five instances, 3 structure, 2 the greatest fixed point)*

Any five of: ε-closure (W1); FIRST/FOLLOW (W2); constant folding to a fixed point (W4); liveness (W5); dominators (W5); mark-phase worklist (W6); unification/inference (W8).

**Shared structure:** iterate a monotone transfer function over a finite lattice until nothing changes; termination is guaranteed because the sets only grow (or only shrink) and the domain is finite.

**Dominance converges to the greatest fixed point** — it is a *must* analysis merging with intersection, so it starts full and shrinks.

**C2.** *(8 — 4 instances, 2 what is rejected/retained, 2 the reason)*

Four of: liveness's *may* over-approximation (W5); reference counting, which cannot see cycles (W6); Hindley-Milner, which rejects `(λi. i i) (λx. x)` (W8); the C standard declining to define races (W9); Rust's borrow checker (W12).

**The single reason: exactness is undecidable** — Week 7 §13, the halting problem in different notation. Every analysis must approximate, and always in the direction that cannot cause a wrong answer.

**C3.** *(7 — 4 three mechanisms, 3 two instruments)*

Mechanisms as in the final's Q7(b) scheme.

**Instruments that agreed with a bug** (two): Week 5's printer, which rendered `store` as though it defined its destination; Week 6's peak RSS, pinned by the collection threshold and blind to retention; Week 7's `0 == False`, passing every boolean test; Week 11's phase timer, measuring `fork` and reporting code generation; Week 9's cache-line layout, changing a rate 100×.

---

## Part D — Judgement (20)

**D1.** *(10)* Six questions, six specific answers, about a language not in L25 §5. **Deduct for "safe" and "fast" used as answers** — the question says so.

**D2.** *(10 — 6 the three decisions with who pays, 4 the disliked one)*

Any domain, three decisions, and **"who pays" must be assigned** for each: machine (run-time cost), programmer (design time, rejected programs), or user (latency, crashes).

**The last bullet is the marked one.** A student who names a decision they dislike and explains why the domain requires it anyway is demonstrating exactly the judgement the course was for. *(Good answers: "no GC on the 32 KB controller, even though I would rather have one"; "dynamic typing in the notebook, even though I prefer static"; "no floating point in the ledger".)*

---

## Overall

**Expected distribution:** high, and that is by design — this is an evening's work in the last week of term, deliberately weighted toward the arguments the final will ask for.

**Two failure modes:**

1. **Quoted lecture numbers instead of measured ones.** The brief says run them. Ratios that match the reference table to three significant figures on different hardware did not come from a machine.
2. **Part C answered as a list.** Naming five fixed points is 5 of 10; the structure and the greatest-fixed-point question are the other 5.

---

*CS 211 · Week 12 · PS 12 Solutions · © CSE Department*
