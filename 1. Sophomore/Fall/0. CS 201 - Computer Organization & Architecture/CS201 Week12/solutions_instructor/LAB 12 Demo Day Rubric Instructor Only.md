# CS 201 · Lab 12 — Demo Day Rubric and TA Notes
## Instructor Only

---

> **Demo day for Project 2.** The demo is a graded component of Project 2 (see that spec); this file
> is how to run the session and score the live demos consistently. There is no unmarked-lab
> checklist — the whole session *is* the assessment for a slice of the project.

---

## Running the Session

**Six minutes per student**, four demonstrations plus one "got wrong and fixed". With ~24 students and two TAs running parallel stations, that is ~75 minutes of demos plus setup — it fits the slot if you keep time firmly.

**Set up two demo stations** so the class splits; students not demoing watch the other station or prepare. **Enforce the six-minute limit** — a demo that overruns is usually one that is not ready, and the time pressure is fair.

**Have the four required demonstrations written on the board** (Project 2 §4) so every student hits the same points and the marking is comparable.

---

## Scoring the Demo (part of Project 2)

The live demo is worth a portion of the Project 2 mark; the report and code carry the rest. Score the demo on **whether the four demonstrations actually run and produce sensible numbers**, and on the quality of the "what I got wrong" reflection.

| Demonstration | Looking for |
|---|---|
| **1. Pipelining** | Independent stream completes in ≈ N+4 cycles, not 5N. IPC stated and near 1 |
| **2. Hazard** | A dependency chain is measurably slower; hazard stats shown |
| **3. Cache** *(centrepiece)* | Cache-friendly vs hostile shows a real miss-rate and cycle gap; **student connects it to Week 11's 7.45× / 50%→8% and names where their model simplifies** |
| **4. Own program** | Anything that shows engagement beyond the required set |
| **The reflection** | A *specific* bug found and fixed — not "it was hard" |

**Demonstration 3 is the discriminator.** A student who reproduces the cache effect *and* can say honestly where their simplified model diverges from the real measurement (no prefetching, a fixed miss penalty, no TLB) has understood both the cache and the limits of modelling — which is the whole Project 2 thesis.

---

## Common Project 2 Failure Modes

Watch for these in the demos; they are where marks are lost:

| Symptom | Underlying error |
|---|---|
| Every program reports 1 cycle/instruction | The pipeline is not actually modelled — it is Project 1 with a cycle counter |
| N independent instructions take 5N cycles | Stages are serial, not overlapped — the pipeline is not pipelining |
| The cache-hostile case is *not* slower | The cache miss penalty is not applied to the cycle count, or the access pattern does not actually miss |
| Cycle count cannot be hand-derived | No validation — the number is unfalsifiable (Week 11's cross-check, skipped) |
| Forwarding never happens (everything stalls) | Data-hazard resolution too conservative |
| Branch penalty is zero | Misprediction not modelled |

**The two that matter most are the first three** — a "pipelined cache simulator" that does neither pipelining nor cache timing has done Project 1 twice. **Demonstration 1 (N+4 cycles) and demonstration 3 (cache gap) are the proof that both halves work**; insist on seeing both.

---

## The Look-Back (if time allows)

End the session, if the demos finish early, with a short synthesis discussion (L38). **Ask the room for the one thing that never clicked** — the answers tell you what to emphasise in the final review, and the students who articulate a lingering question are usually the ones who understood the most.

**Point them at the two closing documents:** the FINAL EXAM Revision Guide (before the exam) and the Course Retrospective (after). **Be explicit that the retrospective is not revision** — it is for afterward, and it will land better then.

---

## What Success Looks Like — for the Cohort

By demo day, a student should be able to:

1. Show a pipeline that overlaps instructions (N+4, not 5N) and report IPC.
2. Show that a hazard and a cache miss cost cycles, with statistics.
3. **Reproduce the course's cache result inside a model they built, and name the model's limits.**
4. State one specific bug they found and fixed by validating against hand computation.

**A cohort that can do this has built the machine, not just simulated it** — which is the point of ending a machine-organisation course by making the students construct a small machine.

---

*CS 201 · Week 12 · Lab 12 Demo Day Rubric · Instructor Only*
