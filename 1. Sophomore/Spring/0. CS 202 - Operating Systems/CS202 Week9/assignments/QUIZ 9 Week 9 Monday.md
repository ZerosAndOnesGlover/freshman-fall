# CS 202 · Quiz 9
## Administered: Monday, Week 9 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 8** — crash consistency, journaling, copy-on-write, checksums.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **PS 8 is due Friday, and Lab 8 is tomorrow afternoon. Project 2 is assigned this week**, and
> **Project 1 is due in two weeks.**

---

**Q1.** Creating a file writes the inode, the directory entry and the directory's size. **Give two different states a crash between those writes can leave**, and say which is worse.

&nbsp;

&nbsp;

---

**Q2.** A journal's four steps are log, commit, install, clear. **Which single block write decides whether the operation happened**, and what is true of the disk immediately before and after it?

&nbsp;

&nbsp;

---

**Q3.** Replaying a log after a crash must be safe even if the machine crashes again during the replay. **What property makes that true**, and what kind of log entry would not have it?

&nbsp;

&nbsp;

---

**Q4.** Measured: `myfs` with a journal took **113** block writes for an operation that needed **92** without one — 1.23×, not 2×. **Explain the shortfall.**

&nbsp;

&nbsp;

---

**Q5.** A file system journals metadata only, in `data=ordered` mode. **What does it promise about a file you wrote one second before a power cut, and what does it not?**

&nbsp;

&nbsp;

---

**Q6.** A snapshot of a 64 MiB copy-on-write image cost **196 KiB**. Then 64 scattered 4 KiB writes grew it by **4,160 KiB**. **Explain both numbers.**

&nbsp;

&nbsp;

---

**Q7.** One byte is flipped in an ext4 inode table, and one byte in a file's data block. **Which does `e2fsck` detect, and why the difference?**

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **An orphaned inode** — the inode is marked in use and no directory entry names it: a block of the disk is lost, silently. **A dangling entry** — a name pointing at a free inode: **worse**, because opening it reads whatever the inode is reused for, which is another file's data.

---

**Q2.** **The log header — the commit record.** Before it, the log holds the new contents but the header says the log is empty, so recovery ignores it and the disk is the **old** state. After it, recovery will replay the log, so the disk is the **new** state even though no home block has been touched yet.

---

**Q3.** **Replay is idempotent**: `install_blocks` writes whole blocks' *new contents*, so doing it twice writes the same bytes. **A relative entry** — "add 4 to the free count", "decrement `nlink`" — would not be: applying it twice gives a different answer.

---

**Q4.** **Absorption.** A block written many times inside one operation takes **one** log slot: the bitmap, the inode and the indirect block are each logged once but written repeatedly. Measured: 19 log slots covered an operation of 92 home writes.

---

**Q5.** **It promises the file system's own structures are consistent** — no orphaned inodes, no leaked blocks — and, in `ordered` mode, that **no file contains another file's deleted data**. **It does not promise your data is there**: the write may have been in the page cache. Only `fsync` promises that.

---

**Q6.** **196 KiB** is the overlay's own metadata — its L1 table and header; **it holds no data, and reads fall through to the backing file.** **4,160 KiB for 256 KiB written** is copy-on-write at cluster granularity: the image's cluster is **64 KiB**, so the first write anywhere in a cluster copies the whole cluster — 64 × 64 KiB.

---

**Q7.** **The inode-table flip is detected** — ext4's `metadata_csum` stores a CRC on every metadata structure and checks it on read. **The data flip is not**: ext4 checksums its own structures, not file data, so `e2fsck` reports the file system clean and the program gets the corrupted byte. That is the case ZFS's end-to-end checksums exist for.

---

### What to Do With Your Score

There is no score. Instead, before Friday:

| If you missed | Reread |
|---|---|
| Q1 | L25 §1–§2 |
| **Q2, Q3** | **L26 §1–§3 — and PS 8 Q2 is exactly this** |
| Q4 | L26 §5 |
| Q5 | L26 §6 |
| Q6 | L27 §2 |
| Q7 | L27 §5 — **Lab 8 Part C** |

---

*CS 202 · Week 9 · Quiz 9 · covers Week 8 · ungraded*
