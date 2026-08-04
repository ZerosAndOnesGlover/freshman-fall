# PROG 102 · Lab 8 — Solutions and Checkoff Notes
## Building an Event System

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Project 1 is due Friday.** This lab is short and must finish inside the session. **Say so at the
start** and hold to it — budget A 35 min, B 40 min, C 20 min, D 10 min, 15 min slack.

**This is the first lab where students build rather than repair.** Expect the first twenty minutes to
be slower than usual while they get the `weak_ptr<void>` token idea. **Have the shape on the board:**

```cpp
struct Sub { std::weak_ptr<void> owner; Handler h; };
std::map<std::string, std::vector<Sub>> topics;
```

That is the whole design and giving it away costs nothing — Part A is worth 14 of 40 and the marks are
in B.

**The `weak_ptr<void>` is the part to explain out loud.** The subscriber passes a `shared_ptr` it
already owns — often `shared_from_this`, or a dedicated token — and the bus watches it without owning
anything. **The handler itself does not need to be a `shared_ptr`**, which means a lambda capturing
`this` works, and that is the common case.

---

## Part A — A Working Event System (14)

### A1 (8)

Reference implementation is the shape above, with `publish` doing lock-and-prune exactly as L25 §4.

**Why a `weak_ptr<void>` token beats requiring a `shared_ptr` handler:** the handler is usually a
lambda, which has no shared identity of its own. **The token lets the subscriber choose what controls
the subscription's lifetime** — typically the object whose method the lambda calls.

*Marking: 5 the implementation, 2 pruning, 1 the one-line justification.*

### A2 (6)

Reference:

```
count(news) before: 0
count(news) with both: 2
  A got first
  B got first
count(news) after B dies: 2  (stale)
  A got second
count(news) after publish: 1  (pruned)
publishing to an unknown topic: no error
```

*Marking: 4 the demonstration, 2 the three counts **including the stale one**. A student who reports 1
immediately after the death has either not measured or has an eager-cleanup design — if the latter,
ask how they detected the death, and award the marks if the answer is sound.*

---

## Part B — Break It (14)

### B1 (6) — re-entrancy

**(a)** Subscribing from inside `publish` mutates the vector being iterated. Under ASan this typically
surfaces as `heap-use-after-free` on the reallocated buffer. **Any reproducible failure earns the
marks** — with a small vector it may also silently "work", which is worth flagging as the nastier
outcome.

**(b)** The standard fix is to **notify over a copy** of the subscriber list, or to defer mutations to
a pending queue applied after the walk.

**The cost:** copying the list on every publish (a per-publish allocation), or the extra complexity and
subtle ordering questions of a deferred queue. **Both are real and the student must name one.**

*Marking: 3 + 3. **The fix must come with its cost**, as the sheet requires.*

### B2 (4) — unsubscribe during publish

Releasing your own token during notification. **A copy-based B1 fix already covers this**, because the
copy holds `weak_ptr`s and the walk is over the copy — the student should notice and say so.

*Marking: 2 the demonstration, 2 for correctly stating whether B1's fix covered it. **Both "yes" and
"no" can be right depending on their B1 fix** — mark the consistency with their own design.*

### B3 (4) — ordering

Two handlers whose combined effect depends on registration order.

**(2 of the 4) — the assessed half.** Both positions are defensible:

- **Guarantee registration order.** It is what everyone assumes, it is free to provide with a vector,
  and it makes behaviour reproducible. The cost is that you can never parallelise notification or
  reorder for efficiency.
- **Guarantee nothing, and document it.** Handlers that depend on each other's ordering are coupled in
  a way the pattern exists to prevent, and guaranteeing order makes that coupling permanent.

*Marking: 2 the demonstration, 2 for a committed position **with what they would document**. A student
who says "it depends" without committing gets 1 — the sheet demands a position.*

---

## Part C — Cost (8)

### C1 (5)

Times will vary. **What must be true: per-publish cost grows roughly linearly with subscriber count,
and per-notification cost is roughly flat** (with the fixed `map` lookup amortised away at 100
subscribers).

*Marking: 5 for both figures at all three counts. **Check they divided** — reporting only per-publish
misses the point of the second column.*

### C2 (3)

Expected substance:

> No, `std::function` is the right choice here. An event bus must store handlers of **different types**
> in one container, which a template parameter cannot do — that is exactly the case L26 §3.2 names.
> And the per-notification cost is dominated by whatever the handler does; the 1.85× from L26 applies
> to a comparison inside a sort's inner loop, not to a callback that touches a UI or writes a log.

*Marking: 3. **Full marks require both halves** — that a template parameter cannot express this, and
that the benchmark's context does not transfer. A student who says "yes it's the wrong choice, it's
slow" has applied the number without its conditions and gets 1.*

---

## Part D — Reflection (4)

### D1 (2)

Not reached: **cycles** (needs two buses or a self-publishing handler with a termination question) and
**threads** (Week 10 — they have no concurrency yet).

*Marking: 1 each with a reason.*

### D2 (2)

**"Always use a library" earns nothing without a reason.** The expected substance:

> Writing one is easy; the last 20% is what the library sells. But having built one, you now know
> *which* questions to ask of a library — what it guarantees about ordering, re-entrancy and exceptions
> — and those are usually answered in a paragraph of documentation most people skip.

*Marking: 2 for any argued position that engages with the specific bugs they found.*

---

## Checkoff Checklist

1. Part A prunes during publish; **no `detach`**, no `shared_ptr` handler requirement.
2. A2 reports the **stale** count.
3. B1's fix comes with a stated cost.
4. B3 commits to a position.
5. C1 reports **per-notification** as well as per-publish.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 14 |
| B | 14 |
| C | 8 |
| D | 4 |
| **Total** | **40** |

---

## Note for the Lab

Close on D2, and do not let the room settle on either glib answer.

> **You built a working, lifetime-safe event bus in about an hour, and then found three bugs in it in
> thirty minutes.** Two you fixed. One — ordering — does not have a right answer, only a documented
> one.

Then the useful conclusion:

> **"Use a library" is not the lesson.** The lesson is that you now know what to *ask* a library.
> Every event system you might use has made a choice about B3, and about what happens when a handler
> throws — **and you can go and find out which**, which is different from trusting it.

Finally, set up next week, because Lab 8 ends exactly where Week 9 starts:

> Your `publish` has no answer for a handler that throws. Right now the exception propagates out, the
> remaining subscribers are never notified, and the list is half-pruned. **Next week you will learn
> that this is not one of the three exception guarantees — it is the absence of all of them**, and you
> will have written it yourself.

---

*PROG 102 · Week 8 · Lab 8 Solutions · © CSE Department*
