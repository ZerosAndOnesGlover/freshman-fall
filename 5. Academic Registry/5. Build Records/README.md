# Build Records

Process documents from the construction of the vault, kept for provenance and **not** part of any
course's student-facing content.

Nothing here is assessed, assigned, or linked from a course folder. These files record *why* a
course's material is arranged the way it is — which is worth keeping, but does not belong in a
directory a student browses.

---

## Year 1 Freshman Fall

| File | What it records |
| --- | --- |
| [[PROG 101 Realignment Plan]] | Built Week 1 covered two curriculum weeks; every later week inherited the compression. Records the redistribution back onto the curriculum's week numbering. |
| [[MATH 141 Realignment Plan]] | Same compression problem — curriculum Weeks 0–10 had been built into 8 folders, and Weeks 11–12 were never written. Records the redistribution and the two new weeks. |
| [[MATH 151 Realignment Plan]] | Alignment audit written *before* any file was changed, listing which curriculum weeks existed and which did not. |

**The authority in every case** is
`5. Academic Registry/1. Scheduling/Year1 - Freshman/CSE_Year1_Freshman_Curriculum.docx`.

---

## Year 2 Sophomore

| File | What it records |
| --- | --- |
| [[Registry Reconciliation]] | The state of the Year 2 scheduling files before any course content was written: two broken timetable grids, two real lecture clashes hiding inside them, two wrong course titles, midterms sitting in the wrong weeks, and a week-to-date mapping that contradicted itself. Records what was changed and what was deliberately left alone. |
| [[PROG 201 Scheduling Notes]] | What had to be settled before PROG 201 could be written: a Monday lab that forces a full-week lag, thirteen labs against twelve usable Monday slots once Fall Break is removed, a Week 0 Friday on which three courses already hold labs, and the reference machine every Week 0 measurement was taken on. Also records — without fixing — an overlap between CS 201's and CS 211's own Week 0 lab sessions. |
| [[MATH 241 Scheduling Notes]] | What had to be settled before MATH 241 could be written: a curriculum entry that states no assessment weights at all, a Week 0 whose Monday is Labor Day and whose three lectures therefore move, a Thursday recitation that must lag a full week, an unfilled TA slot, and the one quiz that cannot be sat on a Monday. Also records the `recitation/` section added to the site builder, and the vault-wide wikilink-resolution fix that followed: 424 of the site's 1,015 rendered links were broken because the builder matched filename stems only, and 166 stems are shared. |

| [[CS 202 Scheduling Notes]] | What had to be settled before CS 202 could be written: a Spring Week 0 whose registry dates contradict its own rule, a Friday-morning Lab 0 that leaves the afternoon for PROG 202, a course with no staff on record, a Project 2 the curriculum puts in Week 12 and the registry in the completion period, and which xv6 — the x86 version, with a two-flag GCC 13 build fix found by bisection, and a second `Makefile` fix found in Week 1 after QEMU 8.2's CPU topology had left xv6 silently on one CPU. Also the tool survey taken before any week was written, every measurement week by week, and the curriculum's lazy-FPU claim checked against this kernel's headers. |
| [[CS 212 Scheduling Notes]] | What had to be settled before CS 212 could be written: the first Year 2 course with no laboratory slot, so `project/` replaces `lab/` and appears in seven weeks rather than thirteen; a Week 0 with six slots for three lectures, whose spare Thursday became the team-formation workshop held *after* the project brief and *before* the add/drop deadline; a Tuesday quiz day where CS 202 has a Monday; a Week 6 holding a presentation, a midterm and a quiz in three consecutive days, none of them movable; and the reference codebase `roomsvc` — its fixed metrics, and the one 2024 double-booking incident carried deliberately across all thirteen weeks. |

**The authority** is
`5. Academic Registry/1. Scheduling/Year2 - Sophomore/CSE_Year2_Sophomore_Curriculum.docx`.

---

## Where Deviations Are Recorded

Realignment plans describe work that was *done*. Deviations that **remain** are documented in the
affected course's own syllabus, so that a reader encountering the course sees them without needing
this folder:

| Course | Deviation | Stated in |
| --- | --- | --- |
| CS 101 | Curriculum gives Problem Sets 40%; split here into Problem Sets 30% + Projects 10% | [[CS101 Week0/resources/Course Overview Syllabus\|Course Overview Syllabus]] |
| MATH 141 | Curriculum specifies no assessment weights; the division is departmental | same file, MATH 141 |
| MATH 151 | Curriculum specifies no assessment weights; the division is departmental | same file, MATH 151 |
| PHYS 141 | Curriculum lists torque and moment of inertia in Week 7; taught in Week 6, since rotational dynamics is unteachable without them. Week 7 takes angular momentum and static equilibrium. Union covers union. | same file, PHYS 141 |
| PHYS 141 | Curriculum specifies no assessment weights; the division is departmental | same file, PHYS 141 |
| CS 190 | Curriculum lists "Open Source Licenses" in Week 7; the licence taxonomy is taught in Week 2 with the open source ecosystem. Week 7 covers why licences bind. | [[CS190 Week0/Course Overview Syllabus\|Course Overview Syllabus]] |

---

## One Known Cosmetic Inconsistency

**MATH 151 lecture numbering.** Prose "Lecture N" corresponds to file `L(N−1)`, consistently across
all 13 weeks. It is a convention rather than an error, and it is uniform, but normalising it would be
a reasonable separate task.

---

*Academic Registry · Build Records · © CSE Department*
