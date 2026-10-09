# CS 212 · Software Engineering
## Week 12 · Lecture 3 of 3
### Career Paths, and What This Course Was For

*“Study after study shows that the very best designers produce structures that are faster, smaller, simpler, clearer, and produced with less effort. The differences between the great and the average approach an order of magnitude.”* — Fred Brooks, "No Silver Bullet" (1986)

---

**Sat:** Thursday of Week 12, 10:00–10:50, TH 200 · **The last lecture.** · **Reading:** Sommerville Ch. 1, re-read; Brooks, "No Silver Bullet" (1986) · **Next:** Demo Day, Tuesday 28 April · report and code, Friday 1 May 17:00 · **Final exam, Friday 8 May, 09:00–11:30**

**Coursework:** 📝 **Assignment 11** due Fri this week 17:00 · 📝 **Assignment 12** due Fri this week 17:00 · 🎤 **Demo Day** Tue of the completion period, report due Fri of the completion period 17:00 · 📕 **Final exam** Fri of finals week 09:00–11:30

---

## 1. The Two Tracks, and What They Actually Differ In

**Most serious employers have two senior tracks**, and the distinction is not seniority.

| | **Individual contributor** | **Management** |
|---|---|---|
| Titles | Senior → Staff → Principal → Distinguished | Lead → Manager → Director |
| **Your output is** | **Technical judgement** applied to hard problems | **Other people's effectiveness** |
| **Your feedback loop** | Hours to weeks | **Months to years** |
| The hardest part | Choosing which problem matters | Deciding without doing |
| What you lose | Organisational leverage | Hands-on skill, within a few years |

**The second row is the real difference**, and the fourth row is what makes each hard.

**The second-to-last row is worth dwelling on after thirteen weeks of arguing that short feedback loops are the whole of engineering progress.** Every process innovation since 1968 shortened the loop (W0 L02 §6), and **management is a job where the loop is months.** You find out whether you hired well in a year, whether you reorganised well in two. **If the thing you value about engineering is finding out quickly whether you were right, you will find management uncomfortable in a way that is not about the people.**

**And the reversibility asymmetry from L38 §6 matters more than people expect:** the move back is easy at one year, hard at five.

---

## 2. What the First Two Years Actually Ask For

**Not what you might expect from a degree.**

| Frequently | Rarely |
|---|---|
| **Reading code nobody can explain** | Designing a system from scratch |
| Making a small change safely in a large codebase | Choosing a database |
| **Writing the test that makes the change safe** | Implementing an algorithm |
| Finding out what a requirement actually means | Optimising anything |
| **Asking the question that saves a fortnight** | Being right about an architecture |

**Every row on the left is something this course made you do**, and A 9 — refactoring `roomsvc`, a codebase you did not write, whose authors left, where **86% of commits have no recoverable reason** — is the closest simulation of a first job available in a classroom.

**Two pieces of advice that hold across employers:**

**Optimise for the codebase and the colleagues, not the domain.** You will learn far more in two years on a well-engineered system with people who review carefully than on an exciting product with none. **The domain is interesting for a month; the codebase is your daily experience for two years.**

**In an interview, ask: *"how long from commit to production, and who can deploy?"*** The answer tells you more about the engineering culture than any statement of values will — **it is DORA's lead time and its bus factor, in one question** (W8 L25 §6, W11 L35 §3). *"Two weeks, and only the platform team"* and *"twenty minutes, anyone"* are different jobs.

---

## 3. Where to Go From Here

**Within this degree**, three courses build directly on this one:

| | |
|---|---|
| **CS 311 (Compilers)** | Large, structured, well-specified codebase. **The best place in the degree to practise reading unfamiliar code** — and it will make W4 L15 §5's expression problem concrete |
| **CS 321 / 331** | Where W3 L12's distributed-systems bill gets paid in full, with the consensus and consistency theory |
| **The capstone** | Where this course's process apparatus is either used or missed, at four times the scale |

**Three books, in order of when they will help:**

1. **Feathers, *Working Effectively with Legacy Code*.** Read it in your first job, in the first fortnight, when you are staring at something you cannot change. **It will be the most useful book on your shelf for two years.**
2. **Ousterhout, *A Philosophy of Software Design*.** Short, opinionated, and the best available counter-argument to *Clean Code* — which this course has disagreed with in five places and which your colleagues will have read.
3. **Winters, Manshreck & Wright, *Software Engineering at Google*.** The best writing on engineering *over time*, at scale. **Read it when you have been somewhere long enough to be irritated by something.**

**And one habit worth more than the books: keep a decision log of your own.** Not for an employer — for you. **What you decided, what you rejected, what you expected.** Then read it in a year. **It is the only way to find out whether your engineering judgement is improving**, and it is the same instrument as an ADR pointed at yourself.

---

## 4. What This Course Was For

**Four things. The first is the whole of it and the rest are consequences.**

### 1. Code you cannot change safely is worthless, however correct it is

**`confirm_booking` was correct for most inputs.** It was 487 lines, complexity 94, eleven tests against ninety-four paths, with 78% of its surviving lines written by somebody who left in 2023. **When it turned out to be wrong, the fix was twelve lines and it took four months** — not because the fix was hard, but because **nobody could convince themselves that touching it was safe.**

**Everything in this course is an answer to that sentence.** The invariant written down (W1), cohesion (W2), the placement (W3), tests that are worth something (W5–W6), a second reader (W7), a pipeline (W8), characterisation tests (W9). **Eight weeks of apparatus to make an afternoon possible** — which is the bill for **60% of lifetime cost falling after first release, and only a fifth of that being bug-fixing.**

### 2. Every practice is a claim about cost, in a context, with evidence — and you should ask for all three

**The course stated contested things as contested.** The evidence for test-first is weak and the benefit tracks small steps. Four of SOLID's five letters restate coupling and cohesion. Coverage correlates with effectiveness only through suite size. The 60%-of-defects figure is about an activity you have never performed. **And Fagan's number, Fielding's REST, the Agile Manifesto and Cunningham's debt were all disowned by their originators** — four times in thirteen weeks, because the memorable name travels and the caveats do not.

**The posture is not cynicism.** It is: **adopt a practice if the evidence and the context hold, and be able to say which.**

### 3. Instrument what you intend to act on, and act on it

**Goodhart's law appeared five times** and the mechanism was never dishonesty — a measure is a proxy, and optimising a proxy diverges from the goal where the proxy is weakest. **So: measure, read, act on individual findings, never set a target, ratchet where you must.**

**And the same failure appeared four times in a different costume — a signal generated and never read.** A flaky test that gets re-run. A linter rule everyone dismisses. A nightly sweep nobody opens. An alert that fires and means nothing. **Seventeen deprecations, the oldest from March 2021.** Every one was tolerated because tolerating it was cheaper that day.

### 4. The hard part is other people, and it is mostly mechanical

**Not a soft-skills coda.** The specific mechanisms:

- **Bus factor 1 is a technical fact with a technical fix** — review, so that more than one person has read it.
- **Psychological safety is what makes review possible**, and **severity labels make it cheap.**
- **"They keep making the same mistake" is answered by a config file**, not a conversation.
- **Blame destroys the information you needed.**
- **The question is never "who broke it?" but "what allowed one ordinary mistake to break it?"**

---

## 5. The One Sentence

If you remember one thing from thirteen weeks:

> **You are not optimising for a program that is correct. You are optimising for a program that can
> be changed by someone who did not write it, years after you have left — and every technique in this
> course is a way of buying that.**

**`roomsvc` is what it costs when nobody buys it.** Twelve lines, four months, two lectures in one room on 14 October 2024.

---

## 6. What Is Left

| | |
|---|---|
| **A 11 and A 12** | **Friday 24 April, 17:00.** A 12 is short and is built on your six retrospectives and your debt register |
| **Dress rehearsal** | **This Thursday, in this room, after the lecture.** Optional, and every team that has used it has been glad |
| **🎤 Demo Day** | **Tuesday 28 April.** Deploy on **Monday**, not on the day. [[CS212 Week8/project/DEPLOYMENT CHECKLIST\|DEPLOYMENT CHECKLIST]] has the list |
| **Code and report** | **Friday 1 May, 17:00.** 3,000–4,000 words. **What you chose not to build, and one ADR you would reverse** |
| **📕 Final exam** | **Friday 8 May, 09:00–11:30.** Comprehensive. **Weeks 11 and 12 appear here and nowhere else** — there was no Quiz 12 |
| **Peer assessment** | With the report. It affects individual marks |

**And the last practical instruction of the course: read your own `git log` before you write the report.** Thirteen weeks, in order, with the messages you wrote at the time. **It is the most honest document your team produced**, it will remind you of three things you have forgotten, and it is what the report's process section is actually about.

---

## 7. Summary

- **Two senior tracks, differing in what your output is** — technical judgement against other people's effectiveness — **and in feedback-loop length: hours-to-weeks against months-to-years.** After a term arguing that short loops are everything, that is the honest difficulty. **The move back is easy at one year, hard at five.**
- **The first two years ask for reading code nobody can explain, changing it safely, and writing the test that makes it safe** — not for designing systems from scratch. **A 9 was the closest simulation available.**
- **Optimise for the codebase and the colleagues.** And ask in an interview: ***"how long from commit to production, and who can deploy?"*** — DORA's lead time and a bus factor, in one question.
- **Four things this course was for:** code you cannot change safely is worthless however correct; **every practice is a claim about cost, in a context, with evidence**; **instrument what you intend to act on, and act on it**; and **the hard part is other people, and it is mostly mechanical.**
- **Four originators disowned what their ideas became** — Fagan's number, Fielding's REST, the Agile Manifesto, Cunningham's debt. **The memorable name travels; the caveats do not.**
- **Keep a decision log of your own**, and read it in a year. It is the only instrument you have for finding out whether your judgement is improving.
- **The one sentence: you are optimising for a program that can be changed by someone who did not write it, years after you have left.**

---

*CS 212 · Week 12 · L39 · the last lecture · © CSE Department*
