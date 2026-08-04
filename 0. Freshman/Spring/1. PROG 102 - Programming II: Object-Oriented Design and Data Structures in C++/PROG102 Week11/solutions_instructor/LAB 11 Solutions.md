# PROG 102 · Lab 11 — Solutions and Checkoff Notes
## Profiling Lambda Overhead

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Project 2 is due next Friday and the final is that week.** Keep this inside the session. Budget
A 35 min, B 30 min, C 30 min, D 10 min, 15 min slack.

**Part A1 is designed to fail.** Students write the obvious benchmark, two of the three versions report
0.00 ns, and they must diagnose it. **Do not warn them in advance** — the sheet already tells them it
will happen, and the value is in recognising the shape.

**When someone puts their hand up with "my lambda is infinitely fast":** ask what the loop body depends
on. That is the whole hint.

**This is the fourth self-deleting benchmark of the course** — Week 2's instantiations, Week 5's leaked
allocation, Week 10's hoisted counter, and now this. **Say that at the end**, not the start.

---

## Part A — Three Ways to Call (14)

### A1 (5)

First attempt, constant arguments:

```
lambda    0.0 ms (0.000 ns) | std::function  441.1 ms (2.206 ns) | fn ptr    0.0 ms (0.000 ns)
```

**(a)** The lambda and the function pointer vanished.

**(b)** **The `std::function` survived because the compiler cannot see through the type erasure.** It
does not know what the call does, so it cannot prove the loop's result is loop-invariant, so it cannot
hoist. The lambda's body is visible and the function pointer's target is a known constant, so both
were folded away.

*Marking: 2 the failed transcript, 3 the explanation. **Full marks require the "cannot see through it"
step.** "std::function is slower so it took longer" gets 1 — the other two took **zero**, which is not
a speed difference.*

### A2 (6)

| run | lambda | fn pointer | `std::function` |
| --- | --- | --- | --- |
| 1 | 0.667 ns | 1.507 ns | 2.205 ns |
| 2 | 0.610 ns | 1.499 ns | 2.153 ns |
| 3 | 0.606 ns | 1.539 ns | 2.209 ns |

*Marking: 4 the three measurements, 2 stating the fix. **Accept any technique** — indexing a data
array, using the loop counter, `volatile` inputs — provided all three are non-zero.*

### A3 (3)

Ratios ≈ **2.4×** and **3.5×**.

**Why the function pointer is in the middle:** it is one indirect call — the target is unknown at
compile time so it cannot be inlined, but the call itself is direct-to-address. **`std::function` adds
the erasure layer on top**: a call through the stored operation table to a wrapper, which then calls
the target.

*Marking: 1 the ratios, 2 the explanation. Must distinguish "one indirection" from "two".*

---

## Part B — The Hidden Allocation (12)

### B1 (6)

```
sizeof(std::function<int()>) = 32
capture  16 bytes -> allocations 0
capture  17 bytes -> allocations 1   <- HEAP
```

**Threshold: 16 bytes.**

*Marking: 4 the threshold found by sweeping, 2 the `sizeof`. **Any threshold is acceptable** —
implementation-defined. A student who looked it up rather than measuring gets 2.*

### B2 (3)

`std::string` by value = 32 bytes → **allocates**. By reference = 8 bytes → **does not**.

**The risk:** the by-reference version dangles if the `std::function` outlives the string.

*Marking: 2 the measurements, 1 the risk. **The risk is the point** — students reach for the reference
capture as an optimisation and reintroduce L34 §3's bug.*

### B3 (3)

Five lambdas of varying size; the total is the count of those exceeding 16 bytes.

**Reducing it:** capture less (pointers or indices instead of objects), capture by reference **where
lifetime allows**, or avoid `std::function` entirely by templating the consumer.

*Marking: 2 the count, 1 a sensible reduction.*

---

## Part C — Does It Matter? (10)

### C1 (6)

Inside a real sort of 10⁶ elements the ratio is much smaller than 3.5× — **Week 8's figure was 1.85×**
on 2,000,000 ints (lambda 160 ms, `std::function` 296 ms).

*Marking: 6 for both measurements at a realistic size. **Accept any ratio between about 1.2× and
2.5×** depending on element type and comparison cost.*

### C2 (4) — the assessed question

**(a)** Roughly **3.5×** per call, roughly **1.85×** inside the sort.

**(b)** Expected substance:

> Both are correct. Per call, the erasure is essentially all of the cost. Inside a sort, the comparison
> shares the body with swaps, moves and memory traffic, so the same absolute overhead is a smaller
> fraction. **The number to quote a colleague is the one with the denominator they care about** — "it
> costs 1.85× of your sort" is actionable; "3.5×" invites rewriting code that was fine.

*Marking: 2 + 2. **A student who says one measurement is "more accurate" has missed it** — they measure
different things and both are exact.*

---

## Part D — The Rule (4)

### D1 (2)

Any rule derived from their numbers. Expected: **not in a hot loop, and not as a parameter type for
something you could template.**

### D2 (2)

Must be specific and from their own code. **The strongest answer is Week 8's event bus or Project 1's
callback registry** — a container of callables of different types, which no template parameter can
express.

*Marking: 2 + 2. **A generic "when you need flexibility" gets 1.***

---

## Checkoff Checklist

1. A1's **failed** benchmark is reported, not silently fixed.
2. A2 has all three non-zero and states the fix.
3. B1's threshold was **measured**, not looked up.
4. B2 names the dangling risk.
5. C2 keeps both ratios and picks one to quote, with a reason.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 14 |
| B | 12 |
| C | 10 |
| D | 4 |
| **Total** | **40** |

---

## Note for the Lab

Close on C2, because it is the course's argument in its last measurable form.

> **You have two correct numbers for the same overhead: 3.5× and 1.85×.** Which one you say out loud
> determines whether a colleague spends a day rewriting code that was fine.

Then the general form:

> **A ratio with no denominator is not an answer.** "`std::function` is 3.5× slower" is true and
> useless. "`std::function` costs about 1.5 ns per call, which is 1.85× of your sort's time and
> probably 0.1% of your program" is the same measurement and a different conversation.

And the fourth-time observation, which should get a laugh and then land:

> **Part A is the fourth benchmark this course has deleted out from under you.** Week 2's
> instantiations, Week 5's leaked allocation, Week 10's hoisted counter, and today. By now the reflex
> should be automatic: **a suspiciously good number means read the assembly, not celebrate.**

If there is time, connect forward — it is one week away:

> Next week you will measure a cache miss at roughly **100 nanoseconds**. Today's lambda call was
> **0.6**. **Hold both numbers in your head over the weekend** and ask which one your program is
> actually spending its time on.

---

*PROG 102 · Week 11 · Lab 11 Solutions · © CSE Department*
