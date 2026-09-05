# CS 211 · Lab 12
## Lightning Talks, and Demo Day

**Friday of Week 12 · 14:00–15:50 · BH 220 · the last session**
**Unmarked and mandatory.** The TA checks you off in the session.

> **Project 2 is due today at 17:00 and is demoed here.** Bring something that runs from a clean
> checkout in one command. If it does not run, come anyway and demo what does — a working Part A
> shown honestly beats a Part C described.

---

## Format

**First hour: Project 2 demos.** Five minutes each, in pairs at your machines, TA circulating.

**Second hour: lightning talks.** Five minutes, no slides required, on **a programming language of your choice** — one this course did not cover.

---

## Part A — Project 2 Demo (55 min)

Have ready, in one terminal:

```bash
git clone <your repo> && cd <your repo>
./run_tests.sh              # or whatever your one command is
python3 cyanc.py demo.cy 1071 462 --run
```

**Show, in five minutes:**

1. **It runs.** One program, source to answer.
2. **Your differential test passing** — interpreter against JIT.
3. **One optimisation, with the counts** before and after.
4. **The `opt -O2` comparison**, honestly. If your pass made no difference to the final output, say so — that is the expected result and it is worth marks in the report.
5. **One thing that does not work**, and why.

**Point 5 is not a trap.** Every compiler in this room is incomplete, the report asks for it, and a student who can name their own limitation precisely is demonstrating exactly what the last twelve weeks were for.

---

## Part B — Lightning Talks (55 min)

**Five minutes on a language this course did not cover.** No slides needed; a terminal is fine.

Good choices: Go, Zig, Kotlin, Swift, Erlang, Elixir, Haskell, OCaml, Julia, TypeScript, Scheme, Prolog, APL/J, Forth, Ada, Clojure, Nim, Crystal, Elm, Idris.

**Cover four things.** Not a feature tour — an argument:

1. **The central decision.** What did this language decide to make impossible, or possible, that its neighbours did not?
2. **What that bought, and what it cost.** Be specific. "Safe" and "fast" are not answers.
3. **One thing from this course that appears in it.** Type inference, a collector, a macro system, a memory model, an ownership rule, a JIT — every language on that list contains several.
4. **Would you use it, and for what?**

**A five-minute talk is about 600 words.** That is one paragraph per point. Practise it once out loud; the difference is obvious from the front of the room.

---

## Part C — Looking Back (10 min)

Together, before you leave.

**One question, answered around the room:**

> **What did you believe in Week 0 that you no longer believe?**

Candidates, if nobody starts:

- That a compiler is one program rather than nine.
- That optimisation is about making code shorter.
- That "memory safe" is one property.
- That a test suite can find a concurrency bug.
- That types are annotations you write for the compiler's benefit.
- That the hard part of a compiler is parsing.

---

## Before You Leave

1. **Confirm Project 2 is submitted.** Not "will be at 16:50".
2. Give your lightning talk.
3. Say your Part C answer.

**And note the date: the final exam is Tuesday 16 December, 09:00–11:30, VNC 100.** The revision guide is in `resources/`, and the eleven quiz keys are the best material you have.

---

*CS 211 · Week 12 · Lab 12 · © CSE Department*
