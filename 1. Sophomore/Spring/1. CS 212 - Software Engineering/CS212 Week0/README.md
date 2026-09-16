# CS 212 · Software Engineering
## Week 0: Software Engineering as a Discipline

**Credits:** 3 · **Prerequisites:** PROG 102, CS 101
**Assessment for this course (overall):** Team Project 40%, Individual Assignments 30%, Midterm 15%, Final 15%
**This week's deliverables:** A 0, and a team. **No quiz** — Quiz 1, in Week 1, covers this week.

> **Week 0 is ten teaching days long**, running Jan 12 to Jan 23, absorbing registration and
> add/drop. Week 1 — when graded work begins — opens Jan 26. CS 212 lectures **Tue/Wed/Thu
> 10:00–10:50 in TH 200**, so Week 0 offers six slots for three lectures: **L01 Wed Jan 14,
> L02 Thu Jan 15, L03 Tue Jan 20**, with the **Team Formation Workshop on Thu Jan 22** — the last
> slot before the add/drop deadline the following morning.

---

### Why This Week Exists

Because everything you have been taught so far assumes the program is finished when it is correct.

**Roughly 60% of what a piece of software costs is spent after its first release**, and only about a fifth of that is fixing bugs. The rest is change: to working software, by people who did not write it, for reasons that did not exist when it was written. **CS 212 is about that 60%**, and it starts here because the discipline itself was named — at NATO Garmisch in October 1968, deliberately and provocatively — by people who had just spent three days agreeing that nobody knew how to do it.

**This week also introduces the two codebases the whole term runs on.** `roomsvc` is the department's real booking service: 11,438 lines, six years old, four of its six authors gone, **61% line coverage and a 31% mutation score.** On 14 October 2024 it booked two lectures into VNC 101 at the same time. The fix was fourteen lines and it took four months.

**And `slot` is what you build to replace it**, in a team of 4–5, starting Thursday.

---

### Learning Objectives

By the end of Week 0, you should be able to:

1. Say **where the phrase "software engineering" came from and why it was chosen**, and what its authors were claiming did not exist.
2. State the crisis as an economics problem — **cost growing faster than linearly in size** — and give Brooks's $n(n-1)/2$ as one mechanism.
3. **Name four failures whose cause was process rather than code**, and say for each what would have had to be true for the fatal decision to have been right.
4. Quote the **~60/40 split of lifetime cost**, and the fact that **only ~21% of maintenance is corrective** — and say what that implies about what you are optimising for.
5. **Quote the sentence on page 329 of Royce (1970)** in which he rejects his own Figure 2, and name two of his five fixes and their modern descendants.
6. Say what **Boehm's ~100× cost-of-change curve** claims, and state Beck's objection to it accurately.
7. Give **a better argument for short cycles than the cost curve** — that ~2/3 of delivered features are rarely or never used, and no analysis identifies which third in advance.
8. Read each line of the Agile Manifesto as **a trade-off with a stated deciding property**, and give a real situation where the right-hand side wins.
9. **Name five contexts where agile methods genuinely do not apply**, including the one that is not about the domain at all — a team that cannot deploy.
10. Distinguish **Scrum's load-bearing parts** from its ceremonies, and state **Little's Law** as the reason a WIP limit works.
11. Say which practices in this field have **strong** empirical support and which have **essentially none**, and why the asymmetry falls where it does.
12. **Read `roomsvc`'s numbers and say which one you would act on** — and explain why 61% coverage and a 31% mutation score are two different facts.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L01 Why Software Engineering Was Invented]] | NATO Garmisch 1968 as a provocation; Dijkstra and Brooks; **six failures, four of them process failures**; the 60/40 split and the 21% that is bug-fixing; **`roomsvc` introduced with every metric**; the VNC 101 double-booking and the six later weeks it reappears in |
| [[L02 Process Models and What They Were Reacting To]] | A process as a bet on *when you find out*; **Royce p. 329 against his own Figure 2**; the sequential model stated fairly, with DO-178C; **Boehm's 100× curve and Beck's objection**; **45% of features never used**; spiral and risk-first; Scrum's load-bearing parts; **Little's Law**; the evidence, rated honestly |
| [[L03 The Agile Manifesto Read Critically]] | All 68 words, and **the closing sentence everyone deletes**; each value as a trade-off with its failure mode — **Knight Capital against "individuals over processes"**; four signatories repudiating the word; **five contexts where it does not apply**; the six practices that survive; how your project actually runs |
| [[CS212 Week0/project/PROJECT BRIEF slot\|PROJECT BRIEF slot]] | The system, the fixed domain, **the invariant**, what Phase 1 and the final demand, and the rules |
| [[CS212 Week0/project/TEAM CHARTER template\|TEAM CHARTER template]] | Definition of Done, WIP limit, role rotation, **and what happens when someone goes quiet** |
| [[CS212 Week0/project/TEAM FORMATION WORKSHOP\|TEAM FORMATION WORKSHOP]] | **Thursday Jan 22, 10:00–10:50, TH 200.** The one rule, and what you leave the room with |
| [[CS212 Week0/assignments/A 0 The Software Crisis and the Agile Manifesto\|A 0]] | Four questions, 100 points, **1,200–1,800 words**, due **Friday of Week 1** |
| [[CS212 Week0/resources/Course Overview Syllabus\|Course Overview Syllabus]] | **Read in full this week** — assessment, why there is no lab, tool versions, **and five places this course disagrees with its own textbooks** |
| [[CS212 Week0/resources/Reading Guide Week 0\|Reading Guide Week 0]] | Ninety minutes of required reading, and **which two books not to open yet** |
| [[CS212 Week0/resources/roomsvc metrics\|roomsvc metrics]] | Every number the lectures quote, with the command that produced it |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The fix for the VNC 101 double-booking was one line of DDL, and it took four months.**

Not because the bug was hard — a unique index on `(room, slot)` is a thing databases have done since 1975. It took four months because `confirm_booking` is 487 lines long with a cyclomatic complexity of 94, because the person who wrote 78% of its surviving lines left the department in 2023, because eleven tests cover a function with ninety-four independent paths, and because **nobody could convince themselves that touching it was safe.**

**Every week of this course is one answer to the question that sentence raises.** How do you end up in a state where a fourteen-line fix takes an afternoon? Week 2 says: by separating the rule from the plumbing. Week 3: by deciding which layer owns an invariant. Weeks 5 and 6: by having tests whose passing is evidence. Week 7: by having more than one person who has read it. Week 8: by making the deployment a machine's job. Week 9: by paying the cost down continuously instead of never. **They are not six topics. They are six answers.**

---

### Assessment Reminder

**Quizzes carry no weight. The project carries 40%.**

> **⚠️ CS 212 differs from every other Year 2 course on exactly this point.** In CS 201, CS 202,
> PROG 201 and PROG 202 the practical work is the lab, and the lab is unmarked. **CS 212 has no
> lab. Its practical work is the team project, and it is the largest single component in any
> course you take this year.** A student who treats it the way a lab is treated will fail it.

**Quiz *N* covers Week *N−1***, runs ten minutes at the start of **Tuesday's** lecture in Weeks 1–11, and prints its own answer key below the questions — sit it closed-book, then mark it yourself before leaving the room. Tracked in [[_CS 212 Quiz Record]].

**Assignments** are released Wednesday 17:00 and due Friday 17:00 of the week after. **The lowest of the thirteen is dropped.**

---

### Connections

**Back:** **PROG 102 and CS 101 are assumed and not re-taught** — Python to the level of classes and modules, and the ability to read code you did not write. **Git for your own work is assumed; git in a team is not**, and Week 1 spends twenty minutes on it.

**Sideways:** **CS 202 is teaching the vocabulary for this week's bug.** The VNC 101 double-booking is a check-then-act race on a critical section, which is CS 202's Week 3; the two courses reach the same failure from opposite ends, one in a kernel and one in a web service, and the fix in both cases is to make the check and the act indivisible. **MATH 251's Week 0** is the start of the machinery Week 6 needs to say what a mutation score means.

**Forward:** **Week 1 is requirements**, where the double-booking turns out to be an invariant nobody wrote down — and where your walking skeleton is due. **Week 6 is Phase 1 and the midterm, in consecutive days.** **Week 9 finally removes the bug** introduced today, and shows that the technical part took an afternoon. **Week 11 measures `roomsvc`'s debt with the numbers printed in this week's resources.**

---

*CS 212 · Week 0 · © CSE Department*
