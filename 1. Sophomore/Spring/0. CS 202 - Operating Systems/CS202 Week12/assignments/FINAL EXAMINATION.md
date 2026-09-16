# CS 202 · Operating Systems
# FINAL EXAMINATION

**Wednesday of finals week · 09:00–11:30 · VNC 100, overflow to TH 200**
**150 minutes · 100 marks · 15% of the course**

---

**Name:** _________________________________ **Student ID:** ___________________ **Section:** ________

---

> **Comprehensive: Weeks 0–12.**
>
> **Permitted:** **two handwritten pages of A4, both sides.** No calculators, no electronic devices.
> **All arithmetic on this paper is designed to be done by hand**, and the numbers are small on
> purpose.
>
> **Answer all five questions.** Each is worth 20 marks. **Show your working** — a table with a
> wrong final number earns most of the marks; a bare number earns few.
>
> **Where a question asks for a measured figure from the course, an order of magnitude is
> accepted.** "About a microsecond" earns what "840 ns" earns. **Where it asks what you would
> measure, a specific command or program earns the marks and a description does not.**
>
> If a question seems to need something you were not given, **state your assumption and continue.**

---

## Question 1 — One Mechanism, Several Times (20 marks)

**(a) [9]** For **each** of the three mechanisms below, name **the interposition point** (what makes the check unavoidable), **the table** it consults, and **the cache** of that table — or state that there is none. Then name **what invalidates the cache**.

| | Mechanism |
|---|---|
| (i) | **Address translation** for a user process |
| (ii) | **Reading a file** that was read a moment ago |
| (iii) | **A guest's access to an emulated device**, under KVM |

**(b) [6]** A program reads a 16 MiB file. Take a system call to cost **1 µs** and a function call to cost **2 ns**.

1. Reading **one byte at a time**: how many system calls, and roughly how long in system call overhead alone?
2. Reading **64 KiB at a time**: the same two numbers.
3. **State the ratio**, and name the general design rule it demonstrates.

**(c) [5]** Below are four costs measured in this course. **Put them in order, smallest first**, and for **each adjacent pair** give one sentence on what the gap buys:

> a TLB miss · a page fault on first touch · a VM exit · a round trip to another machine

---

## Question 2 — Concurrency and Deadlock (20 marks)

**(a) [6]** Two threads:

```c
/* thread one */                      /* thread two */
lock(&A);                             lock(&B);
lock(&B);                             lock(&A);
   /* work */                            /* work */
unlock(&B); unlock(&A);               unlock(&A); unlock(&B);
```

Name **Coffman's four conditions**, say **which one the fix removes**, and give the fix in one line. Then: **a colleague proposes `trylock` and retry instead.** Say what that trades the deadlock for, and name the measurement from this course that showed the trade is real.

**(b) [10]** Four processes, three resource types. **Available = (2, 1, 2).**

| | **Max** | | | **Allocation** | | |
|---|---|---|---|---|---|---|
| | A | B | C | A | B | C |
| **P0** | 4 | 2 | 3 | 1 | 0 | 2 |
| **P1** | 3 | 3 | 3 | 2 | 1 | 1 |
| **P2** | 5 | 1 | 4 | 3 | 0 | 2 |
| **P3** | 2 | 2 | 2 | 0 | 1 | 1 |

1. **[3]** Compute the **Need** matrix.
2. **[4]** Is this state safe? **Show the safety check** and give a safe sequence, or show that none exists.
3. **[3]** **P0 requests (2, 1, 0).** The resources are available. **What does the Banker's algorithm do, and why?**

**(c) [4]** From the same original state, **P2 requests (2, 1, 2)** and it is **granted**, leaving **Available = (0, 0, 0)**.

**Nothing is available and the state is still safe.** Explain how both can be true — and say what assumption about the four processes the whole algorithm rests on.

---

## Question 3 — Memory (20 marks)

**(a) [10]** The reference string, **six distinct pages, twenty references**:

```
7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1
```

1. **[6]** Fill in the table. Count **every** fault, including the compulsory ones.

| Frames | FIFO | LRU | OPT |
|---|---|---|---|
| **3** | | | |
| **4** | | | |

2. **[2]** **At four frames, two of the three algorithms tie.** Which, and what does that say about this string?
3. **[2]** Belady's anomaly is **not** visible in your table. **State what it is**, and say what you would have to change about the string to show it.

**(b) [5]** A process has a 2 GiB working set and the machine's TLB holds 1,536 entries.

1. **[3]** What is the **TLB reach** with 4 KiB pages, and with 2 MiB pages?
2. **[2]** This course measured the resulting difference as about **17 ns per access** at 2 GiB. **Why is that number small at a 4 MiB working set and large at 2 GiB?**

**(c) [5]** A machine with 7.7 GiB of RAM runs a program whose working set is 1% larger than the memory available to it.

1. **[3]** Describe what happens to throughput, and **why the collapse is abrupt rather than gradual**.
2. **[2]** Eventually the OOM killer chooses a victim. **Name the two inputs to its choice**, and state which one the administrator controls.

---

## Question 4 — Storage and Crash Consistency (20 marks)

**(a) [8]** An inode has **512-byte blocks** and **4-byte block numbers**, so a block holds **128** pointers.

1. **[2]** xv6 as shipped: **12 direct** and **one indirect**. Largest file, **in bytes**?
2. **[3]** Project 2's version: **11 direct, one indirect, one double indirect**. Largest file, in bytes? **Account for every block.**
3. **[3]** Why must the inode **not** change size when you add the double indirect pointer? Say what breaks if it does.

**(b) [7]** A file system appends a block to a file. Three things must reach the disk: **the data block**, **the inode** (with the new size and pointer), and **the free-block bitmap**.

1. **[3]** **Give an order in which a crash leaves the file system inconsistent, and say what the inconsistency is.** Name the worst of the possible inconsistencies and say why it is the worst.
2. **[4]** A journal is added. **State the rule that makes the journal work**, name the barrier that enforces it, and say what the journal costs in the steady state — **and what `fsync` returning actually promises.**

**(c) [5]** You are given a file system and a claim: *"it is crash-consistent."* **Describe the experiment that tests the claim** — how you interrupt it, what you vary, and what you check afterwards. **State one way the experiment can report success when the file system is broken.**

---

## Question 5 — Distribution and Protection (20 marks)

**(a) [7]** Five nodes run Raft.

1. **[2]** How many must agree to elect a leader, and **how many failures does that tolerate**?
2. **[2]** The cluster is grown to **six** nodes. Give the new majority, and say **how many failures it now tolerates.** Comment.
3. **[3]** A partition splits the five nodes into **3 and 2**. Describe what each side does, **how many leaders exist in the cluster**, and why this does **not** violate Raft's safety property. Then say what happens to the minority's leader when the partition heals.

**(b) [6]** A program you downloaded is to be run on this laptop.

1. **[2]** Write the **threat model** in three lines: what is protected, from whom, and what is out of scope.
2. **[2]** You run it under a sandbox that sets resource limits and a seccomp allowlist. **Name two things it still can do**, given that it runs as you.
3. **[2]** The sandbox costs about **50 ns per system call**. **Is that a reason not to use it?** Answer with the comparison that settles it.

**(c) [7]** Each of the following is a claim someone made about a machine. **For each, give the one command or program you would run to test it, and say what result would show the claim to be false.**

1. **[2]** *"This kernel is built with UMIP, so user code cannot read descriptor-table addresses."*
2. **[2]** *"Adding these rules to our seccomp filter will slow the service down, so we kept the filter short."*
3. **[3]** *"Our sandbox limits each job to 40 processes, using `RLIMIT_NPROC`."*

---

> **End of paper.**
>
> **Before you hand in:** every question that asked for a number should have one, and every number
> should have the working that produced it.

---

*CS 202 · Final Examination · © CSE Department*
