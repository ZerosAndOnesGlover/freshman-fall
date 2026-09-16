# CS 202 · Problem Set 11
## Raft: Electing a Leader

---

**Released:** Week 11, Wednesday · **Due:** Week 12, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS11_{LastName}_{StudentID}.pdf`, plus your `raftsim.c` in a tarball `PS11_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine and encouraged. The write-up and the code must be
> yours. State at the top: *"I worked on this problem set independently"* or name who you discussed
> which question with.
>
> **`raftsim.c` must compile clean under `gcc -O2 -Wall -Wextra`** and reproduce the outputs below.
>
> **Project 1 was due last Friday. Project 2 is due in the completion period** — Part B is the long
> one, and this is the week to be finishing it.

**You are implementing Raft's leader election** in a simulator that gives you a network which delays, drops and partitions messages, and a seeded generator so that every run is reproducible.

**Files provided** in `assignments/ps11/`:

| File | Yours to write | Provided |
|---|---|---|
| `raftsim.c` | `step_node`, `step_down_if_behind`, `handle_vote_request`, `handle_vote_response`, `handle_heartbeat` | the network (loss, delay, partitions), the event loop, the crash and partition schedule, printing, and the safety check |

**One tick is one millisecond.** Election timeouts are drawn from **[150, 300)** ticks, heartbeats go every **50**, and messages take **2 to 11** ticks to arrive.

> **The simulator checks the one thing that must never happen**: if two nodes ever become leader in
> the same term, it prints `** TWO LEADERS IN TERM n **` and exits with status 2. **If you see that,
> your vote rule is wrong** — do not proceed to the experiments.

---

### Q1: Standing for Election (30 points)

Implement **`step_node`**, called once per tick for every node:

- **A leader** sends `MSG_HEARTBEAT` to every other node every `HEARTBEAT` ticks.
- **A follower or candidate whose `election_deadline` has passed** becomes a candidate: **increment the term, vote for itself, count one vote, reset its timer**, and send `MSG_VOTE_REQ` to every other node. Count the election in `elections`.

**(a) [20]** Reproduce, exactly:

```
$ ./raftsim -n 5 -seed 1 -ticks 1000
5 nodes, 0% loss, seed 1, 1000 ticks
t= 158  node 1 times out and stands for election in term 1
t= 170  node 1 wins term 1 with 3 of 5 votes
after 1000 ticks: 1 elections started, 1 leaders elected, 170 ticks without a leader (17.0%)
```

*(The `wins` line needs Q2; do Q1 and Q2 together and check this output once.)*

**(b) [5]** **Why is the first election at tick 158 and not tick 0?** Where does 158 come from, and what would happen if every node's timeout were exactly 200?

**(c) [5]** **12 ticks passed between standing and winning.** Account for them from the simulator's constants.

---

### Q2: Votes, and Why There Is Only One Leader (30 points)

**(a) [8]** Implement **`step_down_if_behind`**: a term larger than ours means we are stale — adopt it, become a follower, forget our vote, and report that it happened.

**(b) [12]** Implement **`handle_vote_request`**: grant the vote **only if** the request's term is at least ours **and** we have not already voted for someone else in that term. Update your term, reset your election timer when you grant, and reply either way.

**(c) [6]** Implement **`handle_vote_response`**: count granted votes for the term you are standing in; **a majority makes you leader at once**, and a new leader sends its first heartbeat immediately.

**(d) [4]** **Prove, in three sentences, that two leaders in one term is impossible** given your code. Name the two rules you rely on, and the counting argument. **Then say which line of your code would have to be wrong for the simulator's check to fire.**

---

### Q3: Losing the Leader (15 points)

Implement **`handle_heartbeat`**: a heartbeat from a leader of at least our term makes us a follower and resets our election timer; an older one is ignored.

**(a) [8]** Run, and report:

```
$ ./raftsim -n 5 -seed 4 -ticks 2000 -crash 500:4 -recover 1500:4
```

**Say when the cluster had no leader, and for how long.**

**(b) [7]** **Split that interval into "waiting to notice" and "holding the election".** Which dominates, and by how much? **What would halving the election timeout do to each half — and what would it cost?**

---

### Q4: A Network That Loses Messages (15 points)

**(a) [9]** For loss rates **0, 10, 20, 40, 60 and 80 percent**, run five seeds each with `-n 5 -ticks 5000 -quiet` and tabulate the **average** elections started, leaders elected, and percentage of ticks without a leader.

**(b) [6]** **The table has a knee, not a slope. Say where it is**, and explain **why the cluster thrashes** rather than slowing down — in particular, why the number of *leaders elected* falls at 80% while the number of *elections* rises.

---

### Q5: A Partition (10 points)

```bash
./raftsim -n 5 -seed 3 -ticks 2000 -partition 300:3 -heal 1200
```

**(a) [5]** Report the run. **For how long were there two leaders**, in which terms, and what deposed the older one?

**(b) [5]** The isolated leader could still be reached by clients on its side. **Explain precisely what it can and cannot do**, and say **which property of Raft makes the answer safe**. Then: **what should a client on the minority side experience**, and what must the leader do to provide that?

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Standing for election | 30 |
| 2 | Votes, and why there is only one leader | 30 |
| 3 | Losing the leader | 15 |
| 4 | A network that loses messages | 15 |
| 5 | A partition | 10 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **The lowest problem set of the term is dropped** — and this is the last one.

---

*CS 202 · Week 11 · PS 11 · © CSE Department*
