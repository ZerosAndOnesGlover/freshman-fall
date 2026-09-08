# PROG 201 · Lab 7
## Corrupt and Recover a Filesystem
### Covers Week 7 · sat **Monday of Week 8**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 7 and is sat in Week 8.** Lab *N* is sat on the Monday of Week *N+1*.
>
> **Midterm 2 is the same day**, 18:00–19:30, covering **Weeks 4–7** — this lab ends at 16:50 and
> the paper starts seventy minutes later. That is the third time this term a lab and a midterm have
> landed together, and it is systematic rather than accidental: this course's midterms are on
> Mondays and so are its labs. **Come having revised.** [[PROG 201 Scheduling Notes]] records it.
>
> **Unmarked.** The TA checks your work off in the session.

**What you are building:** confidence about what `fsck` can and cannot give you back.

You will make a real ext4 filesystem, break it four ways, and repair it — **without root and without ever mounting anything.** `mke2fs`, `debugfs`, `dumpe2fs` and `e2fsck` all work perfectly well on an ordinary file; only `mount` needs privileges, and nothing here needs `mount`.

The fourth corruption is one 1,024-byte block. **Every file survives it and every name is lost**, and working out why that had to happen is the point of the session.

---

## 0. Setup (5 minutes)

```bash
mkdir -p "$PROG201/week7/lab7"        # $PROG201 is set in ~/.bashrc -- see Lab 0
cd "$PROG201/week7/lab7"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week7/lab/"{mkimage.sh,verify.sh,links.c,vfs.c,durable.c,durable2.c,Makefile} .
chmod +x mkimage.sh verify.sh

make
./mkimage.sh disk.img 64
./verify.sh disk.img
```

You should see `all checks passed`. **Keep a pristine copy** — you will want it four times:

```bash
cp disk.img pristine.img
```

`mkimage.sh` builds a 64 MiB ext4 filesystem with **1 KiB blocks** — small blocks so that indirect blocks and extents are visible on files you can create in a second. `verify.sh` runs `e2fsck -fn` for structure and eight `debugfs` checks for contents. **Read both scripts**; neither is long, and Q1 asks about one line of `verify.sh`.

---

## 1. Part A — Look Before You Break (25 min)

**(a) The layout.**

```bash
dumpe2fs -h disk.img
dumpe2fs disk.img | grep -iE "superblock at|Inode table at|Block bitmap at" | head -6
```

Write down: the block size, the inode count, the block count, **the block numbers of all the backup superblocks**, and where group 0's inode table starts. You will need the superblock list in Part B.

**(b) The inodes.** Compare a hard link, a short symlink and a long one:

```bash
debugfs -R "ls -l /"        disk.img
debugfs -R "stat /alias.txt"    disk.img
debugfs -R "stat /link.txt"     disk.img
debugfs -R "stat /longlink.txt" disk.img
```

Three things to note, because Q2 asks:

- `/docs/note.txt` and `/alias.txt` have the **same inode number** and `Links: 2`;
- `/link.txt` has `Blockcount: 0` and a line saying `Fast link dest:`;
- `/longlink.txt` has `Blockcount: 2` and an `EXTENTS:` line.

**(c) Where the data is.** ext4 uses extents; ext2 uses indirect blocks. Build an ext2 image and compare the same file:

```bash
dd if=/dev/zero of=ext2.img bs=1M count=64 status=none
mke2fs -q -t ext2 -b 1024 -F ext2.img
head -c 5000000 /dev/urandom > huge.bin
debugfs -w -R "write huge.bin huge.bin" ext2.img

debugfs -R "stat /huge.bin" ext2.img    # (0-11), (IND), (DIND), ...
debugfs -R "stat /huge.bin" disk.img    # EXTENTS: two records
```

**Count the pointer blocks in the ext2 version.** `TOTAL:` minus the number of data blocks is the answer, and Q3 wants both numbers.

**(d) The journal.**

```bash
dumpe2fs -h disk.img | grep -i journal
debugfs -R "stat <8>" disk.img | head -4
```

The journal is a **file**. Note its size, and what fraction of a 64 MiB filesystem it is.

---

## 2. Part B — Four Corruptions (45 min)

**Restore from `pristine.img` before each one.** Run `./verify.sh` after every repair.

### (1) The superblock

```bash
cp pristine.img sb.img
dd if=/dev/zero of=sb.img bs=1024 seek=1 count=1 conv=notrunc status=none
dumpe2fs -h sb.img            # "Bad magic number in super-block"
```

Recover it. `e2fsck` will find a backup by itself; do it **explicitly** with `-b` and one of the block numbers from Part A(a), so that you know which one you used.

```bash
e2fsck -fy -b 8193 sb.img
./verify.sh sb.img
```

**Everything should come back.** Q4.

### (2) The link count

`debugfs`'s `ln` creates a directory entry and does **not** update the inode's link count — which is exactly the inconsistency a half-completed metadata write produces.

```bash
cp pristine.img lc.img
debugfs -w -R "ln /docs/note.txt /second.txt" lc.img
e2fsck -fn lc.img ; echo "rc=$?"
e2fsck -fy lc.img ; echo "rc=$?"
```

**Record both exit statuses.** They are different and they both mean something — `man 8 e2fsck`, EXIT CODE. Which pass caught it? Q5.

### (3) A data block

```bash
cp pristine.img data.img
BLK=$(debugfs -R "stat /big.bin" data.img 2>/dev/null | grep -A1 EXTENTS | tail -1 | sed 's/.*://; s/-.*//')
echo "corrupting block $BLK"
dd if=/dev/urandom of=data.img bs=1024 seek=$BLK count=1 conv=notrunc status=none
e2fsck -fn data.img ; echo "rc=$?"
./verify.sh data.img
```

**Read that output carefully before moving on.** Q6, and it is the most important question on the sheet.

### (4) One directory block

```bash
cp pristine.img dir.img
RB=$(debugfs -R "stat <2>" dir.img 2>/dev/null | grep -A1 EXTENTS | tail -1 | sed 's/.*://')
echo "corrupting the root directory's block $RB"
dd if=/dev/urandom of=dir.img bs=1024 seek=$RB count=1 conv=notrunc status=none
e2fsck -fn dir.img 2>&1 | head
e2fsck -fy dir.img 2>&1 | head -20
./verify.sh dir.img
debugfs -R "ls /" dir.img
debugfs -R "ls -l /lost+found" dir.img
```

Ours:

```
=== structure ===
  ok    e2fsck: clean
=== contents ===
  FAIL  /docs/note.txt exists
  FAIL  /alias.txt exists
  ... 8 check(s) failed

$ debugfs -R "ls /" dir.img
 2  (12) .    2  (12) ..    18  (988) lost+found

$ debugfs -R "ls -l /lost+found" dir.img
     11   40700 ...  #11
     12   40755 ...  #12
     14  100664 ... 200000  #14
     15  100664 ... 5000000  #15
```

**The filesystem is clean and every file is intact — `#15` is all five million bytes of `huge.bin` — and not one of them has a name.** Q7 and Q8 are about that, and they are the lab.

---

## 3. Part C — Durability (20 min)

`fsck` is about the filesystem's consistency. This is about your data.

```bash
./durable
./durable2
```

Ours:

```
200 records of 4096 bytes
  write only, one fsync at the end        0.005 s   0.02 ms per record   41980 rec/s
  write + fdatasync every record          0.733 s   3.67 ms per record     273 rec/s
  write + fsync every record              0.783 s   3.91 ms per record     255 rec/s

overwrite in place, 200 records (size never changes)
  fsync every record                      4.11 ms each
  fdatasync every record                  1.26 ms each

the safe-write pattern, 50 times
  write, fsync, rename                    4.17 ms each
  write, fsync, rename, fsync the directory  8.05 ms each
```

Three things to explain, and Q9 and Q10 ask for two of them:

- the **154×** between buffered and durable;
- why `fdatasync` is barely faster when **appending** and 3.3× faster when **overwriting**;
- why the directory `fsync` is there at all, given that `rename` is atomic.

Also run `./links` and `./vfs` — they are L22 and L23's demonstrations and take ten seconds each. `./links` step 4 is the one to look at.

---

## 4. Questions

Answer in the answer sheet. Three or four sentences each unless stated.

**Q1.** `verify.sh` calls `e2fsck -fn` and treats **rc=4** as a failure but **rc=1** as something else. Look up both. Why would a checking script want to use `-n`, and what would `-p` be for?

**Q2.** `/link.txt` uses **zero blocks** and `/longlink.txt` uses one. Give the rule, the approximate threshold, and where in the inode the short target is stored.

**Q3.** Report the ext2 numbers for `huge.bin`: data blocks, `TOTAL`, and therefore pointer blocks. Then say how many disk accesses are needed to reach the **last** byte of that file on ext2, and how many on ext4.

**Q4.** After you zeroed the primary superblock, every file came back. Say what a superblock actually contains, and why losing it does not lose any data.

**Q5.** Give both `e2fsck` exit statuses from corruption (2), say what each means, and name the pass that found the problem. Then say which of the five passes would catch a block belonging to two different files.

**Q6.** In corruption (3) you replaced 1,024 bytes of a file's data with random noise. **What did `e2fsck` say, and what does that tell you about what a filesystem check is for?** *(One paragraph. This is the question.)*

**Q7.** In corruption (4), every file survived and every name was lost. Explain why the names could not be recovered — your answer must refer to what an inode does and does not contain.

**Q8.** `lost+found` contained `#11`, `#12`, `#14`, `#15`. Where do those numbers come from, and what would you do next if this were a filesystem you cared about? *(Be specific: name a command.)*

**Q9.** Explain the 154×. Then say what a database does to get durability without paying it per record — name the technique.

**Q10.** `rename` is atomic, so why does the safe-write pattern need an `fsync` on the **directory**? Say exactly what can be lost without it, and what the extra 4 ms is buying.

---

## 5. Checkoff

Show the TA:

- [ ] `./verify.sh sb.img` passing after you recovered from a backup superblock.
- [ ] Corruption (3): `e2fsck` reporting a clean filesystem, and you saying why.
- [ ] Corruption (4): `lost+found` full of numbered files, and Q7 answered out loud.
- [ ] Your written answers to **Q6, Q7 and Q10**.

**If you finish early:** work out how to get the names back in corruption (4) *if* you had made a copy of the directory block first — then do it with `dd` and `verify.sh`. That is what a backup of a filesystem's metadata is, and it is what `e2image -r` produces.

**Take with you:** **Midterm 2 is tonight**, 18:00–19:30, Weeks 4–7. **PS 7 is due Friday** — it is a filesystem of your own in a disk image, and Part A's `debugfs` output is the shape you are implementing. **Project 1 is due Week 9.**

---

*PROG 201 · Week 7 · Lab 7 · © CSE Department*
