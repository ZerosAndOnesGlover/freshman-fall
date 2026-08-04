# PROG 102 · Problem Set 9 — Solutions and Marking Notes
## Making a Container Exception-Safe

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux. Code sizes and structural results are exact;
timings are not.

**This set is due in Midterm 2 week and is the best revision for it.** Expect students to have done it
early or not at all. **Mark Part B thoroughly** — it is 30 points, it is the week's real skill, and it
is what Project 1 Part 3.3 needed.

---

## Part A — What Exceptions Cost (20)

### A1 (8)

| | ns/call | text |
| --- | --- | --- |
| with exceptions | 1.53–1.66 | **240 bytes** |
| `-fno-exceptions` | 1.49–1.60 | **88 bytes** |

*Marking: 5 the timings with three runs and functions in a separate TU, 3 the `size` output for both.*

**A student whose timings differ by more than ~10% should check that their function was not inlined** —
the whole point of the separate TU. **A student reporting 0.00 ms has had the loop deleted** (Week 5
§L16 §5.4) and should be sent back.

### A2 (4)

**~1.68 µs per throw**, roughly **1000×** a normal call.

*Marking: 3 the measurement, 1 expressing it as a multiple **of their own measured call cost**.*

### A3 (8)

**(a)** **Supported:** the time on the happy path is indistinguishable. **Refuted:** code size is 2.7×.
"Zero-cost" means zero *time* cost when nothing throws, and the slogan drops the qualifier.

**(b)** Any rule derived from the numbers. The expected form: **a failure that happens once per program
run costs 1.68 µs and is free; a failure that happens per element costs 1.68 µs × n and is
catastrophic.** So: exceptions for exceptional conditions, return values for expected ones.

**(c)** It compared **two different APIs** — different signatures, different work (an out-parameter, a
return code) — not the same code with and without exception support. It measured the cost of an API
style, not of the exception mechanism.

*Marking: 3 + 3 + 2. **(c) is the assessed idea** and it is Week 4's lesson restated: a benchmark
answers the question its design encodes, not the question you asked. "It wasn't a fair comparison" is
1 of the 2 — say **why** it was unfair.*

---

## Part B — Determining Your Guarantee (30)

### B1 (8)

`Fragile` with a static `throw_on_copy` counter and a static live count.

*Marking: 5 the implementation, 3 the verification test. **A student who did not verify `Fragile`
itself before using it** has built their whole Part B on an untested instrument — deduct 3 and say so.*

### B2 (14)

Reference shape, for a container of 2 receiving 4 elements:

| n | before | after | leaked | guarantee at n |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | no | strong |
| 2 | 2 | 3 | no | basic |
| 3 | 2 | 4 | no | basic |
| … | | | | |

*Marking: 14 — roughly 4 per operation plus 2 for sweeping rather than testing a single failure point.*

**The sweep is the assessed method.** A student who armed the failure only at *n* = 1 will report
"strong" for an operation that is basic, and that is exactly the error B3(a) exists to catch. **Deduct
6 if there is no sweep**, regardless of how good the rest is.

**Leak checking is required.** Basic requires *no leaks*, and a student who never checked has not
demonstrated basic — they have demonstrated "did not crash".

### B3 (8)

**(a) (4)** The guarantee is the **weakest observed**. An operation strong at *n*=1 and basic at *n*=3
**provides basic.**

**(b) (4)** Any honest report. **Award full marks for a wrong prior honestly reported** — that is the
point of asking. For a student right on all three, the answer to "how would you be sure rather than
lucky" is: test more operations, more element types, and failure points in allocation as well as in
copying.

*Marking: 4 + 4. **A student reporting the best case as their guarantee gets 0 of the first 4**, even
if their table is perfect — the table is the evidence and the conclusion contradicts it.*

---

## Part C — Upgrading to Strong (26)

### C1 (10)

Copy, do the risky work on the copy, `swap` to commit. The re-run sweep must show **strong at every
n**.

*Marking: 6 the implementation, 4 the re-run sweep. **A "strong" version whose commit step can throw is
not strong** — check their `swap` is `noexcept`.*

### C2 (8)

Time and peak memory before and after. **The expected shape: roughly $O(n)$ time and $O(n)$ additional
memory for an operation that was $O(k)$.**

*Marking: 8 for both metrics measured. Accept any reasonable memory measurement — a counted allocator,
`/usr/bin/time -v`, or an instrumented `operator new`.*

### C3 (8)

**(a) (4)** `push_back` appends one element at the end; rolling back means removing it, which is cheap
and needs no copy. Middle `insert` shifts every subsequent element; rolling that back would require
having copied the container first — **exactly the C2 cost they just measured**, on every insert.

**(b) (4)** Any operation in a hot loop where an $O(n)$ copy per call would dominate. **The
justification must reference their C2 numbers.**

*Marking: 4 + 4. **(a) must connect to their own measurement**, not restate the rule.*

---

## Part D — `noexcept` and Contracts (24)

### D1 (6)

```
warning: 'throw' will always call 'terminate' [-Wterminate]
terminate called after throwing an instance of 'std::runtime_error'
Aborted (core dumped)          exit 134
```

**The `catch (...)` does not run.**

*Marking: 3 the warning and runtime output, 3 for confirming the catch was skipped **and explaining
that there is no unwinding**.*

### D2 (6)

Without `noexcept`, `vector` growth **copies**; with it, it **moves**.

**What a missing `noexcept` costs:** silently, the entire benefit of move semantics in the place it
matters most — and nothing warns.

*Marking: 4 the counts both ways, 2 the sentence.*

### D3 (6)

1. **Assertion** — a private helper's index is a bug; no correct caller can trigger it.
2. **Exception** — a file may legitimately be malformed; the world, not the program.
3. **Either, defensibly.** Exception if it is public API taking user input; assertion if it is internal.
   **Mark the justification, not the choice.**
4. **Assertion** — an invariant is a claim about your own code.
5. **Exception** — the network is the world.

*Marking: 1.2 each. **Item 3 is deliberately ambiguous**; a student who notices and argues both ways
should get full marks for it.*

### D4 (6)

Every public function with precondition, postcondition and guarantee.

**The second half is the assessed part.** Common honest answers for "a contract I could not state
cleanly": a function that both mutates and returns; one whose behaviour on an empty container was never
decided; a destructor whose behaviour when an element throws is undefined; an operation whose guarantee
depends on `T` and was never parameterised.

*Marking: 4 the contracts, 2 the reflection. **"I could state them all" gets 0 of the 2** — the question
presumes there is one, and there always is.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 20 |
| B | 30 |
| C | 26 |
| D | 24 |
| **Total** | **100** |

---

## What to Watch For

1. **No sweep in B2.** The single most common failure, and it produces a wrong answer that looks right.
2. **Reporting the best-case guarantee** in B3(a), contradicting their own table.
3. **No leak check** — "did not crash" is not the basic guarantee.
4. **A throwing commit step** in C1.
5. **"It wasn't fair"** as the whole of A3(c).
6. **"I could state every contract"** in D4.

---

## Feeding Into Week 10 and Midterm 2

**Midterm 2 covers Weeks 5–9** and this problem set is the best available revision for its last third.
**Say so on Monday.**

For Week 10, the connection to draw is uncomfortable and worth stating: **everything in this problem
set assumed one thread.** An exception escaping a thread's function calls `std::terminate` immediately
— there is no caller to unwind to. The strong guarantee's "commit with a `noexcept` swap" assumes no
other thread is reading during the swap.

**Week 10 does not extend this week's material; it invalidates parts of it**, and students should
arrive expecting that.

---

*PROG 102 · Week 9 · PS 9 Solutions · © CSE Department*
