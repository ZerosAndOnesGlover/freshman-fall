# CS 202 · Operating Systems
## Week 11 · Lecture 2 of 3
### Agreement: Raft's Leader Election

*“Either you will be a leader, or a follower, and my goal is for you to be a leader.”* — Richard Hamming, *The Art of Doing Science and Engineering* (1991)

---

**Sat:** Wednesday of Week 11, 09:00–09:50, VNC 101 · **Reading:** Ongaro & Ousterhout, "In Search of an Understandable Consensus Algorithm" §§1–5 · **Next:** L36, partitions and what real systems do

**Coursework:** 📝 **PS 11** released today, due Fri of Week 12 17:00 · 📋 **Project 1** due Fri this week 17:00 · 📝 **PS 10** due Fri this week 17:00 · 🔬 **Lab 11** Tue of Week 12 15:00–16:50

> **Project 1 is due Friday at 17:00.**

---

## 1. The Problem, Stated Precisely

**Several machines must agree on a sequence of operations**, so that each can apply them in the same order and end in the same state — **a replicated log**, which is Week 8's journal with the disk replaced by a network.

**The hard part is not the log; it is agreeing who writes it.** Raft splits the problem in two, and this lecture is the first half:

1. **Elect one leader.** All decisions flow through it, so there is nothing to reconcile.
2. **Replicate the log** from that leader, and commit an entry once a **majority** has stored it.

**Everything rests on one invariant: at most one leader per term.** If that holds, the second half is bookkeeping.

---

## 2. Terms: A Clock Without Time

**Raft divides time into *terms*, numbered 1, 2, 3, …** — L34 §4's logical clock, with one rule:

- **Every message carries its sender's term.**
- **A node that sees a larger term adopts it and becomes a follower**, whatever it was doing.
- **A node that sees a smaller term ignores the message.**

```c
static int step_down_if_behind(int i, int term)
{
    if (term > node[i].term) {
        node[i].term = term;
        node[i].state = FOLLOWER;
        node[i].voted_for = -1;
        return 1;
    }
    return 0;
}
```

**That is the whole mechanism for detecting staleness.** A leader that was isolated for a minute learns it is deposed **the instant it hears any message from the new term** — and, measured in the simulator, it does:

```
t=1200  the partition heals
t=1247  node 0 steps down: it saw term 2 while in term 1
```

---

## 3. The Election

**A node is a follower, a candidate, or the leader.**

- **A follower that hears nothing from a leader for its *election timeout* becomes a candidate**: it increments its term, votes for itself, and asks everyone for a vote.
- **A node grants at most one vote per term**, to the first candidate that asks.
- **A candidate with votes from a majority becomes the leader**, and starts sending heartbeats — which stop everyone else's timers.

**At most one leader per term follows immediately**: two leaders in one term would need two disjoint majorities of the same set, and there are none.

**The timeouts are randomised** — 150 to 300 ms here — and that is not a detail. **With equal timeouts, every follower would stand at the same instant, split the vote, and repeat forever** — L34 §5's FLP result, avoided by randomisation rather than by cleverness.

`raftsim` is this, and nothing else, with a network that delays, drops and partitions. On a quiet network:

```
$ ./raftsim -n 5 -seed 1 -ticks 1000
t= 158  node 1 times out and stands for election in term 1
t= 170  node 1 wins term 1 with 3 of 5 votes
after 1000 ticks: 1 elections started, 1 leaders elected, 170 ticks without a leader (17.0%)
```

**One timeout, one round trip, one leader** — 12 ticks from standing to winning, which is the time for a vote request and its reply to cross the simulated network twice.

---

## 4. What Happens When the Leader Dies

**Nothing, until somebody notices** — and the only way to notice is that the heartbeats stopped:

```
$ ./raftsim -n 5 -seed 4 -ticks 2000 -crash 500:4 -recover 1500:4
t= 183  node 4 wins term 1 with 3 of 5 votes
t= 500  node 4 crashes
t= 719  node 1 times out and stands for election in term 2
t= 732  node 1 wins term 2 with 3 of 5 votes
```

**The cluster was leaderless from t=500 to t=732 — 232 ticks**, of which 219 were *waiting for the timeout to expire* and 13 were the election itself. **The timeout is the cost of failure detection**, and it is the dominant term.

**That is the central trade of the whole design:**

| Shorter election timeout | Longer election timeout |
|---|---|
| failures are noticed sooner | a slow leader is not deposed by accident |
| **more false elections** under load or packet loss | **longer outages** when the leader really dies |

**Raft's recommendation — a timeout ten to twenty times the round trip — is exactly this trade**, and L36 §2 measures what happens when the network makes it impossible to satisfy.

---

## 5. Why a Majority

**Any two majorities of the same set intersect.** That single fact does all the work:

- **Two candidates cannot both win a term**, because some node would have had to vote twice.
- **A leader elected in a later term necessarily contains a node that voted in the earlier one** — which is how Raft's log-matching rules (the second half of the algorithm) guarantee that committed entries survive.
- **A partitioned minority can elect nobody**, so it cannot commit anything and cannot diverge (L36 §1).

**The price is stated plainly: a cluster of 2*f* + 1 nodes survives *f* failures.** Three nodes tolerate one; five tolerate two. **More nodes mean more failures tolerated and more messages per decision** — five nodes need three replies, not two.

---

## 6. What the Simulator Does Not Do

**This is leader election only.** Raft's complete algorithm adds:

- **A log.** Entries are appended by the leader and replicated; an entry is **committed** when a majority has stored it, and only then applied.
- **Log matching in elections.** A candidate whose log is behind must not win, or committed entries could be lost. The vote request carries the candidate's last log index and term, and a voter refuses a candidate less up to date than itself.
- **Membership changes**, which need their own protocol so that two disjoint majorities never coexist during the change.

**The election you are implementing is the part where agreement actually happens**, and the rest is careful bookkeeping on top of it.

---

## 7. What to Take Away

1. **Consensus is a replicated log; Raft reduces it to electing one leader** and letting that leader order everything.
2. **A *term* is a logical clock**: every message carries one, a larger term deposes you, a smaller one is ignored — measured, a healed partition deposed the old leader **47 ticks** after it healed.
3. **One vote per node per term plus a majority gives at most one leader per term**, because two majorities always intersect.
4. **Randomised election timeouts** are what prevent endless split votes — FLP avoided by chance rather than by cleverness.
5. **Failure detection is the timeout, and it dominates the outage**: a crashed leader cost **232 ticks**, of which 219 were waiting.
6. **2*f* + 1 nodes tolerate *f* failures**, at the cost of more messages per decision.

---

## Exercises

1. Two candidates stand in the same term in a five-node cluster and each gets two votes. **What happens next**, and how long does it take? *(What must be true for the third node's vote to be split?)*
2. **Why must a node's vote be remembered across a crash** in real Raft, and what does that cost per election? *(What does it force to disk?)*
3. A cluster of four nodes: **how many failures can it tolerate**, and how does that compare with three? **What does the fourth node buy?**
4. The leader is not crashed but merely slow — its heartbeats arrive every 400 ms instead of 50. **Trace what happens**, and say which of L34's impossibilities this is an instance of.
5. **Show that two leaders in one term is impossible** without appealing to Raft's code: state the two rules used, and the counting argument.

---

*CS 202 · Week 11 · L35 · © CSE Department*
