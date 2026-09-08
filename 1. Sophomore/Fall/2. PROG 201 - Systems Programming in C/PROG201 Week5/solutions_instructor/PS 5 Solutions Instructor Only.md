# PROG 201 · PS 5 Solutions
## A Concurrent HTTP/1.0 Server — Instructor Only

---

**Do not distribute.** Q1(c) and Q4(b) depend on students discovering the results themselves.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04), Intel i5-8250U, 4 physical cores / 8 hardware threads. All loopback.

**On the deadline:** this is due at 17:00 on the Friday of Week 6 and Lab 5 is sat 16:00–17:50 the same day. **Expect submissions at 16:55 and be generous about the last five minutes**; the collision is the calendar's, not the students'.

---

## Reference Fragments

A complete reference is not distributed — the assignment is the implementation. These four fragments are the ones marking turns on.

**The path check — Q1(c):**

```c
static char DOCROOT[PATH_MAX];        /* realpath()'d once at startup */

static int safe_path(const char *target, char *out)
{
    char joined[PATH_MAX];
    if (snprintf(joined, sizeof joined, "%s%s", DOCROOT, target) >= (int) sizeof joined)
        return -1;
    char resolved[PATH_MAX];
    if (!realpath(joined, resolved)) return -1;          /* ENOENT lands here too */
    size_t rl = strlen(DOCROOT);
    if (strncmp(resolved, DOCROOT, rl) != 0) return -1;  /* escaped the root   */
    if (resolved[rl] && resolved[rl] != '/') return -1;  /* /rootevil, not /root/ */
    strcpy(out, resolved);
    return 0;
}
```

**The request read — Q1(a):** read until `"\r\n\r\n"` appears in the accumulated buffer, with a cap, not until one `read` returns.

**`open` then `fstat`, never `stat` then `open` — Q3(a):**

```c
int fd = open(path, O_RDONLY);
if (fd < 0) { status(c, errno == EACCES ? 403 : 404, ...); return; }
if (fstat(fd, &st) < 0 || !S_ISREG(st.st_mode)) { status(c, 403, ...); return; }
```

**`pthread_create` failing is a response, not a silence — Q2(a):**

```c
int rc = pthread_create(&t, NULL, thread_body, (void *)(long) c);
if (rc == 0) pthread_detach(t);
else { status(c, 503, "Service Unavailable", "no worker\n"); close(c); }
```

---

## Q1 — The Server (30)

**(a) [12]** Marks: reading until the blank line rather than once **[4]**, `GET` and `HEAD` **[2]**, 405 for others **[2]**, 400 for a malformed line **[2]**, a stated and enforced cap **[2]**.

The four-mark item is the one to check by testing, not by reading: `printf 'GET / HTTP' ; sleep 1 ; printf '/1.0\r\n\r\n' | nc 127.0.0.1 <port>` splits the request across two packets. A server that reads once returns 400.

The cap: any figure with a reason. 8 KiB matches nginx's default and is a good answer; the mark is for having decided rather than for the number.

**(b) [12]** Marks: 200 with correct `Content-Length` **[3]**, five content types **[2]**, 404 **[2]**, 403 distinct from 404 **[2]**, `HEAD` with headers and no body **[2]**, `/` handled **[1]**.

`Content-Length` must be the file's size, from `fstat` on the **open descriptor**. A student who uses `stat` on the path has Q3(a)'s bug and should lose the mark there, not here.

**(c) [6]** The `realpath` check **[4]**, the three demonstrations **[1]**, the explanation of why textual rejection fails **[1]**.

Reference behaviour, verified:

```
normal file            200
/../../etc/passwd      404
/%2e%2e/%2e%2e/...     404
symlink to /etc/passwd 404
```

**Why textual `..` rejection is not enough**, and the answer has two halves:

1. **A symlink inside the docroot pointing outside it** contains no `..` at all. Only resolving the path catches it — and this is the half most students miss.
2. **Percent-encoding.** `%2e%2e` is `..` after decoding. **But note the ordering:** the reference does not decode at all, so `%2e%2e` is simply a filename that does not exist. A server that *does* decode must **decode first, then resolve, then check** — checking before decoding is the classic CVE, and a student who decodes and still checks correctly deserves the extra credit for having a harder implementation right.

The `resolved[rl] != '/'` line catches `/srv/wwwevil` matching a `/srv/www` prefix. A submission without it is [3 of 4]; point at it rather than deducting more, since it is a genuinely easy thing to miss.

---

## Q2 — Concurrency (20)

**(a) [12]** Six marks per model.

`fork`: child closes the listener **[2]**, parent closes the connection **[2]**, `SIGCHLD` handled **[2]**. The "which did you get wrong first" answer is almost always the parent's `close` — the symptom is that `curl` hangs, because the client never sees EOF (Week 1 L06 §4).

`thread`: detach or join **[2]**, `pthread_create` checked **[3]**, the "why is this better" answer **[1]**. The answer wanted: **an unchecked failure silently closes the connection and the client sees an empty response** (Lab 5 Q6); a 503 tells the client to back off.

`pool`: bounded queue **[3]**, capacity stated **[1]**, full-queue behaviour stated **[2]**. Blocking the accept loop when the queue is full is acceptable and should be recognised as **backpressure**; dropping with a 503 is also acceptable. Growing the queue without limit is not, and is worth saying so — it converts a latency problem into an out-of-memory one.

`epoll`: non-blocking everywhere **[2]**, per-connection state **[2]**, an output buffer and `EPOLLOUT` on `EAGAIN` **[2]**. Very few will get the third right on a first attempt; check by serving a large file to a client that stops reading (Q3(a)).

**(b) [8]** Two marks per row.

| | fork / thread | pool | epoll |
| --- | --- | --- | --- |
| client sends nothing forever | one process/thread stuck in `read` forever; **thousands of them is the attack** (Slowloris) | one worker gone; *N* such clients kill the server | one idle registration, costs nothing |
| client stops reading | `write` blocks once the socket buffer fills — **about 2.5 MiB on loopback, then indefinitely** | same, and the worker is gone | `EAGAIN`, buffer the rest, move on — **if you implemented it** |
| handler segfaults | fork: one connection dies. thread: **the whole server dies** | the whole server | the whole server |
| 10,000 at once | fork: process ceiling. thread: **`EAGAIN` at ~7,637** | queued, at whatever latency | fine |

The second row is the eight marks' worth. **"For how long" is: forever** — there is no default send timeout. `SO_SNDTIMEO` is the fix nobody sets. A student who says "until the client reads or disconnects" has it.

**The third row separates `fork` from everything else**, and is the reason Chrome and nginx use processes at the isolation boundary.

---

## Q3 — Make It Survive (18)

**(a) [6]** Two each.

`SIGPIPE`: `signal(SIGPIPE, SIG_IGN)` and check `EPIPE`, or `send(..., MSG_NOSIGNAL)`. Both fine; the mark is for demonstrating the server survives, with output.

Short `write`: forcing it with a small `SO_SNDBUF` is the intended method and works. Accept any forcing method that actually produces a short write; **do not accept "my `write_all` loops so it must be fine"** without a demonstration.

`stat`-then-`open`: the class is a **TOCTTOU race** — time of check to time of use. Naming it is the mark. Week 1 L05 §5's "two system calls are not one" is the same idea, and a student who makes that connection should be told they have.

**(b) [6]** Reporting both numbers **[2]**, what the columns mean for a listener **[3]**, the diagnosis **[1]**.

For a **listening** socket, `ss` reports `Recv-Q` = **the number of connections currently in the accept queue** and `Send-Q` = **the configured backlog**. They are not bytes. Almost every student will say bytes; the man page and the experiment both say otherwise.

A persistently high `Recv-Q` means the accept loop is not keeping up — the process is spending its time serving rather than accepting, or it has blocked.

**(c) [6]** Numbers **[2]**, the SYN explanation **[4]**.

Reference, from `backlog.c`: with `listen(4)`, **5 connections completed immediately** and the rest timed out; with `listen(16)`, **17**. The queue holds `backlog + 1`.

The explanation: **the kernel silently drops the SYN.** No RST is sent, so the client does not get `ECONNREFUSED`; its TCP retransmits after 1 s, 2 s, 4 s, and either eventually gets in or times out. **A full listen queue presents as latency, not as an error** — full marks require that sentence or its equivalent.

---

## Q4 — Measure It (18)

**(a) [8]** Ten data points, both models. Marks are for completeness and for reporting percentiles rather than only the mean; **p99 is where the models differ and the mean is where they look alike.**

Any shape is acceptable if it is theirs. Ours for reference (`server.c`, trivial work, conc 50): iterative 46,810, fork 15,038, thread 39,186, pool 50,687, epoll 42,985 req/s.

**(b) [6]** The collapse **[3]**, the explanation **[3]**.

Reference: `epoll` drops from 42,985 to **434 req/s** — which is 1/0.002 — and the iterative server gives the same number. The explanation: **the `usleep` runs on the event loop's single thread**, so nothing else is served while it runs; `epoll` gives concurrency over waiting on registered descriptors, not over blocking calls in the handler.

Students without an `epoll` model must predict it. Award full marks for a correct prediction with the right reason; this is the most important idea in the week and it does not require having implemented it.

**(c) [4]** Reference, each run in **a separate process**:

| how | MiB/s | `ru_maxrss` |
| --- | --- | --- |
| `read` + `write` | 2,444 | 1,768 kB |
| `mmap` + `write` | 3,043 | **132,716 kB** |
| **`sendfile`** | **4,456** | **1,640 kB** |

**The memory column is the better argument.** Throughput is 1.8×, which a faster disk or a busier machine could swallow; the resident-memory difference is **eighty times**, and for a server holding a thousand connections open it is the difference between working and not. `sendfile` never brings the file into the process at all.

And the trap: run all three in one process and `ru_maxrss` reports **132,908 kB for all three**, because it is a high-water mark. **A student who reports that, notices it is impossible, and re-runs separately has done the better piece of work** — say so.

---

## Q5 — The Protocol and the Options (14)

**(a) [4]** The two costs: **a TCP handshake per request** on the client (one round trip before any data), and **a `TIME_WAIT` per request** on whichever side closes — 11,261 of them after 20,000 requests in Lab 5, out of 28,232 ephemeral ports. The header: **`Connection: keep-alive`**, made the default in HTTP/1.1.

**(b) [4]** Report whatever they measure, and **"no measurable difference" is the expected answer**, for a reason worth full marks: an HTTP response is normally **one `write`** of headers plus body, so there is never a second small segment for Nagle to hold. L18 §5's 39 ms needs *two* small writes and a wait — which is what a server that writes headers and body separately does, and that is the case where `TCP_NODELAY` earns its keep.

A student who splits their writes, measures the 40 ms, and then fixes it with `writev` instead has done the best possible version of this question.

**(c) [3]** Linux **auto-tunes the receive window** between `tcp_rmem`'s minimum and maximum based on the connection's bandwidth-delay product. **Calling `setsockopt(SO_RCVBUF)` at all disables that**, pinning the buffer — so the usual result of "tuning" it is a connection that is slower on a fast link and no better on a slow one.

**(d) [3]** `AF_INET6` in the `socket` call; `struct sockaddr_in6` (or better, `getaddrinfo` with `AF_UNSPEC` and `AI_PASSIVE`); and **`setsockopt(IPPROTO_IPV6, IPV6_V6ONLY, &zero, ...)`** — which is the option whose default varies, because it follows `/proc/sys/net/ipv6/bindv6only` (0 on these machines). Full marks require naming `IPV6_V6ONLY` and saying the default is per-system.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | The server | 30 |
| 2 | Concurrency | 20 |
| 3 | Make it survive | 18 |
| 4 | Measure it | 18 |
| 5 | The protocol and the options | 14 |
| | **Total** | **100** |

---

*PROG 201 · Week 5 · PS 5 Solutions · Instructor Only · © CSE Department*
