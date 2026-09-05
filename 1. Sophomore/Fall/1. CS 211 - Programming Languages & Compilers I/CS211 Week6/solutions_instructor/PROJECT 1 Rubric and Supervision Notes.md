# CS 211 · Project 1 — Rubric and Supervision Notes
## Instructor Only

**Do not distribute.** Assigned Week 6, due Week 11 Friday 17:00. 12.5% of the course grade.

---

## What This Project Is Actually Testing

Not "can they write a compiler" — they have one. **It tests whether they understand that a language feature is not local to a phase.**

Every week of this course has handed out a phase and a bug in it. That produces students who can explain what a parser does and who have never once had to make eight things agree. The characteristic Project 1 failure is a beautiful parser, a plausible type rule, and a `SLOTS` table that was never updated — which does not fail until a collection lands in the wrong place, which is Week 6's entire lesson arriving as a grade.

---

## Feature Difficulty Calibration

Use this when approving proposals in Week 7.

| Feature | Difficulty | The part they will underestimate |
|---|---|---|
| `for` loops | **Low** | Almost none. Warn that a pure desugar makes for a thin report — require the +4 bonus or a second feature. |
| Nested blocks | **Low–medium** | Shadowing. They must *choose* a rule; most have never considered that it is a choice. |
| `break` / `continue` | **Medium** | The CFG. `build_cfg` links fall-through edges, and an early exit creates an edge to a block that is not the next one. `loops.py` may stop finding the natural loop. |
| `switch` / match | **Medium** | Exhaustiveness. Also that a jump table is a data structure the back end has never emitted. |
| Strings as objects | **Medium–high** | The first *variable-sized* heap object. `Obj.words` becomes dynamic and every size calculation in `heap.py` must follow. |
| `null` / option types | **Medium–high** | The type rule is easy; the *flow-sensitivity* is not. `if (x != null) { x.f }` requires narrowing, which the Week 3 checker cannot express. **Approve only if they scope it to explicit unwrapping.** |
| Dynamic arrays | **High** | The object **moves** on growth. Every existing `Ref` to it must be found — which is either a copying collector or an indirection they have to design. |
| First-class functions | **High** | Captured variables must be **heap-allocated**, so the feature creates a new kind of heap object *and* changes where existing locals live. Escape analysis is the correct solution and is out of scope; a uniform boxing rule is the acceptable one. |

**Refuse:** anything expressible entirely in the parser (new operators that desugar to existing ones, new literal syntaxes, comments). The project has no spine without a cross-phase obligation. Suggest they pair it with something from the table.

**Approve enthusiastically:** anything that allocates. Section 4 of the brief exists for those, and they are the ones where Week 6 pays off.

---

## Marking

| Component | Marks | What full marks look like |
|---|---|---|
| Feature through all eight phases | 30 | Every phase shown working, with a dump. A missing `SLOTS` entry caps this at 20 regardless of how well the rest works. |
| No regressions, demonstrated | 10 | A script, run in front of the marker, non-interactive. "I checked by hand" is 3. |
| Correct under all four collectors | 10 | All four, same answer. `--gc=none` only is 2. |
| Verification | 20 | See below. |
| Report | 25 | See below. |
| Code quality | 5 | Readable diffs, comments where surprising, no commented-out experiments left in. |

### Verification (20)

- **Regression script (8).** One command, exit code meaningful, prints pass/fail per file. Deduct 3 if it needs a human to read the output to know whether it passed.
- **Feature tests (7).** Eight programs, ≥3 rejection tests with expected messages. **Deduct heavily if the rejection tests only check that compilation failed** rather than that it failed with the right message at the right line — a type checker that rejects everything passes that test.
- **Collector safety (5).** A low-threshold run with an asserted answer. **Differential testing (`--gc=none` vs `--gc=mark`) is the model answer** and should be pointed out to anyone who has not found it.

### Report (25)

| | Marks |
|---|---|
| Semantics, precise enough to reimplement from | 5 |
| Phase-by-phase, with the surprise named | 5 |
| Grammar argument | 3 |
| Evidence — one program, all the way through | 5 |
| Collector section (if it allocates; otherwise redistribute) | 3 |
| What is still wrong | 4 |

**"What is still wrong" is worth 4 and is the most reliable discriminator in the whole project.** A student who writes "my `break` does not work inside a `switch` inside a loop, because the lowering uses a single exit label per loop and the inner construct overwrites it" has understood their own compiler. A student who writes "everything works" has told you they did not test it, and the marker should spend five minutes proving it — which historically takes two.

---

## Milestone Supervision

The milestones in the brief are not marked, and they are the difference between a distribution centred at 70 and one centred at 55. **Check them in the Week 8, 9 and 10 lab sessions**, verbally, five minutes per student.

| Week | The question to ask | The bad answer |
|---|---|---|
| 7 | "What are your three rejection tests?" | "I'm still deciding on the feature." |
| 8 | "Show me an AST dump." | "The parser is nearly done." |
| 9 | "What line and column does your error message name?" | "It raises an exception." |
| 10 | "Run it under `--gc=none`." | Anything other than running it. |

**The Week 10 checkpoint is the one that matters.** A student not executing by the end of Week 10 will not finish, and the intervention that works is to make them cut the feature down — a `for` loop that does not support `continue` and runs is worth far more than a closure implementation that parses.

---

## Relationship to Project 2

Project 2 (Week 12, full compiler with optimisation) assumes this codebase. **State in the Week 11 feedback whether their code is extensible**, because that is the single strongest predictor of the Project 2 mark and it is actionable in Week 11 and not in Week 12.

The specific failure to flag: a feature implemented by special-casing it in every phase rather than by extending the representations. It works, it marks well here, and it makes Project 2 miserable.

---

## Academic Integrity

The compilers literature is full of implementations of everything on the feature list, and LLM assistance will produce a plausible `for` loop in seconds.

**This is why the report asks which phase surprised them, and why the milestones are verbal.** A student who cannot say what went wrong in Week 9 did not write it in Week 9. Neither observation is proof on its own; both are grounds for the standard conversation, and both are far more reliable than reading the code for style discontinuities.

**The evidence section is also load-bearing here** — one program, dumped at every phase, is tedious to fabricate and trivial to produce if you built the thing.

---

*CS 211 · Week 6 · Project 1 Rubric · © CSE Department*
