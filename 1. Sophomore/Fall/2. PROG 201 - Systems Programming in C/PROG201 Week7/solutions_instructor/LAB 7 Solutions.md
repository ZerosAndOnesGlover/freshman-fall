# PROG 201 · Lab 7 Solutions
## Corrupt and Recover a Filesystem — Instructor Only

---

**Do not distribute.** Corruptions (3) and (4) are the lab, and both are spoiled by knowing the answer.

**Machine these numbers came from:** Linux 7.0.0-30-generic, `e2fsprogs 1.47.0`, root filesystem ext4 mounted `noatime` on NVMe. **Nothing in this lab needs root and nothing is ever mounted** — `mke2fs`, `debugfs`, `dumpe2fs` and `e2fsck` all operate on an ordinary file, and that is worth saying to the room at the start, because several students will assume they cannot do this on a shared machine.

---

## 1. Setup and What Provides What

`mkimage.sh` and `verify.sh` are provided complete; `links.c`, `vfs.c`, `durable.c` and `durable2.c` are the lecture demonstrations, also complete. **Students write no C in this lab** — it is a lab about a tool and a data structure, and the writing is in the answers.

One detail in `mkimage.sh` worth knowing: it runs `e2fsck -fy` at the end, **because `debugfs`'s `ln` does not update the link count** and the image would otherwise start dirty. Corruption (2) then re-creates that same inconsistency deliberately. A student who notices the `e2fsck` in the build script and asks why has found the mechanism early; tell them.

---

## 2. Reference Output

**Part A(a) — layout**, 64 MiB, 1 KiB blocks:

```
Inode count: 16384      Block count: 65536      Block size: 1024
Blocks per group: 8192  Inodes per group: 2048  Overhead clusters: 7451

  Primary superblock at 1,     Group descriptors at 2-2
  Backup superblock at 8193,   Group descriptors at 8194-8194
  Backup superblock at 24577,  Group descriptors at 24578-24578
  Backup superblock at 40961,  Group descriptors at 40962-40962
  Backup superblock at 57345,  Group descriptors at 57346-57346
  Inode table at 275
```

**Part A(b) — the three inodes:**

```
/alias.txt      Links: 2   (same inode as /docs/note.txt)
/link.txt       Size: 14   Blockcount: 0    Fast link dest: "/docs/note.txt"
/longlink.txt   Size: 75   Blockcount: 2    EXTENTS: (0):4583
```

**Part A(c) — the same 5,000,000-byte file, both filesystems:**

```
ext2:  (0-11):882-893, (IND):894, (12-267):895-1150,
       (DIND):1151, (IND):1152, (268-523):1153-1408, ... 17 more IND ...
       TOTAL: 4904          <- 4,883 data blocks + 21 pointer blocks

ext4:  EXTENTS: (0-3608):4584-8192, (3609-4882):8451-9724
                            <- 2 records, 0 pointer blocks
```

**Part A(d) — the journal:** inode 8, `Size: 4194304`, `Total journal size: 4096k` — **6.2% of a 64 MiB filesystem.** `tune2fs -O ^has_journal` reclaims exactly 4,096 blocks.

**Part B(1) — superblock:** `dumpe2fs` gives *"Bad magic number in super-block"*; `e2fsck -fy -b 8193` reports a couple of count fixes and `FILESYSTEM WAS MODIFIED`; `verify.sh` then passes all eight content checks. **`e2fsck` also finds a backup unaided** — *"Superblock invalid, trying backup blocks..."* — which several students will discover by forgetting `-b`.

**Part B(2) — link count:**

```
$ e2fsck -fn lc.img
Pass 4: Checking reference counts
Inode 13 ref count is 1, should be 2.  Fix? no
lc.img: ********** WARNING: Filesystem still has errors **********
rc=4

$ e2fsck -fy lc.img
Inode 13 ref count is 1, should be 2.  Fix? yes
lc.img: ***** FILESYSTEM WAS MODIFIED *****
rc=1
```

**Part B(3) — a data block:**

```
$ e2fsck -fn data.img
Pass 5: Checking group summary information
data.img: 17/16384 files (5.9% non-contiguous), 14595/65536 blocks
rc=0

$ ./verify.sh data.img
  ok    e2fsck: clean
  ...
all checks passed
```

**The filesystem is clean, `verify.sh` passes everything, and 1,024 bytes of `big.bin` are random noise.** `verify.sh` checks *sizes*, not contents — which is itself worth pointing out, and a student who says "your script is wrong" has understood the question.

**Part B(4) — one directory block:**

```
$ e2fsck -fy dir.img
Pass 2: Checking directory structure
Directory inode 2, block #0, offset 0: directory corrupted
Salvage? yes
Missing '.' in directory inode 2.  Fix? yes
Missing '..' in directory inode 2.  Fix? yes
Pass 3: Checking directory connectivity
Unconnected directory inode 11 (was in /)  Connect to /lost+found? yes
/lost+found not found.  Create? yes
Unconnected directory inode 12 (was in /)  Connect to /lost+found? yes
...
Pass 4: Inode 11 ref count is 3, should be 2.  Fix? yes
rc=1                                    <- errors corrected, not "clean"

$ ./verify.sh dir.img
=== structure ===
  ok    e2fsck: clean
=== contents ===
  FAIL  /docs/note.txt exists
  ... 8 check(s) failed

$ debugfs -R "ls /" dir.img
 2  (12) .    2  (12) ..    18  (988) lost+found

$ debugfs -R "ls -l /lost+found" dir.img
     11   40700 ...            #11
     12   40755 ...            #12
     14  100664 ...   200000   #14
     15  100664 ...  5000000   #15
     16  120777 ...       14   #16
     17  120777 ...       75   #17
```

**Every file, complete, with no name.** `#15` is all five million bytes of `huge.bin`.

**A note on that `rc=1`.** `e2fsck -fy` exits **1** — errors corrected — not 0, and a run of `e2fsck -fn`
afterwards gives 0 because there is now nothing left to fix. If a student reports rc=0 from the
repair itself, they have almost certainly piped `e2fsck` into `head` and read the pipeline's status
rather than `e2fsck`'s. **It is worth catching**, because Q1 is about exactly that exit code and the
same mistake was made while writing this file.

**Part C — durability:** as in L24 §7–§8. On tmpfs (`/dev/shm`) the whole table collapses to microseconds, which is the extension.

---

## 3. Answers

**Q1 — `e2fsck` exit codes.**

**0** clean, **1** errors corrected, **2** corrected and reboot needed, **4** errors left **uncorrected**, 8 operational error, 16 usage error.

`-n` answers "no" to every question and **opens the filesystem read-only**, so a monitoring script can ask "is this filesystem healthy?" without changing anything; rc=4 then means "there are errors and I have not touched them". `-p` is **preen**: fix only what is unambiguously safe, without asking, and exit with 4 if anything needs a human. **`-p` is what boot scripts run**, and rc=4 is what makes the machine drop to a maintenance shell.

**Q2 — the fast symlink.**

ext4 stores the target **inside the inode**, in the 60 bytes that would otherwise hold the extent tree or block pointers, when the target is short enough to fit — so `Blockcount: 0`. The threshold is **60 bytes**; 14 fits and 75 does not.

Full marks require "in the space the block pointers would have used". A student who says "in the inode" gets [2 of 3]; ask them *where* in the inode.

**Q3 — the pointer blocks.**

**4,883 data blocks, `TOTAL: 4904`, so 21 pointer blocks** — one single-indirect for the first 256, one double-indirect, and 19 more single-indirects hanging off it.

Accesses to the **last** byte: on ext2, **four** — inode, DIND, IND, data. On ext4, **one** (plus the inode), because the extent covering it is in the inode itself.

**Q4 — the superblock.**

It holds the filesystem's *parameters*: magic number, block size, block and inode counts, blocks per group, feature flags, the state and the UUID. **It contains no file data and no pointers to any** — the inode table's location is derivable from the parameters, and the inodes are where they always were. So a zeroed superblock makes the filesystem unreadable without destroying anything in it, and 1 KiB from a backup restores it.

**Q5 — the exit codes and the pass.**

**rc=4** from `-fn` (errors, not corrected); **rc=1** from `-fy` (errors corrected). **Pass 4** — reference counts — found it.

A block belonging to two files is caught in **pass 1**, which is the pass that builds the block map and notices a collision. That is the corruption that destroys data rather than wasting space (L24 §3), and it is the reason pass 1 is first.

**Q6 — the data block. This is the question.**

**`e2fsck` reported the filesystem completely clean, rc=0.**

Because a filesystem check verifies the filesystem's own invariants — that the bitmaps match the inodes, that every entry points at a live inode, that link counts are right — and **your file's contents are not one of them.** ext4 checksums its *metadata* (`metadata_csum` is in the feature list) and does not checksum data at all; there is nothing in the filesystem that knows what `big.bin` was supposed to contain.

So: **`fsck` tells you the filesystem is usable, not that your data is correct.** Filesystems that do check data — ZFS and btrfs, with per-block checksums — exist precisely for this, and cost space and CPU for it.

Full marks need the distinction stated. "It didn't notice" is [1]; "it didn't notice, because data integrity is not one of the invariants it checks" is [4].

**Q7 — why the names were unrecoverable.**

**Because an inode does not contain a name.** The mapping from names to inode numbers lived entirely in the directory's data block, and that block is what was destroyed. The inodes survived intact — every one of them has its mode, size, link count and block pointers — but nothing anywhere in the filesystem records what any of them was *called*.

`e2fsck` could tell that inodes 11–17 were in use and unreferenced, so it invented names for them (`#N`) and put them in `lost+found`. That is the most it can do.

This is L23 §1 arriving as a consequence, and it is the lab's point.

**Q8 — `lost+found`.**

The numbers are the **inode numbers**. `e2fsck` has no other identifier available.

What to do next, and any of these earns the mark provided it is specific: **`file *` in `lost+found`** to identify types; **`grep`** for known content; check sizes against what you remember; and — the real answer — **restore from a backup**, because this is what backups are for. A student who says "restore from backup" with the reasoning that names are unrecoverable in principle has the best answer.

**Q9 — the 154×.**

Buffered writes go to the page cache and return; a durable write waits for the storage device to acknowledge that the data is on stable media, which is milliseconds even on NVMe. 41,980 rec/s against 255.

What a database does: **group commit** — batch many transactions into one `fsync`, so *N* transactions cost one flush rather than *N*. Accept also "a write-ahead log" (one sequential fsync per batch instead of scattered random ones) or "a battery-backed write cache". The mark is for naming a technique that amortises the flush, not for avoiding it.

**Q10 — the directory `fsync`.**

`rename` is atomic **with respect to other processes**: a concurrent reader sees the old file or the new one, never a mixture. It says nothing about what survives a power cut, because the new directory entry is metadata sitting in the page cache like anything else.

Without the directory `fsync` you can lose **the file entirely**: `cfg.txt` still names the old inode or nothing, and `cfg.tmp` is gone too, so a crash leaves you with neither. The extra 4.17 ms is buying **the durability of the name**, having already bought the durability of the contents.

---

## 4. Checkoff

The four boxes are in the lab sheet. In practice:

- **Corruptions (3) and (4) back to back** are the session. Do not let a pair skip (3) to get to (4); the pair only works as a contrast.
- **Ask Q7 out loud.** Almost everyone says "because the block was destroyed"; push for *why nothing else knew the names*.
- Students who finish Part B early should be sent to Part C rather than given more corruptions — the durability numbers are on Midterm 2 and the corruptions are not.
- **`verify.sh` checks sizes, not contents.** If a student points that out, they have earned the extension: have them add a checksum check and re-run corruption (3).

**Timing.** Setup 5, Part A 25, Part B 45, Part C 20 — 95 against 110, which leaves room for the checkoff queue. **The room must be clear by 16:50: Midterm 2 is at 18:00.**

---

*PROG 201 · Week 7 · Lab 7 Solutions · Instructor Only · © CSE Department*
