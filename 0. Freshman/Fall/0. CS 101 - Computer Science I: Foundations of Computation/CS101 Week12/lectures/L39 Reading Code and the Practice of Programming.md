# CS 101 · Lecture 39 (Week 12, Lecture 3)
## Reading Code, and the Practice of Programming

---

## 0. The Last Lecture

Every program you wrote this term, you wrote from scratch, to a specification someone else had
already made unambiguous, in a codebase built specifically to teach you one thing.

You will almost never do that again.

Professional programming is mostly **reading**: understanding code you did not write, that does more
than you need, whose author is unavailable, and whose reasons are not recorded. This lecture is
about that skill, and about the judgement that surrounds it.

It is the one part of the course with no problem set. That does not make it the least important.

---

## 1. Reading Is the Majority of the Work

The commonly cited ratio is ten parts reading to one part writing. Whatever the true number, the
direction is not in dispute, and the reason is structural: any line you write, you and others will
read many times — when debugging it, when extending it, when deciding whether it can be deleted.

Yet reading is almost never taught. You were taught to write essays *and* to read them; in
programming, the second half usually gets skipped.

### Why unfamiliar code is hard

Not because it is bad. Because you lack three things the author had:

1. **The problem context** — what was actually required, including the awkward requirement that
   explains the awkward code
2. **The history** — what was tried before and failed
3. **The constraints** — the deadline, the legacy system, the library version, the bug being worked
   around

Code records *what*, weakly records *how*, and almost never records *why*. Most of reading is
reconstructing the why.

---

## 2. A Method

When you meet an unfamiliar codebase, do not start at line 1 of the largest file.

**1. Run it first.** Before reading anything, make it work. What does it print? What files does it
touch? Behaviour you have observed is worth more than behaviour you have inferred.

**2. Find the entry point.** `main`, the CLI parser, the route handler, the test suite. Read
outward from where control actually enters.

**3. Read the data structures before the functions.** This is the highest-leverage habit in the
lecture, and it is Thread 1 from L37. The shape of the data constrains everything that can be done
to it. A `dict` keyed by user ID tells you lookups are by ID and ordering was not wanted. Ten
functions become predictable once you know the structure they operate on.

**4. Read the tests.** Tests are executable documentation that cannot silently go stale. They tell
you what the author believed mattered, and they often encode edge cases the prose never mentions.

**5. Follow one path all the way down.** Pick a single realistic input and trace it end to end,
ignoring everything it does not touch. One complete path beats a shallow impression of the whole.

**6. Change something and see what breaks.** Rename a variable, add an assertion, break a function
deliberately. What fails tells you what depended on it — you are probing the system, not just
reading it.

**7. Write down what you learn.** Your understanding at hour three is not recoverable at hour thirty.

---

## 3. Reading Strange Code Charitably

You will meet code that looks wrong. Some of it is. Much of it is a repair whose reason has been
forgotten.

> **Chesterton's Fence.** Coming across a fence in a field, do not tear it down until you know why
> it was put there.

The programming version:

```python
# Retry once before failing. Do not remove.
if not result:
    time.sleep(0.1)
    result = fetch()
```

That is ugly. It is also almost certainly a scar: someone was woken at 3 a.m. by an intermittent
failure and this stopped it. Deleting it because it offends you re-creates the outage.

**The rule:** understand why code exists before removing it. If you cannot find the reason, that is
information about the codebase's documentation, not licence to proceed.

**The counter-rule, which matters equally:** a fence whose reason you *have* established as obsolete
should come down. Chesterton's Fence is an argument for investigation, not for paralysis. Code that
nobody dares touch is its own serious problem.

### On "bad" code

Before concluding that code is bad, ask:

- Was it written under a deadline you did not have?
- Does it handle a case you have not thought of?
- Was it correct for a version of the requirements you have not read?
- Is it *ugly* — or is it actually *wrong*? These are different, and only one is urgent.

You will write code that a stranger later finds baffling, for exactly these reasons.

---

## 4. Writing for the Next Reader

The other half. Every convention this term had a reader in mind.

**Names carry the most information per character.** `n` in a three-line loop is fine; `n` as a
module-level variable is theft from the reader. Naming is the cheapest documentation.

**Comments should say *why*, not *what*.**

```python
i += 1                        # increment i          <- worthless
i += 1                        # skip the header row  <- the reason
```

The code already says what. Only you know why.

**Functions should do one thing** — because a function that does one thing can be named accurately,
and an accurate name means the next reader need not read the body.

**Consistency beats personal preference.** In an existing codebase, match the surrounding style even
where you would have chosen differently. A file with two styles is harder to read than a file with
either one.

**Delete aggressively.** Commented-out code is noise; version control already remembers it. Every
line you delete is a line nobody has to understand.

---

## 5. Judgement: The Thing That Is Actually Hard

You now know several ways to do most things. Knowing *which* to use is the skill that takes years,
and the course has been quietly building it.

**When is a fancy structure worth it?** A hash table beats a list scan at large n. At n = 20, the
list is faster *and* clearer. Week 6 gave you the analysis; judgement is knowing when the analysis
is the deciding factor and when it is noise.

**When is defensive code worth it?** Week 10's atomic write is right for a file a user would be upset
to lose, and overkill for a cache you can regenerate. "Always be maximally defensive" is not
engineering; it is superstition with extra steps.

**When do you optimise?** After measuring. Every term someone rewrites a function to save 3ms in a
program that spends 400ms waiting on disk. You have the tools to know better.

**When do you stop?** Requirements are never fully specified and code is never finished. "Good
enough for what it is for" is a judgement, and refusing to make it is its own failure mode.

**When do you say a thing cannot be done?** Week 11's real gift. When asked to detect all infinite
loops, you can now explain precisely why not — and propose the timeout instead. That reframing, from
"no" to "not that, but here is what is possible", is the most professionally valuable thing in the
course.

---

## 6. Some Habits Worth Keeping

- **Read the error message.** All of it. The answer is in there more often than not.
- **Reproduce before fixing.** A bug you cannot trigger is a bug you cannot verify you fixed.
- **Change one thing at a time.** Two simultaneous changes and a behaviour change tell you nothing.
- **When stuck, explain it aloud.** To a person, a rubber duck, or an empty room. Articulating the
  problem is often the fix, because the wrong assumption surfaces when you say it.
- **Write the test that fails first.** Then you know when you are done.
- **Keep a bug journal.** The bugs you find hardest reveal your specific blind spots, and they
  repeat.
- **Be precise about what you know.** "It doesn't work" is not a report. "It raises `KeyError` on
  line 40 when the config lacks a `timeout` field" is.

That last one is the through-line of the whole course. Precision about what you actually know —
versus what you assume, measured versus guessed, proved versus tested — is the discipline underneath
all of it.

---

## 7. Closing

You started with `print("Hello, world")`. You have since built sorting algorithms and analysed their
growth, implemented hash tables, parsed text, survived corrupt files, simulated a Turing machine, and
proved that certain programs cannot exist.

More usefully, you have learned that **every abstraction leaks**, that the leaks are learnable, and
that knowing where they are is what separates using a tool from understanding it.

The field is much larger than this course. It is also, at its foundations, smaller than it looks:
represent the data well, respect the boundaries, measure before believing, and know the difference
between hard and impossible.

That is enough to build almost anything. The rest is practice.

---

## Summary

| Idea | Takeaway |
|---|---|
| Reading dominates | Most programming is understanding code you did not write |
| Why it is hard | You lack the context, history, and constraints the author had |
| The method | Run it → entry point → **data structures** → tests → one path → probe → notes |
| Chesterton's Fence | Understand why code exists before deleting it — *and* remove genuinely dead fences |
| Ugly ≠ wrong | Only one of the two is urgent |
| Write for the reader | Names, *why*-comments, one thing per function, consistency, deletion |
| Judgement | Knowing which correct option to choose — the part that takes years |
| The through-line | Be precise about what you actually know |

---

## Reading

- **Kernighan & Pike, *The Practice of Programming*** — the best book on this material; short
- **Ousterhout, *A Philosophy of Software Design*** — on complexity and interfaces; opinionated and
  worth arguing with
- **Hunt & Thomas, *The Pragmatic Programmer*** — optional; broad, uneven, several ideas that stick
- **Any codebase you use.** Pick a small tool you rely on and read its source this holiday. That is
  the actual assignment, and nobody will grade it.

---

*CS 101 · Week 12 · Lecture 39 (Fri) · © CSE Department*
