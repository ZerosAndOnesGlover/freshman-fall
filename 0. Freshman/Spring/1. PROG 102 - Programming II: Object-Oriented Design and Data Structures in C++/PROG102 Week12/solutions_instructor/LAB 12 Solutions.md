# PROG 102 · Lab 12 — Checkoff Notes
## Project Demo and Code Review

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**This is the last lab, in final-exam week, with Project 2 due Friday.** The room will be at capacity.

**Two administrative things first:**

1. **Check the lab register.** Labs are 20% of this course and there is no completion gate, but a
   student who has missed several should know where they stand **before** the final rather than after.
2. **Pair people who have not seen each other's projects.** If numbers are odd, make one group of
   three and give them ten minutes each rather than eight.

**Say at the start that a project which does not build is not a disaster.** The honest version — "Part
4 is unfinished, here is what works" — is worth more marks than a demo that talks around a broken
build, and students need permission to say it.

**Timing is tight.** Hold the demos to eight minutes with a visible timer, or Part B loses the time it
needs.

---

## Part A — The Demo (16)

### A1 (4) — builds and runs

*Marking: 4 for a clean build and a passing suite from the [[PROG102 Week12/README|README]] command. **Deduct 1, not 4, for
warnings.** Deduct 2 for a build that needed undocumented steps.*

**A project that does not build:** award up to 2 if they say so immediately and demonstrate what does
work. **Award 0 for a demo that conceals it** — and it is always obvious.

### A2 (4) — one right, one wrong

*Marking: 2 + 2. **The "wrong" half is not a formality.** A student who says "nothing went wrong" gets
0 of those 2 — everyone's Project 1 feedback said something, and Project 2 Part 1.3 required them to
list changes.*

**The best answers are specific and slightly uncomfortable:** "I claimed `erase` was strong and the
sweep showed basic at the third failure point." Reward those visibly; it sets the tone for the room.

### A3 (4) — a number

*Marking: 2 the benchmark run live with a standard-library comparison, 1 stating what it does not
measure, 1 **what they did to stop the compiler deleting it.***

**The last point is the course's signature and should be asked about if they omit it:** *"How do you
know the loop ran?"*

### A4 (4) — defending a decision

Two questions, from the reviewer or you. Good ones:

- *"Why a sentinel?"* — expect the four-cases-become-one answer.
- *"Why does `find` return a raw pointer?"* — expect non-owning, and Week 5's preference list.
- *"Which guarantee does `insert` provide, and how do you know?"* — expect a sweep, not an assertion.
- *"Your iterator is bidirectional. What does that stop you doing, and why is that good?"*

*Marking: 2 per answer. **Mark the defence, not the decision.** A student who chose differently from
the reference and can say why deserves full marks.*

---

## Part B — The Review (18)

### B1 (4)

Built it, ran the tests, reported warnings.

*Marking: 4. **Require evidence they actually built it** — a warning count, a test output line.*

### B2 (6)

Three findings **with file and line**: one well done, one correctness concern, one design question.

*Marking: 2 each. **"Good code" or "looks fine" is 0 for that item.** The design question must be
phrased as a question — an instruction where a judgement was needed loses 1.*

### B3 (4) — the assessed part

**Pick a claim from their `CONTRACTS.md` or `DESIGN.md` and test it.**

*Marking: 4 for a claim identified, a test written, and a result reported. **Either outcome scores
full** — "it held" is as good a review as "it did not".*

**This is the part that separates a review from an opinion**, and it is where the lab's argument lives.
If a pair finishes early, this is what to extend.

### B4 (4)

A paragraph of assessment, and one thing they will take into their own work.

*Marking: 3 + 1. **"Nothing" for the second gets 0** — the sheet says there is always something.*

---

## Part C — Reflection (6)

### C1 (3), C2 (3)

One disagreement argued; one correct point they had not seen.

*Marking: 3 each. **Both required.** A student who agrees with everything has not read the review; one
who agrees with nothing has not either. Award 3 of 6 for a well-argued one-sided response, 0 for
neither.*

---

## Checkoff Checklist

1. Built from [[PROG102 Week12/README|README]], in front of a TA.
2. A2's "what went wrong" is specific.
3. A3 states how they know the benchmark ran.
4. The review has **file and line** references.
5. **B3 tested an actual claim.**
6. C has both a disagreement and a concession.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 16 |
| B | 18 |
| C | 6 |
| **Total** | **40** |

---

## Note for the Last Lab

There is no new material. **Use the last five minutes on the point the course has been making, because
this is the last time the room is together.**

The version that works:

> **Part B3 asked you to take a claim from someone else's documentation and test it.** Their
> `CONTRACTS.md` said `insert` was strong. Somebody wrote that at midnight with a deadline — which is
> to say, under exactly the conditions that produce most of the claims you will read for the rest of
> your career.
>
> **It took you ten minutes to find out.**

Then close it:

> Twelve weeks ago you compiled a member function and a free function and compared the assembly, to
> check whether a lecture was telling the truth. Last week you shuffled an index array and found that
> **Week 3 of this course had given you an explanation that was almost right and not quite.**
>
> **C++ is the vehicle.** It will change — the language you write in ten years will have absorbed half
> of Weeks 7 and 8 into features. **What will not change is that software is full of confident claims,
> most of them well-meant, and that there is almost always a way to go and look.**

Then point them at the **Course Retrospective** — after the final, not before — and let them go.

---

*PROG 102 · Week 12 · Lab 12 Solutions · © CSE Department*
