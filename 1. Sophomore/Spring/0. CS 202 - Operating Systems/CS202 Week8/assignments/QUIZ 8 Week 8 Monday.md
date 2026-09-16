# CS 202 · Quiz 8
## Administered: Monday, Week 8 (first 10 minutes of lecture)

**Name:** _________________________________ **Section:** ___________ **Date:** ___________

**Covers Week 7** — inodes, directories, the page cache, write-back, durability, and real file-system layouts.

**Instructions:** Closed notes. 10 minutes.

> **This quiz is not marked and carries no weight.** The answer key is printed below the questions.
>
> **Midterm 2 is this evening**, 18:00–19:15, VNC 100, covering **Weeks 4–7**. Every question here is
> fair game for it. **PS 7 is due Friday, and Lab 7 is tomorrow afternoon.**

---

**Q1.** A path is `/docs/a.txt`. **List the disk reads needed to read its first byte**, with nothing cached, and say what each read is for.

&nbsp;

&nbsp;

---

**Q2.** An inode has 12 direct addresses and one indirect block; blocks are 512 bytes and addresses 4 bytes. **What is the largest file, and how many blocks does a 7,000-byte file occupy on disk?**

&nbsp;

&nbsp;

---

**Q3.** Two directory entries name inode 14, whose `nlink` is 2. **One is removed. What happens to the file?** What would `nlink` have to be for the blocks to be freed?

&nbsp;

&nbsp;

---

**Q4.** A program reads one byte of a cold 512 MiB file. **How many pages does Linux bring into the page cache, and why not the maximum readahead window?**

&nbsp;

&nbsp;

---

**Q5.** `write()` of 64 MiB returned in 15 ms on a disk that can write 500 MB/s. **Where is the data, what does `/proc/meminfo` show, and when does it reach the disk if nobody calls `fsync`?**

&nbsp;

&nbsp;

---

**Q6.** A 4 KiB write costs 2.9 µs buffered and about 3,900 µs with `fsync`. **What is being waited for in the second case?** Would `O_DIRECT` alone make the write durable?

&nbsp;

&nbsp;

---

**Q7.** ext4 describes a contiguous 600 KiB file with **one extent**. **How many block addresses would xv6's scheme need for the same file**, and what does ext4 give up to make extents work well?

&nbsp;

&nbsp;

---
---

## Answer Key

**Q1.** **Six reads:** the root inode; the root's data block (to find `docs`); `docs`'s inode; `docs`'s data block (to find `a.txt`); `a.txt`'s inode; and the file's first data block. *(A seventh — the indirect block — for any byte past block 11.)*

---

**Q2.** Indirect block holds 512 ÷ 4 = **128** addresses, so the maximum is (12 + 128) × 512 = **71,680 bytes**. A 7,000-byte file needs ⌈7000/512⌉ = **14 data blocks, plus the indirect block = 15**, because it is past the twelve direct addresses.

---

**Q3.** **Nothing happens to the file**: the entry is removed and `nlink` drops to 1; the other name still reaches it. **The blocks are freed when `nlink` reaches 0** — and on Linux, only when no process still has it open.

---

**Q4.** **Four pages — 16 KiB.** `read_ahead_kb` is 128, but that is the **maximum**: the kernel has no evidence yet that the read is sequential, and grows the window only as the pattern continues.

---

**Q5.** **In the page cache, as dirty pages** — `Dirty` rises by 64 MiB. **It reaches the disk when the pages pass `dirty_expire_centisecs`** (15 s here) and the flusher writes them, or earlier if dirty memory crosses `dirty_background_ratio`.

---

**Q6.** **The flush of the drive's own write cache** (and the file system's metadata) — an actual round trip to durable storage. **No**: `O_DIRECT` bypasses the page cache but the drive still acknowledges into volatile cache; measured, `O_DIRECT` alone was 27.9 µs, and adding `fdatasync` brought it back to 3,682 µs.

---

**Q7.** 600 KiB ÷ 512 = **1,200 block addresses** — 12 in the inode and the rest through an indirect block, which xv6 could not even hold (its limit is 140 blocks). **ext4 gives up per-block freedom**: extents are compact only while free space comes in long runs, so it must fight fragmentation — hence delayed allocation.

---

### What to Do With Your Score

There is no score. Instead, before six o'clock:

| If you missed | Reread |
|---|---|
| Q1, Q2, Q3 | L22 §3–§7 — and the **Midterm 2 Revision Guide**'s inode arithmetic |
| Q4 | L23 §2 |
| **Q5, Q6** | **L23 §3–§4** — the table is worth memorising |
| Q7 | L24 §3 |

---

*CS 202 · Week 8 · Quiz 8 · covers Week 7 · ungraded*
