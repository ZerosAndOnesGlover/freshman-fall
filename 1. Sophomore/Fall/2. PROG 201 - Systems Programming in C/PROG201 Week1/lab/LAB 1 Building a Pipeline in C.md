# PROG 201 · Lab 1
## Building a Pipeline in C — `ls | grep | wc` With No Shell
### Covers Week 1 · sat **Monday of Week 2**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 1 and is sat in Week 2.** The lab is on Monday and this course's lectures
> are Tuesday to Thursday, so a lab can never be sat in the week it covers — Lab *N* is sat on the
> Monday of Week *N+1*. **There was no lab session in Week 1**; Lab 0 was sat on the Friday that
> closed Week 0. Every lab file states its own week; the file is authoritative.
>
> **Unmarked.** The TA checks your work off in the session.

**What you are building:** the four lines of C that are underneath every `|` you have ever typed.

By the end you will have a program that runs `ls -1 /etc : grep host : wc -l` and produces byte-for-byte what the shell produces for `ls -1 /etc | grep host | wc -l` — with `pipe`, `fork`, `dup2`, `close`, `execvp` and `waitpid` written out, and no shell anywhere.

**The hard part is not the pipes. It is the closes.** Half this room will write a pipeline that hangs, and the process that hangs will not be the one with the bug.

---

## 0. Setup (5 minutes)

```bash
cd ~/prog201/lab1
make                      # builds ./pipeline from the skeleton
./pipeline echo hello : wc -l
```

The skeleton forks and execs both stages and connects nothing, so `echo` prints to your terminal and `wc` reads from your keyboard. **Press Ctrl-D** to give it the EOF it is waiting for. That is the baseline.

`./compare.sh` is your test harness: it runs eight pipelines through your program and through the shell and reports any difference in stdout or exit status. **Run it after every TODO.** At the end it should print `all checks passed`.

---

## 1. Part A — Two Stages (30 min)

Do TODOs 1–4 for the two-stage case only. The shape, for stage *s*:

```
        pipe(fd)
           │
  fork ────┼──────────────► child:  dup2 the ends it needs
           │                        close EVERYTHING else
           │                        execvp
           ▼
      parent: close the end it gave away,
              keep the other for the next stage
```

**Target:**

```bash
$ ./pipeline ls -1 /etc : wc -l
253
$ ls -1 /etc | wc -l
253
```

**Q1.** Before you write a line: `wc` must read from the pipe. It does not know a pipe exists — it reads descriptor 0. Which single call makes descriptor 0 mean "the pipe", and in **which process** must it run: the parent, or the child, and before or after `fork`? Answer in one sentence, then implement it.

**Q2.** Your first version will very likely hang. When it does — **do not add prints.** In another terminal:

```bash
ps -o pid,stat,wchan:20,comm -C wc
```

Report the `WCHAN` you see. Then explain, using L06 §3, which process is holding the descriptor that is preventing EOF. *(The reference bug produces `anon_pipe_read`.)*

---

## 2. Part B — N Stages (25 min)

Generalise the loop to any number of stages. The invariant that makes this easy is the one variable the skeleton already declares:

> **`in` is the descriptor the next stage should read from.** It starts as `STDIN_FILENO`; each
> iteration gives the child the current `in`, then replaces `in` with the read end of the pipe it
> just created.

**Target:**

```bash
$ ./compare.sh
  ok      one stage
  ok      two stages
  ok      three stages
  ok      no matches
  ok      big input
  ok      early exit
  ok      exit status
  ok      command not found
  all checks passed
```

**Q3.** The `early exit` check runs `ls -1 /usr/bin : head -3`. `head` exits after three lines while `ls` is still writing — on this machine `ls -1 /usr/bin` produces 2,073 of them. **What happens to `ls`?** Name the signal, say who sends it, and say why the shell does not consider this an error. *(W0 L03 §8 and L06 §3.)*

**Q4.** The `exit status` check runs `true : false` and expects exit status 1. Your program forked two children; a shell reports the status of the **last** stage only. Write down what `waitpid` gives you for each, and what you do with the first one's status. *(Then check: does your loop still reap it? A stage you do not reap is W0 L02's zombie.)*

---

## 3. Part C — Break It Deliberately (20 min)

Three one-line changes. Predict, run, explain. **Restore each before the next.**

| Change | Predict |
|---|---|
| **(a)** Delete the parent's `close(fd[1])` | Which stage hangs, and what does `wchan` say? |
| **(b)** Delete the child's `close(fd[0])` in a *middle* stage | Does it hang? Why is this different from (a)? |
| **(c)** In the child, `dup2(fd[1], STDOUT_FILENO)` but do **not** `close(fd[1])` | Does it hang? Count the write-end descriptors open in each process |

**Q5.** For each of (a), (b), (c): at the moment the reader called `read`, how many descriptors were open on **each end** of the pipe, and in how many processes? A table of three rows is the answer.

**Two of the three do not hang.** Say why not — and be precise, because "I closed enough of them" is not an explanation. The rule is about *which end* the extra descriptor is on and *which process* is holding it.

> **This is the part of the lab that transfers.** The rule — *EOF arrives when the last write-end
> descriptor anywhere is closed* — is one sentence, and the reason a pipeline hangs is always a
> descriptor in a process you were not thinking about. In Week 6's shell you will have five
> processes and eight descriptors, and the debugging technique is exactly the one you use here.

---

## 4. Part D — Measure It (15 min)

```bash
strace -f -c -e trace=pipe2,clone,dup2,close,execve,wait4 ./pipeline ls -1 /etc : grep host : wc -l
```

**Q6.** Report the call counts. How many `dup2` calls did *you* make, and how many does `bash` make for the same pipeline? *(`strace -f -e trace=dup2 bash -c 'ls -1 /etc | grep host | wc -l'`.)* If the numbers differ, that is interesting rather than wrong — say what the extra ones are for.

**Q7.** Time your pipeline against the shell's on a large input:

```bash
time ./pipeline ls -1 /usr/bin : wc -l
time bash -c 'ls -1 /usr/bin | wc -l'
```

They should be within noise of each other. **Explain why** — what work is the shell doing that your 90 lines are not, and why does it not show up in the timing?

---

## 5. Checkoff

Show the TA:

- [ ] `./compare.sh` printing **all checks passed**.
- [ ] The hang from Part C(a), diagnosed live with `ps -o wchan`, and fixed while they watch.
- [ ] Your written answers to **Q2, Q3 and Q5** — three or four sentences each.

**Take with you:** this program is the core of **Project 1**. Week 6 adds a parser in front of it, `<`/`>` redirection alongside it, and process groups and job control around it. The pipe wiring does not change.

---

*PROG 201 · Week 1 · Lab 1 · © CSE Department*
