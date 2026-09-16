# CS 202 · Operating Systems
## Week 12: Security, and What the Course Was

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** PS 11 due **Friday, 17:00**; **PS 12 released Wednesday** (due Friday of the completion period); **no quiz — Quiz 11 in Week 11 was the last.**
**Lab 11 is sat on the Tuesday of this week and is the Project 2 Part B checkpoint. Lab 12 is demo day, on the Tuesday of the completion period.**

> ### **This is the last week of teaching.**
> **Due Friday of the completion period, 17:00, both of them:** **Project 2** (15%) and **PS 12**.
> **The final is Wednesday of finals week, 09:00–11:30, VNC 100** — overflow to TH 200, check your
> seat on the portal. **Comprehensive, two handwritten pages permitted.**
> **Bring a kernel that does not boot to demo day.** That is what the session is for.

---

### Why This Week Exists

Because every mechanism in this course was designed against bad luck, and **an adversary is not bad luck.** It picks the worst case rather than the average, it has read your source, and it does not have to use the interfaces you designed.

**So the questions change.** Not "how fast is this?" but **"what happens when it is wrong, and how much does the attacker get?"** Not "does the protection exist?" but **"is it on the path of every access, and can anything skip it?"**

**And then the course ends, which means the last lecture has a different job**: to show that the thirteen weeks were **one mechanism applied to six resources** — an interposition point the hardware enforces, a table that says what maps to what, and a cache of that table because consulting it every time is too slow. **Every week of this course was that, plus the question of what it costs.**

**The costs are collected in one table in L39 §2**, and they are all your own measurements.

---

### Learning Objectives

By the end of Week 12, you should be able to:

1. **Write a threat model** — what is protected, from whom, and what is explicitly out of scope — and explain why the last line is the one that makes the model usable.
2. **List and count a trusted computing base**, and explain why **18 setuid binaries out of 2,049** is a more useful fact than "the kernel is trusted".
3. **State the reference monitor's three requirements**, say which one every general-purpose kernel fails, and say what seL4 pays to satisfy it.
4. **Distinguish `_FORTIFY_SOURCE`, the stack canary and NX** by the moment at which each acts, and explain why one leaked address defeats ASLR.
5. **Apply least privilege**, comparing setuid, capabilities, seccomp, rlimits and cgroups by what each can express — and say why `CAP_SYS_ADMIN` undermines the capability argument.
6. **Quote what a sandbox costs** — about **50 ns per system call, independent of the number of rules** — and defend a decision about whether to pay it.
7. **Explain why a sandbox policy must be derived by tracing** rather than written from first principles.
8. **Give the interposition point, table and cache for any mechanism in the course**, and name what invalidates the cache.
9. **Describe two of this term's broken measurement harnesses** and the check that would have caught each.

---

### This Week

| | Lecture | Sat |
|---|---|---|
| **L37** | **What We Are Protecting, and From Whom** — threat models; the TCB, counted; the reference monitor's three requirements; one bug caught three ways; ASLR measured over 200 runs; a timing channel, and how much of a secret it actually yields | Monday |
| **L38** | **Least Privilege, and What It Costs** — setuid against capabilities against seccomp; `NO_NEW_PRIVS`; the filter's price, measured with a control; the allowlist you cannot write from memory; the limit that counts the wrong thing; the mechanisms this machine refuses to give us | Wednesday |
| **L39** | **What This Course Was About** — one mechanism, six times; the term's whole price list; the Week 0 claim re-tested in Week 12; every measurement this course got wrong, and the check that caught it; what the final asks | Friday |

| | Work | When |
|---|---|---|
| **PS 11** | Raft leader election | **due Friday, 17:00** |
| **PS 12** | **A Cage You Can Trust** — build `jail`: rlimits, a seccomp allowlist, and an honest account of what it does not do | released **Wednesday**, due **Friday of the completion period** |
| **Lab 11** | Raft observed | sat **Tuesday of this week** — also the **Project 2 Part B checkpoint** |
| **Lab 12** | **Demo Day** — the Week 12 measurements, then Project 2 demos | **Tuesday of the completion period**, 15:00–16:50 |
| **Project 2** | xv6 memory and file system features | **due Friday of the completion period, 17:00** |
| **Final** | Comprehensive, Weeks 0–12 | **Wednesday of finals week, 09:00–11:30** |

**There is no Quiz 12.** Quizzes ran in Weeks 1–11 and **Quiz *N* covered Week *N*−1**, so no quiz covers Weeks 11 or 12. **Both are on the final.**

---

### What Is Measured This Week

**Everything in the lectures, on the reference machine.** The programs are in `lab/`:

| Claim | Program | Result |
|---|---|---|
| The TCB, counted | `find`, `getcap` | **18 setuid/setgid of 2,049 binaries; 4 with file capabilities** |
| One bug, three builds | `smash.c` | fortify catches it **before the copy**; the canary **at the return**; the third build **transfers control** |
| Randomisation | `aslr.c`, 200 runs | **200 distinct values for all five regions**; stack ~2²² pages, the rest ~2³²; **`setarch -R` makes them identical** |
| A sandbox's price | `seccost.c` | **≈ +50 ns per system call — and the same for 6 instructions, 205 instructions, or five stacked filters** |
| A filter that kills | `jailed.c` | **`SIGSYS`, exit 159** |
| A timing channel | `timing.c` | **2.5 ns per byte over a 1.25 ns noise floor** — and it recovers **one byte of eight** |
| The Week 0 claim, re-tested | `sgdt.c` | **still leaks a live kernel address**, while `kptr_restrict` zeroes `/proc/kallsyms` |

---

### Folder

```
CS202 Week12/
├── README.md
├── summary.md
├── lectures/     L37, L38, L39
├── assignments/  PS 12, the FINAL EXAMINATION, and ps12/ (jail.c, victims.c)
├── lab/          LAB 12 Demo Day, and six programs
├── resources/    Reading Guide Week 12, Final Revision Guide
└── solutions_instructor/   INSTRUCTOR ONLY
```

---

### Where This Sits

**Week 11** gave you agreement across machines. **This week asks who is allowed to ask** — and then closes the course.

**Nothing follows Week 12.** The next thing is the final, and after that the reading in L39 §6.

---

*CS 202 · Week 12 · © CSE Department*
