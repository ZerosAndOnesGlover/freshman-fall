# PROG 201 · Systems Programming in C
## Week 7 · Lecture 3 of 3
### On-Disk Layout, Journalling, and Durability

*“Design bugs are often subtle and occur by evolution with early assumptions being forgotten as new features or uses are added to systems.”* — Fernando J. Corbató, "On Building Systems That Will Fail" (Turing Award lecture, 1991)

---

**Reading:** TLPI §14.3–14.5, §13.3 · APUE §4.24 · `man 5 ext4`, `man 8 e2fsck`, `man 2 fsync` · **Previous:** L23 · **Next:** Lab 7 — corrupt and recover a filesystem, **Monday of Week 8**

**Coursework:** 📝 **PS 6** due Fri this week 17:00 · 🔬 **Lab 7** Mon of Week 8 15:00–16:50 · 📊 **Quiz 8** Tue of Week 8 · 📝 **PS 8** released Wed of Week 8, due Fri of Week 9 17:00

---

## 1. What a Filesystem Looks Like on Disk

`mke2fs` on a 64 MiB file, and `dumpe2fs` reading it back:

```
Inode count:              16384
Block count:              65536
Block size:               1024
Blocks per group:         8192
Inodes per group:         2048
Inode blocks per group:   256
Overhead clusters:        7451
```

The shape:

```
 block 0        boot block (unused by the filesystem)
 block 1        SUPERBLOCK          -- the whole filesystem's parameters
 block 2        group descriptors   -- one per block group
 ...
 block group 0: [ sb backup ][ gd backup ][ block bitmap ][ inode bitmap ][ inode table ][ data ... ]
 block group 1: [ ... the same shape ... ]
 ...
```

**A block group is a filesystem in miniature**: its own bitmaps, its own slice of the inode table, and its own data blocks. Eight of them here, 8,192 blocks each.

**They exist for locality.** A file's inode and its data blocks are allocated in the same group if possible, and a new directory goes in a group with free space — so reading a file is a short seek rather than a long one. On an SSD it matters much less than it did in 1993; on the rotating disk ext2 was designed for it was the difference between usable and not.

**Overhead is 7,451 blocks of 65,536 — 11%** on a filesystem this small, most of it the inode table. `mke2fs` allocates all the inodes at format time (16,384 of them here, one per 4 KiB of disk by default), which is why **you can run out of inodes with free blocks** — `df -i` is the command, and a mail spool full of tiny files is the classic way to do it.

---

## 2. The Superblock, and Why There Are Nine of Them

The superblock holds everything about the filesystem: block size, counts, feature flags, the state, the UUID. Lose it and the filesystem is unreadable.

So there are backups:

```
  Primary superblock at 1,     Group descriptors at 2-2
  Backup superblock at 8193,   Group descriptors at 8194-8194
  Backup superblock at 24577,  Group descriptors at 24578-24578
  Backup superblock at 40961,  Group descriptors at 40962-40962
  Backup superblock at 57345,  Group descriptors at 57346-57346
```

Zero the primary and the filesystem vanishes:

```
$ dd if=/dev/zero of=sb.img bs=1024 seek=1 count=1 conv=notrunc
$ dumpe2fs -h sb.img
dumpe2fs: Bad magic number in super-block while trying to open sb.img
```

And comes back:

```
$ e2fsck -fy -b 8193 sb.img
Free inodes count wrong (16373, counted=16368).  Fix? yes
sb.img: ***** FILESYSTEM WAS MODIFIED *****

$ debugfs -R "ls /" sb.img
 2  (12) .   11  (20) lost+found   12  (12) docs   14  (16) big.bin   13  (20) alias.txt ...
```

**Every file was still there**, because a superblock is 1 KiB of parameters and none of the data depends on it. `e2fsck` will even find a backup by itself — *"Superblock invalid, trying backup blocks..."* — and `-b 8193` only tells it where to look.

**The magic number is `0xEF53`**, at offset 0x438 within the superblock, and it is what every tool checks first. `sparse_super`, a feature you will see in the flags, is why the backups are at 8193, 24577, 40961 — powers of 3, 5 and 7 times the group size, rather than in every group.

---

## 3. What a Crash Breaks

Creating one file touches at least four things:

1. the **inode bitmap** — mark an inode used;
2. the **inode table** — write the inode;
3. the **block bitmap** and the **data blocks**;
4. the **directory** — add the name.

**A crash between any two of them leaves the filesystem inconsistent**, and the failures are not symmetric:

| Crash after | Result |
| --- | --- |
| bitmap, before the inode | an inode marked used with garbage in it |
| the inode, before the directory | an **orphan**: a file with data and no name — this is what `lost+found` is for |
| the directory, before the inode | a **name pointing at nothing**, or at whatever was there before |
| freeing blocks, before updating the bitmap | **leaked** blocks: allocated to nobody, never reused |
| updating the bitmap, before freeing | **doubly-allocated** blocks: two files sharing data. The worst one |

The last row is the one that destroys data rather than merely wasting it, and it is why the ordering of metadata writes was, for twenty years, the hardest problem in filesystem design.

**The pre-journal answer was `fsck`**: on every boot, walk the entire filesystem and check the invariants. It works, and it takes time proportional to the number of inodes — minutes for a 1990s disk, **hours for a modern one**. A server that takes two hours to boot after a power cut is not a server.

---

## 4. The Journal Is a File

ext3's answer, inherited by ext4: **write down what you are about to do, before you do it.**

```
Filesystem features:  has_journal ext_attr resize_inode dir_index filetype extent ...
Journal inode:        8
Total journal size:   4096k
Total journal blocks: 4096
```

and inode 8 is an ordinary-looking file:

```
Inode: 8   Type: regular   Mode:  0600   Size: 4194304   Blockcount: 8192
```

**Four mebibytes, which is 6.2% of this 64 MiB filesystem.** Remove it and the space comes back exactly:

```
$ tune2fs -O ^has_journal nojournal.img
  with journal   : 50941 free blocks
  without journal: 55037 free blocks     -> 4096 blocks reclaimed
```

The protocol, per transaction:

```
1. write the changed metadata blocks into the journal
2. write a COMMIT record
3. ...later... write the metadata to its real location  ("checkpointing")
4. free that part of the journal
```

**Recovery is then trivial**: replay every transaction that has a commit record, discard any that does not. It takes seconds rather than hours, and it is bounded by the journal's size rather than the filesystem's.

**Note what the journal does not promise: that your data is safe.** It promises the *filesystem's own structures* are consistent — no doubly-allocated blocks, no orphans. Whether your file's contents survive is §5.

---

## 5. Three Journalling Modes, and What Each One Actually Promises

`data=` is a mount option, and the default is the middle one:

| Mode | Journals | After a crash |
| --- | --- | --- |
| `data=journal` | metadata **and data** | both consistent. Every byte written **twice** |
| **`data=ordered`** (default) | metadata; **data written before the metadata commits** | metadata consistent, and a file never shows another file's old data |
| `data=writeback` | metadata only, in any order | metadata consistent; **a file may contain stale blocks** — somebody else's deleted data |

**`ordered` exists because of the security problem in `writeback`.** If the inode says "this file is 4 KB" before the 4 KB has been written, a crash leaves a file whose contents are whatever was in those blocks before — which might be another user's deleted mail. Ordering the data write before the metadata commit costs nothing extra and removes it.

**And none of the three promises that a file you just wrote exists at all.** Journalling is about consistency, not durability, and the difference is §6.

*(A related surprise: ext4's **delayed allocation** — L23 §7 — means a `write` that returned success may not have been allocated a block yet, so a crash can lose up to 30 seconds of it. This produced a famous argument in 2009 when applications that replaced config files with `rename` started ending up with empty files. The kernel now special-cases that pattern; §7 is how to be safe without relying on it.)*

---

## 6. `fsck` Still Exists, and Here Is It Working

A journal makes `fsck` unnecessary after a *crash*. It does not make it unnecessary after a *bug*, bad memory, or a disk that lied.

`debugfs` can create a hard link without updating the link count, which is exactly the kind of inconsistency a bad write produces:

```
$ e2fsck -fn disk.img
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Inode 13 ref count is 1, should be 2.  Fix? no
disk.img: ********** WARNING: Filesystem still has errors **********
rc=4
```

```
$ e2fsck -fy disk.img
Inode 13 ref count is 1, should be 2.  Fix? yes
disk.img: ***** FILESYSTEM WAS MODIFIED *****
rc=1
```

**Read the pass names**, because they are the invariants a filesystem has:

| Pass | Checks |
| --- | --- |
| 1 | every inode's blocks are sane and no block belongs to two inodes |
| 2 | every directory entry points at an in-use inode of the right type |
| 3 | every directory is reachable from `/` — unreachable ones go to `lost+found` |
| 4 | every inode's link count equals the number of entries pointing at it |
| 5 | the bitmaps match what passes 1–4 actually found |

**And the exit status is an API**: 0 clean, **1 errors corrected**, **2 corrected and reboot needed**, **4 errors left uncorrected**, 8 operational error. A boot script reads that number; `-n` (answer no) plus a check for 4 is how you find out whether a filesystem needs attention without touching it.

---

## 7. Durability Is a Separate Question, and It Costs 154×

`write` returning success means the kernel has your data. It does not mean the disk does.

`durable.c`, 200 records of 4 KiB on this machine's NVMe SSD:

| | rec/s | per record |
| --- | --- | --- |
| write only, one `fsync` at the end | **41,980** | 0.02 ms |
| write + `fdatasync` every record | 273 | 3.67 ms |
| write + `fsync` every record | 255 | 3.91 ms |
| `O_SYNC` | 280 | 3.58 ms |
| `O_DSYNC` | 266 | 3.76 ms |

**A hundred and fifty-four times.** That gap is the entire reason databases exist as separate programs: they are, largely, machinery for getting durability without paying 4 ms per record — group commit, write-ahead logs, and a lot of care about what actually has to be on the platter.

### `fsync` against `fdatasync`

The appending test above shows almost no difference, because appending changes the file's **size** and `fdatasync` must then write the inode anyway. Take the size change away — overwrite in place — and the difference appears:

| overwrite in place, size never changes | per record |
| --- | --- |
| `fsync` | **4.11 ms** |
| `fdatasync` | **1.26 ms** |

**Three and a quarter times**, and it is one inode write. `fdatasync` skips metadata that is not needed to read the data back — the timestamps, chiefly. **Use `fdatasync` unless you need the timestamps**, which almost nobody does.

---

## 8. The `fsync` Everybody Forgets

Here is the pattern for replacing a file safely, and the mistake in it:

```c
int fd = open("cfg.tmp", O_WRONLY | O_CREAT | O_TRUNC, 0644);
write(fd, data, n);
fsync(fd);                       /* the CONTENTS are durable */
close(fd);
rename("cfg.tmp", "cfg.txt");    /* atomic swap */
```

**`rename` is atomic** — a reader sees the old file or the new one, never a half-written one — and that is why this is the pattern. But after a crash, **the new name may not exist**, because the directory entry that `rename` created is metadata that has not been written yet. You can lose the file entirely: `cfg.txt` gone, `cfg.tmp` gone.

The fix is one more `fsync`, on the **directory**:

```c
int d = open(".", O_RDONLY | O_DIRECTORY);
fsync(d);                        /* now the NAME is durable */
close(d);
```

And it is not free:

| the safe-write pattern, 50 times | per write |
| --- | --- |
| write, `fsync`, `rename` | 4.17 ms |
| write, `fsync`, `rename`, **`fsync` the directory** | **8.05 ms** |

**It doubles the cost**, which is why so much software omits it — and why "my config file was empty after the power cut" is a bug report every project eventually receives.

**The rules, in order:**

1. `fsync` the file before you `rename` it, or the new name may point at nothing.
2. `fsync` the **directory** after, or the new name may not exist.
3. Check `fsync`'s **return value**. It can fail, and on Linux before 4.13 a failed writeback could be reported once and then forgotten — the "fsyncgate" of 2018, which caused PostgreSQL to change how it handles the error, to panicking.
4. **None of this survives a disk that lies.** Consumer drives with volatile write caches acknowledge a flush before the data is on the medium unless the cache is disabled or the drive honours FUA. `hdparm -W` is the knob and the honest answer is that you find out by testing.

---

## Summary

- A filesystem is **superblock, group descriptors, and block groups**, each with bitmaps, an inode table slice and data. Overhead was **11%** on a 64 MiB image, mostly the inode table — **inodes are allocated at format time**, so `df -i` can fill while `df` does not.
- **Superblock backups at 8193, 24577, 40961, 57345.** Zero the primary and `e2fsck -b 8193` brings everything back; `e2fsck` finds one by itself anyway.
- A crash between metadata writes gives **orphans, leaked blocks, or doubly-allocated blocks** — the last is the one that destroys data. `fsck` on every boot was the old answer and takes hours.
- **The journal is a file** — inode 8, 4 MiB, **6.2%** of a 64 MiB filesystem. Write the intent, commit, then checkpoint; recovery replays committed transactions in seconds.
- Three modes: **`data=journal`** writes everything twice, **`data=ordered`** (default) writes data before the metadata commits, **`data=writeback`** can leave stale blocks in your file.
- **A journal promises consistency, not durability.**
- `e2fsck`'s five passes are the filesystem's five invariants, and **its exit status is an API**: 1 fixed, 4 not fixed.
- **Durability costs 154×** — 41,980 rec/s buffered against 255 with `fsync` per record. In place, **`fdatasync` is 3.3× cheaper than `fsync`** (1.26 ms against 4.11).
- **`fsync` the file, `rename`, then `fsync` the directory** — which doubles the cost, and omitting it is why config files come back empty.

---

## Exercises

1. `df -i` on your machine. How many inodes are free, and how many bytes per inode did `mke2fs` choose? Now work out what workload would exhaust them first.
2. Make a 64 MiB image, fill it with 1-byte files until something fails. Which ran out first, and what was the error?
3. Zero **two** superblocks — the primary and the one at 8193 — and recover. Which backup did you use, and how did you find it?
4. Corrupt a single byte in the inode table with `dd`, then run `e2fsck -fn`. Which pass caught it, and what did it propose?
5. Reproduce §7's table. Then run it against `/dev/shm` (tmpfs) and explain the numbers you get.
6. Write §8's safe-write pattern both ways and `strace` both. Count the system calls, and say which one the extra 4 ms is.
7. `data=writeback` is faster than `data=ordered`. Find the paragraph in `man 5 ext4` that says what you are giving up, and decide whether you would run a mail server on it.

---

*PROG 201 · Week 7 · L24 · © CSE Department*
