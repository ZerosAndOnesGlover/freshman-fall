# PROG 102 · Lab 9 — Solutions and Checkoff Notes
## Testing for Failure

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Project 1 is due today.** Expect a distracted room. This lab is short and its Part C/D is *directly*
Project 1 Part 3.3 — **say that at the start**, because it converts the lab from a competing demand
into help.

**On the framework.** The curriculum names Catch2 and it is not installed on the reference machine.
Lab 9 ships a minimal Catch2-compatible header, verified clean under `-Wall -Wextra -pedantic`.

**Be straight with students about this.** The fallback has no tags, no matchers, no filtering, no BDD
syntax and no generators. **It is enough for this lab and no more.** Anyone with Catch2 should use it,
and their `tests.cpp` should be identical either way — the spellings match deliberately.

**Budget:** A 25 min, B 25 min, C 40 min, D 15 min, 15 min slack. **Part C is the substance and
students always underestimate the sweep.**

---

## Part A — A Test Suite That Can Fail (10)

### A1 (4)

Eight test cases with real coverage.

*Marking: 4. **Check the assertions are non-trivial** — `REQUIRE(true)` and `REQUIRE(v.size() ==
v.size())` appear more often than you would hope.*

### A2 (3) — the assessed idea

A deliberately broken assertion, with the framework reporting file, line and expression:

```
a deliberate failure, to prove failures are reported
  FAILED: 1 == 2
    at selftest.cpp:18
  FAILED (2 assertions)

2/3 test cases passed, 1 assertion failures
```

*Marking: 3. **Require the transcript**, not a claim. A student who skipped this has not demonstrated
their suite can detect anything.*

### A3 (3)

Exit 1 on failure, 0 on pass.

**Why it matters:** a build script, CI system or `make check` decides pass/fail on the exit code. **A
suite that prints "FAILED" and exits 0 is invisible to automation** and will be ignored for months.

*Marking: 2 the demonstration, 1 the reason. The reason must mention automation.*

---

## Part B — Testing the Error Paths (12)

### B1 (6)

Four documented error behaviours with the contract stated **before** the test.

*Marking: 6, 1.5 each. **Deduct where the contract is stated after the fact** — "it throws
`out_of_range`" written by reading their own code is not a contract, it is an observation.*

### B2 (6) — the assessed question

**There is always at least one.** The most common honest answers:

- **What happens if an element's copy constructor throws during `insert`?** Almost nobody has decided.
- **What does the destructor do if an element's destructor throws?** Undefined in most student code.
- **Is `operator[]` on an empty container UB or checked?** Often neither documented nor consistent.
- **What is the state of a moved-from container?** Week 5 §L18 §4.1's question, usually unanswered.

**Bug or undocumented decision?** Both answers are defensible: *undocumented decision* if the behaviour
is sane and merely unstated; *bug* if the behaviour is inconsistent or leaves an invariant broken.

*Marking: 3 the identified gap and the test they would write, 3 the judgement with justification.
**"There isn't one" gets 0** and should be met with "what does your destructor do if an element
throws?"*

---

## Part C — The Throwing Element (12)

### C1 (6)

```cpp
struct Fragile {
    static int throw_on_copy;
    Fragile(const Fragile& o) : v(o.v) {
        if (throw_on_copy && --throw_on_copy == 0) throw std::runtime_error("copy failed");
    }
};
```

with a test that arms it and requires the third copy to throw.

*Marking: 4 the type, 2 verifying it **before** using it. **An unverified instrument invalidates Part
C** — if their `Fragile` is off by one, every conclusion shifts.*

### C2 (6)

The sweep. Reference shape:

| n | before | after | guarantee at n |
| --- | --- | --- | --- |
| 1 | 2 | 2 | strong |
| 2 | 2 | 3 | basic |
| 3 | 2 | 4 | basic |

*Marking: 6. **The sweep across every n is the whole exercise.** A student who armed the failure once
gets 2 — they have a data point, not a table.*

**Watch for students who cannot find more than one failure point.** Usually their operation copies once
(e.g. `push_back` of a single element), in which case the sweep is trivially short — **that is fine**,
and they should say so and pick a second operation that copies several times.

---

## Part D — What You Actually Provide (6)

### D1 (4)

**The weakest observed, not the best.**

*Marking: 2 the correct conclusion from their table, 2 the comparison with their prior. **A student
whose table shows basic at n=3 and who concludes "strong" gets 0 of the first 2**, and this is the
most important correction in the lab.*

**Award the prior marks for a wrong prior honestly reported.** That is the point of asking.

### D2 (2)

Copy, do the risky work on the copy, commit with a `noexcept` swap. **Cost: an $O(n)$ copy and $O(n)$
peak memory for an operation that was $O(k)$.**

*Marking: 2. Both the method and the cost required.*

---

## Checkoff Checklist

1. A2's deliberately-broken transcript is present.
2. A3 confirms the exit code.
3. `Fragile` verified **before** being used to conclude anything.
4. C2 sweeps **every** failure point.
5. D1 reports the **weakest** observed guarantee.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 10 |
| B | 12 |
| C | 12 |
| D | 6 |
| **Total** | **40** |

---

## Note for the Lab

Two things, and the first takes thirty seconds.

> **Part A2 asked you to break a test on purpose.** A suite that has never failed is not evidence of
> anything — it might be asserting something always true, or running a test case that is never
> registered. **The only way to know your tests can see a problem is to give them one.**

Then the real one, which is Part D1:

> **The guarantee is the weakest you observed, not the best.** An operation that is strong when the
> first copy fails and basic when the third does **provides basic**.

Push on why that is tempting to get wrong: the first failure point is the one everybody tests, it is
usually the cleanest case, and it gives the flattering answer. **Reporting it is not dishonesty; it is
stopping too early**, which is the same failure this course has met in Lab 2 (no control), Lab 3 (the
wrong question) and Week 4 (three benchmarks before the right one).

And close by connecting it forward, because it is due today:

> **Project 1 Part 3.3 asks which guarantee your container provides.** You now have the method, and
> "the weakest observed" is the standard you are being marked against. If you wrote "strong" in your
> `DESIGN.md` this morning without a sweep, you have an hour to check.

---

*PROG 102 · Week 9 · Lab 9 Solutions · © CSE Department*
