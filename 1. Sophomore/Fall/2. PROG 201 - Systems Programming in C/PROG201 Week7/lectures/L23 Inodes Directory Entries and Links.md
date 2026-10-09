# PROG 201 · Systems Programming in C
## Week 7 · Lecture 2 of 3
### Inodes, Directory Entries, and Links

*“We have persistent objects, they're called files.”* — Ken Thompson, Plan 9 fortune file (1992)

---

**Reading:** APUE §4.14–4.17 · TLPI Ch. 18 · CS:APP §10.2 · `man 2 link`, `man 7 symlink`, `man 8 debugfs` · **Previous:** L22 · **Next:** L24 — on-disk layout, journalling and durability

**Coursework:** 📝 **PS 7** released today, due Fri of Week 8 17:00 · 📝 **PS 6** due Fri this week 17:00 · 🔬 **Lab 7** Mon of Week 8 15:00–16:50 · 📊 **Quiz 8** Tue of Week 8

---

## 1. An Inode Does Not Contain a Name

This is the sentence the week is built on, and everything surprising follows from it.

**A file is an inode.** It has an owner, permissions, timestamps, a size, a link count, and pointers to its data. It does **not** have a name — names live in *directories*, which are files whose contents are a list of (name → inode number) pairs.

So a name is a pointer to a file, and there can be several. `links.c` makes one file and three names on the real filesystem:

```
1. one file, three names:
  a.txt        - inode 3539906   links 2   size 9
  b.txt        - inode 3539906   links 2   size 9
  s.txt        l inode 3539907   links 1   size 5        -> a.txt
```

**`a.txt` and `b.txt` are the same inode.** Not copies — the same file, with `links 2` recording that two directory entries point at it. `s.txt` is a **different inode** whose contents are the five characters `a.txt`.

Remove the original name:

```
2. remove the ORIGINAL name:
  a.txt        No such file or directory
  b.txt        - inode 3539906   links 1   size 9
  s.txt        l inode 3539907   links 1   size 5        -> a.txt   (DANGLING)
```

**The hard link is still a complete file** — the link count dropped to 1 and nothing else changed. There is no "original"; `a.txt` was never more real than `b.txt`. The **symlink is now dangling**, because it holds a *name*, and that name no longer resolves.

That is the whole difference, and it is worth stating in one line: **a hard link is another name for the file; a symbolic link is a file containing a name.**

---

## 2. What Is Actually In One

`debugfs` prints an ext4 inode directly. This is a 18-byte file:

```
Inode: 13   Type: regular    Mode:  0664   Flags: 0x80000
User:     0   Group:     0   Project:     0   Size: 18
Links: 2   Blockcount: 2
 ctime: ... atime: ... mtime: ... crtime: ...
Size of extra inode fields: 32
Inode checksum: 0x9b5cc064
EXTENTS:
(0):4386
```

Everything `stat` shows you, plus three things it does not:

- **`crtime`** — ext4 records creation time, and POSIX has no call for it. `statx(STATX_BTIME)` is Linux's way to read it.
- **`Inode checksum`** — ext4 checksums its own metadata (`metadata_csum`), so a corrupted inode is detected rather than believed.
- **`EXTENTS`** — where the data is. §6.

**`Blockcount: 2` for an 18-byte file**, in 512-byte units, is one 1 KiB block. The smallest file that has any content costs a whole block; a filesystem full of 18-byte files wastes 98% of itself, which is why small-file workloads want a small block size and everything else wants a large one.

---

## 3. A Directory Is a File Full of Names

A directory's *data* is a list of records: an inode number, a record length, a name length, a file type, and a name. `readdir` hands them to you one at a time (L22 §4).

Three properties that follow from it being an ordinary file:

**Deleting a name does not shrink the directory.** ext4 marks the record free by extending the previous record's length over it. A directory that once held ten thousand files stays large, and `ls` of an empty-but-once-huge directory is slow. `e2fsck -D` re-optimises; on ext4 you otherwise create a new directory and move things.

**`.` and `..` are real entries.** `.` points at the directory itself and `..` at its parent — which is why an empty directory has `st_nlink` of **2** (its name in the parent, plus its own `.`) and a directory with *n* subdirectories has *n* + 2.

**Lookup was linear and now is not.** ext2 scanned the directory for each name — *O(n)*, which made a 100,000-entry directory unusable. ext4's `dir_index` feature keeps a hashed B-tree (an "htree") keyed on the name hash, and it is on by default:

```
Filesystem features:  has_journal ext_attr resize_inode dir_index filetype extent ...
```

**That is why `readdir` returns entries in no useful order**: on an indexed directory, the order is hash order. Code that assumes alphabetical, or creation order, works on small directories and breaks on large ones, which is the worst possible failure schedule.

---

## 4. Hard Links, Precisely

```c
link("a.txt", "b.txt");        /* another entry, same inode, count++ */
unlink("a.txt");               /* remove an entry, count-- */
```

**`unlink` does not delete a file.** It removes a name and decrements the count. The inode and its blocks are freed when **two** conditions hold: the link count is zero **and** no process has it open.

The second half is Week 1's open-then-unlink trick, and `links.c` shows what it looks like from outside:

```
4. open, then unlink the last name:
  b.txt        No such file or directory
   still readable through the descriptor: the data
   /proc/self/fd/3 -> /tmp/.../links/b.txt (deleted)
```

**The name is gone, the data is not, and `/proc` says `(deleted)`.** This is how a temporary file that cannot be left behind is made, how a program deletes its own executable while running, and — the operational version — **why deleting a large log file does not free any disk space while the process that opened it is still running.** `lsof | grep deleted` is the standard way to find that, and `df` disagreeing with `du` is the symptom.

Two rules about what may be linked:

```
5. what you may and may not hard-link:
   link to a directory : Operation not permitted
   symlink to a directory: allowed
```

**Hard links to directories are forbidden** (`EPERM`), because they would let you make a cycle in what is supposed to be a tree — and `..` would no longer have one answer. Only `.` and `..` are exceptions, and they are made by the filesystem, not by you.

**Hard links cannot cross filesystems**, and fail with `EXDEV`. An inode number is only meaningful within its filesystem (L22 §5), so a directory entry on one filesystem cannot name an inode on another.

---

## 5. Symbolic Links, Fast and Slow

A symlink is an inode whose "data" is a path. And ext4 has two ways to store it, which you can see:

```
Inode: 15   Type: symlink   Size: 14   Blockcount: 0
Fast link dest: "/docs/note.txt"

Inode: 16   Type: symlink   Size: 75   Blockcount: 2
EXTENTS:
(0):4583
```

**A 14-byte target lives inside the inode itself, using zero blocks.** ext4 stores short targets in the 60 bytes that would otherwise hold block pointers — a "fast symlink". A 75-byte target does not fit, so it gets a data block like any other file.

**Sixty bytes is the threshold** on ext4, and it is why `ls -l` on a directory of short symlinks touches no data blocks at all.

What a symlink buys and costs, against a hard link:

| | hard link | symlink |
| --- | --- | --- |
| Points at | an **inode** | a **path** |
| Crosses filesystems | no (`EXDEV`) | **yes** |
| To a directory | no (`EPERM`) | **yes** |
| Survives the target being renamed | **yes** — it is the file | no — dangles |
| Survives the target being deleted | **yes** | no — dangles |
| Costs | one directory entry | an inode, and a lookup per traversal |
| Visible as a link | **no** — indistinguishable | yes, `S_ISLNK` |

**The last row is the one that matters in practice.** You cannot tell by looking at `b.txt` that it is "a link"; it is just a name. `ls -l` shows `links 2` and nothing about *where* the other name is — finding it means searching the filesystem for the inode number (`find / -inum N`).

---

## 6. Where the Data Is: Indirect Blocks

An inode has room for a fixed number of block pointers, and files are larger than that. ext2's answer — which is the classic Unix answer, from 1974 — is **12 direct pointers, then one indirect, then double, then triple.**

`debugfs` on an ext2 image with 1 KiB blocks. A 15,000-byte file:

```
(0-11):786-797, (IND):798, (12-14):799-801
TOTAL: 16
```

**Twelve direct blocks, then an indirect block, then the rest.** Block 798 is not data — it is 1,024 bytes of block numbers.

A 5,000,000-byte file:

```
(0-11):882-893, (IND):894, (12-267):895-1150,
(DIND):1151, (IND):1152, (268-523):1153-1408, (IND):1409, (524-779):1410-1665,
... 17 more IND blocks ...
TOTAL: 4904
```

Read the arithmetic off it: a 1 KiB block holds **256** four-byte pointers, and indeed each `(IND)` covers exactly 256 blocks — `(12-267)` is 256 of them. When one indirect block runs out, a **double indirect** block appears: a block of pointers to blocks of pointers.

The addressing limits, with 1 KiB blocks:

| | reaches |
| --- | --- |
| 12 direct | 12 KiB |
| + single indirect (256) | 268 KiB |
| + double indirect (65,536) | 64 MiB |
| + triple indirect (16,777,216) | **16 GiB** |

**That is ext2's maximum file size at this block size**, and it is why 4 KiB blocks became universal — the same structure reaches 4 TiB.

And the overhead is real: the 5 MB file used **4,883 data blocks and 4,904 total — 21 blocks of pointers.** Under half a percent, which is fine; the cost that hurts is not space but **seeks**: reading byte 4,000,000 means reading the inode, a double indirect block, an indirect block, and then the data. **Four accesses to reach one.**

---

## 7. Where the Data Is: Extents

ext4 replaced all of that. The same 5,000,000-byte file, on ext4:

```
EXTENTS:
(0-3608):4584-8192, (3609-4882):8451-9724
```

**Two records for the whole file, and zero pointer blocks.** An extent is `(logical range) → (physical start)`, so a contiguous run of any length costs one 12-byte record. Four fit in the inode; beyond that ext4 builds a B-tree of them.

The comparison, same file, same block size:

| | ext2 | ext4 |
| --- | --- | --- |
| Structure | 12 direct + IND + DIND + 19 IND | **2 extents** |
| Pointer blocks | 21 | **0** |
| Accesses to reach the last byte | 4 | **1** |

And the earlier 200,000-byte file was a **single** extent, `(0-195):4387-4582` — 196 consecutive blocks, described in twelve bytes.

**Extents work because allocation is contiguous, and it is contiguous because ext4 delays it.** Rather than allocating a block per `write`, ext4 keeps the data in the page cache and allocates when it flushes, by which time it knows how big the file is. That is **delayed allocation**, it is the reason extents are short, and it is also why a crash can lose a file that `write` returned success for — which is L24.

---

## Summary

- **An inode does not contain a name.** A directory maps names to inode numbers, and a file can have several names.
- **A hard link is another name for the file; a symlink is a file containing a name.** Delete the first name and the hard link is a complete file while the symlink dangles.
- `unlink` removes a name and decrements a count. **The blocks are freed when the count is zero *and* nobody has it open** — which is why deleting a log file frees no space while a process holds it, and `/proc/pid/fd` says `(deleted)`.
- **Hard links cannot cross filesystems (`EXDEV`) or point at directories (`EPERM`).** Symlinks can do both.
- ext4 stores a symlink target **inside the inode** if it fits in 60 bytes — measured: 14 bytes and **zero blocks**, against 75 bytes and one block.
- A directory is a file of records; **deleting a name does not shrink it**, `.` and `..` are real entries, and `dir_index` makes `readdir`'s order a hash order.
- **ext2: 12 direct, then indirect, double, triple.** 256 pointers per 1 KiB block; 16 GiB maximum file; **21 pointer blocks** for a 5 MB file and four accesses to reach the last byte.
- **ext4: extents.** The same file in **two records and no pointer blocks**, because delayed allocation makes the data contiguous.

---

## Exercises

1. Make a file, hard-link it twice, and find all three names from the inode number alone. Which command, and how long does it take on a real filesystem?
2. Create a symlink whose target is 59 characters and one whose target is 61. Check `Blockcount` for both with `debugfs` or `stat`. Where exactly is the boundary?
3. `df` and `du` on a filesystem where a process holds a deleted 1 GiB file open. Reconcile them, then find the process.
4. `ln -s a b; ln -s b a`, then `cat a`. Which `errno`? Now make a chain of 39 and 41 links and find the real limit.
5. Make a directory with 100,000 files, delete them all, and time `ls` on the now-empty directory against a fresh one. Explain the difference.
6. Write a 5 MB file to an ext2 image and to an ext4 image and compare `debugfs stat` on both. Count the pointer blocks in each.
7. With 4 KiB blocks, redo §6's table. What is ext2's maximum file size, and what does that tell you about why 1 KiB blocks disappeared?

---

*PROG 201 · Week 7 · L23 · © CSE Department*
