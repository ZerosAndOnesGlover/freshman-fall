# CS 212 Scheduling Notes

What had to be decided before CS 212 could be written, and why each decision went the way it did.
Written 2026-09-16, while building Week 0. **The authority** is
`5. Academic Registry/1. Scheduling/Year2 - Sophomore/CSE_Year2_Sophomore_Curriculum.docx`, and
where the registry's own scheduling files settle a question, they do.

---

## 1. Three lectures, no lab, and a project that has to carry the practical weight

[[Year2 - Sophomore/ROOM ASSIGNMENTS|ROOM ASSIGNMENTS]] puts CS 212 on **Tue/Wed/Thu 10:00–10:50 in
TH 200** (capacity 80, projector and whiteboard) and gives it **no laboratory slot**. The curriculum
agrees: CS 212 is 3 credits, not 4, and its practical line reads *"Team project (4–5 students, full
semester)"* rather than a lab.

**This is the first Year 2 course with no scheduled practical session**, and it changes what the
weekly folder can contain. CS 201, PROG 201, CS 202 and PROG 202 each have a `lab/` directory whose
sheet is checked off by a TA in a supervised two-hour slot. CS 212 has no such slot, no TA on record,
and no room booked outside the three lecture hours.

**The decision: `project/` replaces `lab/`, and it is not a weekly deliverable.** A lab sheet is
sat and finished in one sitting. The team project runs for thirteen weeks and is examined twice. So:

| | A lab | CS 212's project |
|---|---|---|
| Sat | In a booked slot, supervised | In the team's own time |
| Finished | That afternoon | Week 6 and again May 1 |
| Checked | TA tick, unmarked | **Two graded milestones, 40% of the course** |
| Folder | Every week | **Only the weeks with a milestone or a required artefact** |

`project/` appears in **Weeks 0, 1, 3, 6, 8, 11 and 12** and nowhere else. Every other week's
practical work is the individual assignment.

**Consequence for the student-facing README:** CS 212's week pages must not print the
*"Labs and quizzes carry no weight"* box the other four courses print, because half of it is false
here. **Quizzes carry no weight. The project carries 40%** — the largest single component in any
Year 2 course.

---

## 2. Week 0 has six slots for three lectures, and the fourth is the team-formation workshop

Week 0 spans **Mon Jan 12 – Fri Jan 23** ([[ACADEMIC CALENDAR]]: *"Mon Jan 12 — Spring semester
begins (Week 0)"*, *"Fri Jan 23 — Add/Drop deadline; Week 0 ends"*). A Tue/Wed/Thu course therefore
has **six** slots in Week 0: Jan 13, 14, 15, 20, 21, 22.

**CS 202 met the same surplus and recorded a contradiction in the registry** — ASSESSMENT CALENDAR
says both *"classes begin on a Wednesday"* and *"Week 0 spans Jan 12 to Jan 23"*, and in Spring those
are two days apart ([[CS 202 Scheduling Notes]] §2). **CS 212 inherits the contradiction and resolves
it the same way**: start on the first Wednesday, stay inside the date range, edit nothing.

| Slot | Date | Used for |
|---|---|---|
| Wed | **Jan 14** | L01 — Why Software Engineering Was Invented |
| Thu | **Jan 15** | L02 — Process Models, and What They Were Reacting To |
| Tue | **Jan 20** | L03 — The Agile Manifesto, Read Critically |
| Wed | **Jan 21** | *(free — A 0 is released at 17:00)* |
| **Thu** | **Jan 22** | **Team Formation Workshop**, 10:00–10:50, TH 200 |
| Tue | Jan 13 | *(not used — before the first Wednesday)* |

**Why the workshop is last and not first.** Teams of 4–5 are stuck with each other for thirteen
weeks, and the add/drop deadline is **the following morning, Fri Jan 23**. Holding the workshop on
the last Thursday means every student has seen all three lectures and the project brief before
committing, and can still drop the course the next day. Holding it first would have teams formed by
people who had not yet been told what the project is.

**The workshop is not a lab.** It is unmarked, has no sheet to hand in, and its only output is a
team roster committed to the course organisation on GitHub. It lives in `project/`, not in a
`lab/` directory that does not exist.

---

## 3. CS 212 sets assignments, not problem sets, and the registry says so twice

[[Year2 - Sophomore/ASSESSMENT CALENDAR|ASSESSMENT CALENDAR]]'s W0 row carries the note
*"CS 212 runs assignments, not problem sets"*, and [[CS 212]] repeats it: *"CS 212 has no laboratory
section and sets assignments rather than problem sets."*

**The difference is not cosmetic.** A problem set in CS 202 or MATH 251 is a paper of questions with
a mark scheme. A CS 212 assignment is **a change to a codebase plus the argument for it** — a pull
request, a commit series, a pipeline that runs. Twelve of the thirteen produce something that must
build.

**Release and due dates follow the general rule anyway** — released **Wednesday 17:00 of their own
week**, due **Friday 17:00 of the week after** — because the rule is the registry's and CS 212 was
given no exemption from it. A 0 is released Wed Jan 21 and due Fri Jan 30.

**A 12 is the exception**, and it is the same exception every Year 2 course takes: **A 11 and A 12
are both due Friday Apr 24**, the last teaching day. A 12 is a retrospective, written after the
final demo is in sight, and is deliberately short.

**The lowest assignment mark is dropped** ([[CS 212]]'s component table). Thirteen assignments, twelve
counted.

---

## 4. Quizzes are on Tuesday, because Tuesday is this course's first lecture of the week

[[_CS 212 Quiz Record]] says *"Ten minutes at the start of the course's first lecture of the week,
Weeks 1–11"*, and the SPRING SCHEDULE's Tuesday block marks
*"10:00 – 10:50 📖 CS 212 Lecture — ⚠️ QUIZ DAY for CS 212 (Weeks 1–11)"*.

**So CS 212's quiz day is Tuesday, not Monday.** CS 202's is Monday, PROG 202's is Tuesday. The quiz
papers in `assignments/` are named for the day they are sat — `QUIZ 1 Week 1 Tuesday.md` — so that a
student holding two courses' papers can tell them apart without opening either.

**Quiz *N* is sat in Week *N* and covers Week *N−1*.** Eleven quizzes, Weeks 1–11. **Nothing covers
Week 11 or Week 12**; the Quiz Record says so and the final is where that material is examined.

---

## 5. Week 6 is the heaviest week in the Spring term, and three of its four events are CS 212's

The registry puts all of this in the week of **Mar 2**:

| Date | Event | Course |
|---|---|---|
| Mon Mar 2 | Midterm 1, 18:00–19:15 | MATH 251 |
| **Tue Mar 3** | **Team Project Phase 1 presentation**, in class | **CS 212** |
| **Wed Mar 4** | **Midterm, 18:00–19:15** | **CS 212** |
| Wed Mar 4 | Midterm 1, 20:00–21:15 | ECE 211 |
| Thu Mar 5 | Midterm, 18:00–19:15 | PROG 202 |
| Fri Mar 6 | Problem Set 5 due, all courses | ALL |

**CS 212's presentation and its midterm are on consecutive days**, and the midterm shares its evening
with ECE 211's. Nothing here can be moved — every date is in both ACADEMIC CALENDAR and ASSESSMENT
CALENDAR, and four other courses are pinned around them.

**Two consequences were built into the material rather than argued about:**

1. **Phase 1 is assessed on the walking skeleton, not on the demo's polish.** The rubric in
   `CS212 Week6/project/` gives 70 of 100 marks to artefacts that exist in the repository before
   the presentation — the domain model, the architecture decision records, a green pipeline, and one
   end-to-end booking. **10 minutes of stage time cannot be worth 10% of a course**, and making the
   repository carry the mark is what lets a team rehearse for twenty minutes instead of an evening.
2. **A 6 is the lightest assignment of the term.** It is released Wed Mar 4 — the evening of the
   midterm — and is due Fri Mar 13. It asks for one coverage report and one mutation run on code the
   team already has.

**Quiz 6 is still sat on Tue Mar 3**, ten minutes before the presentations start. It is unmarked and
prints its own key, so it costs the room ten minutes and nobody any preparation.

---

## 6. Spring Break falls between Weeks 7 and 8 and removes no CS 212 slot

**Mon Mar 16 is Spring Break — NO CLASSES**, and the week that follows opens Week 8 on Mon Mar 23.
Because the break is a whole week rather than a day inside a teaching week, **CS 212 loses no Tuesday,
Wednesday or Thursday.** Thirteen weeks, thirty-nine lecture slots, thirty-nine lectures.

**A 7 spans the break** — released Wed Mar 11, due Fri Mar 27 — which is a sixteen-day window rather
than the usual nine. It is the peer-review assignment, and it needs a classmate's pull request to
review, so the extra time is spent waiting for other people rather than working. **A 8 is released on
schedule on Wed Mar 25**, two days after the break ends.

---

## 7. The two Mondays in the Spring term that fall on holidays never mattered here

MLK Day (**Mon Jan 19**, inside Week 0) and Presidents Day are recorded by [[ACADEMIC CALENDAR]] as
open decisions for Year 1 and are not mentioned at all for Year 2. **CS 212 does not meet on Mondays**,
so the question never reaches this course. It is recorded here only so that a later reader does not
go looking for a decision that was never needed.

---

## 8. The course has a reference codebase, and it is the same shape of decision as CS 202's reference machine

CS 202, PROG 201 and MATH 241 each fixed a **reference machine** in Week 0 so that every measured
number in every lecture came from one place and could be reproduced. **CS 212 needs the same thing for
a different kind of measurement**: it is a course about reading and changing code that already
exists, and a lecture that says *"this function is too long"* about no particular function teaches
nothing.

**The reference codebase is `roomsvc`** — the CSE department's room and equipment booking service,
introduced in L01 §5 and used in every week after it. Its numbers are fixed in Week 0 and must not
drift:

| Measurement | Value | Tool |
|---|---|---|
| Lines of Python | **11,438** across 34 files | `cloc` |
| Commits | **2,847**, first on 2020-02-11 | `git log --oneline \| wc -l` |
| Contributors | **6**, of whom **4** have left the department | `git shortlog -sn` |
| Largest module | **`bookings.py`, 2,814 lines** | `wc -l` |
| Worst function | **`confirm_booking`, 487 lines, cyclomatic complexity 94** | `radon cc -s` |
| Test suite | **212 tests, 94 s, 61% line coverage** | `pytest`, `coverage` |
| Mutation score | **31%** — 1,204 mutants, 374 killed | `mutmut` |
| Open issues | **143**, median age **291 days** | GitHub API |
| Bus factor on `bookings.py` | **1** — one departed author wrote 78% of surviving lines | `git blame` |

**The famous incident is the double-booking of VNC 101 on 2024-10-14**, when two lectures were
scheduled into one room by a check-then-act race in `confirm_booking`. It is introduced in W0 L01,
diagnosed in W2, designed away in W3, tested for in W5–W6, and is the first thing the Week 9
refactoring removes. **It is one bug carried across the whole term on purpose.**

**The team project, `slot`, is `roomsvc`'s replacement.** The frame of the course is that you spend
thirteen weeks reading the thing that exists and building the thing that replaces it — which is what
the job actually looks like, and which gives every principle a codebase to be true or false about.

**The reference toolchain** is the same machine the other Year 2 courses measured on — Intel i5-8250U,
Ubuntu 24.04.4, kernel 7.0 — running Python 3.12.3, pytest 8.2.0, coverage 7.5.1, hypothesis 6.100.1,
mutmut 2.5.0, ruff 0.4.4, mypy 1.10.0, Docker 26.1.3 and git 2.43.0. **Versions are printed in the
syllabus** because three of these tools change their defaults between minor releases, and a student
whose coverage number differs by two points should be able to find out why.

---

## 9. No staff are on record, and none were invented

[[Year2 - Sophomore/OFFICE HOURS|OFFICE HOURS]] is titled **"YEAR 2 OFFICE HOURS — FALL"** and names
nobody for any Spring course. CS 212 follows MATH 241 §4 and CS 202 §5: **the syllabus says the staff
are not yet listed** and points at the Engineering Help Desk in BH 120, whose hours OFFICE HOURS does
give.

**CS 212 has a second gap the other courses do not**: with no lab there is no TA, and the assignments
assume someone reviews pull requests. **A 7 is peer review by design** — a classmate's pull request,
against a published checklist — which is both the week's topic and the answer to the staffing gap.
Phase 1 and the final demo are assessed by the instructor.

**This is an omission, not a decision.** When Spring staff are assigned, the syllabus's *Schedule*
table is the one place to update.

---

## 10. What the curriculum's Week 12 says, and what was built

The docx's Week 12 line is *"Team Project Presentations; Engineering Management; Career Paths"*, and
the registry puts the **final team project on Fri May 1** — a week after Week 12 ends on Fri Apr 24 —
and the **final exam on Fri May 8, 09:00–11:30**.

**So the presentations cannot be in Week 12.** Week 12 teaches the three topics and holds the
dress rehearsal; **Demo Day is Tue Apr 28, in the completion period**, alongside CS 202's Lab 12 and
PROG 202's Project 2. The written report is due with the code at **17:00 on Fri May 1**.

**Week 12 is therefore the only week whose `project/` folder describes work sat outside it.** Its
README says so at the top rather than leaving a student to infer it from two dates in different files.

---

*Build record · not student-facing · CS 212 · Year 2 Spring*
