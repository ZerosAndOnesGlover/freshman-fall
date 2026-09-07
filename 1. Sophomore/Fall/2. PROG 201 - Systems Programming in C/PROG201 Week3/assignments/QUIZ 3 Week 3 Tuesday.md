# PROG 201 · Quiz 3
## Administered: Tuesday, Week 3 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 2** — pipes and their capacity, `PIPE_BUF`, FIFOs, message queues, shared memory and semaphores.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
> Sit it closed-book, then turn the page and mark it yourself before you leave the room — the point
> is to find out what has not landed while there is still a term left to fix it.
>
> **Midterm 1 is next week** and covers Weeks 0–3. Anything you miss here, fix this week.

---

**Q1.** A pipe accepts 65,536 bytes when written 4,096 at a time, and only 45,066 bytes when written 4,097 at a time. Explain, in terms of what a pipe is made of.

&nbsp;

&nbsp;

---

**Q2.** State the `PIPE_BUF` guarantee exactly. Give the value on these machines and the header it is declared in.

&nbsp;

&nbsp;

---

**Q3.** Four processes write 8 KB records into one pipe. A test with a fast reader shows zero corruption in 8,000 records. What, if anything, have you learned?

&nbsp;

&nbsp;

---

**Q4.** A FIFO-based server reads requests in a loop. It handles the first client and then stops. What happened, and what is the one-line fix?

&nbsp;

&nbsp;

---

**Q5.** You call `shm_open`, then `mmap`, then write one byte through the pointer, and the process dies. Which signal, and what did you forget?

&nbsp;

&nbsp;

---

**Q6.** Four processes increment a shared counter 200,000 times each without a lock. Roughly what fraction of the increments survive, and why is the answer not "almost all of them"?

&nbsp;

&nbsp;

---

**Q7.** A pipe moved 256 MiB at 3,680 MiB/s; a one-slot shared-memory ring moved the same data at 574 MiB/s. Give the two reasons.

&nbsp;

&nbsp;

---
---

# Answer Key

*Mark your own. Be honest — nobody else will see this.*

---

**Q1.** A pipe is a **ring of sixteen buffers, each one page (4,096 bytes)** — the enforced limit is the *slot count*, not the byte count. A write merges into the tail buffer only if the whole write fits in the room left there, so a 4,097-byte write never merges cleanly, spills into a second page, and exhausts the sixteen slots after about 45 KB. **68.8% efficiency, measured.** *(L07 §2.)*

---

**Q2.** **A write of `PIPE_BUF` bytes or fewer to a pipe is never interleaved with data from other writers.** It is **4,096** on Linux, declared in **`<limits.h>`** — not `<unistd.h>`, which is where people look. Note that it bounds *your request size*, not the pipe's capacity: 4,096 is atomic even though 65,536 fit. *(L07 §4.)*

---

**Q3.** **Nothing.** 8 KB is twice `PIPE_BUF`, so the guarantee does not cover it and the program is wrong. The same code with a reader that drains in pieces smaller than a record corrupted **1,192 of 1,200**. A test that does not tear is not evidence of atomicity — it is evidence that this run did not reach the failure. *(L07 §4. This is the week's most transferable idea and it is on the midterm.)*

---

**Q4.** When the first client closed its write end, **no write end was open anywhere**, which is EOF — and the server could not distinguish "no client right now" from "no client ever again". The fix: the server **opens the FIFO for writing as well and never writes to it**, so the last write end never closes and a gap between clients is a block rather than an end. *(L07 §6.)*

---

**Q5.** **`SIGBUS`**, not `SIGSEGV`. You forgot **`ftruncate`** — a `shm_open`ed object is created with zero length, `mmap` does not check the length, and the first page fault finds nothing behind the mapping. `SIGSEGV` means "not mapped"; `SIGBUS` means "mapped, but nothing behind it". *(L08 §6.)*

---

**Q6.** About **a third** survive — 282,666 of 800,000, **64.7% lost**. It is not "almost all" because `counter++` is load-add-store and four processes on four cores are executing those three instructions on the same cache line as fast as they can. **A race window is only narrow relative to how often you aim at it**, and here every iteration aims at it. *(L09 §2. Compare Week 3's threaded version: 70.7%.)*

---

**Q7.** **(1) A pipe already has a sixteen-slot ring**, so producer and consumer overlap; a one-slot shared ring forces a blocking handoff every 4 KB, at ~3 µs each against a 118 ns copy. **(2) There were never fewer system calls** — 131,114 for the pipe against 131,817 futex calls for the ring. What shared memory removes is the copy, and the copy was not the cost. Deepening the ring to four slots gets past the pipe; below ~64 KB per message, shared memory loses. *(L09 §5–§6.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L07 §2 |
| **Q2, Q3** | **L07 §4** — and be able to state the guarantee without the observation |
| Q4 | L07 §6 |
| Q5 | L08 §6 |
| **Q6** | **L09 §2**, and this week's L10 §6 is the same result with threads |
| **Q7** | **L09 §5–§6** — the whole of Lab 2 is this answer |

**Q2, Q3 and Q7 are the ones that recur, and Midterm 1 is next week.** Q3's shape — *a test that passes does not establish the guarantee* — is the single idea from Weeks 0–3 most likely to be asked about in prose rather than in code.

---

*PROG 201 · Week 3 · Quiz 3 · covers Week 2 · ungraded*
