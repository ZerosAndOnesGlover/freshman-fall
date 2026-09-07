═════════════════════════════════════════════════════════════
# YEAR 2 PREREQUISITE AUDIT
### Sophomore · Fall + Spring · All Ten Courses
═════════════════════════════════════════════════════════════


> ✅ **Headline: zero prerequisite findings in the material that exists.**
> The blocker is not sequencing — it is that **eight of Year 2's ten courses have not
> been built**, and a ninth is built only to Week 4.

**Audited:** 2026-08-16 · **Method:** §11 of the Year 1 audit, applied from the outset —
*grep the lecture body, not the topic index, before recording a gap.*

---

## 1 · Build State — What Could Be Audited

| Semester | Course | Weeks | Lectures | Assessments | Auditable |
|---|---|---|---|---|---|
| Fall | **CS 201** Computer Organization & Architecture | 13 | 39 | 28 | ✅ **fully** |
| Fall | **CS 211** Programming Languages & Compilers I | 5 of 13 | 10 | 10 | ⚠️ **W0–W4 only** |
| Fall | PROG 201 Systems Programming in C | 0 | 0 | 0 | ❌ empty |
| Fall | MATH 241 Linear Algebra | 0 | 0 | 0 | ❌ empty |
| Spring | CS 202 Operating Systems | 0 | 0 | 0 | ❌ empty |
| Spring | CS 212 Software Engineering | 0 | 0 | 0 | ❌ empty |
| Spring | PROG 202 Functional & Logic Programming | 0 | 0 | 0 | ❌ empty |
| Spring | MATH 251 Probability & Statistics for CS | 0 | 0 | 0 | ❌ empty |
| Spring | ECE 211 Signals and Systems | 0 | 0 | 0 | ❌ empty |
| Spring | CS 290 Ethics & Society II | 0 | 0 | 0 | ❌ empty |

**Roughly a quarter of Year 2 exists.** The eight empty courses are directories with zero files —
not stubs, not partial drafts.

---

## 2 · Findings — None

Both built courses were swept for external dependencies, same-course forward references, and
content borrowed from unbuilt courses. **Nothing was found that needs fixing.**

This is a genuinely different result from Year 1, which produced 27 raised findings. The difference
is discipline about forward pointers: where these courses reach ahead, they *say so, with the week
attached.* Examples, all verified in place:

- **CS 201 LAB 5** — *"The general statement, which **Week 11 will name** the roofline model…"*
- **CS 211 PS 2** — *"emits an AST that **Week 3's type checker** will annotate"*
- **CS 201 Reading Guide W6** — *"§9.9 onward is dynamic memory allocation, **which PROG 201
  covers**"*

That is the CS 101 pattern from Year 1, applied as a habit rather than an exception.

---

## 3 · Verified Clean

Each of these was a plausible gap that did not survive the lecture-level test.

- ✅ **CS 201 needs no probability whatsoever.** A sweep for *expected value*, *probability*,
  *random variable*, *Poisson* across all 39 lectures returned **zero hits**. This matters because
  MATH 251 is unbuilt — had CS 201 depended on it, the gap would have been unfixable.
- ✅ **CS 201's linear-algebra references are workloads, not theory.** Five lectures mention matrix
  multiply or dot product (`L15 Locality as Leverage`, `L33 The GPU and the SIMT Model`, `L35`,
  `L37`, `L39`), but every one uses them as a *cache* or *throughput* workload — the triple nested
  loop, not vector spaces or eigenvalues. **MATH 241's absence does not block CS 201.**
- ✅ **CS 211 builds its own automata theory.** `L04 Finite Automata and the Subset Construction`
  opens: *"This lecture is the proof, and it is constructive."* It develops
  regex → NFA → DFA → minimal DFA from scratch. No prior formal-language course is assumed, and
  MATH 151 (Year 1) does not teach automata.
- ✅ **CS 201 has no same-course forward references.** Four candidates surfaced on a keyword sweep;
  all four dissolved on inspection — two were incidental words inside quiz commentary, one was a
  lab tooling note about `cachegrind`, and one was the explicit Week 11 pointer quoted above.
- ✅ **CS 211 W0–4 likewise.** Its W0 hits for `SSA`, `Hindley-Milner` and `LALR` are all in the
  syllabus's **pipeline diagram** — `source text → tokens → parse tree → AST → typed AST → TAC →
  SSA → LLVM IR → machine code` — which is a roadmap, not a dependency.
- ✅ **Year 1 → Year 2 hand-off is sound.** Both built courses rest on Year 1 material that is
  complete: CS 201 on PROG 101's C and CS 102's algorithms, CS 211 on MATH 151's logic and
  CS 102's trees and graphs.

---

## 4 · The One Real Risk: Dangling Pointers

CS 201 refers to **PROG 201** at least nine times — in `L27`, `L30`, `L39`, four Reading Guides, the
syllabus and the README — always as *"PROG 201 covers this"* or *"PROG 201 runs alongside and
assumes it"*. The syllabus states the two were **designed to interlock**:

> *"PROG 201 has been running alongside CS 201 and assuming it. Every `fork`, `mmap`, `epoll` and
> signal handler you wrote there stands on this course's stack frame, virtual memory and I/O."*
> — `L39 The Road Ahead`

**PROG 201 does not exist.** These are not prerequisite gaps in the audited sense — CS 201 is
self-contained and teaches everything it needs — but they are promises to a reader that currently
resolve to nothing. The same applies to CS 202, referenced repeatedly as "next semester".

This is a **build-order** problem, not a sequencing one, and it resolves itself the moment PROG 201
is written. No action needed in CS 201.

---

## 5 · Carry-Forward from Year 1

Year 1's finding 21 flagged that **CS 102 `L25` uses expected value**, defined nowhere in Year 1,
and pointed forward to MATH 251 in Year 2 Spring. That dependency **still cannot be discharged**:
MATH 251 is unbuilt. The scoped preview added to `L25` remains the only thing standing in for it,
and should stay until MATH 251 exists.

---

## 6 · Recommendation

There is nothing to fix in Year 2's curriculum. The work is to **build the missing eight courses**,
and the audit's one piece of advice for that:

> Keep doing what CS 201 and CS 211 already do. Every time a lecture reaches forward, name the week
> it lands in. Year 1 produced 27 findings largely because its courses reached forward silently;
> Year 2's two built courses produced none because they do it out loud.

Re-audit each course as it is built, and apply §11's test from the first pass rather than the third.

---

*Audit covers Year 2 Sophomore. CS 201 fully; CS 211 Weeks 0–4; the remaining eight courses do not
yet exist. See [[Year1 - Freshman/PREREQUISITE AUDIT|PREREQUISITE AUDIT]] for the Year 1 audit and for §11's method.*
