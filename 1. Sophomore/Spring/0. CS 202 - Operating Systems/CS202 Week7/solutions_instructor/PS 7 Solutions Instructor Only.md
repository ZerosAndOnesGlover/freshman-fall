# CS 202 · Problem Set 7 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 7.** This is the term's first "build the whole thing" problem set, and **the driver's output format does the marking for you**: a correct set of functions reproduces every line. **Give the implementation marks for output, and the explanation marks for the reasoning**, which is where students who copied an implementation come apart.

**PS 8 adds journaling to this code.** A student whose `myfs` does not work cannot start PS 8, so **chase down non-working submissions in the Week 8 lab session** rather than waiting for the marks to be returned.

**Reference:** `solutions_instructor/myfs reference (do not distribute).c` — the skeleton with the eleven functions filled in. Both it and the skeleton compile with no compiler output.

All output below is from the reference on the reference machine (Ubuntu 24.04.4, GCC 13.3.0).

---

## Q1: Blocks and Inodes (20 points)

### (a) [12]

```
$ ./myfs test.img format 2048
formatted 2048 blocks of 512 bytes: superblock 1, inodes 2-17, bitmap 18-18, data 19-2047
128 inodes, 2029 data blocks, max file 71680 bytes
$ ./myfs test.img dump
dump: size 2048 ninodes 128 inodestart 2 bmapstart 18 datastart 19
bitmap: ff ff 1f 00 00 00 00 00  (blocks 0-63)
```

**Reference `balloc` and `ialloc`** are the same scan-and-set that xv6 uses:

```c
static uint32_t balloc(void)
{
    char blk[BSIZE];
    for (uint32_t b = 0; b < sb.size; b += BPB) {
        bread(sb.bmapstart + b / BPB, blk);
        for (uint32_t bi = 0; bi < BPB && b + bi < sb.size; bi++) {
            int m = 1 << (bi % 8);
            if (!(blk[bi / 8] & m)) {
                blk[bi / 8] |= m;
                bwrite(sb.bmapstart + b / BPB, blk);
                char zero[BSIZE] = { 0 };
                bwrite(b + bi, zero);          /* hand out clean blocks */
                return b + bi;
            }
        }
    }
    die("out of blocks");
    return 0;
}
```

**[12] for both lines of output.** **Deduct 4** for a `balloc` that does not zero the block — it shows up in Q3, where a truncated-and-rewritten file reads back old bytes in its last partial block.

### (b) [4]

**`ff ff 1f` is blocks 0–20 marked** — `ff` = 0–7, `ff` = 8–15, `1f` = 16–20. **[2]**

**Those are exactly the metadata blocks plus the root directory's first data block [2]:** block 0 unused, 1 superblock, 2–17 inode table (128 inodes ÷ 8 per block = 16 blocks), 18 bitmap, 19 the first data block — and **block 20 is the root directory's first data block**, allocated by `format` when it writes `.` and `..`. *(Data starts at 19, and 19 is the block `balloc` handed to the root.)*

**Accept** any answer that names metadata + the root directory's block; **do not accept** "the first 21 blocks are reserved".

### (c) [6 — the handout says 4; mark out of 4 and record the extra 2 as bonus at your discretion]

For 100,000 blocks, with the reference's fixed 128 inodes:

| Region | Blocks |
|---|---:|
| unused + superblock | 2 |
| inode table | 128 ÷ 8 = **16** |
| bitmap | ⌈100,000 ÷ 4,096⌉ = **25** |
| data | 99,957 |

**Metadata is 43 blocks — 0.043%.** **[2]**

**How it changes [2]:** the bitmap grows **linearly** with the disk (one bit per block), the inode table does not grow at all here, so **the metadata fraction falls towards the bitmap's fixed 1/32,768 of the disk** — one bit per 4,096-bit block. **A student who notices that 128 inodes for 100,000 blocks is absurd** — a disk that runs out of inodes with 99% of its blocks free — **should be given the bonus**: real file systems size the inode table as a fraction of the disk (L24 Exercise 2).

---

## Q2: Files (25 points)

### (a) [15]

```
$ ./myfs test.img mkdir /docs
mkdir /docs: inode 2
$ ./myfs test.img create /docs/a.txt
create /docs/a.txt: inode 3
$ ./myfs test.img write /docs/a.txt 100 41
write /docs/a.txt: 100 bytes at 0, size now 100, 1 blocks
$ ./myfs test.img stat /docs/a.txt
stat /docs/a.txt: inode 3 file links 1 size 100 blocks 1
$ ./myfs test.img write /docs/a.txt 8192 42
write /docs/a.txt: 8192 bytes at 0, size now 8192, 16 blocks
$ ./myfs test.img stat /docs/a.txt
stat /docs/a.txt: inode 3 file links 1 size 8192 blocks 17
```

**The common bug**: `bmap` allocating the indirect block but forgetting to write the inode back, so the address is lost on the next command — the second `write` then reports 16 blocks and `fsck` reports leaks. **Deduct 5**, and point at it in feedback.

### (b) [5]

**8,192 bytes = 16 data blocks, and `stat` counts 17 [2]: the seventeenth is the indirect block**, which holds the addresses of blocks 12–15.

**The count first exceeds the data blocks at block 13 — 6,657 bytes [2]**: twelve blocks fit in the inode's direct addresses, so a file of 6,144 bytes needs no indirect block, and one byte more does.

**At most they differ by one [1]**, because there is only one indirect block in this design.

### (c) [5]

```
$ ./myfs test.img write /big 71680 44
write /big: 71680 bytes at 0, size now 71680, 140 blocks
$ ./myfs test.img write /big 71681 44
myfs: file too large
```

**The derivation [2]:** 12 direct + 128 indirect addresses (512 ÷ 4) = **140 data blocks × 512 = 71,680 bytes.**

**Raising it [3]** — any one, with its cost:

| Change | New maximum | Cost |
|---|---|---|
| a **double indirect** address, as Unix does | +128 × 128 blocks = **8.4 MiB** | 4 more bytes of inode; **two extra reads** per access past 71,680 bytes |
| bigger blocks, 4 KiB | (12 + 1,024) × 4,096 = **4.2 MiB** | internal fragmentation: a 19-byte file costs 4 KiB |
| more direct addresses | +512 bytes each | inode grows; fewer inodes per block, so the table grows |

**The xv6 kernel agrees with the arithmetic**: `bigf` in L22 §3 wrote 71,680 bytes and then `write` returned −1.

---

## Q3: Reading and Writing (20 points)

### (a) [12]

```
$ ./myfs test.img append /docs/a.txt 512 43
append /docs/a.txt: 512 bytes at 8192, size now 8704, 17 blocks
$ ./myfs test.img read /docs/a.txt 8180 40
read /docs/a.txt 8180+40: 40 bytes  42 x12  43 x28
```

**The marks are for partial blocks.** A student who reads and writes only whole blocks gets the file sizes right and this line wrong.

### (b) [4]

**Bytes 8,180–8,191 are the last twelve bytes of block 15** — written by `write … 8192 42`, hence `42`. **Bytes 8,192–8,219 are the first 28 bytes of block 16**, which `append … 512 43` created, hence `43`. **[2 for the split, 2 for naming which command wrote each.]**

### (c) [4]

Any sequence that writes past a gap. With the provided commands, the simplest is:

```
$ ./myfs test.img create /hole
$ ./myfs test.img write /hole 100 41
$ ./myfs test.img append /hole 100 42
```

— which has no hole. **The honest answer is that the driver's commands cannot make one**, because `write` and `append` always start at 0 or at the end. **Full marks for a student who says so and describes what would**: a `write` command taking an offset, leaving `bmap` to return 0 for the untouched blocks in between. **[2]**

**Size and block count [2]:** for a file with holes, **`size` is the offset of the last byte written, and the block count is only the blocks actually allocated** — the count can be far smaller than `size ÷ 512`, exactly as L24 §5's sparse file has size 10 MiB and zero blocks.

---

## Q4: Directories, Names and Links (25 points)

### (a) [15]

```
$ ./myfs test.img link /docs/a.txt /b.txt
link /docs/a.txt /b.txt: inode 3 links 2
$ ./myfs test.img ls /
ls /
  .              inode   1 dir  links 3 size 64
  ..             inode   1 dir  links 3 size 64
  docs           inode   2 dir  links 2 size 48
  b.txt          inode   3 file links 2 size 8704
$ ./myfs test.img rm /docs/a.txt
rm /docs/a.txt: inode 3 still has 1 links
$ ./myfs test.img stat /b.txt
stat /b.txt: inode 3 file links 1 size 8704 blocks 18
$ ./myfs test.img rm /b.txt
rm /b.txt: inode 3 freed
```

**Watch for `namei` that does not handle the root path `/`** and for `dirlink` that appends instead of reusing a freed slot — the latter shows up as `/` growing after the `rm`s.

### (b) [5]

**Root's 3 links [2]:** its own `.`, its `..` (the root is its own parent), and **`/docs`'s `..`**.

**`/docs`'s 2 links [1]:** the name `docs` in the root, and its own `.`.

**Creating a directory adds one to its parent [1]**, because the new directory's `..` points at the parent. **Removing a file changes no directory count [1]**, because a file has no `..` — only the file's own `nlink` falls.

### (c) [5]

```
$ ./myfs test.img df
df: 21 of 2048 blocks used (2027 free), 2 of 127 inodes used
$ ./myfs test.img fsck
fsck: 2 inodes in use, 21 blocks marked, 21 blocks reachable, 0 leaked, 0 used twice, 0 used but not marked
```

**[3] for reproducing both.** *(21 blocks: 19 metadata + 1 root data + 1 `/docs` data; 2 inodes: the root and `/docs`.)*

**The deliberate leak [2]:** removing the `itruncate` call from `rm` when `nlink` reaches 0 — the inode is freed, so nothing reaches its blocks, but their bits stay set. **`fsck` would then report the file's blocks as `leaked`** — for the 8,704-byte file, **18 leaked** — with `blocks marked` 18 higher than `blocks reachable`. **Accept** any equivalent (freeing the inode before the blocks, or `bfree`ing only the direct blocks).

---

## Q5: What This Design Costs (10 points)

### (a) [5]

For `write /docs/a.txt 8192 42` over a 100-byte file, the reference performs, per 512-byte chunk: `bmap` (reads the inode block implicitly through the cached struct, plus the indirect block for blocks 12–15), a `bread` of the target block, and a `bwrite`. Counting the whole command:

| Operation | Count |
|---|---:|
| `itruncate`: bitmap reads/writes | 1 read + 1 write (the one old block) |
| `balloc` per new block: bitmap read, bitmap write, zero-write | 16 × 3 = 48 |
| inode writes (one per newly allocated direct block, plus the indirect) | 13 |
| indirect block reads/writes | 4 reads + 4 writes |
| data block read-modify-write | 16 reads + 16 writes |
| **about** | **≈ 100 block operations for 16 blocks of data** |

**Full marks for any careful count in this range with the reasoning shown [4]**, plus **[1]** for what a real file system avoids: **the read-before-write of a block that is about to be overwritten completely** (ext4 skips it), **the bitmap write per block** (multi-block allocation marks a run at once), and **the inode write per block** (one write at the end). *(L23 §3's write-back cache makes all of these cheap in memory, too.)*

### (b) [5]

**A directory of 10,000 files is 10,000 × 16 = 160,000 bytes = 313 blocks [2]**; a linear scan reads **157 on average for a hit, all 313 for a miss.** A four-element path reads that for each element: **over 600 block reads for one `open`.**

**ext4 hashes the name into a tree (`dir_index`), reading one or two blocks whatever the size [2]. The cost [1]:** the entries are no longer in creation order, so **`readdir` returns a hash order** — which is why programs that read a directory and stat every file get random access patterns, and why ext4 must keep a stable cookie for `telldir`/`seekdir` across a tree that can split.

---

*CS 202 · Week 7 · PS 7 Solutions · Instructor Only*
