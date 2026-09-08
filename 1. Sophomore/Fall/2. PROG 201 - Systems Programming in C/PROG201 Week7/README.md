# PROG 201 · Systems Programming in C
## Week 7: Filesystems — VFS, Inodes, and On-Disk Layout

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101; CS 201 as co-requisite
**Assessment for this course (overall):** Problem Sets 35%, Projects 25%, Midterms 25%, Final 15%
**This week's deliverables:** PS 6 (due Friday), PS 7 (released Wednesday, due Friday of Week 8) and **Quiz 7** (Tuesday, covers Week 6).
**Lab 6 is sat on the Monday of this week**; **Lab 7 covers this week and is sat on the Monday of Week 8.**

> ### **Midterm 2 is the Monday of Week 8**, 18:00–19:30, covering **Weeks 4–7**.
> This is the last week of material on it. **Lab 7 is that same afternoon**, ending seventy minutes
> before the paper — the third time this term a lab and a midterm have landed together, and it is
> systematic: this course's midterms and its labs are both on Mondays.
> **Project 1 is due the Friday of Week 9.**

---

### Why This Week Exists

Because you can corrupt one thousand and twenty-four bytes of a filesystem, run `fsck`, get a perfectly clean filesystem back with every file intact — and not one of them will have a name.

Weeks 1 and 4 used files: descriptors, offsets, `mmap`, the page cache. **This week is what is underneath** — the data structure on the disk that all of that has been talking to, and what happens to it when the power goes out.

Three ideas:

1. **An inode does not contain a name.** Names live in directories, a file can have several, and every surprising thing about links, `unlink`, `df` versus `du`, and `lost+found` follows from that sentence.
2. **The VFS is one interface over many implementations** — six filesystem types answered one `statfs` call, two of them with no storage at all.
3. **Consistency and durability are different questions with different answers.** A journal gives you the first in seconds instead of hours. The second costs **154×** and an `fsync` almost everybody forgets.

---

### Learning Objectives

By the end of Week 7, you should be able to:

1. Explain what the VFS is and name its four cached object types.
2. Say why `st_size` is 0 for a file you can read forty bytes from.
3. Describe path resolution, including what `x` on a directory means and when symlinks are followed.
4. Say what `openat` is for — both reasons.
5. Read a `struct stat` correctly: `(st_dev, st_ino)` as identity, `st_blocks` in 512-byte units, and what `st_ctime` actually is.
6. **State the difference between a hard link and a symbolic link**, and predict what happens to each when the target is removed.
7. Explain when `unlink` frees blocks, and diagnose `df` disagreeing with `du`.
8. Say why hard links cannot cross filesystems or point at directories.
9. Describe a directory as a file of records, and why `readdir` has no useful order.
10. **Draw ext2's direct/indirect/double-indirect structure** and compute its addressing limits.
11. Say what an extent is and what problem it solves.
12. Describe a filesystem's on-disk layout, find its backup superblocks, and recover from losing the primary.
13. **Explain what a crash between two metadata writes can leave**, and what a journal does about it.
14. Name the three journalling modes and what each promises.
15. Read `e2fsck`'s five passes and its exit status.
16. **Quantify durability**, choose between `fsync` and `fdatasync`, and write the safe-write pattern with both of its `fsync`s.

---

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L22 The VFS and the POSIX Filesystem API]] | Six filesystems, one `statfs`; **`/proc/self/stat` has size 0 and reads 40 bytes**; the four VFS objects; path resolution; `openat` and TOCTTOU; what is really in `struct stat` |
| [[L23 Inodes Directory Entries and Links]] | **An inode has no name**; hard against symbolic links, measured; `unlink`, link counts and `(deleted)` in `/proc`; **a 14-byte symlink in zero blocks against 75 bytes in one**; directories as records; **ext2's 21 pointer blocks against ext4's two extents** |
| [[L24 On Disk Layout Journalling and Durability]] | Block groups and 11% overhead; **backup superblocks, and recovery from one**; what a crash breaks; **the journal is a file — inode 8, 4 MiB, 6.2%**; three journalling modes; `e2fsck`'s five passes; **durability at 154×**; the directory `fsync` |
| [[LAB 7 Corrupt and Recover a Filesystem]] | Break a real ext4 four ways and repair it, with no root and no mounting. **Monday of Week 8** |
| `lab/mkimage.sh`, `lab/verify.sh` | Build the image; check structure and contents |
| `lab/links.c`, `lab/vfs.c`, `lab/durable.c`, `lab/durable2.c`, `lab/Makefile` | L22–L24's demonstrations, provided complete |
| [[PS 7 A Filesystem in a File]] | Implement `myfs`: superblock, bitmaps, inodes, directories, links, and your own `fsck`. Due **Friday of Week 8** |
| [[PROG201 Week7/assignments/QUIZ 7 Week 7 Tuesday\|QUIZ 7 Week 7 Tuesday]] | Ten minutes, covers **Week 6**, answer key printed |
| [[PROG201 Week7/resources/Reading Guide Week 7\|Reading Guide Week 7]] | APUE Ch. 4, TLPI Ch. 14–18, and **OSTEP 39–42**, which is free and is the implementation half |
| `solutions_instructor/` | Instructor only |

---

### The One Thing to Take From This Week

**`fsck` restores the filesystem. It does not restore your data.**

Two experiments in the lab make the point, and they are opposite failures:

| What you break | What `e2fsck` says | What you actually have |
| --- | --- | --- |
| 1,024 bytes of a **file's data** | **clean, rc=0** | a file of the right size, full of noise |
| 1,024 bytes of the **root directory** | fixed it, **clean** | every file intact in `lost+found`, **no names** |

In the first, the filesystem's invariants all hold and your data is gone. In the second, every byte of every file survived — `#15` is all five million bytes of `huge.bin` — and the thing that was lost was the mapping from names to inodes, which lived in the block you destroyed.

**The names could not be recovered because an inode does not contain a name.** There was nowhere else to look. That is L23 §1 arriving as a consequence rather than as a definition, and it is why backups are not the same thing as a filesystem check.

---

### Assessment Reminder

**Labs and quizzes carry no weight** and are still required. **Quiz 7 is at the start of Tuesday's lecture and covers Week 6**; the answer key is printed in the paper.

**Midterm 2 is the Monday of Week 8, 18:00–19:30, worth 12.5%**, and covers **Weeks 4–7**: `mmap` and allocators, sockets and the C10K problem, the shell and job control, and this week.

> **Lab 6** — Week 6's job control — is sat on the **Monday of this week**. **Lab 7** covers this week
> and is sat on the **Monday of Week 8**, the afternoon of Midterm 2.

Both are tracked in [[_PROG 201 Lab and Quiz Record]].

---

### Connections

**Back:** **Week 1 drew the VFS without naming it** — the descriptor table, the open file description and the inode are three of its four objects. **Week 1's sparse file** is L22 §5's `st_size`/`st_blocks` disagreement, and its `lseek`-then-`write` race is L22 §3's reason for `openat`. **Week 4's page cache** is what `fsync` flushes, and **Week 4's `SIGBUS`** was a mapping outrunning a file. **Week 6's `cd` and `>`** were talking to this all along.

**Sideways:** **CS 201 Week 7 is on storage and I/O**; the block-group locality argument in L24 §1 is its seek-time model with a filesystem built on top.

**Forward:** **Week 8's dynamic linker** reads ELF files through exactly these calls, and `mmap`s them. **Week 9 profiles** I/O properly. **Week 11's containers are overlay filesystems** — two directories stacked with copy-on-write, which is L22 §6's last sentence. **PS 7 is the filesystem you will have read about in OSTEP 40.**

---

*PROG 201 · Week 7 · © CSE Department*
