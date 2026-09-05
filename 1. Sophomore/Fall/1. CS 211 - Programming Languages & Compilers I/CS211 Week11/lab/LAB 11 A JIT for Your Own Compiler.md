# CS 211 · Lab 11
## A JIT for Your Own Compiler

**Friday of Week 11 · 14:00–15:50 · BH 220 · covers Week 11**
**Unmarked and mandatory.** The TA checks you off in the session.

> ## Project 1 is due today at 17:00.
>
> **This lab ends at 15:50.** If your project is not submitted, submit what you have *before* the
> session and use the two hours here on the report — it is 25 marks and it is the part people
> leave until it is too late. Tell the TA; nobody will mind.

---

## Setup

```bash
cd "CS211 Week11/lab"
python3 cyanc.py gcd.cy
llc --version | head -3
```

---

## Part A — The Whole Thing, Once (25 min)

**Q1.** Run every phase and record the nine lines:

```bash
python3 cyanc.py gcd.cy
```

Then look at any one phase in full:

```bash
python3 cyanc.py gcd.cy --emit=tac
python3 cyanc.py gcd.cy --emit=cfg
python3 cyanc.py gcd.cy --emit=llvm
```

**Q2.** Make it run:

```bash
python3 cyanc.py gcd.cy 1071 462 --run
python3 cyanc.py gcd.cy 270 192 --run
```

**Report the exit codes.** That is machine code your compiler produced, running on this processor.

**Q3.** Now a real executable:

```bash
python3 cyanc.py gcd.cy 1071 462 -o /tmp/gcd
file /tmp/gcd
/tmp/gcd ; echo "exit $?"
```

**Q4.** Check it against Week 6's interpreter, which is an independent implementation:

```bash
python3 runtime.py gcd.cy gcd 1071 462 --gc=none
python3 cyanc.py gcd.cy --fn=gcd 1071 462 --run
```

Do this for at least **six** calls across `gcd.cy`, `cls.cy` and `sc.cy`. *(Careful: `sc.cy`'s function is called `f` and takes two booleans — pass 0 or 1.)*

**Any disagreement is a compiler bug.** If you find one, tell the TA — but check your function names first.

---

## Part B — What LLVM Does to Our IR (30 min)

**Q5.** Look at the IR we emit:

```bash
python3 cyanc.py gcd.cy --emit=llvm > /tmp/gcd.ll
grep -c alloca /tmp/gcd.ll
grep -cE 'load|store' /tmp/gcd.ll
```

**It is terrible on purpose.** Say why, in one sentence.

**Q6.** Now let LLVM fix it:

```bash
opt -passes=mem2reg -S /tmp/gcd.ll -o /tmp/gcd_m.ll
grep -c alloca /tmp/gcd_m.ll ; grep -c phi /tmp/gcd_m.ll
diff <(grep -c . /tmp/gcd.ll) <(grep -c . /tmp/gcd_m.ll)
```

- Report allocas and φ-functions before and after.
- **Open `/tmp/gcd_m.ll` and find the φ.** Which variable is it for, and which two blocks feed it? Check against `--emit=cfg`.
- **Name the Week 4 algorithm you are looking at the output of.**

**Q7.** The full pipeline:

```bash
opt -O2 -S /tmp/gcd.ll -o /tmp/gcd_o.ll
```

Do the same for `cls.cy` and `fold.cy`. Build this table:

| program | our TAC (opt.py) | our IR | `mem2reg` | `-O2` |
|---|---|---|---|---|

**`fold` should end at one instruction.** Look at it and say what happened.

**Q8.** Compare the two optimisers:

```bash
python3 cyanc.py cls.cy | grep "our optimiser"
```

**Ours removes 0% from `cls`; `-O2` removes 82%.** Before you conclude anything, state the reason a raw percentage comparison is unfair here. **Then say why `cls` survives that objection anyway.**

---

## Part C — One IR, Many Machines (30 min)

**Q9.** Our compiler has no back ends. Watch it target eight architectures:

```bash
for t in x86-64 aarch64 riscv64 wasm32 ppc64le mips64 sparcv9 avr; do
  printf "%-10s " $t
  llc -march=$t -filetype=asm -o /tmp/o.s /tmp/gcd_o.ll 2>/dev/null \
    && grep -cE '^\s+[a-z]' /tmp/o.s || echo unsupported
done
```

Record all eight. **The range is about fifteenfold.**

**Q10.** Now find out *why*, by reading the assembly:

```bash
llc -march=aarch64 -o - /tmp/gcd_o.ll | grep -E "sdiv|msub"
llc -march=riscv64 -o - /tmp/gcd_o.ll | grep -E "call"
llc -march=wasm32  -o - /tmp/gcd_o.ll | head -20
```

- **aarch64** uses `sdiv` then `msub`. Why two instructions for one `%`?
- **riscv64** emits `call __moddi3`. **What does that tell you about the RISC-V base ISA?**
- **wasm32** has `block` and `br_if` rather than arbitrary branches. What did the back end have to reconstruct?

**Q11.** Open the AVR output:

```bash
llc -march=avr -o - /tmp/gcd_o.ll | head -40
```

**124 instructions.** Say what an 8-bit machine has to do with an `i64`.

**Q12.** *(Discussion.)* We wrote a front end for a language we invented and got eight code generators.

- State LLVM's *m* × *n* → *m* + *n* argument.
- **Name a cost of it** that is not performance.
- Your language must run in a browser *and* on a microcontroller. Look at your Q9 table. **What do you do?**

---

## Part D — JIT (15 min)

**Q13.** `lli` compiles into memory and jumps to it:

```bash
time python3 cyanc.py gcd.cy 1071 462 --run
time /tmp/gcd
```

The JIT takes tens of milliseconds; the binary takes about four.

**That comparison is meaningless. Say why**, then say what the JIT time actually consists of.

**Q14.** A JIT knows things an ahead-of-time compiler cannot. Name **four**, and for each say what it enables.

Then connect it to Week 9: `Hoist.java` terminated while interpreted and **hung once C2 compiled the loop**. Which of your four is that, and what does it say about testing?

---

## If You Finish Early

**Q15.** Add `--emit=asm` to `cyanc.py`, calling `llc` and printing the assembly for a chosen `-march`.

**Q16.** Write a Cyan program using arrays and watch `llvmgen.py` refuse it. **Read the message.** What would you need to build? *(This is PS 11 Part C.)*

**Q17.** Write a recursive Cyan function. `llvmgen.py` currently emits one function at a time — does it work? If not, fix it. *(This is PS 11 B2.)*

**Q18.** Run `opt -O2 -debug-pass-manager -S /tmp/gcd.ll 2>&1 | head -40` and count the passes. Find three whose names you recognise from Weeks 4 and 5.

---

## Before You Leave

Show the TA:

1. Your Q2 exit codes — 21 and 6.
2. Your Q4 agreement table, at least six calls.
3. Your Q6 answer: allocas and φs before and after, and the Week 4 algorithm named.
4. Your Q9 table of eight targets, and your Q10 explanation of the riscv64 `call`.

**And confirm Project 1 is submitted.**

---

*CS 211 · Week 11 · Lab 11 · © CSE Department*
