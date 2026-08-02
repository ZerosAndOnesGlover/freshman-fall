# CS 101: Lecture 38 (Week 12, Lecture 2)
## What Comes Next: The Map of the Field

---

## 0. The Purpose of This Lecture

L37 inventoried what you know. This lecture maps what you do not, and says where each piece is
taught.

This is not a course catalogue. It is an argument that the things CS 101 left out were left out for
**specific reasons**, and that knowing those reasons tells you what to expect when you meet them.

---

## 1. The Single Biggest Omission: Concurrency

Every program you wrote this term did one thing at a time. Statements executed in order, and when
you called a function it finished before the next line ran.

**Almost no real system works this way.** Your phone runs hundreds of processes. A web server
handles thousands of simultaneous requests. Your laptop's CPU has multiple cores that genuinely
execute at the same instant.

### Why it was left out

Because concurrency breaks the one assumption every debugging technique you have relies on:
**reproducibility**.

A sequential bug happens every time you run the program. A concurrency bug happens on Tuesdays, in
production, under load, and never when you are watching. The reason is that with two threads
touching shared state, the number of possible interleavings is enormous, and only a few of them are
wrong.

Here is the canonical example. Two threads each run `counter += 1`, a thousand times:

```python
# counter += 1 is NOT one operation. It is three:
tmp = counter      # read
tmp = tmp + 1      # modify
counter = tmp      # write
```

If both threads read before either writes, one increment vanishes. Run this and you will get
something less than 2000, varying between runs.

**Recognise the shape of that bug.** It is a *read-modify-write* race, and it is the same structural
problem as the **TOCTOU** bug from Week 10 — check the file exists, then open it, and something
changes in between. You have already met concurrency's central hazard; you met it at the filesystem
boundary rather than between threads.

### What you will learn

- **Mutexes, locks, semaphores** — enforcing that only one thread touches shared state at a time
- **Deadlock** — two threads each holding what the other needs, both waiting forever
- **Atomicity** — operations that cannot be observed half-done (`os.replace` was one)
- **Message passing** — avoiding shared state rather than protecting it
- **Python's GIL** — why Python threads do not give you CPU parallelism, and what to use instead

**Where:** CS 250 (Operating Systems), CS 340 (Concurrent Programming)

---

## 2. The Layers Below

PROG 101 gave you C, so you have seen pointers and manual memory. What sits below that:

| Layer | What it does | Course |
|---|---|---|
| **Operating system** | Processes, scheduling, virtual memory, filesystems, syscalls | CS 250 |
| **Computer architecture** | Pipelines, caches, branch prediction, the memory hierarchy | CS 230 |
| **Compilers** | Lexing, parsing, type checking, optimisation, code generation | CS 220 |
| **Digital logic** | Gates, adders, registers — how a CPU is actually built | CS 130 |

Two things from this term point directly down into these:

**The cache is why your Big-O sometimes lies.** Week 6 said an algorithm's growth rate dominates.
True asymptotically — but a Θ(n log n) algorithm with poor locality can lose to a Θ(n²) one at
realistic sizes, because a cache miss costs roughly a hundred times a cache hit. CS 230 explains
this; it is the most common reason a "faster" algorithm measures slower.

**Parsing is layered because of L34.** Regular expressions cannot count, so they cannot match nested
brackets. Compilers therefore use regex for **tokenising** (words) and a grammar for **parsing**
(structure). That two-stage design is a direct engineering consequence of the theorem you proved
three weeks ago.

---

## 3. The Layers Above

| Field | The question it asks | Course |
|---|---|---|
| **Databases** | How do you query and update terabytes safely and concurrently? | CS 320 |
| **Networks** | How do machines talk over an unreliable medium? | CS 310 |
| **Distributed systems** | What if the machines disagree, or some are lying? | CS 450 |
| **Security** | What if the input is written by an adversary? | CS 330 |
| **Machine learning** | What if you cannot write the rules, only supply examples? | CS 360 |
| **HCI** | What if the hard part is the human? | CS 270 |

Three of these deserve a sentence each, because this term set them up.

**Databases** are where your Week 10 atomic-write discipline becomes a formal theory. You wrote
`mkstemp` + `fsync` + `os.replace` to survive a crash mid-write. A database generalises that to
**transactions** with ACID guarantees, and Lab 10's recovery exercise — where the backup lagged by
exactly one write — is precisely why real systems use a **write-ahead log**.

**Security** inverts your assumptions. Every course so far treats input as *possibly malformed*.
Security treats it as *deliberately crafted by someone who has read your source*. Your Week 9 ReDoS
exercise was the first taste: a regex that is fine on normal input and hangs forever on a string
chosen to make it backtrack.

**Machine learning** is the one whose relationship to this course is most misunderstood. It does not
repeal anything you learned. Training is an optimisation loop with a complexity cost; inference is a
sequence of matrix multiplications whose cost is analysable with Week 6 tools; the data pipeline is
Week 9 and Week 10 work, and is where most of the actual effort goes. And no amount of learning
decides the halting problem.

---

## 4. The Craft You Have Only Sampled

These are not separate fields. They are practices, learned across all your courses.

**Testing.** You ran test suites; you did not design them. You have not met property-based testing,
fuzzing, mutation testing, or coverage as a metric with known failure modes. And Week 11 gave you the
theoretical ceiling: testing shows presence, never absence. *(CS 210)*

**Version control.** You committed. You have not resolved a difficult merge, bisected to find a
regression, or read a five-year history to work out why a line exists. Reading history is a research
skill.

**Debugging.** You used print statements and read tracebacks. A debugger with breakpoints,
watchpoints and reverse execution is a different instrument. So is `valgrind`, which you met in
PROG 101 without systematising.

**Design.** You have written programs of a few hundred lines. The problems that appear at ten
thousand lines — coupling, dependency direction, the cost of a bad abstraction that everything now
depends on — cannot be demonstrated at this scale. *(CS 240)*

**Reading code.** Addressed in L39, because it is the largest gap.

---

## 5. How to Choose What to Learn Next

A rough ordering, and the reasoning behind it:

**1. Finish the core sequence.** CS 102, CS 210, CS 230, CS 250. These are prerequisites in the real
sense — not bureaucratically, but because later material is genuinely incomprehensible without them.

**2. Learn a language with a different model.** You know Python (dynamic, garbage-collected) and a
little C (manual, unsafe). Add one that argues with you: **Rust** (ownership enforced at compile
time), **Haskell** (no mutation), or **Go** (concurrency as a first-class feature). The goal is not
the language — it is discovering which of your habits were *Python* rather than *programming*.

**3. Build something nobody assigned.** Coursework tells you what to build and when it is done. Both
of those turn out to be the hard parts. A project you chose will teach you more about design than
any course, because you will make bad decisions and then have to live in them.

**4. Read code you did not write.** See L39.

**5. Follow the thing you found interesting.** You are a first-year. The strongest signal you have
about what to specialise in is which lecture this term you wanted to keep thinking about after it
ended. That signal is worth more than any ranking of career prospects.

---

## 6. Summary

| Area | Left out because | Where |
|---|---|---|
| **Concurrency** | It destroys reproducibility, which every technique here assumes | CS 250, CS 340 |
| Operating systems | Needs the C and architecture layers first | CS 250 |
| Architecture | Explains why measured time and Big-O diverge | CS 230 |
| Compilers | Regex-then-grammar is L34's theorem as engineering | CS 220 |
| Databases | Week 10's atomic write, generalised to transactions | CS 320 |
| Security | Assumes an adversarial input author, not a careless one | CS 330 |
| Machine learning | Repeals nothing; the pipeline is Weeks 9–10 work | CS 360 |
| Testing, design, debugging | Practices, learned across everything | CS 210, CS 240 |

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Two threads each execute `counter += 1` exactly 1000 times, starting from 0. State
the largest and smallest final values possible, and explain what interleaving produces the smallest.

**2. (Explain.)** §2 claims a Θ(n log n) algorithm can lose to a Θ(n²) one at realistic input sizes
because of caching. Explain how this is consistent with everything Week 6 taught, rather than a
contradiction of it.

**3. (Build.)** Take the TOCTOU bug from Week 10 and the `counter += 1` race from §1. Write out the
structure both share as a three-step pattern, and state the general defence.

**4. (Stretch.)** §3 claims machine learning "does not repeal anything you learned." Pick one thing
from this course and argue concretely that it still applies to an ML system — then name one genuinely
new question ML raises that CS 101 gives you no tools for.

### Answers

**1.** **Largest: 2000.** Every increment completes before the next begins — the threads happen not
to interleave badly, or the operation is protected by a lock.

**Smallest: 2.** This is the surprising one; most people say 1000.

The pathological interleaving: thread A reads `counter` (getting 0) and is then descheduled *before
writing*. Thread B runs to completion, taking the counter to 1000. Thread A now wakes and writes its
stale `0 + 1 = 1`, destroying all 1000 of B's increments. B is finished, so A proceeds alone for its
remaining 999 iterations, ending at 1000.

To get all the way down to **2**, both threads must interleave this way in *both* directions —
each stalling mid-increment while the other completes a full run, so that each run in turn is wiped
out. The final write of each thread is the only one that survives.

*Accept 2 with a coherent argument; accept 1000 with the "one stale write wipes a run" reasoning as
substantially correct.* The point is that the loss is not one increment — a single stale write can
discard an unbounded amount of work.

**2.** There is no contradiction, because Big-O and wall-clock time answer different questions.

Big-O describes the **growth rate as n → ∞**, discarding constant factors. The claim "Θ(n log n)
beats Θ(n²)" is a statement about sufficiently large n, and it is true.

Caching lives entirely in the **discarded constant**. A cache miss costs roughly 100× a hit, so an
algorithm with poor locality carries a large constant multiplier. For a range of realistic n, the
worse-growth algorithm with good locality can win — and then, past some crossover point, it always
loses, exactly as the asymptotics predict.

**The consistent statement:** Big-O tells you who wins *eventually*; it does not tell you where
"eventually" starts. Week 6 said this explicitly when it noted bubble sort beats merge sort at
n = 10. Caching just moves the crossover point, sometimes a long way.

**3.** The shared structure:

1. **Observe** some state (read `counter`; check `os.path.exists`)
2. **Decide** based on what you observed (compute `tmp + 1`; decide to open the file)
3. **Act** on the decision (write `counter`; open the file)

The bug is that **the state can change between step 1 and step 3**, so the decision is acted upon
after the world it was based on has gone. The observation is stale by the time it is used.

**The general defence: make the observe-decide-act sequence atomic** — indivisible from the
perspective of anything else that might interfere. Concretely that means a lock (threads), an atomic
instruction like compare-and-swap (hardware), a transaction (databases), or an operation that fuses
all three steps into one (`os.replace`; opening the file and catching the exception rather than
checking first).

Note what the defence is *not*: checking again. A second check has the same problem as the first.

**4.** **What still applies** — several good answers:

- **Week 9/10.** Loading, cleaning, encoding, and validating training data is text-and-file work, and
  it is where most real ML effort goes. A mis-decoded byte or an unnormalised Unicode string corrupts
  a dataset exactly as it corrupted your word counter.
- **Week 6.** Training cost scales in dataset size, parameter count, and epochs; inference cost is
  analysable per layer. "Why is this slow?" is still a complexity question.
- **Week 8.** Tokenisers are hash-table lookups; embedding tables are keyed lookups.
- **Week 11.** No model decides the halting problem. Learned approximation does not cross the
  computability boundary.

**A genuinely new question** — accept any of:

- **Correctness without a specification.** Every program this term had a right answer you could test
  against. A model that is 94% accurate is not "buggy" in any sense Week 7 covers, and there is no
  assertion to write.
- **Statistical rather than logical guarantees.** Your tools prove or test individual behaviours; an
  ML system's behaviour is a distribution.
- **Data as the artefact.** The training set determines behaviour more than the code does, and
  nothing in this course tells you how to reason about, version, or debug a dataset.

*Full marks require both halves — a concrete application and a genuine gap.* An answer that only says
"ML is just statistics" has missed the question.

---

## Reading

- **Anderson & Dahlin, *Operating Systems: Principles and Practice*, Ch. 4–5** — threads and races
- **Ulrich Drepper, "What Every Programmer Should Know About Memory"** — the caching claim in §2, at
  length
- **Julia Evans's zines** — optional; short, concrete introductions to most of §2 and §3

---

*CS 101 · Week 12 · Lecture 38 (Wed) · © CSE Department*
