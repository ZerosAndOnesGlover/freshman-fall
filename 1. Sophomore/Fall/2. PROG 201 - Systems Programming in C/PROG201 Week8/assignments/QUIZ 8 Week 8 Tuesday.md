# PROG 201 · Quiz 8
## Administered: Tuesday, Week 8 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 7** — the VFS, inodes, directory entries, links, on-disk layout, journalling and durability.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Midterm 2 was last night** and covered Weeks 4–7. This is that material once more; use it to
> find out what the paper found, before the marks come back.

---

**Q1.** `stat` a file and get `st_size` 0, then `read` forty bytes from it successfully. Where is that file, and what is the general rule?

&nbsp;

&nbsp;

---

**Q2.** `a.txt` and `b.txt` are hard links to one file; `s.txt` is a symlink to `a.txt`. You delete `a.txt`. What is the state of each of the three, and why?

&nbsp;

&nbsp;

---

**Q3.** You delete a 10 GiB log file and `df` reports no more free space than before. What has happened, and how do you find the cause?

&nbsp;

&nbsp;

---

**Q4.** ext2 stores a 5,000,000-byte file in 4,883 data blocks and 21 more. What are the 21, and how many disk accesses does it take to reach the last byte? What does ext4 do instead?

&nbsp;

&nbsp;

---

**Q5.** You zero the primary superblock of a filesystem. Every file comes back after `e2fsck -b 8193`. Why did losing it not lose any data?

&nbsp;

&nbsp;

---

**Q6.** You overwrite 1,024 bytes of a file's data with random noise and run `e2fsck -fn`. It reports the filesystem clean. Explain, and say what kind of filesystem would not.

&nbsp;

&nbsp;

---

**Q7.** Writing 4 KiB records with an `fsync` after each is 154× slower than writing them and syncing once. And a safe file replacement needs **two** `fsync`s. Name the second one and say what is lost without it.

&nbsp;

&nbsp;

---
---

# Answer Key

*Mark your own. Be honest — nobody else will see this.*

---

**Q1.** It is under **`/proc`** (or `/sys`) — `/proc/self/stat` is the measured example. Those filesystems have no storage; their files are generated when read, and `stat` fills in zeros for fields with no meaning.

The rule: **read until `read` returns 0; never size a buffer from `st_size`** on a file you did not create. *(L22 §1.)*

---

**Q2.** **`a.txt`: gone** — the name was removed. **`b.txt`: a complete file**, unchanged except that its link count dropped from 2 to 1; there was never an "original", and both names were equally real. **`s.txt`: dangling** — it holds the *string* `a.txt`, which no longer resolves.

**A hard link is another name for the file; a symlink is a file containing a name.** *(L23 §1, measured.)*

---

**Q3.** **A process still has the file open.** `unlink` removes a name and decrements the link count; the blocks are freed only when the count is zero **and** no descriptor refers to it.

Find it with **`lsof | grep deleted`**, or by looking for `(deleted)` in `/proc/*/fd/`. The fix is to restart or signal the process, not to delete anything else. `df` disagreeing with `du` is the classic symptom. *(L23 §4.)*

---

**Q4.** **Pointer blocks** — one single-indirect, one double-indirect, and 19 more single-indirects hanging off it. With 1 KiB blocks an indirect block holds 256 pointers, so each one covers 256 data blocks.

Reaching the **last** byte takes **four** accesses: the inode, the double indirect, an indirect, then the data.

ext4 uses **extents** — the same file is two records of (logical range → physical start), no pointer blocks, and **one** access, because the extent is in the inode. *(L23 §6–§7.)*

---

**Q5.** The superblock holds the filesystem's **parameters** — magic number, block size, counts, feature flags, state, UUID — and **no file data and no pointers to any**. The inode table's location is derivable from the parameters, and every inode is where it always was.

So the filesystem became unreadable without anything being destroyed, and 1 KiB copied from a backup at block 8193 restored it. *(L24 §2.)*

---

**Q6.** Because **data integrity is not one of the invariants a filesystem check verifies.** `e2fsck` checks that bitmaps match inodes, that directory entries point at live inodes, and that link counts are right. ext4 checksums its **metadata** (`metadata_csum`) and does not checksum data at all — nothing in the filesystem knows what the file was supposed to contain.

**ZFS and btrfs would**, because they checksum every data block, and pay space and CPU for it. *(L24 §6, measured: rc=0, "clean".)*

---

**Q7.** The second `fsync` is on the **directory** — open it `O_RDONLY|O_DIRECTORY` and `fsync` that descriptor, after the `rename`.

Without it you can lose **the file entirely**: `rename` is atomic with respect to other processes, but the new directory entry is metadata in the page cache like anything else, so a crash can leave neither the new name nor the temporary one. Measured, it doubles the cost: 4.17 ms to 8.05. *(L24 §8.)*

---

### What to Do With Your Score

There is no score. Instead:

| If you missed | Reread |
|---|---|
| Q1 | L22 §1 and §5 |
| **Q2, Q3** | **L23 §1 and §4** — and run `./links` from the Lab 7 folder |
| Q4 | L23 §6–§7 |
| Q5, Q6 | L24 §2 and §6 — you sat Lab 7 yesterday |
| **Q7** | **L24 §8** — and it is on PS 7 |

**Q6 is the one that recurs.** It is this term's fifth instance of the same idea: a check that passes tells you about the check. Week 2's untorn records, Week 4's 339×, Week 5's "Hello, world" benchmark, Week 7's clean `fsck` — and this week, a `LD_PRELOAD` profiler reporting zero allocations because the compiler deleted them.

---

*PROG 201 · Week 8 · Quiz 8 · covers Week 7 · ungraded*
