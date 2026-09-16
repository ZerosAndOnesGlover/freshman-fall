# CS 202 · Problem Set 7
## `myfs`: a File System on a Disk Image

---

**Released:** Week 7, Wednesday · **Due:** Week 8, Friday 17:00 — **the Friday after Spring Break**
**Total: 100 points** · Submit one PDF, `PS7_{LastName}_{StudentID}.pdf`, plus your `myfs.c` in a tarball `PS7_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **Your `myfs.c` must reproduce every expected output below exactly**, and compile clean under
> `gcc -O2 -Wall -Wextra`.

> **This problem set is released before Spring Break and due the Friday after it.** **Start now**:
> Q1 and Q2 are most of the work, and **PS 8 adds journaling to the file system you write here**, so
> a `myfs` that works is worth more than a `myfs` finished late.

**The file system**, in `assignments/ps7/myfs.c`, is xv6's shape on an image file:

```
 block 0      1         2 .. 17        18        19 .. 2047
 [ unused | superblock | inode table | bitmap | data blocks ]
```

**512-byte blocks; 128 inodes; twelve direct block addresses and one indirect block** of 128 addresses, so a file is at most **140 blocks = 71,680 bytes**; **directory entries are 16 bytes** — a 2-byte inode number and a 14-byte name.

| Provided | Yours to write |
|---|---|
| `bread`, `bwrite`, `iread`, `iwrite`, the `format` command, and the whole command driver | **Q1:** `balloc`, `bfree`, `ialloc` · **Q2:** `bmap`, `itruncate` · **Q3:** `iread_data`, `iwrite_data` · **Q4:** `dirlookup`, `dirlink`, `dirunlink`, `namei` |

**Read the comment above each function**: it specifies exactly what that function must do, including what to return in each error case. The driver's output format is already written, so **if your functions are right, the output matches.**

---

### Q1: Blocks and Inodes (20 points)

**(a) [12]** Implement `balloc`, `bfree` and `ialloc`. Then:

```
$ ./myfs test.img format 2048
formatted 2048 blocks of 512 bytes: superblock 1, inodes 2-17, bitmap 18-18, data 19-2047
128 inodes, 2029 data blocks, max file 71680 bytes
$ ./myfs test.img dump
dump: size 2048 ninodes 128 inodestart 2 bmapstart 18 datastart 19
bitmap: ff ff 1f 00 00 00 00 00  (blocks 0-63)
```

**(b) [4]** **Explain the bitmap bytes** `ff ff 1f`. Which blocks are marked, and why is exactly that set marked immediately after `format`?

**(c) [4]** `format` computes `inodestart`, `bmapstart` and `datastart` from the block count. **Work out, for an image of 100,000 blocks, how many blocks each region takes**, and what fraction of the disk is metadata. **How does that fraction change with the block count, and why?**

---

### Q2: Files (25 points)

**(a) [15]** Implement `bmap` and `itruncate`. Then:

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

*(`mkdir` and `create` need Q4's functions; write them in whichever order you like — the tests are listed in the order the output above was produced.)*

**(b) [5]** **The 8,192-byte file occupies 16 blocks of data but `stat` reports 17.** Explain. At what file size does the count first exceed the data blocks, and by how much can the two differ at most?

**(c) [5]** Write 71,680 bytes, then try 71,681:

```
$ ./myfs test.img write /big 71680 44
write /big: 71680 bytes at 0, size now 71680, 140 blocks
$ ./myfs test.img write /big 71681 44
myfs: file too large
```

**Derive 71,680 from the on-disk structures.** Then: **if you could change one constant to raise the limit, which, and what would the cost be** — in bytes of inode, in blocks per file, and in reads per access?

---

### Q3: Reading and Writing (20 points)

**(a) [12]** Implement `iread_data` and `iwrite_data`, including partial blocks at both ends. Then:

```
$ ./myfs test.img append /docs/a.txt 512 43
append /docs/a.txt: 512 bytes at 8192, size now 8704, 17 blocks
$ ./myfs test.img read /docs/a.txt 8180 40
read /docs/a.txt 8180+40: 40 bytes  42 x12  43 x28
```

**(b) [4]** **That read crossed a block boundary and a write boundary at once.** Say which bytes came from which block, and which `write` or `append` put them there.

**(c) [4]** `iread_data` returns zeros for a block address of 0 — **a hole.** Construct a sequence of `myfs` commands that produces a file with a hole, show `stat`'s block count, and **say how `stat`'s size and block count relate for such a file.** *(Compare L24 §5.)*

---

### Q4: Directories, Names and Links (25 points)

**(a) [15]** Implement `dirlookup`, `dirlink`, `dirunlink` and `namei`. Then:

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

**(b) [5]** **The root directory's link count is 3 and `/docs`'s is 2.** Account for every link to each, by name. **What does creating a directory do to its parent's count, and why does removing a file not change any directory's count?**

**(c) [5]** After the two `rm`s:

```
$ ./myfs test.img df
df: 21 of 2048 blocks used (2027 free), 2 of 127 inodes used
$ ./myfs test.img fsck
fsck: 2 inodes in use, 21 blocks marked, 21 blocks reachable, 0 leaked, 0 used twice, 0 used but not marked
```

**Reproduce both.** Then **make `fsck` report a leak on purpose**: describe a small change to your `rm` that would leave blocks marked but unreachable, and say what `fsck`'s numbers would become. **Do not submit the broken version** — explain it.

---

### Q5: What This Design Costs (10 points)

**(a) [5]** **Count the block reads and writes** your implementation performs for `./myfs img write /docs/a.txt 8192 42`, starting from a file of 100 bytes. Count `bread` and `bwrite` separately, and say which of them a real file system would avoid, and how. *(L23 §1 and L24 §3.)*

**(b) [5]** `dirlookup` scans a directory linearly. **For a directory of 10,000 files, how many blocks does one lookup read on average, and how many for a path of four elements?** Name what ext4 does instead (L24 §4), and **state one thing that answer costs.**

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Blocks and inodes | 20 |
| 2 | Files | 25 |
| 3 | Reading and writing | 20 |
| 4 | Directories, names and links | 25 |
| 5 | What this design costs | 10 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped** — but **PS 8 builds on this code**, so a dropped PS 7 still has to work.

---

*CS 202 · Week 7 · PS 7 · © CSE Department*
