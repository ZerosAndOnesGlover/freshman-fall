# LAB 12 · Demo Day and Code Review

**PROG 201 · Week 12 · Synthesis** · Sat on the **Monday of the completion period**
**Bring:** your Project 2 daemon, built, and a terminal · **Submit:** the completed review of one peer's daemon (`review.md`)

---

## What This Lab Is

The last lab is not a new program — it is **watching Project 2 daemons prove themselves**, yours and a partner's. Half the session is a live demo against the provided harness; half is a structured code review of a peer's daemon, because reading someone else's production code — and finding the missing `close`, the unsafe handler, the parser that trusts `Content-Length` — is the skill this whole course was building toward. There is no reference solution to check against and no quiz. The daemon either survives the harness or it does not, in front of you.

---

## Part A — The Demo (run these against your own daemon)

Build your daemon and the harness:

```
$ cd project2 && make
$ cd ../lab/harness && make          # builds bench and rudeclient
```

Run each check and record the result in your demo log. **Each line must name the command.**

1. **It serves.** `./httpd 8080 8`, then `bench 8080 50 200`. Record throughput, mean and **p99** latency.
2. **It scales (or honestly does not).** `bench` at 1/2/4/8 workers for `/`, and for a `/slow` endpoint. Two tables. Which regime is each in?
3. **It drains.** Start it, open a slow request, `kill -TERM` the pid. Show the in-flight request completed and the **exit code is 0**.
4. **It survives a rude client.** `rudeclient 8080 fin` while a response is in flight (use `/slow` + a second `rudeclient`). Show the server logs the disconnect and **keeps serving** (a follow-up `bench` request succeeds).
5. **It does not leak.** `bench 8080 50 200` ×5 while you watch `VmRSS` and the `/proc/<pid>/fd` count. Both flat.
6. **The negative control.** Rebuild with `signal(SIGPIPE, SIG_IGN)` removed and repeat check 4. Show it now **dies** — report the exit code (141) and decode it. This is the measured pair; a daemon that never shows you the failure has not earned the claim.

## Part B — The Code Review (review a partner's daemon)

Swap daemons with a partner. Read their code — do not run it first — and fill in `review.md` against this checklist. For each item, cite the **file and line**, and mark ✓ / ✗ / N/A with a one-line justification.

**Signals & shutdown**
- [ ] The signal handler calls only async-signal-safe functions (`signal-safety(7)`). Which does it call?
- [ ] `SIGPIPE` is ignored (or `MSG_NOSIGNAL`/`SO_NOSIGPIPE` used on every send).
- [ ] Blocking syscalls (`accept`, `poll`, `read`) handle `EINTR`.
- [ ] Shutdown drains in-flight work rather than `exit()`-ing from the handler.

**Concurrency & resources**
- [ ] A fixed pool, not thread-per-connection.
- [ ] The connection queue is **bounded**; full-queue behaviour is backpressure, not unbounded growth.
- [ ] Every accepted fd is `close`d on **every** path, including errors. Find the error paths.
- [ ] No per-request allocation without a matching free.

**The parser (the attack surface)**
- [ ] Reads are bounded by the buffer size; an over-long request line is rejected, not overflowed.
- [ ] No `gets`/`strcpy`/`sprintf`-shaped code on untrusted input; `Content-Length` is validated.
- [ ] Built with `-Wall -Wextra -Werror`, `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`.

**Operations**
- [ ] Privilege drop (if any) is `setgroups`→`setgid`→`setuid`, in that order.
- [ ] Logs to stderr; does not daemonize itself; a `systemd` unit is provided or described.

**Write two things at the end of `review.md`:**
1. The **single most serious defect** you found, the failing input or sequence that triggers it, and the one-line fix.
2. One thing the daemon does **well** that you will steal for yours.

---

## What to Submit

`review.md` — your Part B review of a partner's daemon, with file:line citations, the checklist, and the two closing paragraphs. (Your own demo log goes in your Project 2 report, not here.)

## Grading

Ungraded, required, and the most useful hour of the term: the defects your partner finds in your daemon are the ones you would otherwise have found in production at 3 a.m. Tracked in [[_PROG 201 Lab and Quiz Record]].

> **The harness is provided, not to be trusted blindly.** `bench` measures loopback throughput, which is an upper bound no real network will match; `rudeclient` models one failure mode of many. A green demo is necessary, not sufficient — the same lesson as every measurement this term.

---

*PROG 201 · Week 12 · Lab 12 · © CSE Department*
