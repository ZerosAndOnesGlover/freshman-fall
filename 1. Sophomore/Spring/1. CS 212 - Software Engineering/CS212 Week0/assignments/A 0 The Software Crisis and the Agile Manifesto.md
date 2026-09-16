# CS 212 · Assignment 0
## The Software Crisis and the Agile Manifesto — A Critical Reading

---

**Released:** Week 0, second Wednesday, 17:00 · **Due:** Week 1, Friday 17:00
**Total: 100 points** · Submit one PDF, `A0_{LastName}_{StudentID}.pdf`

> **This is the only assignment of the term with no code in it.** Every other one changes a
> repository. This one establishes the habit the rest are marked against: **a claim about
> engineering is a claim about cost, in a context, with evidence — and you are expected to say
> which.**
>
> **Length: 1,200–1,800 words**, excluding tables and references. A paper of 3,000 words is marked
> down; part of the exercise is saying it in the space available.
>
> **Cite properly.** Anything you quote or lean on gets an author, a title and a year. A URL alone
> is not a citation. **Quoting a source you have not opened is the one thing that fails this
> paper outright** — and it is detectable, because the most-quoted sentences in this field are
> routinely quoted wrongly.
>
> Collaboration: discuss freely, write alone. State at the top: *"I wrote this independently"* or
> name who you discussed which question with.

---

### Q1: Read the Primary Source (20 points)

Royce's 1970 paper, *"Managing the Development of Large Software Systems"*, is freely available. **Read it.** It is 11 pages.

**(a) [6]** Quote, with page number, the sentence in which Royce evaluates the model of his Figure 2. Then state in your own words **what he recommends instead**, in no more than four sentences.

**(b) [8]** Royce lists five steps to fix the model. **Pick two**, and for each, name the modern practice that is its descendant and say what that practice does that Royce's version did not. Be specific about the mechanism, not the name.

**(c) [6]** The single-pass waterfall was written into **DOD-STD-2167** in 1985 and stayed in defence contracts for a decade. **Give one reason a procurement organisation would prefer the misreading to the paper**, and say whether that reason is a bad one. *(There is a defensible answer on each side. Take a position.)*

---

### Q2: The Manifesto as Four Trade-Offs (30 points)

**(a) [12]** For **each** of the four value statements, fill in this table. **One row per line; three to four sentences per cell, no more.**

| Value statement | A concrete situation where the left-hand side is right | A concrete situation where the **right**-hand side is right | The property of the situation that decides it |
|---|---|---|---|

**Your four deciding properties in column 4 must be different from each other.** If two rows reduce to "it depends how big the team is", you have not found the distinction.

**(b) [10]** L03 §2 argues that *"individuals and interactions over processes and tools"* is **the wrong instruction for deployment**, using Knight Capital. **Either** extend the argument — name a second class of task where the right-hand side should win, and say what the two classes have in common — **or** rebut it: argue that Knight Capital is not a counter-example to the manifesto and say why.

**(c) [8]** Read the **twelve principles** on the manifesto's second page. **Name the one that is hardest to satisfy in a university team project, and say precisely what makes it hard** — not "we're busy". Then say what the nearest achievable substitute is for your team, and what it loses relative to the real thing.

---

### Q3: A Failure, Reconstructed (30 points)

**Pick one** system from L01 §3 **other than Ariane 5** (it is done for you in the lecture), or any documented failure with a published inquiry — the Post Office Horizon scandal, the 2012 RBS batch failure, Heartbleed, the 2017 Equifax breach, the NHS National Programme for IT.

**(a) [10]** In **no more than 300 words**, state what happened: the system, the failure, the cost, and the immediate technical cause. Cite the inquiry, post-mortem or paper you used. **Wikipedia may be your route to the source; it may not be your source.**

**(b) [12]** **Name three decisions, made before the failure, that made it possible.** For each: who was placed to make it, what the alternative was, and — the part that carries the marks — **what would have had to be true for the decision made to be the right one.** This is not an exercise in blame. Every one of these decisions looked reasonable to a competent person at the time, and your job is to reconstruct the reasoning that made it look that way.

**(c) [8]** **Which practice from this course's syllabus would most likely have caught it, and which would definitely not have?** Name one of each, with a mechanism. *"Better testing"* earns nothing; *"a property-based test asserting that the total dose never exceeds the prescribed dose, which would have been checked on every path including the fast-keystroke one"* earns full marks.

---

### Q4: The Evidence Question (20 points)

L02 §8 rates the evidence for six practices from *strong* to *essentially none*.

**(a) [8]** **Pick one claim rated "weak" or "mixed" and investigate it.** Find **two** studies that reach different conclusions. For each: what was measured, on whom, how many, for how long. Then say **why they disagree** — sampling, definition of the outcome, task, experience level, duration, publication bias. A real answer names a specific methodological difference.

**(b) [6]** L01 §8 says the Standish CHAOS figures are unreliable and points at Jørgensen & Moløkken (2006). **Read their criticism** and state the two strongest objections in your own words. Then answer: **does the criticism mean the reports are worthless, or that they are measuring something other than what they claim?** Defend your answer.

**(c) [6]** **What would it take to actually know whether TDD works?** Design the study: population, intervention, control, outcome measure, duration, and the confound you cannot eliminate. Then say **why it has never been run**, in terms of cost and of who would pay for it.

---

## Marking

| Band | What it looks like |
|---|---|
| **90–100** | Primary sources read and quoted accurately. Positions taken and defended. At least one place where the student disagrees with the lecture and gives a reason that holds. Q3(b) reconstructs the *reasoning*, not the blame |
| **75–89** | Correct, well-sourced, specific. Every claim attached to something. Positions taken but not much pushed on |
| **60–74** | Accurate summary of the lectures with real citations, thin on independent judgement. Q2(a)'s column 4 collapses into one distinction |
| **45–59** | Restates the lectures. Cites secondary sources for claims the primary source contradicts. Q3 describes a failure without reconstructing a single decision |
| **< 45** | Quotes Royce's figure as though he endorsed it. Treats the four values as commandments. No sources, or sources that do not say what they are claimed to say |

**One instruction that carries across the whole term:** where you disagree with the lectures, **say so and give a reason.** Nothing in this paper is marked on agreement. The Week 0 lectures state contested things as though they were settled in at least four places, and finding one is worth more than agreeing with all of them.

---

## Sources You Will Need

All freely available; none behind a paywall.

- Naur, P. & Randell, B. (eds.), *Software Engineering: Report on a Conference Sponsored by the NATO Science Committee, Garmisch, 7–11 October 1968* (1969)
- Royce, W. W., *"Managing the Development of Large Software Systems"*, Proc. IEEE WESCON (1970), pp. 328–338
- Dijkstra, E. W., *"The Humble Programmer"*, CACM 15(10) (1972)
- Beck, K. *et al.*, *Manifesto for Agile Software Development* (2001) — **both pages**, agilemanifesto.org
- Leveson, N. & Turner, C., *"An Investigation of the Therac-25 Accidents"*, IEEE Computer 26(7) (1993)
- Lions, J. L. (chair), *Ariane 5 Flight 501 Failure: Report by the Inquiry Board* (1996)
- SEC, *Administrative Proceeding File No. 3-15570: Knight Capital Americas LLC* (2013)
- Jørgensen, M. & Moløkken-Østvold, K., *"How large are software cost overruns? A review of the 1994 CHAOS report"*, Information and Software Technology 48(4) (2006)
- Fucci, D. *et al.*, *"An External Replication on the Effects of Test-Driven Development"*, ESEM (2016)
- Fowler, M., *"The State of Agile Software in 2018"*, martinfowler.com

---

*CS 212 · Week 0 · Assignment 0 · 100 points · due Friday of Week 1, 17:00*
