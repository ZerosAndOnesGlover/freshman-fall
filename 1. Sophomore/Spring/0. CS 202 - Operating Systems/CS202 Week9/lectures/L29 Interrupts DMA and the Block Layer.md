# CS 202 · Operating Systems
## Week 9 · Lecture 2 of 3
### Interrupts, DMA, and the Block Layer

*“Computers don't introduce order anywhere as much as they expose opportunities.”* — Alan Perlis, "Epigrams on Programming" (1982), #96

---

**Sat:** Wednesday of Week 9, 09:00–09:50, VNC 101 · **Reading:** OSTEP Ch. 36 §36.4–§36.6, Ch. 37; xv6 book Ch. 3 §3.5 · **Next:** L30, writing a driver

**Coursework:** 📋 **Project 2** released today, due Fri of the completion period 17:00 · 📝 **PS 9** released today, due Fri of Week 10 17:00 · 📝 **PS 8** due Fri this week 17:00 · 📊 **Quiz 10** Mon of Week 10 · 🔬 **Lab 9** Tue of Week 10 15:00–16:50

---

## 1. The Device Is Slower Than You, and Then It Is Not

**A driver's central problem is waiting.** L19 measured a page read from this machine's SSD at **90 µs**; in that time the CPU executes roughly **three hundred thousand instructions**. The question every driver answers is what to do with them.

| Strategy | The CPU | Good when |
|---|---|---|
| **Polling** — read the status register until ready | spins, doing nothing else | the wait is shorter than the cost of switching away |
| **Interrupts** — sleep, and let the device raise a line | runs something else | the wait is long |
| **DMA** — the device moves the bytes itself | not involved in the copy at all | the transfer is large |

**The trade is the same as Week 3's spin-or-sleep** (L11 §6), with the numbers a thousand times larger — and, as there, **the right answer changed when the hardware did.**

---

## 2. What an Interrupt Costs, and How Many There Are

**Every interrupt is a trap**: the CPU saves state, switches to the kernel stack, runs the handler, and returns — Week 0's mechanism, unbidden. **The kernel counts them**, per device and per CPU:

```
$ grep -E "nvme|i8042" /proc/interrupts
   1:        630  …  IR-IO-APIC    1-edge      i8042
 159:          0  …  IR-PCI-MSIX-0000:3e:00.0    0-edge      nvme0q0
 160:          0      98674  …  IR-PCI-MSIX-0000:3e:00.0    1-edge      nvme0q1
```

**The keyboard has raised 630 interrupts since boot; the disk's first queue, 98,674.** Note that the disk's interrupts land on **one CPU** — each queue is bound to one — which is a deliberate choice this lecture returns to in §5.

**How many interrupts does an I/O actually cost?** Reading 256 MiB with `O_DIRECT`, so that nothing is cached:

| Request size | Interrupts | Per unit | Time |
|---|---:|---|---:|
| **1 MiB reads** | **1,969** | **7.7 per MiB — one per 128 KiB** | 0.136 s |
| **4 KiB reads** | **65,536** | **exactly one per read** | 1.115 s |

**Two things to read out of that.**

- **The large-request case is limited by `max_sectors_kb` = 128**: the block layer splits a 1 MiB request into eight 128 KiB commands, and each completion raises one interrupt. **The interrupt is per command, not per byte.**
- **The small-request case pays an interrupt per 4 KiB** — 65,536 of them for the same data, and **eight times the wall-clock time.** Same bytes, same disk; the difference is entirely per-request overhead.

---

## 3. DMA: The Device Does the Copying

**The CPU does not move the data.** It writes a **descriptor** — where in memory, how much, which direction — into a queue the device reads, and rings a doorbell. **The device transfers the bytes over the bus into memory directly**, and raises the interrupt only when it is done.

**What the CPU still must do:**

- **Set up the buffer** so the device can reach it: physical addresses, and pages that cannot move.
- **Handle cache coherence** — on x86 the hardware does this; on other architectures the driver must flush or invalidate.
- **Deal with the completion**: find which request finished, wake whoever was waiting.

**xv6's IDE driver is this, in miniature and without DMA**: `idestart` writes the sector number and command to the controller's ports, the process sleeps, and `ideintr` — the interrupt handler — copies the sector **word by word with `insl`** and calls `wakeup`. **The CPU does the copying**, which is exactly what DMA exists to stop.

---

## 4. Polling Came Back

**At 90 µs per I/O, sleeping is obviously right**: the context switch costs 3 µs (L17 §5) and the CPU gets 87 µs of other work.

**But this machine's SSD can serve a 4 KiB read in about 90 µs including software, and the fastest NVMe devices are nearer 10 µs** — and an interrupt plus a wake-up plus a switch is a few microseconds of that. **When the device becomes fast enough, the interrupt is the overhead**, and the kernel offers to poll instead:

```
$ cat /sys/block/nvme0n1/queue/io_poll
0
```

**Off here**, as it usually is, because polling costs a whole CPU per queue. **The rule is OSTEP's**, with modern numbers: **poll when the wait is shorter than the cost of switching away twice.**

---

## 5. The Block Layer

**Between the file system and the driver sits a queue** — and on this machine, eight of them:

```
  scheduler        [none] mq-deadline
  nr_requests      1023
  max_sectors_kb   128
  rotational       0
  hardware queues  8
  queue depth      1023 per queue
```

**Each CPU has its own submission queue**, so two CPUs submitting I/O do not contend for one lock — the change that made Linux scale on SSDs. **The scheduler is `none`.** On a rotating disk, reordering requests to minimise seeks was everything (OSTEP 37: SSTF, SCAN, the elevator); **on a device with no seek and 1,023-deep queues, reordering mostly adds latency**, so the default is to submit in order and let the device sort it out.

**What the block layer still does:**

- **Merging** adjacent requests — `/proc/diskstats` shows this machine has merged **1,071,768 writes** since boot, against 337,872 issued.
- **Splitting** requests larger than `max_sectors_kb`, which §2 counted.
- **Accounting** — every number in `/proc/diskstats` and `iostat`.
- **Fairness and priority**, when a scheduler is selected.

---

## 6. Interrupt Handlers May Not Sleep

**An interrupt handler runs on whatever process happened to be running**, on that CPU's stack, with no process context of its own. **So it may not sleep**: there is nothing sensible to wake, and the interrupted process would be blocked for someone else's reason.

**That single rule shapes every driver:**

- **xv6's `ideintr` calls `wakeup`, never `sleep`** — it hands the work to the process that was waiting.
- **It takes a spinlock, never a sleeping lock** (Week 3 L11), and the lock's holder must therefore disable interrupts on that CPU — which is why `acquire` does exactly that (L10 §6).
- **Linux splits handlers in two**: a **top half** that acknowledges the device and queues work, and a **bottom half** — softirq, tasklet or workqueue — that may do the rest later, and in the workqueue case may sleep.

**The measured consequence is in §2's table**: 65,536 interrupts for 256 MiB, each one stealing a CPU from whatever was running, each one unable to do anything but wake somebody.

---

## 7. What to Take Away

1. **A driver's problem is what to do while the device works**: poll, take an interrupt, or let DMA do the transfer.
2. **Interrupts are counted per command, not per byte**: measured, **one per 128 KiB request** and **one per 4 KiB request** — the same 256 MiB costing 1,969 or 65,536 interrupts, and 0.14 s or 1.1 s.
3. **DMA removes the copy from the CPU**; xv6's IDE driver, which copies with `insl` in the handler, shows what that is worth.
4. **Polling returned** for devices fast enough that an interrupt costs more than the wait.
5. **The block layer is per-CPU queues, merging, splitting and accounting** — with **no scheduler by default** on a device with no seek.
6. **An interrupt handler may not sleep**, which forces the top-half/bottom-half split and the spinlock discipline of Week 3.

---

## Exercises

1. From §2: **why does the 4 KiB run take eight times as long** as the 1 MiB run for the same bytes, when both read at the same rate per command?
2. A device completes in 5 µs. An interrupt plus wake-up plus switch costs 4 µs, and polling costs the CPU the whole wait. **Which is cheaper, and at what device latency do they cross?**
3. `max_sectors_kb` is 128. **What happens to §2's interrupt count if it is raised to 1024**, and what does that cost in latency for a small request queued behind a large one?
4. xv6's `ideintr` copies 512 bytes with `insl` while holding `idelock` with interrupts disabled. **Estimate the time that takes**, and say what it delays.
5. The block layer merges adjacent writes — over a million of them on this machine. **Which layer above it made merging possible**, and what would `fsync` do to the merge rate?

---

*CS 202 · Week 9 · L29 · © CSE Department*
