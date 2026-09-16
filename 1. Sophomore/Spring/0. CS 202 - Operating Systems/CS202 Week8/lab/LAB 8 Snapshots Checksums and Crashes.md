# CS 202 · Lab 8
## Snapshots, Checksums, and Crashes
### Week 8 · sat **Tuesday of Week 9**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 8** and is sat on the **Tuesday of Week 9**. Lab *N* is always sat in
> Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** making copy-on-write snapshots and measuring what they cost, corrupting a file system on purpose and finding out what it notices, and crashing a file system at every possible moment to see which designs survive.

**The curriculum asks you to use ZFS snapshots and measure their cost.** **ZFS and btrfs are not installed on the lab machines** — both need kernel modules and root. Part B measures the same mechanism in a place an ordinary account can reach: **`qcow2` images, which are copy-on-write with a backing file.**

---

## 0. Setup (5 minutes)

```bash
W8="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week8"
mkdir -p "$CS202/week8/lab8" && cd "$CS202/week8/lab8"
cp "$W8/lab/crashsweep.sh" . && chmod +x crashsweep.sh
cp "$W8/assignments/ps8/myfsj.c" .        # your PS 8 version if you have one
gcc -O2 -Wall -Wextra -o myfsj myfsj.c
which qemu-img qemu-io mkfs.ext4 debugfs e2fsck
```

---

## 1. Part A — The Tools You Do Not Have (10 min)

```bash
zfs list; btrfs --version
cp --reflink=always myfsj.c copy.c
```

**Q1.** Report all three. **What does `cp --reflink` ask the file system to do**, and why can ext4 not do it? Name **two** file systems that can, and say what they have in common with `qcow2` (§2).

---

## 2. Part B — Copy-on-Write, Measured (30 min)

```bash
qemu-img create -f qcow2 base.qcow2 256M
qemu-io -f qcow2 -c "write -P 0xaa 0 64M" base.qcow2
ls -s --block-size=1K base.qcow2
qemu-img create -f qcow2 -b base.qcow2 -F qcow2 over.qcow2
ls -s --block-size=1K over.qcow2
qemu-img info --backing-chain over.qcow2
```

**Q2.** **How big is a snapshot of a 64 MiB image?** Read one region of the overlay that has never been written — `qemu-io -f qcow2 -c "read -P 0xaa 1M 4k" over.qcow2` — and say **where that data came from** and how the format knows.

**Now write into the overlay:**

```bash
for i in $(seq 0 63); do off=$(( (i * 997 % 16384) * 4096 )); printf ' -c "write -P 0x55 %d 4k"' $off; done \
  | xargs -I{} sh -c 'eval qemu-io -f qcow2 {} over.qcow2 > /dev/null'
ls -s --block-size=1K over.qcow2
```

**Q3.** **You wrote 256 KiB. How much did the overlay grow?** Explain the ratio from `qemu-img info`'s `cluster_size`. Then **repeat the whole experiment with `-o cluster_size=4096`** on both images and report the new growth. **Which cluster size would you choose for a database that writes 8 KiB pages, and what does the other choice buy?**

**Q4.** **Time 200 scattered 4 KiB writes into the base, and into an overlay on top of it** *(`date +%s.%N` around the `qemu-io` run)*. **Report both and the ratio.** What work does the overlay do that the base does not?

---

## 3. Part C — What a File System Notices (25 min)

```bash
truncate -s 32M fs.img && mkfs.ext4 -q -F -b 1024 fs.img
printf 'the quick brown fox\n' > f.txt
debugfs -w -R "write f.txt hello.txt" fs.img
e2fsck -fn fs.img                                   # clean
dumpe2fs fs.img | grep -m1 "Inode table at"          # note the block number
```

**Corrupt one byte of the inode table** with a few lines of Python (open the image, seek to `block × 1024 + 60`, read a byte, write it back XORed with 0xFF), then:

```bash
e2fsck -fn fs.img
```

**Q5.** Report what `e2fsck` says. **What made the detection possible?** *(`dumpe2fs -h` — look for a feature flag.)*

**Now do the same to a file's data**: put a 64 KiB file in a fresh image, find its first block with `debugfs -R "blocks data.bin"`, flip one byte of **that** block, and then:

```bash
e2fsck -fn fs2.img
debugfs -R "dump data.bin /dev/stdout" fs2.img | xxd | head -1
```

**Q6.** **What does `e2fsck` say now, and what does the file contain?** Explain the difference from Q5 in one sentence. **What would a file system have to store to catch this**, and where would ZFS put it? *(L27 §4–§5.)*

---

## 4. Part D — Crashing on Purpose (25 min)

```bash
./myfsj base.img format 2048 && ./myfsj base.img mkdir /d && ./myfsj base.img create /d/x
./myfsj base.img write /d/x 4096 41
./crashsweep.sh ./myfsj base.img recover create /d/y
./crashsweep.sh ./myfsj base.img recover write /d/x 8192 43
./crashsweep.sh ./myfsj base.img norecover write /d/x 8192 43
```

**Q7.** Report the three lines. **With recovery, how many crash points left the file system inconsistent?** Without it? **Where in L26 §1's four steps do the failures fall**, and why can they only fall there?

**Q8.** **Find the exact crash point at which the operation becomes durable** — the largest *N* whose image recovers to the *old* file, and the smallest that recovers to the *new* one. **What single block write is the boundary?** Show the `logdump` on either side of it.

**Q9.** Build the **unjournaled** file system — your PS 7 `myfs`, or the instructor copy — and sweep the same two operations, checking with **this week's `fsck`**. **Report the counts and the kinds of damage.** For one inconsistent image, say **exactly which write was missed** and why that produces the damage you see.

---

## 5. Checkoff

Show the TA:

- [ ] Your Part B table: snapshot size, growth per 256 KiB written, at both cluster sizes (**Q2, Q3**).
- [ ] Both `e2fsck` results from Part C, with your one-sentence explanation (**Q5, Q6**).
- [ ] Your three sweep lines and the durability boundary (**Q7, Q8**).
- [ ] Your written answer to **Q9**.

**Take with you:** **PS 8** is Part D's journal, written by you, and **Week 9** goes below the file system to the device it has been writing to all term.

---

*CS 202 · Week 8 · Lab 8 · © CSE Department*
