# CS 202 · Lab 1
## Reading the Process Table
### Week 1 · sat **Tuesday of Week 2**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 1** and is sat on the **Tuesday of Week 2**, because this course's lab day
> comes before two of the week's three lectures. Lab *N* is always sat in Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** reading the kernel's own records of running processes — yours, other people's, and xv6's — and checking every number against what you know the process did. By the end you will have seen address space that is not memory, a process that is asleep and cannot be woken, a file whose permission bits lie, and two xv6 processes quietly sharing one floating-point register.

**Everything in this lab is reading.** You will not change the kernel. The skill is to predict what a record will say before you read it, and to explain every number that surprises you.

---

## 0. Setup (5 minutes)

```bash
W1="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week1"
mkdir -p "$CS202/week1/lab1" && cd "$CS202/week1/lab1"
cp "$W1/resources/"{layout.c,rss.c,states.c,hog.c} .
cp "$W1/lab/"{spin.c,fpu.c} .
for p in layout rss states hog; do gcc -O2 -Wall -Wextra -o $p $p.c; done
```

If `$ACADEMICS` or `$CS202` is empty, Lab 0 §0 sets them.

---

## 1. Part A — Your Own Map (20 min)

```bash
MAPS=1 ./layout
```

`layout` prints the address of nine things, then its own `/proc/<pid>/maps`.

**Q1.** For each of the nine addresses, **find the line of `maps` that contains it** and write down that line's permissions and what it is backed by — the program file, `libc.so.6`, `[heap]`, `[stack]`, `[vdso]`, or nothing. **Two of the nine are in regions with no name at all.** Which, and why do they have none?

Now run it three times without `MAPS`, and twice under `setarch -R`:

```bash
for i in 1 2 3; do ./layout | head -1; done
setarch -R ./layout | head -1; setarch -R ./layout | head -1
```

**Q2.** Across the three normal runs, **which hex digits of `main`'s address never change?** Give the reason in one sentence. Then give the address under `setarch -R` and say what `-R` turned off, and why a debugger wants it off.

---

## 2. Part B — Address Space Is Not Memory (15 min)

```bash
./rss
```

**Q3. Predict first**, before you run it: after the `mmap` of 256 MiB and before anything is touched, what will `VmSize` and `VmRSS` each have done? Then run it, and explain the table line by line. **Finally, change the `memset` in `rss.c` to a loop that only *reads* one byte per page, and predict `VmRSS` again.** Run it. *(Week 5 explains the answer fully; you can already give the name of the page every read got.)*

---

## 3. Part C — States and Switches (20 min)

```bash
./states
./hog
```

`states` puts processes in six different states and reads each back from `/proc/<pid>/stat`.

**Q4.** One of them is in state **D**. Say what it is doing, and **why the kernel will not let even `SIGKILL` interrupt it** — what would the child be left with if the parent were killed mid-`vfork`? *(`man 2 vfork`, the paragraph on what the child shares.)*

`hog` pins a CPU-bound child and a sleeping child to the same CPU for five seconds.

**Q5.** Report both children's voluntary and involuntary counts. **Explain why each pair is lopsided in the opposite direction**, and why the two large numbers are close to each other.

---

## 4. Part D — Somebody Else's Table (20 min)

PID 1 belongs to root. Try:

```bash
grep -E '^(Name|Uid|CapEff)' /proc/1/status
ls -l /proc/1/maps /proc/1/environ
head -2 /proc/1/maps
cat /proc/1/environ
```

**Q6.** `status` is readable. `environ` is not, and its permission bits say so. **`maps` shows `-r--r--r--` — readable by everyone — and you still get `Permission denied`.** Explain: what check is the kernel making that the permission bits do not show, and why would a process's memory map be sensitive? *(L06 §2 is one reason. `man 5 proc`, under `/proc/pid/maps`, names the check.)*

Now a program that holds a privilege, and gives it up:

```bash
getcap /usr/bin/ping
ping -c 5 127.0.0.1 > /dev/null &
sleep 1; grep -E '^Cap(Prm|Eff)' /proc/$(pgrep -n -x ping)/status
```

**Q7.** What capability does the file grant, and what does the running process hold one second later? What did `ping` do in between, and why is it unable to change its mind?

---

## 5. Part E — xv6's Table (25 min)

In your xv6 tree from Lab 0, add both programs to `UPROGS` and boot with **one CPU**.

> **First check your tree has both of Lab 0's `Makefile` fixes.** `grep -- '-smp' Makefile` must
> show `sockets=$(CPUS)`. If it does not, your xv6 has been running on one CPU since Lab 0 —
> apply the second `sed` from Lab 0 Part D now. Today's first run is on one CPU on purpose; the
> last question is on two.

```bash
cd "$CS202/xv6"
grep -- '-smp' Makefile                  # must mention sockets=$(CPUS)
cp ../week1/lab1/{spin.c,fpu.c} .
sed -i 's/^\t_zombie\\$/\t_zombie\\\n\t_spin\\\n\t_fpu\\/' Makefile
grep -n '_spin\|_fpu' Makefile          # two lines inside UPROGS
make qemu-nox CPUS=1
```

At the xv6 prompt:

```
$ spin &
$ spin &
```

Then press **Ctrl-P**. Wait two seconds and press it again.

**Q8.** Copy both listings. **How many processes are `run` and how many `runble`, and does it change between the two listings?** Why can there never be more than one `run` in this boot? Then look at the sleeping `sh` line: what are the hexadecimal numbers after its name, and roughly where would you look them up? *(`kernel.sym`, or `addr2line -e kernel`.)*

Kill the spinners by rebooting — Ctrl-A X, then `make qemu-nox CPUS=1` again — and run:

```
$ fpu
```

The two processes' lines are printed one character at a time and will be interleaved. Untangle them.

**Q9.** Each process should finish at `x*2 = 20000000`. Report both final values, **add them**, and run `fpu` a second time. **Explain the sum** — where the variable `x` lived during the loop, and what xv6's context switch did and did not save. *(L05 §6.)*

Now reboot with two CPUs — Ctrl-A X, then `make qemu-nox CPUS=2` — **check that `cpu1: starting 1` appears at boot**, and run `fpu` twice more.

**Q10.** Report both runs. **Is the bug fixed?** Say what changed and what did not, and why a bug that shows up less often on more CPUs is harder to deal with than one that shows up every time.

---

## 6. Checkoff

Show the TA:

- [ ] `MAPS=1 ./layout` with each of the nine addresses matched to its `maps` line.
- [ ] `./states` output with the `D` explained.
- [ ] xv6 Ctrl-P output with two `spin`s, and `fpu`'s two numbers with their sum.
- [ ] Your written answers to **Q2, Q6 and Q9** — three or four sentences each.

**Take with you:** PS 1's `pm` reads the same `/proc` files you read by hand today — parse `stat` the way Q1's output taught you to trust it, which is not at all. And the FPU sum in Q9 is PS 1 Q4's starting point.

---

*CS 202 · Week 1 · Lab 1 · © CSE Department*
