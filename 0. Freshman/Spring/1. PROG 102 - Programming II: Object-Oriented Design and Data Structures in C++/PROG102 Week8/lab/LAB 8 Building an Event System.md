# PROG 102 · Lab 8
## Building an Event System

**Date:** Monday 22 March 2027 · 15:00–16:50 · Lab section (Week 9) — covers Week 8 (L25–L27)
*2-hour lab · 40 points · in-lab checkoff · part of the Labs component (20%)*
**Deliverable:** `events.hpp`, `RESULTS.md`. In-lab checkoff.

> **Project 1 is due Friday.** This lab is short by design. **Finish it in the session.**

---

## Purpose

Lecture 25 §6 listed five problems the Observer pattern does not solve: ordering, re-entrancy,
exceptions, cycles and threads.

**You are going to hit three of them in ninety minutes**, in the order they hit real event systems,
and fix two.

This is the first lab where you build something from an interface rather than repairing something
given to you. **The bugs are ones you will introduce yourself**, which is the point.

---

## Part A — A Working Event System (14 pts)

**A1.** *(8)* Build `EventBus`:

```cpp
class EventBus {
public:
    using Handler = std::function<void(const std::string&)>;
    void subscribe(const std::string& topic, std::weak_ptr<void> owner, Handler h);
    void publish(const std::string& topic, const std::string& payload);
    std::size_t subscriber_count(const std::string& topic) const;
};
```

Requirements:

- several subscribers per topic;
- **a subscriber whose `owner` has expired is skipped and pruned**, exactly as in L25 §4;
- publishing to a topic with no subscribers is not an error.

**The `weak_ptr<void>` is a lifetime token** — the subscriber passes a `shared_ptr` it owns, and when
that dies the subscription dies with it. **In one line, say why this is better than requiring the
handler itself to be a `shared_ptr`.**

**A2.** *(6)* Demonstrate: three subscribers on two topics, one of which goes out of scope. Show that
publishing after the death notifies the survivors, prunes the dead entry, and is sanitizer-clean.

**Report `subscriber_count` before the death, after it, and after the next publish.**

---

## Part B — Break It (14 pts)

Each of these is a real bug in real event systems. **Demonstrate each, then fix the ones marked
"fix".**

**B1.** *(6)* **Re-entrancy — fix.** Write a handler that calls `subscribe` on the same topic from
inside `publish`.

- **(a)** *(3)* Show what happens. Run under `-fsanitize=address` and paste the report.
- **(b)** *(3)* Fix it. **State what your fix costs**, and confirm the original demonstration now
  passes.

**B2.** *(4)* **Unsubscribe during publish — fix.** A handler that causes its *own* owner to be
released during notification.

Show the problem, fix it, and **say whether your B1 fix already covered this.**

**B3.** *(4)* **Ordering — do not fix.** Construct two handlers where the result depends on which was
registered first. Show both orders producing different output.

**Then answer:** *(2 of the 4)* Should `EventBus` guarantee an order? Argue either way in three
sentences — **but commit to a position and say what you would document.**

---

## Part C — Cost (8 pts)

**C1.** *(5)* Measure `publish` with 1, 10 and 100 subscribers on a topic, over at least 100,000
publishes.

Report **per-publish** and **per-subscriber-notification** times.

**C2.** *(3)* Your handlers are `std::function`. From L26 §3, that is the slowest of the four ways to
hold a callable.

**Is that the wrong choice here?** Answer in three sentences, referring to your C1 numbers and to what
an event bus must be able to do.

---

## Part D — Reflection (4 pts)

**D1.** *(2)* Of Lecture 25 §6's five unsolved problems, you met three. **Name the two you did not**,
and say in one sentence each why this lab could not reach them.

**D2.** *(2)* You wrote an event system in ninety minutes and found three bugs in it.

**In two sentences: what does that suggest about using a library event system instead?** An answer of
"always use a library" earns nothing without a reason.

---

## Submission

- `events.hpp` and your demo.
- `RESULTS.md` — every transcript in order, the C1 table, and all written answers.
- Machine, OS, compiler version at the top.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 14 | A working, lifetime-safe event bus |
| B | 14 | Three real bugs; two fixed |
| C | 8 | What it costs, and whether that matters |
| D | 4 | What the exercise implies |
| **Total** | **40** | |

---

## Reference Behaviour

From Lecture 25 §4, the shape your Part A should reproduce:

```
observers registered: 2
temp saw 1
alive saw 1
after temp dies, registered: 2
alive saw 42
after notify (pruned):     1
```

**Note the middle line: the count is 2 after the death and 1 only after the next notification.** That
staleness is correct and expected, and A2 asks you to report it.

---

## What This Lab Is Really Showing

**Part D2 is the question, and the glib answer is wrong in both directions.**

You built a working event bus in about an hour. It is not a toy — lifetime-safe subscriptions with
`weak_ptr` tokens is what real systems do. And in the next thirty minutes you found three bugs in it,
two of which you could fix and one of which does not have a right answer.

**"Always use a library" is not the lesson**, because you now know something you could not have learned
by using one: an event system that does not document its ordering guarantee has not solved ordering,
it has left it to you. Every library you might use instead has made a choice about B3, and **you can
now go and find out which** — which is a different skill from being told to trust it.

**The honest version:** writing one is easy, and getting the last 20% right — re-entrancy, ordering,
exception behaviour under load, thread safety — is what the library actually sells you. **You have just
built the easy 80% and met the boundary.**

That boundary is where Week 9 starts. Your `publish` currently has no answer for a handler that
throws, and after next week you will know exactly which guarantee you failed to provide.

---

*PROG 102 · Week 8 · Lab 8 · © CSE Department*
