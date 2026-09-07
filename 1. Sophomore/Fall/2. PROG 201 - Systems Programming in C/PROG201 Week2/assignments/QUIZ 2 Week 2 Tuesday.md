# PROG 201 · Quiz 2
## Administered: Tuesday, Week 2 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 1** — file descriptors, the three tables, `read`/`write`, the cost of a system call, `dup2` and redirection.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room — the point
> is to find out what has not landed while there is still a term left to fix it.
>
> Do not look at the key first. It costs you the only thing the exercise is for.

---

**Q1.** A process has 0, 1 and 2 open and nothing else. It calls `open("a")`, `open("b")`, `close(3)`, `open("c")`. What descriptor does the third `open` return, and what rule decides it?

&nbsp;

&nbsp;

---

**Q2.** There are three tables between a descriptor and a file's bytes. Name them, and say which one holds the **file offset**.

&nbsp;

&nbsp;

---

**Q3.** Two descriptors, both onto `log.txt`. In case (a) the second came from `dup`; in case (b) from a second `open`. Write `AAAA` through the first and `BBBB` through the second. What is in the file in each case, and how many bytes long is it?

&nbsp;

&nbsp;

&nbsp;

---

**Q4.** Copying 64 MiB one byte at a time took 167.964 s; one page at a time took 0.222 s. Give the approximate cost of one system call that this implies, and say what happens to the curve above 4,096 bytes.

&nbsp;

&nbsp;

---

**Q5.** Four processes append to one log file. Version (a) uses `lseek(fd, 0, SEEK_END)` then `write`. Version (b) opens with `O_APPEND` and writes. One of them lost 95% of its lines. Which, and why?

&nbsp;

&nbsp;

---

**Q6.** `cmd > f 2>&1` and `cmd 2>&1 > f` differ. Say what each does, and explain the difference in terms of what `dup2` copies.

&nbsp;

&nbsp;

---

**Q7.** A pipeline hangs: `wc` never prints. Every process has exec'd correctly. Give the most likely cause in one sentence, and name the command that would confirm it.

&nbsp;

&nbsp;

---
---

# Answer Key

*Mark your own. Be honest — nobody else will see this.*

---

**Q1.** **3.** `open("a")` got 3 and `open("b")` got 4; `close(3)` freed 3; the **lowest-free-descriptor rule** says the kernel always allocates the smallest available number, so `open("c")` gets 3, not 5. *(L04 §1.)*

---

**Q2.** The per-process **descriptor table** → the **open file description** (Stevens calls it the file table entry) → the **inode** (the v-node). **The offset is in the middle one**, the open file description — not in the descriptor and not in the file. *(L04 §2. This is the single most examinable sentence of Week 1.)*

---

**Q3.** **(a) `dup`:** one open file description, one shared offset. The file is `AAAABBBB`, **8 bytes**. **(b) two `open`s:** two descriptions, two independent offsets, both starting at 0. The second write lands on top of the first: the file is `BBBB`, **4 bytes** — and **half the data is gone with no error reported**. *(L04 §3, measured: `11112222` against `2222`.)*

---

**Q4.** A byte at a time is one `read` and one `write` per byte, so 64 MiB is **134,217,728 calls**: 167.964 s / 134 M ≈ **1.25 µs per system call**. Above 4,096 bytes **the curve is flat**: one page is where the per-call cost stops dominating, which is exactly what `stdio`'s buffer is buying you. *(L05 §2.)*

---

**Q5.** **(a) lost the data.** `lseek` then `write` is **two system calls**, and another process can append between them, so both write at the same offset and one overwrites the other. `O_APPEND` fuses the seek and the write into **one atomic operation inside the kernel**. Measured: 4,396 lines of 80,000 survived (a), all 80,000 survived (b). *(L05 §5. "Two system calls are not one" is the week's sentence.)*

---

**Q6.** `> f 2>&1` — stdout is pointed at `f`, **then** stderr is made a copy of stdout, so both go to `f`. `2>&1 > f` — stderr is made a copy of stdout **while stdout is still the terminal**, then stdout alone is moved to `f`; stderr stays on the terminal. `dup2` copies **where the descriptor points at the moment it runs**, not a permanent link to descriptor 1. *(L06 §3.)*

---

**Q7.** Some process still holds a **write end of the pipe open** — usually the parent forgetting to close the end it gave away — so the reader never sees EOF. Confirm with **`ps -o pid,wchan,cmd`**: the hung reader is parked in `pipe_read`. *(L06 §4.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L04 §1 |
| **Q2, Q3** | **L04 §2–§3** — draw the three tables from memory until you can. This is on the Midterm |
| Q4 | L05 §2 |
| **Q5** | **L05 §5** — and Week 2 L09 §2 is the same bug in shared memory |
| Q6 | L06 §3 |
| Q7 | L06 §4, and Lab 1 Part C |

**Q2, Q3 and Q5 are the ones that recur.** Every mechanism in Week 2 is either giving you an atomicity guarantee (`PIPE_BUF`) or refusing to (shared memory), and you cannot reason about either without Q3's picture and Q5's rule.

---

*PROG 201 · Week 2 · Quiz 2 · covers Week 1 · ungraded*
