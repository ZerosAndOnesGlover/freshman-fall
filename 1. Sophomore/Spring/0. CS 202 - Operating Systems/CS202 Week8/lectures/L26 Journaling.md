# CS 202 · Operating Systems
## Week 8 · Lecture 2 of 3
### Journaling: Write It Down First

*“Documentation is like term insurance: It satisfies because almost no one who subscribes to it depends on its benefits.”* — Alan Perlis, "Epigrams on Programming" (1982), #71

---

**Sat:** Wednesday of Week 8, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 42 §42.3; xv6 book Ch. 8 · **Next:** L27, copy-on-write

**Coursework:** 📝 **PS 8** released today, due Fri of Week 9 17:00 · 📝 **PS 7** due Fri this week 17:00 · 📊 **Quiz 9** Mon of Week 9 · 🔬 **Lab 8** Tue of Week 9 15:00–16:50

---

## 1. Write-Ahead Logging

**The rule is one sentence: before changing anything in place, write down what you are about to do.**

An operation proceeds in four steps:

1. **Log** the new contents of every block the operation touches, into a reserved area of the disk.
2. **Commit**: write one block — the log header — recording how many blocks the log holds and where each belongs. **This single write is the moment the operation becomes real.**
3. **Install**: copy each logged block to its home.
4. **Clear**: write the header again, with zero blocks.

**A crash anywhere has exactly two possible outcomes.** Before step 2, the header says nothing is logged, so the log is ignored and **the disk holds the old state**. After step 2, recovery finds a committed log and **replays it**, producing the new state — however many times the machine crashes while doing so, because **installing a block twice writes the same bytes.**

---

## 2. The Commit Point, Measured

`myfsj` is PS 7's file system with that log (PS 8 asks you to add it). **Its layout puts the log right after the superblock:**

```
$ ./myfsj j.img format 2048
formatted 2048 blocks of 512 bytes: superblock 1, log 2-32, inodes 33-48, bitmap 49-49, data 50-2047
128 inodes, 1998 data blocks, log holds 30 blocks, max file 71680 bytes
```

**The same crash sweep as L25 §2, on the same operations:**

| Operation | Writes to complete | Crash points | Old state | New state | **Inconsistent** |
|---|---:|---:|---:|---:|---:|
| `create /d/y` | 7 | 6 | 3 | **3** | **0** |
| `write /d/x 8192` | 113 | 112 | 92 | **20** | **0** |

**Not one of 118 crash points left a broken file system**, against 36 of 93 without the log. **And now some crashes leave the *finished* operation**: the 20 points after the commit record all recover into the new file, because the log already held everything needed to finish it.

**The boundary is one block write.** Crash at write 96 of 113 and the file is unchanged; crash at 97 and it is written — **because write 97 is the header.**

---

## 3. Recovery Is Not Optional

**The log only helps if something replays it.** A real file system does that at mount; `myfsj` does it before every command that changes the disk. **Skip it, and the same sweep gives:**

```
without running recover: 14 of 112 crash points leave fsck complaining
```

**Those fourteen are the crashes during *install*** — after the commit, while blocks were being copied home. **The disk is half-updated and the log holds the other half**; the information to finish is right there, and ignoring it is what breaks the file system. **A journal without recovery is worse than no journal**, because it costs the extra writes and delivers nothing.

---

## 4. xv6's Log

xv6 has had one since the beginning; `log.c` is 240 lines, and the shape is §1 exactly:

```c
struct logheader {
  int n;
  int block[LOGSIZE];
};
```

```
  #define MAXOPBLOCKS  10             // max blocks any one operation writes
  #define LOGSIZE      (MAXOPBLOCKS*3)  // 30 blocks of log
```

**Three details are worth more than the code:**

- **`begin_op` and `end_op` bracket every system call that touches the disk**, and `log_write` replaces `bwrite`. A system call never writes its own blocks home.
- **Absorption**: writing the same block twice inside one operation takes **one** log slot. A file write that allocates ten blocks updates the bitmap ten times and logs it once.
- **Batching**: several system calls can share one commit. `end_op` decrements a count of outstanding operations and **commits only when it reaches zero** — so a busy file system pays one commit for many operations, which is where a log wins back some of its cost.

**And `MAXOPBLOCKS` is why xv6's file operations are small**: one system call may never touch more than ten blocks, because the log must hold a whole operation. `myfs`'s `write` of 8,192 bytes would not fit — **`myfsj` therefore logs a whole command as one transaction with a 30-block log, and its `write` command splits naturally** because each 512-byte chunk is its own set of blocks.

---

## 5. What the Log Costs

**Every logged block is written twice** — once to the log, once home. Measured:

| Operation | Without a journal | With | Ratio |
|---|---:|---:|---:|
| `create /d/y` | 3 writes | 7 | **2.3×** |
| `write /d/x 8192` | 92 writes | 113 | **1.23×** |

**Not 2× in either case.** The `create` costs more than double because the log adds **two header writes** to a three-write operation. The big `write` costs far less than double because **absorption**: the bitmap block, the inode block and the indirect block are each logged once, while the operation writes them many times.

**In a real file system the cost is measured in flushes, not writes.** The commit record must reach the disk **before** the installed blocks, or a crash could find installed blocks with no log — so a commit needs a flush, at L23 §4's ~4 ms. **This is why databases and file systems batch**, and why `fsync` on a journaled file system is often two flushes: one for the log, one for the commit record.

---

## 6. What ext4 Actually Journals

**Journaling every data block would double every write on the machine.** ext4 offers three modes:

| Mode | What is logged | What a crash can leave |
|---|---|---|
| `data=ordered` *(the default)* | **metadata only**, but data blocks are **forced to disk before** the metadata that points at them | metadata always consistent; **a file may lose recent writes, never show someone else's old data** |
| `data=writeback` | metadata only, no ordering | metadata consistent; **a file can contain stale blocks** — someone else's deleted data |
| `data=journal` | **everything**, data included | the strongest, at roughly **double the write traffic** |

```
$ dumpe2fs -h fs.img
Filesystem features:  has_journal ext_attr resize_inode dir_index filetype extent …
Journal inode:        8
Total journal size:   4096k
```

**The journal is a file** — inode 8 — of 4 MiB here, and `debugfs -R "logdump"` reads it. **Note what `data=ordered` does not promise**: that your file's contents are there after a crash. **Only `fsync` promises that** (L23 §5), and the file system's job is only to keep *itself* consistent.

---

## 7. What to Take Away

1. **Write-ahead logging makes a group of block writes atomic** by reducing it to one block write: the commit record.
2. **Measured: 0 of 118 crash points left `myfsj` inconsistent**, against 36 of 93 without the log — and 20 of them left the completed operation.
3. **Recovery is part of the design**: without it, **14 of 112** crash points break the file system.
4. **xv6's log is the same four steps**, with `begin_op`/`end_op`, **absorption**, and **batching** across system calls; `MAXOPBLOCKS` bounds an operation to what the log can hold.
5. **The cost is a second write per logged block** — 1.23× for a large write, 2.3× for a tiny one — **plus a flush per commit**, which is the part that actually hurts.
6. **ext4 journals metadata by default and orders data before it**, which keeps the file system consistent and says nothing about your data.

---

## Exercises

1. In §2's sweep, **92 of 112 crash points left the old state and 20 the new.** From §1's four steps, say which step each group falls in, and why the split is where it is.
2. **Why is replaying a log idempotent**, and what would break if `install_blocks` had to *append* rather than overwrite?
3. xv6's `MAXOPBLOCKS` is 10 and `LOGSIZE` is 30. **Why is the log three times the maximum operation**, and what happens if a single system call needs 11 blocks?
4. A file system commits with `data=writeback`. **Construct a crash after which a user's new file contains another user's deleted data**, and say what `data=ordered` does to prevent it.
5. Journaling doubles writes; **absorption reduces it**. For `write /d/x 8192`, §5 measured 113 against 92 writes. **Account for the 21 extra**, using the log's structure.

---

*CS 202 · Week 8 · L26 · © CSE Department*
