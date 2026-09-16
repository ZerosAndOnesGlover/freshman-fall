# CS 202 · Operating Systems
## Week 7 · Lecture 3 of 3
### Real File Systems on Disk

---

**Sat:** Friday of Week 7, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 41; Silberschatz §11.4 · **Next:** Spring Break, then Week 8 — crash consistency

---

## 1. What a Real Disk Format Has to Solve

L22's xv6 file system is the whole idea in 1,000 blocks: superblock, inodes, bitmap, data. **It also shows what a real file system cannot afford:**

| xv6 | Why it does not scale |
|---|---|
| 12 direct + 1 indirect block | **maximum file 71,680 bytes** |
| one free-block bitmap for the disk | a scan of the whole disk to allocate; every allocation writes the same blocks |
| inodes in one table at the front | **every file access seeks to the front and back** |
| directory = linear list of 16-byte entries | a lookup in a 10,000-file directory reads 160 KB |
| block = 512 bytes | metadata for a 1 GiB file: 2 million pointers |

**Everything in this lecture is an answer to one of those rows.** The examples are ext4, which is what BH 210's machines run, inspected on an image you can make yourself — **no root, no mounting**:

```bash
truncate -s 64M ext4.img
mkfs.ext4 -q -F -b 4096 -I 256 ext4.img
debugfs -R "stat /docs/big.bin" ext4.img
```

---

## 2. Bigger Blocks, and Block Groups

**ext4's block is 4 KiB** — one page, which is what the page cache deals in (L23). Bigger blocks mean fewer pointers and fewer seeks, at the cost of internal fragmentation: a 19-byte file still occupies 4 KiB.

**The disk is divided into block groups**, each with its own metadata:

```
$ dumpe2fs ext4.img
Blocks per group:         32768
Inodes per group:         16384
Group 0: (Blocks 0-16383)
  Primary superblock at 0, Group descriptors at 1-1
  Block bitmap at 9 (+9)
  Inode bitmap at 25 (+25)
```

**Each group holds its own bitmaps and inode table, next to its own data blocks.** A file's inode and its data are allocated in the same group whenever possible, so reading them is one short seek instead of two long ones — **FFS's idea from 1984**, and the reason a modern layout looks like many small file systems side by side.

**It also contains damage**: one corrupt group's bitmap costs that group, not the disk. *(A superblock copy lives in several groups, too.)*

---

## 3. Extents Instead of Pointers

**A 600 KiB file, in xv6's scheme, is 1,200 block numbers.** In ext4:

```
$ debugfs -R "ex /docs/big.bin" ext4.img
Level Entries       Logical      Physical Length Flags
 0/ 0   1/  1     0 -   149  2067 -  2216    150
```

**One extent: "logical blocks 0–149 are physical blocks 2067–2216".** Twelve bytes describe the whole file, and the file is **contiguous on disk** — one sequential read at 1.6 GB/s (L23 §1) instead of 150 scattered ones at 94 µs each.

- **An inode holds four extents inline**; a file needing more grows an **extent tree**, whose interior nodes point at further extents. The `0/0` above is the depth.
- **Fragmentation is now the enemy**, not pointer overhead: extents are cheap only while free space comes in long runs, which is why ext4 uses **delayed allocation** — it holds dirty pages in the page cache (L23 §3) and decides where they go when it writes back, by which time it knows how big the file is.
- **xv6's indirect block is the alternative**, and costs one extra read for every 128 blocks past the first twelve — plus a block of disk per file over 6 KiB.

The inode itself grew too: **256 bytes here**, holding nanosecond timestamps, a creation time, and room for extended attributes.

---

## 4. Directories Are Still Files — With an Index

```
$ debugfs -R "ls -l /docs" ext4.img
     12   40755 (2)      0      0    4096 16-Sep-2026 04:00 .
      2   40755 (2)      0      0    4096 16-Sep-2026 04:00 ..
     13  100664 (1)      0      0      19 16-Sep-2026 04:00 small.txt
     14  100664 (1)      0      0  614400 16-Sep-2026 04:00 big.bin
     14  100664 (1)      0      0  614400 16-Sep-2026 04:00 hard.bin
```

**The same structure as xv6's**: a directory is a file whose contents map names to inode numbers, `.` and `..` included. Two differences:

- **Entries are variable length** — a name up to 255 bytes, with its length stored — instead of xv6's fixed 14-byte field, which silently truncates.
- **`dir_index`**, on by default: large directories are stored as a **hashed tree** of blocks, so a lookup hashes the name and reads one block instead of scanning. **xv6 reads the whole directory, entry by entry** (L22 §5).

**And `big.bin` and `hard.bin` are one file**: both entries name **inode 14**, whose link count is 2. **Nothing in the directory says which name came first**; the file exists while any name does — exactly as in xv6, because this part of Unix has not changed since 1974.

---

## 5. Files With Holes

A 10 MiB file, written from a source that contained nothing:

```
$ debugfs -R "stat /sparse.bin" ext4.img
Size: 0
Links: 1   Blockcount: 0
```

**`ls -s` on the local 10 MiB file that produced it reports 0 blocks used, with `size 10485760`.** A file's **size and its block count are independent**: a region never written has no blocks, and reads as zeros — the file system's version of L18 §3's zero page.

**Sparse files are why `du` and `ls -l` disagree**, why copying a sparse file naively can turn 10 MiB into 10 GiB of writes, and why databases and virtual-machine images use them deliberately.

---

## 6. Allocation Policy: What the File System Chooses

**Correctness is the easy half; the policy decides performance.** Every file system answers these:

| Question | ext4's answer | xv6's answer |
|---|---|---|
| Which block for this file? | the same group as the inode, near its other blocks; **delayed** until write-back | the **first free bit** in the bitmap |
| Which group for a new directory? | one with free space and few directories, to spread them | there are no groups |
| How much to allocate at once? | multi-block, guided by the file's size and by **preallocation** | one block per `bmap` call |
| Small files? | packed in the same group as their directory | wherever the first free bit is |

**xv6's "first free bit" is a policy too, and a bad one**: over time the free bits are scattered, and every file's blocks are wherever the last deletion happened.

---

## 7. What Any of This Costs on a Crash

**Every operation in this lecture touches more than one block.** Creating a file writes the inode, the inode bitmap, the directory's data block, and the directory's inode. **The disk applies them in whatever order it likes** (L23 §5), and a crash in the middle leaves a file system that no longer makes sense: a directory entry pointing at a free inode, an inode pointing at blocks the bitmap calls free.

**`fsck` can find some of it** — myfs's `fsck` command in PS 7 does exactly this comparison, and can be made to report `leaked`, `used twice` and `used but not marked` blocks — **but it must read the entire disk to do so**, and on a large disk that takes hours.

**Week 8 is the alternative**: write down what you are about to do, before you do it.

---

## 8. What to Take Away

1. **A real layout answers xv6's limits point by point**: 4 KiB blocks, block groups with their own metadata, extents, indexed directories.
2. **Block groups put an inode near its data**, which is FFS's 1984 insight and still the reason layouts look the way they do.
3. **One extent described a 600 KiB file** — `0–149 → 2067–2216` — where xv6 would need 1,200 pointers and an indirect block.
4. **Directories are still files of name-to-inode entries**, now variable-length and hashed; **hard links are two entries naming one inode**, as in 1974.
5. **Size and block count are independent**: a sparse file of 10 MiB can occupy nothing.
6. **Allocation policy is where performance is decided**, and delayed allocation exists so the file system can decide late, knowing more.
7. **Every operation spans several blocks, and a crash can tear it** — which is Week 8.

---

## Exercises

1. A 1 GiB file, in blocks of 4 KiB. **How many pointers does xv6's scheme need, and how many extents does ext4 need** if the free space is one contiguous run? If it is in 1 MiB pieces?
2. `mkfs.ext4` on a 64 MiB image made **16,384 inodes for 16,384 blocks.** What ratio is that, and **what kind of file system runs out of inodes** with free blocks left?
3. **Why does ext4 delay deciding where a file's blocks go** until write-back? Name something it knows then that it did not know at `write()`.
4. `dir_index` hashes names. **What does that cost when a program reads a directory in order** — and what does `readdir` have to do to give a stable order?
5. In §7's list of four writes for one file creation, **give an ordering of the writes that leaves the file system consistent if it is interrupted at any point**, or argue that none exists.

---

*CS 202 · Week 7 · L24 · © CSE Department*
