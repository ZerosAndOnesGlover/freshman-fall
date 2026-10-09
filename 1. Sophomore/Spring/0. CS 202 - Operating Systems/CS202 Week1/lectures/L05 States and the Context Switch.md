# CS 202 · Operating Systems
## Week 1 · Lecture 2 of 3
### States, and the Context Switch

*“...our intellectual powers are rather geared to master static relations and... our powers to visualize processes evolving in time are relatively poorly developed.”* — Edsger W. Dijkstra, "Go To Statement Considered Harmful" (1968)

---

**Sat:** Wednesday of Week 1, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 6 §6.3; xv6 book Ch. 5 on context switching; `swtch.S` · **Next:** L06, address spaces and a process from `fork` to `wait`

**Coursework:** 📝 **PS 1** released today, due Fri of Week 2 17:00 · 📝 **PS 0** due Fri this week 17:00 · 📊 **Quiz 2** Mon of Week 2 · 🔬 **Lab 1** Tue of Week 2 15:00–16:50

---

## 1. The State Machine

OSTEP gives a process three states — **running**, **ready**, **blocked** — and every real kernel has more, because the three leave out the beginning and the end.

**xv6 has six**, in `proc.h`, and each transition is one function in `proc.c`:

| From → To | Caused by | Function |
|---|---|---|
| `UNUSED` → `EMBRYO` | a slot is claimed for a new process | `allocproc` |
| `EMBRYO` → `RUNNABLE` | the new process is ready to run | `fork`, `userinit` |
| `RUNNABLE` → `RUNNING` | a CPU picks it | `scheduler` |
| `RUNNING` → `RUNNABLE` | **the timer took the CPU away** | `yield` |
| `RUNNING` → `SLEEPING` | it must wait — for a disk block, a pipe, a child | `sleep` |
| `SLEEPING` → `RUNNABLE` | what it waited for happened | `wakeup` |
| `RUNNING` → `ZOMBIE` | it called `exit` | `exit` |
| `ZOMBIE` → `UNUSED` | its parent collected it | `wait` |

**`EMBRYO` and `ZOMBIE` are the two OSTEP leaves out**, and both exist to fence off a process that is half-built or half-destroyed so that no other code mistakes it for a live one.

**Linux reports at least seven**, as one letter in `/proc/<pid>/stat`. `states.c` puts a process in each on purpose and reads it back:

| What the process is doing | State | Meaning |
|---|---|---|
| a busy loop | **R** | running, or runnable and waiting for a CPU — Linux does not distinguish them here |
| `pause()` | **S** | sleeping, *interruptible*: a signal will wake it |
| stopped by `SIGSTOP` | **T** | stopped |
| exited, not yet reaped | **Z** | zombie |
| stopped under `ptrace` | **t** | tracing stop — a debugger holds it |
| **parent waiting inside `vfork()`** | **D** | sleeping, *uninterruptible*: no signal will wake it until the child `exec`s or exits |
| this process, reading `/proc` | R | |

**`D` is the one to respect.** A process in uninterruptible sleep is inside the kernel waiting for something that must complete — classically a disk I/O — and **even `SIGKILL` waits for it.** A machine with processes stuck in `D` is a machine with a device or a filesystem that has stopped answering.

**And across the whole reference machine, at one instant:**

```
$ ps -eo stat= | cut -c1 | sort | uniq -c
    261 S
     81 I
      1 R
```

**One process running — `ps` itself — out of 343.** 261 are asleep, and 81 are **`I`**, *idle* kernel worker threads, which are asleep in a way the kernel does not count towards the load average. **This is L01's "81% idle" seen from the other side**: nearly everything is waiting, and a waiting process costs memory and no CPU.

---

## 2. Two Ways to Leave the CPU

A running process gives up the CPU in one of two ways, and the kernel counts both, per task, in `/proc/<pid>/status`:

- **Voluntarily** — it asked for something it has to wait for: a `read` with no data, a `sleep`, a `wait`. It goes to `SLEEPING`.
- **Involuntarily** — it wanted to keep running and **was preempted**, by the timer or because something more urgent woke up. It goes to `RUNNABLE`.

`hog.c` pins two children to the same CPU for five seconds — one that never stops computing, one that sleeps for a millisecond at a time — and reads both counters:

| | Voluntary | Involuntary |
|---|---:|---:|
| **hog** — `for (;;) x++;` | **0** | **4,788** |
| **sleeper** — `for (;;) usleep(1000);` | **4,748** | **0** |

**Perfectly complementary.** The hog never once gave up the CPU; it was taken from it 4,788 times, roughly once per millisecond. The sleeper never once had it taken away; it gave it up 4,748 times. **Both are true of every process on the machine, and the ratio tells you what kind of process it is.** Week 2's scheduler uses exactly this distinction to decide who is interactive.

---

## 3. The Switch in xv6

A context switch is **saving one flow of control's registers and loading another's.** xv6's is the clearest there is. Follow a CPU-bound process being preempted:

```
user code running in process A
   │  timer interrupt (lapic.c: TICR 10,000,000, vector IRQ_TIMER)
   ▼
alltraps           trapasm.S   saves A's user registers: struct trapframe, 76 bytes
trap()             trap.c:107  "if it's the timer, and a process is running: yield()"
yield()            proc.c:386  A->state = RUNNABLE
sched()            proc.c:366
swtch(&A->context, cpu->scheduler)      proc.c:380   ── A's kernel stack → scheduler's stack
   ▼
scheduler()        proc.c:323  loop over ptable for a RUNNABLE process — finds B
switchuvm(B)                   load B's page table (CR3) and kernel stack (TSS)
swtch(&cpu->scheduler, B->context)      proc.c:346   ── scheduler's stack → B's kernel stack
   ▼
... returns inside B's earlier call to sched(), then yield(), then trap() ...
trapret            trapasm.S   restores B's user registers from B's trapframe
iret                           user code running in process B
```

**Two saves of two different register sets.** The trap frame holds the **user** registers, pushed on entry to the kernel exactly as in L03. The context holds the **kernel** registers at the moment of the switch. xv6 goes through a separate **scheduler thread** per CPU — A to scheduler, scheduler to B — so there are two `swtch` calls per process switch.

### `swtch.S`, all of it

```asm
.globl swtch
swtch:
  movl 4(%esp), %eax        # struct context **old
  movl 8(%esp), %edx        # struct context *new

  # Save old callee-saved registers
  pushl %ebp
  pushl %ebx
  pushl %esi
  pushl %edi

  # Switch stacks
  movl %esp, (%eax)
  movl %edx, %esp

  # Load new callee-saved registers
  popl %edi
  popl %esi
  popl %ebx
  popl %ebp
  ret
```

**Four registers and a return address.** That is `struct context` — `edi`, `esi`, `ebx`, `ebp`, `eip`, **20 bytes** — and the `eip` is not pushed explicitly, because the `call` to `swtch` already put it there.

**Why only four?** The x86 calling convention CS 201 taught: **`eax`, `ecx` and `edx` are caller-saved.** Whoever called `swtch` has already saved anything it needed from them, because any function call may destroy them. `swtch` is a function call. **So it saves exactly the registers a function call must preserve, and nothing else** — the user registers are safe in the trap frame, and the caller-saved ones are the caller's problem.

**The moment of the switch is one instruction: `movl %edx, %esp`.** Before it, the CPU is on the old stack; after it, every `pop` reads the new process's saved values, and the final `ret` returns into wherever *that* process called `swtch` — possibly many seconds ago.

---

## 4. Linux's Version Is the Same Idea

Linux's x86-64 switch is `__switch_to_asm`, and the frame it leaves on the outgoing task's kernel stack is declared in `arch/x86/include/asm/switch_to.h`, readable in the reference machine's headers:

```c
struct inactive_task_frame {
    unsigned long r15;
    unsigned long r14;
    unsigned long r13;
    unsigned long r12;
    unsigned long bx;
    unsigned long bp;
    unsigned long ret_addr;
};
```

**Six callee-saved registers and a return address — 56 bytes.** They are exactly the x86-64 System V callee-saved set, for exactly xv6's reason. The user registers are already in `pt_regs`, from the entry in L03 §2.

**Two differences worth knowing:**

1. **Linux switches directly from the old task to the new one**, inside `schedule()`, without passing through a scheduler thread. One stack switch per process switch, not two.
2. **Linux also switches the FPU, and that register set is not 56 bytes.** §6.

---

## 5. What a Switch Costs

**You cannot time a single context switch** — it happens in the kernel, between two instructions of two different processes. So measure many, in a way that forces them.

`ctxsw.c` has two processes pass one byte back and forth through two pipes. Each `read` finds nothing and sleeps; each `write` wakes the other side. **It counts the switches that actually happened**, voluntary and involuntary, in both processes, and **separately times the same `write` and `read` in one process where no switch can occur.** On the reference machine:

```
baseline: one write+read pair with no other process: 1438 ns
CPUs 2 and 2: 1.224 s for 200000 rounds; 400009 switches (2.00 per round); 0.575 s of that is the calls; 1622 ns per switch
CPUs 2 and 3: 1.431 s for 200000 rounds; 399890 switches (2.00 per round); 0.575 s of that is the calls; 2139 ns per switch
```

| | Per switch |
|---|---:|
| both processes on one CPU | **≈ 1.6 µs** |
| on two different CPUs | **≈ 2.1 µs** |

**Exactly two switches per round**, which is what a ping-pong should cause: one on each side. Subtract the system calls — four per round, two `write`+`read` pairs — and divide what is left by the switches.

> **This is an upper bound on the switch alone, not an exact figure.** The subtraction assumes a
> `write` and `read` cost the same whether or not they block and wake someone, and they do not:
> putting a task to sleep and waking another does work that the baseline never does. **What
> 1.6 µs measures is "one switch and the sleeping and waking that caused it"**, which is the
> number that matters for a program — nobody switches without a reason.

**Why is the cross-CPU case slower, when there is no competition for a CPU at all?** Because each side, after writing, has nothing to do and **its CPU goes idle** — and the other side's `write` must then wake a sleeping CPU with an **inter-processor interrupt**. On one CPU the woken task simply runs next. The counters confirm the difference: on two CPUs, **every switch in both processes was voluntary** (199,981 and 199,960, with 1 and 2 involuntary); on one CPU they split roughly half and half, because the task that writes is often **preempted by the task it just woke** before it can reach its own `read`.

**The curriculum's range is 1–10 µs, and 1.6 µs is inside it.** At L01's 9,533 switches per second across 8 CPUs — about 1,200 per CPU — the direct cost is around **2 ms of CPU time per second per CPU, 0.2%**. That is the part a ping-pong can see. **What it cannot see** is the cost of a switch to a process with a large working set, whose caches and TLB entries went cold while it was away. The ping-pong's working set is one byte.

---

## 6. The Register Set Nobody Mentions: the FPU

The curriculum's account of the context switch says the kernel saves the general-purpose registers and the instruction pointer, and that **the FPU and SSE state — "hundreds of bytes" — is saved lazily**: only when the new process first uses a floating-point instruction, signalled by a fault.

**How big is it?** `xsave.c` asks the CPU:

```
XSAVE area: 1088 bytes for the features enabled in XCR0
```

**1,088 bytes** — x87, SSE, AVX and MPX state — **against 56 for the integer switch frame. Nineteen times larger.** Saving it on every switch is real work, which is exactly why lazy saving was invented: most processes never touch the FPU between switches, so why save what has not changed?

**Linux no longer does it that way.** The reference machine's headers, `arch/x86/include/asm/fpu/sched.h`:

```c
/*
 * switch_fpu() saves the old state and sets TIF_NEED_FPU_LOAD if
 * TIF_NEED_FPU_LOAD is not set.  This is done within the context
 * of the old process.
 *
 * Once TIF_NEED_FPU_LOAD is set, it is required to load the
 * registers before returning to userland or using the content
 * otherwise.
 */
```

**The outgoing task's FPU state is saved at every switch — eagerly.** Only the *restore* is deferred, to the moment the incoming task returns to user space, and it is skipped if that task last ran on this CPU and nothing has touched the registers since. **There is no fault on first use.** Lazy FPU switching was abandoned: modern CPUs save the state quickly with `XSAVEOPT`, which skips components that have not changed, and in **2018 the *LazyFP* disclosure showed that lazily switched FPU state could be read speculatively by the next process** — the Meltdown pattern from L02 §6, applied to floating-point registers. **The curriculum describes a real design that Linux has retired**; the syllabus records the difference.

### xv6 does not save it at all

xv6's `struct context` has no FPU state, its trap frame has none, and nothing in `swtch.S` touches it. **So what happens to two xv6 processes that both use floating point?**

`fpu.c` forks, and both processes add `0.5` to a `double` twenty million times, checking forty times along the way. Built into xv6 and run on one CPU:

```
$ fpu
child : 40 of 40 checkpoints wrong, final x*2 = 39552364 (expected 20000000)
parent: 40 of 40 checkpoints wrong, final x*2 = 447636 (expected 20000000)
```

*(The two lines were interleaved on the console character by character; they are separated here.)*

**Both are wrong — each should be 20,000,000. And 39,552,364 + 447,636 = 40,000,000 exactly**: the two correct answers, added together. A second run: **39,786,312 + 213,688 = 40,000,000.**

**The two processes shared one accumulator.** During the loop, `x` lives in the x87 register stack, which is part of the CPU, not part of either process. When the timer switched from one process to the other, xv6 saved four integer registers and left the FPU exactly as it was — **so the other process continued adding to the first one's number.** Between them they did all 40 million half-additions into the same register, and the total is perfect. Neither process's answer is.

**On two CPUs the damage shrinks, and does not go away.** Booted with `CPUS=2`:

```
child : 0 of 40 checkpoints wrong, final x*2 = 20000000 (expected 20000000)
parent: 1 of 40 checkpoints wrong, final x*2 = 19958711 (expected 20000000)
```

Mostly the two processes ran on different CPUs, each with an x87 of its own, and the child was exactly right. **But a process is not tied to a CPU**, and at some point in the parent's run the two came to share one across a switch. **More CPUs made the bug rarer — which is worse**, because now it is a bug that passes most of its tests.

> **State the kernel does not save is state the processes share.** No security boundary, no
> isolation, no error — just two programs quietly computing one wrong answer each. **This is the
> same lesson as L02 §5, from the other direction**: there, a protection that was configured did
> not operate; here, a mechanism that every textbook describes is simply absent, and nothing
> reports it. PS 1 Q4 asks you to design the fix.

---

## 7. What to Take Away

1. **xv6 has six states and Linux at least seven**; `EMBRYO` and `ZOMBIE` fence off half-built and half-destroyed processes, and `D` is a sleep no signal can interrupt.
2. **At any instant almost everything is asleep**: 1 running of 343 on the reference machine.
3. **Voluntary and involuntary switches say what kind of process it is**: the hog 0 and 4,788, the sleeper 4,748 and 0.
4. **xv6's `swtch` saves four callee-saved registers and a return address — 20 bytes**; Linux's saves six and a return address — 56 bytes. The user registers are already in the trap frame, and the caller-saved ones are the caller's.
5. **A switch costs about 1.6 µs here, 2.1 µs across CPUs** — an upper bound, including the sleeping and waking that caused it.
6. **FPU state is 1,088 bytes**. Linux saves it eagerly at every switch and restores it on return to user space. **xv6 does not save it at all, and two processes' floating-point sums merged into exactly one.**

---

## Exercises

1. Run `ctxsw.c` with both processes pinned to CPU 0 instead of 2. Does the per-switch figure change? What else runs on CPU 0 on your machine? *(`cat /proc/interrupts`, first column.)*
2. In `hog.c`, give the hog `nice -n 19`. Predict the sleeper's two counters before you run it, then explain what did or did not change.
3. In xv6, add a `cprintf` to `swtch`'s caller in `sched()` that prints the PID being switched away from. Boot it. **Why does the console become unusable almost immediately?** *(Count.)*
4. xv6's `struct context` includes `eip` but `swtch.S` never pushes it. Where does it come from? Where is it popped?
5. Why does Linux's `inactive_task_frame` contain `r12`–`r15` but not `r8`–`r11`? Answer from the x86-64 calling convention, not from memory of the struct.

---

*CS 202 · Week 1 · L05 · © CSE Department*
