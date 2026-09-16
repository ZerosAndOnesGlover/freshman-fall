# CS 202 · Problem Set 8 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 8.** The journal is 60 lines and either works or does not — **the sweep in Q3 is the test, and it is binary**: a correct implementation has **zero** inconsistent crash points. **Put the marks on Q3, Q4 and Q5**, where the student has to explain what the sweep shows.

**References in this folder:** `myfsj reference (do not distribute).c` (the five functions filled in) and `myfs without a journal, with crash (do not distribute).c` (PS 7's file system with the same crash simulator, for Q3(c)). Both compile with no compiler output, as does the student skeleton.

All figures below are from the reference machine.

---

## Q1: The Log (30 points)

### Reference implementations

```c
static void write_head(void)
{
    char blk[BSIZE] = { 0 };
    memcpy(blk, &lh, sizeof lh);
    raw_write(LOGHDR, blk);
}

static void log_write(uint32_t b, const void *buf)
{
    if (!in_op) die("log_write outside an operation");
    uint32_t i;
    for (i = 0; i < lh.n; i++)
        if (lh.block[i] == b) break;          /* absorption */
    if (i == NLOG) die("log full");
    raw_write(LOGSTART + i, buf);
    lh.block[i] = b;
    if (i == lh.n) lh.n++;
}

static void end_op(void)
{
    if (!in_op) die("end_op outside an operation");
    if (lh.n > 0) {
        write_head();          /* the commit */
        install_blocks();
        lh.n = 0;
        write_head();          /* done */
    }
    in_op = 0;
}
```

### (a) [20]

Output as printed in the handout. **[15]** for the four commands, **[5]** for `fsck` and `logdump`.

**The two bugs that pass casual testing and fail Q3:**

| Bug | Symptom |
|---|---|
| `end_op` installs **before** writing the header | Q3(a) shows inconsistent crash points in the install window — the classic failure, and the whole point of the question |
| `log_write` appends without scanning (no absorption) | `write /d/x 8192` dies with `log full`; slot counts in (c) are wrong |

### (b) [5]

**`logdump` reads the header from disk, and `end_op` clears it [2]** — a completed operation leaves the log empty by design, because the log is only needed between the commit and the end of the install.

**The two moments a concurrent reader would see `n > 0` [3]:** between **the commit write** and **the clearing write** — that is, during `install_blocks`. Before the commit, the header on disk still says 0 even though blocks have been written into the log area; after the clear, it says 0 again. *(A student who says "during install" earns the marks.)*

### (c) [5]

**`write /d/x 4096 41` uses 10 log slots [3]** — measured with an instrumented build: **8 data blocks + 1 bitmap block + 1 inode block.**

**Without absorption [2]:** the bitmap block is written once per `balloc` (8 times), the inode once per newly allocated block (8), plus 8 data blocks and 8 zeroing writes — **over 30 entries, which overflows a 30-block log.** Absorption is what makes the operation fit. *(Reference slot counts for the other commands, if a student asks: `create` 2, `mkdir` 4, `write 8192` 19.)*

---

## Q2: Recovery (25 points)

### (a) [15]

With the reference, the commit falls at **write 93** of `write /d/x 8192 43`:

```
$ ./myfsj t.img crash 93 write /d/x 8192 43
myfs: crashed after 93 writes
$ ./myfsj t.img logdump
logdump: n 19 49 33 52 53 54 55 56 57 ...
$ ./myfsj t.img recover
recover: replayed a committed log
  19 blocks installed
$ ./myfsj t.img fsck
fsck: … 0 leaked, 0 used twice, 0 used but not marked, 0 dangling, 0 orphaned, 0 bad link counts, log n 0
$ ./myfsj t.img read /d/x 8000 8
read /d/x 8000+8: 8 bytes  43 x8
```

**A crash at 92 gives `logdump: n 0` and the old file.** **[10]** for a working recovery on some crash point past the commit, **[5]** for reporting the number and showing both sides. **Students' numbers will differ** if their `write_head`/`log_write` order differs; **accept any number with a consistent `logdump` on either side.**

### (b) [5]

**Replay is idempotent because `install_blocks` *overwrites* home blocks with the logged contents [3]** — doing it twice writes the same bytes, so a crash during recovery is repaired by the next recovery.

**An operation that would not have it [2]:** anything **relative** — "add 4 to the free count", "append this entry", "decrement `nlink`". **A log of *new contents* is idempotent; a log of *changes* is not** — which is why this design logs whole blocks (physical logging) rather than operations.

### (c) [5]

**A header claiming more than `NLOG` blocks can only come from a block that is not a header [3]** — a crash during `format`, a wrong `logstart`, an image from a different build, or plain corruption.

**Without the check [2]:** `install_blocks` would read `lh.block[i]` for *i* past the array, **installing garbage block numbers over arbitrary parts of the disk** — recovery would destroy the file system it exists to save. **Accept** "out-of-bounds read and wild writes".

---

## Q3: Every Crash Point (25 points)

### (a) [10]

```
./crashsweep.sh ./myfsj base.img recover create /d/y
7 writes to complete; 6 crash points: 3 before, 3 after, 0 inconsistent
./crashsweep.sh ./myfsj base.img recover write /d/x 8192 43
113 writes to complete; 112 crash points: 92 before, 20 after, 0 inconsistent
```

**The mark is for the zero [10].** Any nonzero count is an implementation bug; **tell the student which window it falls in** — before the commit means the log is being installed early, after it means recovery is incomplete.

### (b) [8]

```
./crashsweep.sh ./myfsj base.img norecover write /d/x 8192 43
113 writes to complete; 112 crash points: … 14 inconsistent
```

**Fourteen [3]** — and **all of them fall in step 3, the install [3]**: the commit record is on disk, some home blocks have been updated and others have not, and the information to finish is sitting in the log, unread.

**Worse than no journal [2]:** the file system pays the extra writes and the flush for the log, **and still ends up inconsistent** — it has bought nothing. The journal's guarantee is the log **plus** replay, not the log alone.

### (c) [7]

**Prediction [1]** — any reasoned guess; the marks are for the measurement and the explanation.

```
./crashsweep.sh ./myfs base.img norecover create /d/y
3 writes to complete; 2 crash points: 0 before, 0 after, 2 inconsistent
./crashsweep.sh ./myfs base.img norecover write /d/x 8192 43
92 writes to complete; 91 crash points: 57 before, 0 after, 34 inconsistent
```

**36 of 93 crash points leave a broken file system [3].**

**The damage, explained [3]:**

- **`create`, both points: an orphaned inode.** `ialloc` writes the inode (marking it in use) **before** `dirlink` writes the directory entry. A crash between them leaves an inode nothing names — it can never be reached or freed. *(The reverse order would leave a **dangling entry** instead: a name pointing at a free inode, which is worse, because opening it reads another file's data.)*
- **`write`, 34 points: leaked blocks.** `balloc` marks a bitmap bit and zeroes the block **before** the inode that will point at it is written. A crash in between leaves a block marked in use and reachable from nothing. **Measured example:** `26 blocks marked, 25 reachable, 1 leaked`.
- **No crash point left the finished operation**, because the last write is the one that completes it.

---

## Q4: What It Costs (10 points)

### (a) [6]

| Operation | No journal | Journal | Ratio |
|---|---:|---:|---:|
| `create /d/y` | 3 | 7 | **2.3×** |
| `write /d/x 8192 43` | 92 | 113 | **1.23×** |

**[3] for the table.** **[3] for the two reasons:**

- **`create` costs more than double** because the journal adds **two header writes** — a fixed cost — to an operation of only three writes. **2 log writes + 2 headers + 3 installs = 7.**
- **`write` costs far less than double** because of **absorption**: 19 log slots cover an operation that writes 92 blocks, since the bitmap, inode and indirect blocks are written many times and logged once. **19 logged + 19 installed + 2 headers + the rest ≈ 113.**

### (b) [4]

**One flush per commit [2]:** 1,000 × 3.9 ms = **3.9 s**.
**Batched 50 per commit [1]:** 20 × 3.9 ms = **0.078 s** — fifty times less.

**What batching costs the first program [1]:** **latency** — its operation is not durable until the batch commits, so it waits for up to 49 other operations. **A system that promises durability per call cannot batch without making the caller wait**, which is exactly why `fsync` is slow and why databases offer "group commit" as a trade.

---

## Q5: What a Journal Does Not Promise (10 points)

### (a) [5]

**Guaranteed [2]:** the file system's **own structures** are consistent — no orphaned inodes, no leaked blocks, no entries pointing at free inodes. **In `data=ordered`, also: no file contains blocks that belonged to a deleted file**, because data is forced out before the metadata that points at it.

**Not guaranteed [2]: that your data is there.** The write may have been in the page cache when the power failed, and a journal of metadata says nothing about it. **The file can be empty, or short, or have its old contents.**

**The call [1]: `fsync` — about 3.9 ms**, against 2.9 µs for the buffered write (L23 §4).

### (b) [5]

**The sequence [3]:**

1. User A's file holds blocks 100–199 and is deleted; those blocks return to the free list.
2. User B creates a file; `balloc` gives it block 100; B writes its data into the page cache.
3. **The metadata — inode and bitmap — is journaled and committed**, so after a crash B's file *exists* and *claims block 100*.
4. **The crash happens before B's data page reaches the disk.** Block 100 still holds **A's old bytes**, and B's file now reads them.

**The rule `data=ordered` adds [2]:** **a file's data blocks must reach the disk before the metadata that points at them is committed.** Then a crash either shows no file, or a file whose blocks contain B's data — never someone else's.

---

*CS 202 · Week 8 · PS 8 Solutions · Instructor Only*
