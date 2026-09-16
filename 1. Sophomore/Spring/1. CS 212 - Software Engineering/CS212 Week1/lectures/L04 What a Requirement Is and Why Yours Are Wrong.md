# CS 212 · Software Engineering
## Week 1 · Lecture 1 of 3
### What a Requirement Is, and Why Yours Are Wrong

---

**Sat:** Tuesday of Week 1, 10:00–10:50, TH 200 · **⚠️ Quiz 1 in the first ten minutes** — covers Week 0 · **Reading:** Sommerville Ch. 4 §4.1–4.3 · **Next:** L05, user stories

---

## 1. The Cheapest Defect and the Most Expensive One

Boehm's curve (W0 L02 §3) says a requirements defect found in production costs ~100× what it costs when found in requirements. **Requirements are where the leverage is, and they are also where nobody wants to spend time**, because writing them feels like not-working.

**The FBI's Virtual Case File was cancelled after $170M**, and its post-mortems agree on the cause: the requirements never stabilised, the specification grew past 800 pages, and the first honest integration was also the last. **No amount of implementation skill recovers from that.**

So: what *is* a requirement, and how do you write one that is worth the leverage?

---

## 2. The Four Categories, and the One That Kills Projects

| Kind | What it constrains | `slot` example |
|---|---|---|
| **Functional** | What the system does | *"A user can cancel a booking they own."* |
| **Non-functional (quality)** | How well it does it | *"The week view renders in under 300 ms at the 95th percentile with 500 bookings loaded."* |
| **Constraint** | What you are not free to choose | *"Authentication uses the university SSO."* |
| **Invariant** | What must **never** be true, at any moment, regardless of what anyone does | **"A resource has at most one confirmed booking per slot."** |

**The fourth one is not in Sommerville and it is where `roomsvc` died.**

An invariant is not a feature and it does not appear in a feature list, because it is not something the system *does* — it is something the system *is*. Nobody writes a story called *"as a user I want the room not to be double-booked"*, because it never occurs to anyone that it could be. **It lived in `roomsvc`'s issue tracker as precisely zero issues until 14 October 2024**, and then as issue #1247.

> **How to find your invariants.** For each entity in your domain, ask: **what sentence, if it ever
> became false, would mean the system had lied to somebody?** Write those sentences down, in
> `docs/domain-model.md`, in the section called *Invariants*. **You will find three to six for
> `slot`**, and the interesting question for each is not "how do we check it" but **"where is it
> enforced?"** — which is Week 3.

**Non-functional requirements have a related failure**, which is being unfalsifiable. *"The system shall be fast"* is not a requirement; it is a mood. **A non-functional requirement is only a requirement if you can write the test.** Every one in your Phase 1 must name a number, a percentile and a load.

---

## 3. Requirements Are Discovered, Not Collected

The verb "gather" does enormous damage. It implies the requirements exist, in stakeholders' heads, whole, and the analyst's job is transport.

**They do not exist yet.** Four reasons, in increasing order of how badly they bite:

1. **People describe the process they have, not the outcome they want.** Ask the departmental administrator what they need and you will be told about the spreadsheet. The spreadsheet is a workaround for `roomsvc` being slow. **Ask what they are trying to achieve and the answer changes.**
2. **Tacit knowledge is invisible to its holder.** Nobody will tell you that a lecture slot cannot start at 09:30, because everybody already knows. **These are exactly the rules your system will violate**, and you find them by watching, not asking.
3. **Preferences are constructed during the asking.** This is a robust finding in behavioural research and it applies directly: the answer you get depends on the order and framing of your questions. **Two teams interviewing the same administrator will get different requirements**, and neither is lying.
4. **Stakeholders conflict, and the conflict is not stated.** It shows up as vagueness. §5.

**The consequence for your project:** you cannot do requirements in Week 1 and be done. What you do in Week 1 is form hypotheses; what makes them requirements is contact with somebody who has to use the thing. **The report in May asks which of your requirements changed, and a set that never changed is a set that was never tested.**

---

## 4. Elicitation: Four Techniques and What Each Is Blind To

| Technique | Good for | Blind to |
|---|---|---|
| **Interview** | Goals, history, why the current system is hated | Tacit rules; anything the interviewee thinks is obvious; what they actually do as opposed to what they say |
| **Observation** | The workarounds — the spreadsheet, the WhatsApp group, the sticky note on the monitor | Rare cases; anything that happens once a term; why |
| **Document analysis** — forms, policies, the existing system | Hard rules, legal constraints, the real vocabulary | Which rules are still enforced. Half the policy document is dead letter and nobody will tell you which half |
| **Prototype / mock-up** | Reactions. People cannot specify an interface but can criticise one instantly | Scale, performance, anything about the long run |

**The highest-yield question in an interview**, and it is not a requirements question:

> **"Tell me about the last time this went wrong."**

Failures are memorable, specific, and unrehearsed. They surface the edge cases, the workarounds, and the political conflict in one answer. **You get more from that question than from twenty minutes of "what would you like the system to do".**

**Second-highest:** *"What do you do when the system is down?"* — which is where the real process lives, unmediated by the software.

---

## 5. Ambiguity Is Usually Unresolved Conflict

Consider this, from `roomsvc`'s actual issue tracker (#812, open since 2022):

> *"Admins should be able to cancel bookings."*

Seven words, at least five questions:

| Question | Why it matters |
|---|---|
| **Any** booking, including one that has already started? | Someone is in the room right now |
| **Whose** bookings — everyone's, or only their own department's? | This is a political question wearing a technical costume |
| Is the owner **notified**? How, and how far ahead? | Week 8's deployment of an email you cannot recall |
| Can it be **undone**? | Determines whether cancellation is a state change or a deletion, which is a schema decision |
| **Why** does an admin need this? | The actual answer, from the administrator: *"because when a room floods we need to clear it"* — which is a **different feature**, and one that should cancel a whole day at once |

**The last row is the pattern.** The vague requirement is vague because the person who wrote it was summarising a conversation in which two people wanted different things. *"Should be able to cancel"* is what you write when the registrar wants control and the lecturer wants not to be overridden, and nobody settled it.

> **The rule: when a requirement is vague, look for the two stakeholders.** Then get them to
> disagree explicitly, in front of you. **An argument in Week 1 is cheap; the same argument in
> Week 10 is a schema migration.**

**`slot` has four stakeholders with genuinely conflicting interests**, and you should be able to name them by Friday: the **registrar** (control, auditability), the **lecturer** (speed, certainty), the **student** (visibility), the **facilities team** (they unlock the doors, and they need to know by 17:00 the day before). Every requirement that feels vague to you is probably two of them disagreeing.

---

## 6. Traceability, and Why You Want a Lightweight Version

**Traceability** is the ability to answer, for any line of code, *which requirement is this for?* — and for any requirement, *where is this implemented and tested?*

In regulated work it is mandatory and heavy: DO-178C requires bidirectional traceability from every requirement through design to code to test, audited. **You are not doing that.** But the cheap version costs almost nothing and pays back in Week 11:

```
feat(bookings): reject overlapping confirmed bookings

Closes #14.
```

**That is traceability.** The issue holds the story and the acceptance criteria; the commit holds the code; `git log --grep '#14'` connects them; and in April, when someone asks *"why does this reject 09:00–09:50 against 09:50–10:40?"*, the answer exists.

**What it buys you concretely**, and this is measurable in `roomsvc`: it has 2,847 commits and **412 of them reference an issue — 14%**. For the other 86%, the reason is gone. **Week 11's debt register can only be written about the 14%.**

---

## 7. How Much Requirements Work Is Enough

The honest answer is: **enough to know what you are building next, and what you would have to un-build if you are wrong.**

A usable heuristic, and it is the spiral model wearing work clothes (W0 L02 §4):

> **Specify in detail only what you will build in the next two weeks. For everything further out,
> record the decision that would be expensive to reverse, and nothing else.**

For `slot`, the expensive-to-reverse decisions are known now and you should write them down this week even though you will not build them for a month:

| Decision | Why reversal is expensive |
|---|---|
| **Does a booking belong to a person or to a course?** | It is in every foreign key. Changing it in Week 9 is a migration plus every query |
| **Are recurring bookings stored as one row with a rule, or as N rows?** | Determines whether "cancel one week of a recurring booking" is easy or impossible |
| **Is cancellation a state change or a delete?** | Determines whether you can answer "who cancelled this and when", which the registrar will eventually require |
| **What is the unit of time?** | 50-minute slots, or arbitrary intervals? Everything downstream depends on it |

**The fourth one is a trap and it is worth sixty seconds.** "Arbitrary intervals" sounds more general and therefore better. It is not: it makes the double-booking invariant an *overlap* check rather than an *equality* check, which no unique index can express, which puts you back in `confirm_booking`'s position. **The constrained model is enforceable by the database; the general one is not.** That is a real engineering trade and W3 comes back to it.

---

## 8. Summary

- **Requirements defects are the most expensive to fix late**, and the FBI VCF is what unbounded requirements churn costs.
- **Four kinds**: functional, non-functional, constraint — **and invariant**, which is the one that is never written down and the one that killed `roomsvc`. Find yours by asking what sentence, if false, would mean the system had lied.
- **A non-functional requirement without a number, a percentile and a load is a mood, not a requirement.**
- **Requirements are discovered, not gathered**: people describe their workaround, tacit rules are invisible to their holders, preferences are constructed while you ask, and conflict hides as vagueness.
- **The highest-yield interview question is *"tell me about the last time this went wrong"*.**
- **Vagueness is usually two stakeholders disagreeing.** `slot` has four, with real conflicts: registrar, lecturer, student, facilities. **Have the argument in Week 1.**
- **Cheap traceability is an issue number in a commit message.** `roomsvc` has it on 14% of commits, and the reason for the other 86% is gone.
- **Specify in detail two weeks out; for everything else, record only the expensive-to-reverse decisions.** For `slot` there are four, and the one about time units decides whether your invariant is enforceable at all.

**Next:** L05 — user stories, acceptance criteria, and why the story format is worth less than the conversation it is supposed to trigger.

---

*CS 212 · Week 1 · L04 · © CSE Department*
