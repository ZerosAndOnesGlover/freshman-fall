# CS 202 · Lab 8 — Solutions and TA Notes
## **INSTRUCTOR ONLY** · Do not distribute

---

**Session:** Tuesday of Week 9, 15:00–16:50, BH 210. **Unmarked** — checked off in the session.

**What the session is actually for.** Week 8's lectures assert that a journal makes every crash point safe and that copy-on-write makes snapshots cheap. **This lab is where students cause the crashes themselves** and watch both claims hold — and watch ext4 hand back a corrupted byte with a clean bill of health.

**PS 8 is due the Friday of this week.** Part D is PS 8's own test harness, so **students who have done PS 8 will finish Part D in ten minutes** — put them on Part C, which nobody finds easy, and use them to help others.

---

## Timing

| Minutes | Part | TA action |
|---|---|---|
| 0–10 | A | Instant; do not let anyone try to install ZFS |
| 10–40 | B | `qemu-io` syntax is the only obstacle; put the loop on the board |
| 40–65 | **C** | **The best part of the lab.** Students expect `e2fsck` to catch both corruptions |
| 65–90 | D | PS 8 students will be done; pair them with students who are not |
| 90–110 | Checkoff | |

---

## Answers

Reference machine: ext4 on NVMe, `qemu-img`/`qemu-io` 8.2.2, `e2fsprogs` 1.47.0, no ZFS, no btrfs.

### Q1 — the tools you do not have

```
zfs: command not found
btrfs: command not found
cp: failed to clone 'copy.c' from 'myfsj.c': Operation not supported
```

**`cp --reflink` asks the file system to make a second file that shares the first file's blocks**, copying a block only when one of them is written — **copy-on-write at file granularity.** **ext4 cannot**: its extents record which blocks a file owns, with **no reference count**, so two files cannot share a block and know when to copy.

**Two that can: btrfs and XFS** *(also ZFS, in its own way)*. **What they share with `qcow2`:** blocks are **reference-counted and never overwritten in place** — a write to a shared block allocates a new one. **Accept** any two of btrfs/XFS/ZFS with that reason.

### Q2 — the size of a snapshot

| | Size on disk |
|---|---:|
| base, 64 MiB written | **65,796 KiB** |
| **fresh overlay** | **196 KiB** |

**A snapshot of a 64 MiB image costs 196 KiB** — its L1 table and header, nothing else.

```
$ qemu-io -f qcow2 -c "read -P 0xaa 1M 4k" over.qcow2
4 KiB, 1 ops
```

**The data came from the backing file.** The overlay's L2 tables mark every cluster it does not have as **unallocated**, and the format's `backing_file` header field says where to look instead. `qemu-img info --backing-chain` prints the chain. **Accept** "the overlay has no entry for that cluster, so the read falls through".

### Q3 — write amplification

| Cluster size | 64 scattered 4 KiB writes (256 KiB of data) | Growth |
|---|---:|---:|
| **64 KiB** (default) | overlay 196 → **4,356 KiB** | **+4,160 KiB ≈ 16×** |
| 4 KiB | overlay 16 → **404 KiB** | **+388 KiB ≈ 1.5×** |

**The ratio is the cluster size ÷ the write size**: touching one byte of a cluster that lives in the backing file **copies the whole cluster**, then applies the write. 64 KiB ÷ 4 KiB = 16. **[The 1.5× at 4 KiB clusters is the data plus L2 metadata.]**

**For a database writing 8 KiB pages: small clusters** — 4 KiB or 8 KiB — or the first write to every page costs 64 KiB. **What large clusters buy:** far fewer L2 entries (less metadata, better sequential layout) and **fewer allocations**, which matters for large sequential writes and for images that are mostly untouched.

### Q4 — the cost of the first write

200 scattered 4 KiB writes:

| Target | Per write |
|---|---:|
| the base image | **1.90 ms** |
| an overlay on it | **2.31 ms** (**+21%**) |

**The overlay must read the cluster from the backing file, merge the 4 KiB, allocate a new cluster, write it, and update its L2 table** — a read-modify-write plus metadata, where the base simply writes. **Accept** "read-modify-write of the cluster".

*(Both numbers are dominated by `qemu-io` issuing each write separately with a flush; the **ratio** is the point, not the absolute figures.)*

### Q5 — corrupt metadata

```
$ e2fsck -fn fs.img
e2fsck: Inode checksum does not match inode while reading bad blocks inode
This doesn't bode well, but we'll try to go on...
Error while iterating over blocks in inode 1: Inode checksum does not match inode
```

**Detected — by the `metadata_csum` feature** (`dumpe2fs -h` lists it in *Filesystem features*). **Every metadata structure — superblock, group descriptors, inodes, directory blocks, extent blocks, the journal — carries a CRC32c**, checked when it is read. **[Full marks require naming the feature flag.]**

### Q6 — corrupt data

```
$ e2fsck -fn fs2.img
fs2.img: 12/8192 files (0.0% non-contiguous), 7002/32768 blocks       ← clean
$ debugfs -R "dump data.bin /dev/stdout" fs2.img | xxd | head -1
00000000: e65b c195 026f f1bf                      .[...o..
   the file began: 195b c195 026f f1bf
```

**`e2fsck` reports the file system clean, and the file returns the corrupted byte.** **One sentence:** **ext4 checksums its own structures, not your data**, so nothing in the file system can notice.

**To catch it**, the file system must **store a checksum of every data block** — and **ZFS puts it in the block pointer, in the parent**, not in the block itself, so that a misdirected or stale write cannot bring its own matching checksum along. With redundancy (a mirror or RAID-Z) it can then **repair** rather than merely report. **[2 marks: the checksum; 2: where ZFS puts it and why; 1: repair needs a second copy.]**

### Q7 — the sweeps

```
7 writes to complete; 6 crash points: 3 before, 3 after, 0 inconsistent          (create, recover)
113 writes to complete; 112 crash points: 92 before, 20 after, 0 inconsistent    (write 8192, recover)
113 writes to complete; 112 crash points: … 14 inconsistent                      (write 8192, norecover)
```

**With recovery: none. Without: fourteen.**

**Where they fall:** all fourteen are in **step 3, the install** — after the commit header is on disk and before the home blocks have all been written. **They can fall nowhere else**: before the commit, the header says the log is empty and the image is simply the old state; after the clear, the operation is complete. **[The window is exactly `lh.n` block writes wide — 19 for this operation — of which 14 produced a detectably broken image; the other five happened to write blocks whose absence `fsck` cannot see.]**

### Q8 — the durability boundary

| Crash after | `logdump` | After `recover` |
|---:|---|---|
| 92 writes | `n 0` | **the old file** |
| **93 writes** | **`n 19 49 33 52 …`** | **the new file** |

**Write 93 is the log header — the commit record.** It is one 512-byte write, and it is the entire difference between the operation having happened and not. **[Students' numbers differ with their implementation; what must be shown is `n 0` on one side and `n > 0` on the other.]**

### Q9 — without a journal

```
3 writes to complete; 2 crash points: 0 before, 0 after, 2 inconsistent           (create)
92 writes to complete; 91 crash points: 57 before, 0 after, 34 inconsistent       (write 8192)
```

**36 of 93 crash points leave a file system this week's `fsck` calls broken**, and **no crash point leaves the completed operation.**

**One case, in full:** crashing `write /d/x 8192 43` after 30 writes gives

```
fsck: 3 inodes in use, 26 blocks marked, 25 reachable, 1 leaked, …
```

**The missed write is the inode.** `balloc` had marked a bitmap bit and zeroed the new block — two writes — and the crash came before the `iwrite` that would have recorded the block's address in the inode. **The bitmap says the block is used; nothing points at it; it can never be allocated again and never be found.**

**For `create`, the missed write is `dirlink`'s**: `ialloc` marks the inode in use first, so a crash between them **orphans an inode**. **Accept** either failure with the write named.

---

## Common Problems

| Symptom | Cause | Fix |
|---|---|---|
| `qemu-io: command not found` | not installed on a personal machine | it is on the lab image; `apt` is not available to students |
| Overlay grows by the full 64 MiB | wrote sequentially over the whole image | the point is *scattered* writes; use the given offsets |
| `e2fsck` reports nothing after the metadata flip | flipped a byte in an unused inode, or in a block group's padding | use the inode table block `dumpe2fs` prints, and an offset inside a live inode |
| Sweep reports inconsistencies with a correct-looking journal | `end_op` installs before writing the header | ask where the commit point is |
| Sweep takes minutes | the image is large, or `write 8192` on a slow home directory | 2,048-block images; run in the lab file system, not on a network mount |

---

*CS 202 · Week 8 · Lab 8 Solutions · Instructor Only*
