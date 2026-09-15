# CS 202 · Operating Systems
## Week 4: Deadlock

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** **Midterm 1** (Monday, 18:00–19:15, VNC 100, Weeks 0–3, 12.5%), PS 3 due **Friday**, PS 4 released **Wednesday**, **Quiz 4** at the start of **Monday's** lecture (covers Week 3).
**Lab 3 is sat on the Tuesday of this week**, the afternoon after the midterm; **Lab 4 covers this week and is sat on the Tuesday of Week 5.**

> ### **Midterm 1 is Monday of this week**, 18:00–19:15, VNC 100 — **Weeks 0–3**, 12.5% of the course.
> 75 minutes, 100 marks, one handwritten sheet, one side. **Nothing in Week 4 is on the paper.**
> [[CS202 Week4/resources/MIDTERM 1 Revision Guide|MIDTERM 1 Revision Guide]] has the structure and
> what belongs on your sheet. **Quiz 4 is the same morning, and Lab 3 the next afternoon.**
>
> **Monday is also the third Monday in February.** The Year 2 calendar schedules classes and the
> paper as normal; if that changes, this README will say so.

---

### Why This Week Exists

Because Week 3 made every thread take locks, and a thread that holds one lock while waiting for another can wait forever.

**Two threads, two locks, opposite orders: deadlocked in every run**, usually within a few hundred rounds. Nothing crashes, nothing is reported, and both threads sleep — so a deadlocked server looks, to the kernel and to `top`, exactly like an idle one. **This week is about three questions**: what it takes for a deadlock to happen at all, how to make it impossible or avoid it, and — when neither is affordable — how to find one and what to do about it.

**The answers are unequally popular.** Kernels prevent deadlock by agreeing on a lock order and checking it only on debug builds. The Banker's algorithm avoids it perfectly and is almost never used, for reasons you will measure. Databases detect it and roll back. And for your own programs, Linux does nothing at all.

---

### Learning Objectives

By the end of Week 4, you should be able to:

1. **Reproduce a two-lock deadlock** and explain why holding the first lock longer makes it arrive sooner.
2. State **Coffman's four conditions** and show each in a concrete program.
3. Draw a **resource-allocation graph** and a **wait-for graph**, and say when a cycle is and is not a deadlock.
4. **Diagnose a deadlock from `/proc`** — state, `wchan`, and the `futex` arguments in `syscall` — without a debugger.
5. **Diagnose a deadlock with `gdb`**, and explain why it must start the program on these machines.
6. Prevent deadlock by breaking each condition, and **prove that a total lock order prevents it**.
7. Define **safe and unsafe states**, and explain why unsafe is not deadlocked.
8. **Run the Banker's algorithm by hand**, including a request that is available and refused.
9. Say **what the safety check costs** and **how conservative it is**, with measurements.
10. **Run the detection algorithm** for several instances of each resource, and say how it differs from the safety check.
11. **Measure livelock**, and explain why random back-off cures it.
12. Say what Linux, glibc and xv6 each do — and do not do — about deadlock.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L13 Deadlock What It Takes and What It Looks Like]] | **ABBA deadlocking in every run**; the four conditions; resource-allocation graphs; **the cycle read from `/proc`** and **named by `gdb`**; `ptrace_scope`; deadlock against livelock against starvation; **xv6's `panic: acquire`** |
| [[L14 Preventing Deadlock and the Bankers Algorithm]] | Breaking each condition; **`lockdep`, not in this kernel**; safe and unsafe; **the Banker reproducing the textbook**, P0's small request refused; **O(n²m): 21–75 ms at 3,200 processes**; **42% naive deadlocks against none** |
| [[L15 Detection Recovery Livelock and Ignoring the Problem]] | Detection with several instances — **nothing free and no deadlock; one more unit and four deadlocked**; recovery; **the hung-task detector watches only `D`**; **livelock at 32 failures per success**, cured by back-off; error-checking and robust mutexes |
| [[CS202 Week4/assignments/QUIZ 4 Week 4 Monday\|QUIZ 4 Week 4 Monday]] | Ten minutes, covers **Week 3**, answer key printed — **midterm-day revision** |
| [[CS202 Week4/assignments/MIDTERM 1\|MIDTERM 1]] | **Monday, 18:00–19:15, VNC 100.** Weeks 0–3 |
| [[CS202 Week4/resources/MIDTERM 1 Revision Guide\|MIDTERM 1 Revision Guide]] | Structure, the arithmetic to practise, what belongs on your sheet |
| [[PS 4 The Bankers Algorithm and Deadlock Detection]] | The Banker, detection, how conservative it is, what it costs, and back-off. Due **Friday of Week 5** |
| `assignments/ps4/` | `banker.c`, `detect.c`, `banksim.c` with `TODO`s, and six states |
| [[LAB 4 Finding a Deadlock]] | Hang a program; prove the cycle from `/proc` and from `gdb`; make it impossible and measure. **Tuesday of Week 5** |
| `lab/abba.c` | The two-lock deadlock, with a watchdog that reads `/proc` |
| [[CS202 Week4/resources/Reading Guide Week 4\|Reading Guide Week 4]] | OSTEP 32 and Silberschatz on the Banker — **after the midterm** |
| `resources/*.c` | `errchk.c`, `livelock.c`, and xv6's `uptime.c` |
| `solutions_instructor/` | Instructor only — including the midterm's mark scheme and the script that checks it |

---

### The One Thing to Take From This Week

**A deadlock is a cycle, and every tool that finds one is drawing the same graph.**

`/proc` gave it as addresses: two threads asleep in `futex`, each on the address of a mutex the other owned. `gdb` gave it as names and line numbers. The detection algorithm gives it as the set of processes left unfinished. **The fix is always to make the cycle impossible to draw** — and for locks, the cheapest way by far is a rule that every thread takes them in the same order, which turned a program that deadlocked within a few hundred rounds into one that ran 199 million rounds in thirty seconds.

**And none of this is automatic.** The kernel on your machine checks no lock order; the hung-task detector ignores sleeping threads; glibc's mutexes catch a thread relocking its own lock and nothing more. **Preventing deadlock is a discipline, not a feature.**

---

### Assessment Reminder

**Midterm 1: Monday, 18:00–19:15, VNC 100, Weeks 0–3, 12.5%.**

**PS 3 is due Friday at 17:00. PS 4 is released Wednesday.**

**Labs and quizzes carry no weight** and are still required. **Quiz 4 is at the start of Monday's lecture and covers Week 3.**

> **Two labs touch this week.** **Lab 3** — Week 3's futex lock — is sat on the **Tuesday of this
> week**, the afternoon after the midterm. **Lab 4** covers this week and is sat on the **Tuesday of
> Week 5**.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 3's locks** are every resource this week; **L12's philosophers** were deadlock prevented by ordering and by seats; **L11's three-state futex** is the `0x2` you read out of `/proc` in L13 §4. **Week 2's MLFQ boost** was a cure for starvation, the third failure in L15 §5's table.

**Sideways:** **MATH 251** reaches expectation and variance; L15's random back-off works because the expected number of collisions falls when the retry time is random.

**Forward:** **Week 5's page tables** are protected by locks with a strict order in every kernel. **Week 8's journaling** is recovery by rollback — L15 §2's database technique, used by a filesystem. **Week 11's distributed systems** cannot see a global wait-for graph at all, and have to detect deadlock by timeout.

---

*CS 202 · Week 4 · © CSE Department*
