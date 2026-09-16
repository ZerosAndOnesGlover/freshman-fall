# CS 212 · Software Engineering
## Week 0 · Lecture 1 of 3
### Why Software Engineering Was Invented

---

**Sat:** first Wednesday of Week 0, 10:00–10:50, TH 200 · **Reading:** Sommerville Ch. 1 · **Next:** L02, process models and what they were reacting to

---

## 1. The Discipline Was Named as a Provocation

In **October 1968**, fifty-odd people met in **Garmisch-Partenkirchen** at a NATO Science Committee conference. The title on the programme was *Software Engineering*, and the people who chose it said afterwards exactly why:

> "The phrase 'software engineering' was deliberately chosen as being provocative, in implying the
> need for software manufacture to be based on the types of theoretical foundations and practical
> disciplines that are traditional in the established branches of engineering."
> — *Software Engineering: Report on a conference sponsored by the NATO Science Committee*, Naur & Randell (eds.), 1969, p. 13

**Read that twice.** The name was not a description of something that existed. It was an accusation that it did not. The report's own participants spent three days agreeing that large programs were routinely late, over budget, unreliable, and — the word appears repeatedly — *unmaintainable*, and that nobody knew why.

**Fifty-eight years later the accusation is only partly answered**, and this course is about the part that has been.

> **What changed and what did not.** We now know a great deal about how to build software that
> *works* — types, tests, review, continuous integration, version control. We know much less about
> how to build software that *is wanted*, on a *predicted* date, for a *predicted* cost. **Weeks 1–11
> are almost entirely the first problem.** Week 12 is honest about the second.

---

## 2. The Word "Crisis" Came From the Same Room

The conference produced a phrase that outlived it. **The software crisis** is the observation, repeated by Dijkstra in his 1972 Turing Award lecture, that our ability to build machines had outrun our ability to program them:

> "The major cause of the software crisis is that the machines have become several orders of
> magnitude more powerful! To put it quite bluntly: as long as there were no machines, programming
> was no problem at all; when we had a few weak computers, programming became a mild problem, and
> now we have gigantic computers, programming has become an equally gigantic problem."
> — Dijkstra, *The Humble Programmer*, CACM 15(10), 1972

**The economic argument in one line:** hardware capability grew exponentially, the size of the programs people wanted grew with it, and the cost of building a program grew *faster than linearly* in its size. That last clause is the whole subject. If a 100,000-line program cost exactly ten times a 10,000-line one, there would be no discipline here — you would just hire ten times as many people.

**Brooks's OS/360** is where the industry learned it does not work that way. IBM's OS/360 consumed roughly **5,000 person-years** and shipped late with, by Brooks's own account, around a thousand known defects per release. His conclusion became the one line of software engineering everyone can quote:

> "Adding manpower to a late software project makes it later."
> — Brooks, *The Mythical Man-Month*, 1975, Ch. 2

**The mechanism matters more than the slogan.** Communication paths between $n$ people grow as $n(n-1)/2$. Going from 4 people to 8 doubles the labour and **more than triples** the pairs who must stay in agreement: 6 pairs becomes 28. Your project team is 4–5 people for exactly this reason, and Week 12 revisits the arithmetic with the term's own data.

---

## 3. What Failure Actually Costs

Abstractions about "quality" are easy to nod at. **Here are six failures, with what went wrong, because the mechanisms recur in this course.**

| System | When | Cost | The engineering cause |
|---|---|---|---|
| **Therac-25** | 1985–87 | **Six massive radiation overdoses, three deaths** | A **race condition** between the operator's keystrokes and the machine's setup routine, reachable only by an operator typing fast enough. Hardware interlocks present on the Therac-20 had been **removed** and replaced by the same software. No independent code review; the software was assumed correct because it was reused |
| **London Ambulance CAD** | 26 Oct 1992 | System withdrawn in 2 days; deaths attributed by inquiry, number disputed | Delivered against a **fixed price and fixed date** by a supplier with no experience of the domain. Load testing was never done at real volume; the system slowed, operators worked around it, the queue grew, and it failed under exactly the conditions it existed for |
| **Ariane 5 Flight 501** | 4 June 1996 | **$370M**, 37 seconds of flight | A 64-bit float converted to a 16-bit signed integer overflowed. The code was **inherited from Ariane 4**, where the value could not overflow, and it was **not needed after liftoff at all** — it was a leftover alignment routine left running for convenience. Both redundant units ran the same software and failed identically, 72 milliseconds apart |
| **FBI Virtual Case File** | 2000–2005 | **$170M written off** | Requirements were never stabilised; the specification reached 800 pages and kept moving. A single big-bang delivery meant the first honest integration was also the last |
| **Knight Capital** | 1 Aug 2012 | **$440M in 45 minutes**; the firm was sold | A deployment updated **seven of eight servers**. The eighth still ran code in which a **repurposed feature flag** now enabled an eight-year-old test routine. There was no automated deployment verification, and the flag's old meaning had never been deleted |
| **Boeing 737 MAX (MCAS)** | 2018–19 | **346 deaths**, aircraft grounded 20 months | A control system taking input from a **single** angle-of-attack sensor, with authority to repeatedly trim the aircraft nose-down. The hazard analysis classified it as less severe than it was, and the change was kept out of the documentation pilots read |

**Four of the six are not coding errors.** They are errors of *process*: what was reviewed, what was tested, what was documented, what was deployed, and who was allowed to decide that a change was small. **This is the course's subject.** You already know how to write a correct function; PROG 102 and CS 201 saw to that. You do not yet know how to stop a correct function from being deployed to seven servers out of eight.

> **Ariane 5 is the one to keep.** Every individual component behaved as specified. The
> specification for the reused component was correct **for Ariane 4**. Nobody re-derived it for a
> rocket with a different trajectory, because reusing working code felt like the safe option.
> **Week 9 is thirteen lectures' worth of the same lesson: code carries its assumptions with it,
> and the assumptions are invisible.**

---

## 4. The Numbers Behind "Maintenance"

The single most consequential fact about professional software is where the money goes.

| Phase | Share of total lifetime cost | Source |
|---|---|---|
| Requirements, design, implementation, first release | **~40%** | Lientz & Swanson (1980); Boehm (1981); Sommerville Ch. 9 |
| **Everything after the first release** | **~60%**, and higher for long-lived systems | *ibid.* |

And of that maintenance share, the breakdown is the surprise:

| Kind of maintenance | Share | What it means |
|---|---|---|
| **Perfective** | ~50% | New features and changed requirements for a working system |
| **Adaptive** | ~25% | The system still does the same thing; the world around it changed — a new OS, a new browser, a new tax rate |
| **Corrective** | **~21%** | Fixing bugs |
| Preventive | ~4% | Changing code that works, to make later change cheaper — i.e. refactoring |

**Only a fifth of "maintenance" is fixing bugs.** Four fifths is *change to software that is working correctly*. That reframes every design decision you will make this term:

> **You are not optimising for a program that is correct. You are optimising for a program that can
> be changed by someone who did not write it, years after you have left.**

**This is why `roomsvc` exists**, and it is why Week 2's principles, Week 9's refactorings and Week 11's debt measurements are not stylistic preferences. They are the difference between a change costing an afternoon and costing a quarter.

---

## 5. The Reference Codebase: `roomsvc`

Every measured claim in this course comes from one of two places: **`roomsvc`**, which exists, or **your team's `slot`**, which will. Both are introduced now and used every week after.

`roomsvc` is the CSE department's **room and equipment booking service**. It is the thing that produces `5. Academic Registry/1. Scheduling/Year2 - Sophomore/ROOM ASSIGNMENTS.md`. It has been in production for six years, written by six people in succession, four of whom have left. Here is what it measures as, on the reference toolchain:

```console
$ cloc --include-lang=Python .
      34 files        1,902 blank        1,455 comment       11,438 code

$ git log --oneline | wc -l
2847
$ git log -1 --format=%cd $(git rev-list --max-parents=0 HEAD)
Tue Feb 11 09:41:06 2020 +0000

$ git shortlog -sn --all | head
  1183  A. Okonkwo          <- left 2023
   702  M. Lindqvist        <- left 2022
   488  R. Teixeira         <- left 2024
   301  J. Park
   126  S. Abadi            <- left 2021
    47  (dependabot)

$ wc -l roomsvc/*.py | sort -rn | head -4
   2814 roomsvc/bookings.py
    986 roomsvc/models.py
    743 roomsvc/views.py
    612 roomsvc/notify.py

$ radon cc -s -n C roomsvc/bookings.py | head -4
roomsvc/bookings.py
    F 291:0 confirm_booking - F (94)
    F 812:0 _resolve_conflicts - E (38)
    F 1455:0 render_week - D (27)
```

**`confirm_booking` is 487 lines long and has a cyclomatic complexity of 94.** That number is the count of linearly independent paths through the function: to exercise every branch once you would need 94 test cases. There are **eleven** tests that touch it.

```console
$ pytest -q
212 passed in 94.31s
$ coverage report --precision=1 | tail -1
TOTAL                        11438   4461   61.0%
$ mutmut results | tail -1
1204 mutants generated, 374 killed (31.1%), 802 survived, 28 timeout
```

**Hold on to the last line.** 61% of the lines are executed by the test suite; **31% of deliberately introduced bugs are caught by it.** Those are two very different numbers measuring two very different things, and Week 6 is entirely about why the gap exists and which number you should believe.

---

## 6. One Bug, Carried All Term

On **14 October 2024**, `roomsvc` scheduled two lectures into **VNC 101** at 09:00. CS 201 and a visiting seminar both had a confirmation email. The room has one projector and 64 seats; the seminar moved to a corridor.

The cause is eight lines, and you can see it without knowing the rest of the codebase:

```python
# roomsvc/bookings.py, around line 291, inside confirm_booking()
existing = db.query(
    "SELECT id FROM bookings WHERE room=? AND slot=? AND state='confirmed'",
    room, slot)
if existing:
    raise RoomUnavailable(room, slot)
...                                    # 40 lines of email, audit log, price calc
db.execute(
    "INSERT INTO bookings (room, slot, owner, state) VALUES (?,?,?,'confirmed')",
    room, slot, owner)
db.commit()
```

**Check, then act.** Between the `SELECT` and the `INSERT` there are forty lines and two network calls, and two web workers ran them at the same time. Both read an empty result; both inserted. **CS 202 is teaching you the word for this in Week 3** — a race on a critical section with no mutual exclusion — and the database has had the right tool since 1975: a unique constraint on `(room, slot)` where `state='confirmed'`, which the schema does not have.

**This bug is the spine of the course.** You will meet it again in:

| Week | What it becomes |
|---|---|
| **W1** | A requirement nobody wrote down: *"a room holds at most one confirmed booking per slot"* is an **invariant**, and it appears in no user story in the issue tracker |
| **W2** | A design failure: `confirm_booking` mixes the rule, the persistence and the email, so the rule cannot be enforced where the data is |
| **W3** | An architecture decision: which layer owns an invariant, and why "the database" is an answer people resist |
| **W5** | A test that cannot be written at the unit level, because the bug does not exist in one process |
| **W6** | A mutant that survives, telling you the test suite never checked the thing that broke |
| **W9** | The first refactoring — and a demonstration that the fix is **one line of DDL**, and that the reason it took two years is not technical |

**It took 23 days to diagnose and 4 months to fix.** Not because it is hard. Because `confirm_booking` is 487 lines long, nobody who wrote it still works here, and the team could not convince itself that a change to it was safe. **That sentence is the course.**

---

## 7. What You Are Building: `slot`

Your team project is **`slot`** — `roomsvc`'s replacement. Full brief in [[CS212 Week0/project/PROJECT BRIEF slot|PROJECT BRIEF slot]]; the parts that matter today:

- **Teams of 4–5**, formed in Thursday's workshop, fixed for the term.
- **Python 3.12, FastAPI, PostgreSQL, Docker, GitHub Actions, pytest.** Not a free choice — the course marks your *engineering*, and thirteen assignments assume one toolchain.
- **Two graded milestones.** Phase 1 in Week 6 (10%): requirements, architecture, a domain model, a green pipeline, and one booking that works end to end. Final on 1 May (30%): demo and report.
- **Everything is in git, on GitHub, from Week 1.** Your commit history is evidence and it is read. A project that arrives as one commit on 30 April has failed the course's actual subject whatever it does when you run it.

> **Why a booking system and not something more exciting.** Because it has a **hard invariant**
> (no double-booking), **contested requirements** (who may cancel whose booking?), **a real domain
> with vocabulary** (slot, resource, reservation, hold, waitlist), and **it already exists**, so
> every week can compare your decision with a decision someone made in 2020 and had to live with.
> Excitement is not a design input. Maintainability is.

---

## 8. What This Course Is Not

Three honest disclaimers, made now so you can calibrate.

1. **It is not a programming course.** You will write less code this term than in PROG 201. The code you write will be read more.
2. **Its claims are weaker than they sound.** Software engineering has a real empirical literature — and it is much thinner than the confidence of its textbooks implies. The Standish *CHAOS* reports, the source of "only 31% of projects succeed", have had their methodology heavily criticised (Jørgensen & Moløkken, 2006: the sampling is self-selected and the definition of "failure" includes any schedule overrun). **When this course gives you a number, it names where the number came from, and you should ask.**
3. **Much of what you will be told in industry is folklore.** "Comments should explain why, not what" is good advice with almost no empirical support. "Code review finds 60% of defects" comes from a handful of studies of 1970s-style formal inspections at IBM and HP, not from GitHub pull requests. **Week 7 shows you what the evidence for review actually is**, and it is both weaker and more interesting than the slogan.

**The stance this course asks for:** treat every practice as a claim about cost, in a context, with evidence. Adopt it if the evidence and the context hold. **A 0 asks you to do exactly that to the Agile Manifesto**, which is the most-quoted and least-read document in the field.

---

## 9. Summary

- **"Software engineering" was coined at NATO Garmisch in 1968 as a provocation**, naming a discipline that did not yet exist because large software was routinely late, broken and unmaintainable.
- **The crisis is an economics problem**: cost grows faster than linearly in size, and Brooks's $n(n-1)/2$ communication paths are one reason why.
- **Six named failures**, and four of them were process failures rather than coding errors. Ariane 5 reused correct code whose assumptions had silently changed.
- **~60% of lifetime cost is after first release**, and only ~21% of that is bug fixing. **You are optimising for changeability, not for correctness.**
- **`roomsvc`** is the reference codebase: 11,438 lines, 2,847 commits, a 487-line function with complexity 94, 61% coverage and a **31% mutation score**.
- **The VNC 101 double-booking of 14 Oct 2024** is a check-then-act race that took 23 days to find and 4 months to fix — and the fix is one line of DDL. **It recurs in Weeks 1, 2, 3, 5, 6 and 9.**
- **Your project is `slot`**, `roomsvc`'s replacement, in teams of 4–5, for the whole term.

**Next:** L02 — process models, and what each one was reacting to. Including the fact that the paper universally cited as inventing the waterfall model spends its second page arguing that it does not work.

---

*CS 212 · Week 0 · L01 · © CSE Department*
