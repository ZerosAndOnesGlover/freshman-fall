# MATH 142 — Calculus II: Integration Techniques and Series — Course Audit

**Question:** Do the labs, problem sets and quizzes of each week need mathematics or tools that the
lectures have not yet taught? Are any of them larger than they need to be?

**Method:** Same as the Fall MATH 141 audit.
- Each week's three lectures were read against its problem set, lab and quiz.
- A scan for every later-week topic (by parts … Runge–Kutta) was run over every deliverable. Each hit
  was read in context. Every hit was a false positive: "improper *fraction*", the Week 7 integral-test
  "remainder", or "system" in its ordinary sense.
- MATH 141 (Fall) counts as taught.
- The Python used in the labs was checked against what CS 101 taught.

**Timing conventions (re-based to 18 Jan 2027):**
- Lectures run Mon, Tue and Fri at 11:00, which is what the lecture files, ROOM ASSIGNMENTS and the
  timetable say. The weekly overviews said "Wednesday" for Lecture 3.
- **Quiz *N*:** Monday of Week *N*, 11:00–11:15, covering Week *N−1*. The ungraded Quiz 00 is Mon
  18 Jan, 11:00–11:25.
- **PS *N*:** released Friday of Week *N* at 12:00, after Lecture 3; due the following Friday at
  17:00.
  - PS 0 is compressed: released Mon 18 Jan, due Fri 22 Jan.
  - PS 12 is an ungraded diagnostic.
- **Lab *N*:** Wednesday of Week *N+1*, 15:00–16:50.
- **Exams:**
  - Midterm 1: Wed 3 Mar, 18:00–19:15.
  - Midterm 2: Wed 31 Mar, 18:00–19:15.
  - Final: Tue 20 Apr, 09:00–11:30.

---

## Summary

**The mathematics is well ordered.** No problem set or quiz needs a later week's lecture. The
problem sets cross-reference earlier weeks explicitly, e.g. "partial fractions first (Week 2)" and
"the integral is one you met in Week 1".

Lab 00 uses Simpson's rule, which MATH 141 never taught (Fall removed it from MATH 141's Lab 09 for
that reason). Here it is fine: Lab 00 gives all three rules in full, and every later lab that uses
Simpson points back to Lab 00.

The real problems were tools and scheduling:

| Finding | Fix |
| --- | --- |
| **Labs 2–12 require `sympy`, `mpmath` and `matplotlib`**, which no course teaches. Labs 1 and 3 give code; the rest assume the libraries. | A **SymPy box** in Lab 02 and an **mpmath box** in Lab 03 list every call any lab uses. Labs 4–12 point to them, and Lab 01 explains `Fraction` in one line. Lab 11's slope field is now a hand sketch from a printed table of slopes (the matplotlib requirement is gone). Any "numerical quadrature" may use the student's own Lab 00 Simpson rule. |
| **The problem sets were "released Wednesday, due Wednesday at the start of class", but MATH 142 has no Wednesday class.** The overviews also put Lecture 3 on Wednesday. | Fri → Fri, dated; overviews say Friday. |
| **There was no lab slot at all** in the Spring timetable, although the syllabus has 13 two-hour labs. | Wed 15:00–16:50, a free slot, placed after each week's three lectures. |
| **Midterm 1 was "Week 5"** in the course, but the registry says Wed 3 Mar (Week 6). | Moved everywhere: overviews, lectures, summaries, quizzes, keys, revision guide. Scope stays Weeks 0–4, as in the gradebook. |
| **Registry disagrees with the course and gradebook.** The ASSESSMENT CALENDAR showed Midterm 1 at 20% and the final at 40%, and had **no Midterm 2**. The gradebook and syllabus say 15/15/20. | The regenerated calendar takes weights from the gradebook and lists Midterm 2 (Wed 31 Mar). |

Problem sets are already 100 points with 16–18 items, in line with Fall's MATH 141 after its cut.
They were not trimmed further.

---

## Decisions (2026-09-23)

1. **Lab 12 moves to Thu 15 Apr, 15:00–16:50, in the recitation slot (SSB 108).** Lab 12 covers
   Lectures 1–2 of Week 12, both taught by Tue 13 Apr. Lecture 3 ("The Road Ahead") adds nothing that it
   assesses. This keeps
   finals week free of labs. The syllabus and the Week 12 Overview agree.
2. **The Wednesday 15:00 lab slot is kept** for Labs 0–11. It is free in the Spring timetable, and it
   falls after each week's three lectures.
3. **The weights are the gradebook's:** PS 30%, Midterms 30% (15 + 15), Final 20%, Labs 10%, Quizzes
   10%. The MASTER TIMETABLE and ASSESSMENT CALENDAR now say the same.
4. **Holidays follow UNIVERSITY POLICIES.** MLK Day is a no-classes day:
   - Lecture 1 moves to Tue 19 Jan and Lecture 2 to Wed 20 Jan, both at 11:00.
   - The diagnostic Quiz 00 moves to the Thu 21 Jan recitation at 15:00.
   - PS 0 is released Tue 19 Jan at 12:00.

   Presidents Day is not a university holiday, so Quiz 04 runs on Mon 15 Feb.
5. **Midterm 1 covers Weeks 0–4**, and Week 5 (parametric and polar) goes on Midterm 2, as the course
   planned.
