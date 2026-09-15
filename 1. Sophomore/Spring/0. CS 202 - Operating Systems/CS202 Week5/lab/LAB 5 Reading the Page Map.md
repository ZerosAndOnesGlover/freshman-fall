# CS 202 · Lab 5
## Reading the Page Map
### Week 5 · sat **Tuesday of Week 6**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 5** and is sat on the **Tuesday of Week 6**. Lab *N* is always sat in
> Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** watching the kernel manage your pages — **as it does it**. `/proc/<pid>/pagemap` holds one 64-bit entry for every virtual page of a process, and you will read it while memory is demand-allocated, shared by `fork`, tracked for writes, and paged out.

**The curriculum asks you to "examine `/proc/pid/pagemap`"** — typically, to find the physical frame behind an address. **On BH 210 you cannot**, and Part A finds out why. **Everything else in the entry is there**, and it turns out to be the more interesting half.

---

## 0. Setup (5 minutes)

```bash
W5="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week5"
mkdir -p "$CS202/week5/lab5" && cd "$CS202/week5/lab5"
cp "$W5/lab/pmwalk.c" "$W5/lab/pmlab.c" .
gcc -O2 -Wall -Wextra -o pmwalk pmwalk.c
gcc -O2 -Wall -Wextra -o pmlab pmlab.c
man 5 proc_pid_pagemap        # keep it open: you need bits 63, 62, 56 and 55
```

**Read both programs first.** `pmwalk` summarises every mapping of a process; `pmlab` watches four pages of one fresh mapping. Neither is long.

---

## 1. Part A — What a Process's Map Holds (25 min)

```bash
./pmwalk
```

One line per mapping in `/proc/self/maps`: how many pages it spans, and how many of them are **present** (in RAM), **swapped**, **exclusive** (mapped by this process only), and present **with a nonzero frame number**.

**Q1.** Find the four or five `libc.so.6` lines. **Which is the code**, and how can you tell from the counts? *(Compare with `/proc/self/maps`' permission column.)* Why are **not all** of libc's code pages present, and why is **none** of them exclusive? Why are libc's last two mappings **entirely** exclusive?

**Q2.** Look at the last column and the last line. **Report the number of present pages with a nonzero frame number.** Using `man 5 proc_pid_pagemap` and L18 §7, **explain why**, and say what kind of process would see the real numbers.

**Now look at other processes:**

```bash
sleep 300 & ./pmwalk $! | tail -4
./pmwalk $(pgrep -u $USER -x pipewire | head -1) | tail -2      # or any process of yours your shell did not start
./pmwalk 1 | head -2
kill %1
```

**Q3.** **Which of the three can you read?** In Lab 4, `gdb -p` was refused on a process of your own. **Why is reading `pagemap` of a process your shell did not start allowed, when attaching `gdb` to it was not?** What rule refuses pid 1?

---

## 2. Part B — Memory on Demand (15 min)

```bash
./pmlab demand
```

Each page is shown as three characters: **`P`** present, **`S`** swapped or **`-`** neither; **`x`** exclusive; **`d`** soft-dirty. The last column is **the page faults the step itself took**.

**Q4.** Explain every line. **In particular:**
- Why is page 0 present after a *read*, but **not exclusive**? What frame is it mapped to?
- Why did the **write** to page 0 fault, when page 0 was already present?
- Page 1 was written without being read. **How many faults did that take, and why fewer than page 0's?**

**Q5.** A program `calloc`s 100 MiB, reads all of it to check it is zero, and then writes every byte. **How many page faults, and how many frames used after the read? After the writes?** *(Ignore huge pages.)*

---

## 3. Part C — Copy-on-Write (20 min)

```bash
./pmlab cow
```

**Q6.** Explain the child's three lines. **Why are all four pages present but none exclusive right after `fork`**, and why did only one child operation fault?

**Q7.** Now the parent's line after the child exits. **Page 1 is exclusive in the parent again, and reading it took no fault. Explain.** Would a **write** to page 1 by the parent now fault? **Predict, then check** by adding a step. *(Hint: what would the kernel have to do on a write fault to a page that only one process maps?)*

**Q8.** Before the `STEP` for the parent's read, the program writes `sink = 0`, with a comment. **Delete that line, rebuild, and run it three times.** What changes in the output, and **why**? *(What else did `fork` make read-only?)*

---

## 4. Part D — Tracking Writes (15 min)

```bash
./pmlab dirty
```

**Soft-dirty** is a bit the kernel keeps per page, **set when the page is written** — separately from the CPU's own dirty bit, which the kernel uses for itself. Writing `4` to `/proc/self/clear_refs` clears it for every page of the process.

**Q9.** Explain the lines. **Why did the write to page 2 fault**, when page 2 was present, writable and exclusive? *(How can the kernel find out about the next write to a page, if the CPU does not tell it?)* Why did the second write to page 2 not fault?

**Q10.** **Who would want this?** A tool that checkpoints a running process to disk — **CRIU** does exactly this — wants to save its memory repeatedly, while it keeps running. **Describe how it would use `clear_refs` and bit 55** to save only what changed since the last checkpoint.

---

## 5. Part E — Paging Out (15 min)

```bash
./pmlab pageout
```

`madvise(MADV_PAGEOUT)` asks the kernel to **reclaim** pages now — write them to swap and free their frames — as it would under memory pressure (Week 6).

**Q11.** Report the output. **What happened to the flags of pages 0 and 1?** Your entries for swapped pages carry a swap type and offset in the low bits (`man 5 proc_pid_pagemap`): **modify `pmlab` to print them** for swapped pages, and report what you see. Is that consistent with Part A?

**Q12.** Reading page 0 back took one fault and returned `'a'`. **Was it a major fault** — one that read the page from disk? Modify `faults()` to count `ru_majflt` separately, run it three times, and report. **If it was not a major fault, where was the page's content?** *(Look up the swap cache.)*

---

## 6. Part F — What the Tables Cost (10 min)

```bash
grep VmPTE /proc/self/status
for f in /proc/[0-9]*/status; do awk '/^Name:/{n=$2} /^VmRSS:/{r=$2} /^VmPTE:/{p=$2} END{if (p) print p, r, n}' $f 2>/dev/null; done | sort -n | tail -5
```

**Q13.** Report the five processes with the most page-table memory, with their resident memory. **What fraction of each process's memory is page tables?** Use L16 §7 to say whether that fraction is what you would expect for a process whose memory is dense.

---

## 7. Checkoff

Show the TA:

- [ ] `pmwalk` on your own process, and your answer to **Q2**.
- [ ] `pmlab cow` with your added parent write, and your answer to **Q7**.
- [ ] `pmlab pageout` printing swap types and offsets, and the major-fault count, with your answers to **Q11 and Q12**.
- [ ] Your written answers to **Q4, Q9 and Q13**.

**Take with you:** **PS 5** builds the structure these bits live in — a two-level page table with a TLB — and **Week 6** asks what the kernel does when Part E stops being voluntary.

---

*CS 202 · Week 5 · Lab 5 · © CSE Department*
