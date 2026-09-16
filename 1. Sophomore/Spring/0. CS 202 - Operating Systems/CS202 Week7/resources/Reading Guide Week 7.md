# CS 202 · Reading Guide · Week 7
## File Systems: OSTEP 39–41, and xv6's on Disk

---

**The curriculum names no reading for Week 7.** **Read OSTEP 40 before Wednesday** — it is the design PS 7 asks you to build — and **read the xv6 chapter with `fs.c` open**, because PS 7's functions are its functions with the locking removed.

> **Spring Break follows this week, and PS 7 is due the Friday you return.** The reading below is the
> shortest path to having PS 7 working before you leave.

| Source | Now? | Why |
|---|---|---|
| **OSTEP 39. Interlude: Files and Directories** | **Read** | The API — `open`, `read`, `link`, `unlink`, `fsync`, `rename` — and what each means on disk. **L22, L23 §5** |
| **OSTEP 40. File System Implementation** | **Read, twice** | Inodes, bitmaps, the multi-level index, directories. **This is `myfs`.** **L22, PS 7** |
| OSTEP 41. Locality and The Fast File System | **Read** | Block groups, and why putting an inode near its data mattered enough to reorganise the disk. **L24 §2** |
| **xv6 book (x86, rev. 11), Ch. 6 "File system"** | **Read §§6.1–6.6 with `fs.h` and `fs.c` open** | The code PS 7 mirrors. Skip the logging section — that is Week 8 |
| Silberschatz Ch. 11 §11.2–§11.4 | *Reference* | Allocation methods and free-space management, with pictures |
| `man 8 debugfs`, `man 8 dumpe2fs` | **Before L24** | How to read a real file system without root |
| `man 2 fsync`, `man 2 posix_fadvise`, `man 2 mincore` | **Before Lab 7** | The three calls the lab is built on |

**If you have two hours:** OSTEP 40, then xv6 Chapter 6 §6.3–§6.5, then start PS 7 Q1.

---

## OSTEP 39 — the API

1. `unlink` does not take a file descriptor and `close` does not delete anything. **Explain, using `nlink` and the open-file count, how a program can create a file that no other process can ever open and that disappears if the program crashes.**
2. OSTEP shows `rename` being used to update a file atomically. **What does "atomic" mean here exactly** — atomic with respect to what, and observed by whom? **What is still not durable** after the `rename` returns? *(L23 §5.)*
3. `fsync` on a file is not enough to make a *new* file durable. **Why not?** Which second object needs one?

---

## OSTEP 40 — implementation

4. OSTEP's example file system has 64 blocks: 8 inode blocks, bitmaps, and data. **Draw xv6's 1,000-block layout to the same scale** from L22 §2, and say which region xv6 has that OSTEP's does not.
5. **Work out, by hand, the reads needed to `open("/foo/bar", O_RDONLY)` and read the first block**, with nothing cached. Then check your answer against L22 §7's table.
6. §40.3 describes the multi-level index. **Compute the largest file for: 12 direct blocks; 12 direct + 1 indirect; and 12 direct + 1 indirect + 1 double indirect**, with 512-byte blocks and 4-byte addresses. **Which of those is xv6?**
7. OSTEP's `inumber` → block arithmetic is PS 7's `iread`. **For 64-byte inodes in 512-byte blocks, which block holds inode 100?**
8. §40.7 asks what happens when the file system is full but the bitmap says otherwise. **What does PS 7's `fsck` command check, and what could it not detect?**

---

## OSTEP 41 — FFS

9. FFS's answer to "where should this file's blocks go" is **the cylinder group of its inode**. **What is the modern equivalent**, and what does an SSD do to the argument? *(There is no seek; is locality still worth anything? L23 §2 has a clue.)*
10. FFS keeps a **free-space reserve** — it refuses to fill the disk completely. **Why does allocation quality collapse on a nearly full file system**, and what does that cost a file system using extents (L24 §3)?

---

## xv6 Chapter 6 — the code PS 7 mirrors

11. `bmap` allocates a block when one is missing, **even for a read**, in xv6. **Find the call and say why that is not a bug in xv6 — and why `myfs`'s `bmap` takes an `alloc` argument instead.**
12. `ialloc` scans the inode table linearly. **How many disk reads does allocating an inode cost on a file system with 200 inodes**, in the worst case? What does a real file system keep to avoid that?
13. `dirlink` reuses a free entry if it finds one. **Construct the sequence of creates and deletes after which a directory's size is far larger than the number of files in it**, and say what would reclaim the space.

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| **Love**, Ch. 13 "The Virtual Filesystem" | How Linux lets ext4, FAT and NFS all be file systems | For L24 |
| McKusick et al. (1984), "A Fast File System for UNIX" | The original cylinder-group argument | *Optional*, for L24 §2 |
| `man 5 ext4` | Every feature flag `dumpe2fs` prints | For L24 §2 |
| Kernel documentation, `filesystems/ext4/` (online) | Extent trees, `dir_index`, delayed allocation | For L24 §3–§6 |

---

*CS 202 · Week 7 · Reading Guide · © CSE Department*
