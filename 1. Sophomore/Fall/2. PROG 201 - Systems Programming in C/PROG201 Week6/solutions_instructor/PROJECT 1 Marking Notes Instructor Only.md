# PROG 201 · Project 1 Marking Notes
## `tsh` — A Unix Shell · Instructor Only

---

**Assigned Week 6 Friday, due Week 9 Friday 17:00, worth 12.5% of the course.**

This file is a marking guide rather than a solution. The reference shell is in `PROG201 Week6/lab/` — the Lab 6 skeleton plus the Lab 6 solutions' five TODOs — and is about 400 lines. **A full-marks submission is not expected to look like it**, and several will be better.

---

## How to Mark This

**Run it before you read it.** Twenty minutes with the shell in front of you tells you more than an hour of reading, and the parts that matter are behavioural.

A twelve-command session that separates a 40 from an 85:

```
ls | wc -l                      # pipelines
yes | head -1                   # closes, and SIGPIPE in the shell
sort < /etc/services | tail -1  # redirection into a pipeline
echo a > /tmp/p1 ; echo b >> /tmp/p1 ; cat /tmp/p1
nosuchcommand                   # 127, and a message naming it
sleep 100 &                     # background
jobs                            # the table
sleep 100                       # then Ctrl-Z
jobs                            # two jobs, one Stopped
fg                              # brings it back; then Ctrl-C
sleep 5 | cat | cat &           # one job, three processes
kill %1 ; jobs                  # gone
exit                            # with a stopped job: does it warn?
```

**Then `ps -o pid,ppid,pgid,sid,tpgid,stat` while a foreground job runs.** If `tpgid` is not the job's `pgid`, Part 2's terminal marks are not earned however good `jobs` looks.

---

## Part 1 — The Language (20)

Reuse of their own PS 6 is expected and explicitly permitted; mark it as new work here only to the extent PS 6 did not already.

**[16]** As PS 6 Q1–Q2. **Deduct here only for regressions** — a student whose PS 6 handled `ls>out` and whose project does not has broken something, and that is worth knowing.

**[4] The extension.** Any of the five, or another with a case made. The mark is for **the structural answer**: *what did you have to change, and where?*

| Extension | The answer that earns the mark |
| --- | --- |
| Quoting | a state machine replaced the `strchr` loop; the executor is untouched |
| `;`/`&&`/`\|\|` | `struct cmd` became a tree; execution became recursive |
| Per-stage redirection | the redirection fields moved from `cmd` into `stage` |
| Globbing | a new pass **between** tokenise and parse |
| `$VAR` | the same pass, and a decision about quoting interacting with it |

A working feature with no structural account is [2].

---

## Part 2 — Job Control (32)

**[10] The job table.** Ids, pgids, **every pid**, state, count, command line. The `getpgid`-after-`waitpid` bug (Lab 6 Q4) reappears here in perhaps a third of submissions; the symptom is `jobs` never clearing.

**[10] Stopping and continuing.** `WUNTRACED` **[3]**, `WCONTINUED` or an equivalent **[2]**, `fg`/`bg` with and without `%n` **[3]**, **terminal handed over before `SIGCONT`** **[2]**.

Test the last one specifically: `cat &`, which stops on `SIGTTIN`, then `fg`. Wrong order fails intermittently — run it three times.

**[6] The terminal.** `tcsetpgrp` both directions **[3]**, `SIGTTOU` ignored around both **[2]**, modes saved and restored **[1]**.

Test the modes: run something that changes them (`stty -echo` in a child, or `vi` and quit badly) and check the prompt still echoes.

**[6] Reporting.** Completions at the next prompt **[2]**, correct wording **[2]**, **a job is done when its last process is** **[2]**. `sleep 5 | cat &` must report once, not twice.

---

## Part 3 — Robustness (20)

**[6] Signals.** The shell ignoring five **[3]**, **children getting the defaults back before `exec`** **[3]**.

The second is the one that is silently wrong: a child that inherits `SIG_IGN` for `SIGINT` cannot be interrupted at all. Test with `sleep 100` in the foreground and Ctrl-C — if nothing happens, this mark is gone, and the student almost certainly never tested it.

**[6] Startup and shutdown.** The L20 §7 sequence **[3]**, tolerating already being a session leader **[1]**, the stopped-jobs warning **[2]**.

The session-leader case: run their shell under `script -qc ./tsh /dev/null`. A shell that exits with `setpgid: Operation not permitted` has not been tested anywhere but an interactive terminal. **This is worth calling out generally** — it is how the reference shell failed first.

**[4] Non-interactive.** `echo 'ls | wc -l' | ./tsh` works, no prompt, no job-control calls. Without this their own Part 4 cannot exist.

**[4] Hygiene.** `ls /proc/<pid>/fd | wc -l` before and after a hundred pipelines **[2]**; no zombies after a hundred background jobs **[1]**; the job table does not fill **[1]**.

---

## Part 4 — Proving It (18)

**[12] The test suite.** Twenty cases **[6]**, the six required categories **[4]**, an honest pass/fail report **[2]**.

**Award the honesty marks generously.** A suite reporting 17/20 with three documented failures is better work than 20/20 with the hard cases removed, and the rubric should visibly reward it — otherwise next year's suites will all report 20/20.

**[6] The job-control transcript.** Six behaviours **[4]**, annotated with what each proves **[2]**. A transcript with no annotation is [2].

---

## Part 5 — The Write-Up (10)

**[4] Three bugs**, with symptom, diagnosis and fix; **at least one diagnosed from outside the process**. The `ps`/`strace`/`/proc` requirement is the point of the section — a student who has never looked at their program from outside has missed the term's recurring habit.

Common genuine bugs, for calibration: the missing parent `close`; `WUNTRACED`; `getpgid` after `waitpid`; `SIGTTOU` stopping the shell; children inheriting `SIG_IGN`; the `fg` ordering; the tokeniser destroying the line needed by `jobs`.

**[3] What it does not do**, with **structural** reasons. "No `&&`" is [1]; "no `&&`, because my parser produces a flat list and `&&` needs a tree" is [3].

**[3] One measurement**, with a number, a unit, **what it is per**, and an explanation. Week 4's habit, and it is worth naming that in the feedback.

---

## Grade Boundaries, Roughly

| | |
| --- | --- |
| **~40** | Pipelines, redirection and builtins work; no job control |
| **~60** | Job control works interactively but breaks under `ps` inspection — wrong `tpgid`, or the `SIGCONT` ordering |
| **~75** | Everything works; the test suite is thin or the write-up is a feature list |
| **~85** | A real test suite with documented failures, and three real bugs in the write-up |
| **~95** | The above, plus an extension whose structural account is correct |

**The most common shape of a 60** is a shell that works perfectly when a person drives it and has never been run non-interactively or looked at with `ps`. Say so in the feedback; it is the same lesson as Weeks 5 and 6.

---

*PROG 201 · Weeks 6–9 · Project 1 Marking Notes · Instructor Only · © CSE Department*
