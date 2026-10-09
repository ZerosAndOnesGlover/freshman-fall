# CS 202 · Operating Systems
## Week 9 · Lecture 1 of 3
### One Interface for Every Device

*“UNIX does not allow path names to be prefixed by a drive name or number; that would be precisely the kind of device dependence that operating systems ought to eliminate.”* — Andrew S. Tanenbaum, *Modern Operating Systems*, 3rd ed.

---

**Sat:** Monday of Week 9, 09:00–09:50, VNC 101, **after Quiz 9** · **Reading:** OSTEP Ch. 36; xv6 book Ch. 3 §3.5 · **Next:** L29, interrupts and the block layer

**Coursework:** 📊 **Quiz 9** today · 🔬 **Lab 8** Tue this week 15:00–16:50 · 📋 **Project 2** released Wed this week, due Fri of the completion period 17:00 · 📝 **PS 9** released Wed this week, due Fri of Week 10 17:00 · 📝 **PS 8** due Fri this week 17:00

---

## 1. Everything Is a File, and Something Has to Make That True

**`read()` works on a file, a pipe, a socket, a terminal and a disk.** The program cannot tell which it has, and that is the point: a shell can redirect any of them into any program.

**The kernel makes it true with a table of function pointers per open file.** `read()` looks up the file, finds its operations, and calls the one in the `read` slot. **That is polymorphism, in C, at the system-call boundary** — and it is the whole architecture of device support.

```
$ ls -l /dev/null /dev/zero /dev/urandom
crw-rw-rw- 1 root root 1, 3 /dev/null
crw-rw-rw- 1 root root 1, 5 /dev/zero
crw-rw-rw- 1 root root 1, 9 /dev/urandom
```

**`c` is a character device; `1, 3` is its major and minor number.** The file in `/dev` holds no data: **it is a name carrying two integers**, and the major number selects the driver.

---

## 2. xv6's Version, in Nine Lines

```c
// table mapping major device number to device functions
struct devsw {
  int (*read)(struct inode*, char*, int);
  int (*write)(struct inode*, char*, int);
};

extern struct devsw devsw[];
#define CONSOLE 1
```

**An inode of type `T_DEV` stores a major number instead of block addresses**, and `fileread` dispatches:

```c
if(f->ip->type == T_DEV)
    return devsw[f->ip->major].read(f->ip, addr, n);
```

**`mknod("console", CONSOLE, 0)`** — which xv6's `init` runs at boot — creates that inode. **Nothing else in the kernel knows what a console is.**

**PS 9 adds a second entry to that table.** The reference — a ring buffer with blocking reads — is 60 lines, and behaves like a device from user space:

```
$ ringtest 300
parent: reading (this blocks until the child writes)
parent: read 300 bytes of 300; the last byte was 'n', which is byte 299
```

**The parent called `read()` on a file and slept in the driver until a writer arrived** — the same `sleep`/`wakeup` pair as Week 3's condition variable, reached through `open` and `read`.

---

## 3. Linux's Version, and What It Adds

A Linux character driver fills in `struct file_operations`:

| xv6 `devsw` | Linux `file_operations` |
|---|---|
| `read` | `.read` / `.read_iter` |
| `write` | `.write` / `.write_iter` |
| — | `.open`, `.release` |
| — | `.unlocked_ioctl` — everything that is not a read or a write |
| — | `.poll` — "is there data?" for `select`/`poll`/`epoll` |
| — | `.mmap` — map the device's memory into a process |
| — | `.llseek`, `.fsync`, `.flush`, … |

**`ioctl` is the confession**: some device operations are not reads or writes — eject the disc, set the baud rate, get the terminal size — and rather than invent a system call for each, Unix added one call with a number and a pointer. **It is the interface's escape hatch**, and every driver defines its own numbers.

---

## 4. What the Dispatch Costs

**`devcost.c`** makes the same calls to several devices, 200,000 times each:

| | 4 bytes | 4 KiB |
|---|---:|---:|
| `/dev/null` (write) | **659 ns** | 684 ns |
| `/dev/zero` (read) | **687 ns** | 882 ns |
| `/dev/urandom` (read) | 946 ns | **12,689 ns** |
| a cached file (read) | 819 ns | 1,064 ns |
| `ioctl` (on a non-tty, returning `ENOTTY`) | **595 ns** | |
| `poll`, data ready | 673 ns | |

**Read the first column first: every one of them is 600–950 ns**, and `/dev/null` — a driver whose `write` function *does nothing* — costs 659. **That is the system call itself** (Week 0 measured `getppid` at ~590 ns on this machine, with page-table isolation), plus the file lookup and the dispatch. **The device's own work is what is left over.**

**The second column separates the two.** `/dev/zero` at 4 KiB costs 882 ns: 659 of dispatch and ~200 of `memset`. **`/dev/urandom` costs 12,689** — 3 ns per byte of generated randomness, **twenty times the dispatch** — because that driver actually computes something.

**The lesson for a driver writer:** for small transfers **you are competing with the syscall, not the device**, which is why fast devices get `io_uring` and `mmap` interfaces that amortise or remove it.

---

## 5. Block Devices Are Not Character Devices

**A character device is a stream**: bytes arrive in order, and the driver is asked for *n* of them. **A block device is an array**: the kernel asks for **block number 4,217**, and expects it to be cacheable, reorderable, and the same on every read.

| | Character | Block |
|---|---|---|
| Unit | a byte | a fixed-size block |
| Random access | rarely | **always** |
| Cached by the kernel | no | **yes** — the page cache (L23) |
| Queued and reordered | no | **yes** — the block layer (L29) |
| xv6 example | console, and PS 9's ring | the IDE disk, through `bread`/`bwrite` |

**Which is why `bread` exists in xv6's file system and `devsw` does not**: the file system talks to the buffer cache, and the buffer cache talks to one driver.

---

## 6. Copying Across the Boundary

**A driver is given a pointer from user space, and must not trust it.** The address may be unmapped, may belong to the kernel, or may be unmapped *between* the check and the use by another thread.

- **Linux**: `copy_to_user` and `copy_from_user`, which fault safely and return how much they failed to copy.
- **xv6**: `argptr` validates a pointer against the process's size before a system call uses it; `copyout` walks the process's page table to write into it.

**Week 5 L18 §2 met the failure this prevents**: a kernel that dereferences a bad user pointer takes a page fault **in kernel mode**, where xv6 panics and Linux would oops. **It is the single most common bug in a first driver**, which is why PS 9 asks for it explicitly.

---

## 7. What to Take Away

1. **One system call reaches every device through a table of function pointers** — `devsw` in xv6, `file_operations` in Linux.
2. **A device file is a name and two numbers**; the major number picks the driver, and `mknod` creates it.
3. **xv6's whole device interface is `read` and `write`**; Linux adds `open`, `release`, `ioctl`, `poll` and `mmap` — **`ioctl` being the admission that not everything is a read or a write.**
4. **Dispatch costs about 650 ns on this machine, device work excluded** — measured with a driver that does nothing — so **small I/O is dominated by the system call**.
5. **Block devices are arrays, cached and queued; character devices are streams** and neither.
6. **A driver must copy across the user boundary with the kernel's helpers**, never by dereferencing.

---

## Exercises

1. `/dev/null`'s `write` does nothing and costs 659 ns. **Account for that time** using Week 0's measurements, and say what fraction is page-table isolation.
2. **Why is `/dev/zero` at 4 KiB only 200 ns dearer than at 4 bytes**, when `/dev/urandom` is 11,700 ns dearer?
3. xv6's `devsw` has no `open`. **What can a Linux driver do at `open` that xv6's cannot**, and give a device that needs it.
4. `ioctl` takes an unsigned number and a pointer. **Name two problems that creates** — one for portability, one for security.
5. A student's driver dereferences the user pointer directly and works in testing. **Give two inputs that break it**, and say what each does to the kernel.

---

*CS 202 · Week 9 · L28 · © CSE Department*
