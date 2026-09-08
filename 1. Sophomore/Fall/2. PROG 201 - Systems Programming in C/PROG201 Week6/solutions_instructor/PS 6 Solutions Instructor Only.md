# PROG 201 · PS 6 Solutions
## A Shell: Parser and Executor — Instructor Only

---

**Do not distribute.** Q4 is three deliberate breakages and the answers are the marks.

**Machine these numbers came from:** Linux 7.0.0-30-generic, gcc 13.3.0 (Ubuntu 24.04), Intel i5-8250U.

**On scope:** the curriculum lists both "PS 6: implement a shell (tsh)" and "Project 1: Unix shell (tsh)". They are the same program, so the build splits them: **PS 6 is the parser, executor and builtins; Project 1 adds job control and everything else.** Students are told to write PS 6 so that Project 1 can build on it, and Project 1 says explicitly that reusing their own PS 6 is expected. [[PROG 201 Scheduling Notes]] §13 records the decision.

**Do not accept job control here.** A submission with a working `fg` is not penalised, but it is not marked either — the marks are all in the parser and the executor, and a student who spent the week on job control has probably done Q1 and Q2 thinly.

---

## Reference Fragments

**The tokeniser — Q1(a):**

```c
while (*p && n < max - 1) {
    while (*p == ' ' || *p == '\t') p++;
    if (!*p) break;
    if (!strncmp(p, ">>", 2)) { tok[n++] = ">>"; p += 2; continue; }   /* longest first */
    if (!strncmp(p, "2>", 2)) { tok[n++] = "2>"; p += 2; continue; }
    if (strchr("<>|&", *p))   { tok[n++] = one_char_op(*p); p++; continue; }
    char *start = p;
    while (*p && !strchr(" \t<>|&", *p)) p++;
    if (*p) *p++ = 0;
    tok[n++] = start;
}
```

**The pipeline loop — Q2(a):** unchanged from L19 §5.

**The double `setpgid` — Q2(a):**

```c
if (k == 0) { setpgid(0, pgid); ... execvp(...); }
setpgid(k, pgid);                      /* and again in the parent */
```

---

## Q1 — Tokenising and Parsing (26)

**(a) [10]** The table **[4]**, longest-operator-first **[3]**, operators splitting words with no whitespace **[3]**.

Reference table, and the three no-space rows are the ones to check:

| input | tokens |
| --- | --- |
| `ls -l /etc` | `ls` `-l` `/etc` |
| `ls > out` | `ls` `>` `out` |
| **`ls>out`** | `ls` `>` `out` |
| **`ls>>out`** | `ls` `>>` `out` |
| **`a\|b\|c`** | `a` `\|` `b` `\|` `c` |
| `make 2> err &` | `make` `2>` `err` `&` |

The classic failure is checking `>` before `>>`, which turns `>>out` into `>`, `>`, `out` and then a parse error about a missing filename. **Ask to see `ls>>out`** — it is the one-line test.

**(b) [10]** A `struct cmd` with stages, three targets, append and background **[7]**; the ownership sentence **[3]**.

The cost of pipeline-level redirection: **`a > f1 | b > f2`** is accepted by every real shell and rejected (or silently mishandled) here — with one `outfile` field there is nowhere to put `f1`. Accept any correct example. A student who says "no cost, I put them in the stage" has done Project 1's extension early and should get the marks plus a note.

**(c) [6]** Six messages, one mark each, **and none of them may fork**.

Test it: `strace -f -e trace=clone,execve ./tsh <<< 'ls |'` must show no `clone`. A student whose parser is inside the execution loop will fail this and should be shown the trace rather than told.

---

## Q2 — Executing (28)

**(a) [14]** *n* stages **[4]**, one process group with `setpgid` in both **[4]**, all closes correct **[3]**, `execvp` failure reporting and 127 **[2]**, last-stage status and `128 + signal` **[1]**.

**`yes | head -1` returning to the prompt is the test that matters** and it fails for two different reasons: a missing `close` in the parent (the pipeline hangs) or an unhandled `SIGPIPE` in the shell (the shell dies when `head` exits). Run it before reading the code.

The "why both `setpgid`" answer: **it is a race** — whichever process runs first makes it true, the parent's call may fail with `EACCES` if the child already `exec`ed, and the child's may not have happened when the parent wants to `tcsetpgrp`. Full marks need both directions.

**(b) [8]** Four redirections **[5]**, `O_APPEND` rather than `lseek` with the reason **[2]**, failure handling in the child **[1]**.

The `O_APPEND` reason is Week 1 L05 §5: **`lseek`-then-`write` is two system calls and another process can append between them** — measured then at 4,396 lines of 80,000 surviving. A student who says "it's simpler" gets [1] of the [2].

**(c) [6]** `&` working **[2]**, the demonstration **[2]**, the correct answer **[2]**.

Without the `setpgid`, a background job is in the shell's process group, so **Ctrl-C kills it too** — which is not what `&` means. With it, Ctrl-C reaches only the foreground group. **The `setpgid` version is correct**, and the demonstration is `sleep 100 &` then Ctrl-C then `ps`.

---

## Q3 — Builtins (16)

**(a) [8]** Both working **[5]**, the explanation **[3]**.

The explanation: **the working directory is per-process** (Week 0 L01 §3). `fork` gives the child a *copy*, so a child's `chdir` changes the child's directory and dies with it. There is no mechanism by which a child can change its parent's — which is why `/bin/cd` does not and cannot exist, while `/bin/echo` does.

Watch for "because it's faster", which is the answer to the *other* half of the question.

**(b) [8]** The measurement **[4]**, the comparison **[4]**.

Reference, through the shell, 2,000 commands each:

| | total | per command |
| --- | --- | --- |
| builtin | under 10 ms | **under 5 µs** |
| `/bin/true` | 1.91 s | **955 µs** |

and the breakdown from `cmdcost.c`:

| | µs |
| --- | --- |
| `fork` + `_exit` + `wait` | 127.1 |
| `fork` + `exec /bin/true` + `wait` | 779.2 |
| a trivial **dynamic** binary | 679.3 |
| the same, **static** | **532.4** |

Any ratio between about 100× and 300× is fine. **The mark is for the explanation of a difference**, and the two legitimate ones are: a slower disk or cold cache raises the exec cost, and a shell that does more per builtin (history, expansion) raises the builtin cost. A student who reports 5× has almost certainly timed the shell's startup rather than the loop — ask how many commands they ran.

---

## Q4 — Getting It Wrong on Purpose (18)

**(a) [6]** Which process hangs **[2]**, the outside diagnosis **[4]**.

**The reader hangs, not the process with the bug.** With `ls | wc -l` and the parent keeping the write end, `wc` never sees EOF. The identifying line:

```
  PID STAT WCHAN      CMD
12345 S    pipe_read  wc -l
```

**`wchan` is the mark.** A student who says "I saw it hang and added the close back" has not answered the question; the point is that `ps` named the kernel function.

**(b) [6]** The observation **[2]**, the explanation **[4]**.

With `exit` instead of `_exit`, the child flushes **the stdio buffers it inherited from the shell**, so any output the shell had buffered but not written is printed **again** by the child. With the shell's stdout on a pipe (fully buffered), the duplication is visible; on a terminal (line buffered) it usually is not.

Week 0 L01 §6 measured exactly this: **one `x` on a pty, eight through a pipe**. Full marks require naming the inherited buffer, not just "exit flushes things".

**(c) [6]** The report **[2]**, the race **[4]**.

**"None were wrong" is the expected result** and is worth full marks with the explanation — the window is tiny and the parent almost always wins on an idle machine. The explanation is the same as Q2(a)'s, and a student who cross-references their own earlier answer should be told that is the right instinct.

---

## Q5 — What It Is Not (12)

**(a) [4]** Both outputs **[2]**, the tokeniser answer **[2]**.

`bash` prints `hello world`; the teaching shell prints `"hello world"` — quotes and all, as two arguments. The change is a **state machine in the tokeniser**: inside quotes, whitespace and operators stop being separators. It is not an executor change because the executor never sees quotes either way — it gets an `argv`, and the question is only how the words were cut.

**(b) [4]** `;` implemented or described **[2]**, the `&&` answer **[2]**.

`;` needs a **list of `struct cmd`** rather than one — the structure stays flat. `&&` needs the exit status of the left side to decide whether to run the right, so the structure becomes a **tree with an operator at each node**, and execution becomes a recursive walk rather than a loop. **That is the bigger change**, and it is where a shell stops being a parser and starts being an interpreter.

**(c) [4]** Any three of: `$VAR`, `$(cmd)`, `*.c` globbing, `~`, `{a,b}` brace expansion, arithmetic `$((...))`.

The pass/tree distinction: **all of the expansions are passes over a flat token list** — they replace tokens with other tokens, in a defined order (`man bash`, "EXPANSION", lists seven). **None of them needs the tree.** A student who realises that the whole of expansion sits between tokenising and parsing, and that only control flow needs a tree, has the point of the question.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Tokenising and parsing | 26 |
| 2 | Executing | 28 |
| 3 | Builtins | 16 |
| 4 | Getting it wrong on purpose | 18 |
| 5 | What it is not | 12 |
| | **Total** | **100** |

---

*PROG 201 · Week 6 · PS 6 Solutions · Instructor Only · © CSE Department*
