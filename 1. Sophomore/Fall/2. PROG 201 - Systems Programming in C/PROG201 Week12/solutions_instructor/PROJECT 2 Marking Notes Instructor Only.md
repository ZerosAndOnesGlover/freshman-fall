# PROG 201 · Project 2 Marking Notes
## A Production HTTP Daemon — Instructor Only

---

**Do not distribute.** The reference daemon is `httpd reference (do not distribute).c` in this folder;
the expected measurements below came from it. Students build their own from their Week 5–6 server.

**Machine these numbers came from:** Intel i5-8250U (8 logical CPUs), Ubuntu 24.04, glibc 2.39,
Linux 7.0.0-30, all traffic over loopback. Throughput and latency drift run to run; the *shapes*
(flat vs linear scaling, exit 0 on drain, exit 141 on unhandled SIGPIPE, delta-0 fds, flat RSS) are
invariant. Load client: `bench` (in `lab/harness/`); disconnect: `rudeclient`.

> **A note that will save you grading grief:** a student whose `bench` reports throughput but whose
> daemon logged a `bind: Address already in use` is measuring **someone else's server** on a shared
> port (this bit the reference build — a `java` process held `*:8080`). Require a **high, free** port
> (checked with `ss -ltn`) in the demo log. This is itself a good teaching moment about trusting a
> measurement without checking what produced it.

---

## Expected measurements (the reference daemon)

**Part 1 — pool + bounded queue.** `httpd PORT N` starts N workers, one accept loop, a 256-slot
bounded queue. Backpressure: with an unbounded queue and a burst, `VmRSS` climbs without limit; with
the bound, accept blocks on `qnotfull` and the kernel backlog absorbs the rest.

**Part 2 — signals.**
| Check | Command | Expected |
|---|---|---|
| graceful drain | `kill -TERM <pid>` mid-request | `[httpd] SIGTERM: draining` → `drained and exiting 0`, **exit 0**, in-flight request completed |
| SIGPIPE handled | `rudeclient PORT fin` mid-response | `[worker] client gone (EPIPE), handled`; server **survives**; follow-up `bench` succeeds |
| SIGPIPE NOT handled | rebuild without `signal(SIGPIPE,SIG_IGN)` | process **killed**, **exit 141** (128+13) |

The two-write reproduction (`sigtest_server`/`sigtest_client` shape): `write1 = 17 (ok)` then either
`SIGPIPE → exit 141` (default) or `write2 = -1 (Broken pipe)` + `SURVIVED` + `exit 0` (ignored).

**Part 3 — robustness.**
| Check | Command | Expected |
|---|---|---|
| throughput, trivial | `bench PORT 50 200` | ~**33–36k req/s**, roughly flat across 1/2/4/8 workers |
| latency | same | mean ~**2.3ms**, p50 ~1.8ms, **p99 ~11ms**, max ~18ms |
| throughput, blocking | `bench PORT 10 4 /slow` | **linear: 5/10/20/40 req/s** at 1/2/4/8 workers |
| fd leak | `/proc/<pid>/fd` before/after 10k | **6 → 6, delta 0** |
| memory leak | `VmRSS` over 5×10k rounds | **1712→1728 kB then flat** |

The two scaling tables are the intellectual core: trivial handler is **accept-bound** (flat, and 16
workers is *slower* than 4 — ~32k); blocking handler is **worker-bound** (linear 5×N). A report that
presents both and explains the difference has understood the week; one that shows only "more workers
= faster" has not measured the trivial case.

**Part 4 — parser.** Guard build (`-Werror -fstack-protector-strong -D_FORTIFY_SOURCE=2`) + an ASan
target + a `libFuzzer` run. Accept "fuzzed N million iterations clean" **or** a located bug with a
reproducer (they may reuse the Week 10 `fuzz_parser.c` shape). No AFL (not installed) — clang
`-fsanitize=fuzzer` is the substitute, as in Week 10.

**Part 5 — operations.**
| Check | Command | Expected |
|---|---|---|
| privileged port | `httpd 80 1` unprivileged | `bind :80: Permission denied` (**EACCES**) |
| privilege drop | read `/proc/self/status` `Groups:` | with `setgroups(0,NULL)`: **empty**; without: **root's groups remain** (e.g. `0 4 27 …`) |
| systemd unit | inspection | `Restart=on-failure`, `User=`, `MemoryMax`, `TasksMax`, `AmbientCapabilities=CAP_NET_BIND_SERVICE` |

The `setgroups` finding is the graded part of Part 5 and the course's **seventh** "present but not
working." Full marks require the student to exhibit the leftover `Groups:` line and name `getuid()`
as the liar. They read/reason this on the lab machines (no root to actually `setuid`); accept that,
exactly as Week 11 accepted the `mount` EPERM.

---

## Grading (100 pts)

| Part | Pts | Full-marks bar |
|---|---|---|
| 1 | 20 | pool + bounded queue; backpressure *shown* (unbounded-queue contrast measured) |
| 2 | 24 | self-pipe handler (safe fns named); drain measured to exit 0; **SIGPIPE pair** both directions, 141 decoded |
| 3 | 20 | fd delta 0; RSS flat table; **both** scaling tables + p99 |
| 4 | 20 | safe parser code; guard+ASan build; fuzzed (bug located or N-million clean) |
| 5 | 16 | EACCES shown; **Groups: finding exhibited**; systemd unit mapped; isolation paragraph |

**The synthesis page** (required close of the report): at least six earlier weeks named, and one of
their own findings identified as "present but not working" with the revealing measurement. A strong
capstone connects the daemon back through the whole course; mark generously for genuine synthesis and
lightly for a checklist.

## Common errors

- **`exit()` inside the signal handler** — works in the demo, truncates in-flight replies on TERM.
  Ask them to hold a slow request and TERM it; the truncation appears. −6 (Part 2).
- **`printf` in the handler** — not async-signal-safe. Often invisible until it deadlocks under load.
  −4 even if it "worked" in the demo; the demo not triggering it is not a defence.
- **Unbounded queue** — passes every functional test, dies under a burst. Require the backpressure
  demonstration; −8 if the queue can grow without limit.
- **Missing `close` on an error path** — fd count climbs. Their own Part-3 measurement should catch
  it; if their report claims delta 0 but the code leaks on the error path, they did not actually run
  the error path. Probe with malformed input.
- **`getuid()` cited as proof of privilege drop** — the whole point of Part 5. It is necessary and
  not sufficient; the `Groups:` line is the proof. −4 if they stop at `getuid`.
- **Trusting `Content-Length`** — a classic. Read the parser; a `read(fd, buf, content_length)` with
  an attacker-supplied length is the Week 10 overflow, reborn.
- **Committed binaries / measuring the wrong server** — see the port note above.

---

*PROG 201 · Week 12 · Project 2 Marking Notes · Instructor Only*
