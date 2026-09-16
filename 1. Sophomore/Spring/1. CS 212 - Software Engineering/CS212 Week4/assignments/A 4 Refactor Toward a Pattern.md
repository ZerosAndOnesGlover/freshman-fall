# CS 212 · Assignment 4
## Refactor Toward a Design Pattern; Document the Smell It Removes

---

**Released:** Week 4, Wednesday 17:00 · **Due:** Week 5, Friday 17:00
**Total: 100 points** · Submit **a pull request against your team repository** plus a PDF, `A4_{LastName}_{StudentID}.pdf`

> **The order in the title is the order of the work.** You find a smell; you establish that it is a
> smell; you refactor towards whatever removes it — **which might not be a named pattern at all.**
> Q3 exists precisely so that *"the right answer here was a dict"* is a full-marks answer.
>
> **This is a refactoring.** Behaviour does not change; the tests that passed before pass after. If
> you need to change a test, you have changed behaviour, and you must say so and justify it.
>
> **The smell must be in your own project.** Not `roomsvc`, and **not the pricing `if` tree** —
> that was A 2 and it is explicitly out of bounds.

---

### Q1: Find and Evidence the Smell (25 points)

**(a) [8]** Identify **one** smell in your team's repository. State it as a problem, in the form L13 §4 requires: what recurs, where, and what it costs.

**Evidence required — at least two of:**
- The same construct in three or more places (`grep`, with line numbers)
- A `git log` showing it has been edited more than once for the same kind of reason
- A test that is hard to write, or absent, because of it
- A file-touch count (W2 L07 §2's method)

**(b) [7]** **Name the three candidate responses**, including at least one that is not a pattern — inline it, delete it, a dict, a parameter, a language feature. For each: what it would cost a reader (files to open), and what it would buy.

**(c) [10]** **Say why you chose the one you chose**, and apply L13 §5's three tests explicitly:
- **[4]** Name the problem, not the pattern.
- **[3]** **Name the second case.** If there isn't one, say what that implies and why you proceeded anyway.
- **[3]** **Count the files a reader must open** to answer one behavioural question, before and after. **If the count went up, justify what got better in exchange.**

---

### Q2: Do It (30 points)

**In the pull request.**

| | |
|---|---|
| **[12]** | The refactoring is correct and complete. No callers left on the old path; no dead code left behind |
| **[8]** | **Tests pass unchanged.** If any test changed, the PR description says which, why, and what behaviour changed |
| **[6]** | Commits are separate and ordered so that each one is reviewable. **A refactoring is the easiest thing in the world to commit in small steps, and this is the week to prove you can** |
| **[4]** | The PR description names the smell, the pattern (or non-pattern), and what a reviewer should check first |

> **Do it in the order Week 9 will teach formally:** make sure you have a test that covers the
> behaviour **before** you change anything. If you do not, write it first — **and that commit is
> separate, and it passes before and after.**

---

### Q3: Write the Pattern Description (20 points)

Produce the four-part description from L13 §4 **for what you actually did**, in your own words, referring to your own code.

| | |
|---|---|
| **[5]** | **Problem / when to use it** — stated so that a teammate could recognise the *next* occasion |
| **[5]** | **Solution** — the core, in Python, with the ceremony Python does not need removed |
| **[7]** | **Consequences** — **at least two costs.** Indirection, allocation, debugging, a reader's file count, a new failure mode |
| **[3]** | **Known uses** — where else you have seen it work. **"Only the textbook" is an honest answer and should be written if true** |

**If your answer was "not a pattern" — a dict, a parameter, a deletion — write the description anyway.** The four parts apply. **A student who produces a clean description of "replace the class hierarchy with a lookup table" has done the harder and more useful thing.**

---

### Q4: Norvig's Test (15 points)

**(a) [8]** Take **one GoF pattern you did not use** and demonstrate Norvig's claim on it: show the GoF structure, then the Python version, and **state precisely what disappeared and what did not.**

**The "what did not" is the mark.** Something always survives — the *idea* — and saying what it is, is the point. *"Strategy becomes a function argument, but the design decision that this varies at runtime and is chosen by the caller survives entirely"* is the standard.

**(b) [7]** L15 §4 lists eight patterns that became syntax. **Pick one and find when and why the language feature was added** — the PEP, the release, the motivation. Then answer: **what is the next pattern in this list?** Name a pattern you expect a future Python to absorb, and what the syntax would have to look like.

*(There is no right answer to the second part. It is marked on whether the argument is coherent.)*

---

### Q5: The One You Did Not Do (10 points)

**Find a second smell in your repository, and deliberately leave it.**

| | |
|---|---|
| **[4]** | State it, with the same evidence standard as Q1(a) |
| **[4]** | **Why leaving it is the right call this fortnight.** Cost of fixing, cost of not fixing, what else that time buys, and when you would revisit |
| **[2]** | **Record it** — an issue in your tracker, labelled, linked from the PDF. **Week 11 asks for your debt register and this is its first entry** |

> **This question is worth ten marks because knowing what not to fix is half the skill**, and
> because a team that refactors everything it notices ships nothing. **"We left it because we ran
> out of time" is not the answer; "we left it because X was worth more this fortnight, and we will
> revisit it when Y" is.**

---

## Marking

| Band | |
|---|---|
| **90–100** | The smell is evidenced with a count, not asserted. A non-pattern is seriously considered in Q1(b). The file-count goes up and is justified, or goes down and is measured. Commits are small and ordered. Q3's consequences are real costs. Q5 has a dated revisit condition |
| **75–89** | Sound refactoring, tests green, pattern justified, description complete with two costs. Q4 correct |
| **60–74** | Pattern applied correctly, smell asserted rather than evidenced. Consequences are generic ("adds indirection"). One large commit. Q5 is "we ran out of time" |
| **45–59** | A pattern applied where there was no smell. Tests changed without explanation. No second case named and none sought |
| **< 45** | Tests broken; or the pricing case redone; or the "pattern" is a rename |

**Two automatic caps**, both stated in the paper: **tests failing → 50**; **the smell being the A 2 pricing case → 55**, because the point is to find your own.

**And one bonus worth naming:** a student who does Q1, concludes in Q1(c) that the right response is to **delete** the construct entirely, and does so, is doing the best available version of this assignment. **Deletion is a refactoring and it is the one nobody chooses.**

---

*CS 212 · Week 4 · Assignment 4 · 100 points · due Friday of Week 5, 17:00*
