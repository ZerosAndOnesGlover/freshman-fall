# Year 2 Registry Reconciliation

What was wrong with the Year 2 scheduling files before any course content was written, and what was
done about it. Written 2026-08-09, before CS 201 was started.

**The authority** is
`5. Academic Registry/1. Scheduling/Year2 - Sophomore/CSE_Year2_Sophomore_Curriculum.docx`,
except where noted below.

---

## 1. Two timetable grids were structurally broken

`FALL SCHEDULE.md` and `SPRING SCHEDULE.md` each had one row that had lost its leading `| **HH:MM** |`
cell and had its `<br>` separators replaced by real newlines, so the lab row rendered as loose text
under the table rather than inside it.

The Daily Breakdown prose in both files survived intact, and was used to reconstruct the rows.

## 2. Reconstructing them exposed two real clashes

Not cosmetic — in both cases a student could not attend both sessions.

| Clash | Resolution |
| --- | --- |
| CS 211 lectures Tue/Thu 09:30–10:45 against PROG 201 Tue/Thu 10:00–10:50 (45 min, twice weekly) | CS 211 moved to **Tue/Thu 08:30–09:45**. Tue/Thu 08:30 was empty — CS 201 holds that slot Mon/Wed/Fri only — so nothing else had to move, and CS 211 keeps its 2 × 75-minute format. |
| Spring Friday afternoon stacked ECE 211 lecture 13:00–14:15, PROG 202 lab 14:00–15:50 and CS 290 seminar 15:00–15:50 | PROG 202 lab moved to **Wed 13:00–14:50**, free until the MATH 251 recitation at 15:00. Friday clears completely, and ECE 211 and CS 290 stay where `ROOM ASSIGNMENTS.md` already put them. |

Both moves were propagated to `MASTER TIMETABLE.md`, `ROOM ASSIGNMENTS.md` and the Daily Breakdown
and weekly-deadline tables. `OFFICE HOURS.md` needed no change — no instructor's hours touch either
slot.

A residual overlap is **left in place**: PROG 202 lectures run Tue/Thu 11:00–12:15, fifteen minutes
into the protected lunch block. Fixing it would have required moving a third course, and a 15-minute
encroachment twice a week is not a scheduling failure in the way a 45-minute lecture collision is.

## 3. Two course titles were wrong

`MASTER TIMETABLE.md` called CS 211 *"Programming Languages Theory"* and MATH 251
*"Probability & Statistics"*. Both are the Year 1 docx's **Year 2 preview table** wording, and both
are wrong. The Year 2 docx — authoritative for its own year — says *Programming Languages &
Compilers I* and *Probability & Statistics for Computer Science*.

`DEGREE REQUIREMENTS.md` already had both correct and needed no change.

## 4. The midterms sat in the wrong weeks

The docx assigns each midterm to a specific week **inside that week's own assignment list**, with
stated coverage. `ASSESSMENT CALENDAR.md` and `0. Institution/ACADEMIC CALENDAR.md` instead stacked
all four Fall midterms into Week 6 and all the second midterms into Week 10, with wider coverage
than the docx claims.

The docx wins. Exams moved to the weeks it names, and both calendars were rewritten to match.

| Course | Was | Now |
| --- | --- | --- |
| PROG 201 Midterm 1 | W6, Oct 7 | **W4**, Sep 22 · Weeks 0–3 |
| CS 211 Midterm 1 | W6, Oct 7 | **W4**, Sep 23 · Weeks 0–3 |
| CS 201 Midterm 1 | W6, Oct 6 · Weeks 0–5 | **W5**, Sep 29 · Weeks 0–4 |
| PROG 201 Midterm 2 | W10, Nov 4 | **W8**, Oct 20 · Weeks 4–7 |
| CS 211 Midterm 2 | W10, Nov 4 | **W8**, Oct 21 · Weeks 4–7 |
| CS 202 Midterm 1 | W6, Mar 2 · Weeks 0–5 | **W4**, Feb 9 · Weeks 0–3 |
| CS 202 Midterm 2 | W10, Apr 13 | **W8**, Mar 9 · Weeks 4–7 |

MATH 241, MATH 251, ECE 211, CS 212 and PROG 202 keep the registry's Week 6 / Week 10 exam weeks —
the docx says nothing about them, and silence is not conflict.

A side effect worth having: no week now carries four evening exams.

## 5. The week-to-date mapping did not exist, and the two calendars disagreed

`ASSESSMENT CALENDAR.md` was internally inconsistent — it placed Week 1 at Sep 8 and Week 6 at
Oct 6, which are four weeks apart, not five. A **Week-to-Date Map** has been added at the top of
that file, derived from the institutional calendar's fixed anchors (classes begin Wed Aug 27; Labor
Day Sep 1; Fall Break Oct 13; Spring Break Mar 16) and checked against the project due dates that
both files already agreed on (Oct 31 = W9 Friday, Nov 14 = W11 Friday).

Thirteen teaching weeks from Aug 27 end on Nov 21, while the institutional calendar names Dec 8 as
the last week of instruction. The intervening weeks are Thanksgiving recess plus a
**project-completion and demo period**, which is where Project 2 and the Week 12 demo days actually
land. This is now stated rather than left as a gap.

**Course material should quote week numbers, never dates.** The map is the only place the
conversion lives.

## 6. Quizzes were described as weighted; they cannot be

`MASTER TIMETABLE.md` gave weekly quizzes 5–10% with "lowest 2 dropped", and `COURSE POLICIES.md`
repeated the drop rule. But every Year 2 course's stated components already reach 100% without a
quiz line — CS 201 is Problem Sets 35 + Midterms 25 + Final 20 + Projects 20, and the other nine are
the same shape. There is no weight available to give.

Year 2 therefore follows the **ECE 110 precedent**: quizzes are written, sat, and self-marked
against a key printed in the paper, and they stay out of the gradebook.

The same argument applies to **labs**, which no Year 2 course's split makes room for either. They
are checked off by the TA in the session and enforced by the attendance rule in `COURSE POLICIES.md`
— a second unexcused absence costs a letter grade. CS 102 in Year 1 already works this way.

Both are recorded in `2. Gradebook/Year2 Sophomore/<term>/_<COURSE> Lab and Quiz Record.md`.

Also corrected: the quiz range read "Weeks 2–14" in a term whose last week is 12. The docx numbers
Quiz *N* in Week *N*, so the range is **Weeks 1–11**, and **Quiz *N* covers Week *N−1***.

## 7. Year 2 had no gradebooks, no submissions folders and no transcript rows

Created:

- Ten gradebooks under `2. Gradebook/Year2 Sophomore/`, all parsing, all summing to 100%.
- Nine lab-and-quiz records alongside them. CS 290 has none — it is a one-credit seminar whose
  participation mark *is* weighted, at 40%.
- Ten course folders under `4. Submissions/Year2 Sophomore/`, numbered to match the vault.
- Year 2 Fall and Spring sections in `3. Transcript/TRANSCRIPT.md`.

`python3 tools/gpa.py` reports Fall 16 credits and Spring 18, matching the docx's stated 34, and
`--self-test` still passes 38/38.

---

## Not Done

- **Years 1, 3 and 4 carry the same "Weeks 2–14" template text**, and Year 3's schedule grids have
  the same broken lab rows Year 2's had. Left alone deliberately: Year 1's quiz-to-week convention
  differs per course — CS 102 and MATH 142 use Quiz *N* → Week *N−1*, PHYS 141 uses Quiz *N* →
  Week *N*, and ECE 110 numbers after the material — so a blanket edit there would introduce errors
  rather than remove them.
- **`ECE 110.md` has no `<!-- BEGIN COMPUTED -->` markers**, so `gpa.py --write` silently skips its
  Computed block. Every other gradebook has them. Not fixed here because it is a Year 1 defect and
  unrelated to this pass.
