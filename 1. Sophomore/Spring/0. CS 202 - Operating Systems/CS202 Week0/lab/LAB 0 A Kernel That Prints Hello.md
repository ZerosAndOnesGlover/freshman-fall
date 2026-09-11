# CS 202 · Lab 0
## A Kernel That Prints Hello
### Week 0 · sat **Friday of Week 0**, 10:00–11:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 0** and is sat on the **Friday that closes Week 0**, after all three of
> this week's lectures. From Lab 1 onwards this course's labs are on **Tuesdays, 15:00–16:50, and
> cover the previous week** — Lab *N* is sat on the Tuesday of Week *N+1*. There is **no lab in
> Week 1**.
>
> **10:00 is not the usual time**, and it happens once. Every Year 2 course holds its Week 0 lab on
> this Friday, and the morning is the one window free for every Spring Year 2 student.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence, which is the only enforcement there is and the only one needed.

**What you are building:** a kernel. Not a program that runs on one — the thing underneath. It will be about forty lines of C and twenty of assembly, it will run with no operating system beneath it, and it will print *Hello* by talking to a serial port directly.

**And then you will run the exact same instruction from a normal program and watch it get killed.** The difference between those two outcomes is this week's entire subject. By the end of the session you will also have built and booted **xv6**, the kernel this course extends until May, and watched it kill a program for the same reason.

---

## 0. Before You Start — Where You Work (10 minutes)

BH 210 runs **Ubuntu 24.04, GCC 13.3.0, QEMU 8.2.2**. On your own machine, check:

```bash
gcc -m32 -ffreestanding -nostdlib -c -x c /dev/null -o /dev/null && echo "gcc -m32 ok"
qemu-system-i386 --version | head -1
strace -V | head -1
```

**If `gcc -m32` fails on your own machine**, you are missing 32-bit compiler support (`sudo apt install gcc-multilib`). In BH 210 it works.

**Where you work.** Not your home directory — your coursework for this course goes in the Academic
Registry, alongside its answer sheets, at
`5. Academic Registry/4. Submissions/Year2 Sophomore/Spring/0. CS 202/`. Name that path once, in
`~/.bashrc` (the registry's [[4. Submissions/README|README]] has the block for every course):

```bash
export ACADEMICS=~/"Documents/1. Academics/0. Computer Science and Engineering (B.Sc)"
export CS202="$ACADEMICS/5. Academic Registry/4. Submissions/Year2 Sophomore/Spring/0. CS 202"
```

Create the directory and make it a repository of its own — it is kept out of the vault's git repo deliberately, so you commit CS 202 from inside `$CS202`:

```bash
mkdir -p "$CS202"
cd "$CS202"
git init
```

Now get this lab's files. The skeletons ship with the course material:

```bash
W0="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week0"
mkdir -p "$CS202/week0/lab0"
cd "$CS202/week0/lab0"
cp "$W0/lab/"{Makefile,boot.S,kernel.c,link.ld,int13.c} .
cp "$W0/resources/privfault.c" .
```

**Quote every `"$CS202"`.** The path contains spaces; unquoted, it splits into several arguments.

---

## 1. Part A — What a Program Asks For (20 min)

Write the smallest possible C program:

```c
#include <stdio.h>
int main(void) { printf("hello\n"); return 0; }
```

Build it twice, once dynamically and once statically:

```bash
gcc -O2 -o hello_dyn hello.c
gcc -O2 -static -o hello_static hello.c
strace ./hello_static
```

`strace` prints one line per system call: its name, its arguments, and what it returned. **Find the line that actually printed `hello`.** Everything above it is the C runtime setting up a process.

**Q1.** Count the system calls each binary makes, including the `execve`:

```bash
strace -o trace.txt ./hello_static > /dev/null; grep -vc '^+++' trace.txt
strace -o trace.txt ./hello_dyn    > /dev/null; grep -vc '^+++' trace.txt
```

The dynamic one makes about twice as many. **Name three system calls it makes that the static one does not, and say what they are for.** *(Hint: what file does it have to find and load before `main` can call `printf`?)*

**Q2.** Now send the static binary's output somewhere different, and compare:

```bash
strace -o a.txt ./hello_static | cat
strace -o b.txt ./hello_static > /dev/null
diff a.txt b.txt
```

**Ignoring addresses and PIDs, one call is in one trace and not the other.** Which, and why does glibc make it in one case only? *(PROG 201's L01 §6 explains what stdio needs to know about its output before it can decide how to buffer.)*

**Q3.** `strace -c ls /`. Which system call does `ls` make most often? Explain why, from what `ls` has to do.

---

## 2. Part B — What Ring 3 May Not Do (15 min)

```bash
gcc -O2 -Wall -Wextra -o privfault privfault.c
```

**Do not run it yet.** `privfault.c` executes nine instructions, one per child process, and reports whether each ran or killed the child. Read the table in its source and **write your prediction for each of the nine** — ran, or killed, and by which signal.

Now run it.

**Q4.** Which of your predictions were wrong? For each one, say which of L02 §4's three kinds of rule was involved. **If `sgdt` ran, report the address it returned, and run `grep -c -w umip /proc/cpuinfo`.** Explain in two sentences why `CONFIG_X86_UMIP=y` in `/boot/config-$(uname -r)` does not tell you whether `sgdt` will fault.

---

## 3. Part C — A Kernel of Your Own (35 min)

`kernel.c`, `boot.S` and `link.ld` together are a complete, bootable kernel. Build it and boot it:

```bash
make
make run
```

**It will print nothing and hang.** Press **Ctrl-C** to stop QEMU. The kernel booted — QEMU found the Multiboot header, loaded the ELF at 1 MB, and jumped to `_start` in ring 0 — but `kmain` does nothing yet, and when it returns, `boot.S` halts the CPU forever.

Read `boot.S` once, top to bottom. It is thirty lines. **Then do `kernel.c`'s five TODOs in order, running `make run` after each.**

| TODO | What | Test |
|---|---|---|
| 1 | `serial_putc`: one character out of the serial port, using `outb` | nothing visible yet |
| 2 | `serial_puts`: a whole string | nothing visible yet |
| 3 | print `Hello from ring 0` | **it appears in your terminal** |
| 4 | print `CPL = ` and the digit | `CPL = 0` |
| 5 | power off through `DEBUG_EXIT` | `make run` returns by itself |

**The rules of the environment**, because nothing will tell you when you break them:

- **There is no libc.** No `printf`, no `strlen`, no `<stdio.h>`. If you include a header, it had better be one you wrote.
- **There is no protection.** A wild pointer writes wherever it points — including over your own kernel. There is no `SIGSEGV` to catch it, because there is nobody above you to send one.
- **There are no interrupts.** `boot.S` never enables them. Nothing will take the CPU away from you, and nothing will give it back if you loop forever.

**Q5.** After TODO 5, `make run` prints `QEMU exited with status 1`. You wrote 0 to the port. **Where did the 1 come from?** *(The comment at the top of the `Makefile` says.)* Why might QEMU's designers have made it impossible for a guest to produce an exit status of 0?

**Q6.** Your kernel printed `CPL = 0`. In Part B, `privfault` printed `CS = 0x33, so CPL = 3`. **Both programs executed the same `outb` instruction to the same port, `0x3f8`.** In one sentence each: what did the CPU do with it in your kernel, and what did the CPU do with it in `privfault`? Then say, precisely, which process or program *decided* that `privfault` would run in ring 3.

**Stretch.** Write your message into the VGA text buffer at `0xB8000` as well: each cell is 16 bits, the low byte the character and the high byte the colour (`0x0F` is white on black). To see it, boot with a display: `qemu-system-i386 -kernel hello.elf -device isa-debug-exit,iobase=0xf4,iosize=0x04` — and remove TODO 5's power-off first, or the window will close before you can read it.

---

## 4. Part D — xv6 (25 min)

This is the kernel you will extend in both projects. **Build it cleanly today**, because Week 7 assumes it works.

```bash
cd "$CS202"
git clone https://github.com/mit-pdos/xv6-public xv6
cd xv6
git checkout eeb7b415dbcb12cc362d0783e41c3d1f44066b17
```

**xv6 does not build with GCC 13 as it is.** Its `Makefile` passes `-Werror`, and GCC 13 raises two warnings — `array-bounds` in `mp.c` and `infinite-recursion` in `sh.c` — that older compilers did not. Keep `-Werror` for everything else and demote those two:

```bash
sed -i 's/-m32 -Werror/-m32 -Werror -Wno-error=array-bounds -Wno-error=infinite-recursion/' Makefile
git diff --stat          # 1 file changed, 1 insertion, 1 deletion — nothing else
make qemu-nox
```

You should see, after some linker warnings you can ignore:

```
xv6...
cpu0: starting 0
sb: size 1000 nblocks 941 ninodes 200 nlog 30 logstart 2 inodestart 32 bmap start 58
init: starting sh
$
```

**That `$` is a shell running in ring 3 on a kernel you just compiled.** Try `ls`, `echo hi`, `cat README`. **To leave QEMU, press Ctrl-A, then X.**

**Q7.** `ls` prints three numbers per file. The last line is `console 3 19 0`. What are the three numbers, and what is type 3? *(Read `ls.c` and `stat.h` — they are short.)* Then count the system calls in `syscall.h`. **How many does xv6 have, and which PROG 201 system call that you used every week is missing?**

**Now add a program that misbehaves.** You copied `int13.c` in Part 0. Put it in the xv6 directory and add it to the list of user programs:

```bash
cp ../week0/lab0/int13.c .
sed -i 's/^\t_zombie\\$/\t_zombie\\\n\t_int13\\/' Makefile
grep -n _int13 Makefile          # one line, inside UPROGS
make qemu-nox
```

At the xv6 prompt, run `int13`, then `int13 cli`.

**Q8.** Both runs are killed, and xv6 prints a line for each. **Neither line was printed by `int13`.** Which function in which file printed them, and in which ring was it running? Then **decode the error code** for the `int $13` run: it is not 0, and L02 §7 says what it means. Write it in hex and split it into its fields.

---

## 5. Checkoff

Show the TA:

- [ ] Your kernel printing `Hello from ring 0` and `CPL = 0`, and `make run` returning by itself.
- [ ] `privfault` run, with your written predictions beside its output.
- [ ] xv6 booted to a `$` prompt, and `int13` killed by trap 13.
- [ ] Your written answers to **Q2, Q6 and Q8** — three or four sentences each. These are the three that are actually about this week's lectures.

**Take with you:** the kernel from Part C comes back in **Week 10**, where you write the hypervisor that boots it — the program that plays the part QEMU played today. **Keep `$CS202/week0/lab0` intact.** And the xv6 in `$CS202/xv6` is where Project 1 starts in Week 7: commit it now, patch and all, so you can always get back to a clean build.

```bash
cd "$CS202" && git add week0 && git commit -m "Lab 0: a kernel that prints Hello"
```

*(xv6 is its own git repository, cloned inside yours. Commit your changes to it from inside `$CS202/xv6` when you start changing it in Week 7.)*

---

*CS 202 · Week 0 · Lab 0 · © CSE Department*
