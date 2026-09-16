# CS 202 · Operating Systems
## Week 7 · Lecture 1 of 3
### Files, Inodes, and Directories

---

**Sat:** Monday of Week 7, 09:00–09:50, VNC 101, **after Quiz 7** · **Reading:** OSTEP Ch. 39–40; xv6 book Ch. 6 · **Next:** L23, the page cache

---

## 1. What a File Is, on Disk

**A file is a name, some metadata, and a way to find its blocks.** Unix splits those three deliberately:

| Thing | Where it lives | What it holds |
|---|---|---|
| the **name** | a **directory** — itself a file | the name, and one number |
| the **metadata** | an **inode**, found by that number | type, link count, size, block addresses |
| the **data** | data blocks | the bytes |

**The number in the directory is the inode number**, and it is the only connection between a name and a file. **Nothing in the inode records a name** — which is why a file can have several names, or none at all while still being open.

xv6's on-disk inode is fifteen lines (`fs.h`):

```c
struct dinode {
  short type;              // file, directory, device — or 0, meaning free
  short major, minor;      // device numbers (T_DEV only)
  short nlink;             // how many directory entries point here
  uint size;               // bytes
  uint addrs[NDIRECT+1];   // 12 direct block numbers, then one indirect
};
```

---

## 2. The Disk, Divided

xv6's `mkfs` builds the image and prints its layout:

```
$ make fs.img
nmeta 59 (boot, super, log blocks 30 inode blocks 26, bitmap blocks 1) blocks 941 total 1000
```

```
 block 0   1      2 .. 31   32 .. 57    58        59 .. 999
 [ boot | super |   log   |  inodes  | bitmap |  data blocks ]
```

- **The superblock** says how many blocks each region has and where each begins — everything else is found through it.
- **The log** is Week 8's subject: every file-system operation goes through it.
- **The inode table** is an array: **inode *i* lives at `inodestart + i/IPB`**, offset `(i % IPB)` — with 512-byte blocks and 64-byte inodes, **8 inodes per block**, 26 blocks for 200 inodes.
- **The bitmap** has one bit per block of the whole disk: **one 512-byte block covers 4,096 blocks**, so 1,000 blocks need one.
- **941 of 1,000 blocks are for data** — the metadata is 6% of this disk.

**Every structure here is an array indexed by a number**, which is why the code is short: no search, just arithmetic.

---

## 3. Finding a File's Blocks

**`bmap(ip, n)` answers "which disk block holds block *n* of this file?"**

```c
if(bn < NDIRECT)            // 0..11: the address is in the inode
  return ip->addrs[bn];
bn -= NDIRECT;
if(bn < NINDIRECT)          // 12..139: read the indirect block, then index it
  ...
```

**Twelve direct addresses, then one indirect block of 128 more** (512 bytes ÷ 4). So the largest xv6 file is **140 blocks = 71,680 bytes**, and `bigf` — which writes 512-byte blocks until `write` fails — agrees exactly:

```
$ bigf
wrote 71680 bytes = 140 blocks, then write returned -1
```

**The design is a deliberate trade:**

- **A small file costs nothing extra**: its blocks are named in the inode, which the kernel has already read.
- **A file over 6 KiB costs one extra block and one extra read** per access past block 11.
- **A file over 70 KiB is impossible.** Real systems add double and triple indirect blocks — a double indirect would take xv6 to 128 × 128 + 140 blocks, about 8 MiB — **or replace the scheme with extents** (L24 §3).

---

## 4. Allocating Blocks and Inodes

**Both allocators are linear scans of a bitmap or table.** `balloc` reads each bitmap block, looks for a zero bit, sets it, **zeroes the data block**, and returns its number. `ialloc` walks the inode table for one whose `type` is 0.

**Two details matter more than they look:**

- **`balloc` zeroes the block before returning it.** Without that, a new file would start with the previous owner's bytes — a file-system-level version of Week 5's uninitialised page, and a straightforward information leak.
- **The bitmap is the truth about free space; the inodes are the truth about what is used.** They can disagree only if something went wrong — which is exactly what `fsck` checks, by walking every inode and comparing (PS 7 Q4).

---

## 5. Directories Are Files

**A directory's data is an array of `struct dirent`**: a 2-byte inode number and a 14-byte name.

```c
struct dirent {
  ushort inum;
  char name[DIRSIZ];   // DIRSIZ is 14
};
```

**`dirlookup` reads the directory like any file and compares names**; an entry with `inum == 0` is free. **Lookup is a linear scan** — a directory of 1,000 files is 16,000 bytes, 32 blocks, read in full for a miss.

**Path resolution is repeated lookup**: `namex` splits `/docs/a.txt` at slashes, starts at the root inode (**always inode 1**), and looks up each element in turn. **Each element costs an inode read plus a scan of that directory.**

**Two consequences worth stating plainly:**

- **A name longer than 14 characters is truncated**, silently, by `strncpy` into a fixed field. Modern file systems store a length (L24 §4).
- **`.` and `..` are ordinary entries**, written when the directory is created. That is why a new directory has a link count of 2 — its name in the parent, and its own `.` — and why the parent's count goes up by one, for the new `..`.

---

## 6. Links: Names Are Not Files

**`link(old, new)` adds a second directory entry pointing at the same inode and increments `nlink`.** There is no "original": both names are equal.

**`unlink` removes an entry and decrements `nlink`. The file's blocks are freed only when the count reaches zero.** In the `myfs` you build in PS 7 — the same design as xv6's — that is visible directly:

```
$ ./myfs test.img link /docs/a.txt /b.txt
link /docs/a.txt /b.txt: inode 3 links 2
$ ./myfs test.img rm /docs/a.txt
rm /docs/a.txt: inode 3 still has 1 links
$ ./myfs test.img rm /b.txt
rm /b.txt: inode 3 freed
```

**Linux adds one more rule**: an open file descriptor counts too, so a file can be unlinked while open and live until the last `close`. **That is how temporary files are made safe** — no name, so nothing else can open it, and it disappears when the program does, crash or not.

---

## 7. The Cost of the Whole Design

**Ask what it costs to read one byte of `/docs/a.txt`**, with nothing cached:

| Step | Reads |
|---|---:|
| root inode | 1 |
| scan root's data for `docs` | 1 or more |
| `docs`'s inode | 1 |
| scan `docs`'s data for `a.txt` | 1 or more |
| `a.txt`'s inode | 1 |
| the data block | 1 |
| | **6 or more** |

**Six disk reads for one byte** — at L23's measured 94 µs each, over half a millisecond. **Two things save it:** the page cache, which makes every repeat free (L23), and a layout that puts these blocks near each other (L24).

**And a seventh read appears for any file past 6 KiB**: the indirect block.

---

## 8. What to Take Away

1. **A name, an inode and the data are three separate things**, joined by an inode number; the inode holds no name.
2. **xv6's disk is five arrays**: boot, superblock, log, inodes, bitmap, data — **59 metadata blocks of 1,000**, everything else found by arithmetic.
3. **Twelve direct addresses and one indirect block cap a file at 71,680 bytes**, measured.
4. **`balloc` zeroes what it hands out**, or files would start with someone else's data.
5. **Directories are files of fixed 16-byte entries**, scanned linearly; paths are repeated lookups; names over 14 bytes are truncated.
6. **Links make names cheap and files independent of them**; the file dies when the last link — and on Linux, the last open descriptor — goes.
7. **Six reads for one byte**, before any caching.

---

## Exercises

1. `IPB` is 8 and inodes start at block 32. **Which block holds inode 100, and at what offset?**
2. A file is 6,656 bytes. **How many blocks does it occupy, including the indirect block?** How many reads to fetch its last byte?
3. **Why does `unlink` not free the inode when `nlink` reaches 0 in Linux, but does in xv6?** What does Linux count that xv6 does not?
4. A directory holds 1,000 entries and the file you want is last. **How many blocks are read by one lookup?** What if the file is not there at all?
5. xv6's `dirlink` scans for a free entry before appending. **What does that cost in a directory where 900 of 1,000 files have been deleted, and what does it save?**

---

*CS 202 · Week 7 · L22 · © CSE Department*
