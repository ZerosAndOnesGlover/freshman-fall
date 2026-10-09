# PROG 201 · Systems Programming in C
## Week 5 · Lecture 3 of 3
### `epoll`, Non-Blocking Sockets, and the Options That Matter

*“One can only display complex information in the mind. Like seeing, movement or flow or alteration of view is more important than the static picture, no matter how lovely.”* — Alan Perlis, "Epigrams on Programming" (1982), #25

---

**Reading:** TLPI Ch. 63 · APUE §14.4–14.5 · `man 7 epoll`, `man 7 tcp`, `man 7 socket`, `man 2 sendfile` · **Previous:** L17 · **Next:** Lab 5 — build a load generator and stress your server, **Friday of Week 6**

**Coursework:** 📝 **PS 4** due Fri this week 17:00 · 📊 **Quiz 6** Tue of Week 6 · 📝 **PS 6** released Wed of Week 6, due Fri of Week 7 17:00

---

## 1. Three Ways to Ask "Which of These Is Ready?"

`select` (1983), `poll` (1986) and `epoll` (2002) answer the same question. `readiness.c` creates *N* socket pairs, makes exactly one of them readable, and times one call:

| descriptors | `select` | `poll` | `epoll` |
| --- | --- | --- | --- |
| 10 | 1.3 µs | 1.1 µs | **0.72 µs** |
| 100 | 6.8 µs | 6.3 µs | **0.69 µs** |
| 1,000 | *cannot* | 71.3 µs | **0.69 µs** |
| 4,000 | *cannot* | 613.0 µs | **0.85 µs** |
| 8,000 | *cannot* | 2,020.6 µs | **0.98 µs** |
| 16,000 | *cannot* | 4,827.4 µs | **0.89 µs** |

**`poll` is linear and `epoll` is flat.** At 16,000 descriptors one `poll` call costs 4.8 **milliseconds** — the server spends more time asking what is ready than doing anything about it. `epoll` costs 0.89 µs at 16,000 and 0.72 µs at 10, which is to say it does not care.

The reason is the interface, not the implementation. `select` and `poll` are **stateless**: you hand the kernel the entire set of descriptors on every call, it walks all of them, and it returns. That is *O(n)* per call and there is no way to make it otherwise. `epoll` is **stateful**: you register descriptors once with `epoll_ctl`, the kernel attaches a callback to each, and `epoll_wait` returns a ready list that was built as events arrived. *O(ready)*, not *O(watched)*.

**This is the C10K answer.** L17 §7's 20,000 connections are possible because watching them costs the same as watching ten.

---

## 2. `select` Cannot Be Used, and It Fails Badly

The `cannot` in that table is not slowness. `fd_set` is a **fixed-size bitmap**, `FD_SETSIZE` is **1024**, and `FD_SET(fd, &s)` with `fd >= 1024` writes past the end of the structure.

It is not diagnosed by the compiler. On glibc with fortification it aborts at runtime:

```
*** bit out of range 0 - FD_SETSIZE on fd_set ***: terminated
```

and without fortification it is silent memory corruption. **Note that `RLIMIT_NOFILE` on this machine is 1,048,576**, so a program can hold a thousand times more descriptors than `select` can represent, and the descriptor numbers that break it arrive with no warning — the 1,025th connection, on a Tuesday.

There is no fix. Recompiling with a bigger `FD_SETSIZE` is undefined behaviour (glibc's headers and your program would disagree about the structure). **`select` is for portability to systems that have nothing else, and for waiting on a handful of descriptors with a timeout.** `poll` has no such limit and is fine up to a few hundred. Past that, `epoll` — or `kqueue` on BSD and macOS, which is the same idea with a better API.

---

## 3. `epoll`, Properly

```c
int ep = epoll_create1(EPOLL_CLOEXEC);

struct epoll_event ev = { .events = EPOLLIN, .data.fd = fd };
epoll_ctl(ep, EPOLL_CTL_ADD, fd, &ev);          /* once per descriptor */

struct epoll_event out[256];
int n = epoll_wait(ep, out, 256, -1);           /* per iteration       */
for (int i = 0; i < n; i++) handle(out[i].data.fd);
```

`data` is a union — an `int fd` or a `void *ptr`. **Use the pointer** and point it at your per-connection struct; you will need the state anyway, and looking it up by descriptor is a hash table you did not have to write.

### Level-triggered against edge-triggered

**Level-triggered** (the default) means *"tell me whenever this descriptor is readable"*. If data arrives and you read half of it, the next `epoll_wait` reports it again.

**Edge-triggered** (`EPOLLET`) means *"tell me when this descriptor becomes readable"*. You are told once per arrival, and if you do not drain the socket you will not be told again — the remaining data sits there and the connection hangs forever.

So `EPOLLET` imposes a rule with no exceptions: **read in a loop until `EAGAIN`**, and the same for writing.

```c
for (;;) {
    ssize_t n = read(fd, buf, sizeof buf);
    if (n < 0 && errno == EAGAIN) break;         /* drained */
    if (n <= 0) { close_conn(fd); break; }
    consume(buf, n);
}
```

Edge-triggered is fewer system calls and a much narrower margin for error. **Start level-triggered.** The one place edge-triggering earns its keep early is the listening socket, where level-triggered mode wakes every thread in a multi-threaded accept loop — the thundering herd — and `EPOLLEXCLUSIVE` is the modern fix for that specific case.

### The rule that catches everyone

**A descriptor is removed from an epoll set automatically when it is closed** — but only when the *last* descriptor referring to the open file description is closed. `dup` it, close one copy, and it stays in the set pointing at something you think is gone. Call `epoll_ctl(ep, EPOLL_CTL_DEL, fd, NULL)` before `close` and stop thinking about it.

---

## 4. Non-Blocking Sockets

```c
int f = fcntl(fd, F_GETFL, 0);
fcntl(fd, F_SETFL, f | O_NONBLOCK);           /* the three-step from Week 1 L06 */
```

or, without the race, `socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK, 0)` and `accept4(ls, NULL, NULL, SOCK_NONBLOCK)`.

Then every call can return **`EAGAIN`** (`EWOULDBLOCK` is the same value on Linux), which is not an error — it means "not now". Three cases:

**`accept` returning `EAGAIN`** means the listen queue is empty. In an accept loop that is the exit condition, not a failure.

**`read` returning `EAGAIN`** means no data has arrived. Go back to `epoll_wait`.

**`write` returning `EAGAIN`** means the send buffer is full, and this is the one people get wrong. You must **keep the unsent remainder, register `EPOLLOUT`, and finish the write when the socket is writable again** — which means every connection needs an output buffer and a "how much have I sent" counter. A server that assumes `write` completes works perfectly until a client stops reading, at which point it silently truncates responses.

**How much can you write before that happens?** Measured against a peer that never reads, on loopback:

```
server SO_SNDBUF 2626560, client SO_RCVBUF 131072
wrote 2625024 bytes (2.50 MiB) before EAGAIN, with the peer never reading
```

**Two and a half megabytes, and then nothing, forever.** A *blocking* server in the same position does not get `EAGAIN` — it blocks in `write`, with no timeout, until the client reads or disconnects. That is one thread or process held hostage per slow client, and it is the mechanism behind the Slowloris denial of service. `SO_SNDTIMEO` is the option almost nobody sets.

**`connect` returning `EINPROGRESS`** is the non-blocking handshake. Wait for the socket to become *writable*, then ask what happened:

```c
int err; socklen_t len = sizeof err;
getsockopt(s, SOL_SOCKET, SO_ERROR, &err, &len);
if (err) { /* the connect failed, and this is its errno */ }
```

**`SO_ERROR` is the only way to find out**, because the `connect` call itself already returned. That is how a client gets a connection timeout, since there is no `SO_CONNTIMEO`.

---

## 5. Nagle, Delayed ACK, and 40 Milliseconds

`nagle.c` writes a one-byte header, then a four-byte body, then waits for the reply. Twenty round trips, **over loopback, where there is no network at all**:

```
  Nagle on (default)        :   38.963 ms per round trip
  TCP_NODELAY               :    0.209 ms per round trip
  ratio                     :    186.6x
```

**Thirty-nine milliseconds to move five bytes to a program on the same machine.** Two reasonable algorithms, interacting:

- **Nagle's algorithm** (1984): do not send a small segment while an earlier small segment is unacknowledged. It exists because telnet sent one packet per keystroke — 41 bytes of headers per byte of payload.
- **Delayed ACK**: do not acknowledge immediately; wait up to 40 ms in case there is data to piggyback on.

The first write goes out. The second is small and the first is unacknowledged, so Nagle holds it. The receiver has nothing to reply with — it is waiting for the rest of the request — so delayed ACK holds the acknowledgement. **Each is waiting for the other, and the delayed-ACK timer breaks the tie 40 ms later.**

Two fixes, and the second is better:

1. **`setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one)`** — disable Nagle. Correct for any request/response protocol, and what every RPC library and HTTP server does.
2. **Do not write a message in two pieces.** Build the header and body in one buffer, or use `writev` (Week 1 L06 §6). Then there is no second small segment and Nagle never engages. This fixes the cause; `TCP_NODELAY` treats the symptom, and treating the symptom is fine.

**A latency that is a suspiciously round 40 ms, or 200 ms, is a protocol interaction and not your code being slow.** It is the single most useful diagnostic in this lecture.

---

## 6. The Options Worth Knowing

| Option | Level | What it does |
| --- | --- | --- |
| **`SO_REUSEADDR`** | `SOL_SOCKET` | Bind despite a `TIME_WAIT` on the address. **Always.** (L16 §5) |
| **`TCP_NODELAY`** | `IPPROTO_TCP` | Disable Nagle. **Any request/response protocol.** (§5) |
| `SO_REUSEPORT` | `SOL_SOCKET` | Several sockets on one port, kernel-balanced. One accept loop per core |
| `SO_KEEPALIVE` | `SOL_SOCKET` | Probe idle connections. **Default is 2 hours** — tune `TCP_KEEPIDLE` or it is useless |
| `SO_RCVBUF` / `SO_SNDBUF` | `SOL_SOCKET` | Buffer sizes. Linux auto-tunes; **setting them disables the auto-tuning** |
| `SO_LINGER` | `SOL_SOCKET` | Make `close` block until data is sent, or reset the connection. Rarely what you want |
| `SO_ERROR` | `SOL_SOCKET` | Retrieve and clear a pending error. Required after a non-blocking `connect` (§4) |
| `TCP_CORK` | `IPPROTO_TCP` | The opposite of `NODELAY`: hold everything until uncorked. For `sendfile` headers |
| `IPV6_V6ONLY` | `IPPROTO_IPV6` | Whether an IPv6 socket also serves IPv4 (§7) |

**Two defaults that bite:** `SO_KEEPALIVE`'s two-hour idle timer is longer than any load balancer's, so a "keepalive" that never fires is the normal case unless you set `TCP_KEEPIDLE`. And **setting `SO_RCVBUF` at all** turns off Linux's window auto-tuning, so the usual outcome of "tuning" the buffer is a slower connection.

---

## 7. IPv6, and One Socket for Both

`names.c` binds an `AF_INET6` socket with `IPV6_V6ONLY` off:

```
getaddrinfo(NULL, 8080, AF_UNSPEC | AI_PASSIVE):
   AF_INET   0.0.0.0     port 8080
   AF_INET6  ::          port 8080

an AF_INET6 socket with IPV6_V6ONLY=0 bound to [::]:19400
LISTEN 0  8   *:19400   *:*
IPV6_V6ONLY reads back as 0
```

A dual-stack listener accepts IPv4 connections too, and they arrive as IPv6-mapped addresses (`::ffff:127.0.0.1`). One socket, both families — and the default of `IPV6_V6ONLY` is a **per-system** setting (`/proc/sys/net/ipv6/bindv6only`, 0 here), so a program that does not set it explicitly behaves differently on different machines.

**Set it explicitly, in whichever direction you want.** And write the rest of the code family-agnostically: `getaddrinfo` for addresses, `struct sockaddr_storage` for `accept`, `getnameinfo` for printing, and never a hard-coded `sizeof(struct sockaddr_in)`.

---

## 8. What Comes After

The costs this week has measured are copies and system calls. Two directions out.

**Fewer copies.** `zerocopy.c` sends a 128 MiB file down a loopback socket three ways:

| how | MiB/s |
| --- | --- |
| `read` into a buffer, then `write` | 2,504 |
| `mmap` the file, then `write` | 3,367 |
| **`sendfile(sock, file, ...)`** | **4,206** |

Each step removes a copy. `read`+`write` copies page cache → user buffer → socket buffer; `mmap`+`write` removes the first; **`sendfile` never enters userspace at all** — the kernel splices the page cache to the socket. `splice` generalises it to any pair of descriptors where one is a pipe. This is Week 4 L13 §5's "`read` copies" argument, with a network on the end.

**Fewer system calls.** `epoll` is *O(1)* per event but still two or three syscalls per request. **`io_uring`** (2019) replaces them with two shared ring buffers — you write submission entries into memory the kernel is watching and read completions out of memory you are watching, and a busy server can go for millions of operations with almost no syscalls at all. It is Week 2's shared-memory ring, applied to the kernel interface itself, and it is what "C10M" is built on.

**And the direction nobody takes seriously enough:** the fastest request is the one you do not serve. Caching, keep-alive, and not opening a connection per request (L16 §5) beat every option in this lecture.

---

## Summary

- **`poll` is *O(watched)* and `epoll` is *O(ready)*.** At 16,000 descriptors: 4,827 µs against **0.89 µs**.
- **`select` cannot be used above `FD_SETSIZE` = 1024**, and fails by aborting or by corrupting memory — on a machine whose `RLIMIT_NOFILE` is 1,048,576.
- `epoll_ctl` once, `epoll_wait` per iteration; put a **pointer** in `data`; `EPOLL_CTL_DEL` before `close`.
- **Edge-triggered means read until `EAGAIN`**, every time, or the connection hangs. Start level-triggered.
- Non-blocking means **`EAGAIN` is normal**. A `write` that returns `EAGAIN` needs an output buffer and `EPOLLOUT`; a `connect` that returns `EINPROGRESS` needs `SO_ERROR`.
- A peer that stops reading absorbs **2.50 MiB** and then blocks you **forever** — one thread per slow client, which is Slowloris.
- **Nagle plus delayed ACK cost 38.963 ms per round trip over loopback**, against 0.209 ms with `TCP_NODELAY` — **186×**. A suspiciously round 40 ms is a protocol interaction.
- Always `SO_REUSEADDR`. Usually `TCP_NODELAY`. **Setting `SO_RCVBUF` disables auto-tuning**, and `SO_KEEPALIVE`'s default idle timer is two hours.
- Set `IPV6_V6ONLY` explicitly; its default is per-system.
- Copies: `read`+`write` 2,504 MiB/s, `mmap`+`write` 3,367, **`sendfile` 4,206**. Syscalls: `io_uring` is the next step.

---

## Exercises

1. Take `readiness.c` to 100,000 descriptors (raise `RLIMIT_NOFILE` if you must). Does `epoll` stay flat? Where does `poll` become unusable in a 10 ms budget?
2. Write an edge-triggered echo server that reads exactly once per event. Send it 100 KiB in one `write` and explain the hang.
3. Make a client stop reading mid-response and watch a server that ignores `write`'s return value. How much of the response was lost, and where did it go?
4. Reproduce §5 and then fix it with `writev` instead of `TCP_NODELAY`. Confirm with `strace` that there is one `writev` and with the timing that Nagle never engaged.
5. Set `SO_RCVBUF` to 4 KiB and to 4 MiB on a loopback transfer and measure both. Then remove the call entirely and measure again. Which is fastest, and what does that say about tuning?
6. Bind a dual-stack listener and connect to it over IPv4. Print the peer address with `getnameinfo`. What does it look like, and what would a naive `sin_addr` comparison do with it?
7. Serve a 1 GiB file with `sendfile` and with `read`+`write`, and compare the process's `ru_maxrss` as well as the time. Which of the two numbers is the better argument for `sendfile`?

---

*PROG 201 · Week 5 · L18 · © CSE Department*
