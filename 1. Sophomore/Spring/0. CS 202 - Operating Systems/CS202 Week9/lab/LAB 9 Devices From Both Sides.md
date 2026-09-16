# CS 202 · Lab 9
## Devices, From Both Sides
### Week 9 · sat **Tuesday of Week 10**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 9** and is sat on the **Tuesday of Week 10**. Lab *N* is always sat in
> Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** measuring what it costs to reach a device from a program, counting the interrupts a disk raises for the same data at two request sizes, and then running a driver you wrote — in xv6, where you are allowed to.

**The curriculum asks you to load a kernel module and write to it from user space.** **You cannot load one on BH 210**, and Part A measures exactly why. **Part D is the same device, in the kernel you own.**

---

## 0. Setup (5 minutes)

```bash
W9="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week9"
mkdir -p "$CS202/week9/lab9" && cd "$CS202/week9/lab9"
cp "$W9/lab/devcost.c" . && cp -r "$W9/assignments/ps9/linux" .
gcc -O2 -Wall -Wextra -o devcost devcost.c
```

---

## 1. Part A — The Module That Will Not Load (20 min)

```bash
cd linux && make && ls -la cs202ring.ko && modinfo cs202ring.ko | head -8
size cs202ring.ko
insmod cs202ring.ko
lsmod | head -5
cd ..
```

**Q1.** **How large is the `.ko`, and what does `size` say is actually code?** Where is the rest? *(Look at `modinfo`'s fields and at `objdump -h`.)*

**Q2.** Report the `insmod` error exactly. **Which capability does loading need**, and what could a module do that makes it equivalent to owning the machine? **Name two things you *can* still do without it**, from the commands above.

**Q3.** `modinfo` shows a `vermagic` line. **What is it for, and what happens if it does not match the running kernel?** Why does a module built for 7.0.0-31 not simply work on 7.0.0-30?

---

## 2. Part B — What Reaching a Device Costs (25 min)

```bash
taskset -c 2 ./devcost
```

**Q4.** Report the table. **`/dev/null`'s driver does nothing. Explain its cost**, naming each component you can. Compare with Week 0's measured cost of `getppid` on this machine, and say what the difference is.

**Q5.** Compare the 4-byte and 4 KiB columns for `/dev/zero` and `/dev/urandom`. **Give the per-byte cost of each device's own work**, and say which of the two would benefit from `mmap` instead of `read`, and why.

**Q6.** The `ioctl` in the program returns `ENOTTY` every time. **It is still the fastest line in the table. What does that tell you** about where the time in the other lines goes?

---

## 3. Part C — Counting Interrupts (25 min)

```bash
grep -E "nvme|i8042" /proc/interrupts
dd if=/dev/urandom of=io.bin bs=1M count=256 status=none && sync
A=$(grep nvme0q /proc/interrupts | awk '{for(i=2;i<=NF-3;i++) s+=$i} END {print s}')
dd if=io.bin of=/dev/null bs=1M iflag=direct status=none
B=$(grep nvme0q /proc/interrupts | awk '{for(i=2;i<=NF-3;i++) s+=$i} END {print s}')
echo "1 MiB reads: $((B-A)) interrupts"
# repeat with bs=4k
```

**Q7.** **Report both interrupt counts and both elapsed times** for the same 256 MiB. **Divide each by the number of requests**: what is the interrupt-per-request ratio in each case?

**Q8.** With 1 MiB reads you should see far fewer than 256 interrupts per 256 MiB, but more than 256 ÷ 1. **Find `max_sectors_kb` in `/sys/block/nvme0n1/queue/` and explain the number exactly.**

**Q9.** Look at `/sys/block/nvme0n1/queue/scheduler` and count `/sys/block/nvme0n1/mq/*`. **Why is the default scheduler `none` here**, and what is the point of one queue per CPU? *(L29 §5.)*

---

## 4. Part D — A Driver You Can Run (25 min)

Use your PS 9 xv6 tree — or the skeleton, if PS 9 is not done yet.

```bash
make qemu-nox
$ ringtest 300
```

**Q10.** Report the output. **The test's child sleeps 20 ticks before opening the device.** What does that prove about where the parent was during those ticks, and which two lines of your driver put it there?

**Now break it on purpose**, one change at a time, rebuilding between each:

1. Delete the `wakeup(&ring.r)` from `ringwrite`.
2. Put the `sleep` back but change `while(ring.r == ring.w)` to `if(ring.r == ring.w)`.
3. Have `ringread` return `n` instead of the number of bytes it copied.

**Q11.** **For each, say what happened when you ran `ringtest`**, and name the Week 3 or Week 4 concept it is an instance of. **Which of the three is worst, and why?** *(Consider what a program that trusted the return value would then do.)*

---

## 5. Checkoff

Show the TA:

- [ ] Your `insmod` refusal and your answer to **Q2**.
- [ ] Your `devcost` table with the per-byte costs (**Q4, Q5**).
- [ ] Both interrupt counts and your explanation of `max_sectors_kb` (**Q7, Q8**).
- [ ] `ringtest` passing, and your three broken versions with their symptoms (**Q10, Q11**).

**Take with you:** **Project 2** extends the kernel you just wrote a driver in, and **Week 10** asks what happens when the whole machine is itself a program.

---

*CS 202 · Week 9 · Lab 9 · © CSE Department*
