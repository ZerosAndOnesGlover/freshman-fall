# CS 202 · Problem Set 9 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 9.** Q1 cannot be run, so **mark the code and the build output**; Q2 can be run, so **mark the run**. Students who write a plausible `ringread` that never blocks will pass their own eyeball test and fail `ringtest` — **ask for the test output, not a description of it.**

**Reference:** `solutions_instructor/ring reference (do not distribute).c` — the xv6 device, complete. The Linux skeleton in `assignments/ps9/linux/` builds warning-free as issued.

All figures from the reference machine: i5-8250U, Ubuntu 24.04.4, kernel 7.0.0-31, GCC 13.3.0.

---

## Q1: The Module You Cannot Load (30 points)

### (a) [5]

```
$ ls -la cs202ring.ko
330976 cs202ring.ko
$ modinfo cs202ring.ko
description:    A ring-buffer character device, for CS 202 Week 9
author:         CS 202
license:        GPL
srcversion:     647FB3852530609967A4448
depends:
$ insmod cs202ring.ko
insmod: ERROR: could not insert module cs202ring.ko: Operation not permitted
```

**The capability is `CAP_SYS_MODULE` [2]** — in practice, root.

**Why refusing it is right [3]:** a module runs **in kernel mode with no boundary at all** — it can read and write any physical memory, replace any system call, and switch off every check the rest of the course has described. **Granting a student account the right to load one is granting the machine**, and on a shared lab machine, everyone else's work with it. *(Accept "it is equivalent to root, so it is root".)*

### (b) [15]

A correct pair, under the mutex, with the copies done properly:

```c
static ssize_t cs202ring_read(struct file *f, char __user *buf, size_t n, loff_t *off)
{
	size_t avail, chunk, not_copied;

	mutex_lock(&ring_lock);
	avail = head - tail;
	chunk = min(n, avail);
	if (chunk > RINGSIZE - (tail % RINGSIZE))
		chunk = RINGSIZE - (tail % RINGSIZE);      /* one wrap at a time */
	not_copied = copy_to_user(buf, ring + (tail % RINGSIZE), chunk);
	chunk -= not_copied;
	tail += chunk;
	mutex_unlock(&ring_lock);
	return chunk;
}
```

**Marks:** 5 for the lock, **5 for `copy_to_user`/`copy_from_user`** (a submission that dereferences `buf` loses all five), 3 for the wrap, 2 for a build with no warnings.

**The common failure**: holding the mutex across `copy_to_user`. It is **allowed** — `copy_to_user` may sleep, and a mutex may be held while sleeping — but a student who claims it is forbidden has confused it with a spinlock; **give the marks and correct the reasoning.**

### (c) [5]

`copy_to_user` returns **the number of bytes it could not copy** — usually 0. **[2]**

```c
	not_copied = copy_to_user(buf, src, chunk);
	chunk -= not_copied;          /* report only what actually arrived */
```

**A driver that ignored it [3]** would return *chunk* while some of the user's buffer was never written — **handing the program whatever was in its own memory**, which is an information leak, and a wrong count besides. *(This is the same class of bug as L28 §6's unvalidated pointer.)*

### (d) [5]

**A wait queue [2]:** `DECLARE_WAIT_QUEUE_HEAD(q)`, then **`wait_event_interruptible(q, head != tail)`** in `read` and **`wake_up_interruptible(&q)`** in `write`. *(Accept `prepare_to_wait`/`schedule` too.)*

**Why not spin [3]:** on a single CPU the spinner **prevents the writer from running at all** — the classic deadlock-by-priority of L11 §6 — and on any machine it burns a core for the whole wait. **Blocking hands the CPU to whoever will make the condition true**, which is what a device driver's read must do.

---

## Q2: The Device You Can Run (40 points)

### (a) [10]

```c
void
ringinit(void)
{
  initlock(&ring.lock, "ring");
  devsw[RING].read = ringread;
  devsw[RING].write = ringwrite;
}
```

**Before `ringinit` runs [5]:** `devsw[RING].read` is **a null pointer**, and `fileread`'s call through it **jumps to address 0 in kernel mode** — an immediate panic, not an error returned to the program. *(xv6 does not check; Linux's `register_chrdev` is what makes the equivalent impossible.)*

### (b) [15]

```c
int
ringread(struct inode *ip, char *dst, int n)
{
  int got = 0;

  iunlock(ip);
  acquire(&ring.lock);
  while(ring.r == ring.w){
    if(myproc()->killed){
      release(&ring.lock);
      ilock(ip);
      return -1;
    }
    sleep(&ring.r, &ring.lock);
  }
  while(got < n && ring.r != ring.w)
    dst[got++] = ring.buf[ring.r++ % RINGSIZE];
  release(&ring.lock);
  ilock(ip);
  return got;
}
```

**Marks:** 5 for the `while` around `sleep` (an `if` is Week 3 L12 §2's lost wake-up — **deduct all five**), 4 for releasing and re-taking the inode lock in the right order, 3 for the killed check, 3 for returning the count actually copied.

### (c) [10]

```c
  for(i = 0; i < n; i++){
    if(ring.w - ring.r >= RINGSIZE){
      ring.dropped += n - i;
      break;
    }
    ring.buf[ring.w++ % RINGSIZE] = src[i];
  }
  wakeup(&ring.r);
```

**5 for the wake-up** — without it the reader sleeps forever and the machine looks idle (Lab 9 Q11) — 3 for the bound check, 2 for returning *i*.

### (d) [5]

```
$ ringtest 300
parent: reading (this blocks until the child writes)
parent: read 300 bytes of 300; the last byte was 'n', which is byte 299
$ ringtest 1000
parent: reading (this blocks until the child writes)
parent: read 1000 bytes of 1000; the last byte was 'l', which is byte 999
```

**The child sleeps 20 ticks before it opens the device**, so the parent printed its line and then **blocked inside `ringread`** — the only place it could be. **The proof is the order of the output plus the fact that the run completes**: a driver that returned 0 instead of sleeping would print the "reading" line and then finish with 0 bytes. *(`'n'` is `'a' + 299 % 26` and `'l'` is `'a' + 999 % 26`; a student whose last byte differs has a wrapping bug.)*

---

## Q3: Two Interfaces, Compared (15 points)

### (a) [6]

| Linux has | xv6 does not | A device that needs it |
|---|---|---|
| `.open` / `.release` | — | a tape or serial port that must be reset per open; any device with exclusive access |
| `.unlocked_ioctl` | — | a terminal (`TIOCGWINSZ`), a CD-ROM (eject), a GPU (everything) |
| `.poll` | — | anything used with `select`/`epoll`: a socket, a serial line, an event device |
| `.mmap` | — | a framebuffer, a sound buffer, an NVMe queue in user space |
| `.llseek`, `.fsync`, `.write_iter`, … | — | a block-like character device; anything with scatter-gather |

**2 marks per correct pair, to 6.**

### (b) [5]

**xv6: `argptr`** (and `copyout` for writing back), which checks the pointer against the process's size before use. **Linux: `copy_from_user` / `copy_to_user`**, which fault safely.

**The bug if skipped [3]:** the kernel dereferences an address the process does not own. **In xv6 that is a page fault in kernel mode → `panic`** (L18 §2); in Linux it is an **oops**, killing the process and often leaving a lock held. **Either way the failure is the kernel's, not the program's** — which is the distinction the whole course rests on.

### (c) [4]

**xv6 has one kernel, built as a unit, with a fixed set of devices [2]** — a constant is enough, and `mknod` in `init` uses it.

**Linux loads drivers at runtime and cannot know which numbers are free [2]**, so `register_chrdev(0, …)` asks for one. **What that makes possible:** a driver written years later, by someone else, loaded into a running machine, without a central registry of numbers — and `udev` creating `/dev/…` from what the driver reports.

---

## Q4: What It Costs to Reach a Device (15 points)

### (a) [8]

| | 4 bytes | 4 KiB |
|---|---:|---:|
| `/dev/null` (write) | **659 ns** | 684 ns |
| `/dev/zero` (read) | 687 ns | 882 ns |
| `/dev/urandom` (read) | 946 ns | **12,689 ns** |
| a cached file (read) | 819 ns | 1,064 ns |
| `ioctl` returning `ENOTTY` | **595 ns** | |
| `poll`, ready | 673 ns | |

**What is being measured with `/dev/null` [4]:** **the system call itself** — `syscall` entry and return, with page-table isolation's two `CR3` switches (Week 0 measured `getppid` at ~590 ns on this machine) — **plus** the file-descriptor lookup, the reference count, and the indirect call through `file_operations`. **The driver contributes nothing.**

### (b) [4]

**`/dev/zero`: ~195 ns for 4,092 more bytes ≈ 0.05 ns per byte** — a `memset` running at tens of gigabytes per second. **`/dev/urandom`: ~11,740 ns ≈ 2.9 ns per byte** — ChaCha20 generating pseudorandom bytes, about sixty times dearer per byte. **[2 + 2]**

### (c) [3]

**Per byte: ~660 ns** — the whole call — against roughly 1 ns of actual work. **[1]**

**Two interface changes [2]:** **read in larger blocks** (amortise one call over *n* bytes — the same lesson as Midterm 1's buffered read), and **`mmap` the device** so that bytes are fetched without a call at all. *(Also acceptable: `io_uring`, or a batched `readv`.)* **Note both are changes to how the device is used, not to the driver.**

---

*CS 202 · Week 9 · PS 9 Solutions · Instructor Only*
