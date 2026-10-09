# PROG 201 · Systems Programming in C
## Week 12 · Lecture 3 of 3
### Running Unattended, and the Synthesis

*“The notion of "intricate and beautiful complexities" is almost an oxymoron. Unix programmers vie with each other for "simple and beautiful" honors — a point that's implicit in these rules, but is well worth making overt.”* — Doug McIlroy, as quoted in Eric S. Raymond, *The Art of Unix Programming* (2003)

---

**Reading:** TLPI Ch. 37 (daemons), Ch. 38 (setuid) · `man 2 setuid`, `man 2 setgroups`, `man 5 systemd.service`, `man 7 capabilities` · **Previous:** L38 — concurrency and capacity · **Next:** Lab 12 (demo day), Project 2

**Coursework:** 📋 **Project 2** due Fri this week 17:00 · 📝 **PS 11** due Fri this week 17:00 · 🔬 **Lab 12** Mon of the completion period

---

## 1. The Privileged-Port Problem, and Dropping What You Took

A web server listens on port 80. Binding a port below 1024 is privileged — measured, as an ordinary user:

```
$ ./httpd 80 1
bind :80: Permission denied              # EACCES
```

So a real web server has a bootstrapping problem: it must **start as root** to bind port 80, but it must **not still be root** while it parses bytes from the open internet, because a bug in that parser (Week 10, every bug in Week 10) would then be a root compromise of the host. The pattern, as old as Unix daemons, is: **start privileged, take exactly what needs privilege, then drop to an unprivileged user for the lifetime of the process.**

```c
/* as root, early: */
listen_fd = bind_and_listen(80);        /* the one privileged act */
/* then irreversibly drop: */
setgroups(0, NULL);                     /* <-- drop supplementary groups FIRST */
setgid(pw->pw_gid);                     /* then gid */
setuid(pw->pw_uid);                     /* then uid -- last, or you lose the privilege to do the rest */
```

The order is not decoration. `setuid` last, because once you drop the uid you no longer have the privilege to call `setgid` or `setgroups`. And `setgroups(0, NULL)` **first** — which brings the week's recurring trap.

---

## 2. `setuid` Without `setgroups` — the Present-but-Not-Working Finale

A daemon that calls `setgid` and `setuid` but **forgets `setgroups(0, NULL)`** looks like it dropped privilege — `getuid()` returns the unprivileged uid, `id` shows the new user — and it did not. The process **keeps root's supplementary group memberships**, because `setuid` drops the *user* identity but never touches the *group list*. If root was in the `docker` or `disk` or `shadow` group, the "unprivileged" server still is, and an attacker who exploits the parser inherits those groups.

You can read it directly, and this is the measurement that matters — not `getuid()`, which lies by omission, but `/proc/self/status`:

```
# after setuid()+setgid() but WITHOUT setgroups(0,NULL):
Uid:  1000  1000  1000  1000
Gid:  1000  1000  1000  1000
Groups:  0 4 27 998           <-- still in root's groups (0=root, 27=sudo, ...)

# with setgroups(0,NULL) first:
Groups:                       <-- empty. actually dropped.
```

This is the **seventh and final** appearance of the course's law — *a mechanism present is not a mechanism working*. The privilege drop is present (`setuid` returned 0, `getuid` confirms the new uid) and not working (the supplementary groups survive). It is the same shape as the SIGPIPE trap in L37, the `mount` EPERM in Week 11, the inert CET in Week 10, and it closes the pattern with the most consequential example of all, because here the thing that looks done and is not is *the security boundary the whole daemon rests on.* The way you know is not that `setuid` succeeded — it did — but that you read `Groups:` in `/proc/self/status` and saw it empty.

> On the reference machine you cannot bind :80 or become another user without root, so this is taught by reading the two `/proc/self/status` outputs and by the CET/mount precedent — the same honest handling as Week 11's stripped capabilities. The lab has you exhibit the group list; the mechanism is not in doubt, only the privilege to run it on this image.

---

## 3. Supervision and Resource Limits: the Daemon Does Not Supervise Itself

A production daemon does **not** daemonize itself with the old double-`fork`/`setsid` dance, does not write its own PID file, and does not restart itself when it crashes. Modern practice inverts all of that: the daemon runs in the **foreground**, logs to **stderr**, and lets a **supervisor** — `systemd` — own its lifecycle. The unit file is the operational contract:

```ini
[Service]
ExecStart=/usr/local/bin/httpd 80 8
Restart=on-failure              # crash -> systemd restarts it
User=www-data                   # systemd drops privilege for you (see §2, done right)
MemoryMax=256M                  # cgroup memory cap (Week 11)
TasksMax=512                    # cgroup pids cap (Week 11)
AmbientCapabilities=CAP_NET_BIND_SERVICE   # bind :80 WITHOUT being root at all
NoNewPrivileges=true
```

Two things to read here. First, **the supervisor does the hard parts correctly**: `User=` drops privilege with the group list handled, `Restart=on-failure` turns a crash into a blip, and — elegantly — `AmbientCapabilities=CAP_NET_BIND_SERVICE` grants *just* the one capability to bind a low port (Week 11's "root is ~40 capabilities" — hand over only that one), so the process never needs to be root at all and §2's whole dance becomes unnecessary. Second, **`MemoryMax` and `TasksMax` are the Week 11 cgroup controls** applied to a service: the same `memory.max` that OOM-killed the hog at exit 137 now bounds the daemon, and the same `pids.max` that stopped the fork bomb now caps its threads. The reference `httpd`'s measured footprint — **RSS flat at 1728 kB** (L38) — sits four orders of magnitude under a 256 MB cap, so the cap is a safety net against a leak bug, not a routine constraint. Resource control you learned as a container primitive is, here, one line of a service file.

---

## 4. The Untrusted Parser: Week 10 Applied at the Front Door

Everything a network daemon reads is written by an adversary. The request parser is the attack surface, and Week 10 is the discipline that hardens it — applied here as a routine, not a special event:

- **Bounded reads, no `gets`-shaped code.** `read` into a fixed buffer with the size passed; never trust a `Content-Length`; reject a request line longer than the buffer instead of overflowing it (Week 10 L31).
- **Compile with the guards on** — `-Wall -Wextra -Werror`, `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, `-fsanitize=address,undefined` in CI. The canary, NX and fortify that Week 10 watched catch attacks are simply the default build.
- **Fuzz the parser** (Week 10 L33). The parser is a pure function from bytes to a parsed request — the ideal `libFuzzer` target. `LLVMFuzzerTestOneInput(data, size)` calls the parser on the fuzzer's mutated input; coverage guidance drives it into the branches your tests never reached, and ASan turns any overflow into an immediate, located crash. A daemon whose parser has survived a few million fuzz iterations under ASan is in a different category of trustworthy than one that "passed the tests."

The synthesis: the parser is fuzzed (Week 10), the process runs unprivileged with dropped groups (§2) inside a cgroup budget (Week 11), behind a supervisor that restarts it (§3), and its own code ignores SIGPIPE and drains on SIGTERM (L37). **Defence in depth is not one wall; it is every layer of the course stacked so that a failure of any one is caught by the next.**

---

## 5. What the Course Was About

Twelve weeks, and the daemon is where they converge. Trace the assembly:

- **Weeks 0–2 (processes, `fork`/`exec`, I/O and redirection):** the daemon is a process that manages file descriptors precisely — the fds measured flat in L38 are the same discipline as wiring a pipe in Week 2.
- **Weeks 3–4 (threads, synchronisation, virtual memory):** the thread pool, the condition variables, the bounded queue, and the flat RSS.
- **Weeks 5–6 (sockets, the concurrent server, the shell):** the server itself, and the signal/job-control machinery that becomes graceful shutdown.
- **Week 7 (filesystems):** what the daemon serves and how it logs.
- **Weeks 8–9 (dynamic linking, performance):** the build, and the measure-don't-guess method that produced every table this week.
- **Week 10 (security):** the hardened, fuzzed parser at the front door.
- **Week 11 (containers):** the isolation and resource budget it runs inside.
- **Week 12 (this):** the assembly, and the operational judgement — drain don't drop, measure don't assert, drop privilege and prove it, cap the resources, let the supervisor supervise.

And running through all of it, the one idea the course returns to seven times: **a mechanism present is not a mechanism working.** `PRIO_INHERIT`, lazy binding, ASLR-without-PIE, inert CET, the stripped user namespace, the SIGPIPE trap, and — last — the privilege drop that keeps root's groups. The engineer this course was trying to build is not the one who wrote the `setuid` call. It is the one who then read `/proc/self/status` to check that it worked.

**That is the whole degree of it: the difference between working code and code that runs unattended is the measurement you took after you thought you were done.**

---

## Summary

- **Privileged ports need root to bind** (measured: `bind :80` → EACCES unprivileged), so a daemon **starts privileged, takes only what needs privilege, and drops** — `setgroups(0,NULL)` then `setgid` then `setuid`, in that order (`setuid` last, or you lose the privilege to do the rest).
- **`setuid` without `setgroups` is the week's final "present but not working":** the drop looks complete (`getuid` shows the new uid) but the process **keeps root's supplementary groups** — visible only by reading `Groups:` in `/proc/self/status`, empty only when `setgroups(0,NULL)` ran. The **seventh** entry in the course's central table, and the most consequential.
- **Supervision is inverted:** the daemon runs foreground, logs to stderr, and `systemd` owns its lifecycle — `Restart=on-failure`, `User=` (privilege dropped correctly), `MemoryMax`/`TasksMax` (the Week 11 cgroup caps), and `AmbientCapabilities=CAP_NET_BIND_SERVICE` (bind :80 with one capability instead of full root).
- **The parser is the attack surface:** bounded reads, the Week 10 compile-time guards on by default, and `libFuzzer`+ASan on the parse function as routine CI.
- **The synthesis:** fuzzed parser (W10) + dropped privilege + cgroup budget (W11) + supervisor restart + SIGPIPE-ignored/SIGTERM-drain (L37) = defence in depth, every course layer catching the failure of the one before.
- **The course in one line:** the difference between working code and code that runs unattended is the measurement you take after you think you are done.

---

## Exercises

1. Write the privilege-drop sequence and read `/proc/self/status` before and after. Then delete the `setgroups(0,NULL)` line and read `Groups:` again. What is still there, and why is `getuid()` a liar about it?
2. Why must `setuid` come last in the three-call sequence? Show what fails if you call it first.
3. Write a `systemd` unit for the reference `httpd` with `Restart=on-failure`, `User=`, `MemoryMax=256M`, and `AmbientCapabilities=CAP_NET_BIND_SERVICE`. Explain what each line replaces from the "do it yourself" daemon.
4. `AmbientCapabilities=CAP_NET_BIND_SERVICE` lets the process bind :80 without being root. Relate this to Week 11's "root is ~40 capabilities" and explain why it is safer than starting as root and dropping.
5. Turn the request parser into a `libFuzzer` target (`LLVMFuzzerTestOneInput`). Plant one overflow and show ASan locating it. Why is a parser an especially good fuzz target?
6. `MemoryMax=256M` on a daemon whose measured RSS is 1.7 MB — what is the cap *for*, given it will never be hit in normal operation? Relate it to the Week 11 OOM measurement.
7. List the seven "present but not working" findings of the course (Weeks 3, 8, 10×2, 11, 12×2). For each, name the single measurement that revealed the gap. What do those measurements have in common?

---

*PROG 201 · Week 12 · L39 · © CSE Department · end of the lecture sequence*
