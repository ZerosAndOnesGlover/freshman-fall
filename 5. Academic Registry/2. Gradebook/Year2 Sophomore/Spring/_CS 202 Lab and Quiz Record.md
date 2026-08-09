# CS 202 · Lab and Quiz Record
## Not part of the course grade

> **This file is deliberately outside the gradebook's weighted components.** CS 202's
> labs and quizzes carry **no weight** — Problem Sets 30, Projects 30, Midterms 25 and Final 15 already sum to 100% without them,
> and `CS 202.md` says so.
>
> The leading underscore in the filename keeps this file out of `tools/gpa.py`'s course scan. Do not
> rename it without checking `collect()` in that script.

---

## Why This Is a Separate File

The gradebook parser reads a component's items from its heading until the **next `##` heading
containing a percentage**. An unweighted subheading has none, so its rows are silently absorbed into
the component above it. The failure was found in CS 102 in Year 1, where eleven quiz rows quietly
attached themselves to Project 2. Year 2 avoids it the same way Year 1 settled on: the unweighted
work lives here, and the gradebook has no table for it at all.

**The `Out of` column reads `—`, not a number.** That is load-bearing. `tools/make_answer_sheets.py`
reads it, and a non-numeric entry is what makes a sheet say `Marks: ___ / —` rather than inventing a
total the paper never claimed. Writing `0` would mean the same thing to a reader and the wrong thing
to the tool.

Use the **Done** column as a tick. The point of the record is that you can see, in one place, which
weeks you actually did the work.

---


## Labs

**Thirteen labs, Weeks 0–12, in the scheduled session.** Mandatory. The TA checks the work off during or just after the session; nothing is marked out of anything.

> **Attendance is the enforcement.** `COURSE POLICIES.md` reduces the final course grade > by one letter after a second unexcused lab absence. That rule, not a mark, is why the > lab is not optional.

| Lab | Week | Topic | Out of | Done |
|---|---|---|---|---|
| Lab 0 | Week 0 | Trace a system call with strace; a minimal kernel that prints Hello | — | |
| Lab 1 | Week 1 | Read /proc/pid/maps and /proc/pid/status for running processes | — | |
| Lab 2 | Week 2 | Use chrt and nice to set process priorities | — | |
| Lab 3 | Week 3 | Use futex() for an efficient user-space lock | — | |
| Lab 4 | Week 4 | Reproduce a deadlock with threads; detect it with gdb | — | |
| Lab 5 | Week 5 | Examine /proc/pid/pagemap | — | |
| Lab 6 | Week 6 | Observe the OOM killer; experiment with overcommit settings | — | |
| Lab 7 | Week 7 | Instrument the page cache with bpftrace | — | |
| Lab 8 | Week 8 | Use ZFS snapshots and measure the performance cost | — | |
| Lab 9 | Week 9 | Load a kernel module and write to it from user space | — | |
| Lab 10 | Week 10 | Boot a VM in your own hypervisor | — | |
| Lab 11 | Week 11 | Use etcd to observe Raft in action | — | |
| Lab 12 | Week 12 | Demo day | — | |

---

## Quizzes

**Ten minutes at the start of the course's first lecture of the week, Weeks 1–11.** Closed book. Not marked — the answer key is printed in the paper, below the questions.

**Quiz *N* is sat in Week *N* and covers Week *N−1*.** Year 2 numbers its quizzes after the week they are sat in. *(Year 1 was not consistent about this: CS 102 and MATH 142 used the same rule, but ECE 110 numbered its quizzes after the material instead. Check the course before assuming.)*

| Quiz | Sat in | Covers | Topic | Out of | Done |
|---|---|---|---|---|---|
| Quiz 1 | Week 1 | Week 0 | Kernel and user space; the trap mechanism | — | |
| Quiz 2 | Week 2 | Week 1 | Implement a user-space process manager | — | |
| Quiz 3 | Week 3 | Week 2 | Simulate MLFQ and CFS | — | |
| Quiz 4 | Week 4 | Week 3 | A user-space mutex using compare-and-swap; dining philosophers | — | |
| Quiz 5 | Week 5 | Week 4 | Implement the Banker's algorithm | — | |
| Quiz 6 | Week 6 | Week 5 | Implement a 2-level page table in C | — | |
| Quiz 7 | Week 7 | Week 6 | Simulate LRU and Clock page replacement | — | |
| Quiz 8 | Week 8 | Week 7 | Implement a complete file system (myfs) on a disk image | — | |
| Quiz 9 | Week 9 | Week 8 | Add journaling to myfs | — | |
| Quiz 10 | Week 10 | Week 9 | Write a simple Linux kernel module (character device) | — | |
| Quiz 11 | Week 11 | Week 10 | A minimal hypervisor using KVM ioctls | — | |

*There is no quiz covering Week 11 or Week 12 — those are examined only on the final.*

---

## Why Unmarked Work Is Worth Doing

The feedback loop that matters here is the one that closes in the next five minutes, not the one that closes when a grade comes back three weeks later. A quiz you mark yourself against the key in the same sitting tells you what has not landed while there is still a term left to fix it. Marking it would add a number and subtract nothing from the misunderstanding.

---

*CS 202 · Lab and Quiz Record · Year 2 Spring*
