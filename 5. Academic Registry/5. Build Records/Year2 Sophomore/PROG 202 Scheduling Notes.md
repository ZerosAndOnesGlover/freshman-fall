# PROG 202 Scheduling Notes

What had to be decided before PROG 202 could be written, and why each decision went the way it did.
Written 2026-09-17, while building Week 0. **The authority** is
`5. Academic Registry/1. Scheduling/Year2 - Sophomore/CSE_Year2_Sophomore_Curriculum.docx`, and
where the registry's own scheduling files settle a question, they do.

---

## 1. Two lectures a week, so 26 lectures and not 39

[[Year2 - Sophomore/MASTER TIMETABLE|MASTER TIMETABLE]] and [[Year2 - Sophomore/ROOM ASSIGNMENTS|ROOM ASSIGNMENTS]] both give this course
**Tue/Thu 11:00–12:15 in TH 205** — two slots of 75 minutes, 150 contact minutes a week. CS 202 and
CS 212 are also 3-credit and get three 50-minute slots.

**Lectures are therefore numbered L01–L26, two per week**, where every other Year 2 course this vault
holds numbers them L01–L39. Nothing else in the structure changes: still thirteen weeks, thirteen
labs, thirteen problem sets, eleven quizzes.

It is the first thing a student notices and so it is stated in the syllabus, in the Week 0 README, and
in every week's summary line.

---

## 2. The lab lags a full week, because Wednesday is in the middle

The lab is **Wed 13:00–14:50, BH 215**; the lectures are Tuesday and Thursday. A lab sat on the
Wednesday of Week *N* would have had **one** of that week's two lectures.

**Lab *N* covers Week *N* and is sat on the Wednesday of Week *N+1***, which is the same shape CS 202
uses (Tuesday lab, Mon/Wed/Fri lectures) and the same shape PROG 201 used in Fall for the same
reason. **There is no lab in Week 1.**

---

## 3. Thirteen labs, thirteen slots, nothing moved

| Sitting | Which lab |
|---|---|
| Friday of Week 0 | Lab 0 |
| Wednesdays of Weeks 2–12 (11 Wednesdays) | Labs 1–11 |
| Wednesday of the completion period (Apr 29) | Lab 12 (demo day) |

Thirteen, and **Spring Break (Mar 16) takes no teaching Wednesday with it** — [[ACADEMIC CALENDAR]]
places it between Week 7 (Mar 9) and Week 8 (Mar 23) as its own non-teaching week.

**This course is luckier than PROG 201**, whose Fall Break ate a Monday and forced Lab 5 onto a
Friday. The syllabus says so explicitly, because a student takes both and will otherwise carry the
expectation across.

---

## 4. Lab 0 is at 13:00 on the Friday of Week 0

[[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]] puts **every** Year 2 course's Week 0 lab on the Friday that closes the
ten-day Week 0 (Jan 23). On that day:

| Course | Time | Room |
|---|---|---|
| CS 202 Lab 0 | 10:00–11:50 | BH 210 |
| **PROG 202 Lab 0** | **13:00–14:50** | **BH 215** |

**13:00–14:50 is this course's ordinary lab time, on an unusual day.** CS 202 has the morning, BH 215
has no other Spring booking, and no third Spring course holds a Week 0 lab. Unlike PROG 201's 17:00
start in Fall, no compromise was needed. Applies to Lab 0 only.

---

## 5. One midterm, and Weeks 6–12 examined only on the final

The docx says *Midterm 15%*, singular. [[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]] places it **Thursday Mar 5 of
Week 6, 18:00–19:15, covering Weeks 0–5**, and lists no second.

Consequence, stated in the syllabus: **the final is the first and only examination of Weeks 6–12**,
which is why it is comprehensive at 150 minutes for the same 15%, and why Week 12's lecture is a
revision lecture rather than a valediction.

---

## 6. Lab 5 is sat the day before this course's own midterm, and that is fine

Lab 5 covers Week 5 (monads) and is therefore sat **Wednesday of Week 6, 13:00–14:50** — and the
midterm is **Thursday of Week 6 at 18:00**, covering Weeks 0–5.

Nothing is moved. A two-hour practical on the `State` monad twenty-nine hours before a paper that
examines it is good timing. **The collision worth knowing about is the other one:** CS 212's midterm
is the *Wednesday* evening of the same week at 18:00, three hours after this lab ends, and MATH 251's
is the Monday. Week 6 of Spring carries four evening exams across four evenings.

---

## 7. Where the projects sit

The registry fixes both due dates and neither assignment date:

| | Due | Weight |
|---|---|---|
| Project 1 — a Haskell interpreter | **Fri Mar 13, Week 7, 17:00** | 15% |
| Project 2 — Prolog / property-testing | **Fri May 1, completion period** | 15% |

**Project 1 is assigned Wednesday of Week 4.** It needs ADTs (W1), higher-order functions (W2) and
monads (W5); assigning it in W4 gives four weeks, of which Week 6 is largely lost to the midterm.
Assigning it in W5, when the last prerequisite lands, would give two.

**Project 2 is assigned Wednesday of Week 9.** The Prolog half can start immediately (W8 facts and
rules, W9 execution model); the specification half needs Week 11. Lab 12 on Wed Apr 29 is the demo,
two days before the deadline.

---

## 8. The machine: what is here, and the one thing that is not

Measured on this machine, 2026-09-17:

| | |
|---|---|
| GHC / GHCi / `runghc` | **9.4.7** |
| `cabal` | 3.8.1.0 — **cannot reach Hackage** |
| SWI-Prolog | **9.0.4**, unbounded integers |
| Cores | 8; threaded RTS ways present (`thr`, `thr_dyn`, …), `Support SMP: YES` |
| GHC package db | 37 packages: `base`, `containers`, `array`, `bytestring`, `text`, `mtl`, `transformers`, `parsec`, `stm`, `deepseq`, `time`, `process`, `unix`, `binary`, `template-haskell`, `Cabal`, … |
| SWI libraries | `clpfd` (**`bounded=false`**), `chr`, `dcg/basics`, tabling (built in; `library(tabling)` deprecated) |
| Absent | **`QuickCheck`**, **`random`**, `stack`, `hlint`, `ormolu`, `gprolog` |

### 8.1 QuickCheck cannot be installed, and Week 11 is better for it

```
$ cabal update
Config file not found: /home/…/.cabal/config
Writing default configuration to /home/…/.cabal/config
<repo>/root.json does not have enough signatures signed with the appropriate keys
```

**There is no Hackage here and a student account cannot supply one.** `QuickCheck` is not in the
global package database and neither is `random`, which it depends on.

The curriculum's Week 11 is *"Property-Based Testing with QuickCheck"*. **Week 11 therefore builds
one** — a splitmix-style PRNG, an `Arbitrary` class with a size parameter, `forAll`, counterexample
reporting, and shrinking — in about 150 lines, shipped as `Week11/resources/Check.hs`. The
Claessen–Hughes paper is read either way.

This is the same shape as PROG 201's substitutions (no `perf` → write a sampling profiler; no `ab` →
write a load generator; no Docker → build a container from `clone`), and like those it is a
pedagogical improvement rather than a loss: **shrinking is the part every tutorial skips, and you
cannot skip it if you are writing it.**

### 8.2 `par`/`pseq` come from `base`

Every tutorial writes `import Control.Parallel`. The `parallel` package is absent. **`par` and `pseq`
are in `GHC.Conc` in `base`** with identical semantics, and `-threaded -rtsopts` with `+RTS -N8` is
the whole story on eight cores. Week 7 says so rather than failing to compile.

---

## 9. The course's running example, and where its data comes from

**`sched`**, a timetable checker over **this vault's own Year 2 Spring timetable** — the seventeen
sessions in [[Year2 - Sophomore/SPRING SCHEDULE|SPRING SCHEDULE]]. Built in Haskell across Weeks 0–7 (tuples → ADTs → folds →
type class → `State`), rebuilt in Prolog across Weeks 8–10, property-tested in Week 11, and compared
in Week 12.

Verified on this machine: **17 sessions, 1,070 contact minutes a week (17 h 50 min), zero clashes.**

Per course: CS 202 260, PROG 202 260, MATH 251 200, CS 212 150, ECE 211 150, CS 290 50.

---

## 10. Lab 0 finds a real defect in the registry, and it is not fixed here

The `sched` checker's first run reports that **two sessions overrun the protected 12:00–13:00 lunch
hour, and both are PROG 202's own lectures** — Tue and Thu 11:00–12:15, fifteen minutes each, thirty
minutes a week, **6.5 hours across the term.**

The conflict is between two registry files:

- [[Year2 - Sophomore/SPRING SCHEDULE|SPRING SCHEDULE]]'s grid marks 12:00–13:00 every weekday `🍽️ Lunch Break (protected — no
  classes scheduled)`, and the Monday breakdown repeats it as *"protected — schedule this, do not
  skip it"*.
- [[Year2 - Sophomore/MASTER TIMETABLE|MASTER TIMETABLE]] and [[Year2 - Sophomore/ROOM ASSIGNMENTS|ROOM ASSIGNMENTS]] independently book TH 205 for this course Tue/Thu
  **11:00**, and the docx's 3-credit line makes the session 75 minutes.

**Nothing has been changed.** Two independent records agree on the booking and one un-sourced claim
disagrees; the booking is more likely right, but "more likely" is not a licence to edit the registry
from inside a course build. It is recorded here, it is the payoff of Lab 0 §4d, and PS 0 Q5(d) asks
the student to argue it and to propose a one-number fix.

**The cheapest fix, for whoever takes it up:** move the protected hour to **12:15–13:15 on Tuesday
and Thursday only**. Nothing else is scheduled in that window on either day, so it breaks nothing.
Moving the lectures instead does break something — 10:45–12:00 collides with CS 212's 10:00–10:50 in
a different building, and 11:00–12:00 takes the course below its 150 contact minutes.

---

## 11. Numbers measured for Week 0, and one that had to be re-measured

Every figure in Week 0 came off this machine. Two are worth recording because getting them right
took a second pass.

**The CSE measurement (L01 §3).** `gcc -O2`, *n* = 10⁹: a pure C function called twice costs what one
call costs (0.44 s / 0.44 s); adding one `calls++` to a global nothing reads takes it to 0.88 s.
**Making the counter `static` does not restore the optimisation** (0.89 s) — checked, because the
solutions initially claimed it would. GCC's analysis is simply conservative, which is a better point
than the one it replaced.

**The 44 KB / 273 MB measurement (L02 §6).** The first draft attributed the whole gap to list fusion
and to `-O2`. **Wrong, and re-measured at both optimisation levels:**

| | `-O0` allocated | `-O0` residency | `-O2` allocated | `-O2` residency |
|---|---:|---:|---:|---:|
| `print (sum [1..n], length [1..n])` | 1,600 MB | **44,328 B** | **52,944 B** | **44,328 B** |
| `let xs = [1..n] in print (sum xs, length xs)` | 880 MB | **244,958,408 B** | 640 MB | **272,645,056 B** |
| `let xs = [1..n] in print (sum xs)` | 880 MB | 44,328 B | 52,312 B | 44,328 B |

**Two separate effects.** The residency gap is *retention* and is present at `-O0` — the optimiser
neither causes nor fixes it. What `-O2` adds is *fusion*, visible only in the allocation column, and
**naming the list switches fusion off**. The lecture, the lab and the solutions all now say this, and
the lab solutions note out loud that the earlier version was wrong — the course's own habit applied
to itself.

Also measured: `runghc` 8.5 s vs `-O0` 1.03 s vs `-O2` 0.15 s on `primes.hs` (**57×**); persistent
`Data.Map.Strict` insert at **560 B** into 1,000 entries and **1,040 B** into 1,000,000 (**1.86×** for
1,000× the data, against a `log₂` prediction of exactly 2×); `x = x + 1` compiled gives `<<loop>>` and
hangs in `ghci`.

---

## 12. Syntax is taught explicitly, in every language

Each new language in this course ships a **syntax-and-symbols reference** as a Week 0 / Week 8
resource, and each week's README carries a **"New syntax and symbols this week"** table naming every
mark introduced, how it is said out loud, and what it means.

`Week0/resources/Haskell Syntax and Symbols.md` covers layout, types, bindings, lists, application,
the operator zoo (`<$>`, `<*>`, `>>=`, `<>`, `<|>`), `do`-notation and pragmas, with a **Week** column
saying where each is taught, so a student meeting `>>=` in Week 0 can at least say *"that's bind"*.
Week 8 does the same for Prolog from nothing.

**Rationale:** you cannot look up a symbol whose name you do not know, and Haskell's reputation for
unreadability is mostly punctuation. This was a build instruction from the vault's owner and it
applies to every future language course here.

---

## 13. Week 0 brought into line with the conventions settled after it was written

Week 0 was written on 2026-09-17. Several vault-wide conventions were settled between then and
2026-09-28, and Week 0 was reworked to them rather than left as the one week that does not follow
them.

| Convention | What changed in Week 0 |
|---|---|
| **Lecture opening block** — title, verified quote, exact `**Reading:**`, generated `**Coursework:**` | L01 and L02 gained a quote and a generated coursework line. `Y2_DAYS` in `tools/make_lecture_notices.py` already carried `"PROG 202": "TR"`; `--check` now reports 0 changes |
| **Problem-set volume: about three hours, roughly 8 problems / 15 answer parts, still 100 points** | PS 0 went from 20 parts to **15**, and from 236 lines to 207. Cut: the `length xs / 2` argument (Q1d), the five-item transparency list trimmed to three, the nested-`:sprint` session (old Q3c), `freeSlots` (old Q5b). Merged: old Q2c+Q2d, old Q4b+Q4c. Points still sum to exactly 100 |
| **Lab finishes inside its 110-minute session, ≤30 min write-up** | Timings were 120 minutes. Now §0 10 · §1 20 · §2 12 · §3 10 · §4 40 · §5 12 · checkoff 5 = **109**. §5's eight-number table moved to PS 0 Q4(b), where it has marks; the lab keeps one extra number |
| **Submissions are one repo per semester, with a git-ignored `practice/` in every week** | Lab 0 §0 no longer tells students to `git init` a per-course repo. Work goes in `week0/practice/`, nothing from the session is submitted, and the sheet has them run `git check-ignore -v` to see the rule named |
| **No Claude attribution in commits** | Week 0's own commit `6524661` carries a `Co-Authored-By` trailer, because it predates the rule by five days. **96 commits sit on top of it, so it has not been rewritten.** No later PROG 202 commit has one |
| **No revision notes in handouts** | Checked: the lectures, the lab sheet, the problem set and the syllabus carry none. The one "this replaces an earlier version" note is in **Lab 0 Solutions §5**, which is a key, where the convention puts change history |

**The course's submission folder** was created to the checklist at the same time:
`4. Submissions/Year2 Sophomore/Spring/2. PROG 202/` with `week0`–`week12`, a `practice/` in each, a
course README, and a shape-based `.gitignore` whose allow-list is `*.hs *.lhs *.pl *.plt Makefile
*.cabal *.sh *.md *.csv *.txt .gitignore` with `practice/` last. Verified in a scratch repo: sources
and answer sheets are tracked; GHC's `.hi`, `.o`, extensionless executables and `.prof` dumps are
ignored; everything under `practice/` is ignored including `.hs` and `.md`.

**Still outstanding, and not this course's to do alone:** `Year2 Sophomore/Spring` is not yet a git
repo and has no GitHub remote, and CS 202, CS 212, MATH 251, ECE 211 and CS 290 have no submission
folders. That is a semester-level job needing the other five courses and a repository the user
creates.

### One measurement added while reworking PS 0 Q2(b)

The question now asks students to *try to win back* the optimisation `calls++` cost. Measured, so the
key can mark the attempts:

| `impure_sum`, *n* = 10⁹ | once | twice |
|---|---:|---:|
| as written | 0.44 s | 0.88 s |
| `static long calls` | 0.44 s | **0.89 s** — no help |
| `gcc -O2 -flto` | 0.45 s | **0.89 s** — no help |
| `__attribute__((noinline,const))` | 0.44 s | **0.44 s** — restored |

The last row is the punchline and it is why the question is worth asking: `const` is the programmer
*promising* what GCC could not prove, **with no check that the promise is true**. A type system gives
the same guarantee and does check it.

---

*Written while building Week 0. Sections are added as later weeks raise new decisions.*
