# PROG 201 · Reading Guide · Week 5
## Stevens, still, and the one web page everybody in this field has read

---

**This is the week where the reading is a person rather than a chapter.** W. Richard Stevens wrote *UNIX Network Programming* in 1990 and it is still the book; APUE Chapter 16 is his own condensed version of it, and TLPI's socket chapters are Kerrisk doing the Linux specifics Stevens could not.

And then there is **Dan Kegel's C10K page**, written in 1999, updated until 2014, and the single most-read document about servers ever posted. It is not long. Read it after L17.

| Source | Read? | Why |
|---|---|---|
| **APUE Ch. 16** | **All of it** | Sockets, end to end, in fifty pages. This is L16 |
| **TLPI Ch. 56–57** | **All of it** | Sockets and Unix domain sockets, with the Linux detail |
| **TLPI Ch. 58–59** | **Read** | Internet domain sockets, `getaddrinfo`, byte order |
| **TLPI Ch. 60** | **Read** | Server design: iterative, concurrent, and the trade-offs |
| **TLPI Ch. 61** | **Read** | Advanced topics: `shutdown`, `sendfile`, `TCP_NODELAY`, `SO_LINGER` |
| **TLPI Ch. 63** | **All of it** | `select`, `poll`, `epoll`, signal-driven I/O. This is L18 |
| **Kegel, *The C10K Problem*** | **All of it** | Twenty pages on the web. The argument L17 measures |
| UNIX Network Programming Vol. 1 | Reference | If your library has it, §6 and §16 are the definitive treatment |

---

## APUE Chapter 16 — the questions to hold

**§16.2 Socket descriptors**

1. Stevens lists the socket types. Which of them gives you message boundaries, and which gives you the Week 2 framing problem back? Write down what that means for a protocol you design.
2. `SOCK_STREAM` over `AF_UNIX` against a pipe: name two things the socket gives you that the pipe does not. *(One of them is why systemd, X11 and Docker all use Unix sockets.)*

**§16.3 Addressing**

3. Byte order. Write down what `htons(8080)` is in hex, and what a server that forgot it would listen on. **Then check with `ss`.**
4. Stevens covers `getaddrinfo` and the older `gethostbyname`. Find one reason `gethostbyname` cannot be fixed. *(Look at its return type and think about threads — Week 3.)*
5. `getaddrinfo` returns a **list**. Find the sentence that says why, then write the client loop that uses it properly.

**§16.4 Connection establishment**

6. `listen`'s second argument. Stevens describes it as a hint; Linux treats it as a limit on the *accepted* queue. Find what `man 2 listen` says about `somaxconn`, and reconcile the two.
7. **`accept` returns a new descriptor.** Say in one sentence what the listening socket is for after that, and what happens if you `read` from it.

**§16.5 Data transfer**

8. `send`/`recv` against `write`/`read`. What do the flags buy you? Find `MSG_NOSIGNAL` and `MSG_PEEK` and say when each is the right answer.
9. Stevens shows a `readn`/`writen` pair. Compare with your Week 1 `write_all` — is there anything he handles that you did not?

**§16.6 Socket options**

10. Read the `SO_REUSEADDR` discussion, then read `man 7 socket`'s. **They emphasise different things.** Which one explains `TIME_WAIT`, and which explains multicast?

---

## The C10K Problem — read it as history and as a checklist

11. Kegel lists five or six I/O strategies. **Tick off the ones you measured in Lab 5**, and name the two that Linux no longer offers (real-time signals, and `/dev/poll`).
12. He wrote it when a machine had 1 GB of RAM. Work out, from L17 §7's measurements, what the per-connection cost actually is now for an event-driven server — and then say what makes C10M hard, since it is clearly not memory.
13. Find where he discusses threads. His conclusion about thread-per-connection was right in 1999 and is **half wrong now**. Which half, and what changed? *(L17 §7's 7,637 is the surviving half.)*

---

## The Man Pages for This Week

| Page | The paragraph |
|---|---|
| **`man 7 tcp`** | The socket-options list, and everything it says about `TCP_NODELAY` and `TCP_CORK` |
| **`man 7 epoll`** | The "Level-triggered and edge-triggered" section and **Example 2**. Read both twice |
| **`man 2 listen`** | The `backlog` and `somaxconn` paragraph, and the note about the queue length |
| **`man 3 getaddrinfo`** | The `ai_flags` table, and the EXAMPLES section, which is a working client and server |
| `man 7 socket` | `SO_*` in full. Reference, not reading |
| `man 2 sendfile` | Short. Note what it says about the output descriptor |

**And one command:** `ss -tan` and `ss -ltn`. Run them while your server is under load in Lab 5. Everything in L16 §4 and §5 is visible in that output, and being able to read it is half of diagnosing a server.

---

## Where to Go Deeper

| Source | Topic |
|---|---|
| Nagle, RFC 896 (1984) | Two pages, and it is L18 §5's first algorithm in the author's own words |
| RFC 1122 §4.2.3.2 | Delayed ACK, and the requirement that produces the 40 ms |
| `man 7 udp`, and TLPI §58.6 | The protocol this week deliberately skipped |
| Kerrisk, *The Linux Programming Interface* Ch. 62 | Terminals — which is Week 6's job control |
| Axboe, *Efficient IO with io_uring* (2019) | Twenty pages. What comes after `epoll` (L18 §8) |
| Cloudflare and Netflix engineering blogs | Where these options get tuned in anger, with numbers |

---

## The Habit for This Week

**Look at the socket, not just at your program.**

Every previous week's habit was about your own code. This one is not: a networked program has a second party and a kernel between you, and **most of what goes wrong is visible from outside the process and invisible from inside it.**

- A `Recv-Q` that sits near `Send-Q` on a listening socket says your `accept` loop is behind — and your program has no way to notice.
- Eleven thousand sockets in `TIME_WAIT` says your client opens a connection per request — and the program that will fail is the *next* one to run.
- A latency that is a round 40 ms says Nagle and delayed ACK, not slow code.
- A client that "connected fine" to a server that ran out of threads was never served — and both sides think the other is at fault.

`ss`, `ss -i`, `/proc/net/sockstat`, `tcpdump -i lo` and `strace -e trace=network` are the instruments. **Before you change a line of a server that is behaving oddly, look at its sockets.** It is usually there.

---

*PROG 201 · Week 5 · Reading Guide · © CSE Department*
