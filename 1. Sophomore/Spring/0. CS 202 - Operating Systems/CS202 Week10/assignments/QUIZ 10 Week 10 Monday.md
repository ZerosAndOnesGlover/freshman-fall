# CS 202 · Quiz 10
## Administered: Monday, Week 10 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 9** — the device interface, interrupts and DMA, the block layer, and writing a driver.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **PS 9 is due Friday, and Lab 9 is tomorrow afternoon. Project 1 is due Friday of next week.**

---

**Q1.** `read()` works on a file, a pipe and a terminal. **Name the structure that makes that possible in Linux and in xv6**, and say what a device file in `/dev` actually holds.

&nbsp;

&nbsp;

---

**Q2.** A write to `/dev/null` — whose driver does nothing — costs about **659 ns**. **What are you paying for?**

&nbsp;

&nbsp;

---

**Q3.** Reading 256 MiB with `O_DIRECT` cost **1,969** interrupts in 1 MiB requests and **65,536** in 4 KiB requests. **Explain both numbers**, naming the setting that decides the first.

&nbsp;

&nbsp;

---

**Q4.** **Why may an interrupt handler not sleep?** What does Linux do with work that must sleep?

&nbsp;

&nbsp;

---

**Q5.** A driver's `read` finds its buffer empty. **What must it do, and what must it not do?** Name the xv6 calls.

&nbsp;

&nbsp;

---

**Q6.** A student's driver copies to the user's pointer with `memcpy`. It passes every test. **Give the input that breaks it and say what happens** — in xv6, and in Linux.

&nbsp;

&nbsp;

---

**Q7.** `insmod hello.ko` fails with "Operation not permitted" although the module built. **Which capability is missing, and why is that the right default?**

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **Linux: `struct file_operations`** — a table of function pointers per open file. **xv6: `devsw[]`**, with just `read` and `write`, indexed by major number. **A device file holds no data**: it is a name carrying a **type, a major and a minor number**, created by `mknod`; the major number picks the driver.

---

**Q2.** **The system call**, not the driver: `syscall`/`sysret`, **two `CR3` switches for page-table isolation**, the file-descriptor lookup, and the indirect call through the operations table. Week 0 measured a bare `getppid` at about 590 ns on the same machine.

---

**Q3.** **One interrupt per command, not per byte.** The block layer splits requests at **`max_sectors_kb` = 128**, so a 1 MiB read becomes eight commands — about 2,000 interrupts for 256 requests. **A 4 KiB read is one command, so 65,536 reads raise 65,536 interrupts** — and take eight times as long for the same data.

---

**Q4.** **It runs on whatever process happened to be interrupted, with no context of its own** — there is nothing sensible to put to sleep, and the interrupted process would be blocked for someone else's reason. **Linux splits the work**: a top half that acknowledges the device, and a **bottom half** (softirq, tasklet, or a workqueue, which *may* sleep).

---

**Q5.** **It must block**: release nothing it should hold, and `sleep(&channel, &lock)` **inside a `while` loop** that re-tests the condition; the writer calls **`wakeup(&channel)`**. **It must not spin**, and must not return data it does not have.

---

**Q6.** **Any pointer the process does not own** — an unmapped address, or a kernel address. **In xv6 the kernel takes a page fault in kernel mode and panics**; in Linux it is an oops, killing the process and possibly leaving locks held. The fix is `argptr`/`copyout` in xv6 and `copy_to_user`/`copy_from_user` in Linux.

---

**Q7.** **`CAP_SYS_MODULE`** — root, in practice. **A loaded module runs in kernel mode with no restrictions**: it can read any memory, replace any system call, and disable every check. On a shared machine, granting it is granting the machine.

---

### What to Do With Your Score

There is no score. Instead, before Friday:

| If you missed | Reread |
|---|---|
| Q1, Q2 | L28 §1–§4 |
| Q3 | L29 §2 |
| Q4 | L29 §6 |
| **Q5, Q6** | **L30 §4–§5 — and PS 9 Q2 is exactly this** |
| Q7 | L30 §2 |

---

*CS 202 · Week 10 · Quiz 10 · covers Week 9 · ungraded*
