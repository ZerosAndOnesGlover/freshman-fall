# CS 212 · Reading Guide · Week 2

---

## Required

| # | What | Length | Why |
|---|---|---|---|
| 1 | **Parnas (1972)**, *"On the Criteria To Be Used in Decomposing Systems into Modules"* | **4 pages** | The best value-per-page on this course. Fifty-four years old, entirely current, and it settles a question people still argue about. **Read it before L07** |
| 2 | **Sommerville §7.1**, "Design and implementation" | ~12 pages | The textbook framing of coupling and cohesion |
| 3 | **Hunt & Thomas, *The Pragmatic Programmer*, §7** — "The Evils of Duplication" | ~8 pages | The source of DRY, and it says *knowledge*, not *code*, in the first paragraph |
| 4 | **Martin, *Clean Architecture*, Ch. 7–11** | ~40 pages | The five letters in their author's words. **Read critically** — L08 disagrees with two of the verdicts you will find here |

**About two hours.** Parnas is the one to read slowly.

---

## Recommended

| What | Why |
|---|---|
| **Page-Jones, *"Comparing Techniques by Means of Encapsulation and Connascence"*** (CACM, 1992) | The origin of connascence. Short, and the ordering is the useful part |
| **Metz, *"The Wrong Abstraction"*** (2016, sandimetz.com) | **Three pages, and the most useful three pages this week.** Read it twice |
| **North, *"CUPID — for joyful coding"*** (2021, dannorth.net) | A direct, well-argued attack on SOLID as a set. A 2 Q4 is easier after reading it, and it is a model of how to disagree in public |
| **Stevens, Myers & Constantine, *"Structured Design"*** (IBM Systems Journal, 1974) | Where cohesion and coupling come from. Skim the scales; the prose around them is dated |

---

## On Reading *Clean Architecture* and *Clean Code*

Both are on this course's shelf and **both should be read with the syllabus §7 open beside them.**

**What they are good for:** Martin is unusually clear about dependency direction, and Chapter 11 on dependency inversion is the best short statement of it anywhere. His examples are concrete and his conviction is useful — a code review needs shared vocabulary more than it needs nuance.

**Where to push back:**

| His claim | The problem |
|---|---|
| Functions should be 2–4 lines | No empirical support; produces code whose control flow lives in the reader's head. **The course's rule is Fowler's: extract when the extracted part needs a name** |
| A comment is a failure | The *why* is not recoverable from code and is the first thing lost when authors leave. `roomsvc` is the evidence |
| The architecture should "scream" its domain and defer the database | Directionally right, frequently over-applied. **W3 L11 shows what it costs a five-person team** |
| SOLID as a set of five equals | They are of very different value, and four of them restate coupling and cohesion (L08 §6) |

**The useful posture:** read him as a strongly-opinionated senior colleague whose instincts are good and whose rules are over-general. **That is the posture the industry mostly failed to take**, which is why the disagreement is now loud.

---

## A Note on Reading `git log` as Evidence

A 2 requires this three times, and it is a skill the course uses right through to Week 11.

```bash
# What has this file been changed for?
git log --format='%s' roomsvc/bookings.py | head -60

# When did a string first appear, and what was the commit for?
git log -S"external_partner" --oneline

# Which files change together? (the crude version of Week 11's change coupling)
git log --name-only --format='---' | awk '...'    # or just read a few commits

# How many files did one change touch?
git show 7b1e4f2 --stat
```

**What you are looking for, in every case, is the axis of change** — the thing that keeps moving. L08 §2's entire verdict on open/closed rests on it, and so does the difference between a good abstraction and speculative generality.

**One warning.** `git log` tells you what changed, not why the person thought it should. For `roomsvc`, only **14%** of commits reference an issue (W1 L04 §6), so for 86% of them the reasoning is gone. **That gap is itself the evidence** for the traceability argument, and you should notice how much harder it makes this assignment than it would have to be.

---

*CS 212 · Week 2 · Reading Guide*
