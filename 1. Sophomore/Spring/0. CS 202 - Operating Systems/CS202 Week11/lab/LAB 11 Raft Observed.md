# CS 202 · Lab 11
## Raft, Observed
### Week 11 · sat **Tuesday of Week 12**, 15:00–16:50, BH 210 · **unmarked, checked off in the session**

---

> **This lab covers Week 11** and is sat on the **Tuesday of Week 12**. Lab *N* is always sat in
> Week *N+1*.
>
> **Nothing here is marked.** The TA checks your work off in the session.
> [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second
> unexcused absence.
>
> **Project 2 is due in the completion period**, and **Lab 12 is demo day.**

**What you are doing:** measuring what distance costs, proving that a successful `write` is not a delivery, watching two clocks disagree — and then breaking a consensus protocol on purpose and watching it recover.

**The curriculum asks you to observe Raft with etcd.** **etcd is not installed on BH 210**, and Part E says what that would have added. The simulator makes up for it in one way: **you can drop 40% of its messages and partition it on command.**

---

## 0. Setup (5 minutes)

```bash
W11="$ACADEMICS/1. Sophomore/Spring/0. CS 202 - Operating Systems/CS202 Week11"
mkdir -p "$CS202/week11/lab11" && cd "$CS202/week11/lab11"
cp "$W11/lab/"*.c . && cp "$W11/assignments/ps11/raftsim.c" .      # your PS 11 version if you have one
for p in netlat delivered clocks raftsim; do gcc -O2 -Wall -Wextra -o $p $p.c; done
```

---

## 1. Part A — What Distance Costs (20 min)

```bash
taskset -c 2 ./netlat
ping -c 5 8.8.8.8 | tail -2
```

**Q1.** Report the five local measurements and the network round trip. **Express each as a multiple of a function call**, and say which step in the ladder is the largest jump.

**Q2.** Loopback never reaches a wire, yet costs about twenty microseconds. **Where does that time go?** *(Name four things, using Weeks 9 and 10.)*

**Q3.** A service does 0.5 ms of work per request and must consult one replica. **Compute its best possible throughput per connection** for a replica on loopback and for one across the internet. **Which term dominates, and what would you change?**

---

## 2. Part B — "Sent" Is Not "Delivered" (15 min)

```bash
./delivered
```

**Q4.** Report the number of bytes. **Where are they**, and what happens to them if the sender crashes now? **Name the two buffers involved.**

**Q5.** The program stops the reader with `SIGSTOP`. **Describe the equivalent failure on a real network** — and say why the sender cannot distinguish it from a reader that is merely slow.

---

## 3. Part C — Whose Clock? (15 min)

```bash
./clocks
timedatectl | head -5
```

**Q6.** Report the four clocks. **`CLOCK_BOOTTIME` and `CLOCK_MONOTONIC` differ. By how much, and why?** *(What has this laptop been doing?)*

**Q7.** For each of: **a 30-second request timeout; a TLS certificate's expiry; measuring how long a function took** — say which clock you would use and what breaks with the wrong one.

---

## 4. Part D — Breaking Consensus (45 min)

```bash
./raftsim -n 5 -seed 1 -ticks 1000
./raftsim -n 5 -seed 4 -ticks 2000 -crash 500:4 -recover 1500:4
./raftsim -n 5 -seed 3 -ticks 2000 -partition 300:3 -heal 1200
```

**Q8.** For the quiet run: **when was the leader elected, and what were the 170 leaderless ticks spent on?**

**Q9.** For the crash run: **how long was the cluster leaderless, and how is that time divided?** Now **halve `ELECTION_LO` and `ELECTION_HI`, rebuild, and run it again** — report the new interval, and say what you would expect to get worse.

**Q10.** For the partition run: **how long were there two leaders?** Say what each could and could not do, and **what deposed the older one.**

**Now the sweep.** For loss 0, 20, 40, 60, 80 (five seeds each, `-ticks 5000 -quiet`), tabulate elections, leaders and leaderless percentage.

**Q11.** **Where is the knee?** Explain why *elections* rise while *leaders elected* falls at high loss.

**Finally, the invariant:**

```bash
for s in $(seq 1 50); do for L in 0 20 50; do ./raftsim -n 5 -loss $L -seed $s -ticks 3000 -quiet > /dev/null || echo "VIOLATION seed $s loss $L"; done; done
```

**Q12.** Report the result. **What exactly is being checked**, and why can no amount of loss or partitioning break it?

---

## 5. Part E — The Tool That Is Not Here (10 min)

```bash
which etcd etcdctl zookeeper-server consul
```

**Q13.** Report the output. **What would `etcdctl endpoint status` have shown you** that the simulator does not, and **what can you do here that you could not do to a production etcd cluster?** Name one of each.

---

## 6. Checkoff

Show the TA:

- [ ] Your latency ladder with the multiples (**Q1**).
- [ ] The byte count from `delivered` and your answer to **Q4**.
- [ ] Your crash-run interval, before and after halving the timeout (**Q9**).
- [ ] Your loss table and the invariant check (**Q11, Q12**).

**Take with you:** **PS 11** is Part D written up properly, and **Week 12** asks what all of this looks like to an attacker.

---

*CS 202 · Week 11 · Lab 11 · © CSE Department*
