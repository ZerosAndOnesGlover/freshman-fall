# CS 202 · Midterm 1 · Revision Guide
## Weeks 0–3 · Sat Week 4, Monday 18:00–19:15, VNC 100

---

**75 minutes, 100 marks.** One handwritten sheet, **one side only**. No calculators, no devices.
**Covers Weeks 0–3.** Week 4's deadlock material is **not** examined.

**Arrive ten minutes early** with your student ID ([[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]]). Quiz 4 is the same morning and covers Week 3 — **its answer key is good revision for Q4.**

---

## What the Paper Looks Like

Five questions, twenty marks each, in course order:

| | Topic | Weeks | What it tends to ask |
|---|---|---|---|
| **Q1** | The kernel boundary | 0 | privilege, `SYSCALL`, **system-call cost arithmetic**, the vDSO |
| **Q2** | Processes and the context switch | 1 | xv6's states and `swtch`, **context-switch arithmetic**, what is not saved |
| **Q3** | Scheduling | 2 | **a schedule by hand**, weights and shares, real-time analysis |
| **Q4** | Synchronization | 3 | interleavings, **the three-state futex traced**, condition variables, spin or sleep |
| **Q5** | **Synthesis** — a design question about xv6 | 0–3 | a new feature, and what each week says about it |

**Budget fifteen minutes a question.** Q5 is worth as much as the others and needs thinking rather than recall, so **do not leave it until the last five minutes.**

---

## The Arithmetic You Must Be Able to Do by Hand

**No calculator.** Every calculation is designed for pencil — but you must know the method cold.

| Calculation | Method | Week |
|---|---|---|
| Calls and time for a file read | calls = ⌈size / buffer⌉ + 1 (the read that returns 0); time = calls × cost per call | L03 §4 |
| Per-switch cost from a ping-pong | (total time − calls × per-call cost) ÷ switches | L05 §5 |
| Turnaround and response | draw the timeline; turnaround = finish − arrival; response = first run − arrival | L07 |
| CPU shares from nice | weight ÷ sum of weights of **the tasks in the same group** | L08 §4, §7 |
| Liu–Layland bound | *n*(2¹ᐟⁿ − 1): 1.000, 0.828, 0.780, 0.757 … ln 2 | L09 §2 |
| Response-time analysis | *R* = *C*<sub>i</sub> + Σ ⌈*R*/*P*<sub>j</sub>⌉ *C*<sub>j</sub> over higher-priority *j*; iterate from *R* = *C*<sub>i</sub> until it stops changing or exceeds the deadline | L09 §2 |

**Practise one of each tonight**, from the lectures' own examples, **without looking at the answer first**.

---

## What Your One Side Should Have On It

**Worth the space** — hard to reconstruct under time pressure, cheap to write down:

- **The nice weights** you might need: nice 0 = 1,024, 1 = 820, 5 = 335, 10 = 110, 19 = 15. (The paper gives any weights it uses, but having them saves reading time.)
- **`SYSCALL`'s register effects**: `RCX` ← `RIP`, `R11` ← `RFLAGS`, `RIP` ← `IA32_LSTAR`; no stack switch.
- **xv6's six states** and the function behind each transition.
- **Drepper's three states** and exactly when `lock` and `unlock` enter the kernel.
- **The response-time analysis recurrence.**
- **The Linux state letters**: R, S, D, T, t, Z.

**Not worth the space** — you either know these or the sheet will not save you:

- Definitions: *process*, *race condition*, *critical section*, *mutual exclusion*.
- Measured numbers from the lectures. **The paper gives every number it expects you to use**; it examines whether you can reason with them, not whether you remember them.
- Anything from Week 4.

---

## What the Markers Are Looking For

**1. The mechanism, not the slogan.** *"fork returns twice"* earns nothing; *"the child's trap frame is a copy of the parent's with `eax` set to 0"* earns the marks.

**2. The interleaving, instruction by instruction.** A concurrency answer that says *"a race could occur"* is not an answer. Write the loads and stores in two columns.

**3. Bounds and assumptions stated.** When an estimate subtracts one cost from another, say what it assumes and which way the error goes.

**4. Where the machine disagreed with the book.** This course has repeatedly measured something textbooks describe differently — FPU saving, the scheduler, `nice` across groups. **Answer about the system the question describes**; if the question says "on Linux 7.0", the answer is not CFS.

---

## A Last Word on the Synthesis Question

Q5 describes a small new xv6 feature and asks four things about it — **one from each week**: where the kernel boundary is crossed and what it costs; what the kernel must not trust; which process state or record is involved; and which lock protects it. **If you get stuck on one part, answer the others**: they are independent, and each is worth five marks.

---

*CS 202 · Midterm 1 · Revision Guide · © CSE Department*
