# CS 202 · Problem Set 11 — Solutions
## **INSTRUCTOR ONLY** · Do not distribute

---

**Marking philosophy for PS 11.** The simulator **checks the safety property itself** — two leaders in one term aborts the run — so **Q1 and Q2 are close to binary**, and the marks beyond them are for explanations. **Q4 and Q5 are where a student demonstrates they understand what they built.**

**Reference:** `raftsim reference (do not distribute).c`, complete. Both it and the skeleton compile with no compiler output. Figures below are from the reference; **students' outputs for the given seeds must match exactly**, because the generator is seeded and the schedule is deterministic.

---

## Q1: Standing for Election (30 points)

### (a) [20]

```
5 nodes, 0% loss, seed 1, 1000 ticks
t= 158  node 1 times out and stands for election in term 1
t= 170  node 1 wins term 1 with 3 of 5 votes
after 1000 ticks: 1 elections started, 1 leaders elected, 170 ticks without a leader (17.0%)
```

Reference `step_node`:

```c
    if (node[i].state == LEADER) {
        if (tick >= node[i].next_heartbeat) {
            for (int j = 0; j < n; j++) if (j != i) send(i, j, MSG_HEARTBEAT, node[i].term, 0);
            node[i].next_heartbeat = tick + HEARTBEAT;
        }
        return;
    }
    if (tick >= node[i].election_deadline) {
        node[i].state = CANDIDATE; node[i].term++; node[i].voted_for = i; node[i].votes = 1;
        elections++; reset_election_timer(i);
        for (int j = 0; j < n; j++) if (j != i) send(i, j, MSG_VOTE_REQ, node[i].term, 0);
    }
```

**The two failures that change the output:** not resetting the candidate's own timer (it stands again mid-election, and the term climbs); and counting its own vote as zero (it needs one more reply, and the tick of victory moves).

### (b) [5]

**158 is node 1's initial election timeout**, drawn from [150, 300) by the seeded generator — **the smallest of the five draws**, which is why node 1 is the one that stands. **[3]**

**With every timeout exactly 200 [2]:** all five stand at tick 200 in term 1, each votes for itself, **nobody reaches three votes**, every candidate times out again, and the cluster **splits the vote forever** — terms climbing, no leader. This is the livelock that randomisation exists to prevent (L35 §3).

### (c) [5]

**Vote requests take 2–11 ticks to arrive; replies take another 2–11.** A win needs two replies, so the fastest possible is 4 ticks and the expected is around 13. **Measured: 12** — the two quickest of the four one-way trips. **Accept any answer that adds one request delay and one reply delay and notes the majority is reached on the *second* reply.**

---

## Q2: Votes, and Why There Is Only One Leader (30 points)

### (a) [8], (b) [12], (c) [6]

The three functions as in the reference (L35 §2 quotes the first). **Marks:**

| Requirement | Marks | If wrong |
|---|---:|---|
| a larger term always demotes, whatever the state | 8 | a deposed leader keeps leading after a partition heals — visible in Q5 |
| **one vote per term**, recorded and checked | 8 | **the simulator aborts with TWO LEADERS** |
| grant only for terms ≥ ours | 4 | an old candidate wins with stale votes |
| reset the election timer when granting | 4 | voters stand for election while an election is in progress; terms climb |
| count votes only for the current term | 3 | a late reply from an old term elects a leader who has already stepped down |
| majority test `votes > n / 2` | 3 | with `>=` a two-node "majority" of five elects two leaders — **the check fires** |

### (d) [4]

**The two rules [2]:** a node grants **at most one vote per term**, and a candidate needs **more than half** the nodes. **The argument [2]:** two leaders in one term would need two sets of voters, each larger than *n*/2, drawn from the same *n* nodes; **any two such sets share a node**, and that node would have voted twice in one term, which the first rule forbids.

**Which line [bonus]:** the `voted_for` check in `handle_vote_request`, or the `> n / 2` test.

---

## Q3: Losing the Leader (15 points)

### (a) [8]

```
t= 183  node 4 wins term 1 with 3 of 5 votes
t= 500  node 4 crashes
t= 719  node 1 times out and stands for election in term 2
t= 732  node 1 wins term 2 with 3 of 5 votes
after 2000 ticks: 3 elections started, 2 leaders elected, 415 ticks without a leader (20.8%)
```

**Leaderless from t=500 to t=732: 232 ticks.** *(The other 183 leaderless ticks are the start-up, before any leader existed.)*

### (b) [7]

**219 ticks waiting for a follower's election timer to expire; 13 ticks running the election. [3]** **Waiting dominates, by 17 to 1.**

**Halving the timeout [4]:** the wait halves — the outage drops to roughly 120 ticks — and **the election itself does not change**, because it is bounded by message delay, not by the timeout. **The cost:** with timeouts of 75–150 ticks against heartbeats every 50 and delays up to 11, **a couple of delayed heartbeats now looks like a dead leader**, and the cluster holds elections it does not need — exactly what Q4's high-loss rows show. **Accept any answer that names spurious elections.**

---

## Q4: A Network That Loses Messages (15 points)

### (a) [9]

Five seeds each, `-n 5 -ticks 5000 -quiet`:

| Loss | Elections | Leaders | Leaderless |
|---:|---:|---:|---:|
| 0% | 1.2 | 1.0 | 3.9% |
| 10% | 1.8 | 1.2 | 3.9% |
| 20% | 4.0 | 2.8 | 4.8% |
| 40% | 19.8 | 5.4 | 22.9% |
| 60% | 54.8 | 4.6 | 60.3% |
| 80% | 85.6 | 0.4 | 97.7% |

**[1.5 per row.]**

### (b) [6]

**The knee is between 20% and 40% [2].**

**Why thrashing rather than slowing [4]:** below the knee, a lost heartbeat costs nothing — the next one arrives well inside the election timeout. Past it, **several heartbeats in a row are lost often enough that followers time out**, and each election **adds traffic** (a request and a reply per node) to a network that is already dropping messages.

**Elections rise while leaders fall** because an election needs **both** the requests and the replies to survive: at 80% loss a candidate's chance of collecting two replies is small, so **candidates keep standing and keep failing** — 85.6 elections producing 0.4 leaders. **The cluster is not slow; it is busy doing nothing**, which is Week 4's livelock at a distance.

---

## Q5: A Partition (10 points)

### (a) [5]

```
t= 189  node 0 wins term 1 with 3 of 5 votes
t= 300  the network partitions: mask 0x3
t= 486  node 2 times out and stands for election in term 2
t= 491  node 2 wins term 2 with 3 of 5 votes
t=1200  the partition heals
t=1247  node 0 steps down: it saw term 2 while in term 1
```

**Two leaders from t=491 to t=1247 — 756 ticks** — node 0 in term 1, node 2 in term 2. **The older was deposed by the first message carrying term 2**, 47 ticks after the heal.

### (b) [5]

**Node 0 can accept client requests, append them locally, and send them to node 1 [2] — and can commit nothing**, because committing needs three of five and it can reach two. **The property that makes this safe [2]: a majority is required for both election and commitment, and two majorities intersect** — so no entry can be committed on both sides, and node 0's uncommitted entries are discarded when it rejoins.

**What the client should experience [1]: a timeout, not a false success.** The leader must **not** acknowledge a write until a majority has stored it — which is why a correct implementation of the full algorithm holds the client's request until commitment or gives up. *(A student who says "it should return an error immediately" should be asked how the leader would know: it cannot distinguish a partition from slow followers — L34 §5.)*

---

*CS 202 · Week 11 · PS 11 Solutions · Instructor Only*
