# CS 202 · Operating Systems
## Week 9 · Lecture 3 of 3
### Writing a Driver — and the Module That Will Not Load

*“Everyone knows that debugging is twice as hard as writing a program in the first place. So if you're as clever as you can be when you write it, how will you ever debug it?”* — Brian Kernighan & P. J. Plauger, *The Elements of Programming Style*, 2nd ed. (1978), ch. 2

---

**Sat:** Friday of Week 9, 09:00–09:50, VNC 101 · **Reading:** LDD3 Ch. 2–3; Love Ch. 17 · **Next:** Week 10, virtualization

**Coursework:** 📝 **PS 8** due today 17:00 · 📊 **Quiz 10** Mon of Week 10 · 🔬 **Lab 9** Tue of Week 10 15:00–16:50 · 📝 **PS 10** released Wed of Week 10, due Fri of Week 11 17:00

---

## 1. A Kernel Module Is Code You Add to a Running Kernel

**Everything in the kernel could be compiled in.** Modules exist because a distribution cannot know which of ten thousand drivers your machine needs, and because a driver you are writing should not need a reboot to try.

**A module is an object file with an init and an exit function:**

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

static int __init hello_init(void) { pr_info("cs202: hello\n"); return 0; }
static void __exit hello_exit(void) { pr_info("cs202: goodbye\n"); }

module_init(hello_init);
module_exit(hello_exit);
MODULE_LICENSE("GPL");
```

**It builds against the running kernel's headers**, which are installed on this machine:

```
$ ls -d /lib/modules/$(uname -r)/build
/lib/modules/7.0.0-31-generic/build
$ make
  CC [M]  hello.o
  LD [M]  hello.ko
$ ls -la hello.ko
183240 hello.ko
```

**183 kilobytes for six lines** — most of it symbol tables, relocations and the BTF/debug sections the kernel build adds.

---

## 2. And Then It Does Not Load

```
$ insmod hello.ko
insmod: ERROR: could not insert module hello.ko: Operation not permitted
```

**Loading a module needs `CAP_SYS_MODULE`** — root, in practice. **The refusal is not an accident of this machine's configuration; it is the security boundary of the whole course.** A module runs in the kernel: it can read any memory, change any table, and disable any check. **Granting a student account the right to load one is granting it the machine.**

**Everything else about modules is visible from an ordinary account:**

```
$ lsmod | head -3
Module                  Size  Used by
tls                   163840  0
ccm                    20480  6
```

**You can see what is loaded, what depends on what, and how large each is** — and `modinfo` will read your own `.ko`'s metadata. **What you cannot do is run it.**

**So this course writes drivers where they can be run: in xv6**, where you own the kernel. **PS 9 asks for both** — the Linux module, built and inspected, and the same device implemented in xv6 and actually used. **The two interfaces are close enough that the comparison is the lesson** (L28 §3).

---

## 3. What the Kernel Takes Away

**A driver is C, and almost nothing else is familiar.**

| Not available | Why | Use instead |
|---|---|---|
| `printf` | no C library is linked into the kernel | `printk` / `pr_info`, and xv6's `cprintf` |
| `malloc` | no user heap; allocation must say whether it may sleep | `kmalloc(size, GFP_KERNEL)`; xv6's `kalloc` — one page |
| **floating point** | the kernel does not save FPU state on entry (Week 1 L05 §6) | integers, or `kernel_fpu_begin()` in the rare case |
| a large stack | the kernel stack is **one page** in xv6, 16 KiB in Linux | no big local arrays, no deep recursion |
| **sleeping in an interrupt** | there is no process to put to sleep (L29 §6) | queue the work; wake someone who can |
| user pointers | they may be unmapped or hostile (L28 §6) | `copy_to_user`, `copy_from_user`; xv6's `argptr` |

**And one thing the kernel adds: every mistake is fatal to the machine.** A null dereference in a program is a `SIGSEGV`; in a driver it is an oops, and if it happens while holding a lock, a hang. **xv6 states this plainly by panicking** — which is why the labs run it under QEMU, where a panic costs a restart.

---

## 4. The Shape of a Character Driver

**Both kernels want the same three things.**

**1. A table of operations.**

```c
/* Linux */                              /* xv6 */
static struct file_operations fops = {   devsw[RING].read  = ringread;
    .owner   = THIS_MODULE,              devsw[RING].write = ringwrite;
    .read    = ring_read,
    .write   = ring_write,
};
```

**2. Registration, which yields a major number.** Linux: `register_chrdev(0, "ring", &fops)` returns one, and `mknod /dev/ring c MAJOR 0` — or `udev` — creates the file. **xv6: the major number is a constant in `file.h`**, and the program calls `mknod("ring", RING, 0)` itself.

**3. The functions themselves**, which must block when there is nothing to do and wake whoever is waiting when there is. **The reference ring device's read is Week 3's condition variable, wearing a device's clothes:**

```c
  while(ring.r == ring.w){
    if(myproc()->killed){ release(&ring.lock); ilock(ip); return -1; }
    sleep(&ring.r, &ring.lock);
  }
```

**and its write ends with `wakeup(&ring.r)`.** Measured, from user space:

```
$ ringtest 300
parent: reading (this blocks until the child writes)
parent: read 300 bytes of 300; the last byte was 'n', which is byte 299
```

**The parent blocked in `read()` before any writer existed**, and woke when one arrived — with no polling, no timeout, and no busy loop.

---

## 5. The Bugs a First Driver Has

1. **Dereferencing the user pointer.** Works in testing; panics the first time a program passes a bad address. **`argptr` or `copy_from_user`, always.**
2. **Sleeping with a spinlock held, or in an interrupt.** xv6's `sleep` takes the lock as an argument for exactly this reason: it releases it while asleep and takes it back on waking.
3. **Forgetting to wake.** The reader sleeps forever; `top` shows an idle machine. **Week 4's deadlock, from the other side.**
4. **`if` instead of `while` around the sleep.** Week 3 L12 §2's lost wake-up, in a driver.
5. **Returning the wrong count.** `read` must return how many bytes it actually produced; a driver that returns *n* regardless hands the program uninitialised memory.
6. **Unbounded loops in the handler.** An interrupt handler that waits for the device holds off every other interrupt on that CPU.

**Five of those six are Week 3 and Week 4 bugs.** A driver is concurrent code that happens to be reachable through `open`.

---

## 6. What to Take Away

1. **A module is code loaded into the running kernel**; it builds against the kernel's headers, and **183 KB of object file came from six lines.**
2. **`insmod` needs `CAP_SYS_MODULE`, and is refused here** — correctly: a module is the machine. **Everything except running one is still visible.**
3. **Drivers in this course are written in xv6**, where the kernel is yours and a mistake costs a restart.
4. **The kernel takes away the C library, the heap you know, floating point, a big stack, and the right to sleep in an interrupt** — and makes every bug fatal.
5. **A character driver is a table of functions, a registration, and code that blocks and wakes properly.**
6. **A first driver's bugs are Week 3's bugs**: unvalidated pointers, lost wake-ups, `if` instead of `while`, and sleeping where you may not.

---

## Exercises

1. `hello.ko` is 183 KB for six lines. **Run `modinfo` and `size` on it** and account for the sections; what would `strip` leave?
2. **Why does the kernel refuse `insmod` rather than restricting what a module may do once loaded?** What would a "restricted module" have to prevent?
3. xv6's kernel stack is one page. **Write a driver function that overflows it**, and say what happens — and how you would notice.
4. A driver's `read` copies *n* bytes but only *k* were available. **Give the three plausible return values** and say what each does to the calling program.
5. **Which of L30 §5's six bugs would `usertests` catch** in an xv6 driver, and which would pass every test and fail in production?

---

*CS 202 · Week 9 · L30 · © CSE Department*
