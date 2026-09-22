# PROG 102 — Programming II: Object-Oriented Design and Data Structures in C++ — Course Audit

**Question:** Do the labs, problem sets, projects and quizzes of each week need C++ features, tools or
algorithms that the lectures have not yet taught? Are any of them larger than they need to be?

**Method:** Same as the Fall audits and the CS 102 audit. Each week's lectures were read against its
deliverables. Lecture 00 §18 ("Not Yet") gives the course's own schedule for introducing features, and
that schedule was the yardstick:

| Feature | Week |
| --- | --- |
| Operators | 1 |
| Templates | 2 |
| STL | 3 |
| `virtual` | 4 |
| Smart pointers and moves | 5 |
| Exceptions | 9 |
| Threads | 10 |
| Lambdas and `std::function` | 11 |

PROG 101 (Fall, C) counts as taught. So does CS 102 where it teaches an algorithm (BST deletion,
successors). Where changed code or claims could be checked, they were compiled with g++ 13.3 and run
under ASan/UBSan.

**Timing conventions (re-based to 18 Jan 2027):**
- Lectures run Tue, Wed and Thu 10:00. Week 0 alone adds a Friday 10:00 slot for L03.
- **Quiz *N*:** Tuesday of Week *N*, 10:00–10:15, covering Week *N−1*. The quiz files already said
  Tuesday; the registry's "Monday" note was stale.
- **Lab *N*:** Monday of Week *N+1*, 15:00–16:50.
- **PS *N*:** released Friday of Week *N* at 10:00 (PS 0 at 11:00, after L03), due the following
  Friday at 17:00.
- **Projects:**
  - Project 1: Tue 2 Mar → Fri 26 Mar.
  - Project 2: Tue 6 Apr → Fri 16 Apr.
- **Exams:**
  - Midterm 1: Tue 2 Mar, 18:00–19:30.
  - Midterm 2: Tue 30 Mar, 18:00–19:30.
  - Final: Thu 22 Apr, 14:00–16:30.

---

## Summary

The lectures themselves break Lecture 00's own schedule in three places, and the deliverables lean on
all three:

| Feature | Taught in | Used from |
| --- | --- | --- |
| **`throw` / `try` / `catch`** | Week 9 | L03, L04 and L06 (Weeks 0–1). PS 1 asks students to throw from `operator[]` and to catch a forced `bad_alloc`. L06's forced-failure harness is shown only as output, never as code. |
| **Empty-bracket lambdas** | Week 11 | Lectures 10 and 12 (Week 3), in comparators and algorithm calls |
| **Capture lambdas and `std::function`** | Week 11 | Week 8's lectures (the "what C++11 obsoleted" argument) and Week 10's `cv.wait` predicates |

**Fix:** three short "just enough" boxes, the same device as Fall's PHYS 141 "Fitting a Straight Line"
box. Lecture 00's table was updated to match. What each construct *is* and what it costs still arrives
in its original week.
- **L04 §4.2** teaches `throw` and a basic `try`/`catch`.
- **L06 §1** prints the forced-failure harness. It was verified to reproduce both of the lecture's
  transcripts exactly, including the ASan use-after-free.
- **L12 §2.2** teaches the empty-bracket lambda as a short form of Lecture 04's function object.
- **L25 §4** teaches capture and `std::function` at use level.

**Beyond that, the problems were:**
- **Duplication.** Seven problem sets re-ran a lab or a lecture's measurement.
- **Items needing an untaught feature or algorithm.** Listed below.
- **One factual error, shared by a lecture and PS 0.** Swapping the member declarations of `Wrong`
  does **not** leave `-Wreorder` firing: both warnings vanish.
- **A missing starter file.** Lab 0's `stack.c` was "given" but did not exist.

---

## Per-week findings and fixes

| Week | Finding | Fix |
| --- | --- | --- |
| 0 | PS 0 C2 overloads `operator new[]` (Week 1). C2(b) claims `-Wreorder` survives swapping the declarations; g++ 13.3 shows both warnings vanish. L02 §4.2 said "change nothing else" but its `NotABug` also reverses the list. Lab 0's `stack.c` does not exist. PS 0 A4 is a puzzle beyond the week. | C2 uses a printing helper. C2(b) now builds `NotABug` (verified: `-Wreorder` ×3, no `-Wuninitialized`, 4 ints). L02 wording fixed. `lab/stack.c` written and verified: `size=5 cap=8`, `25 16 9 4 1`, 32-byte leak without `stack_free`. A4 cut. |
| 1 | PS 1 throws (A1/A2) and catches (C2) before Week 9. C2's `operator new[]` replacement is never shown. D1 and D3 re-run L06's tables. | L04 §4.2 and L06 §1 boxes; C2 uses the printed harness; D1/D3 cut. |
| 2 | PS 2 A2 repeats Lab 2 A (assembly). PS 2 E and Lab 2 D are the same exercise, and both use `std::sort` on `std::vector` (Week 3). Lab 2 runs Mon 8 Feb, the day **before** L10. | Lab 2 D cut. PS 2 E's third error is now `std::pair<P,int> < …` (Week 2, L08 §6); measured at 6, 5 and 24 lines. |
| 3 | PS 3 A needs `nth_element`, the set algorithms, `rotate`, `stable_partition` and `partial_sort`, none of them taught. Its "no raw loops" rule pushed students toward them. PS 3 B and C3 repeat Lab 3. Lab 3 C1 needs `std::shuffle`. | Five problems kept (12 points each); rule relaxed to "prefer L12's algorithms"; B and C3 cut; Lab 3 uses reverse order. |
| 4 | PS 4 A3 and D1 use `unique_ptr` (Week 5). B2/B3 are Lab 4 B. D1 is L14 §5's own three-attempt benchmark. | Shapes held as `Shape*` and deleted by hand (the key already said Week 5 would open on this). B2, B3 and D1 cut. |
| 5 | PS 5 B2, B4 and D3 re-measure L16–L18. Its note said "Midterm 1 was this week". | Cut; note fixed. |
| 6 | PS 6 C3 needs `std::shuffle` and repeats L21 §3.2. Lab 6 C and Project 1 1.1 need `splice`, and Project 1 1.3 needs a node-relinking merge sort. None of these is taught. | Cut. Project 1 gains `remove_if`/`reverse` (relinking only); its BST parts cite CS 102 L04–L05. |
| 7 | PS 7 A4 explicitly allows `std::function` "because it is Week 11". C2 races 16 threads (Week 10). B3 is timing. | A4 uses a function-pointer registry; L23 §3.2 now shows one. C2 and B3 cut. |
| 8 | The whole week uses capture and `std::function`. PS 8 B2–B3 re-time L26 §3. | L25 §4 box; B2–B3 cut. |
| 9 | PS 9 B (the `Fragile` sweep) is Lab 9 C–D. PS 9 A1–A2 re-time L28 §5. C2 asks for "peak memory", which is never taught. Lab 9 said "Project 1 is due today" (it was due the previous Friday). | PS 9 builds on Lab 9's table; A reasons from L28's data; C2 counts copies; lab note fixed. |
| 10 | PS 10 A re-runs L31 §3 (which Lab 10 also runs). PS 10 C re-runs L32 §2 and L33 §2. | Cut. |
| 11 | PS 11 B is Lab 11 A–C. | Cut. |
| 12 | Project 2 required a list `sort()`, never taught. Its Part 5 repeats Project 1's benchmarks. | Cut. |

Every problem set stays at 100 points and every lab at 40. Each problem set opens with a "What this
uses / Not needed" box. Every key follows its set's cuts and carries a dated revision note.

**Dates.** Every lab, quiz, set and project now carries its date and time. Midterm 1 was "Week 5"
throughout, but the registry pins it to **Tue 2 Mar (Week 6)**; it still covers Weeks 0–4, as the
gradebook says. Every mention now agrees, including the revision guides, lectures, READMEs, summaries,
syllabus, quizzes, labs and answer-sheet filing. The final was "Week 12" and is now **Thu 22 Apr**.

---

## Open decisions (left to you)

1. **Lab 12 (the Project 2 demo) is Mon 19 Apr, in finals week**, three days before the final. That is
   arguably the right place for a demo, but it breaks "instruction ends Fri 16 Apr".
2. **Exam lengths.**
   - The final is written for 180 minutes; the registry books 150 (14:00–16:30).
   - The midterm papers are 75 minutes in a 90-minute registry slot (18:00–19:30). They were left as
     75-minute papers.
3. **Week 0's Friday lecture** (L03, Fri 22 Jan 10:00) is outside PROG 102's Tue–Thu pattern. The
   timetable has the slot free.
4. **Holidays:**
   - Presidents Day (Mon 15 Feb) is Lab 3.
   - MLK Day (Mon 18 Jan) has no PROG 102 class.
5. **Quiz file names still say "Monday"** (e.g. `QUIZ 3 Week 3 Monday.md`). Their contents and dates say
   Tuesday. They were not renamed, to keep existing links intact.
