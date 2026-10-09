# PROG 201 · Systems Programming in C
## Week 5 · Lecture 1 of 3
### Sockets, TCP, and the Calls

*“In general, an implementation must be conservative in its sending behavior, and liberal in its receiving behavior.”* — Jon Postel, RFC 791, *Internet Protocol* (1981)

---

**Reading:** APUE Ch. 16 · TLPI Ch. 56–59 · `man 2 socket`, `man 2 listen`, `man 3 getaddrinfo`, `man 7 tcp` · **Previous:** L15 · **Next:** L17 — five ways to serve

**Coursework:** 📊 **Quiz 5** today · 📝 **PS 5** released Wed this week, due Fri of Week 6 17:00 · 📝 **PS 4** due Fri this week 17:00

---

## 1. A Socket Is a Descriptor With an Address

Week 1 said a descriptor is an index into a table and the thing behind it is an open file description. A socket is that, with two differences: it is created by `socket()` rather than `open()`, and it has **two addresses** — a local one and a peer's.

Everything else you already know applies unchanged. `read` and `write` work on it. `dup` works. It is inherited across `fork`. `close` decrements a reference count. `epoll` works because it is a descriptor. **The whole of Weeks 1–4 is the substrate.**

```c
int s = socket(AF_INET, SOCK_STREAM, 0);
```

Three arguments and only the first two matter in practice:

| Argument | Common values |
| --- | --- |
| domain | `AF_INET` (IPv4), `AF_INET6` (IPv6), `AF_UNIX` (same machine, a path) |
| type | `SOCK_STREAM` (TCP: bytes, reliable, ordered), `SOCK_DGRAM` (UDP: messages, neither) |
| protocol | 0 — "the usual one for that pair" |

**`SOCK_STREAM` gives you exactly what a pipe gave you in Week 2**: a byte stream with no message boundaries. If you send two 100-byte records, the reader may get 200 bytes in one `read`, or 37 then 163. Framing is your problem — the same problem, with the same answers (a length prefix, a delimiter, or fixed-size records), and this time there is no `PIPE_BUF` to hide behind because there is a network in the middle.

Linux also lets you or-in flags: **`SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK`**, which sets both without the `fcntl` race Week 1 L06 §5 warned about.

---

## 2. The Server's Four Calls

```c
int ls = socket(AF_INET, SOCK_STREAM, 0);
int one = 1;
setsockopt(ls, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);   /* section 5 */
bind(ls, (struct sockaddr *) &addr, sizeof addr);
listen(ls, backlog);
for (;;) {
    int c = accept(ls, NULL, NULL);
    serve(c);
    close(c);
}
```

**`bind` claims an address**, and that is all it does. **`listen` turns the socket into a *listening* socket** — a different kind of object that can never be read or written, only `accept`ed from. **`accept` returns a new descriptor** for one connection; the listening socket stays open, and forgetting that is the classic first bug.

The address structures are the ugliest part of the API and there is no way around them:

```c
struct sockaddr_in a = {
    .sin_family      = AF_INET,
    .sin_port        = htons(8080),          /* network byte order! */
    .sin_addr.s_addr = htonl(INADDR_LOOPBACK)
};
```

`htons`/`htonl` convert host to network byte order, which is big-endian. On x86-64 they are real byte swaps; on a big-endian machine they are no-ops. **Forgetting `htons` gives you a server on port 36895 instead of 8080** (0x1F90 byte-swapped), and it is the most common single mistake in this week's work.

`struct sockaddr *` is C's attempt at a tagged union from 1983. You fill in a `struct sockaddr_in` or `sockaddr_in6` and cast; the kernel reads `sa_family` to find out which. `struct sockaddr_storage` is the one big enough for any of them, and it is what `accept` should be given.

---

## 3. Do Not Write Address Structures by Hand

`getaddrinfo` builds them for you, resolves names, resolves service names, and handles IPv4 and IPv6 without your code caring. `names.c`:

```
getaddrinfo(NULL, 8080, AF_UNSPEC | AI_PASSIVE):
   AF_INET   0.0.0.0                                  port 8080
   AF_INET6  ::                                       port 8080
getaddrinfo(localhost, http, AF_UNSPEC):
   AF_INET   127.0.0.1                                port 80
```

Note `"http"` became port 80 — it looked it up in `/etc/services` — and `AI_PASSIVE` with a `NULL` host produced the wildcard addresses a server binds to.

The idiom, for a client:

```c
struct addrinfo hints = { .ai_family = AF_UNSPEC, .ai_socktype = SOCK_STREAM };
struct addrinfo *res;
if (getaddrinfo(host, port, &hints, &res) != 0) { ... }      /* NOT errno */
for (struct addrinfo *p = res; p; p = p->ai_next) {          /* try each   */
    int s = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
    if (s < 0) continue;
    if (connect(s, p->ai_addr, p->ai_addrlen) == 0) break;
    close(s);
}
freeaddrinfo(res);
```

**The loop is not optional.** A name may resolve to an IPv6 address that is unreachable and an IPv4 address that works, and a client that tries only the first entry fails on exactly the networks where it matters. `getaddrinfo` returns its own error codes for `gai_strerror`, **not** `errno` — the same trap as pthreads in Week 3.

---

## 4. `listen`'s Backlog Is a Real Queue

The kernel completes the TCP handshake **itself**, before your program calls `accept`, and puts the finished connection on a queue. `backlog` is how deep that queue is. `backlog.c` binds, listens, and then deliberately never calls `accept`:

```
listen(backlog=4), never calling accept.  somaxconn=4096
  5 connects completed immediately
  15 did not complete within 2 s

listen(backlog=16), never calling accept.
  17 connects completed immediately
  3 did not complete within 2 s
```

**The queue holds `backlog + 1`** (Linux's off-by-one, and it is documented in `man 2 listen`). More importantly, look at what happens past it:

**The excess connections do not get `ECONNREFUSED`. They hang.** The kernel drops the incoming SYN silently and the client's TCP retransmits it — after 1 second, then 2, then 4. So an overloaded server does not report an error; it turns a capacity problem into a latency problem, and the client sees a slow site rather than a broken one. That is why "the site was slow" and "the site was down" have the same underlying cause more often than anyone expects.

Two numbers bound it: your `backlog` argument, and **`/proc/sys/net/core/somaxconn`** (4,096 here), whichever is smaller. `ss -ltn` shows both — `Send-Q` is the configured backlog and `Recv-Q` is how many are queued right now:

```
State   Recv-Q Send-Q Local Address:Port
LISTEN  5      4          127.0.0.1:19301
```

**A `Recv-Q` that is persistently near `Send-Q` on a production listener means your `accept` loop is not keeping up**, and it is the first thing to look at when a server is "slow under load".

---

## 5. `SO_REUSEADDR`, and Why Every Server Has It

Restart a server you just killed and it says `Address already in use` — even though nothing is listening. `reuse.c` shows why:

```
the server closed first, so its side is in TIME_WAIT:
TIME-WAIT 0  0   127.0.0.1:19001   127.0.0.1:49142

rebind without SO_REUSEADDR: Address already in use
rebind with    SO_REUSEADDR: succeeded
```

**Whichever side closes a TCP connection first spends 2×MSL — 60 seconds on Linux — in `TIME_WAIT`.** The socket is gone but the *address pair* is reserved, so that a delayed duplicate packet from the old connection cannot be delivered to a new one that reuses the same four-tuple. It is a correctness mechanism, not a bug.

`SO_REUSEADDR` says "let me bind even though a `TIME_WAIT` connection exists on this port". It does **not** let two live servers listen on the same port — that is `SO_REUSEPORT`, a different option with a different purpose (several processes accepting from the same port, kernel-balanced).

**Set `SO_REUSEADDR` on every listening socket you ever write.** There is no case where you want the alternative.

### `TIME_WAIT` at scale is a different problem

After one benchmark run of 20,000 requests, on this machine:

```
TIME-WAIT sockets before: 1, after 20,000 requests: 11,261
ephemeral ports available: 28,232
```

**Eleven thousand ports held for a minute, out of twenty-eight thousand.** Two more runs and the *client* cannot open a connection — `connect` fails with `EADDRNOTAVAIL`. This is the classic failure of a benchmark, a load balancer, or any client that opens a new connection per request:

- The fix that is not a fix: `net.ipv4.tcp_tw_reuse` (2 here) and shortening `tcp_fin_timeout`. They help and they trade away the guarantee `TIME_WAIT` exists to give.
- **The fix that is a fix: stop opening a connection per request.** HTTP keep-alive exists for this reason, and it is why HTTP/1.0's `Connection: close` — which PS 5 implements — is a teaching protocol rather than a production one.

---

## 6. Reading and Writing a Socket

Everything from Week 1 L05 applies, and two things are sharper.

**Short reads and writes are the normal case, not an edge case.** A `read` returns what has arrived, which on a network is whatever fitted in the packets so far. A `write` returns what fitted in the socket's send buffer. `write_all` from Week 1 is mandatory here, not advisory:

```c
static ssize_t write_all(int fd, const void *buf, size_t n)
{
    size_t sent = 0;
    while (sent < n) {
        ssize_t k = write(fd, (const char *) buf + sent, n - sent);
        if (k < 0) { if (errno == EINTR) continue; return -1; }
        sent += k;
    }
    return sent;
}
```

**`read` returning 0 means the peer closed**, exactly as with a pipe. That is an orderly shutdown, not an error.

**Writing to a socket the peer has closed raises `SIGPIPE`**, whose default action kills your process — so a server that does not handle it dies the first time a client disconnects mid-response. Three options, and the first is what every server does:

```c
signal(SIGPIPE, SIG_IGN);            /* then write() returns -1/EPIPE   */
send(fd, buf, n, MSG_NOSIGNAL);      /* per-call, and more precise      */
setsockopt(fd, SOL_SOCKET, SO_NOSIGPIPE, ...);   /* BSD/macOS only      */
```

**`shutdown` is not `close`.** `close` drops your reference to the descriptor; `shutdown(fd, SHUT_WR)` sends a FIN while leaving the socket open for reading, which is how you say "I have finished sending, tell me what you have" — the half-close that `Connection: close` protocols rely on.

---

## 7. The Client's Two Calls

```c
int s = socket(...);
connect(s, addr, addrlen);
```

No `bind` — the kernel picks a source address and an ephemeral port from `/proc/sys/net/ipv4/ip_local_port_range` (32768–60999 here, so 28,232 of them, which is §5's ceiling).

`connect` on a blocking socket performs the whole three-way handshake before returning, which means **it can block for a long time** — up to `tcp_syn_retries` worth of retransmissions, which is over two minutes by default. A client with a timeout requirement must use a non-blocking socket and wait on it (L18 §3), because there is no `SO_CONNTIMEO`.

Its failures are worth knowing by name:

| `errno` | Means |
| --- | --- |
| `ECONNREFUSED` | The host is up and nothing is listening — an RST came back |
| `ETIMEDOUT` | No answer at all. Usually a firewall dropping packets |
| `EHOSTUNREACH` / `ENETUNREACH` | Routing said no |
| `EADDRNOTAVAIL` | **You are out of ephemeral ports** (§5) |
| `EINPROGRESS` | Non-blocking, and the handshake has started (L18 §3) |

**`ECONNREFUSED` fast and `ETIMEDOUT` slow is a diagnostic**: the first means you reached the machine, the second means you did not.

---

## Summary

- A socket is **a descriptor with two addresses**. Everything from Weeks 1–4 applies to it.
- `SOCK_STREAM` is a **byte stream with no message boundaries** — Week 2's framing problem, without `PIPE_BUF`.
- Server: `socket`, `bind`, `listen`, `accept`. **`accept` returns a new descriptor**; the listener stays.
- **Use `getaddrinfo`**, loop over its results, and remember it returns its own error codes rather than setting `errno`.
- The **listen queue holds `backlog + 1`**, capped by `somaxconn`. Past it the kernel **drops SYNs silently** and clients retry — a capacity problem that presents as latency. `ss -ltn`'s `Recv-Q` is the gauge.
- **`TIME_WAIT` holds the address for 60 s**, so every listener needs `SO_REUSEADDR`. At scale it is a different problem: **11,261 `TIME_WAIT`s after 20,000 requests** against 28,232 ephemeral ports.
- Short reads and writes are normal; `write_all` is mandatory; **ignore `SIGPIPE` or your server dies on the first disconnect**.
- `connect` picks an ephemeral port, can block for minutes, and its `errno` values are a diagnostic.

---

## Exercises

1. Write a server that forgets `htons`. What port does it actually listen on? Derive the number before you check with `ss`.
2. `accept` with a `struct sockaddr_storage` and print the peer with `getnameinfo`. Now connect over IPv4 and IPv6 and print both.
3. Run `backlog.c` with `backlog` set to 0, and to `somaxconn + 1`. Explain both results from `man 2 listen`.
4. Kill a server that has served one connection and restart it immediately, without `SO_REUSEADDR`. Time how long until the bind succeeds. Now make the *client* close first and repeat.
5. Write a client that opens and closes 30,000 connections as fast as it can. Watch `ss -tan state time-wait | wc -l`. What is the failure, and what is the `errno`?
6. Remove the `SIGPIPE` handling from a server, connect with `curl` and kill `curl` mid-response. What happens to the server, and what does `waitpid` report?
7. `shutdown(fd, SHUT_WR)` then keep reading. Write the client and server that make this useful, and say what breaks if you use `close` instead.

---

*PROG 201 · Week 5 · L16 · © CSE Department*
