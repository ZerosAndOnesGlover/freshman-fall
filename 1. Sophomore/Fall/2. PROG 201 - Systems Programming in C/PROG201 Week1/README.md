# PROG 201 · Systems Programming in C
## Week 1: File Descriptors and Unix I/O

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** PS 1 (due Friday of Week 2) and **Quiz 1** (Tuesday, covers Week 0).
**No lab session this week** — Lab 0 was sat on the Friday of Week 0, and **Lab 1 is sat on the Monday of Week 2**.

---

### Why This Week Exists

Because `int fd = open(...)` returns **3**, and the reason it is a small integer explains most of Unix.

Week 0 was about processes — how one is made, how one ends, how one is interrupted. **This week is about the other half of what a process is: the table of things it has open.** Everything the rest of the term does — pipes, sockets, `mmap`, the shell, the container — is that table being rearranged.

Three ideas, and the second is the one that takes a week to become automatic:

1. **A descriptor is an index**, and the kernel always gives you the lowest free one.
2. **There are three tables, and the file offset lives in the middle one.** Two descriptors share an offset or do not, depending entirely on how they came to exist — which is why `>` works across a `fork` and why two independent `open`s of a log file destroy each other's data.
3. **A system call costs about a microsecond**, and the difference between reading a file one byte at a time and one page at a time is a factor of a thousand.

By Monday of Week 2 you will have written `ls | grep | wc` in C, with no shell involved.

---

### Learning Objectives

By the end of Week 1, you should be able to:

1. Say what a file descriptor indexes, and state the lowest-free-descriptor rule.
2. Draw the three tables and place the offset, the status flags and the inode correctly.
3. Predict, for any pair of descriptors, whether they share an offset — and be right.
4. Use `open`'s flags deliberately, including `O_CLOEXEC`, `O_APPEND` and `O_CREAT|O_EXCL`, and explain `umask`.
5. Write `write_all`, and say why every unchecked `write` is a latent bug.
6. **Quantify the cost of a system call**, and choose a buffer size for a reason.
7. Explain sparse files, and why a naive copy destroys them.
8. **Explain why `lseek`+`write` from two processes loses data and `O_APPEND` does not.**
9. Perform redirection with `dup2`, and derive the `2>&1` ordering rule rather than memorising it.
10. State the pipe EOF rule, and debug a hung pipeline with `ps -o wchan`.
11. Handle `EAGAIN` and `SIGPIPE`/`EPIPE` correctly.
12. Say why `writev` is faster than three `write`s, and when it is not worth it.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L04 File Descriptors and the Three Tables]] | The small integer; the three tables; `dup` against a second `open`, **measured**; inheritance across `fork`; `open` flags and `umask`; why `close` can fail |
| [[L05 read write and What a System Call Costs]] | Short transfers and `write_all`; **1 B to 1 MB, a 1000× span, flattening at one page**; pipe capacity; sparse files at 1.1 GB in 4 KB; **`O_APPEND` against a 95% data loss** |
| [[L06 dup2 Redirection and Non-Blocking IO]] | `dup2` semantics; redirection written out; the `2>&1` ordering trap; the pipe EOF rule and `wchan`; `FD_CLOEXEC` as a capability; `EAGAIN`; **`writev` 3.2× faster** |
| [[LAB 1 Building a Pipeline in C]] | `ls \| grep \| wc` with no shell. **Monday of Week 2** |
| `lab/pipeline.c`, `lab/Makefile`, `lab/compare.sh` | The skeleton, the build, and eight checks against the shell as oracle |
| [[PS 1 Redirection and the Cost of a System Call]] | Implement `<`, `>`, `>>`, `2>`, `2>&1`; the three tables; two measurements. Due **Friday of Week 2** |
| [[PROG201 Week1/assignments/QUIZ 1 Week 1 Tuesday\|QUIZ 1 Week 1 Tuesday]] | Ten minutes, covers **Week 0**, answer key printed |
| [[PROG201 Week1/resources/Reading Guide Week 1\|Reading Guide Week 1]] | APUE Ch. 3 in full, §5.4 again, and the four man pages worth reading properly |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**The offset is not in the descriptor and it is not in the file.**

It is in the thing between them, and that thing is created by `open` and shared by `dup` and `fork`. Every surprising result this week is that sentence:

- `dup` then write twice → `11112222`, because one offset.
- `open` twice then write twice → `2222`, because two offsets, and **half the data is gone with no error**.
- `fork` then write in both → `parent1child!parent2`, because one offset, which is exactly what makes shell redirection work.
- Four processes appending with `lseek`+`write` → **4,396 lines of 80,000 survive**. With `O_APPEND` → all 80,000.

**Two system calls are not one.** That is the general form, it is the same lesson as `O_CREAT|O_EXCL`, and it is the reason Unix has so many single-purpose flags: a flag is cheaper than a lock, and the kernel is the only place the fusing can happen.

---

### Assessment Reminder

**Labs and quizzes carry no weight** and are still required. **Quiz 1 is at the start of Tuesday's lecture and covers Week 0**; the answer key is printed in the paper and you mark it yourself before leaving.

> **There is no lab this week.** Lab 0 was sat on the Friday that closed Week 0; **Lab 1 covers this
> week and is sat on the Monday of Week 2**, because this course's lab day comes before its
> lectures. From here on it is every Monday.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 0's `fork` is this week's inheritance rule.** L01 §3 listed "open file descriptors, sharing the file offset" as inherited; L04 §4 is what that costs and what it buys. The stdio buffer duplicated by `fork` in W0 L01 §6 is L05 §2's 4 KB row.

**Sideways:** **CS 201 Week 1 is running IEEE 754 this week**, and the two courses meet at a specific place: `read` and `write` move bytes, and what those bytes *mean* is CS 201's subject. The 4 KB flattening point in L05 §2 is CS 201's page, and CS 201 Week 6 is where the page table it lives in gets explained.

**Forward:** **Week 2 is pipes and IPC properly** — L06's `pipe()` becomes FIFOs, message queues and shared memory, and the 64 KB capacity measured here becomes a design constraint. **Week 5's server is `write_all` and `EAGAIN` at scale.** **Week 6's shell is Lab 1 plus a parser plus job control**, and the pipe wiring does not change. **Project 1 starts from Lab 1's file.**

---

*PROG 201 · Week 1 · © CSE Department*
