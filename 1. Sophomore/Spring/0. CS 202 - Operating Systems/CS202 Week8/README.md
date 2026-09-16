# CS 202 · Operating Systems
## Week 8: File Systems II — Crash Consistency and Modern Designs

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** CS 201, PROG 201
**Assessment for this course (overall):** Problem Sets 30%, Projects 30%, Midterms 25%, Final 15%
**This week's deliverables:** **Midterm 2** (Monday, 18:00–19:15, VNC 100, **Weeks 4–7**, 12.5%), PS 7 due **Friday**, PS 8 released **Wednesday**, **Quiz 8** at the start of **Monday's** lecture (covers Week 7).
**Lab 7 is sat on the Tuesday of this week**, the afternoon after the midterm; **Lab 8 covers this week and is sat on the Tuesday of Week 9.**

> ### **This is the first week back from Spring Break, and Midterm 2 is that Monday evening.**
> 18:00–19:15, VNC 100, covering **Weeks 4–7** — deadlock, memory, page replacement, file systems.
> **Nothing from Week 8 is on the paper.**
> [[CS202 Week8/resources/MIDTERM 2 Revision Guide|MIDTERM 2 Revision Guide]] has the structure and
> what belongs on your sheet. **Quiz 8 is the same morning, and Lab 7 the next afternoon.**
>
> **Project 1 is now three weeks from its deadline** (Friday of Week 11). Part A should be working.

---

### Why This Week Exists

Because Week 7 ended with a file system that is correct only if nothing goes wrong.

**One `create` is four block writes, and the machine may stop between any two of them.** Measured on `myfs` without a journal: **36 of 93 crash points left the file system broken** — inodes allocated that no name reaches, blocks marked used that nothing points at — and **not one crash left the finished operation.**

**This week is the two answers.** A **journal** writes everything down before doing it, so that one block write — the commit record — decides whether the operation happened: measured, **0 of 118 crash points inconsistent**, and 20 of them recovered into the completed operation. **Copy-on-write** never overwrites at all, which makes snapshots nearly free — measured at **196 KiB for a snapshot of a 64 MiB image** — and makes the first write to a region cost a whole cluster.

**And the week ends with what neither promises**: ext4 detects a flipped byte in its own metadata and hands you a corrupted file byte with a clean `fsck`.

---

### Learning Objectives

By the end of Week 8, you should be able to:

1. Enumerate the states a **crash during a multi-block operation** can leave, and mark which are repairable.
2. Explain why **write ordering alone** is not enough, and what the only ordering primitive costs.
3. Say what **`fsck`** can and cannot repair, and why its cost is the reason journals exist.
4. Explain **write-ahead logging** — log, commit, install, clear — and identify **the commit point**.
5. Explain **why replay is idempotent**, and what a journal without recovery is worth.
6. Read **xv6's `log.c`**, and explain absorption, batching, and `MAXOPBLOCKS`.
7. **Measure a journal's cost** in writes, and explain why it is neither 1× nor 2×.
8. Explain ext4's **`data=ordered`, `writeback` and `journal`** modes and what each promises about your data.
9. Explain **copy-on-write**, and measure snapshot cost, write amplification and its latency.
10. Explain why **snapshots pin free space**, and what that does to a full file system.
11. Explain **checksums in the parent pointer**, and what ZFS can do that ext4 cannot.
12. **Crash a file system at every possible point** and classify what each crash left.

---

### This Week's Materials

| File | Purpose |
|---|---|
| [[L25 Crash Consistency What Tears]] | The five states a torn `create` can leave; **36 of 93 crash points inconsistent without a log**, with one shown in full; why ordering alone fails; what `fsck` repairs and what it costs |
| [[L26 Journaling]] | Log, commit, install, clear; **0 of 118 crash points inconsistent**, and **14 of 112 broken if recovery is skipped**; xv6's `log.c`, absorption and batching; **1.23× and 2.3× write costs**; ext4's three modes |
| [[L27 Copy on Write and Checksums]] | **A 196 KiB snapshot of a 64 MiB image**; **16× write amplification at 64 KiB clusters, 1.5× at 4 KiB**; snapshots pinning free space; ZFS's checksums described; **ext4 catching a flipped inode byte and missing a flipped data byte** |
| [[CS202 Week8/assignments/QUIZ 8 Week 8 Monday\|QUIZ 8 Week 8 Monday]] | Ten minutes, covers **Week 7**, answer key printed — **midterm-day revision** |
| [[CS202 Week8/assignments/MIDTERM 2\|MIDTERM 2]] | **Monday, 18:00–19:15, VNC 100.** Weeks 4–7 |
| [[CS202 Week8/resources/MIDTERM 2 Revision Guide\|MIDTERM 2 Revision Guide]] | Structure, the arithmetic to practise, what belongs on your sheet |
| [[PS 8 A Journal for myfs]] | Add the log to PS 7's file system, recover from every crash point, and measure what it costs. Due **Friday of Week 9** |
| `assignments/ps8/myfsj.c` | The file system with five log functions to write |
| [[LAB 8 Snapshots Checksums and Crashes]] | qcow2 copy-on-write instead of ZFS; corrupting metadata and data; sweeping every crash point. **Tuesday of Week 9** |
| `lab/crashsweep.sh` | Stops an operation after every possible number of writes and checks what is left |
| [[CS202 Week8/resources/Reading Guide Week 8\|Reading Guide Week 8]] | OSTEP 42–43, xv6 Chapter 8, the ZFS and btrfs papers |
| `solutions_instructor/` | Instructor only — including the journaled reference and the unjournaled one with crash support |

---

### The One Thing to Take From This Week

**Atomicity on a disk means making one block write decide everything.**

The journal does it with a commit record; copy-on-write does it with a new root; L23's safe update did it with `rename`. **Everything else is arranged around that single write** — logged first, or written to free space first — so that the machine can stop at any moment and the disk still means something.

**And consistency is not correctness.** A recovered file system is one whose own structures agree; whether your data is in it is a separate promise, made only by `fsync`, and whether the bytes are the ones you wrote is a third promise that ext4 does not make at all.

---

### Assessment Reminder

**Midterm 2: Monday, 18:00–19:15, VNC 100, Weeks 4–7, 12.5%.**

**PS 7 is due Friday at 17:00. PS 8 is released Wednesday.** **Project 1 is due Friday of Week 11.**

**Labs and quizzes carry no weight** and are still required. **Quiz 8 is at the start of Monday's lecture and covers Week 7.**

> **Two labs touch this week.** **Lab 7** — the page cache — is sat on the **Tuesday of this week**,
> the afternoon after the midterm. **Lab 8** covers this week and is sat on the **Tuesday of Week 9**.

Both are tracked in [[_CS 202 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 7's `myfs`** is what PS 8 adds a journal to, and **L23's write-back** is why the order of writes is not yours to choose. **Week 3's atomicity** is the same problem one level down: there, one instruction; here, one block. **Week 5's copy-on-write `fork`** is L27's mechanism applied to memory.

**Sideways:** **PROG 202**'s persistent data structures are copy-on-write by construction — the same trade, with the same free-space question.

**Forward:** **Week 9's device driver** is what actually carries these writes to the disk, and where the flush command is issued. **Week 11's Raft log** is this week's journal replicated across machines — commit record and all. **Week 12** returns to checksums as integrity, not just reliability.

---

*CS 202 · Week 8 · © CSE Department*
