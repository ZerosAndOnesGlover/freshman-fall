# CS 212 · Assignment 4 — Solutions and Mark Scheme
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 4.** The assignment is designed so that **the best answer is often not to
apply a pattern.** Q1(b) requires a non-pattern candidate, Q3 explicitly accepts a non-pattern
description, and the bonus note rewards deletion. **Mark accordingly**: a student who replaces a
three-class hierarchy with a six-line dict and describes it properly has done better work than one
who adds a correct Strategy.

**The three discriminators:**

1. **Is the smell evidenced or asserted?** Q1(a) demands a count, a `git log` or an absent test. A
   student who writes *"this code felt repetitive"* has not done Q1.
2. **The file-count in Q1(c).** It is the only number in the paper that measures the *cost* of the
   refactoring rather than its benefit, and it is the one students omit.
3. **Q5's revisit condition.** *"We ran out of time"* against *"we will revisit when the third
   resource kind lands, which is issue #41"*.

**Automatic caps, both stated:** tests failing → 50; the A 2 pricing case reused → 55.

**Calibration:** median 68–72.

---

## Q1: Find and Evidence the Smell (25)

### (a) [8]

| | |
|---|---|
| 4 | The smell stated as a **problem** — what recurs, where, what it costs |
| 4 | **Two forms of evidence**, 2 each |

**Deduct 4** for an assertion with no evidence. **Deduct 2** for one form of evidence where two were
required.

**Smells that are genuinely present in most teams' `slot` by Week 4**, for the marker's calibration:

| Smell | Typical evidence | Usual right answer |
|---|---|---|
| The state string compared in five places | `grep -c "== 'CONFIRMED'"` | **An enum**, not a pattern. L15 §3's table |
| `Booking` constructed with 6 fields in 14 tests | Line count in `tests/` | **Test data builder** (L14 §3) |
| `datetime.now()` called inside domain functions | `grep -rn 'now()' src/slot/domain` | **Pass a clock in.** Not a pattern; a parameter |
| A `Notifier` constructed inside `service.py` | One line, but it is the L14 §1 smell exactly | Pass it in |
| Route handlers each opening their own session | 4–6 occurrences | **Unit of Work**, or a FastAPI dependency |
| `if resource.kind == 'ROOM'` in three places | `grep` | Usually: **delete the branch**, because W1 L06 §3 said rooms and equipment are one concept |

**The last row is the best available answer and about one student in fifteen finds it.** If a student
identifies that their own code has re-introduced the room/equipment split the domain model rejected,
and deletes it, that is a 95+ paper. **Say so.**

### (b) [7]

| | |
|---|---|
| 3 | Three genuine candidates |
| 2 | **At least one is not a pattern** |
| 2 | Cost-to-a-reader and benefit for each |

**Deduct all of the "non-pattern" 2** if all three candidates are GoF patterns. The paper requires it
and the requirement is the pedagogy.

**Deduct 2** for candidates that are not really alternatives — "Strategy, or Strategy with an
abstract base class, or Strategy with a registry" is one candidate with three spellings.

### (c) [10]

| | |
|---|---|
| 4 | The problem named without reference to the pattern's name |
| 3 | **The second case, named — or its absence acknowledged with a reason to proceed anyway** |
| 3 | **File-count before and after, as numbers** |

**The "no second case" route is fully creditable** and should be, because it is often true and the
honest answer is *"there is no second case yet; we did it anyway because the enum/table also makes
the invariant testable, which is a benefit that does not depend on a second case"*. **That is a
correct engineering argument and scores 3.** *"There is no second case but patterns are good
practice"* scores 0.

**The file-count marks are for the number, in both directions.** A refactoring that takes the count
from 1 to 2 and justifies it ("the rule is now in one place and exhaustively tested, which the
single file was not") scores 3. A refactoring that takes it from 3 to 1 and says so scores 3. **No
number scores 0**, and this is the most commonly dropped 3 marks in the paper.

---

## Q2: Do It (30)

**Mark from the pull request.**

### [12] Correctness and completeness

- 12: refactoring complete, all callers migrated, old path deleted.
- 8: correct but leaves the old function in place "for now" with no deprecation note.
- 4: partial — some callers migrated.
- 0: the "refactoring" is a rename, or it does not run.

**Check for dead code explicitly.** The most common defect is a correct new implementation with the
old one still present and still called from one place — which is worse than either, because now the
rule lives in two places.

### [8] Tests pass unchanged

8 if `pytest` is green and no test file changed except additions. **If tests changed:** 8 is still
available if the PR description names which, why, and what behaviour changed — **but check whether
the behaviour change was necessary.** A student who changed a test because their refactoring was
wrong, and says so, gets 6 and a note; a student who changed a test silently gets 0 and the paper
is capped at 50.

### [6] Commit granularity

| | |
|---|---|
| 6 | Four or more commits: characterisation test, introduce the new thing, migrate callers one group at a time, delete the old |
| 4 | Three commits with a sensible split |
| 2 | Two commits |
| 0 | One |

**Refactoring is the easiest work in the world to commit incrementally**, and a single commit here is
strong evidence the student refactored by rewriting rather than by transforming. Say so.

### [4] Description

4 requires all three: the smell, what was done, and **what a reviewer should check first.** The
third is the professional habit and is worth pushing on.

---

## Q3: Write the Pattern Description (20)

| | |
|---|---|
| **5** | Problem, stated so the *next* occasion is recognisable |
| **5** | Solution, in Python, ceremony removed |
| **7** | **Two or more consequences that are costs** |
| **3** | Known uses, honestly — including "only the textbook" |

**The 7 marks for consequences are the heart of the question.** Acceptable costs, with the standard:

| Generic (2 of 7) | Specific (7 of 7) |
|---|---|
| "Adds indirection" | "A reader answering *what does a confirmed booking cost?* now opens `policies.py` and `registry.py` instead of one file, and the branch condition is no longer visible at the call site" |
| "Slightly slower" | "One dict lookup per call, which is nothing — but the policy objects are constructed at import time, so a bad entry now fails at startup rather than on first use. That is better, and it is a change" |
| "More files" | "Three new files, and our `grep` for pricing logic no longer finds everything, because the multiplier lives in a data structure rather than in code" |

**Full marks for a non-pattern description**, and the marker should look for these specifically:
*"replace the class hierarchy with a lookup table"*, *"pass the clock in"*, *"replace the string with
an enum"*, *"delete the branch"*. **All four are better engineering than most pattern applications**
and the four-part description works unchanged.

---

## Q4: Norvig's Test (15)

### (a) [8]

| | |
|---|---|
| 3 | GoF structure, correctly |
| 2 | The Python version, correct and idiomatic |
| **3** | **What survived** |

**The 3 marks are for the survival, not the disappearance.** Model answers:

- **Strategy** — disappeared: the interface, the N classes, the field, the constructor. **Survived:
  the design decision that this axis varies at runtime and is chosen by the caller rather than
  branched on internally.**
- **Command** — disappeared: the class and the `execute()` method. **Survived: reification — the
  ability to store, queue, log, retry and invert the request.** And a student who notes that
  reification is exactly what a closure does *not* give you (you cannot serialise it) has found the
  real residue and should get 8.
- **Singleton** — disappeared: everything. **Survived: nothing, and that is the answer** — modules
  are singletons and the pattern was always a workaround for languages without them.
- **Iterator** — disappeared into `yield`. **Survived: the protocol.** `__iter__`/`__next__` *is*
  the pattern, promoted to a language contract.

**Deduct 3** for an answer that says only "it becomes a function".

### (b) [7]

| | |
|---|---|
| 4 | The feature's PEP/release/motivation, correctly found |
| 3 | A coherent argument about the next one |

**Reference facts for the common picks:**

| Feature | PEP | Release | Motivation |
|---|---|---|---|
| Generators | **PEP 255** | 2.2 (2001) | Producer/consumer without threads; the Iterator pattern's boilerplate |
| Decorators | **PEP 318** | 2.4 (2004) | `f = staticmethod(f)` after a long function body was unreadable |
| `with` / context managers | **PEP 343** | 2.5 (2005) | try/finally acquire-release boilerplate |
| `singledispatch` | **PEP 443** | 3.4 (2014) | Generic functions; explicitly cited Visitor-style dispatch |
| Structural pattern matching | **PEP 634–636** | 3.10 (2021) | Destructuring and dispatch over shapes |
| `Protocol` | **PEP 544** | 3.8 (2019) | Static duck typing — **absorbs much of Interface Segregation** |

**The second part has no right answer and is marked on coherence.** Good arguments seen: effect
systems / structured concurrency absorbing the Circuit Breaker and Bulkhead family; an
`@immutable`-style guarantee absorbing Memento and Prototype; dependency injection at the language
level (as in some JVM languages) absorbing Factory. **Reject an answer that names a pattern without
saying what the syntax would be** — the question asks for both.

---

## Q5: The One You Did Not Do (10)

| | |
|---|---|
| 4 | A second smell, evidenced to Q1(a)'s standard |
| **4** | **The cost argument, both directions, plus a revisit trigger** |
| 2 | Recorded as a linked issue |

**The 4 marks require all four parts:** cost of fixing, cost of not fixing, what the time buys
instead, and **when you would revisit.** *"We ran out of time"* scores 0 — the paper says so.

**Full marks example:**

> We have `datetime.now()` in three domain functions, which means the hold-expiry test sleeps for
> two seconds. Fixing it means threading a clock through four call sites (~1 hour) and would cut the
> suite by 6 s. **Not fixing it costs 6 s per run × ~15 runs a week until May ≈ 25 minutes total**,
> which is less than the hour. **We will revisit when we add the expiry background job (issue #38),
> because that code cannot be tested at all without an injectable clock.** Recorded as #44, labelled
> `debt`.

**That is the standard**, and it is worth reading out to the cohort anonymised, because it shows the
arithmetic being done rather than asserted.

**The 2 marks for the issue are mechanical — check the tracker.** Week 11's debt register is built
from these and a student with nothing recorded has to start from zero.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Smell evidenced with counts. A non-pattern seriously considered and possibly chosen. File-count given both ways. Four or more commits. Consequences are specific costs. Q4(a) names what survives. Q5 has arithmetic and a trigger |
| **75–89** | Sound refactoring, green, well-argued. Description complete. Q4 correct. Q5 real but without the arithmetic |
| **60–74** | Correct pattern, asserted smell, generic consequences, one or two commits. Q5 is "no time" |
| **45–59** | Pattern applied without a smell. Tests silently changed. No second case sought |
| **< 45** | Broken tests, the pricing case reused, or a rename presented as a refactoring |

**Feedback note for every paper:** tell them whether you agree their smell was a smell. **Week 9 is
the formal treatment of exactly this judgement**, and a student who arrives having been told
*"this wasn't a smell, it was three lines of honest duplication"* gets far more out of it.

---

*CS 212 · Week 4 · A 4 Solutions · INSTRUCTOR ONLY*
