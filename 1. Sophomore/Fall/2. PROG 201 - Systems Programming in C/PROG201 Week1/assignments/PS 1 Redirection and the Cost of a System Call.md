# PROG 201 · Problem Set 1
## Redirection, and the Cost of a System Call

---

**Released:** Week 1, Wednesday · **Due:** Week 2, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS1_{LastName}_{StudentID}.pdf`, and your code as `PS1_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **Q1 is a program**, and it is the largest single piece of code you have written for this course
> so far. Start it before Thursday. **Q3 and Q4 are measurements on your own machine** — state your
> `gcc --version`, `uname -r`, and whether you are on BH 215 or your own hardware.
>
> Everything compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.

---

### Q1: Implement Redirection (28 points)

Write `redirect.c`. It takes **one** command and any number of redirection operators, and runs it:

```
./redirect wc -l '<' /etc/services
./redirect ls -1 /etc '>' out.txt
./redirect ls -1 /etc '>>' out.txt
./redirect ls /nope '2>' err.txt
./redirect ls /nope '>' both.txt '2>&1'
```

*(The quotes are there so that your shell does not perform the redirection for you. Your program receives `<`, `>`, `>>`, `2>` and `2>&1` as ordinary argv strings, and must do the work itself.)*

**(a) [16]** Implement `<`, `>`, `>>` and `2>`. Requirements:

- Redirections may appear **anywhere** in the argument list, not only at the end, and must not be passed on to the exec'd program.
- `>` truncates; `>>` appends. **Use the flag, not an `lseek`** — and be able to say why (L05 §5).
- A failed `open` must report the filename and `strerror(errno)` and exit **1** without exec'ing.
- The exit status of your program is the exit status of the command, or **128 + signal** if it was killed.

**(b) [6]** Implement `2>&1`, and make it obey the ordering rule: `> f 2>&1` sends both streams to `f`, while `2>&1 > f` sends stdout to `f` and stderr to wherever stdout pointed *beforehand*. **Demonstrate both** with output, and explain the difference in terms of what `dup2` copies.

**(c) [6]** For your implementation, answer: which descriptors are open in the child at the moment `execvp` is called, and which of them are open because you meant them to be? List them. If any is open by accident, fix it and say what the fix was.

---

### Q2: The Three Tables (18 points)

**(a) [8]** Predict the exact contents of `out.txt` for each program, **before running any of them**, then run all four and report both columns. Explain every difference.

```c
/* A */ int a = open("out.txt", O_RDWR|O_CREAT|O_TRUNC, 0644);
        int b = dup(a);
        write(a, "1111", 4); write(b, "2222", 4);

/* B */ int a = open("out.txt", O_RDWR|O_CREAT|O_TRUNC, 0644);
        int b = open("out.txt", O_RDWR);
        write(a, "1111", 4); write(b, "2222", 4);

/* C */ int a = open("out.txt", O_RDWR|O_CREAT|O_TRUNC, 0644);
        write(a, "1111", 4);
        if (fork() == 0) { write(a, "2222", 4); _exit(0); }
        wait(0); write(a, "3333", 4);

/* D */ int a = open("out.txt", O_WRONLY|O_CREAT|O_TRUNC|O_APPEND, 0644);
        int b = open("out.txt", O_WRONLY|O_APPEND);
        write(a, "1111", 4); lseek(b, 0, SEEK_SET); write(b, "2222", 4);
```

**(b) [4]** Draw the three-table diagram for program **B** at the moment of the second `write`. Label every box and arrow.

**(c) [6]** In one paragraph: the file offset lives in the open file description rather than in the descriptor or the inode. Give one thing that would break if it lived in the descriptor, and one that would break if it lived in the inode.

---

### Q3: What a System Call Costs (20 points)

**(a) [10]** Reproduce L05 §2's measurement on your own machine. Copy a file of at least 64 MB with `read`/`write` and buffer sizes 1, 16, 256, 4096, 65536 and 1048576 bytes. Report time, throughput and system-call count for each.

**Derive your per-call cost** from the 1-byte row, and say whether the curve flattens where the notes say it does. If your machine disagrees, say by how much and offer a reason.

**(b) [5]** Repeat the 4096-byte run under `strace -c`. Report the ratio of time in system calls to wall-clock time, and reconcile it with (a).

**(c) [5]** Now copy the same file with `cat in > out` and with `cp in out`, and time both. `cp` beats a 4 KB loop on this machine. **Find out what it is doing differently** — `strace -c cp in out` will tell you in one line — and explain it in two sentences.

---

### Q4: Two System Calls Are Not One (20 points)

**(a) [10]** Reproduce L05 §5's append experiment: *N* processes, each **opening the file itself**, each writing 20,000 identical lines. Report the surviving line count for `lseek(SEEK_END)`+`write` and for `O_APPEND`, at *N* = 1, 2, 4 and 8.

Plot or tabulate lines-lost against *N*, and explain the shape. **Why is the loss zero at *N* = 1?**

**(b) [4]** Now change the experiment so the workers **inherit one descriptor from a parent** rather than each opening the file. Predict the result first. Explain it with the L04 §2 diagram.

**(c) [6]** Give two more examples from this week's material of a **check-then-act** or **seek-then-write** pair that the kernel offers to fuse into one call, name the flag or call that fuses it, and say what the race is in each case if you do not use it.

---

### Q5: A Descriptor Is a Capability (14 points)

**(a) [6]** A program running as root opens `/etc/shadow`, then execs `/usr/bin/less` to display something else entirely. `less` lets the user run a subshell. Explain precisely what the user can now read, and why no permission check stops them. Give the one-flag fix.

**(b) [4]** `fcntl(fd, F_SETFL, O_NONBLOCK)` on a descriptor inherited from your shell can break an unrelated program. Explain the mechanism and give the correct two-call form.

**(c) [4]** Descriptors are inherited across `fork` and survive `exec` unless marked. Argue in one paragraph whether the default should have been the other way round — closed unless explicitly kept — and say what would have had to change in Lab 1's pipeline if it had been.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Implement redirection | 28 |
| 2 | The three tables | 18 |
| 3 | What a system call costs | 20 |
| 4 | Two system calls are not one | 20 |
| 5 | A descriptor is a capability | 14 |
| | **Total** | **100** |

**Late work:** `COURSE POLICIES.md` applies. The lowest problem set of the term is dropped.

---

*PROG 201 · Week 1 · PS 1 · © CSE Department*
