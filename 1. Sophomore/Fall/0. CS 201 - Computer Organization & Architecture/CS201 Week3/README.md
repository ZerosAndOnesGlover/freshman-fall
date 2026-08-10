# CS 201 · Computer Organization & Architecture
## Week 3: Procedures, the Stack, and Calling Conventions

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), ECE 110 (digital logic)
**Assessment for this course (overall):** Problem Sets 35%, Midterms 25%, Final 20%, Projects 20%
**This week's deliverables:** PS 3 (due Week 4 Friday), Lab 3, and **Quiz 3 on Monday, covering Week 2**.

> **Midterm 1 is announced this week** — it sits in **Week 5** and covers **Weeks 0–4**. See the
> Assessment Calendar. Weeks 3 and 4 are the two that carry the most marks on it.

---

### Why This Week Exists

Because a function call is not a language feature. **It is a convention two pieces of machine code agree to follow**, and the hardware enforces none of it.

`call` pushes an address and jumps. `ret` pops an address and jumps. Everything else — which register holds argument three, who preserves `rbx`, where the locals live, whether `rsp` is a multiple of 16 — is agreement. When the agreement holds, code compiled by different compilers in different decades links and runs. When it breaks, you get wrong answers or a crash in a function that is not the buggy one.

**And the fact that `ret` jumps to unvalidated memory is the foundation of Week 9.** By Friday you will have overwritten a return address by hand and watched `rip` become `0xdeadbeef`.

---

### Learning Objectives

By the end of Week 3, you should be able to:

1. Write `call` and `ret` as explicit push/pop/jump sequences.
2. Draw a stack frame with the return address, saved `rbp`, saved registers and locals at their correct offsets — and account for its total size.
3. Explain why a value crossing a call must live in a callee-saved register.
4. Name the caller-saved and callee-saved sets, and state the obligation each places on whom.
5. Place all arguments of a mixed integer/floating-point signature, including any beyond six.
6. Explain why stack arguments are pushed in reverse and cleaned up by the caller.
7. Apply the 16-byte alignment rule and compute `rsp mod 16` at any point in a function.
8. Explain what the red zone is and when a function may use it.
9. **Write a correct recursive function in x86-64 assembly**, with justified register choices and correct alignment.
10. Read a frame in GDB — backtrace, `info frame`, and locals by address.
11. Explain why deep recursion is a memory-safety problem, and what actually stops it.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| `lectures/L10 Call Ret and the Stack Frame.md` | The mechanism; a real 48-byte frame accounted for; five recursive frames in GDB |
| `lectures/L11 The System V Calling Convention.md` | Argument registers, the stack beyond six, caller vs callee-saved, leaf functions |
| `lectures/L12 Alignment the Red Zone and Recursion.md` | The 16-byte rule and what breaks without it; the red zone; recursion by hand |
| `assignments/PS 3 Recursive Fibonacci in Assembly.md` | Frame reading, the convention, recursive fib in NASM, and two deliberate breakages |
| `assignments/QUIZ 3 Week 3 Monday.md` | Ten minutes on Week 2. **Unmarked — key in the paper** |
| `lab/LAB 3 Walking the Stack in GDB.md` | Read a live frame, watch it build, then overwrite a return address |
| `resources/Reading Guide Week 3.md` | CS:APP §3.7 and §3.10.3–4, plus the actual ABI document |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**`ret` jumps to whatever eight bytes are at `rsp`. Nothing checks them.**

In Lab 3 you will write `0xdeadbeef` over a return address in GDB and watch the program jump there — `SIGSEGV at 0x00000000deadbeef`, with no complaint from the hardware, the compiler or the runtime. Then you will point it at `main` instead, and the program will simply re-enter `main`, which the source says is impossible.

**Everything the ABI does is convention on top of that.** The convention is what makes separately compiled code interoperate; its absence at the hardware level is what makes stack smashing work. **Both facts come from the same sentence.**

---

### Assessment Reminder

**Labs and quizzes carry no weight**; the four weighted components already total 100%. Both remain required.

**Quiz 3 is Monday**, covering Week 2, with the key in the paper.

**PS 3 is the hardest assignment so far.** Q3 asks for working recursive assembly and then asks you to break it two ways. **Report what actually happens, including when the broken version still works** — one of the two breakages produces correct output on this machine, and saying so is worth full marks. Saying it crashed when it did not is not.

---

### Connections

**Back:** **Week 2** gave you the instructions; this week gives them a purpose. The `push rbx` in `fib` is L11's rule and L08's registers meeting. **Week 1's `INT_MIN`** shows up once more in PS 3's testing.

**Forward:** **Week 9 is this week plus an attacker.** Lab 3 Part 5 is the mechanism; Week 9 supplies the input that triggers it and the defences — canaries, ASLR, NX — that make it hard. **Week 4's cache** is where `rsp`-relative locality starts to matter. Week 5's pipeline has to predict where `ret` goes, which is why there is a dedicated return-address predictor.

**Sideways:** **PROG 201 is writing `fork`, `exec` and signal handlers this term.** A signal handler runs on your stack, which is why the red zone is disabled in kernel code and why async-signal-safety is a real constraint rather than a stylistic one.

---

*CS 201 · Week 3 · © CSE Department*
