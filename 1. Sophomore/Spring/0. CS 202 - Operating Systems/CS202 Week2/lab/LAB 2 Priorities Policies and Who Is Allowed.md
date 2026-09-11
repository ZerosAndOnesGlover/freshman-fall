# CS 202 · Lab 2
## Priorities, Policies, and Who Is Allowed
### Week 2 · sat **Tuesday of Week 3**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 2** and is sat on the **Tuesday of Week 3**. Lab *N* is always sat in
> Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.

**What you are doing:** telling the Linux scheduler what you want with `nice`, `chrt` and `taskset`, and measuring whether it listened. It will listen to exactly the right degree for some requests, refuse others outright, and — for one setting that is switched on — do nothing at all. **Each of those is a result.**

**The curriculum's version of this lab** has you raise processes to real-time priority with `chrt`. A student account on BH 210 is not permitted to — the refusal is Part B — so the lab measures the policies you are allowed, and the reason for the ones you are not.

---

## 0. Setup (5 minutes)

```bash
W2="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week2"
mkdir -p "$CS202/week2/lab2" && cd "$CS202/week2/lab2"
cp "$W2/lab/"{hog.c,cpushare.sh} "$W2/resources/"{slice.c,lat.c} .
gcc -O2 -Wall -Wextra -o hog hog.c
gcc -O2 -Wall -Wextra -o slice slice.c
gcc -O2 -Wall -Wextra -o lat lat.c
chmod +x cpushare.sh
nproc                        # every experiment pins to CPU 6 or 7; use a lower number if you have fewer
```

`cpushare.sh 4 <pid> <pid>…` reads each process's CPU time from `/proc` before and after four seconds, and prints each one's share. **Read it before you use it** — it is twenty lines.

**Always clean up.** A forgotten `hog` burns a CPU until the machine reboots. `pkill -x hog` between parts.

---

## 1. Part A — `nice`, Measured (20 min)

Start two hogs on the same CPU:

```bash
taskset -c 6 ./hog & A=$!
taskset -c 6 ./hog & B=$!
./cpushare.sh 4 $A $B
```

They should split the CPU roughly equally. Now make B nicer, one step at a time, measuring after each:

```bash
renice -n 1  -p $B; ./cpushare.sh 4 $A $B
renice -n 5  -p $B; ./cpushare.sh 4 $A $B
renice -n 10 -p $B; ./cpushare.sh 4 $A $B
renice -n 19 -p $B; ./cpushare.sh 4 $A $B
```

**Q1.** Tabulate B's share at nice 0, 1, 5, 10 and 19. Linux's weights are nice 0 = 1,024, 1 = 820, 5 = 335, 10 = 110, 19 = 15. **Compute the share the weights predict** for each row and compare. How far off is the worst row?

Now try to undo it:

```bash
renice -n 0 -p $B
ulimit -e
```

**Q2.** What happened, and what does `ulimit -e` print? **Explain why a system lets you make your own process nicer but not less nice** — describe what a user could do to other users if lowering nice were unrestricted. Then `pkill -x hog`.

---

## 2. Part B — Policies, and Refusals (15 min)

```bash
chrt -m
ulimit -r
chrt -f 10 ./hog
chrt -d --sched-runtime 1000000 --sched-deadline 10000000 --sched-period 10000000 0 ./hog
```

Both `chrt` commands should fail immediately. **Now the policies you are allowed:**

```bash
taskset -c 6 ./hog & A=$!
taskset -c 6 chrt -i 0 ./hog & B=$!
./cpushare.sh 4 $A $B
pkill -x hog
cat /proc/sys/kernel/sched_rt_runtime_us /proc/sys/kernel/sched_rt_period_us
```

**Q3.** Report the error from each refused `chrt`, and the value of `ulimit -r`. Report B's share under `SCHED_IDLE`, and **say what weight it implies**. Finally, the two `sched_rt_*` values: **what do they limit, and why would the kernel limit root's real-time tasks too?**

---

## 3. Part C — Groups: a Setting That Does Nothing, and One That Overrides `nice` (20 min)

```bash
cat /proc/sys/kernel/sched_autogroup_enabled
cat /proc/self/autogroup
```

**Autogroup** is supposed to give each *session* its own share of the CPU, so that a nice-19 hog in its own session gets half a CPU against a nice-0 hog in yours. Test it:

```bash
taskset -c 6 ./hog & A=$!
setsid taskset -c 6 nice -n 19 ./hog & sleep 0.5; B=$(pgrep -n -x hog)
grep -H . /proc/$A/autogroup /proc/$B/autogroup      # different sessions, different autogroups
./cpushare.sh 4 $A $B
pkill -x hog
```

**Now find out where your processes live:**

```bash
cat /proc/self/cgroup
CG=$(sed -n 's/^0:://p' /proc/self/cgroup); p=""
for part in $(echo "$CG" | tr '/' ' '); do
    echo "/sys/fs/cgroup$p: $(cat /sys/fs/cgroup$p/cgroup.subtree_control)"; p="$p/$part"
done
```

*(Your path will differ from the lecture's — it depends on how you logged in. The shape will not.)*

**Q4.** Did autogroup change B's share? **Using the `subtree_control` list**, find the deepest cgroup on your path that has the `cpu` controller enabled for its children, and explain why autogroup has no effect on your processes. *(L08 §7.)*

**Now put B in a cgroup of its own, with a CPU weight:**

```bash
taskset -c 6 ./hog & A=$!
systemd-run --user --scope -p CPUWeight=100 taskset -c 6 nice -n 19 ./hog &
sleep 1; B=$(pgrep -x hog | grep -v "^$A$" | tail -1)
sed -n 's/^0:://p' /proc/$B/cgroup
cat "/sys/fs/cgroup$(dirname $(sed -n 's/^0:://p' /proc/$B/cgroup))/cgroup.subtree_control"
./cpushare.sh 4 $A $B
pkill -x hog
```

**Q5.** Report B's share now, **at nice 19**. Report the `subtree_control` of B's parent cgroup while it ran, and again after `pkill`. **Explain in three sentences** how a nice-19 process came to get about half a CPU, and what that means for the usefulness of `nice` on a machine where every service is in its own cgroup.

---

## 4. Part D — How Long Is a Slice? (15 min)

```bash
grep se.slice /proc/self/sched
./slice 2
./slice 3
./slice 4
```

**Q6.** Tabulate the median run length and the median time off the CPU for 2, 3 and 4 hogs. **Which one depends on the number of hogs, and which does not?** `se.slice` is 2,800,000 ns; explain why the measured run length is 3.00 ms, using `grep CONFIG_HZ= /boot/config-$(uname -r)`.

---

## 5. Part E — How Late Is "Now"? (20 min)

```bash
cat /proc/self/timerslack_ns
./lat
./lat slack
for s in /sys/devices/system/cpu/cpu7/cpuidle/state*; do
    printf "%-8s %-8s latency %5s us\n" $(basename $s) "$(cat $s/name)" "$(cat $s/latency)"
done
```

`lat` asks to wake every millisecond and reports how late it was: alone on CPU 7, then with three hogs of different kinds. `lat slack` does the same with its timer slack reduced to 1 ns.

**Q7.** Report both tables. **Account for the busy-CPU median** — why is it about 54 µs in the first table and about 4 µs in the second? **Account for the no-competition median** — why is it *later* than with three hogs, in both tables? Use the `cpuidle` listing.

**Q8.** The hogs at nice 0 did not make the sleeper's median later. **Why not?** Use what L08 said about `vruntime` for a task that sleeps most of the time.

---

## 6. Checkoff

Show the TA:

- [ ] Your Part A table next to the weights' predictions.
- [ ] The two refused `chrt` commands and `ulimit -r`.
- [ ] Your `subtree_control` walk, and B's share in both halves of Part C.
- [ ] Your written answers to **Q2, Q5 and Q7** — three or four sentences each.

**Before you leave: `pgrep -x hog` must print nothing.**

**Take with you:** PS 2's fair model predicts Part A's shares, and PS 2 Q5 asks why it does not predict Part D's slices.

---

*CS 202 · Week 2 · Lab 2 · © CSE Department*
