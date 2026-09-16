# CS 202 · Problem Set 8
## A Journal for `myfs`

---

**Released:** Week 8, Wednesday · **Due:** Week 9, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS8_{LastName}_{StudentID}.pdf`, plus your `myfsj.c` in a tarball `PS8_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **`myfsj.c` must compile clean under `gcc -O2 -Wall -Wextra`** and reproduce the outputs below.

**This problem set adds a journal to PS 7's file system.** You are given `assignments/ps8/myfsj.c`: **PS 7's file system, complete**, with the log's layout, its header structure, the crash simulator and the stronger `fsck` already written — and **five functions to fill in**. If your PS 7 did not work, use this one: the parts you wrote for PS 7 are present.

```
 block 0   1      2         3 .. 32     33 .. 48   49      50 ..
 [ unused | super | log header | log blocks |  inodes  | bitmap | data ]
```

| Provided | Yours to write |
|---|---|
| the whole file system, `read_head`, `bread`/`bwrite` routing, `crash N`, `logdump`, `fsck`, and `lab/crashsweep.sh` | **Q1:** `write_head`, `log_write`, `end_op` · **Q2:** `install_blocks`, `recover` |

**The crash simulator** stops the program after exactly *N* block writes reach the image — a power failure, at a place you choose:

```bash
./myfsj img crash 7 create /d/y      # exits 3 after the seventh write
```

---

### Q1: The Log (30 points)

Implement `write_head`, `log_write` and `end_op`, following the comments exactly. **The order in `end_op` is the whole point**: log the blocks, **write the header (this is the commit)**, install, then clear the header.

**(a) [20]** With a formatted image:

```
$ ./myfsj j.img format 2048
formatted 2048 blocks of 512 bytes: superblock 1, log 2-32, inodes 33-48, bitmap 49-49, data 50-2047
128 inodes, 1998 data blocks, log holds 30 blocks, max file 71680 bytes
$ ./myfsj j.img mkdir /d
mkdir /d: inode 2
$ ./myfsj j.img create /d/x
create /d/x: inode 3
$ ./myfsj j.img write /d/x 4096 41
write /d/x: 4096 bytes at 0, size now 4096, 8 blocks
$ ./myfsj j.img logdump
logdump: n 0
$ ./myfsj j.img fsck
fsck: 3 inodes in use, 60 blocks marked, 60 reachable, 0 leaked, 0 used twice, 0 used but not marked, 0 dangling, 0 orphaned, 0 bad link counts, log n 0
```

**(b) [5]** **Why is `logdump` 0 after a successful operation**, when the operation certainly used the log? At which two moments during `end_op` would a `logdump` from another program have shown a nonzero `n`?

**(c) [5]** `log_write` scans the log for the block before adding it — **absorption**. **Count the log slots** `write /d/x 4096 41` uses, and say which blocks they are. How many writes would the same operation need **without** absorption?

---

### Q2: Recovery (25 points)

Implement `install_blocks` and `recover`. **`recover` must be safe to run at any time and any number of times.**

**(a) [15]** Crash during an operation, then recover:

```
$ cp j.img t.img
$ ./myfsj t.img crash 97 write /d/x 8192 43
myfs: crashed after 97 writes
$ ./myfsj t.img logdump
logdump: n …                                   ← report what you see
$ ./myfsj t.img recover
recover: replayed a committed log
$ ./myfsj t.img fsck
fsck: … 0 leaked, … 0 orphaned, … log n 0      ← and this
$ ./myfsj t.img read /d/x 8000 8
read /d/x 8000+8: 8 bytes  43 x8
```

**Report the crash number you had to use** to land after the commit — it will not be 97 on your machine unless your implementation writes exactly as many blocks as the reference.

**(b) [5]** **Why is replaying a log twice harmless?** What property of `install_blocks` makes that true, and what kind of operation would *not* have it?

**(c) [5]** `read_head` ignores a header claiming more blocks than the log holds. **What state of the disk would produce such a header**, and what would happen without that check?

---

### Q3: Every Crash Point (25 points)

`lab/crashsweep.sh` stops an operation after **every** possible number of writes and checks the image each time.

**(a) [10]** Run it on your journal, for two operations:

```bash
./crashsweep.sh ./myfsj base.img recover create /d/y
./crashsweep.sh ./myfsj base.img recover write /d/x 8192 43
```

**Report both lines.** **Every crash point must be either the old state or the new state, and none inconsistent.** If any are, fix your implementation before answering anything else.

**(b) [8]** Run the same sweeps with **`norecover`**, which skips the replay:

```bash
./crashsweep.sh ./myfsj base.img norecover write /d/x 8192 43
```

**How many crash points are now inconsistent, and where do they fall** in the four steps of L26 §1? **Explain why a journal without recovery is worse than no journal at all.**

**(c) [7]** Your PS 7 `myfs` — or `solutions_instructor`'s, if you must — has no log. **Predict** how many of its crash points leave an inconsistent file system for `create` and for `write 8192`, **then measure it** with the same script and the `fsck` from this problem set. **Explain each kind of damage you see** (orphaned inodes, leaked blocks) in terms of which write was missed.

---

### Q4: What It Costs (10 points)

**(a) [6]** From your sweeps, **the number of writes each operation needs, with and without the journal**, for `create` and for `write 8192`. **Give both ratios**, and explain **why neither is 2×** — one is more, one is less.

**(b) [4]** In a real file system the cost is not writes but **flushes**. Using L23 §4's measured 3.9 ms per flush: **a program creates 1,000 small files, each one operation.** How long does that take **if every commit is flushed**, and **if the file system batches 50 operations per commit** (L26 §4)? What does batching cost the program that asked first?

---

### Q5: What a Journal Does Not Promise (10 points)

**(a) [5]** A program writes a file, and the machine loses power one second later. The file system is journaled in `data=ordered` mode. **What does the file system guarantee about your file, and what does it not?** **Which call would have made the difference**, and what would it have cost (L23 §4)?

**(b) [5]** ext4's `data=writeback` mode journals metadata without ordering data before it. **Construct the sequence of events** — two files, two users — **after which one user's new file contains another user's deleted data.** Say which single ordering rule `data=ordered` adds to prevent it.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The log | 30 |
| 2 | Recovery | 25 |
| 3 | Every crash point | 25 |
| 4 | What it costs | 10 |
| 5 | What a journal does not promise | 10 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped.**

---

*CS 202 · Week 8 · PS 8 · © CSE Department*
