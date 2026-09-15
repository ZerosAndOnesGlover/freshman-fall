# CS 202 · Reading Guide · Week 4
## Deadlock: OSTEP Chapter 32, and Silberschatz on the Banker

---

**The curriculum names no reading for Week 4**, and this week has **Midterm 1 on Monday evening.** The reading below is short on purpose. **Do it after the midterm**, not before — nothing in it is on the paper.

| Source | Now? | Why |
|---|---|---|
| **OSTEP 32. Common Concurrency Problems** | **Read** | Non-deadlock bugs first (atomicity and order violations), then the four conditions, prevention, avoidance by scheduling, detection. **L13 and L14** |
| **Silberschatz, Ch. 8 "Deadlocks"** | **Read §8.3–8.8** | The resource-allocation graph, **the Banker's algorithm** with its worked example, and the **detection algorithm** for several instances. **L14 §3 and L15 §1**; OSTEP does not give the Banker's algorithm in full |
| xv6 book, Ch. 4, the section on lock ordering | **Read** | How xv6 avoids deadlock without detecting it. **L13 §7** |
| **Coffman, Elphick & Shoshani (1971)**, "System Deadlocks", *ACM Computing Surveys* 3(2) | *Optional* | Where the four conditions come from. Short and readable |

**If you have two hours:** Silberschatz §8.6 (the Banker) with a pencil, then OSTEP 32 §32.3, then the xv6 section.

---

## OSTEP Chapter 32

OSTEP opens with a study of real concurrency bugs and finds that **most are not deadlocks**. Keep that in mind; the week is about deadlock, but the chapter's first half is the more common problem.

1. OSTEP distinguishes **atomicity violations** and **order violations**. **Classify L10 §1's race and L12 §3's one-CV deadlock** as one or the other, or neither.
2. §32.3 lists four prevention strategies, one per condition. **For each, give the concrete Week 3 or Week 4 program in this course that uses it** — or say that none does.
3. OSTEP's `trylock` example for breaking hold-and-wait says it can **livelock**. **L15 §4 measures it: 32 failed attempts per success on two CPUs.** Before reading L15, predict what adding a random delay does, and why.
4. §32.3's lock-ordering advice includes **ordering by address**. **What goes wrong if two locks are ever freed and reallocated at different addresses** while a thread holds one of them? Is it still safe?
5. OSTEP calls avoidance by scheduling "only useful in very limited environments". **After L14, say what the Banker's algorithm needs to know in advance** that a general-purpose OS never knows.

---

## Silberschatz Chapter 8 — the Banker

Work §8.6.3's example **by hand before looking at L14 §3**. The reference program reproduces the book exactly, so you can check yourself.

6. Compute **Need** from **Max** and **Allocation** for the five processes, and find **a** safe sequence. Is it the same as the book's? **Must it be?**
7. The book grants P1's request (1, 0, 2) and refuses P0's (0, 2, 0). **Show why P0's makes the state unsafe**: after pretending to grant it, find the first step at which no process's need fits in *Work*.
8. **An unsafe state is not a deadlocked state.** Give a sequence of future events, starting from the unsafe state in question 7, in which no deadlock ever happens. *(Hint: what if the processes never ask for their full maximum?)*
9. §8.7's **detection algorithm** looks almost identical to the safety algorithm. **Name the two differences** and say why each is needed.

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| **Love**, Ch. 10 | Kernel lock ordering and `lockdep` | For L14 §2 |
| `man 3 pthread_mutexattr_settype`, `man 3 pthread_mutexattr_setrobust` | Error-checking and robust mutexes | **Before Lab 4**, and for L15 §6 |
| `man 5 proc`, under `/proc/pid/wchan` and `/proc/pid/syscall` | Diagnosing a hung process | **Before Lab 4** |
| `man 2 futex` | The arguments you will read out of `/proc/<tid>/syscall` | **Before Lab 4** |

**Before Lab 4 you must know how to run a program under `gdb` and get every thread's backtrace**: `run`, Ctrl-C, `info threads`, `thread apply all bt`. PROG 201 taught all four.

---

## The One Habit This Guide Is Trying To Build

**A deadlock is a cycle in a graph, and you should be able to draw the graph from the evidence.**

Every tool this week — `/proc`, `gdb`, the detection algorithm — produces the same thing: who holds what, and who is waiting for what. **The skill is turning those facts into the graph and finding the cycle**, and then finding the one lock acquisition in the source code that, taken in a different order, would have made the cycle impossible.

---

*CS 202 · Week 4 · Reading Guide · © CSE Department*
