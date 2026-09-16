# CS 202 · Reading Guide · Week 11
## Distributed Systems: OSTEP 48, Raft, and the Two Impossibilities

---

**The curriculum names no reading for Week 11.** **Read the Raft paper's first five sections before Wednesday** — PS 11 implements exactly what they describe, and the paper was written to be read by students.

> **Project 1 is due this Friday**, and **Project 2 in the completion period.** The reading is short
> for that reason.

| Source | Now? | Why |
|---|---|---|
| **OSTEP Ch. 48, "Distributed Systems"** | **Read** | Unreliable communication, RPC, and what a timeout can and cannot tell you. **L34** |
| **Ongaro & Ousterhout (2014), "In Search of an Understandable Consensus Algorithm" §§1–5** | **Read** | Terms, elections, votes, and the safety argument. **L35, PS 11** |
| Ongaro & Ousterhout §§6–8 | *Read after PS 11 works* | Membership changes, log compaction, client interaction |
| Lamport (1978), "Time, Clocks, and the Ordering of Events" | *Read the first three pages* | Why causality replaces clocks. **L34 §4** |
| Gilbert & Lynch (2002), "Brewer's Conjecture…" | *Skim* | What CAP actually says, and what it does not. **L36 §5** |
| Fischer, Lynch & Paterson (1985), FLP | *Read the abstract and the intuition* | Why every practical protocol uses timeouts or randomness. **L34 §5** |
| `man 7 tcp`, `man 2 write`, `man 2 clock_gettime` | **Before Lab 11** | Buffers, what a successful write means, and which clock is which |

**If you have two hours:** OSTEP 48, then Raft §5 with the simulator open beside it.

---

## OSTEP Chapter 48

1. OSTEP builds a reliable layer over UDP with acknowledgements and retries. **Which of Week 11's impossibilities does that *not* solve**, and what does the receiver need in order to tolerate the retries?
2. The chapter's RPC makes a remote call look local. **Name three ways the illusion leaks**, and match each to a row of L34 §1's table.
3. **Why is "the server did not reply" not the same as "the server did not act"?** Give a banking example and the two designs that make it safe.

---

## The Raft paper

4. §5.2: a candidate needs votes from a majority. **Work out how many nodes a cluster of 3, 4, 5 and 6 tolerates losing**, and say why even sizes are a poor choice.
5. §5.2 again: **election timeouts are randomised.** Find the sentence that says why, and connect it to FLP.
6. §5.4.1 restricts who may become leader using the candidate's log. **PS 11 does not implement logs — so what does it not have to check?** What could go wrong in the full algorithm without that rule?
7. Figure 2 is the whole algorithm on one page. **Find every rule PS 11 implements**, and list the ones it leaves out.
8. §8 measures how long elections take with different timeout ranges. **Compare their graph with your own Q3 and Q4 measurements**, in ticks against milliseconds.

---

## Lamport, FLP and CAP

9. Lamport's happened-before is a partial order. **Give two events in a Raft run that it cannot order**, and say why that is acceptable.
10. FLP says no deterministic protocol guarantees consensus with one faulty node in an asynchronous system. **Raft is deterministic apart from its timeouts. Which assumption does it break to survive?**
11. CAP is often stated as "pick two". **State it precisely instead**, and say which letter Raft gives up during a partition — and which a shopping-cart service gives up instead.

---

## Where to Go Deeper

| Source | Topic | When |
|---|---|---|
| Howard & Mortier (2020), "Paxos vs Raft" | The two algorithms are closer than the papers suggest | After PS 11 |
| Kleppmann, *Designing Data-Intensive Applications*, Ch. 8–9 | Faults, clocks, and consistency models, at length | Any time |
| Jepsen reports (`jepsen.io`) | What real databases do when partitioned — measured, adversarially | **Highly recommended** |
| etcd documentation, "Tuning" | Election timeouts and heartbeats in production | For L36 §3 |

---

*CS 202 · Week 11 · Reading Guide · © CSE Department*
