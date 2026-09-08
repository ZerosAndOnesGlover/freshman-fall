# PROG 201 · PS 7 Solutions
## A Filesystem in a File — Instructor Only

---

**Do not distribute.** A reference `myfs` is not provided: the assignment is the implementation, and the layout is specified tightly enough in the paper that every submission is directly comparable.

**On scope:** the curriculum sets "PS 7: Implement a simple file system in C using a disk image file." The layout in the paper is deliberately close to OSTEP Chapter 40's `vsfs` and to ext2's shape, so that a student who read either has a head start and the Lab 7 `debugfs` output is recognisably the same thing.

---

## The Arithmetic Every Answer Depends On

Block size 4,096; 4-byte block numbers; 128-byte inodes; 32-byte directory entries.

| | value |
| --- | --- |
| pointers per indirect block | **1,024** |
| largest file | 8 × 4,096 + 1,024 × 4,096 = **4,227,072 bytes** (4.03 MiB) |
| inodes per inode-table block | **32** |
| objects one bitmap block covers | 4,096 × 8 = **32,768** |
| largest image the block bitmap describes | 32,768 × 4,096 = **128 MiB** |
| entries per directory block | **128** |

For a 64 MiB image at one inode per 16 KiB: **4,096 inodes**, **128 blocks** of inode table, `inode_start` = 3, **`data_start` = 131**.

**Check these first.** A submission whose Q1(b) table disagrees has a layout bug, and everything downstream will be subtly wrong.

---

## Q1 — The Layout (30)

**(a) [10]** Superblock written **[2]**, bitmaps zeroed and metadata marked used **[3]**, root directory with `.` and `..` **[3]**, inodes 0 and 1 marked used **[2]**.

The common error is forgetting to mark the *metadata* blocks used in the block bitmap — blocks 0 through `data_start - 1`. It does not show until the filesystem is nearly full, at which point `alloc_block` hands out the superblock.

**(b) [8]** Two marks per row, and the arithmetic must be shown. See the table above.

**(c) [6]** The four functions **[4]**, the bit-order statement **[2]**.

Any consistent convention is acceptable — the reference convention is that block *n* is bit `n % 8` of byte `n / 8`, least significant bit first, which is what ext2 uses and what `xxd` will let them verify. **The mark is for stating it**, because Q1(d) and Q4 both depend on it and a student who has not written it down usually has two conventions in one program.

**(d) [6]** An annotated `xxd` of the superblock **[4]** and of the root inode **[2]**.

Check the magic reads back as `47 4F 52 50` in the dump — little-endian `0x50524F47`. A student who annotates it as `50 52 4F 47` has hexdumped their expectations rather than their file.

---

## Q2 — Files (26)

**(a) [12]** Direct pointers **[5]**, the indirect block allocated on demand **[5]**, sizes and the inode updated **[2]**.

**(b) [8]** Four `cmp` results **[4]**, the honest report **[4]**.

**The 32,769-byte case is the question.** It is the first byte that needs the indirect block, and the failures are: allocating the indirect block but not zeroing it; treating `indirect` = 0 as a valid block number (which is why block 0 must never be allocatable); and off-by-one in `n < 8 ? direct[n] : indirect[n - 8]`.

"I got it right first time" is acceptable and worth the marks **if the four `cmp`s are shown**. Without the evidence it is [2].

**(c) [6]** `nlink` decremented **[2]**, data blocks freed **[2]**, **the indirect block freed too** **[1]**, evidence **[1]**.

Forgetting the indirect block is the classic leak and their own `fsck` will not catch it — a leaked block is not an inconsistency the paper's four checks look for. **Worth saying so in the feedback**: it is exactly the gap real `fsck` closes with a fifth pass over the bitmaps.

---

## Q3 — Directories and Links (18)

**(a) [8]** `mkdir`, `ls`, resolution **[5]**; `.` and `..` with correct `nlink` **[2]**; the root `nlink` answer **[1]**.

**The root's `nlink` after two subdirectories is 4**: its own `.`, its `..` (which points at itself, since the root is its own parent), and one `..` from each subdirectory. A student who says 3 has forgotten that the root's `..` points at the root.

**(b) [6]** `ln` working **[4]**, the directory restriction enforced **[1]**, the reason **[1]**.

The reason: **a hard link to a directory can create a cycle**, so the tree stops being a tree — `..` no longer has one answer, and any recursive walk can loop for ever. Accept "you could not `fsck` it" as an equivalent.

**(c) [4]** `stat` output **[3]**, the hard-link comparison **[1]**. Everything must be identical except the path they typed — same inode number, same `nlink`, same block list.

---

## Q4 — Their Own `fsck` (14)

**(a) [10]** Four checks at [2] each, plus the non-zero exit **[2]**.

Check 2 is the one that separates submissions. Doing it properly means building a full block map — an array over all blocks, filled by walking every in-use inode's direct pointers, indirect block, **and the indirect block itself** — and then comparing against the bitmap in both directions. A submission that only checks "is this block marked used" catches half of it.

**(b) [4]** Three breakages, one each **[3]**, plus the repair discussion **[1]**.

The repair answers worth noting: for a wrong `nlink`, the count of directory entries is authoritative and the fix is unambiguous — which is why real `fsck` fixes it without asking. For a doubly-claimed block, **there is no safe automatic answer**: `e2fsck` either clones the block or asks. For an entry pointing at a free inode, the entry is deleted, and the file is simply gone.

---

## Q5 — What You Built, and What You Did Not (12)

**(a) [4]** Maximum file sizes at 4 KiB blocks:

| | reaches |
| --- | --- |
| **myfs** (8 direct + 1 indirect) | 4,227,072 bytes ≈ **4 MiB** |
| **ext2** (12 direct + 1 + 2 + 3 indirect) | ≈ **4 TiB** |
| **ext4** (extents) | 16 TiB, and the limit is elsewhere |

The one-sentence answer about extents: **a fourth level of indirection would extend the range but not reduce the number of accesses or the metadata per byte** — extents make a contiguous run cost one 12-byte record regardless of length, which is a different axis. Accept any answer distinguishing *reach* from *cost per byte*.

**(b) [4]** Two of: **hashed or B-tree directories** (ext4's `dir_index`) — costs an index to maintain and makes `readdir` order meaningless; **variable-length entries** — costs a scan to find a free slot of the right size and produces fragmentation within the block; **the record-length trick for deletion** — costs directories that never shrink.

**(c) [4]** The two crash windows **[2]**, which check catches each **[1]**, the journal sentence **[1]**.

- Crash after `alloc_block`, before the inode write: **a block marked used that no inode points at** — a leak. **None of their four checks catches it**, which is worth pointing out.
- Crash after the inode, before the directory entry: **an inode with `nlink` = 1 and no entry pointing at it** — an orphan. **Check 4 catches it**, and this is what `lost+found` is for.

The journal sentence: it would have made both windows atomic — either the whole operation is in the log and gets replayed, or none of it is and nothing happened.

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

---

*PROG 201 · Week 7 · PS 7 Solutions · Instructor Only · © CSE Department*
