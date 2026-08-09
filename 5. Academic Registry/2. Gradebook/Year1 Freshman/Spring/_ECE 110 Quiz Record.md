# ECE 110 · Quiz Record
## Not part of the course grade

> **This file is deliberately outside the gradebook's weighted components.** ECE 110's quizzes carry
> **no weight** — Laboratory 25%, Problem Sets 35%, Midterm 25% and Final 15% already sum to 100%
> without them, and `ECE 110.md` says so in as many words.
>
> The leading underscore in the filename keeps this file out of `tools/gpa.py`'s course scan. Do not
> rename it without checking `collect()` in that script.

---

## Why This Is a Separate File

The same reason it is separate in CS 102 and PROG 102, and the failure was found in CS 102 first:
the gradebook parser reads a component's items from its heading until the **next `##` heading
containing a percentage**. An unweighted subheading has none, so its rows are silently absorbed into
the component above it — in CS 102 that quietly attached eleven quiz rows to Project 2.

`ECE 110.md` avoids that today by having no quiz table at all. This file is where the quizzes go
instead, so that they are recorded somewhere rather than nowhere.

---

## What Is Different Here

**CS 102 and PROG 102 mark their quizzes out of 20 and return them.** ECE 110 does not mark its
quizzes at all — each paper says `UNGRADED` at the top, and the answer key is printed in the same
file, below the questions.

So the **Out of** column below reads `—`, not a number. That is load-bearing: the answer-sheet
generator reads it, and a non-numeric entry is what makes a quiz sheet say `Marks: ___ / —` rather
than inventing a total the paper never claimed. Writing `0` there would mean the same thing to a
reader and the wrong thing to the tool.

Use the **Sat** column as a tick. The point of the record is that you can see, in one place, which
weeks you actually checked yourself on.

---

## Quizzes

**10 minutes at the start of Wednesday's lecture, Weeks 2–12.** Closed book. Not marked.

**Quiz *N* covers Week *N*, and is sat in Week *N+1*** — note this is *not* the CS 102 convention,
where Quiz *N* covers Week *N−1*. ECE 110 numbers its quizzes after the material rather than after
the week they are sat in, so Quiz 7 covers Week 7 and is sat in Week 8.

| Quiz | Sat in | Covers | Topic | Out of | Sat |
|---|---|---|---|---|---|
| Quiz 1 | Week 2 | Week 1 | Boolean algebra: axioms, theorems, De Morgan | — | |
| Quiz 2 | Week 3 | Week 2 | Gates, functional completeness, gate-level design | — | |
| Quiz 3 | Week 4 | Week 3 | Half adder, full adder, ripple-carry, delay | — | |
| Quiz 4 | Week 5 | Week 4 | Karnaugh maps, minimization, don't-cares | — | |
| Quiz 5 | Week 6 | Week 5 | Decoders, encoders, multiplexers, demultiplexers | — | |
| Quiz 6 | Week 7 | Week 6 | The ALU and carry-lookahead | — | |
| Quiz 7 | Week 8 | Week 7 | Latches, flip-flops, timing | — | |
| Quiz 8 | Week 9 | Week 8 | Registers, counters, shift registers | — | |
| Quiz 9 | Week 10 | Week 9 | Finite state machines: Mealy and Moore | — | |
| Quiz 10 | Week 11 | Week 10 | Verilog: combinational and sequential description | — | |
| Quiz 11 | Week 12 | Week 11 | Memory circuits: SRAM, DRAM, ROM | — | |

*There is no quiz covering Week 0 (nothing precedes it) and none covering Week 12 (programmable
logic), which is examined only on the final.*

---

## Why An Unmarked Quiz Is Worth Sitting

Digital logic fails in a particular way: the ideas are individually easy and the errors are
procedural. A student who can state De Morgan's laws will still complement `(A+B̄)C` wrongly under
time pressure, and will not find that out from reading. The ten-minute Wednesday quiz is the
cheapest place to find it out — Week 2 rather than Week 6, when the midterm makes the same error
cost 14 points.

Marking them would add nothing to that. The answer key is in the paper because the feedback loop
that matters is the one that closes in the next five minutes, not the one that closes when a grade
comes back.

---

*ECE 110 · Quiz Record · Year 1 Spring*
