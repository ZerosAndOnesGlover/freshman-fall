# CS 102 — Computer Science II: Algorithms and Data Structures — Course Audit

**Question:** Do the labs, problem sets, projects and quizzes of each week require knowledge the
lectures have not yet taught by the time the work is done? Are any of them larger than they need to be?

**Method:** Same method as the Freshman Fall audits. For every week, the three lectures were read in
full, and then each deliverable was checked against the lectures of its own week and earlier ones. That
covers the lab, the problem set, the quiz, the projects, both midterm revision guides and the final
revision guide. CS 101 (Fall) counts as taught; anything from it was checked against the CS 101
lecture files. Reading guides do not count as teaching. A deliverable that repeats another deliverable
was treated as excess, not as a gap.

**Timing conventions (re-based 2026-09-22 to a term opening Mon 18 Jan 2027):**
- Lectures run Mon, Wed and Fri 09:00–09:50. Week *N*'s lectures are L(3N+1)–L(3N+3).
- **Quiz *N*** is Monday of Week *N* at 09:00–09:15 and covers Week *N−1*.
- **Lab *N*** is Tuesday of Week *N+1* at 15:00–16:50, after all three of its lectures.
- **PS *N*** is released Friday of Week *N* at 10:00, after the last lecture. It is due the following
  Friday at 17:00.
- **Projects:**
  - Project 1 is assigned Mon 8 Mar and due Fri 26 Mar 17:00.
  - Project 2 is assigned Mon 29 Mar and due Fri 16 Apr 17:00.
- **Exams:**
  - Midterm 1: Mon 1 Mar, 18:00–19:15.
  - Midterm 2: Mon 29 Mar, 18:00–19:15.
  - Final: Wed 21 Apr, 09:00–11:30.

---

## Summary

CS 102's lectures are unusually well aligned with their deliverables: most lectures end by describing
the lab and problem set that follow, and most numbers in the sets were produced from the lecture code.
**The dominant problem is volume, not untaught material.** Problem sets routinely re-ran the lab's
measurement, or a measurement the lecture had already printed. On top of that, eight items needed
material from a later week or from nowhere.

| Kind | Items |
| --- | --- |
| **Needs a later week** | PS 4 B3 (Floyd–Warshall, Week 8) · PS 7 E2 (LIS, Week 8) |
| **Never taught** | PS 9 E6 (Moore–Hodgson) · PS 11 A4 (ray-casting point-in-polygon) · Lab 10 Part C (winnowing) and A1 (`hashlib`) · Lab 11 Part D ($k$-nearest search) · Project 1 Part 3 (Hirschberg — named in L23, not taught), `argparse`, `tracemalloc` · Project 2 TF–IDF, phrase queries, delta/variable-byte postings compression · Lab 3 C3 `tracemalloc` (tool, now supplied in the lab) · PS 6 E1 "modified Dijkstra" for bottleneck paths |
| **Repeats a lab** | PS 2 C = Lab 2 B · PS 5 B5 = Lab 5 B · PS 6 D = Lab 6 B · PS 6 E3 = Lab 6 C · PS 8 E3–E4 = Lab 8 A–B · PS 9 D2 = Lab 9 A3 · PS 11 E3 = Lab 11 C |
| **Repeats a lecture's measurement** | PS 3 D (L11 §4) · PS 4 A2–A3 (L13 §4), D1–D2 (L15 §4), E (L13 §7) · PS 7 A3 (L22 §5) |
| **Cannot reproduce its own reference** | Lab 4's generator: no reading of "choose uniformly" gives max degree 192 |
| **Dates** | Midterm 1 is Week 5 in the syllabus and lectures but Week 6 in the registry. The final is "Week 12" in the handouts but finals week in the registry. No problem set, lab or quiz carried a date. |

---

## Per-week findings

**Week 0.** Lab 0 uses only CS 101 material: sorts, `random`, `time.perf_counter`. Aligned.

**Week 1.**
- **PS 1:** aligned, but long. A4 restated definitions, D4 restated a lecture paragraph, and E3 was the
  same idea as C4.
- **PS 1 C5** asked for a successor without parent pointers. L05 only gives the version with parent
  pointers, so the method is now stated in the question.
- **Lab 1:** aligned.

**Week 2.**
- **PS 2 Part C** (heights and rotations, sorted and random) was Lab 2 Part B almost word for word.
- **Lab 2 A3** told students to use `check_avl` "from PS 2 B3". PS 2 is released on Fri 5 Feb and not
  due until 12 Feb, so the lab relied on work that had not been submitted.

**Week 3.**
- **PS 3 Part D** re-measured build swap counts. L11 §4 prints those same tables.
- **Lab 3 C3** needs `tracemalloc`, which is never taught. It appears in L11 only in a "Verified" note.

**Week 4.**
- **PS 4 B3** said "implement Floyd–Warshall for unweighted graphs" as a BFS oracle. Floyd–Warshall is
  **Week 8** (L27). This is the clearest out-of-order item in the course.
- **Measurements the lecture already made:**
  - A2–A3 measure memory. L13 §4 prints the numbers.
  - D1–D2 count undirected edge classifications. L15 §4 prints the numbers.
  - Part E times BFS up to $10^6$ vertices. L13 §7 prints the numbers.
- **PS 4 C4** asked for "an independently written cycle detector" for digraphs. The only other one in
  the course is Kahn's algorithm, which is Week 5.
- **Lab 4:** the generator spec is ambiguous. Twelve plausible readings were tried, and none reproduces
  the reference table (192, 164, 142 … top degrees).
- **Lab 4, `random`:** CS 101 taught only `random.randint`. The lab did not say which call to use.
- **Midterm 1:** the syllabus, READMEs, lectures, revision guide and PS 4 all said Week 5, "during the
  lecture slot". The registry pins it to **Week 6, Mon 1 Mar 18:00–19:15**.

**Week 5.**
- **PS 5 B5** (early exit) is Lab 5 Part B.
- **PS 5 B4, C3 and D4** are extra measurement: heap counts, a random failure rate, and timing.
- **PS 5's note** said "MIDTERM 1 was this week".
- **Lab 5:** A\* is taught in L17 §5. Aligned.

**Week 6.**
- **PS 6 Part D** (timing Kruskal against Prim) is Lab 6 Part B.
- **PS 6 E3** (MST clustering) is Lab 6 Part C.
- **PS 6 E1** checked the minimax property against "a modified Dijkstra", which is never described.

**Week 7.**
- **PS 7 E2** asks for the LIS state. LIS is **Week 8** (L26); the question itself says "the
  $n\log n$ one (Week 8)".
- **PS 7 E3** (maximum subarray) has no worked example anywhere. L26 later cites it as where the
  "ending at $i$" state was learned, so it was kept with a hint that names that state.
- **PS 7 A3** timed the Fibonacci versions again; L22 §5 already has the measurement.
- **Project 1:**
  - Part 3 is Hirschberg's algorithm. L23 §5 only names it, as the "stretch component".
  - The allowed-library line leaned on `argparse` and `tracemalloc`, neither of which is taught.
  - Unified `@@` hunks were never specified.

**Week 8.**
- **PS 8 E3–E4** (Floyd–Warshall, and all six loop orders) were Lab 8 Parts A–B verbatim.
- **PS 8 C3** timing was removed.
- **PS 8 D4** asked students to relate their answer to "what Week 9 will require". It now points at
  L26 §3.

**Week 9.**
- **PS 9 E6** (fewest late jobs) is optimal only with Moore–Hodgson. The key's own note says the
  obvious rule fails half the time, and Moore–Hodgson is never taught.
- **PS 9 D2** (bit-packing and a round trip) is Lab 9 A3.
- **Lab 9:** `random.choices` and `zlib` are named in the handout with exact calls. DEFLATE is taught
  in L30 §5. Aligned.

**Week 10.**
- **Lab 10:**
  - Part C (winnowing) is never taught.
  - A1 required `hashlib.blake2b`, also never taught. L32 says Lab 10 is built on Rabin–Karp, so A1
    now uses that.
  - The lab said "MIDTERM 2 is this week", but it runs on Tue 6 Apr, a week after the midterm.
- **PS 10 D1, D2 and D4** were three more timing sweeps.
- **Project 2:** TF–IDF, phrase queries (positional postings) and delta/variable-byte compression
  are taught nowhere. The inverted index itself is defined in L33 and in the brief, so it stays.

**Week 11.**
- **PS 11 A4** (ray-casting point-in-polygon) is not taught. L34 lists only "point in *convex*
  polygon".
- **PS 11 E3** (the k-d tree dimension sweep) is Lab 11 Part C.
- **PS 11 C2 and E2** were timing.
- **Lab 11 Part D** ($k$-nearest with a bounded heap) is not taught.

**Week 12.** Lab 12 is aligned: Held–Karp is from L26, and the MST tour and 2-opt are from L39. Only its
date is a problem (see Open decisions).

---

## Verification and Fixes (2026-09-22)

Commits: the Spring re-base, then CS 102 Weeks 0–6, then Weeks 7–12.

| Claim | Verdict and fix |
| --- | --- |
| PS 4 B3 needs Week 8 | **Upheld**; removed |
| PS 7 E2 needs Week 8 | **Upheld**; removed. E3 kept with a hint (L26 relies on it) |
| PS 9 E6, PS 11 A4, Lab 10 C, Lab 11 D untaught | **Upheld**; all removed |
| Lab 10 needs `hashlib` | **Upheld**; now Rabin–Karp from L32. Jaccard values are unchanged barring a 61-bit collision |
| Lab 3 needs `tracemalloc` | **Upheld**; kept, with the four lines it needs supplied in the lab |
| Project 1 Part 3, `argparse`, `tracemalloc`, `@@` hunks | **Upheld**; removed. The two `sys` lines needed are given. 2,500 → 2,000-word report |
| Project 2 TF–IDF, phrases, compression | **Upheld**; removed. Ranking is by term count with a bounded heap (L12 §4). Now four parts: index, rank, suffix/fuzzy, report |
| PS–lab duplicates (seven listed above) | **Upheld**; the PS copy removed in each case |
| Lecture-measurement repeats (PS 3 D, PS 4 A2–A3/D1–D2/E, PS 7 A3) | **Upheld**; removed |
| Lab 4 reference not reproducible | **Upheld.** The spec now pins `random.randint`, draw order, edge order and tie-breaks. Every number was regenerated by running it: $E$ = 14,994; top degree 192, 181, 166 …; levels 1/181/1,682/2,858/278; diameter 7, radius 4; 36 vertices at eccentricity 7; the double sweep from 0 gives 6; `dfs_iter` depth 3,274. The lab's lesson survives |
| PS 6 E1 "modified Dijkstra" | **Upheld**; the reference is now the threshold test (smallest $w$ that connects $u$ and $v$ via BFS over edges $\le w$) |
| Midterm 1 in Week 5 | **Resolved to the registry:** Mon 1 Mar (Week 6), scope still Weeks 0–4, as in the gradebook. The make_answer_sheets filing rule was patched to match |
| Final "in Week 12" | **Resolved to the registry:** Wed 21 Apr, finals week |

Every problem set stays at 100 points; labs stay at 40. Each problem set now opens with a
"What this problem set uses / Not needed" box. Every key follows its set's cuts and carries a dated
revision note. Greedy coin-change failures (84, 49, 0), MCM 15,125 and left-to-right 40,500 were
re-run and match.

**Also fixed:**
- PS 2 had its own late policy (10%/day), which contradicted the syllabus (20%/day). It now defers to
  the syllabus.
- PS deadlines at 23:59 or "start of lecture" are now Fri 17:00, per the Spring timetable.
- The PS 8 note told students to let Part E slip. Part E is now small, and the note says so.

---

## Open decisions (left to you)

1. **Lab 12 falls in finals week.** Under the Tuesday-after rule it meets Tue 20 Apr, the day before
   the CS 102 final. The alternatives are to run it Tue 13 Apr before L39, which would break
   taught-before-assessed, or to drop it: the 10-of-13 gate still works with 12 labs.
2. **Final exam length.** The paper and revision guide are written for 180 minutes, but the registry
   books 150 (09:00–11:30).
3. **Midterm 1 scope.** It now sits in Week 6 but still covers Weeks 0–4, which matches the gradebook.
   The registry's old note said "Weeks 0–5".
4. **Holidays:** MLK Day (Mon 18 Jan) is the first CS 102 lecture, and Presidents Day (Mon 15 Feb) is
   Quiz 4 and L13.
5. **Project 1 is due the same day as PS 8** (Fri 26 Mar). The set was cut to about four hours for
   that reason, but the collision is still there.
