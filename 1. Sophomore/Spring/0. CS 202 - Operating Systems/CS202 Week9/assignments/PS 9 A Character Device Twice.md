# CS 202 · Problem Set 9
## A Character Device, Twice

---

**Released:** Week 9, Wednesday · **Due:** Week 10, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS9_{LastName}_{StudentID}.pdf`, plus your `cs202ring.c`, your xv6 `ring.c`, and a `git diff` of your xv6 tree, in a tarball `PS9_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.

**You write the same device twice**: once against Linux's `file_operations`, where you can build it and never run it, and once in xv6, where you can run it. **The comparison is the point of the problem set.**

**Files provided** in `assignments/ps9/`:

| File | Yours to write | Provided |
|---|---|---|
| `linux/cs202ring.c` | `cs202ring_read`, `cs202ring_write` | the module skeleton, the operations table, `init`/`exit` |
| `linux/Makefile` | — | builds against `/lib/modules/$(uname -r)/build` |
| `ring.c` | `ringinit`, `ringread`, `ringwrite` | the structure, the lock, the buffer |
| `ringtest.c` | — | the user-space test: a child writes, the parent blocks in `read` |

---

### Q1: The Module You Cannot Load (30 points)

**(a) [5]** Build the skeleton as it stands:

```bash
cd linux && make
ls -la cs202ring.ko
modinfo cs202ring.ko
insmod cs202ring.ko
```

**Report the size of the `.ko`, the `modinfo` output, and the exact error from `insmod`.** **Which capability is missing**, and why is refusing it the right default on a machine you share? *(`man 7 capabilities`.)*

**(b) [15]** Implement `cs202ring_read` and `cs202ring_write`. They must:

- take `ring_lock` around every access to the buffer;
- **copy across the user boundary with `copy_to_user` and `copy_from_user`**, never by dereferencing;
- return the number of bytes actually transferred — **0 from `read` when the ring is empty**, which is a legal short read;
- discard, on `write`, whatever does not fit.

**Your module must compile with no warnings** (`make` output in the PDF).

**(c) [5]** `copy_to_user` returns **how many bytes it failed to copy**, not an error code. **Show the lines of your `read` that handle a partial copy**, and say what a driver that ignored the return value would hand the program.

**(d) [5]** Your `read` returns 0 on an empty ring; the xv6 version in Q2 **blocks**. **What does a Linux driver need in order to block correctly** — name the structure and the two calls — and **why can it not simply spin**? *(LDD3 Ch. 6; L29 §6.)*

---

### Q2: The Device You Can Run (40 points)

Implement `ringinit`, `ringread` and `ringwrite` in xv6's `ring.c`, add `ring.o` to the `Makefile`'s kernel objects, call `ringinit()` from `main.c`, and add `#define RING 2` to `file.h`.

**(a) [10]** `ringinit` initialises the lock and **registers the device in `devsw[RING]`**. Show the three lines, and say **what would happen to a program that opened the device before `ringinit` ran.**

**(b) [15]** `ringread` must **sleep while the buffer is empty** and wake when data arrives, following `consoleread`'s pattern exactly: unlock the inode, take the ring's spinlock, `sleep` in a `while` loop, copy out, release, relock the inode.

**(c) [10]** `ringwrite` appends what fits, counts what does not, and **wakes a sleeping reader**.

**(d) [5]** Build and run:

```
$ ringtest 300
parent: reading (this blocks until the child writes)
parent: read 300 bytes of 300; the last byte was 'n', which is byte 299
```

**Report your run, for 300 and for 1,000 bytes.** The test's child sleeps before writing, **so the parent is asleep in your driver first**; say how the output proves that.

---

### Q3: Two Interfaces, Compared (15 points)

**(a) [6]** Put xv6's `devsw` beside Linux's `file_operations` in a table. **Name three things Linux's interface has that xv6's does not**, and for each, **a device that needs it.**

**(b) [5]** Both drivers copy across the user boundary. **Name xv6's mechanism and Linux's**, and **describe the bug that appears if either is skipped** — including what the kernel does when it happens.

**(c) [4]** In xv6 the major number is a constant in a header; in Linux `register_chrdev` returns one at load time. **Why the difference?** What does Linux's approach make possible that a fixed constant does not?

---

### Q4: What It Costs to Reach a Device (15 points)

**(a) [8]** Build and run `lab/devcost.c`, which times the same call to several devices:

```bash
gcc -O2 -Wall -Wextra -o devcost devcost.c && taskset -c 2 ./devcost
```

**Report the table.** **`/dev/null`'s `write` does nothing at all — so what are you measuring?** Break its cost into the parts you can name, using Week 0's system-call measurement.

**(b) [4]** `/dev/zero` costs about 200 ns more at 4 KiB than at 4 bytes; `/dev/urandom` costs about 11,700 ns more. **Explain both**, and give the per-byte cost of each device's own work.

**(c) [3]** A program reads 4 bytes at a time from your xv6 ring device in a loop. **Using the dispatch costs you measured and Week 0's trap measurements, estimate the cost per byte**, and name **two** changes to the interface — not to the driver — that would reduce it.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The module you cannot load | 30 |
| 2 | The device you can run | 40 |
| 3 | Two interfaces, compared | 15 |
| 4 | What it costs to reach a device | 15 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped.**

---

*CS 202 · Week 9 · PS 9 · © CSE Department*
