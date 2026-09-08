# PROG 201 · Problem Set 5
## A Concurrent HTTP/1.0 Server

---

**Released:** Week 5, Wednesday · **Due:** Week 6, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS5_{LastName}_{StudentID}.pdf`, and your code as `PS5_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **Lab 5 is sat 16:00–17:50 on the day this is due.** Submit before you come to the lab. Nothing
> in the lab needs this code and nothing in this problem set needs the lab, but the two overlap on
> the calendar and the deadline does not move for it.
>
> **Fall Break is the Monday of Week 6.** You have one fewer working day than usual. Start Q1 in
> Week 5.
>
> **Q4 is measurement on your own machine.** State your `gcc --version`, `uname -r`, `nproc`, and
> whether you are on BH 215 or your own hardware.
>
> Everything compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.
> Link with `-lpthread`.

---

### The Server

`httpd.c`, serving files out of a directory over HTTP/1.0:

```
./httpd <port> <docroot> <model> [workers]
```

where `model` is one of `fork`, `thread`, `pool` or `epoll`. It must work with a real client:

```
$ curl -sv http://127.0.0.1:19000/index.html
$ curl -s  http://127.0.0.1:19000/nope        # 404
$ curl -sI http://127.0.0.1:19000/index.html  # HEAD
```

HTTP/1.0 is a small enough protocol to implement honestly in an evening: a request line, some headers you may ignore, a blank line, and a response whose end is the connection closing.

---

### Q1: The Server (30 points)

**(a) [12]** Parse the request. A request line is `METHOD SP TARGET SP VERSION CRLF`, followed by header lines, followed by an empty line.

Requirements:

- **Read until you have the blank line**, not until one `read` returns. A request can arrive in two packets, and it will as soon as you test with something other than `curl` on loopback. (L16 §6.)
- Support `GET` and `HEAD`. Anything else is **405**.
- A malformed request line is **400**. Decide what malformed means and say so.
- **Bound the request.** A client that sends headers forever must not grow your memory without limit — pick a cap, return **431** or **400**, and say what you chose.

**(b) [12]** Serve the file.

- `200` with `Content-Length` and a plausible `Content-Type` for at least `.html`, `.txt`, `.css`, `.png` and one binary type. Everything else is `application/octet-stream`.
- `404` when it does not exist, `403` when it exists and cannot be read.
- `HEAD` sends the headers and no body.
- A request for `/` serves `index.html` if it exists and returns 404 or a listing otherwise — your choice, defended in one sentence.

**(c) [6]** **Do not serve `/../../etc/passwd`.**

Say exactly how you prevent it. `realpath()` the resolved path and check it is still under the document root is the answer expected; rejecting `".."` textually is **not** sufficient, and your write-up should say why (consider `%2e%2e`, and a symlink inside the docroot).

Demonstrate with three requests: a normal file, a `..` traversal, and a symlink pointing outside the root. **Show the response codes.**

---

### Q2: Concurrency (20 points)

**(a) [12]** Implement **two** of the four models, one of which must be `pool` or `epoll`.

For `fork`: the child closes the listening socket, the parent closes the connection, and `SIGCHLD` is handled — say which of the three you got wrong first.

For `thread`: detach or join, and **check `pthread_create`'s return value** (Week 3 L10 §4). Say what your server does when it fails, and why that is better than what it did before you handled it.

For `pool`: Week 3's PS 3 bounded queue with descriptors in it. State your queue's capacity and what happens when it is full.

For `epoll`: every socket non-blocking, an output buffer per connection, and `EPOLLOUT` when a `write` returns `EAGAIN` (L18 §4). This is the most work of the four and the only one that will teach you what a state machine per connection means.

**(b) [8]** A table of what each of your two models does in each of these situations, and one sentence each on why:

| | model A | model B |
| --- | --- | --- |
| a client connects and sends nothing, forever | | |
| a client sends a request and stops reading the response | | |
| the handler segfaults | | |
| 10,000 clients connect at once | | |

The second row is the interesting one: **a slow reader fills your socket buffer and blocks your `write`.** Say for how long, and what that costs each model.

---

### Q3: Make It Survive (18 points)

**(a) [6]** Three failure modes, each demonstrated with output:

- A client that disconnects mid-response. **Your server must not die.** Say which of the three `SIGPIPE` remedies you used and why (L16 §6).
- A `write` that returns fewer bytes than you asked for. Show that your `write_all` handles it — force it by setting a tiny `SO_SNDBUF` on the connection and serving a large file.
- A file that is deleted between your `stat` and your `open`. Say what your code does, and name the general class of bug. *(It has a name, and Week 1 L05 §5 met it as "two system calls are not one".)*

**(b) [6]** `ss -ltn` while your server runs under load. Report `Recv-Q` and `Send-Q` for the listening socket at concurrency 10 and at concurrency 500.

Explain what the two columns mean for a **listening** socket — they do not mean what they mean for a connected one — and say what a persistently high `Recv-Q` tells you about your `accept` loop. (L16 §4.)

**(c) [6]** Set `listen`'s backlog to 1 and hit the server with 100 concurrent connections. Report how many clients fail, how many succeed slowly, and the **latency distribution**.

Then answer: why do the excess clients not get `ECONNREFUSED`? Your answer must describe what the kernel does with the SYN.

---

### Q4: Measure It (18 points)

Use your Lab 5 load generator, or write a smaller one. **State which.**

**(a) [8]** Your two models, at concurrency 1, 10, 50, 200 and 500, serving a small file. Report requests/second and p50, p99 and max latency for each. Ten data points.

**(b) [6]** Add 2 ms of artificial delay to your handler — a `usleep`, standing in for a database call — and repeat at concurrency 50.

If one of your models is `epoll`, **its number will collapse to roughly 500 req/s**. Explain it. If neither of your models is `epoll`, predict what would happen and say why.

**(c) [4]** Serve a 100 MiB file three ways — `read`+`write`, `mmap`+`write`, and `sendfile` — and report the rate **and** the process's `ru_maxrss` for each.

**Run each in a separate process.** `ru_maxrss` is a high-water mark for the life of the process, so measuring all three in one run gives you the largest of them three times. Say so in your write-up; getting this wrong and noticing is worth as much as getting it right.

Then say which of the two columns is the better argument for `sendfile` in a server, and why.

---

### Q5: The Protocol and the Options (14 points)

**(a) [4]** Your server closes the connection to signal the end of a response. Name the two things that costs, one on the client and one on the server, and give the header HTTP/1.1 introduced to avoid both.

**(b) [4]** Set `TCP_NODELAY` on accepted connections and measure the difference for a small response. Report it. If you see no difference, say why not — and be specific about the shape of an HTTP exchange versus L18 §5's experiment.

**(c) [3]** You did not set `SO_RCVBUF` and you should not. In two sentences, say what Linux does that you would be overriding.

**(d) [3]** Your server binds `AF_INET`. Give the three changes that make it dual-stack, and name the option whose default varies between machines.

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*PROG 201 · Week 5 · PS 5 · © CSE Department*
