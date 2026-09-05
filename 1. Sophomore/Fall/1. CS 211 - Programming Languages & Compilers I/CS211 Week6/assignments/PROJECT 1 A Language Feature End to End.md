# CS 211 · Project 1
## A Language Feature, End to End

---

**Assigned:** Week 6 · **Due:** Week 11, Friday 17:00
**Weight: 12.5% of the course grade** · Individual work
**Submit:** a `.zip` of your compiler plus a PDF report, `PROJ1_{LastName}_{StudentID}.pdf`

> **This is the first of two projects.** Project 2, due Week 12, is the full compiler with
> optimisation. **Design for that now** — Project 2's marks assume you are extending this rather
> than restarting, and the single most common way to lose marks in Week 12 is a Week 11 codebase
> nobody could add to.

---

## What You Are Building

**One new feature in Cyan, implemented through every phase you have written.**

Not a new compiler. The one in `CS211 Week6/lab` is yours; it lexes, parses, type-checks, lowers to TAC, builds a CFG, optimises, allocates registers, and — as of this week — runs. You are going to pick a language feature it does not have and put it through all eight phases until a program using it compiles, optimises, and executes correctly.

**Why this project.** Every week so far has handed you a phase and a bug in it. That teaches you what each phase does. It does not teach you the thing that actually makes compilers hard, which is that **a language feature is not local to any phase**. Add one, and you will find the lexer needs a token, the grammar needs a production that does not conflict, the checker needs a rule, the IR needs an opcode, `SLOTS` needs an entry, the optimiser needs to not miscompile it, and the collector needs to know whether it holds pointers. Miss one and you get a compiler that works on your test file.

---

## Choosing a Feature

Pick **one** from this list, or propose your own by **Week 7, Thursday**.

| Feature | What it adds | Where the difficulty is |
|---|---|---|
| **`for` loops** | `for (i = 0; i < n; i = i + 1) { ... }` | Desugaring vs. direct lowering; keeping the back edge findable by `loops.py` |
| **`break` / `continue`** | early exit from a loop | The CFG. Both create edges the structured lowering did not expect |
| **Nested blocks** | `{ let x = 1; ... }` as a statement | Scoping (Week 3), and shadowing rules you must *choose* and defend |
| **`null` and option types** | a pointer that may be absent | The type rule that stops you dereferencing it, and what the collector does with it |
| **Dynamic arrays** | `push`, `len`, growth | Reallocation, and the fact that a growing object *moves* |
| **First-class functions** | calling a value, not a name | Closures capture variables — and captured variables live on the **heap**, not the stack |
| **`switch` / pattern match** | multi-way branch | Lowering to a jump table, and exhaustiveness checking |
| **Strings as objects** | concatenation, indexing | The first heap object with variable size, and interning |

**Closures and dynamic arrays are the hardest two on that list. Both are excellent choices and both have been underestimated by every student who picked them.** If you want one, start in Week 7, not Week 10.

**A feature not on the list is welcome** — send a paragraph in Week 7 saying what it is, which phases it touches, and what you expect the hard part to be. Approval is normally same-day. Proposals are refused only when the feature is local to one phase, because then the project has no spine.

---

## Required Functionality

### 1. It works through all eight phases

For your feature, all of the following must hold, and your report must show each:

1. **Lexer** — any new tokens, with a test that shows them.
2. **Parser** — a grammar that is **unambiguous**. If you added a production, say what conflict it could have caused and show it does not. `first_follow.py` from Week 2 is still in the tree.
3. **Type checker** — a rule, and **an error message that names the line and column**. A feature with no way to be used wrongly has not been type-checked.
4. **TAC** — lowering, and a `SLOTS` entry for any new opcode. `check_coverage` must pass.
5. **CFG** — `build_cfg` must produce the right blocks and edges. Show the CFG for a program using your feature.
6. **Optimiser** — your feature must survive `opt.py` and `live.py`'s DCE unchanged in meaning. **Show a before/after dump.**
7. **Register allocation** — `regalloc.py` must run on it without spilling a live value.
8. **Runtime** — it must **execute** and produce the right answer under **all four collectors**, `none`, `rc`, `mark`, `gen`.

### 2. It does not break anything else

Every `.cy` file in Weeks 3–6 must still compile and produce the same output it did before. **Ship the script that checks this.** A regression suite you ran once by hand is worth no marks; one that runs in a loop and prints pass/fail is worth several.

### 3. It has tests that fail before and pass after

At least **eight** test programs using your feature: at least three that must be *rejected* by the type checker, with the expected message, and at least five that run and produce a known answer.

### 4. If it allocates, the collector must handle it

If your feature can create a heap object — closures, strings, dynamic arrays, option types all can — then:

- Its `SLOTS` entry must be right, and **you must argue why**, not merely assert it.
- `--roots=live` and `--roots=scope` must both give the correct answer.
- **You must show a program using your feature under `--gc=mark` with a small `--threshold`**, and demonstrate that nothing reachable is freed.

**This is where the marks are lost.** L14 §3's crash is what a wrong `SLOTS` entry looks like, and it will not appear until a collection happens to land in the wrong place.

---

## Verification — 20% of the project mark

Working is not the same as demonstrated to work.

- **Regression script** (8) — runs every prior week's `.cy` files and reports pass/fail, non-interactively, in one command.
- **Feature tests** (7) — the eight above, automated, with expected outputs checked rather than eyeballed.
- **Collector safety** (5) — at least one test that runs your feature at a threshold low enough to force many collections, and asserts the answer.

**Differential testing is the strongest technique available to you and it is worth using.** Run the same program under `--gc=none` and `--gc=mark` and compare the answers. A disagreement is a collector bug, found automatically, without you having to guess where to look.

---

## Report — 25% of the project mark

**Six to ten pages.** Not a narrative of what you did each week.

1. **The feature, and its semantics** (1–2 pp). What does it mean? Give the rules precisely enough that someone could implement it from your description. Where you had a choice — shadowing, evaluation order, what `break` does inside a nested loop — **say what you chose and why**.
2. **Phase by phase** (2–3 pp). What changed in each of the eight, with the diff summarised. **Which phase surprised you?** There is always one.
3. **The grammar argument** (1 p). Show your production does not introduce ambiguity, or show how you resolved it.
4. **Evidence** (1–2 pp). Dumps: tokens, AST, TAC, CFG, optimised TAC, register assignment, and a run. One program, all the way through.
5. **The collector** (1 p, required if your feature allocates). Your `SLOTS` entry and the argument for it. The low-threshold test and its result.
6. **What is still wrong** (1 p). Every compiler has a list. **A precise account of a limitation you understand scores better than a claim of completeness that the marker disproves in two minutes**, and this is not a rhetorical flourish — it has decided grades in both directions every year this course has run.

---

## Marking

| Component | Marks |
|---|---|
| Feature works through all eight phases | 30 |
| No regressions, demonstrated | 10 |
| Correct under all four collectors | 10 |
| Verification (above) | 20 |
| Report (above) | 25 |
| Code quality — readable, commented where it is surprising, no dead code | 5 |
| **Total** | **100** |

### Bonus, up to +10 (capped at 100)

- **+4** — your feature is optimised, not merely supported: constant-fold it, or hoist it, or eliminate it when dead, and show the instruction count.
- **+3** — a fuzzer that generates random programs using your feature and checks `--gc=none` against `--gc=mark`.
- **+3** — implement the feature in a *second* way and measure the difference honestly. Desugaring versus direct lowering is the obvious pair.

---

## Milestones

These are not marked. They exist because the failure mode of this project is a working parser in Week 10 and nothing else.

| By the end of | You should have |
|---|---|
| **Week 7** | Feature chosen. A one-page semantics. Three test programs written that *do not compile yet*. |
| **Week 8** | Lexer and parser done. AST dumps correct. The grammar argument written. |
| **Week 9** | Type checker done, including all three rejection tests with their messages. |
| **Week 10** | TAC, CFG, `SLOTS` entry, and it **runs** under `--gc=none`. |
| **Week 11** | Optimiser and all four collectors. Regression suite green. Report written. |

**If you are not running under `--gc=none` by the end of Week 10, ask for help that week.** Not in Week 11.

---

## Practical Advice

**Write the test programs first.** Before you touch the lexer, write the five programs that should work and the three that should be rejected. You will discover an ambiguity in your own design, on paper, in twenty minutes, and it costs nothing.

**Add the `SLOTS` entry when you add the opcode, not later.** `check_coverage` will remind you, and it is the only thing in the tree that will. Weeks 5 and 6 both opened with what happens when that table is wrong.

**Do not start by refactoring.** The compiler in `Week6/lab` is not beautiful. It is nine files you understand, and Week 11 is not the time to find out which of your improvements broke `phi` handling.

**Dump early and dump often.** Every phase prints its representation for a reason. When a program gives a wrong answer, the fastest route is always the first dump that looks wrong — and, as L11 §2 showed, that method is only as good as the dump. If your feature prints ambiguously, fix the printer first.

**Keep a lab notebook of what you tried.** The report asks what surprised you and what is still wrong. Those are much easier to write in Week 11 if you wrote them down in Week 8.

---

*CS 211 · Week 6 · Project 1 · © CSE Department*
