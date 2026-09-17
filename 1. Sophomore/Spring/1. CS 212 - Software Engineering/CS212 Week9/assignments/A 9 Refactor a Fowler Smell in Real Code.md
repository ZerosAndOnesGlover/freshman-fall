# CS 212 · Assignment 9
## Refactor a Fowler Code-Smell Catalogue Entry in Real Code

---

**Released:** Week 9, Wednesday 17:00 · **Due:** Week 10, Friday 10 April, 17:00
**Total: 100 points** · Submit **a pull request against `roomsvc`** (your fork) plus a PDF, `A9_{LastName}_{StudentID}.pdf`

> **This one is on `roomsvc`, not on `slot`.** The whole point of the week is refactoring code you did
> not write, cannot ask about, and do not fully understand — which is where refactoring is actually
> hard and where `slot` cannot exercise you, because you wrote all of it eight weeks ago.
>
> **Two rules from the definition, and both are marked:**
> **the tests pass unchanged**, and **`test:` and `refactor:` are never the same commit.**
>
> **`confirm_booking`'s Split Phase is done for you in L29 §3 and is out of bounds.** So is the
> pricing `if` tree (A 2) and the `Slot` value object (A 4's likely target). **Find your own.**

---

### Q1: Choose by Looking (15 points)

**(a) [6]** Find `roomsvc`'s hotspots. Report both:

```bash
git log --since='2 years ago' --name-only --format='' | grep '\.py$' | sort | uniq -c | sort -rn | head
radon cc -s -n C roomsvc/ | head -20
```

**Then give the intersection** — most-changed × most-complex — and say which file you are working in.

**(b) [5]** **Name the smell**, from Fowler's catalogue, using his name for it. **State it as a problem** (L29 §1): what recurs, where, and what it costs. **Evidence required**, to A 4 Q1(a)'s standard — a count, a `git log`, or an absent test.

**(c) [4]** **Say what the smell indicates *here*.** L29 §1's step 2. A smell is a hint, and the same smell means different things in different code — **Duplicated Code may be real duplication or two lookalikes encoding different knowledge** (W2 L09 §1), and you must say which and apply the test.

---

### Q2: Characterise Before You Touch It (25 points)

**(a) [14]** **Write characterisation tests** for the behaviour you are about to restructure, by L28 §3's procedure.

| | |
|---|---|
| **6** | The tests exist, pass, and cover the behaviour you will change |
| **4** | **At least one shows the procedure** — the paper names the wrong assertion you wrote first and the failure output that gave you the real value |
| **4** | **Each test says in a comment that it records behaviour rather than endorsing it** |

**(b) [7]** **Run coverage over your characterisation tests only.** Report the branch coverage of the function or module you are about to change, and **name the branches you have *not* pinned.** Then say which of those your refactoring could silently break.

**(c) [4]** **Did you pin a bug?** Look at what your tests assert and say whether any of it is wrong. **If yes: pin it anyway, say so, and open an issue.** If genuinely not, say how you checked.

> **Q2(c) is where the marks are and it is the point of characterisation testing.** `roomsvc` has
> undocumented behaviour everywhere — an equipment override that zeroes prices, a hold expiry that
> exists only in query predicates, a `state` column with no constraint. **Finding one is good work.**

---

### Q3: The Refactoring (30 points)

**In the pull request.**

| | |
|---|---|
| **10** | **Correct and complete.** The smell is addressed, no callers left on the old path, no dead code left behind |
| **8** | **All 212 tests pass, unchanged**, plus your characterisation tests. **If any existing test changed, the paper must say which and why — and that is a behaviour change needing justification** |
| **7** | **One hat per commit.** `test:` commits add tests only; `refactor:` commits change no tests and no behaviour. **Minimum four commits** |
| **5** | **You applied a named refactoring from Fowler's catalogue**, and the PDF names it — Extract Function, Move Function, Split Phase, Replace Primitive with Object, Remove Dead Code, Replace Type Code with Subclasses, Hide Delegate |

> **Deletion counts, and it is the best available answer.** `roomsvc/plugins/` is **380 lines, 31
> commits, zero plugins** — Speculative Generality, and **Remove Dead Code is a named refactoring.**
> A student who deletes it, having established with `git log` and `grep` that nothing uses it, has done
> the assignment properly. **A 4's bonus note said deletion is the one nobody chooses; it is still
> true.**

---

### Q4: Would It Fit in a Commit? (15 points)

**(a) [9]** **Name a refactoring `roomsvc` needs that does *not* fit in a reviewable commit**, and **plan it as branch by abstraction** (L30 §2) — all six steps, with the actual names in the actual code, and **a count for step 2** (*"31 call sites"*).

**Candidates:** a repository over the scattered raw SQL; a `Slot` value object across 34 files; splitting `bookings.py`; replacing the global `SETTINGS` dict.

**(b) [3]** **Step 6.** After the old implementation is deleted, does your abstraction survive the second-implementation test (W2 L08 §7)? **Answer for your plan, and justify keeping or deleting it.**

**(c) [3]** **Step 2 is where teams stall.** Say what you would put on the board to stop that, and why a visible denominator works when "remember to finish it" does not.

---

### Q5: What You Did Not Do, and the Danger You Checked (15 points)

**(a) [6]** **A second smell in `roomsvc`, deliberately left.** Same standard as A 4 Q5: stated with evidence, the cost argument in both directions, **and a condition that would make you revisit it.** Recorded as an issue on your fork.

**(b) [6]** **L28 §6's four dangerous cases.** For each, say in one line whether it applies to *your* refactoring. **At least one should** — and for it, say what you did about it.

**The concurrency one is not hypothetical.** *"Can two of these run at once, and have I moved anything out of a critical section?"* **An extract-method that moves an `INSERT` away from its guard preserves every unit test and reproduces the VNC 101 bug.**

**(c) [3]** **What could you not find out?** `roomsvc` has 2,847 commits of which **14% reference an issue**, and four of its five authors have left. **Name one thing you needed to know and could not**, and say what you did instead. **"Nothing" is not a credible answer for this codebase**, and saying so costs the marks.

---

## Marking

| Band | |
|---|---|
| **90–100** | Target chosen from the hotspot intersection. Characterisation tests with the wrong-assertion procedure shown and the unpinned branches named. A pinned bug found and issued. Four-plus single-hat commits, 212 tests unchanged. The named Fowler refactoring is the right one. Q4's six steps have real names and a count. The concurrency question answered about their own diff. Q5(c) names something unknowable |
| **75–89** | Sound refactoring, tests green, smell evidenced, characterisation tests present with comments. Commits separated. Q4 plans correctly |
| **60–74** | Refactoring works; smell asserted rather than evidenced. Characterisation tests written but not by the procedure. Two commits. Q4 lists the six steps generically. Q5 is "no time" |
| **45–59** | Tests changed without justification. No characterisation tests. Hats mixed in one commit |
| **< 45** | The 212 tests do not pass; or the target is out of bounds; or the "refactoring" changed behaviour |

**Three automatic caps.** **Any of the 212 existing tests failing → 45**, because a refactoring that changes behaviour is not one. **Fewer than three commits → 60.** **An out-of-bounds target — `confirm_booking`'s Split Phase, the pricing tree, or the `Slot` object → 55**, because the exercise is finding your own.

---

*CS 212 · Week 9 · Assignment 9 · 100 points · due Friday 10 April, 17:00*
