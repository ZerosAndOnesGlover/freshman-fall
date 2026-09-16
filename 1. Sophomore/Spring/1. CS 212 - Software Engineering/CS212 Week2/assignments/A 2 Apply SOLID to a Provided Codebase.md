# CS 212 · Assignment 2
## Apply SOLID to a Provided Codebase, and Justify Each Change

---

**Released:** Week 2, Wednesday 17:00 · **Due:** Week 3, Friday 17:00
**Total: 100 points** · Submit **a pull request against your fork of `roomsvc`** plus a PDF, `A2_{LastName}_{StudentID}.pdf`

> **This is the first assignment that changes code**, and the shape of it is the shape of the rest:
> **a diff, plus the argument for it.** The diff alone is worth 40; the argument is worth 60. A
> beautiful refactoring with no justification scores below an adequate one that is defended.
>
> **The tests must still pass.** `pytest` is 212 tests and 94 seconds; run it before you open the
> PR. **A refactoring that breaks a test has changed behaviour, which is by definition not a
> refactoring** (Week 9 makes this precise).
>
> Fork `cse-dept/roomsvc` at tag `cs212-reference`. Work on a branch. One PR, with a description
> that could stand alone.

---

### Q1: Find the Actors (15 points)

**(a) [8]** L08 §1 lists five actors served by `bookings.py`. **Verify it, and extend it.** Go through the file and produce a table: each distinct concern, the line range, and **which actor asks for changes to it.** You should find at least seven concerns. Two of them are not in the lecture's list.

**(b) [4]** Use `git log --format='%s' roomsvc/bookings.py | head -60` and classify the last sixty commit subjects by which actor prompted them. **Give the counts.** State what the distribution tells you that the static reading of the file does not.

**(c) [3]** `notify.py` is 612 lines with **3.9% test coverage**. Using L08 §4, **say why those two facts are connected**, in three sentences. Name the specific property of the module that makes it untestable.

---

### Q2: The Open/Closed Case, With Evidence (20 points)

L08 §2 argues that the pricing `if` tree should be a policy registry **now**, and that the same change in 2020 would have been speculative generality.

**(a) [6]** Establish the evidence. Find, with `git log`, **when each of the six booking kinds was added**, and **how many files each addition touched.** A table.

**(b) [4]** Find commit `7b1e4f2` and show, from the diff, **which of the four switch sites it missed.** Then find, from the code as it stands, **what the consequence was** — state it as a sentence a finance officer would understand.

**(c) [10]** **Implement the fix.** A `PricingPolicy` per kind, resolved by a registry, so that adding a kind adds a file and edits nothing. Then, in the PR description:

- **[4]** Name the **axis of change** you have abstracted along, and cite the evidence from (a).
- **[3]** Name **one axis you deliberately did not abstract along**, that a less careful reading of open/closed would have led you to, and say why not.
- **[3]** State what your change **costs** a reader — the indirection, in concrete terms: how many files someone must now open to answer *"what does an external booking cost?"*

---

### Q3: Your Own Project, Audited (25 points)

Turn the lecture on `slot`.

**(a) [8] The second-implementation test** (L08 §7). List **every abstraction** in your repository — every interface, protocol, base class, factory, strategy, and every function whose only job is to call another function. For each: does a second implementation exist, and if not, **can you name the specific circumstance that would create one?**

**Then delete at least one**, or explain, per abstraction, why none should go. **"None should go" is a legitimate answer for a four-week-old project and needs one sentence per row, not a paragraph.**

**(b) [7] The three concerns** (L09 §4). Produce the import graph of your project (`grep '^from\|^import' -r src/` is enough). **Then answer:**

- Does anything in your domain or application layer import `fastapi`, `sqlalchemy`, or an SMTP or HTTP client?
- If yes: show the line, and **fix it**, in the same PR as Q2 or a second one.
- If no: show the two or three imports that *nearly* do, and say what keeps them honest.

**(c) [10] The DRY audit** (L09 §1). Find **one real duplication** and **one false duplication** in your own project.

- **[3]** The real one: two representations of one piece of knowledge. **Merge it.** Show the diff.
- **[4]** The false one: two fragments that look alike and encode different knowledge. **Leave it**, and apply L09 §1's test explicitly — describe the change to the world that would affect one and not the other.
- **[3]** If your project genuinely has no false duplication yet, **find one in `roomsvc` instead** and do the same. *(There are several; `views.py` and `importer.py` is not the only pair.)*

---

### Q4: Disagree With the Scoreboard (25 points)

L08 §6 rates the five letters. **Attack one rating.**

**(a) [10]** Pick one letter and argue the lecture's verdict is wrong — too generous or too harsh. **The argument must contain at least one concrete piece of code**, from `roomsvc`, from `slot`, or from a library you have read.

Candidates, if you want a starting point — but an argument of your own scores higher:

- **I is under-rated.** `typing.Protocol` gives Python structural interfaces with real static checking under mypy, so the "weak in a dynamic language" verdict is dated.
- **D is over-rated.** The indirection cost is real, most projects never swap the detail, and "fast tests" can be bought more cheaply with a test database in a container.
- **S is under-specified.** "One actor" is answerable only when actors are visible; in a product with one customer it collapses back into "one thing".
- **O is not a principle at all**, merely a description of what good abstraction looks like after the fact.
- **L is over-rated for Python**, where nobody uses deep inheritance and the real substitutability failures are in duck-typed function arguments.

**(b) [8]** **Steel-man the lecture's position** before you demolish it. State the best version of the verdict you are attacking, including the strongest evidence for it that the lecture did *not* give.

**(c) [7]** **What would settle it?** Describe the observation — in a codebase, in a study, in your own project by May — that would make you change your mind. **If nothing would, say so, and say what that implies about the claim.**

---

### Q5: The Pull Request (15 points)

Marked on the PR itself, not the PDF. **This is the first thing in the course marked as a piece of professional communication**, and Week 7 marks it much harder.

| | |
|---|---|
| **[5]** | **Commits.** Separate, each one doing one thing, each message saying **why** rather than what. A single commit called "refactor" scores 0 here |
| **[4]** | **The description.** What changed, why, what a reviewer should look at first, and what you are unsure about. **The last one carries two of the four marks** |
| **[3]** | **Reviewability.** Formatting-only changes are not mixed with behavioural ones. If you ran a formatter, it is its own commit |
| **[3]** | **Evidence.** The test run in the description; and if you changed behaviour anywhere, you say so explicitly and justify it |

> **The commonest failure here, every year:** one commit, message `"A2"`, 400 lines, formatting mixed
> with logic, no description. **It is unreviewable, and being unreviewable is a defect in the same
> sense that a bug is** — it is the property that turned a fourteen-line fix into four months.

---

## Marking

| Band | |
|---|---|
| **90–100** | Q1(b)'s commit classification finds something the file's structure does not show. Q2(c) names the axis *not* abstracted and the cost to a reader. Q3(a) deletes something. Q4 attacks a rating with real code and says what would settle it. The PR is reviewable |
| **75–89** | Refactoring correct, tests pass, argument present. Q3 audits honestly. Q4 disagrees but without code |
| **60–74** | The pricing fix works; the justification restates the lecture. Q3 lists abstractions and keeps them all with thin reasons. Q4 picks a suggested candidate and paraphrases the bullet |
| **45–59** | Code changed without justification, or justified without being changed. Tests not run. One commit |
| **< 45** | Refactoring breaks tests. No engagement with `git log`. Q4 agrees with the lecture |

**Two automatic caps.** A submission whose tests do not pass caps at **50**. A submission that is one commit with no description caps at **65**, however good the code — that is Q5's 15 marks plus the reviewability that Q2 and Q3 depend on.

---

*CS 212 · Week 2 · Assignment 2 · 100 points · due Friday of Week 3, 17:00*
