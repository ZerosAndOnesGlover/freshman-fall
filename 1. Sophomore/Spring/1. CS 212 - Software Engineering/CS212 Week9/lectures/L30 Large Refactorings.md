# CS 212 · Software Engineering
## Week 9 · Lecture 3 of 3
### Large Refactorings — Branch by Abstraction, and the Strangler Fig

*“In the long run every program becomes rococo - then rubble.”* — Alan Perlis, "Epigrams on Programming" (1982), #14

---

**Sat:** Thursday of Week 9, 10:00–10:50, TH 200 · **Reading:** Fowler, *"BranchByAbstraction"* and *"StranglerFigApplication"* · **Next:** Week 10, API design

**Coursework:** 📝 **Assignment 8** due Fri this week 17:00 · 📊 **Quiz 10** Tue of Week 10 · 📝 **Assignment 10** released Wed of Week 10 17:00, due Fri of Week 11 17:00

---

## 1. The Problem: Some Changes Do Not Fit in a Commit

**Replacing `roomsvc`'s persistence layer. Splitting `bookings.py` into four modules. Moving from naked `datetime` to a `Slot` value object across 34 files.**

**These are refactorings — behaviour is preserved — and none of them fits in a reviewable commit.** Which leaves an apparent choice, and both options are bad:

| Option | Why it fails |
|---|---|
| **A long-lived branch** | Six weeks of semantic drift (W8 L25 §3); an unreviewable diff (W7 L22 §4); **a merge that is clean and wrong** |
| **One enormous commit** | Unreviewable, unrevertable, and if it breaks something you bisect by hand across 4,000 lines |

**The escape is that the choice is false.** Two techniques let a large restructuring proceed **entirely on `main`, with every intermediate state green and shippable.**

---

## 2. Branch by Abstraction

**For replacing a component that lives *inside* your system.** Six steps, and every one is a normal-sized commit.

**The example: `roomsvc` reaches the database through raw SQL scattered across `bookings.py`, and you want a repository.**

```
Step 1.  Introduce an abstraction over the current implementation.
         BookingRepo, with the methods the callers actually need --
         and nothing else. It delegates to the existing raw SQL.

Step 2.  Migrate callers to the abstraction, a few at a time.
         Each commit is small, green, and shippable. This is the
         longest step and it is entirely boring.

Step 3.  Build the new implementation behind the same abstraction.
         SqlAlchemyBookingRepo. Nothing calls it yet -- it is
         integrated, tested, and dead (W8 L25 section 3, technique 1).

Step 4.  Switch, one caller or one deployment at a time.
         A config flag, or a factory that returns one or the other.

Step 5.  Delete the old implementation.

Step 6.  Consider deleting the abstraction.
```

**Step 6 is the one everybody forgets, and it is a real decision.** Once the old implementation is gone, `BookingRepo` may have one implementation and no named second — **which is W2 L08 §7's test, and it may now fail.** Two defensible answers:

- **Keep it**, because the *test fake* is the second implementation (W3 L11 §2), and the seam buys you fast domain tests.
- **Delete it**, because you have a container-backed suite that is fast enough and the indirection costs a hop.

**Either is fine. Deciding by default is not**, and this is the kind of decision an ADR exists for.

> **Why this works at all is worth naming: step 1 is the only creative step.** Once the abstraction
> exists, steps 2–5 are mechanical, individually small, individually revertable, and can be done by
> different people in parallel — which is exactly the property a long-lived branch destroys.

**Two warnings from practice:**

1. **Step 1's abstraction must be shaped by the *callers*, not by the old implementation.** If `BookingRepo` grows a `raw_sql()` method to accommodate one awkward caller, the abstraction is a pass-through and steps 3–5 become impossible. **Fix the awkward caller first, as its own refactoring** (W3 L11 §2 warned about exactly this leak).
2. **Step 2 is where teams stall.** It is boring, it delivers nothing visible, and it is easy to leave half-done — **at which point you have two ways of reaching the database, indefinitely, which is worse than either.** Put a card on the board with a count: *"12 of 31 call sites migrated."* A visible denominator is what gets it finished.

---

## 3. The Strangler Fig

**For replacing a system from the *outside*** — which is what `slot` is doing to `roomsvc`, and the name is worth ten seconds. Fowler took it from the strangler figs of Australian rainforests: the fig germinates in the canopy, sends roots down around the host tree, and over years replaces it. **The host is load-bearing the whole time, until it is not needed at all.**

```
        ┌───────────┐
client →│   Facade  │
        └─────┬─────┘
        ┌─────┴─────┐
   ┌────▼────┐ ┌────▼─────┐
   │  slot   │ │ roomsvc  │
   │  (new)  │ │  (old)   │
   └─────────┘ └──────────┘
```

**The procedure:**

1. **Put a facade in front of the old system.** Nothing changes behaviour; every request still reaches `roomsvc`.
2. **Implement one capability in the new system.** Route just that capability to `slot`.
3. **Repeat**, capability by capability, in order of value or of risk.
4. **When nothing routes to the old system, delete it.**

**What makes it work, and what makes it hard:**

| Property | |
|---|---|
| **Value arrives early** | The first capability is live in weeks, not after a two-year rewrite |
| **Risk is per-capability** | If `slot`'s booking endpoint is wrong, you route it back. **The rollback is a routing change** |
| **The old system keeps working** | Which is why this is used in anger, where a rewrite cannot be |
| **⚠️ Data is the hard part** | **Both systems must see the same bookings.** This is the whole difficulty |

**The data problem, honestly, because glossy accounts of this pattern omit it:**

| Approach | Cost |
|---|---|
| **Shared database** | Simplest, and both systems are coupled to one schema — so neither can evolve it freely |
| **Replication, old → new** | New is read-only for that data until cutover. **Often the right first step** |
| **Bidirectional sync** | **Two writers, one truth, no transaction between them.** Conflict resolution, which is a distributed-systems problem (CS 202's Week 11) |
| **Capability-partitioned data** | Cleanest — each system owns its tables — **and only possible if the capabilities partition, which for a booking system they mostly do not** |

> **This is why "we'll rewrite it incrementally" is easy to say.** The code is the easy half. **Two
> systems agreeing about the same booking, with no shared transaction, is the hard half** — and it is
> the same bill L12 itemised for microservices, arriving in a migration.

**For `slot` this is contextual, not required.** Your project is a greenfield replacement and you are not asked to run both. **What you should be able to do is say, in the final viva, what the real migration would require** — and the honest answer includes a period of dual writes and a plan for what happens when they disagree.

---

## 4. Parallel Run: Verifying a Replacement

**A technique that fits both patterns and is under-used.** When you have two implementations of the same behaviour, **run both and compare, in production, before you trust the new one.**

```python
def price_for(booking):
    old = legacy_price(booking)
    if settings.PRICING_PARALLEL_RUN:
        try:
            new = policy_for(booking.kind).price(booking)
            if new != old:
                log.warning("pricing_mismatch", kind=booking.kind,
                            hours=booking.hours, old=str(old), new=str(new))
        except Exception:
            log.exception("pricing_new_raised")     # never let the new path break the old
    return old                                       # old is still authoritative
```

**Three properties make this powerful:**

- **It is tested against real inputs**, which are more various and stranger than anything you would generate. **`roomsvc` has 2,847 commits' worth of accumulated special cases, and a parallel run finds the ones nobody documented.**
- **The mismatches are a specification.** Each one is either a bug in the new code or an undocumented behaviour in the old — and **both are findings you could not get any other way.**
- **The blast radius is zero**, because the old path remains authoritative and the new path's exceptions are swallowed.

**Its cost:** you run both, so it is slower and it writes log volume. **Time-box it** — two weeks, then decide — and **remove the flag when you do** (W8 L25 §3's rule, and Knight Capital's lesson).

**This is W6 L20 §3's oracle property, moved from the test suite into production.** Same idea, different venue.

---

## 5. Choosing Between Them

| | Branch by abstraction | Strangler fig |
|---|---|---|
| **Replacing** | A component inside one system | A whole system, from outside |
| **Seam** | An interface in your code | A facade in front of the system |
| **Granularity** | A call site | A capability |
| **Rollback** | Revert a commit, or flip a flag | A routing change |
| **Hard part** | Step 2's boring migration | **The data** |
| **Use for `slot`** | Yes — plausibly this fortnight | Contextual; know it for the viva |

**And the option that is not on the table:**

> **A rewrite.** Joel Spolsky's *"Things You Should Never Do, Part I"* (2000) on Netscape's decision to
> rewrite Navigator from scratch is still the best short statement of why: **you throw away the
> accumulated knowledge of every bug fixed**, you ship nothing for the duration, and **the new system
> acquires its own bugs from zero.** Netscape shipped nothing for three years and lost the market.
>
> **The honest caveat:** rewrites do sometimes succeed, usually when the old system's *requirements*
> have changed beyond recognition rather than merely its code being bad. **The test is whether you are
> replacing an implementation or replacing a product.** If it is the implementation, strangle it.

---

## 6. What to Do on Your Project

A 9 asks for a real refactoring. **Choose by looking, not by taste.**

1. **Find the hotspot.** `git log --since='6 weeks ago' --name-only --format='' | sort | uniq -c | sort -rn | head`. **Your most-changed file is where refactoring pays** — this is W11's method arriving early, and it is one command.
2. **Cross it with complexity.** `radon cc -s -n C src/`. **The intersection of most-changed and most-complex is the one place worth restructuring**, and it is usually one file.
3. **Characterise before you touch it** (L28 §3), and run coverage over the characterisation tests to see what you have not pinned.
4. **Wear one hat.** Commit `test:` then `refactor:`, never together.
5. **If it does not fit in a commit, use branch by abstraction** — and put the denominator on the board.
6. **Ask the concurrency question of your own refactoring** (L28 §6): *can two of these run at once, and have I just moved something out of a critical section?*

---

## 7. Summary

- **Some refactorings do not fit in a commit**, and the apparent choice — a long-lived branch or one enormous commit — is a false one. **Both techniques keep every intermediate state on `main`, green and shippable.**
- **Branch by abstraction, six steps:** introduce the abstraction over the *old* implementation, migrate callers, build the new one behind it, switch, delete the old, **and decide about the abstraction** — which may now fail the second-implementation test, with the test fake as the defensible answer.
- **Step 1 is the only creative step**; 2–5 are mechanical, revertable and parallelisable. **Step 1's shape must come from the callers**, or the abstraction becomes a pass-through. **Step 2 is where teams stall — put a visible denominator on the board.**
- **The strangler fig replaces a system from outside**: a facade, then capability by capability, then delete. Value arrives early and **rollback is a routing change** — **but the data is the hard part**, and two writers with no shared transaction is a distributed-systems problem, not a refactoring one.
- **Parallel run** puts W6's oracle in production: run both, compare, log mismatches, keep the old authoritative. **The mismatches are a specification**, and real inputs are stranger than generated ones. **Time-box it and delete the flag.**
- **A rewrite throws away every bug you ever fixed.** The test is whether you are replacing an implementation or a product; if it is the implementation, strangle it.
- **Choose your target by looking**: most-changed × most-complex, one command each. **Characterise, wear one hat, and ask whether you just moved something out of a critical section.**

**Next:** Week 10 — API design, where "observable behaviour" stops meaning *your* tests and starts meaning *other people's code* — and where expand-and-contract returns as a versioning strategy.

---

*CS 212 · Week 9 · L30 · © CSE Department*
