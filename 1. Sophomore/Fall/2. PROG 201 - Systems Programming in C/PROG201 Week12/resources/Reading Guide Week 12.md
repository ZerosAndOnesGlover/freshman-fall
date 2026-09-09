# PROG 201 · Reading Guide · Week 12
## The manuals, one classic, and the discipline of running unattended

---

**This week has no single paper — it has the operational wisdom that lives in man pages and in one
short, famous document about signals.** Everything below is on the machine. Read `signal-safety(7)`
slowly; it is the densest, most consequential page in the whole course.

| Source | Read? | Why |
|---|---|---|
| **`man 7 signal-safety`** | **All of it — twice** | The list of functions a handler may call. L37 §2. The bug that hides for months |
| **`man 7 signal`** | **All of it** | Disposition, delivery, `EINTR`, `SIGKILL`/`SIGSTOP` uncatchable. L37 |
| `man 2 sigaction` | Read | Why `sigaction` over `signal`; `SA_RESTART`, `sa_mask`. L37 §2 |
| **`man 2 poll`** (or `man 7 epoll`) | **Read** | The event loop the self-pipe plugs into. L37 §3, L38 §2 |
| Bernstein, *the self-pipe trick* (cr.yp.to) | **Read** | Two pages; the idiom in its original statement. L37 §3 |
| `man 3 pthread_cond_wait` | Read | Why the wait releases the lock atomically. L38 §1 |
| **`man 2 accept`**, `man 7 socket` | Skim | `ECONNABORTED`, the listen backlog, `SO_REUSEADDR`/`SO_REUSEPORT`. L38 |
| **`man 2 setuid`**, `man 2 setgroups` | **Read together** | The privilege-drop order, and the group-list trap. L39 §1–§2 |
| `man 7 capabilities` | Skim | `CAP_NET_BIND_SERVICE` — bind :80 without root. L39 §3 |
| **`man 5 systemd.service`**, `man 5 systemd.exec` | **Read the resource + drop directives** | `Restart=`, `User=`, `MemoryMax=`, `AmbientCapabilities=`. L39 §3 |
| CS:APP §12.7 (concurrency issues) + §10.11 | Skim | Thread safety, reentrancy, races — the textbook's version. L37–L38 |

---

## `signal-safety(7)` — the page that matters most

1. Write down five functions that **are** async-signal-safe and five that are **not**. Which category are `printf`, `malloc`, `free`, and `write` in? Why is `malloc`-in-a-handler a deadlock waiting to happen? *(L37 §2.)*
2. Your "obvious" cleanup handler calls `fprintf(stderr, ...)` and `exit()`. Name both bugs, and rewrite it as a one-line self-pipe handler. *(L37 §3.)*
3. `SIGKILL` and `SIGSTOP` cannot be caught. What does that mean a daemon can and cannot promise about its own shutdown, and what is the operator's `SIGTERM`-then-`SIGKILL`-after-a-timeout contract? *(L37 §4.)*

## `poll`/`accept` — the event loop

4. A signal is delivered while you sit in `poll`. What does `poll` return, and what must the surrounding code do? What happens to a daemon that does not expect it? *(L37 §2.)*
5. `accept` can return `-1` with `ECONNABORTED` (the client reset between the SYN and your accept). Why must a server treat this as "try again" rather than "fatal"? *(L38 §1.)*
6. Sketch how you would replace one `poll` over two fds with an `epoll` loop over thousands of connections. What does this fix about the ~36 k req/s accept-bound ceiling in L38 §2?

## `setuid` + `setgroups` — read these two together, always

7. Write the three-call privilege-drop sequence in the correct order and justify each position: why `setuid` **last**, why `setgroups(0,NULL)` **first**? *(L39 §1.)*
8. A daemon calls `setgid` and `setuid` but not `setgroups`. `getuid()` shows the unprivileged uid. What is still true about the process, and which **one line of `/proc/self/status`** reveals it? Why is this the course's seventh "present but not working"? *(L39 §2.)*
9. `AmbientCapabilities=CAP_NET_BIND_SERVICE` in a unit file. What does it let the process do, and why is it strictly better than "start as root, bind, drop"? Relate it to Week 11's "root is ~40 capabilities." *(L39 §3.)*

## `systemd.service` / `systemd.exec` — the operational contract

10. Map each of `Restart=on-failure`, `User=`, `MemoryMax=256M`, `TasksMax=512` to the thing it replaces in a hand-rolled daemon. Which two are Week 11 cgroup controls under another name? *(L39 §3.)*
11. Why does modern practice run the daemon **in the foreground** and log to **stderr** rather than double-`fork`/`setsid` and write a PID file? What does the supervisor own that the daemon used to?

---

## Two questions that close the course

12. **The synthesis.** Take the reference daemon and name, for each of Weeks 0–11, one thing it inherits from that week (fds, threads, condvars, sockets, signals, the parser, the build method, the container). Which week contributes the *measurement discipline* that produced every table in Week 12? *(L39 §5.)*
13. **The recurring law.** List all seven "present but not working" findings (Weeks 3, 8, 10, 10, 11, 12, 12). For each, name the single measurement that exposed the gap between present and working. What do those measurements have in common, and what does that tell you about how to trust your own code? *(L39 §5.)*

---

*PROG 201 · Week 12 · Reading Guide · © CSE Department · end of the reading sequence*
