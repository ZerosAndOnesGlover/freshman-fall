# CS 202 · Operating Systems
## Week 8 · Lecture 3 of 3
### Copy-on-Write, Snapshots, and Checksums

*“Simplicity is prerequisite for reliability.”* — Edsger W. Dijkstra, "How do we tell truths that might hurt?" (EWD498, 1975)

---

**Sat:** Friday of Week 8, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 43 §43.1–§43.4; Bonwick & Ahrens on ZFS · **Next:** Week 9, I/O and device drivers

**Coursework:** 📝 **PS 7** due today 17:00 · 📊 **Quiz 9** Mon of Week 9 · 🔬 **Lab 8** Tue of Week 9 15:00–16:50 · 📋 **Project 2** released Wed of Week 9, due Fri of the completion period 17:00 · 📝 **PS 9** released Wed of Week 9, due Fri of Week 10 17:00

---

## 1. The Other Answer: Never Overwrite

**A journal writes everything twice so that an overwrite can be undone.** The alternative is to **never overwrite anything**: write the new block somewhere free, then update whatever points at it — which is itself a block, written somewhere free — up to the root of the tree. **One final write of the root makes the whole new tree live.**

**The old tree is still there**, complete and consistent, until its blocks are freed. **That gives three things at once:**

- **Crash consistency with no log**: a crash before the root write leaves the old tree; after it, the new one.
- **Snapshots for nothing**: keep the old root and do not free its blocks, and you have the file system as it was.
- **Cheap clones**: two roots can share every block they have in common.

**This is ZFS and btrfs.** *(Neither is installed on the lab machines — see the syllabus deviations — so the descriptions of them in §4 come from their papers and documentation, not from measurements here.)* **What can be measured here is the same mechanism one layer down:** `qcow2`, QEMU's disk image format, which is copy-on-write with a backing file.

---

## 2. Copy-on-Write, Measured

```bash
qemu-img create -f qcow2 base.qcow2 256M
qemu-io -c "write -P 0xaa 0 64M" base.qcow2          # fill it
qemu-img create -f qcow2 -b base.qcow2 -F qcow2 over.qcow2
```

| | Size on disk |
|---|---:|
| the base, 64 MiB written | **65,796 KiB** |
| **a fresh overlay on top** | **196 KiB** |
| the overlay after 64 scattered 4 KiB writes (256 KiB of data) | **4,356 KiB** |

**A snapshot of a 64 MiB image costs 196 KiB** — the overlay holds nothing but its own metadata, and every read falls through to the base:

```
$ qemu-io -c "read -P 0xaa 1M 4k" over.qcow2
4 KiB, 1 ops; 00.00 sec
```

**And then the cost appears, on the first write to each region:**

- **64 scattered 4 KiB writes grew the overlay by 4,160 KiB — sixteen times the data written.** The image's **cluster is 64 KiB**: touching one byte of a cluster copies the whole cluster out of the base.
- **With 4 KiB clusters, the same writes grew it by 388 KiB** — 1.5×, mostly metadata.
- **Writes are slower into an overlay**: 200 scattered 4 KiB writes cost **2.31 ms each against 1.90 ms** into the base — **+21%**, the read-modify-write of the cluster.

**That is copy-on-write's whole trade, in one table**: allocation is free until you write, and then you pay for a whole allocation unit. **A file system with 128 KiB extents and a snapshot will do the same thing to a database that writes 8 KiB pages.**

**Internal snapshots cost the same kind of nothing:**

```
$ qemu-img snapshot -c s1 filled.qcow2        # the image grows by 12 KiB
```

---

## 3. What Happens to Free Space

**Nothing can be freed while any root still points at it.** In §2's overlay, the base's blocks are pinned by the base; in a snapshotting file system, **a snapshot pins every block that has since been overwritten.**

**The consequences are the ones ZFS and btrfs administrators live with:**

- **Deleting a file may free nothing**, if a snapshot holds it.
- **"Disk full" can happen with an empty-looking file system**, and deleting more files makes it worse if snapshots keep them.
- **Free space is a question about a set of trees**, not a bitmap, so it is expensive to compute exactly.
- **Fragmentation is structural**: rewriting the middle of a file moves those blocks elsewhere, so a sequentially written file stops being sequential — exactly what L24 §3's extents wanted.

---

## 4. ZFS and btrfs, Described

*(From the literature; not measured on this machine.)*

| Idea | What it does |
|---|---|
| **Uberblock / superblock switch** | the root is written last and atomically, with several copies; this replaces the journal |
| **Checksums in the parent** | every block pointer carries a checksum **of the block it points at**, verified on every read |
| **Snapshots and clones** | a retained root; clones are writable snapshots |
| **RAID-Z / RAID1 profiles** | redundancy inside the file system, so a checksum failure can be **repaired** from another copy |
| **Send/receive** | the difference between two roots is a stream — incremental backup without scanning |

**The checksum is the part that changes what a file system can promise.** A journal keeps the file system's own structures consistent; **it says nothing about whether the bytes came back the way they went in.**

---

## 5. What ext4 Checks, and What It Does Not

**ext4 has checksums — on metadata.** Flipping one byte inside the inode table of an image:

```
$ e2fsck -fn corrupt.img
e2fsck: Inode checksum does not match inode while reading bad blocks inode
```

**Detected.** Now flip one byte of a **file's data block** instead:

```
$ e2fsck -fn corrupt2.img
corrupt2.img: 12/8192 files (0.0% non-contiguous), 7002/32768 blocks
$ debugfs -R "dump data.bin /dev/stdout" corrupt2.img | xxd | head -1
00000000: e65b c195 026f f1bf                      .[...o..
   the file originally began:
00000000: 195b c195 026f f1bf                      .[...o..
```

**The file system is "clean", and the file quietly returns the wrong byte.** Nothing in ext4 stores a checksum of file data, so **nothing can notice**. The disk is trusted to return what it was given.

**This is what "end-to-end checksums" means in the ZFS literature**, and why the argument for them is about **silent corruption**: bit rot, a firmware bug, a cable, a misdirected write. **Measured here: ext4 catches the metadata case and misses the data case entirely.**

---

## 6. What Linux Actually Ships

**Neither answer has won.**

- **ext4 with a metadata journal is the default on most distributions** — including the lab machines — because it is fast, predictable, and understood.
- **btrfs is the default on some** (openSUSE, Fedora Workstation for `/`), for snapshots and checksums.
- **ZFS is not in the mainline kernel** for licensing reasons, and ships as a separate module.
- **XFS journals metadata and adds copy-on-write for reflinks** — `cp --reflink` clones a file without copying it, which **ext4 refuses**:

```
$ cp --reflink=always a.bin b.bin
cp: failed to clone 'b.bin' from 'a.bin': Operation not supported
```

**The trade has not changed since §2's table**: journaling costs writes, copy-on-write costs fragmentation and free-space complexity, and checksums cost space and CPU to buy detection.

---

## 7. What to Take Away

1. **Copy-on-write never overwrites**, and makes a whole update atomic with one root write — **no log at all.**
2. **Measured on qcow2**: a snapshot of a 64 MiB image costs **196 KiB**; reads fall through to the base; **the first write to a cluster copies the cluster** — 16× amplification with 64 KiB clusters, 1.5× with 4 KiB — and costs **21% more** than a plain write.
3. **Snapshots pin blocks**: deleting a file may free nothing, and free space becomes a question about a set of trees.
4. **ZFS and btrfs add checksums in the parent pointer**, which lets a read *detect* corruption and, with redundancy, repair it.
5. **ext4 checksums metadata only.** Measured: a flipped inode byte is caught; **a flipped data byte is returned to the program with a clean `fsck`.**
6. **Both designs are in use**, and the choice is the trade in (2) and (3) against L26's write amplification.

---

## Exercises

1. A database writes 8 KiB pages into a file on a copy-on-write file system with 128 KiB extents, just after a snapshot. **How much is written per page write, and how does that change as the snapshot ages?**
2. **Why does a fresh qcow2 overlay cost 196 KiB rather than nothing?** What is in it?
3. In §5's experiment, `e2fsck` reported the corrupted-data image as clean. **Design a check ext4 could add** to catch it, and say what it would cost in space and in writes.
4. Copy-on-write makes snapshots cheap to *create*. **What is expensive about deleting one**, and why?
5. **Which of L26's journal and L27's copy-on-write would you choose** for: a laptop's root file system; a database server's data volume; a build machine's scratch disk? One sentence each, naming the measurement that decides it.

---

*CS 202 · Week 8 · L27 · © CSE Department*
