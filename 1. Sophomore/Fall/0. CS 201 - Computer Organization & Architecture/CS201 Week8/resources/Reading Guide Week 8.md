# CS 201 · Week 8 · Reading Guide
## CS:APP Chapter 11 — Network Programming

---

**Set reading:** Bryant & O'Hallaron, **§11.1–11.6**.
**Also:** `man 7 tcp` — the Linux TCP manual page, which is the specification for everything in Lab 8.
**Optional:** Kurose & Ross, *Computer Networking: A Top-Down Approach*, chapters 1 and 3.

---

## What This Chapter Is and Is Not

**CS:APP Chapter 11 is a sockets-programming chapter, not a networking chapter.** It teaches the API well and the protocols barely — there is no congestion control, no routing, and the TCP treatment is a page.

**That is the right emphasis for this course.** CS 302 in Year 3 is a full networking course; what CS 201 needs is the boundary between your program and the network stack, which is exactly what the socket API is.

**So: read Chapter 11 for the API, and take the protocol material from the lectures**, where it is attached to measurements.

---

## Section by Section

| § | Topic | What to take from it |
|---|---|---|
| **11.1** | The client-server model | Two pages. The transaction model |
| **11.2** | Networks | A brisk tour of the hierarchy. Fine as background |
| **11.3** | **The global IP internet** | IP addresses, DNS, connections. **§11.3.2 on address structures is the part you will actually use** |
| **11.4** | **The sockets interface** | The core. `socket`, `bind`, `listen`, `accept`, `connect` |
| **11.4.5** | **`getaddrinfo`** | **Read this properly.** The modern, protocol-independent way to resolve names — the older `gethostbyname` is deprecated and not IPv6-capable |
| **11.4.8–11.4.9** | Helper functions, echo client/server | **This is PS 8.** The book's `open_clientfd`/`open_listenfd` are worth reading before writing your own |
| **11.5** | Web servers | HTTP basics and CGI. The HTTP part is useful; CGI is a historical curiosity |
| **11.6** | Putting it together: TINY | A complete small web server in ~250 lines. **Worth reading end to end** |

---

## Questions to Read Against

**On §11.3–11.4**

1. Why does `getaddrinfo` return a *linked list* of results rather than one address? What should a correct client do with the list?
2. `accept` returns a new descriptor. **What would break if it reused the listening one?**
3. The book's `open_listenfd` sets `SO_REUSEADDR`. **What problem does that solve?** *(Connect it to `TIME-WAIT`.)*
4. §11.4 describes sockets as file descriptors. **Name three things that work on a socket only because of that**, and one thing that does not.

**On the RIO package (§10.5, used here)**

5. The book wraps `read` and `write` in "robust I/O" functions that loop. **Why is the loop necessary?** Give a concrete case where a single `read` returns fewer bytes than requested.
6. `rio_readlineb` reads a line. **How does it know where the line ends, given that TCP has no message boundaries?**

**On §11.5–11.6**

7. HTTP separates headers from body with a blank line. **What framing problem does that solve, and what are two alternatives?**
8. Read TINY's `doit` function. **How many round trips does serving one static file take?** Compare with the 589 ms page load measured in L27.

**Beyond the book — worth thinking about**

9. The chapter never mentions congestion control. **After L26, explain why a short HTTP response never reaches the link's full speed.**
10. TINY handles one connection at a time. Using **Little's Law** and a 187 ms RTT, how many requests per second can it serve? What would you change?

> **Question 10 is the one that connects this week to Week 7.** The answer is about five, and it has
> nothing to do with the CPU.

---

## Reading Against the Machine

```bash
# 1. Your own latency ladder — do this before Tuesday
ping -c 5 -q 127.0.0.1 ; ip route | grep default ; ping -c 5 -q 1.1.1.1

# 2. The TCP state machine, live
ss -tan | awk 'NR>1{print $1}' | sort | uniq -c | sort -rn

# 3. Where a page load actually goes
curl -s -o /dev/null -w "dns=%{time_namelookup} connect=%{time_connect} \
tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n" https://example.com
```

**Run item 3 twice.** The first has a cold DNS cache. *(Measured here: 4.233 s cold, 0.589 s warm — and `dig` alone reported 1487 ms against 3 ms.)*

**A caution the book cannot give you:** its examples predate IPv6 being routine and use `SIGCHLD` reaping and `select`. **`epoll` is what a modern Linux server uses**, and it is PROG 201's material this term — the book's approach is correct and no longer idiomatic.

---

## Terminology You Should Own by Week 9

| | | |
|---|---|---|
| OSI / TCP-IP model | encapsulation | MTU |
| MAC address | IP address | CIDR prefix |
| port | four-tuple | socket |
| three-way handshake | SYN / SYN-ACK / ACK | `TIME-WAIT` |
| sequence number | acknowledgement | retransmission |
| flow control | advertised window | congestion control |
| slow start | AIMD | fast retransmit |
| Nagle's algorithm | delayed ACK | `TCP_NODELAY` |
| byte stream | framing | length prefix |
| RTT | round-trip elimination | CDN |

---

## If You Want More

**Kurose & Ross, chapters 1 and 3** are the standard undergraduate treatment and are genuinely well written. **Chapter 3 covers what L26 compresses into one lecture** — reliable delivery, flow control and congestion control with the derivations. **This is CS 302's textbook**, so reading it now is not wasted.

**`man 7 tcp`** documents every socket option and kernel tunable, including `TCP_NODELAY` and the delayed-ACK behaviour. **Look up `TCP_NODELAY` and `TCP_QUICKACK` after Lab 8** — the descriptions read differently once you have produced the deadlock yourself.

**"It's Always DNS"** is a joke with a measurement behind it: 1487 ms against 3 ms, verified this week. **`dig +trace example.com`** shows the full recursive walk from the root servers, and is worth running once to see where a cold lookup's time goes.

**High Performance Browser Networking** (Ilya Grigorik, free online) is the best treatment of *why* protocols changed — the chapters on TCP, TLS and HTTP/2 are essentially L27 §5 at book length, with the round-trip accounting done properly.

---

*CS 201 · Week 8 · Reading Guide*
