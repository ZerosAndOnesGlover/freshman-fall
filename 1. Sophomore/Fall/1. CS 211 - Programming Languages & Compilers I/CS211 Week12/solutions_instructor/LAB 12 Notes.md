# CS 211 · Lab 12 — Running Notes
## Instructor Only

**The last session.** Project 2 demos, lightning talks, and a look back.

---

## Before the Session

**Check submissions at 14:00 and again at 15:30.** Project 2 is due at 17:00 and every year somebody plans to submit at 16:55 and hits a problem at 16:50. A five-second question at 15:30 prevents most of it.

**Have a fallback machine ready** with the Week 11 lab checked out. Demos die on environment problems, and the demo marks are for the compiler, not for the student's `PATH`.

---

## Part A — Demos (55 min)

**Five minutes each, in pairs, TA circulating.** Do not let this become twenty minutes for the first student.

**What to look for, in order:**

1. **It runs from a clean checkout.** This is the single most common failure and it is worth saying at 14:00.
2. **The differential test.** Interpreter against JIT. If they have not got one, that is Part A of the project and it is 30 marks — tell them now, they have three hours.
3. **One optimisation with counts.**
4. **The `opt -O2` comparison.** **Most students' passes will make no difference to the final output.** That is the expected finding. **Credit them for reporting it and push back hard on anyone who omits it** — the report marks it explicitly.
5. **One thing that does not work.** Anyone who says "everything works" should be asked to try arrays.

**The demo is not separately graded** — it feeds the project mark. Note anything that will not be visible in the zip: a student whose compiler is clearly working but whose report is thin should be told so, today, while it is still fixable.

---

## Part B — Lightning Talks (55 min)

**Five minutes, hard stop.** Twelve talks in an hour needs the timer enforced from the first one.

**The four points in the brief are the rubric.** The failure mode is a feature tour — "Go has goroutines, and interfaces, and…" — with no argument. Redirect with one question: **"What did it decide to make impossible?"**

**Talks that reliably go well:** Erlang (supervision and let-it-crash, straight out of Week 9), Zig (comptime, which is Week 10), Prolog (unification, which is Week 8), APL/J (notation as a tool of thought), Forth (a language you can read the whole implementation of).

**If the room is quiet**, seed it: ask who has used a language whose error messages they liked, and why.

---

## Part C — Looking Back (10 min)

**Do not skip this for time.** It is ten minutes and it is what students remember.

The question is *what did you believe in Week 0 that you no longer believe*. Common answers, and all of them are good:

- that a compiler is one program;
- that parsing is the hard part;
- that "memory safe" is one property;
- that types are for the compiler's benefit;
- that a test suite can find a race.

**One thing worth saying out loud at the end**, because it is true and nobody will say it for you: **they have written a compiler that produces working x86-64**, and the gap between that and a real one is a list they can now read.

---

## Housekeeping

- **Final exam: Tuesday 16 December, 09:00–11:30, VNC 100.** Comprehensive, 150 marks, one A4 sheet **both sides**.
- Point them at `resources/FINAL EXAM Revision Guide.md` and, more importantly, at **the eleven quiz answer keys**, which are the best revision material in the course and already written.
- **PS 11 and PS 12 are both due today**, and the lowest problem set is dropped.

---

*CS 211 · Week 12 · Lab 12 Notes · © CSE Department*
