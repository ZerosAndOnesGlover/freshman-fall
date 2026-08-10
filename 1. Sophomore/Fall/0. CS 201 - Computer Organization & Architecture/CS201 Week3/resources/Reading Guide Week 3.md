# CS 201 · Week 3 · Reading Guide
## CS:APP §3.7 — Procedures

---

**Set reading:** Bryant & O'Hallaron, **§3.7** in full, plus **§3.10.3–3.10.4** (buffer overflow and defences).
**Reference:** *System V Application Binary Interface, AMD64 Architecture Processor Supplement* — §3.2 is the calling convention, and it is the actual specification.

---

## Read §3.10.3 This Week, Not in Week 9

CS:APP puts buffer overflow at the end of Chapter 3, after the memory chapter has been forgotten. **Read it now**, while the frame layout is fresh. Week 9 assumes you have seen it once.

The connection this week makes explicit: **`ret` pops eight bytes and jumps to them, with no validation.** §3.10.3 is what happens when someone else chooses those eight bytes. Lab 3 Part 5 has you choose them yourself.

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **3.7.1** | The run-time stack | Grows down. `push`/`pop` semantics. This is L10 §2 |
| **3.7.2** | Control transfer | `call` and `ret` as push/jmp and pop/jmp. **The whole mechanism** |
| **3.7.3** | Data transfer | The six argument registers, and the stack beyond them |
| **3.7.4** | Local storage on the stack | Why some locals cannot live in registers — address-taken, arrays, too many |
| **3.7.5** | Local storage in registers | **The caller/callee-saved split.** Read twice |
| **3.7.6** | Recursive procedures | The book's example is factorial; ours is Fibonacci, which needs *two* saved values |
| **3.10.3** | Buffer overflow | Read now. Lab 3 Part 5 is this, done deliberately |
| **3.10.4** | Thwarting attacks | Canaries, ASLR, NX. **Where Week 9 starts** |

---

## Questions to Read Against

**On §3.7.1–3.7.2**

1. Write `call` and `ret` as explicit push/pop/jmp pairs. Which register does each modify implicitly?
2. `push` always moves `rsp` by 8, even for a 32-bit operand. Why is there no 4-byte push in x86-64?
3. The book says the return address is pushed by `call`. **Where exactly is it, relative to `rsp`, at the instant the callee's first instruction executes?**

**On §3.7.3–3.7.4**

4. Which arguments go in registers, and in what order? What happens to the seventh?
5. Give three distinct reasons a local variable must live on the stack rather than in a register.
6. Stack arguments are pushed in reverse and popped by the caller. Work out why *both* choices are needed for variadic functions.

**On §3.7.5 — the important one**

7. State the caller-saved and callee-saved sets from memory, then check.
8. **Why does the ABI have both classes rather than one?** Argue what would go wrong with an all-callee-saved convention, and with an all-caller-saved one.
9. In the book's recursive example, which register holds the value that must survive the recursive call, and why that one?

**On §3.10.3–3.10.4**

10. In a frame with a `char buf[16]` at `rbp-0x20`, how many bytes must be written to reach the return address? Draw it.
11. A stack canary sits between the locals and the saved registers. **Why there and not at the very top of the frame?**
12. ASLR randomises the stack base every run — you saw the addresses change between Lab 3 runs. What does that cost an attacker, and what does it *not* prevent?

> **Question 8 is the one worth real thought.** The answer is about who pays for what, and it explains
> why the split is where it is rather than at some other point in the register file.

---

## Reading Against the Machine

```bash
# 1. Watch a frame exist
gcc -O0 -g -o fibmain fibmain.c
gdb -q ./fibmain
  (gdb) break fib if n == 2
  (gdb) run
  (gdb) bt
  (gdb) info frame
  (gdb) x/6gx $rsp

# 2. Find the alignment padding that allocates nothing
#    Compile `void h(void){ g(); }` at -O1 and find the `sub rsp,0x8`.
#    h has no locals. What is it for?

# 3. Find the red zone
#    Compile a leaf function with three int locals at -O0.
#    Confirm there is no `sub rsp` and the locals are below it.
```

**Item 1 is the whole lab**, and doing it once before Tuesday makes the session twice as useful.

---

## Terminology You Should Own by Week 4

| | | |
|---|---|---|
| stack frame | frame pointer | `leave` |
| prologue / epilogue | spill | red zone |
| caller-saved / volatile | callee-saved / non-volatile | ABI |
| System V AMD64 | argument register | variadic |
| return address | stack alignment | leaf function |
| unwinding | `.eh_frame` | stack canary |
| guard page | stack overflow | tail call |

---

## If You Want More

**The System V AMD64 ABI document** is the specification everything here is quoting. §3.2.2 (the register usage table) and §3.2.3 (parameter passing) are four pages and completely readable. **Worth skimming once** so you know that "the ABI says" refers to a real document you could open.

**Agner Fog, *Calling Conventions*** — a comparison across compilers and platforms, including Windows x64. Useful the first time you have to make code work on both.

**`tail call optimisation`** is not in the syllabus and is worth an hour anyway. A call in tail position can reuse the caller's frame instead of building a new one, turning recursion into iteration and removing the depth limit from Q5 entirely. Compile a tail-recursive factorial at `-O2` and look for the `jmp` where you expected a `call`.

---

*CS 201 · Week 3 · Reading Guide*
