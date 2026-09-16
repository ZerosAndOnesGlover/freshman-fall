# CS 202 · Lab 7
## Watching the Page Cache
### Week 7 · sat **Tuesday of Week 8**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 7** and is sat on the **Tuesday of Week 8** — **the day after Midterm 2, and
> the first week back from Spring Break.** Lab *N* is always sat in Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** watching the kernel cache a file, guess what you will read next, hold your writes in memory, and finally put them on the disk — **and measuring what each of those is worth.**

**The curriculum asks you to instrument the page cache with `bpftrace`.** Part A finds out why you cannot, and what an ordinary account can use instead: **`mincore()` to ask which pages of a file are cached, and `posix_fadvise()` to drop them.**

---

## 0. Setup (5 minutes)

```bash
W7="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week7"
mkdir -p "$CS202/week7/lab7" && cd "$CS202/week7/lab7"
cp "$W7/lab/pcache.c" "$W7/lab/durable.c" .
gcc -O2 -Wall -Wextra -o pcache pcache.c
gcc -O2 -Wall -Wextra -o durable durable.c
dd if=/dev/urandom of=big.bin bs=1M count=512 status=none
```

**`big.bin` must be bigger than anything the machine will keep cached by accident, and it must not be compressible** — hence `/dev/urandom`.

---

## 1. Part A — The Tool You Cannot Use (10 min)

```bash
bpftrace -e 'BEGIN { printf("hi\n"); exit(); }'
echo 1 > /proc/sys/vm/drop_caches
man 2 mincore | head -20
man 2 posix_fadvise | grep -A3 DONTNEED
```

**Q1.** Report both refusals. **What would `bpftrace` need**, and why is it reasonable for a shared machine not to give it? Then say what `mincore` and `posix_fadvise(POSIX_FADV_DONTNEED)` let you do **without** it — and what they cannot do that `bpftrace` could. *(Whose pages can you drop?)*

---

## 2. Part B — What the Cache Holds (25 min)

```bash
./pcache big.bin
```

Read the program first: it drops the file's pages, reads one byte, reads the file sequentially, then reads it randomly — cold and warm — reporting residency from `mincore` at each step.

**Q2.** Report the output. **How many pages did the single one-byte read bring in, and how many bytes is that?** Compare with `/sys/block/*/queue/read_ahead_kb`, and explain why the kernel did not read the maximum.

**Q3.** The program then reads pages 0, 1, 2, … one at a time and prints how many pages are resident after each. **Report the sequence and explain its shape.** At what point does the kernel decide this is a sequential read?

**Q4.** **Give the four read costs** — sequential cold, sequential warm, random cold, random warm — **and the ratio between each pair.** Which of the four is limited by the SSD, which by the CPU, and which by neither? *(L23 §1.)*

**Q5.** Compare `Cached` in `/proc/meminfo` before and after the sequential read:

```bash
grep -E '^Cached|^Dirty' /proc/meminfo; ./pcache big.bin > /dev/null; grep -E '^Cached|^Dirty' /proc/meminfo
```

**Did `Cached` rise by 512 MiB?** If not, where did the rest go? *(Week 6 §L19 §2 — what competes for those frames?)*

---

## 3. Part C — Writes That Have Not Happened Yet (25 min)

```bash
./durable .
```

**Q6.** Report the first line. **64 MiB was "written" faster than this SSD can write. Explain**, using the `Dirty` numbers the program prints, and say when that data would have reached the disk if the program had not called `fsync`. *(`/proc/sys/vm/dirty_expire_centisecs`, `dirty_background_ratio`.)*

**Q7.** Report the table of 4 KiB writes. **Give the cost of durability as a ratio**, and explain why `O_DIRECT` without a sync is ten times slower than a buffered write but a hundred times faster than an `fsync`. **What is `O_DIRECT` actually bypassing, and what is `fsync` actually waiting for?**

**Q8.** Watch write-back happen. **Sample for at least 40 seconds, and do not delete the file until the sampling is over** — deleting it throws its dirty pages away instead of writing them:

```bash
( dd if=/dev/zero of=w.bin bs=1M count=256 status=none ; ) &
for i in $(seq 40); do grep -E '^Dirty|^Writeback:' /proc/meminfo | awk '{printf "%s%s ", $1, $2}'; echo "t=${i}s"; sleep 1; done
rm -f w.bin
```

**Report the sequence.** **How long did `Dirty` stay at its peak, and what setting explains that interval?** *(`/proc/sys/vm/dirty_expire_centisecs`.)* **What is the difference between `Dirty` and `Writeback`**, and why is `Writeback` almost always 0 in your samples even though 256 MiB certainly reached the disk?

---

## 4. Part D — The Safe Update (20 min)

Write a short program, `safeupdate.c`, that replaces the contents of a file the way L23 §5 describes: write a temporary file, `fsync` it, `rename` it over the target, then `fsync` the directory. **Time all four steps separately**, for a 1 MiB payload.

**Q9.** Report the four times. **Which dominates?** Now remove the directory `fsync` and time it again — **does the total change measurably?** Explain why the step is nevertheless required, by describing the state a crash could leave.

**Q10.** `rename` is atomic: a reader sees either the old file or the new one, never a mixture. **What would go wrong if you instead opened the target with `O_TRUNC` and wrote it in place?** Give the two distinct failures — one that a reader sees, and one that a crash causes.

---

## 5. Checkoff

Show the TA:

- [ ] Your `pcache` output with the readahead sequence, and your answers to **Q2 and Q3**.
- [ ] Your four read costs and ratios (**Q4**).
- [ ] Your `Dirty`/`Writeback` sequence (**Q8**).
- [ ] Your `safeupdate.c`, its four timings, and your answer to **Q10**.

**Take with you:** **PS 7** builds the file system whose blocks this cache holds, and **Week 8** asks what happens when the machine loses power between two of those writes.

---

*CS 202 · Week 7 · Lab 7 · © CSE Department*
