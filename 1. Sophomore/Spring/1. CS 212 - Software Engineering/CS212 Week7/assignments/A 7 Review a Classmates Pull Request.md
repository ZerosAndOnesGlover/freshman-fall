# CS 212 · Assignment 7
## Review a Classmate's Pull Request Against a Checklist

---

**Released:** Week 7, Wednesday 17:00 · **Due:** Week 8, Friday 27 March, 17:00
**Total: 100 points** · Submit a PDF, `A7_{LastName}_{StudentID}.pdf`. **The review itself is posted on GitHub and is marked there.**

> **⚠️ Spring Break (Mon 16 March) falls inside this assignment's window**, which is why you get
> sixteen days rather than nine. **The extra time is spent waiting for other people, not working** —
> you need a classmate's pull request to exist, and they need yours.
>
> **This is the one point in the term where somebody outside your team reads your code.** This course
> has no TA (syllabus §9), so until now your only reviewers have shared your vocabulary, your
> conventions and your blind spots. **A classmate reading your pull request cold is precisely the
> reader W0 L01 §4 says you are optimising for.**

---

## How the Pairing Works

**Pairs are posted on the portal by 17:00 Wednesday of Week 7.** You are matched with **one student
from a different team**. Reviews are **mutual**: you review theirs, they review yours.

**By Friday of Week 7 (13 March), each of you must have a reviewable pull request open**, and it must
be:

- **80–400 lines of diff.** Under 80 is too little to review; over 400 and L22 §4's evidence says
  your reviewer will find nothing. **If your natural change is bigger, split it and nominate one part**
- **Real work**, on your team's `slot` — not written for this assignment
- **Green in CI**, with a description

**Add your partner as a collaborator with read access** and request their review. If your partner has
not opened a PR by the Monday after the break (23 March), **tell the instructor that day** — do not
wait until the deadline.

---

### Q1: The Review (35 points)

**Marked from the pull request on GitHub, not from your PDF.**

| | |
|---|---|
| **[10]** | **Coverage of the checklist's passes.** At least one substantive comment from **pass 2 (design)** and one from **pass 3 (correctness)**. A review that is entirely pass 5 scores 2 of 10, however many comments it has |
| **[8]** | **Severity labels on every comment** — `blocking:` / `question:` / `nit:` / `praise:`. **Unlabelled comments score 0 here**, and L23 §4 says why: without labels, fourteen nits read as a rejection |
| **[7]** | **Comments are questions where the author may know something you do not.** Assertions where you are certain and it matters. **Not "this is wrong" on a design choice** |
| **[6]** | **Each substantive comment explains why, once.** *"Extract this"* scores nothing; *"this is the third place that computes the grid, and when the library extended to 21:00 one of the three was missed"* scores fully |
| **[4]** | **A verdict, stated**: approve, approve-with-nits, or request-changes — **against L23 §1's standard**, not against whether you would have written it that way |

> **The commonest failure, every year:** eleven comments, all about naming and formatting, no labels,
> and an approval. **That is a review that cost your partner twenty minutes of reading and gave them
> nothing**, and it scores under 10 of 35.

---

### Q2: What You Found, and What It Cost (20 points)

**(a) [8]** Report your review as a table: each substantive comment, its pass (1–5), its label, and **whether the author acted on it.** Then give the counts by pass.

**(b) [6]** **Compare your distribution to Bacchelli & Bird's** (L22 §2): ~29% code improvements, ~14% defects, ~9% knowledge transfer, ~7% alternatives. **Where does yours differ, and why?** A defensible answer names something about the artefact or about you — *"I found more defects because the change was 90 lines of date arithmetic"* or *"almost all mine were pass 5 because I ran out of attention"*.

**(c) [6]** **Time it.** How long did the review take, and how many lines? **Convert to lines per hour** and compare to Cisco's ~500/hour ceiling. Then say honestly whether your attention held, and where it went.

---

### Q3: Being Reviewed (20 points)

**(a) [8]** **Every comment you received, and what you did with it.** Acted / disagreed / discussed. **For each `blocking:` comment, say whether you agreed** — and for at least one, **argue back if you think they were wrong.** L23 §5: a reviewer is not automatically right, and the standard is *"is it reasonable?"* not *"is it what the reviewer would have written?"*

**(b) [6]** **Which comment taught you the most, and what did it reveal?** Not the most severe — the most *informative*. The best answers here are usually a `question:` that showed the code was not saying what its author thought it said.

**(c) [6]** **What did an outside reader not understand that your own team never questioned?** There will be at least one: a name, an abbreviation, a convention, an assumed piece of domain knowledge. **This is the highest-value finding in the whole assignment**, because it is the only evidence you will get all term about your team's shared blind spots. Say what you changed, or why you did not.

---

### Q4: Move Three Things to a Machine (15 points)

**Take three comments — yours or your partner's — that a tool should have caught.**

**(a) [9]** For each: the comment, the layer it belongs to (L24 §2), **and the change that implements it.** 3 marks each, and the mark requires the change to exist in a config file, a hook, or a test — **not a description of one.**

**At least one must be a layer-5 custom rule.** Generic linters do not know your conventions; you do, and you already wrote one in A 3.

**(b) [6]** **Prune something.** Look at your `ruff` `select` list, or your scanner's rule set, or your pre-commit hooks.

- **[3]** Name one rule that fires often and is **always dismissed**, and turn it off. *(If you use `select = ["ALL"]`, you will find several; that itself is the finding, per L24 §6.)*
- **[3]** Say why turning it off is the right call, in terms of the attention budget from L24 §1. **"It was annoying" scores 0; "it fired 41 times, we dismissed 41, and each dismissal cost a reviewer three seconds of the 40 minutes they have" scores 3.**

---

### Q5: The Limit (10 points)

L24 §5 lists seven things no tool can check, and notes that **the VNC 101 race passes all five automated layers.**

**(a) [6]** **Pick the two most relevant to your project** and say, concretely, what defect `slot` could ship today that **neither your review process nor your tooling** would catch. Not the list restated — your own code.

**(b) [4]** **Propose one change to your team's review practice** that would raise the chance of catching one of them. **It must be a change to the practice, not a resolution to try harder** — a question added to the PR template, a required section in the description, a rotation, a checklist item that must be answered in words.

---

## Marking

| Band | |
|---|---|
| **90–100** | The review reaches design and correctness, every comment labelled, whys given. Q2(c) reports a real lines-per-hour figure and an honest account of where attention went. Q3(a) argues back against a blocking comment. Q3(c) names a genuine shared blind spot. Q4 lands three real config changes including a custom rule, and prunes something with the arithmetic |
| **75–89** | A solid review with labels and design comments. Distribution compared. Received comments handled. Three automations, at least two real |
| **60–74** | Review is mostly pass 5 with a few labels. Q2 reports counts without analysis. Q3 lists comments without judgement. Q4's automations are descriptions rather than diffs |
| **45–59** | A terse review, unlabelled. No design or correctness comments. Nothing moved to a machine |
| **< 45** | No review posted, or "LGTM" |

**Two automatic caps.** A review with **no severity labels caps the paper at 65** — it is 8 marks directly and it is the convention the whole week turns on. A review consisting of **approval with no substantive comment caps at 45**, whatever the PDF says: the mark is for the review you give (L22 §6), and there is no such thing as a pull request with nothing worth asking about.

**One bonus worth naming.** A student whose review finds a **real defect in a failure path or under concurrency** — the two places L24 §5 says tools cannot reach — has done the thing the week exists for. **Say so in the feedback, and name it to the cohort anonymised.**

---

*CS 212 · Week 7 · Assignment 7 · 100 points · due Friday 27 March, 17:00*
