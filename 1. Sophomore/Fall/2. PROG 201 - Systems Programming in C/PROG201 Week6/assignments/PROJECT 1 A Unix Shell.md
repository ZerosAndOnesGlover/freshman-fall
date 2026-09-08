# PROG 201 · Project 1
## `tsh` — A Unix Shell

---

**Assigned:** Week 6, Friday · **Due:** Week 9, Friday 17:00
**Weight: 12.5% of the course** · Submit one PDF, `P1_{LastName}_{StudentID}.pdf`, and your code as `P1_{LastName}.tar.gz`

> **This is a project, not a problem set.** Three weeks, one program, and the marks are weighted
> toward it working rather than toward answering questions about it.
>
> **You already have half of it.** PS 6 is the parser, executor and builtins; Lab 6 is the job
> table and `tcsetpgrp`. **Both are yours to reuse in full** — that is what they were for. What this
> project adds is the rest of job control, robustness, and a test suite that proves it.
>
> Collaboration: discussing approaches is fine. The code must be yours, including the parts you
> are reusing from your own PS 6 and Lab 6.
>
> Compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.

---

### What It Must Do

```
tsh> ls -l /etc | grep hosts | wc -l          # pipelines, any length
tsh> sort < in.txt > out.txt 2> err.txt       # < > >> 2>
tsh> make -j4 &                               # background jobs
tsh> jobs                                     # the job table
tsh> fg %1                                    # and bringing one back
tsh> sleep 100
^Z                                            # Ctrl-Z stops it
tsh> bg                                       # and bg resumes it
tsh> cd /tmp                                  # builtins that must be builtins
tsh> exit
```

and it must **survive** everything in Part 4.

---

## Part 1 — The Language (20 points)

Everything in PS 6 Q1 and Q2, working. Reuse your own code.

**[16]** Tokeniser, parser, *n*-stage pipelines, four redirections, background, and syntax errors reported before anything is forked.

**[4]** **One extension of your choice**, implemented and documented:

| Extension | What it adds |
| --- | --- |
| Quoting: `"a b"` and `'a b'` and `\ ` | a state machine in the tokeniser |
| `;` and `&&` and `\|\|` | a grammar with sequencing, and a tree |
| Per-stage redirection: `a > f1 \| b > f2` | moving the redirections into `struct stage` |
| Globbing with `glob(3)` | an expansion pass between tokenise and parse |
| `$VAR` expansion | the same pass, and a decision about when |

State which you chose, show it working, and **say what you had to change and where** — the point of the mark is the structural answer, not the feature.

---

## Part 2 — Job Control (32 points)

**[10] The job table.** Ids, pgids, every pid, state, process count, and the command line. `jobs` prints it in `bash`'s format with `+` and `-`.

**[10] Stopping and continuing.** `WUNTRACED` and `WCONTINUED`; Ctrl-Z reports `[n]+ Stopped`; `fg` and `bg` work with and without a `%n` argument; `fg` hands over the terminal **before** the `SIGCONT`.

**[6] The terminal.** `tcsetpgrp` in both directions with `SIGTTOU` ignored around it; terminal modes saved at startup and restored after every foreground job.

**[6] Reporting.** Background completions appear at the **next prompt**, not mid-line, and say what happened: `Done`, `Terminated`, `Stopped`. A job is finished when its **last** process is.

---

## Part 3 — Robustness (20 points)

**[6] Signals.** The shell ignores `SIGINT`, `SIGQUIT`, `SIGTSTP`, `SIGTTIN`, `SIGTTOU`; **children get the defaults back before `exec`** — a child that inherits `SIG_IGN` for `SIGINT` cannot be interrupted, and that is a bug you will only find by testing it.

**[6] Startup and shutdown.** The startup sequence from L20 §7, including waiting to be foregrounded and tolerating already being a session leader. On `exit` with stopped jobs: warn, and say in your write-up what happens to them if the user exits anyway.

**[4] Non-interactive.** `./tsh < script.txt` and `echo 'ls | wc -l' | ./tsh` must work, with no prompt and no job-control calls — `isatty` decides. **This is how your test suite will drive it.**

**[4] Resource hygiene.** No descriptor leaks (check with `ls /proc/$$/fd` after a hundred pipelines), no zombies (`ps` after a hundred background jobs), no unbounded growth in the job table.

---

## Part 4 — Proving It (18 points)

**[12] A test suite.** A script that runs your shell non-interactively and checks its output against `bash`'s, the way Lab 1's `compare.sh` did. At least **twenty** cases, covering:

- pipelines of 1, 2 and 4 stages;
- each redirection, including `>>` appending to an existing file;
- exit statuses: success, failure, `command not found` (127), and a signalled child (`128 + n`);
- every syntax error your parser rejects;
- `yes | head -1` terminating.

Report how many pass. **A failing case you have documented is worth more than a case you removed**, and the write-up should say which ones fail and why.

**[6] Job control cannot be tested that way**, because it needs a terminal. Demonstrate it instead: a session transcript covering Ctrl-Z, `jobs`, `fg`, `bg`, `kill %n`, a background pipeline as one job, and Ctrl-C reaching a foreground job rather than the shell.

Annotate the transcript with what each line proves.

---

## Part 5 — The Write-Up (10 points)

Four pages at most.

**[4]** **Three bugs you had and fixed**, with the symptom, the diagnosis and the fix. At least one must have been diagnosed from **outside** the process — `ps`, `strace`, `/proc`. This is the most useful part of the document and it is marked as such.

**[3]** **What your shell does not do**, honestly, and for each the structural reason. "No `&&`" is a fact; "no `&&`, because my parser produces a flat list of stages and `&&` needs a tree" is an answer.

**[3]** **One measurement of your own shell**, with a number and an explanation. Builtin against external, pipeline setup cost, startup time against `dash` — anything, provided you say what it is per (Week 4's habit) and what it tells you.

---

## Marks

| Part | Topic | Points |
|---|---|---:|
| 1 | The language | 20 |
| 2 | Job control | 32 |
| 3 | Robustness | 20 |
| 4 | Proving it | 18 |
| 5 | The write-up | 10 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. **Projects are not dropped** — the "lowest problem set dropped" rule covers problem sets only.

---

## Advice

**Do the parts in the order they are numbered, and get each one working before the next.** A shell that does pipelines perfectly and has no job control scores 40 of 100; a shell that half-does everything scores less than that and is much harder to debug.

**Test non-interactively from day one.** Part 3's `isatty` check is not an afterthought — it is what lets you have a test suite at all, and the students who add it last spend Week 9 debugging by hand.

**Keep a log of the bugs as you hit them.** Part 5 asks for three, and reconstructing them in Week 9 from memory is much harder than writing them down in Week 7.

---

*PROG 201 · Weeks 6–9 · Project 1 · © CSE Department*
