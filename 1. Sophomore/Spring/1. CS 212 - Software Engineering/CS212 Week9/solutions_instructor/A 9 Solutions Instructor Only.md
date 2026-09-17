# CS 212 · Assignment 9 — Marking Guidance
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for A 9.** The first assignment that refactors code the student did not write,
cannot ask about, and does not fully understand. **That is the difficulty and it is the point** —
`slot` cannot exercise it, because they wrote all of it.

**Mark the discipline, not the destination.** A modest Extract Function done with characterisation
tests first, in single-hat commits, with the concurrency question answered, is a better paper than an
ambitious restructuring done in one commit with the tests edited to suit.

**The three discriminators:**

1. **Q2(a)'s procedure shown.** Did they write the wrong assertion, read the failure, and paste in the
   real value — and can they show it? About half the cohort writes characterisation tests by reading
   the code and asserting what they think it does, **which is a different and much weaker technique**,
   because it inherits their misreading.
2. **Q2(c) — did they find a pinned bug?** `roomsvc` has several available. A student who finds one has
   done the thing characterisation testing exists for.
3. **Q5(b)'s concurrency line, about their own diff.** Not the general point; whether *their*
   refactoring moved something out of a critical section.

**Three automatic caps, all stated:** any of the 212 tests failing → 45; fewer than three commits →
60; an out-of-bounds target → 55.

**Calibration:** median 64–68 — the lowest of the term after A 2, because working in an unfamiliar
codebase is genuinely harder and several students will choose a target beyond what they can pin.

---

## Before Marking: Check the Caps

```bash
git -C <fork> checkout <branch>
pytest -q                         # must be 212 passed + their characterisation tests
git log --oneline main..HEAD       # count the commits; check the prefixes
git diff main..HEAD -- tests/      # existing test files must show ADDITIONS only
```

**The last command is the important one.** A modified existing test is a behaviour change. **If the
paper does not name it and justify it, apply the 45 cap.** If it does, read the justification — a
student who found that an existing test encoded a bug, said so, and changed it with an argument has
done good work and should score well. **That case is rare and should be rewarded, not capped.**

**Out-of-bounds targets:** `confirm_booking`'s Split Phase (done in L29 §3), the pricing `if` tree
(A 2), the `Slot` value object (A 4's likely target). **Check what they actually touched**, not what
they say — a student who "extracted a helper" from `confirm_booking` without doing Split Phase is in
bounds.

---

## Q1: Choose by Looking (15)

### (a) [6]

| | |
|---|---|
| 3 | Both commands run, output reported |
| 3 | **The intersection named**, and a file chosen from it |

**Expected output**, for checking:

```
891 roomsvc/bookings.py       F 291:0 confirm_booking   - F (94)
204 roomsvc/views.py          F 812:0 _resolve_conflicts - E (38)
186 roomsvc/models.py         F 1455:0 render_week      - D (27)
122 roomsvc/notify.py         F 2103:0 apply_recurrence - D (24)
 98 roomsvc/reports.py        F 88:0  booking_form      - D (22)
```

**The intersection is `bookings.py`**, which is largely out of bounds, **so a good answer notices that
and goes to the second tier** — `views.py` (204 touches, `booking_form` at complexity 22) or
`notify.py` (122 touches, 3.9% coverage). **A student who says "the obvious target is excluded, so here
is the next one and here is why" scores the full 6.**

**Deduct 3** for choosing a file with no evidence — a student who picks `admin.py` because it looked
messy has skipped the question.

### (b) [5]

| | |
|---|---|
| 3 | **Fowler's name** for the smell, correctly used |
| 2 | Stated as a problem, with evidence |

**Check the name against Ch. 3.** Common misuse: calling Divergent Change "Shotgun Surgery" or vice
versa. **They are duals** — Divergent Change is one module changing for many reasons; Shotgun Surgery
is one reason changing many modules. **Deduct 1 and explain**, because the distinction determines the
refactoring.

### (c) [4]

| | |
|---|---|
| 4 | What the smell indicates **here**, with the discrimination the smell requires |

**The mark is for L29 §1 step 2.** For Duplicated Code, they must apply W2 L09 §1's test and say which
kind it is. For Long Function, they must say what the *underlying* problem is (L29 §3). For Primitive
Obsession, whether the primitive is actually doing harm.

**2 of 4** for restating the smell's general definition. **0** for "this is bad code".

---

## Q2: Characterise Before You Touch It (25)

### (a) [14]

| | |
|---|---|
| 6 | Tests exist, pass, cover what will change |
| **4** | **The procedure shown** — the wrong assertion, and the failure output |
| 4 | **A comment per test** saying it records rather than endorses |

**The 4 marks for the procedure are the paper's best discriminator.** What a full answer looks like:

> I first wrote `assert render_week([]) == ""`, which failed with
> `assert '<table class="week">\n<tr>...' == ''` — so the empty case emits a full empty grid, 38
> lines of it, not an empty string. I used approval testing for this one rather than pasting 38 lines
> into an assertion.

**2 of 4** for a claim that they followed the procedure with nothing shown. **0** if the tests were
plainly written by reading the code — the tell is assertions that are *round* (`== 0`, `== []`) where
the real behaviour is messy.

**The comment marks [4]** are mechanical: check the test file. Look for something like
`# Characterisation only. Not a claim that this is correct.` **Deduct 2** for comments on some tests
but not all — the risk is that the uncommented ones get read as specifications.

### (b) [7]

| | |
|---|---|
| 3 | Branch coverage of the target, from characterisation tests only |
| 4 | **The unpinned branches named**, and which the refactoring could break |

**The second part is the engineering.** A student who reports 62% and says *"the three unpinned
branches are the `exam` special case, the equipment override, and the `except ValueError` path — and
my Extract Function touches the second, so I added a test for it"* scores the full 4 **and has done
the assignment properly.**

**Deduct 4** for a coverage number with no branch names.

### (c) [4]

| | |
|---|---|
| 3 | A pinned bug identified, or a credible account of having checked |
| 1 | An issue opened, if a bug was found |

**Bugs available in `roomsvc` for the marker's reference** — these are the ones students find:

| Behaviour | Why it is arguably a bug |
|---|---|
| **The equipment override** zeroes the price *after* all policy logic, silently | Undocumented; means an external partner booking a PA kit is free |
| **Hold expiry exists only in query predicates** — nothing expires the rows | A `state='HELD'` row from 2021 is still in the table |
| **`state` is `String(20)` with no constraint**, and a capitalised variant shipped for three weeks in 2022 | Any typo is accepted |
| **`render_week` emits a full grid for an empty booking list** | Arguably correct; arguably why the week view is slow |
| **`price_for` raises `ValueError` on an unknown kind**, which reaches the user as a 500 | Reached in production twice |
| **Negative `capacity` is accepted** and renders as a negative number in reports | |

**Full marks for "I checked and found none, here is how"** only with a method — *"I read the seven
branches against the finance office's published rate card in `docs/rates.md` and they agree"*. **A bare
"no bugs" scores 1.**

---

## Q3: The Refactoring (30)

### [10] Correctness and completeness

| | |
|---|---|
| 10 | Smell addressed, all callers migrated, nothing dead left behind |
| 7 | Correct but the old path remains, called from one place |
| 4 | Partial |
| 0 | A rename presented as a refactoring, or it does not run |

**Check for the dead-code failure specifically** — a correct new implementation with the old one still
present and still called. **Worse than either, because the logic now lives in two places.**

### [8] Tests pass unchanged

8 for 212 + characterisation tests green with only additions to test files. **See the cap check above
for the modified-test case.**

### [7] One hat per commit

| | |
|---|---|
| 7 | Four or more commits, `test:` adds only tests, `refactor:` changes no tests and no behaviour |
| 5 | Four or more but one commit mixes |
| 3 | Three commits |
| 0 | Fewer than three → **cap at 60** |

**Verify the hats, do not trust the prefixes.** `git show <sha> --stat` on each: a `refactor:` commit
touching `tests/` is mislabelled. **Deduct 2** and say so — the discipline is the point, and a
mislabelled commit defeats the property it exists to provide.

### [5] A named Fowler refactoring

5 for a correctly-named refactoring that is the right one for the smell. **Check the pairing** —
Extract Function for Duplicated Code is right; Extract Function for Divergent Change is not (that
wants Move Function or Split Phase).

**Remove Dead Code on `roomsvc/plugins/` gets the full 5** and should be praised. **Check they
established it is dead**: `grep -rn 'plugins' roomsvc/` and `git log --oneline roomsvc/plugins/`.
A student who deleted it without checking scores 2 — **the check is the work, and there is one import
in `main.py` that must be handled.**

---

## Q4: Would It Fit in a Commit? (15)

### (a) [9]

| | |
|---|---|
| 5 | All six steps, in order |
| 2 | **Real names in the real code**, not a generic template |
| 2 | **A count for step 2** |

**The count is checkable.** For a repository abstraction: `grep -c 'db\.execute\|db\.query' roomsvc/*.py`
gives the call sites. **A student who reports "31 call sites, of which 19 are in `bookings.py`" has
done the work.** A plan with "migrate the callers" and no number scores 0 for that part.

**Deduct 5** for a plan that is the six steps restated with `<component>` placeholders.

### (b) [3]

| | |
|---|---|
| 2 | An answer to the second-implementation test, applied to their plan |
| 1 | A justification either way |

**Both answers are correct.** Keep it because the test fake is the second implementation and the seam
buys fast domain tests; delete it because the suite is fast enough and the indirection costs a hop.
**0 for not addressing it** — it is the step the lecture says everybody forgets.

### (c) [3]

| | |
|---|---|
| 2 | A concrete board mechanism with a denominator |
| 1 | Why a denominator works where a reminder does not |

**The answer wanted:** a visible count makes the remaining work *finite and measurable*, so it can be
picked up by anyone and its incompleteness is visible to the whole team — whereas "remember to finish
it" is invisible the moment the person who remembered moves on. **Accept any version of "unfinished
becomes visible rather than forgotten".**

---

## Q5: What You Did Not Do, and the Danger You Checked (15)

### (a) [6]

| | |
|---|---|
| 2 | A second smell, evidenced |
| 3 | Cost both directions **and a revisit condition** |
| 1 | The issue exists on their fork |

**Same standard as A 4 Q5.** *"No time"* scores 0. The arithmetic is what earns it.

### (b) [6]

| | |
|---|---|
| 4 | All four cases addressed, one line each |
| **2** | **The concurrency case answered about their own diff** |

**The 2 marks require specificity about their change.** *"Concurrency: my refactoring is in
`render_week`, which is read-only and holds no lock, so this does not apply"* → full marks, it is a
correct analysis. *"Concurrency: yes, I should be careful"* → 0.

**Look out for the real case.** Any refactoring in `bookings.py` near the `SELECT`/`INSERT` pair, or
anything touching `_resolve_conflicts`, genuinely does apply — **and a student who notices that their
Extract Function moved a database call relative to a guard has found the thing the lecture warned
about.** Full marks and say so.

**The public-interface row also catches people:** `views.py` returns JSON that other things consume.
A student who realises their rename changed a response field has discovered Week 10 early.

### (c) [3]

| | |
|---|---|
| 2 | Something they needed to know and could not |
| 1 | What they did instead |

**"Nothing" scores 0**, and the paper says so. Credible answers:

- *"Why `confirm_booking` checks `slot.is_provisional` twice. `git log -S` finds the commit; the
  message is 'fix'. I left both checks."* **The canonical one.**
- *"Whether the equipment override is policy or a bug. There is no rate card in the repository and
  nobody to ask, so I characterised it and opened an issue asking finance."* **Best answer available.**
- *"Whether `_entry` dicts are still produced anywhere. `grep` finds two writers and no reader, but
  `calendar_sync` builds keys dynamically, so I could not be sure and did not delete it."**

**Award the full 3 for an answer that ends in a defensible decision made under uncertainty.** That is
the actual skill.

---

## Overall Bands

| Band | |
|---|---|
| **90–100** | Target from the hotspot intersection, with the exclusion noticed. Characterisation procedure shown with real failure output; unpinned branches named; a pinned bug found and issued. Four-plus verified single-hat commits. The right named refactoring. Q4 with real names and a real count. The concurrency question answered about their own diff. Q5(c) ends in a decision under uncertainty |
| **75–89** | Sound refactoring, green, evidenced smell, characterisation tests with comments, commits separated, Q4 correct |
| **60–74** | Works; smell asserted; characterisation tests written by reading the code; two or three commits; Q4 generic; Q5 thin |
| **45–59** | Tests changed without justification; no characterisation tests; hats mixed |
| **< 45** | 212 tests failing (45 cap), out-of-bounds target (55 cap), or behaviour changed |

**Feedback note for every paper:** tell them whether the refactoring they *planned* in Q4 is the one
they should have done, and whether their Q5(a) smell is more urgent than the one they fixed. **Week 11
asks them to prioritise a debt register**, and a student who has already been told their priorities
were inverted gets much more out of it.

**Cohort note:** count how many students chose deletion. **It is usually one or two, and naming that —
anonymously, alongside the plugins directory's 31 commits and zero plugins — is the most effective way
to make the next cohort consider it.**

---

*CS 212 · Week 9 · A 9 marking guidance · INSTRUCTOR ONLY*
