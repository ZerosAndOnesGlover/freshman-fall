# CS 201 · Week 12 · Lab 12
## Demo Day — Project 2

---

**When:** Week 12 lab session, 15:00–16:50, BH 210 *(the last lab)*
**Covers:** the whole course · **Assessment:** unmarked, but **your Project 2 demo happens here** — see the Project 2 spec for how it is graded

> **This is not a normal lab.** There is no new material and no checkpoints to tick. It is demo day for
> Project 2 — the cycle-accurate pipelined CPU simulator — and a chance to see what the rest of the
> class built.

---

## What Happens Today

You demonstrate your **Project 2** simulator running real programs, and you watch others do the same. **The demo is part of the Project 2 mark**; the report and code are submitted separately by Friday.

**Bring:**

- Your simulator, built and working on the lab machines.
- The four required demonstrations ready to run (see the Project 2 spec §4).
- A small program of your choosing that shows something interesting.

---

## Your Demo — 6 minutes

Show these four things, with the numbers on screen:

**1. Pipelining works (1 min).** Run a stream of independent instructions and show it completes in ≈ *N* + 4 cycles, not *5N*. **State the IPC.**

**2. A hazard costs cycles (1.5 min).** Run a dependency chain and show it is slower than the same number of independent instructions. Show your hazard statistics — stalls by cause.

**3. The cache is the story (2 min).** Run your **cache-friendly vs cache-hostile** program (row-major vs column-major, or similar). Show the miss rates and the cycle difference. **This is the centrepiece** — connect it to the real 7.45× / 50%→8% result from Week 11's matmul, and say where your model agrees and where it simplifies.

**4. Something of your own (1.5 min).** A program you found interesting, a bonus feature, or a case where your simulator surprised you.

**Then:** one sentence on the biggest thing you got wrong and fixed. **Every good project has one** — a hazard that stalled when it should have forwarded, a cache that counted a miss as a hit, a cycle count that did not match hand computation. Naming yours is the mark of having understood the machine, not just coded it.

---

## Watching Others — the Real Value

**You will see the same four demonstrations produce different numbers**, because everyone made different modelling choices — a different miss penalty, a different branch predictor, a different forwarding policy. **Notice the divergence and ask why.**

Questions worth asking a classmate's demo:

- "Why is your IPC higher/lower than mine on the independent stream?"
- "Does your cache-hostile number match the real Week-11 measurement? Where does your model diverge?"
- "What does your simulator *not* capture, and how would that change the numbers?"

**The point of demo day is calibration.** You have spent three weeks inside your own model; seeing five others is how you find out which of your choices were reasonable and which were arbitrary.

---

## After the Demos — A Look Back

If there is time, the session ends with a look at the course as a whole (L38's synthesis). **Bring one question** you still have about how the machine works — the thing that never quite clicked, or the connection you suspect but cannot prove. **This is the last time the whole class and the machine are in one room.**

---

## The Final, and the Retrospective

**The final exam covers Weeks 0–12** and is comprehensive — see `resources/FINAL EXAM Revision Guide.md`. **Demo day is not revision;** the revision guide is where your remaining time should go.

**And when the exam is over**, read `resources/Course Retrospective.md`. Not before — it is not revision, and it will mean more afterwards.

---

*CS 201 · Week 12 · Lab 12 — Demo Day*
