# PROG 201 · Reading Guide · Week 7
## APUE Chapter 4, and a book about one filesystem

---

**Week 7 splits cleanly in two**, and the two halves have different best sources. The **API** — inodes, links, `stat`, directories — is APUE Chapter 4, which is complete and does not need supplementing. The **implementation** — layout, journalling, crash consistency — is not in any of this course's set texts at the level the lectures use, and the best readings are a book chapter and two papers.

| Source | Read? | Why |
|---|---|---|
| **APUE Ch. 4** | **All of it** | `stat`, links, directories, permissions. This is L22 and L23 |
| **TLPI Ch. 14** | **Read** | Filesystem layout, i-nodes, the VFS. Kerrisk's diagrams are the ones to copy |
| **TLPI Ch. 15** | **Read** | File attributes, and the `atime` discussion L22 §5 refers to |
| **TLPI Ch. 18** | **All of it** | Directories and links. Section 18.3 is L23 §4 |
| **TLPI §13.3** | **Read** | Buffering, `fsync`, `fdatasync`, `O_SYNC`. Six pages, and it is L24 §7 |
| **CS:APP §10.1–10.2** | Skim | Short and clear on the descriptor/inode relationship |
| **OSTEP Ch. 39–42** | **All of it, if you read one thing** | *Operating Systems: Three Easy Pieces*, **free online**. Chapters 39–42 are files, a simple filesystem, FFS, and crash consistency — and 42 is the best explanation of journalling in print |

---

## APUE Chapter 4 — the questions to hold

**§4.2 `stat`, `fstat`, `lstat`**

1. Three calls, one struct. Which one does **not** follow a symlink, and what is the one situation where you must use it?
2. `st_dev` and `st_ino`. Write the one-line predicate for "these two paths are the same file", and say why `st_ino` alone is wrong.

**§4.3–4.9 File types and permissions**

3. Seven file types. Which two are made by `mknod`, and which one did Week 2 make with `mkfifo`?
4. **`x` on a directory.** APUE says what it means. Write down what you can and cannot do with `r-x`, `-wx` and `r--` on a directory, then check by trying it.
5. `st_mode` holds the type and the permissions in one word. Find the mask that separates them.

**§4.12 `st_size` and §4.13 sparse files**

6. Stevens shows a sparse file and the disagreement between `ls -l` and `du`. Week 1 L05 §4 measured 1.1 GB apparent against 4 KB allocated. **Which of `st_size` and `st_blocks` does each command print, and what unit is the second in?**

**§4.14–4.17 Links**

7. He explains why hard links to directories are forbidden and why `link` cannot cross a filesystem. **Both restrictions have the same root cause. What is it?**
8. `unlink` on a file a process has open. Find the sentence, then work out why `df` and `du` can disagree by gigabytes.
9. `rename` is atomic. Find where he says so — then read L24 §8 and work out what "atomic" does **not** promise.

**§4.22 `st_atime`, `st_mtime`, `st_ctime`**

10. Three times, and **one of them is not what its name suggests**. Which, and what actually moves it? Then check what your root filesystem's mount options say about the first one.

---

## OSTEP 39–42 — the implementation half

These are free at `pages.cs.wisc.edu/~remzi/OSTEP/` and are the reading this week's second half is built on.

11. **Ch. 40** builds `vsfs`, a filesystem with a superblock, two bitmaps, an inode table and data blocks. **That is PS 7's layout**, and reading it before you start the problem set is worth an evening.
12. Ch. 40's "reading a file from disk" table counts the I/Os for `open("/foo/bar")` and each `read`. Do the same count for your own PS 7 layout.
13. **Ch. 42, crash consistency.** Work through the three post-crash cases — data without inode, inode without data, bitmap without either — and match them against L24 §3's table.
14. §42.3, "The Crash Consistency Problem", ends by showing why `fsck` is too slow. Then §42.4 is journalling. **Find where it explains why the journal writes a commit block *separately* from the data**, and note the barrier that requires.

---

## The Man Pages for This Week

| Page | The paragraph |
|---|---|
| **`man 5 ext4`** | The mount-options table: `data=journal\|ordered\|writeback`, `noatime`, `barrier` |
| **`man 8 e2fsck`** | **The EXIT CODE section.** Lab 7 Q1 and PS 7 Q4 both turn on it |
| **`man 8 debugfs`** | `stat`, `ls -l`, `dump`, `write`, `ln`. Your filesystem microscope |
| **`man 2 fsync`** | The paragraph about the directory, and the note about error reporting |
| `man 7 path_resolution` | Four pages, and it is L22 §3 written precisely |
| `man 8 dumpe2fs` | For Lab 7 Part A |

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| Card, Ts'o & Tweedie, *Design and Implementation of the Second Extended File System* (1994) | ext2, by the people who wrote it. Twelve pages |
| Mathur et al., *The new ext4 filesystem* (2007) | Extents and delayed allocation, and why |
| McKusick et al., *A Fast File System for UNIX* (1984) | Where block groups came from. Still worth reading |
| Rosenblum & Ousterhout, *The Design and Implementation of a Log-Structured File System* (1992) | The other answer to crash consistency, and the ancestor of every SSD's firmware |
| **Pillai et al., *All File Systems Are Not Created Equal* (OSDI 2014)** | **Measures what real applications assume about `fsync` and `rename`, and finds most of them wrong.** The best paper on L24 §8 |

---

## The Habit for This Week

**Look at the bytes.**

Every previous week's habit was to look at something *outside* your program — the sockets, the process table. This one goes the other way: **the filesystem is a data structure on a disk, and you can read it.**

```bash
dumpe2fs -h img            # the parameters
debugfs -R "stat /file"    # one inode, in full
debugfs -R "ls -l /"       # the directory as records
xxd -s 1024 -l 128 img     # the superblock, byte by byte
e2fsck -fn img             # every invariant, checked
```

Five commands, and between them they show you that there is nothing mysterious in there. A file is an inode; an inode is 256 bytes at a computable offset; a directory is a list of records; a name is a pointer.

**The lab's whole argument depends on it.** When you corrupt 1,024 bytes and every file survives with no name, that is only a surprise until you have looked at where the names were.

---

*PROG 201 · Week 7 · Reading Guide · © CSE Department*
