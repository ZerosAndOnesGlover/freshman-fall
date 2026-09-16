# CS 202 · Lab 10
## Boot a Machine You Wrote
### Week 10 · sat **Tuesday of Week 11**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 10** and is sat on the **Tuesday of Week 11**. Lab *N* is always sat in
> Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.
>
> **Project 1 is due this Friday.** Bring questions; the last half hour is for them.

**What you are doing:** starting a virtual machine from your own program, watching it leave, measuring what leaving costs, and building a device that does not exist. Then the comparison: the same guest under emulation and under hardware virtualization, and the other kind of isolation — the one this machine will not let you have.

---

## 0. Setup (5 minutes)

```bash
W10="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week10"
mkdir -p "$CS202/week10/lab10" && cd "$CS202/week10/lab10"
cp "$W10/lab/kvmprobe.c" "$W10/lab/vmsplit.c" . && cp "$W10/assignments/ps10/kvmhost.c" .   # your PS 10 version if you have one
for p in kvmprobe vmsplit kvmhost; do gcc -O2 -Wall -Wextra -o $p $p.c; done
ls -l /dev/kvm
```

---

## 1. Part A — What the Kernel Offers (15 min)

```bash
./kvmprobe
lsmod | grep ^kvm
grep -o 'vmx\|ept\|vpid\|unrestricted_guest' /proc/cpuinfo | sort -u
```

**Q1.** Report the API version, the `kvm_run` size, and the three `KVM_CAP` limits. **`NR_VCPUS` and `MAX_VCPUS` differ. What is each?**

**Q2.** `KVM_CREATE_VM` returned a small integer. **What kind of object is it**, and what does that make possible — name two things you can do to a VM because it is that kind of object.

**Q3.** `/dev/kvm` is a character device (Week 9). **Which of Week 9's structures does KVM fill in**, and which of its entries must KVM provide for `ioctl` to work at all?

---

## 2. Part B — A Guest of Your Own (20 min)

```bash
./kvmhost hello
```

**Q4.** Report the output and the exit count. **Why 21 exits for a 21-character string?**

**Now change the guest.** The string lives at guest physical `0x2000`; the code is fifteen hand-assembled bytes at `0x1000`.

**Q5.** Change the message to your own, rebuild, and report the new exit count. Then **make the guest print it twice** — you may add bytes to the guest code or change the host. **Say which you chose and why**, and show the diff.

---

## 3. Part C — The Cost of Leaving (25 min)

```bash
taskset -c 2 ./kvmhost exits 100000
taskset -c 2 ./kvmhost cpuid 65535
./vmsplit
```

**Q6.** Report the two exit costs, three runs each. **Give the ratio**, and explain what the slower one does that the faster one does not. **Where does the boundary lie in each case?**

**Q7.** `vmsplit` creates 500 VMs and then destroys them. **Report both costs per VM.** One is two orders of magnitude larger than the other — **which, and what is the kernel waiting for?** *(`grep -r synchronize_rcu` in the KVM sources is a hint you do not have; reason from what a VM owns.)*

**Q8.** From Q6 and Q7: **a workload creates a VM, runs 1,000 I/O operations in it, and destroys it.** Compute the total overhead, and say which term dominates. **What would you change first?**

---

## 4. Part D — A Device That Does Not Exist (20 min)

```bash
./kvmhost mmio
```

**Q9.** Report the MMIO exit line. **The guest wrote to `0x80000` and the region is 64 KiB. What would happen with a 1 MiB region**, and why? *(Try it: change `GUEST_MEM` and rerun.)*

**Q10.** **Make the exit do something.** In your host's MMIO case, keep a counter; on each write to `0x80000`, print the byte and the running count. **Show the code and the output.** Then say, in two sentences, **how a virtual disk differs from what you just wrote.**

---

## 5. Part E — Emulation, Virtualization, and Containers (20 min)

```bash
cd ~/xv6-public                                    # or wherever your Lab 0 xv6 is
time make qemu-nox                                  # TCG; quit with Ctrl-A X once the shell appears
time qemu-system-i386 -nographic -enable-kvm -drive file=fs.img,index=1,media=disk,format=raw \
     -drive file=xv6.img,index=0,media=disk,format=raw -smp 1,sockets=1,cores=1,threads=1 -m 512
```

**Q11.** **Report both boot times.** The difference is small — **explain it** using what xv6 does while booting and Part C's exit costs.

```bash
unshare --user --map-root-user id
cat /proc/sys/kernel/apparmor_restrict_unprivileged_userns
ls /proc/self/ns/
systemd-run --user --scope -p MemoryMax=128M sh -c 'cat /sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)/memory.max'
```

**Q12.** **Which of the two container mechanisms works here and which does not?** Report both. **What is a container, in terms of the two mechanisms**, and what does it *not* have that your `kvmhost` guest does? **Which isolates better, and against what?**

---

## 6. Checkoff

Show the TA:

- [ ] Your own guest printing your own message twice (**Q5**).
- [ ] Your two exit costs and the ratio (**Q6**).
- [ ] Your MMIO device with its counter (**Q10**).
- [ ] Your two boot times and your explanation (**Q11**).

**Take with you:** **PS 10** is Parts B–D written up properly, and **Week 11** asks what happens when the machines are separate and the network is not reliable.

---

*CS 202 · Week 10 · Lab 10 · © CSE Department*
