# CS 202 · Operating Systems
## Week 8 · Lecture 1 of 3
### Crash Consistency: What Tears

*“In computing, the mean time to failure keeps getting shorter.”* — Alan Perlis, "Epigrams on Programming" (1982), #98

---

**Sat:** Monday of Week 8, 09:00–09:50, VNC 101, **after Quiz 8** — and **Midterm 2 is this evening**, 18:00–19:15, VNC 100, on Weeks 4–7 · **Reading:** OSTEP Ch. 42 · **Next:** L26, journaling

**Coursework:** 📊 **Quiz 8** today · 📘 **Midterm 2** today 18:00–19:15 · 🔬 **Lab 7** Tue this week 15:00–16:50 · 📝 **PS 8** released Wed this week, due Fri of Week 9 17:00 · 📝 **PS 7** due Fri this week 17:00

> **Nothing in this week is on tonight's paper.** It covers Weeks 4–7. **PS 7 is due Friday**, and
> this lecture is the reason PS 8 exists.

---

## 1. One Operation, Several Blocks

**Creating a file in `myfs` changes four things on disk**: the inode's `type` (allocating it), the directory's data block (the new entry), the directory's inode (its size), and — for a file with contents — the bitmap and the data blocks.

**The disk applies one block write at a time**, and L23 §3 showed that the kernel decides the order, not the program. **A crash between any two of them leaves the disk in a state no operation ever intended.**

**The states a torn `create` can leave:**

| Written before the crash | What the disk holds |
|---|---|
| nothing | the old file system — fine |
| the inode only | **an inode marked in use that no name reaches** — lost forever |
| the directory entry only | **a name pointing at a free inode** — opening it reads garbage |
| both, not the directory's size | the entry is beyond the directory's recorded size: **invisible, but its inode is used** |
| everything | the new file system — fine |

**Two of those five are not "a bit of lost work". They are a file system that lies about itself**, and every later operation builds on the lie.

---

## 2. Measured: What Actually Tears

**`myfs` writes every block through one function**, so it can be stopped after exactly *n* writes — a power failure, simulated exactly. `crashsweep.sh` does that for every *n*, and checks the image afterwards with a stronger `fsck` than PS 7's: one that also finds **orphaned inodes** (in use, named by nothing) and **leaked blocks** (marked in the bitmap, reachable from nothing).

**Without a journal:**

| Operation | Writes to complete | Crash points | Left the old state | Left the new state | **Inconsistent** |
|---|---:|---:|---:|---:|---:|
| `create /d/y` | 3 | 2 | 0 | 0 | **2 — both orphan an inode** |
| `write /d/x 8192` | 92 | 91 | 57 | 0 | **34 — leaked blocks** |

**Thirty-six of ninety-three crash points left a broken file system**, and **not one left the completed operation**: an interrupted `write` is never the new file, because the last write is the one that would have made it so.

**One of them, in full:**

```
$ ./myfs t.img crash 30 write /d/x 8192 43
myfs: crashed after 30 writes
$ ./myfsj t.img fsck
fsck: 3 inodes in use, 26 blocks marked, 25 reachable, 1 leaked, 0 used twice, …
$ ./myfs t.img stat /d/x
stat /d/x: inode 3 file links 1 size 2048 blocks 4
```

**The bitmap says 26 blocks are in use; the inodes reach 25.** One block is allocated to nobody — `balloc` marked it and the crash came before the inode that would have pointed at it. **The file system is not corrupt in any way a program would notice today**, and it has just lost a block permanently. Do that a thousand times and the disk is full of nothing.

---

## 3. Why Ordering Alone Does Not Save You

**The obvious fix is to choose the order**: write the data block, then the bitmap, then the inode, then the directory entry — so that every intermediate state is at worst wasteful, never wrong. **That is what "soft updates" does**, and it works, at the cost of tracking dependencies between every pair of blocks in the buffer cache.

**But the file system does not control the order in which its writes reach the platter.**

- **The page cache holds dirty blocks** and writes them back in whatever order suits it (L23 §3) — by index, by locality, in bulk.
- **The drive reorders too**, and acknowledges into its own cache (L23 §4).
- **The only ordering primitive is a flush** — `fsync`, or the kernel's FUA/flush requests — and **each one costs about 4 ms** (L23 §4). An order with *k* constraints costs *k* flushes.

**So ordering is not free, and correctness by ordering alone is fragile**: one reordered write, one drive that lies about its cache, and the invariant is gone.

---

## 4. `fsck`: Repair After the Fact

**The old answer was to check the whole disk after every crash.** `fsck` walks every inode, builds its own picture of which blocks and inodes are in use, and compares it with the bitmaps — exactly what `myfs`'s `fsck` command does, and what `e2fsck` does on ext4:

```
$ e2fsck -fn corrupt.img
e2fsck: Inode checksum does not match inode while reading bad blocks inode
```

**What it can do:** free leaked blocks, clear inodes nothing points to, fix link counts, fix a size that disagrees with the blocks.

**What it cannot do:** know what you meant. **A half-written file is repaired into a consistent file with garbage in it** — consistent is not correct. And an entry naming a freed inode can only be deleted.

**What it costs: the whole disk.** The check above took under a second on a 32 MiB image; **on a 4 TB file system it is hours**, during which the machine is unavailable. **That is the reason journaling exists** — not that `fsck` cannot repair, but that nobody can wait for it.

---

## 5. What We Actually Want

**Atomicity, for a group of block writes**: either all of them take effect or none does — the same property Week 3 wanted for a group of instructions, one level down.

**The disk offers exactly one atomic operation: a single block write.** Everything else must be built from it. **The trick, which L26 measures, is to make one block write the moment the operation becomes real** — write everything somewhere else first, then flip one block to say "it counts".

**The same idea appears three times in this course:**

| | The atomic flip |
|---|---|
| **Journaling** (L26) | the log's commit record |
| **Copy-on-write** (L27) | the new superblock pointing at the new tree |
| L23 §5's safe update | `rename`, which replaces one directory entry |

---

## 6. What to Take Away

1. **One file-system operation is several block writes**, and a crash between them leaves a state no operation intended.
2. **Measured, without a journal: 36 of 93 crash points left `myfs` inconsistent** — orphaned inodes and leaked blocks — **and none left the finished operation.**
3. **Choosing the write order helps, but the file system does not control the order** that reaches the disk: the page cache and the drive both reorder, and the only fix is a flush at ~4 ms each.
4. **`fsck` repairs consistency, not correctness**, and costs a scan of the whole disk — hours on a real one.
5. **What is wanted is atomicity for a group of writes**, and the only atomic unit available is one block. **Everything in the next two lectures is built from that.**

---

## Exercises

1. For the four writes of a `create` (inode, entry, directory size, bitmap), **enumerate all orders** and mark which leave a state `fsck` can repair without losing data.
2. **Why did no interrupted `write` leave the new state**, in §2's table? What would have to be different for one to?
3. A drive acknowledges writes into a volatile cache and reorders them. **Your file system writes A, then flushes, then writes B.** What exactly is guaranteed, and what is not?
4. `fsck` finds an inode with `nlink` 2 but only one directory entry naming it. **Which is more likely to be right, and what should `fsck` do?**
5. §5 lists three atomic flips. **For `rename`, what makes it atomic** — what single block changes, and what happens if the crash lands just before it?

---

*CS 202 · Week 8 · L25 · © CSE Department*
