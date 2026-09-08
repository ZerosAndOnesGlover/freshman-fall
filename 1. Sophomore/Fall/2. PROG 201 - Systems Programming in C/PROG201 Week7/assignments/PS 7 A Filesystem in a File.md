# PROG 201 · Problem Set 7
## A Filesystem in a File

---

**Released:** Week 7, Wednesday · **Due:** Week 8, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS7_{LastName}_{StudentID}.pdf`, and your code as `PS7_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **Midterm 2 is the Monday of Week 8**, covering Weeks 4–7, and **Lab 7 is that same afternoon**.
> This problem set is due four days later, and **Project 1 is due the Friday after that**. Start Q1
> in Week 7 — the layout is an hour's work and everything else depends on it.
>
> Everything compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.
> No external libraries; `open`, `pread`, `pwrite` and `lseek` on one image file.

---

### The Filesystem

You are implementing **`myfs`**, a small Unix-style filesystem living entirely inside one ordinary file. The layout is **specified below and is not yours to choose** — a fixed layout means your image can be inspected, and Q4 asks you to inspect it.

```
block 0        superblock
block 1        inode bitmap   (1 block: one bit per inode)
block 2        block bitmap   (1 block: one bit per block)
blocks 3..K    inode table
blocks K+1..   data blocks
```

**Block size is 4,096 bytes.** All numbers are little-endian and stored as `uint32_t`.

```c
#define BS 4096

struct superblock {         /* block 0, padded to BS */
    uint32_t magic;         /* 0x50524F47 -- "PROG"        */
    uint32_t nblocks;       /* total blocks in the image   */
    uint32_t ninodes;       /* total inodes                */
    uint32_t inode_start;   /* first block of the inode table = 3 */
    uint32_t data_start;    /* first data block            */
    uint32_t root_ino;      /* always 1                    */
};

struct inode {              /* exactly 128 bytes, 32 per block */
    uint32_t mode;          /* 1 = file, 2 = directory, 3 = symlink */
    uint32_t nlink;
    uint32_t size;          /* bytes                        */
    uint32_t direct[8];     /* block numbers, 0 = none      */
    uint32_t indirect;      /* a block of 1024 block numbers */
    uint32_t pad[19];
};

struct dirent {             /* exactly 32 bytes, 128 per block */
    uint32_t ino;           /* 0 = free slot                */
    char     name[28];      /* NUL-padded, not NUL-terminated at 28 */
};
```

**Inode 0 is never used** (so that 0 can mean "none"); **inode 1 is the root directory**.

The tool:

```
./myfs mkfs   img.bin 64           # format a 64 MiB image
./myfs ls     img.bin /            # list a directory
./myfs mkdir  img.bin /docs
./myfs put    img.bin local.txt /docs/note.txt
./myfs get    img.bin /docs/note.txt out.txt
./myfs ln     img.bin /docs/note.txt /alias.txt
./myfs rm     img.bin /alias.txt
./myfs stat   img.bin /docs/note.txt
./myfs fsck   img.bin
```

---

### Q1: The Layout (30 points)

**(a) [10]** `mkfs`. Write the superblock, zero the bitmaps, mark the metadata blocks used, create the root directory with `.` and `..`, and mark inode 0 and inode 1 used.

Size the inode table at **one inode per 16 KiB of image**, rounded up to a whole block. Report, for a 64 MiB image: the inode count, the size of the inode table in blocks, and `data_start`.

**(b) [8]** Work out and state the four limits your layout imposes, with the arithmetic:

| | your answer |
| --- | --- |
| pointers in one indirect block | |
| **largest file** | |
| largest image the block bitmap can describe | |
| entries per directory block | |

**(c) [6]** Bitmap allocation: `alloc_block`, `free_block`, `alloc_inode`, `free_inode`, and a `sync` that writes both bitmaps back.

Say which bit of which byte represents block *n* — get the endianness of the bit order stated explicitly, because Q4's `fsck` and Q1(d)'s hexdump both depend on it.

**(d) [6]** Prove the image is what you say it is: `xxd -l 64 img.bin` after `mkfs`, annotated field by field. Then `xxd` the first inode-table block and point at the root inode.

---

### Q2: Files (26 points)

**(a) [12]** `put`: read a local file and write it into the image. Allocate blocks as needed, fill the 8 direct pointers first, then allocate an indirect block.

**(b) [8]** `get`: read it back. `cmp` the result against the original for a 1-byte file, a 32,768-byte file (exactly the direct pointers), a 32,769-byte file (the first byte of the indirect block), and a 4,000,000-byte file. **Show all four `cmp` results.**

The 32,769-byte case is where implementations break. Say what you got wrong first, or say that you did not.

**(c) [6]** `rm` on a file: decrement `nlink`, and when it reaches zero free every data block **and the indirect block** and free the inode.

Demonstrate that the blocks came back: `fsck` (Q4) reporting free-block counts before and after, or your own count.

---

### Q3: Directories and Links (18 points)

**(a) [8]** `mkdir`, `ls` and path resolution. A path is resolved one component at a time from the root; a component that is not a directory is an error and must say so.

`mkdir` creates `.` and `..` and sets `nlink` correctly. State what the root's `nlink` is after creating two subdirectories, and why.

**(b) [6]** `ln`: a hard link. A second directory entry, the same inode number, `nlink` incremented.

Then answer: **your `ln` cannot link a directory. Enforce that**, and say in one sentence what would break if you allowed it.

**(c) [4]** `stat`: print the inode number, mode, `nlink`, size, and the list of block numbers — the way `debugfs stat` does.

Show `stat` on both names of a hard link and point out the identical parts.

---

### Q4: Your Own `fsck` (14 points)

**(a) [10]** `fsck` checks four invariants and reports, without repairing:

1. the superblock's magic and that the counts are consistent with the image size;
2. **no block belongs to two inodes**, and no in-use block is marked free;
3. every directory entry points at an in-use inode;
4. **every inode's `nlink` equals the number of directory entries pointing at it.**

Report per-check pass/fail plus counts, and **exit non-zero when anything failed** — Lab 7 Q1 is about why that matters.

**(b) [4]** Break your own filesystem three ways with `dd` or a hex editor, and show `fsck` catching each:

- an inode's `nlink` too low;
- a block claimed by two inodes;
- a directory entry pointing at a free inode.

For each, say **which of your four checks caught it** and what a repairing `fsck` would have to decide.

---

### Q5: What You Built, and What You Did Not (12 points)

**(a) [4]** Your inode has 8 direct pointers and one indirect. ext2 has 12 direct and three levels of indirection; ext4 has extents.

Give the largest file each of the three can address at a 4 KiB block size, and say — in one sentence — what problem extents solve that adding a fourth level of indirection would not.

**(b) [4]** Your directory is a linear array of 32-byte records, so lookup is *O(n)* and names are capped at 28 bytes.

Name the two things a real filesystem does differently, and for each say what it costs.

**(c) [4]** **Your filesystem has no journal.** Describe precisely what your image looks like if the machine loses power between your `alloc_block` and your write of the inode that points at it, and again between writing the inode and adding the directory entry.

Which of your four `fsck` checks would notice each? Then say, in one sentence, what a journal would have changed.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The layout | 30 |
| 2 | Files | 26 |
| 3 | Directories and links | 18 |
| 4 | Your own `fsck` | 14 |
| 5 | What you built, and what you did not | 12 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*PROG 201 · Week 7 · PS 7 · © CSE Department*
