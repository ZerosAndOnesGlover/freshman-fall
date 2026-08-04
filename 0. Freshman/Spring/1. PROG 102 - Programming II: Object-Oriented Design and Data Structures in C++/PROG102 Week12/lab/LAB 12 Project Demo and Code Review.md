# PROG 102 · Lab 12
## Project Demo and Code Review

**Week 12 · 2-hour lab session · 40 points**
**Deliverable:** your demo, a written review of a peer's project, `RESULTS.md`. In-lab checkoff.

> **This is the last lab.** Project 2 is due Friday and the final exam is this week.

---

## Purpose

Two things, and the second is the one people underestimate.

**You present Project 2** — not a slideshow, a working demonstration with numbers.

**You review someone else's**, in writing, against the same standards you were held to. **Reading
other people's code is most of what a working programmer does**, and this is the only structured
practice at it the course provides.

---

## Format

| Time | Activity |
| --- | --- |
| 0:00–0:15 | Setup. Everyone builds and runs their own project once, in front of a TA |
| 0:15–0:55 | **Demos** — 8 minutes each, in pairs or small groups |
| 0:55–1:35 | **Code review** — you read your partner's project and write it up |
| 1:35–1:55 | Reviews exchanged and discussed |
| 1:55–2:00 | Checkoff |

**You will be paired with someone whose project you have not seen.**

---

## Part A — Your Demo (16 pts)

**Eight minutes.** Not a presentation — a demonstration.

**A1.** *(4)* **Build and run it from a clean checkout**, with the single command from your
`README.md`. It must build with no warnings and the test suite must pass.

*(If it does not build, say so immediately and demo what you have. An honest "Part 4 is incomplete"
costs far less than a demo that pretends.)*

**A2.** *(4)* **Show one thing you got right and one you got wrong.**

The second is worth as much as the first. "My `erase` was basic when I claimed strong until I swept
the failure point" is a better demo moment than any feature.

**A3.** *(4)* **Show a number.** One benchmark, live, with the comparison against the standard library.

State what it measures, what it does not, and **what you had to do to stop the compiler deleting it.**

**A4.** *(4)* **Answer two questions** from your reviewer or the TA about a design decision.

"Why a sentinel?" "Why is `find` returning a raw pointer?" "Which guarantee does `insert` provide and
how do you know?" **You are marked on whether you can defend the choice**, not on whether it was the
choice we would have made.

---

## Part B — Your Review of a Peer's Project (18 pts)

Written, and given to them. **Be useful and be kind — those are the same thing here.**

**B1.** *(4)* **Build it yourself** from their `README.md`. Report whether it built, whether the tests
passed, and any warnings.

**B2.** *(6)* **Find three specific things**, with file and line:

- one that is **well done** — and say why, specifically. "Good code" is not a review.
- one **correctness concern** — a missing guarantee, an unhandled edge, an iterator invalidation.
- one **design question** — not a bug; a decision you would have made differently, phrased as a
  question.

**B3.** *(4)* **Check one claim.** Pick something their `CONTRACTS.md` or `DESIGN.md` asserts — a
guarantee, a complexity, a thread-safety statement — and **test it.**

Report whether it held. **Either answer is a good review.**

**B4.** *(4)* **One paragraph of overall assessment**, and one sentence on **what you will take from
their project into your own work.**

There is always something. Find it.

---

## Part C — Reflection (6 pts)

`RESULTS.md`.

**C1.** *(3)* You received a review. **Name one thing in it you disagree with**, and argue your case in
three sentences.

**C2.** *(3)* **Name one thing in it that is right and that you had not seen.** Say what you would
change.

**Both are required.** A student who agrees with everything has not read it, and one who agrees with
nothing has not either.

---

## Submission

- `RESULTS.md` — your Part C reflection, plus your demo's benchmark output.
- Your written review of your partner's project, **also given to them.**

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 16 | A working demo, honestly presented |
| B | 18 | A useful, specific, verified review |
| C | 6 | Receiving criticism usefully |
| **Total** | **40** | |

---

## What Makes a Good Review

**Specific beats general.** "Line 47 of `list.hpp`: `erase` returns an iterator to the erased node,
which is now dangling — should it be the next one?" is worth more than a paragraph on style.

**A question beats an instruction** for anything that is a judgement rather than a defect. "Why raw
pointers for `prev`/`next` rather than `unique_ptr`?" invites the answer that they are structure and
not ownership — which is correct, and which you would have missed by writing "use smart pointers".

**Check something.** B3 is the part that separates a review from an opinion. **Their `DESIGN.md` says
`insert` is strong; make it throw and find out.**

**And find the good thing first.** Not politeness — accuracy. A project that got this far has something
in it worth stealing, and noticing it is a skill.

---

## What This Lab Is Really Showing

You have spent twelve weeks being told to go and look — at the assembly, at the symbol table, at the
sanitizer output, at the clock.

**Part B3 is the same instruction pointed at a person's claims.**

Their `CONTRACTS.md` says `insert` provides the strong guarantee. That is a **claim**, made by someone
who was tired and had a deadline — which is to say, made under exactly the conditions that produce the
claims you will read for the rest of your career. **You now have a method for checking it**, and it
takes about ten minutes.

**That is what this course was for.** Not C++ — C++ is the vehicle, and it will change. The habit is
that when someone tells you what code does, including when that someone is you, **there is a way to
find out.**

---

*PROG 102 · Week 12 · Lab 12 · © CSE Department*
