# CS 202 · Lab 12
## Demo Day

---

**Sat:** **Tuesday of the completion period, 15:00–16:50, BH 210** · **Covers Week 12** · **Unmarked, checked off by the TA**

> **This is the last session of the course, and it has two halves.**
>
> **Part A (45 min): the Week 12 measurements**, which are the evidence PS 12 Q5 asks you for.
> **Part B (65 min): Project 2 demos**, four minutes each, in the order the TA posts.
>
> **Bring:** a kernel that boots, or one that does not. **Both are demonstrable** — see Part B.
> **Project 2 and PS 12 are both due Friday at 17:00**, and this is your last chance to ask.

**Programs:** `lab/` in this week's folder — `sgdt.c`, `smash.c`, `aslr.c`, `seccost.c`, `jailed.c`, `timing.c`.

```bash
cd "$REGISTRY/CS 202/labs/week12"
for f in sgdt smash aslr seccost jailed timing; do gcc -O2 -Wall -Wextra -o $f $f.c; done
```

---

# Part A — What This Machine Actually Enforces

## A1 · The claim from Week 0, twelve weeks later (15 min)

**Week 0's L02 claimed that this kernel is built with UMIP, that the CPU does not have it, and that an ordinary program can therefore read a kernel address.** You have spent a term learning what protections exist. **Test it again.**

```bash
grep -c CONFIG_X86_UMIP=y /boot/config-$(uname -r)
./sgdt
grep -m1 ' T ' /proc/kallsyms
```

**Q1.** What did `sgdt` print, and **is the address it printed a kernel address**? How can you tell without any privilege?

**Q2.** `/proc/kallsyms` shows every symbol at address zero, because `kernel.kptr_restrict` is 1. **One mechanism hides kernel addresses and another hands one over.** Is either broken? **Say precisely where the gap is.**

**Q3.** Look at the vulnerabilities directory and **find the one line that does not begin with `Mitigation:` or `Not affected`:**

```bash
grep . /sys/devices/system/cpu/vulnerabilities/* | sed 's|.*/||'
```

**Which flaw is it, and what does "Vulnerable" mean here — that the kernel forgot, or something else?**

---

## A2 · Three ways to catch one bug (10 min)

`smash.c` copies its argument into a 16-byte buffer with `strcpy`. **Build it three ways and run each with 40 bytes:**

```bash
gcc -O1 -o smash_fortify                        smash.c    # Ubuntu's default
gcc -O1 -U_FORTIFY_SOURCE -fstack-protector-strong -o smash_canary   smash.c
gcc -O1 -U_FORTIFY_SOURCE -fno-stack-protector     -o smash_plain    smash.c
for b in fortify canary plain; do ./smash_$b "$(python3 -c 'print("A"*40)')"; echo "  -> $?"; done
```

**Q4.** **Record the exact message and exit status of each.** Two of them abort; **the messages are different, and the difference is the question.** Which mechanism produced each, and **at what moment in the function's execution did each one act**?

**Q5.** Now run all three with **24** bytes instead of 40. **One build survives that did not survive 40, and one dies that you might have expected to survive.** Explain — `-fstack-protector-strong` does something to the frame besides adding a word.

**Q6.** `readelf -sW smash_fortify | grep chk` and the same for the others. **What does the fortified build call that the others do not?**

---

## A3 · Randomisation, and what it is worth (10 min)

```bash
for i in $(seq 200); do ./aslr; done > runs.txt     # code, globals, heap, mmap, stack
awk '{print $1}' runs.txt | sort -u | wc -l
awk '{print $5}' runs.txt | sort -u | wc -l
setarch -R ./aslr; setarch -R ./aslr
```

**Q7.** How many distinct values did each of the five take in 200 runs?

**Q8.** **Subtract the first column from the second in every run.** What do you find, and **what does one leaked code address therefore tell an attacker?**

**Q9.** The stack's addresses span far less than the others. **Estimate the number of distinct stack pages** from your 200 samples, and say what that means for an attacker who can make the program crash and retry a few million times. **Then say why `setarch -R` exists at all.**

---

## A4 · What a filter costs, and what it cannot see (10 min)

```bash
taskset -c 2 ./seccost 0 0        # the control: no filter, measured twice
taskset -c 2 ./seccost 10 1       # one filter of 15 instructions
taskset -c 2 ./seccost 200 1      # one filter of 205 instructions
taskset -c 2 ./seccost 10 5       # five filters, stacked
./jailed; echo "exit $?"
```

**Q10.** **The control must come out at about zero.** What did yours give, and **why is running it first non-negotiable**? *(L38 §4: the first version of this program reported that seccomp made system calls faster.)*

**Q11.** Tabulate the four filter costs. **What does the cost not depend on?** Give the explanation, and say what it implies about how carefully you should ration rules.

**Q12.** `jailed` dies with **exit 159**. **Decompose that number**, name the signal, and say why the kernel uses this signal rather than `SIGKILL`.

---

## A5 · A channel nobody declared (optional, if time) (10 min)

```bash
taskset -c 2 ./timing hot        # secret in cache, early-exit compare
taskset -c 2 ./timing const      # constant-time compare
```

**Q13.** In `hot`, the per-prefix ladder should rise monotonically. **Quote the per-byte step and the noise floor.** Is the signal real?

**Q14.** **The attack recovers the first byte and then usually stalls.** Look at the ladder: **the first step is much larger than the rest.** Explain why, and say what that means for the claim "early-exit comparison leaks the secret".

**Q15.** Compare the `const` ladder. **What has changed, and what has it cost in run time?**

---

# Part B — Project 2 Demos

**Four minutes each. The TA keeps time.** This is a checkpoint, not a viva — **it is not marked**, and nothing you say here changes your project mark.

**Show, in this order:**

1. **It boots.** `make qemu-nox`, to a shell prompt.
2. **One measurement from Part D of your report** — the free-page count across a lazy `sbrk`, or the maximal file size, or a symlink followed and refused. **The number, on screen.**
3. **One thing that went wrong**, and how you found it. **Thirty seconds.**

> ### If your kernel does not boot, come anyway and demo that.
>
> **This is the single most useful four minutes available to you before Friday.** A panic at
> `init` with `eip 0x1010101`, a `symlink()` that returns 56790, a `usertests` that hangs in
> `sbrk` — **the TA has seen all three this term**, and two of them are in the handout's warnings
> because the reference implementation hit them.
>
> "It does not work" is a demo. **"I did not come because it does not work" is a lost mark on
> Friday.**

**Q16.** Before you leave, write down the **one** thing you will fix first, and the command that will tell you it is fixed.

---

## Check-Off

**The TA records attendance and initials your book.** Show:

- **Q1, Q3, Q4, Q10 and Q12 answered** — five lines is enough;
- **your ASLR run** (`runs.txt` with 200 lines);
- **your project demo**, working or not.

---

## Where to Look

| For | Read |
|---|---|
| the UMIP claim, first stated | **Week 0, L02** |
| threat models, the TCB, canaries, ASLR, timing | **L37** |
| seccomp's cost, `SIGSYS`, rlimits against cgroups | **L38** |
| the whole-term price list, and Habit 1 | **L39 §2–§3** |
| the two traps in Project 2 | **PROJECT 2, "Two Warnings"** |

---

*CS 202 · Week 12 · Lab 12 · © CSE Department*
