# ECE 110 — Digital Logic & Circuit Design — Course Audit

**Question:** Do the labs, problem sets and quizzes of each week need material or tools that the
lectures have not yet taught? Are any of them larger than they need to be?

**Method:** Same as the other Spring audits.
- Each week's two lectures were read against its problem set, lab and quiz.
- Every deliverable was scanned for every later-week topic, and each hit was read in context. Quiz *N*
  sits in Week *N+1* and was checked against Week *N*.
- CS 101's Python counts as taught.
- Every replacement exercise was implemented and run before its key was rewritten.

**Timing conventions (re-based to 18 Jan 2027):**
- Lectures run Wed and Thu, 13:00–14:15.
- **Lab *N*:** Friday of Week *N*, 14:00–15:50, after both lectures. This was already the course's rule.
- **PS *N*:** released Thursday of Week *N* at 14:30, after Lecture 2; due the following Thursday at
  13:00.
- **Quiz *N*:** ungraded, Wednesday of Week *N+1* at 13:00, covering Week *N*.
- **Midterm:** Thu 4 Mar, 18:00–19:15, covering Weeks 0–5.
- **Final:** Mon 19 Apr, 08:00–10:00.

---

## Summary

The lectures, problem sets and quizzes are aligned. The scan's hits were false positives:
- "ROM" matching inside "from";
- "counter" meaning a counterexample;
- the FPGA and lookup-table questions in PS 5 and PS 9, which are taught as previews in Lecture 5.2
  §3 and Lecture 9.1 §6.

**One large finding:** **Labs 1–9 required students to write Verilog** — modules, primitive
instances, testbenches, `$signed`, reset handling. Verilog is taught in **Week 10** (Lecture 10.1:
"Describing Hardware, Not Programming It"). Each of those labs had a Verilog part worth 20–35
points, and Lab 6 was built on it. The keys' own notes record the pain this caused: a 1-bit `reg`
loop counter that never terminates, an asynchronous reset that never fires, and width traps. These
are Week 10 lessons, met in Weeks 1–9 without the lecture.

**Fix:** every Verilog part is now a **Python gate-level simulation** of the same circuit. Python is
taught (CS 101) and the labs already used it. The expected results were re-run and are unchanged
except where noted.

| Lab | Was | Now | Verified result |
| --- | --- | --- | --- |
| 1 | Part B: Verilog identity checker | A second, independent checker on truth tables packed into 8-bit integers | 16 identities, 0 failures. The key's "15" was a miscount of its own table; corrected. |
| 2 | Part D: structural `nand` modules and a testbench | NAND-only rebuilds as Python gate functions | 0 failures over 4 inputs × 4 rebuilds |
| 3 | Part C: structural Verilog adder, 512-case testbench | Structural Python adder from gate functions | 512 cases, 0 failures. The width trap is now 256 false failures (unmasked comparison), measured. |
| 4 | D1: Verilog equivalence | Python equivalence over 16 inputs | 0 failures. SymPy's `SOPform`/`POSform` are explained in the Tools line. |
| 5 | Part D: Verilog implementations and `lut3` module | Python functions and `lut3(table_bits, a, b, c)` | 0 disagreements; `0b11101010` computes Σm(1,3,5,6,7), `0b11101001` computes Σm(0,3,5,6,7) |
| 6 | Parts A–B: Verilog ALU and testbench, `$signed` | Python ALU on bit lists, with subtraction reusing the Lab 3 adder | 2048 cases, 0 failures; V checked on 256 pairs, 0 failures (64 overflow) |
| 7 | Part D: structural Verilog master–slave flip-flop | Two gated latches simulated per half-period | 12 edges, 0 failures |
| 8 | D3: Verilog counters | Ripple and synchronous counters simulated per clock; mod-10 with clear = Q3·Q1 | 0 failures; 0…9 repeating |
| 9 | Part C: Verilog Mealy/Moore and a random testbench | State tables in Python, driven by `random.randint` | 2000 cycles, 130 detections, 0 failures each. The reset trap becomes the Moore one-cycle-late trap. |

Lab 1's text told students that `!==` "will matter a great deal in Week 10 — meet it now". That note is
gone, because nothing before Week 10 now uses Verilog. The lectures' "(verified in Verilog)"
provenance notes stay: they describe how the lecture's numbers were produced and are not assessed.

**Dates.**
- Every lab, set and quiz is dated.
- The midterm (Thu 4 Mar, Week 6) already agreed with the registry. Lab 6 (Fri 5 Mar) now says the
  midterm was *yesterday*, not "this week".
- Lecture 6.2 and Lab 12 were corrected the same way: the final is **Mon 19 Apr**, not "this week".

---

## Decisions (2026-09-23)

1. **PS 12 is an ungraded self-check.** Its answers are released Fri 16 Apr, 17:00, before the final
   on Mon 19 Apr. Graded work is PS 0–11. Since the lowest set is dropped anyway, nothing is lost, and
   no work falls due after the final. The gradebook row and the answer sheet were removed.
2. **Holidays** do not touch ECE 110, whose classes meet Wed–Fri.
3. **The Python route for Labs 1–9 is kept.** It needs no new teaching, and Verilog still arrives
   whole in Week 10, where Lectures 10.1–10.2 teach it properly.
