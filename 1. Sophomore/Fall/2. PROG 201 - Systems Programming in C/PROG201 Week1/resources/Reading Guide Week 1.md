# PROG 201 · Reading Guide · Week 1
## APUE Chapter 3, §5.4, and the man pages you will actually use

---

**Week 1 is one chapter**, and unlike Week 0 you should read all of it. APUE Chapter 3 is forty pages and it is the best forty pages written about Unix I/O.

| Chapter | Read? | Why |
|---|---|---|
| **3. File I/O** | **All of it** | This week, entire. §3.10 (`dup`) and §3.11 (`sync`) are L06 |
| **5.4 Buffering** | **Re-read** | You were sent here in Week 0. Now it explains L05 §2's table |
| 4. Files and Directories | Not yet | Week 7 |
| 14.6 `readv`/`writev` | **Read** | Six pages, and it is L06 §6 |
| 14.7 `readn`/`writen` | **Read** | Stevens' `write_all`, written out. Compare with yours |

---

## Chapter 3 — the questions to hold

**§3.3 `open`**

1. The `mode` argument is only consulted when the file is created. What is the resulting permission of a file created with `open(path, O_CREAT|O_WRONLY, 0666)` on your machine? **Predict from your `umask`, then check.**
2. `O_TRUNC` and `O_APPEND` are both about where writing starts. Say what each does in one sentence, and which shell operator corresponds to each.
3. Find `O_EXCL`. **Why can a lock file not be implemented correctly without it?** Write out the two-call version and name the window.

**§3.6 `lseek`**

4. Stevens shows a program that seeks past the end and writes. Run it, then run `du` and `ls -l` on the result. Explain the two numbers. *(L05 §4 measured 1.1 GB apparent against 4 KB allocated.)*
5. Which files can you *not* `lseek` on? Try it on a pipe and report the `errno`.

**§3.9 and §3.10 — `dup`, and the sharing question**

6. **Figure 3.7 and Figure 3.8 are the two diagrams this week is built on.** Draw both from memory, then check. One shows two descriptors sharing an open file description; the other shows two descriptions onto one inode. Which does `dup` produce? Which does a second `open`?
7. Stevens says the file offset is in the "file table entry". This course calls it the **open file description**, which is POSIX's name and the one the man pages use. Same thing. Notice the vocabulary difference now so that reading either does not confuse you later.

**§3.11 — `sync`, `fsync`, `fdatasync`**

8. What is the difference between `fsync` and `fdatasync`, and when does the difference cost you a disk seek? *(Week 7 returns to this with the journal.)*
9. `close()` does **not** imply `fsync()`. What guarantee do you actually have about your data when `close` returns 0?

**§3.12 — `fcntl`**

10. Write the correct three lines to add `O_NONBLOCK` to an existing descriptor. Then say what the *incorrect* one line breaks, and for whom. *(L06 §5.)*

---

## §5.4 — Buffering, again, and now it should land

11. `stdio` is a buffer over `read`/`write`. Given L05 §2's table — 1.25 µs per system call, flattening at one page — **what is `BUFSIZ` on your machine, and is it the right size?** (`getconf` will not tell you; grep `/usr/include/stdio.h`.)
12. When you call `setvbuf(stdout, NULL, _IONBF, 0)`, which row of that table are you choosing?

---

## The Man Pages for This Week

Read these four properly. They are short, and every one of them contains a paragraph that will save you an afternoon:

| Page | The paragraph |
|---|---|
| **`man 2 open`** | The `O_CLOEXEC` note, and the sentence about `mode` and `umask` |
| **`man 2 write`** | "The number of bytes written may be less than `count`" — and *why*, for pipes and sockets |
| **`man 7 pipe`** | `PIPE_BUF` and the atomicity guarantee. Also the capacity, and how to change it |
| **`man 2 dup`** | The `dup2(fd, fd)` special case, and what `dup3` adds |

**And one to skim so you know it exists:** `man 2 fcntl`. It is enormous, it does eleven unrelated things, and you will come back to it for record locks in Week 7 and for `F_SETPIPE_SZ` if Lab 1 leaves you curious.

---

## Where to Go Deeper

**TLPI** is the better book for this week's Linux specifics:

| TLPI | Topic |
|---|---|
| Ch. 4–5 | File I/O, and the "universality of I/O" argument stated properly |
| §5.4–5.5 | Atomicity and `O_APPEND` — the same experiment as L05 §5, with the kernel's side of it |
| Ch. 44 | Pipes and FIFOs. Week 2's reading, but Lab 1 will make you want it early |
| §63.5 | Non-blocking I/O in the context of what it is *for*, which is Week 5 |

---

## The Habit for This Week

**Predict, then measure, then explain the gap.**

Week 0's habit was going to look when the book and the machine disagree. This week's is narrower and harder: **write your prediction down before you run it.** Every question above that says "predict, then check" is testing whether your model of the three tables is right, and the only way to find out is to commit to an answer first. A prediction you did not write down is a prediction you will remember having got right.

---

*PROG 201 · Week 1 · Reading Guide · © CSE Department*
