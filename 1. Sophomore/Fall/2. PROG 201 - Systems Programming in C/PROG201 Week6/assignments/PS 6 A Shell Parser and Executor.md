# PROG 201 · Problem Set 6
## A Shell: Parser and Executor

---

**Released:** Week 6, Wednesday · **Due:** Week 7, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS6_{LastName}_{StudentID}.pdf`, and your code as `PS6_{LastName}.tar.gz`

> Collaboration: discussing approaches is fine. The write-up and the code must be yours.
>
> **This problem set is the first half of Project 1.** Project 1 (assigned this Friday, due Week 9)
> is a complete shell with job control; this is its parser, executor and builtins. **Write it so
> that you can build on it** — the job table and `tcsetpgrp` go on top of what you submit here, and
> a submission that hard-codes two pipeline stages will have to be rewritten rather than extended.
>
> **Job control is explicitly out of scope here.** No `jobs`, no `fg`, no `bg`, no `tcsetpgrp`, no
> `WUNTRACED`. Lab 6 is on the Monday of Week 7 and adds exactly those.
>
> Everything compiles clean under `gcc -Wall -Wextra -O2 -std=c11`. Warnings cost marks.

---

### The Shell

`tsh.c`, reading from a terminal or a pipe:

```
tsh> ls -l /etc | grep hosts | wc -l
tsh> sort < in.txt > out.txt
tsh> make 2> errors.log
tsh> cat huge.txt >> log.txt &
tsh> cd /tmp
tsh> exit
```

The grammar you must support, and no more:

```
pipeline := stage ( '|' stage )*  redirection*  '&'?
stage    := word+
redirection := ('<' | '>' | '>>' | '2>') word
```

---

### Q1: Tokenising and Parsing (26 points)

**(a) [10]** A tokeniser that splits on whitespace **and on operators**, longest operator first.

`ls>out` must produce three tokens, `ls >> out` must produce three, and `>>` must never become two `>`. Show a table of at least six inputs and their token lists, including three that have no spaces around an operator.

**(b) [10]** A parser producing a `struct cmd` with the stages, the three redirection targets, the append flag and the background flag.

**The redirections belong to the pipeline, not to a stage** (L19 §3). State in one sentence what that costs you — give a command a real shell accepts and yours will not.

**(c) [6]** **Write down what your parser rejects.** At least: an empty stage either side of a `|`, a redirection with no filename, `&` anywhere but last, and a line that is only operators.

Each must produce a message naming the problem and **must not fork anything**. Show the six error messages. A shell that forks and then discovers the syntax error has already changed the world.

---

### Q2: Executing (28 points)

**(a) [14]** A pipeline of *n* stages, *n* limited only by a constant you choose.

Requirements:

- **Every stage in one process group**, led by the first — `setpgid` in **both** the parent and the child (L20 §3). Say in your write-up why both.
- The parent closes every descriptor it hands to a child. **Demonstrate that the pipeline terminates**: `yes | head -1` must return to the prompt.
- `execvp` failing prints the command name and `strerror(errno)`, and the child exits **127**.
- The pipeline's exit status is the **last** stage's, and `$?` — or however you report it — shows `128 + signal` for a signalled child.

**(b) [8]** The four redirections. `>` truncates and `>>` appends; use the flag, not an `lseek` (Week 1 L05 §5), and say why in one sentence.

A failed `open` reports the filename and `strerror`, and the **child** exits 1 without exec'ing — the shell must not exit.

**(c) [6]** `&`. The shell prints something identifying the job and returns to the prompt immediately.

Then answer: **your background children are still in your process group unless you moved them.** Show what happens to a background job when you press Ctrl-C, with and without the `setpgid`, and say which is correct.

---

### Q3: Builtins (16 points)

**(a) [8]** `cd` and `exit`, both working, including `cd` with no argument.

Then the question: **`cd` cannot be an external program.** Explain why in two sentences, with reference to what `fork` gives a child.

**(b) [8]** Make `echo` a builtin as well. Time 5,000 `echo x` through your shell with it built in and with `/bin/echo`, and report both.

Compare your ratio with the lecture's measurements — an external command cost **955 µs** against under **5 µs** for a builtin, and of that 955 µs, `fork` was **127 µs** and the rest was `exec`. Say where your ratio differs and why it might.

---

### Q4: Getting It Wrong on Purpose (18 points)

Each part is a deliberate breakage. Make it, observe it, restore it, and explain.

**(a) [6]** Remove **one** `close` from the parent, in the pipeline loop. Run `ls | wc -l`.

Report which process hangs. Then, **without looking at your code**, diagnose it from outside with `ps -o pid,stat,wchan,cmd` and say which line of output identified the problem. (Week 1 L06 §4.)

**(b) [6]** Make the child's `execvp` failure call `exit` instead of `_exit`. Run `ls | nosuchcommand` and describe the output.

Explain it in terms of what `fork` duplicated — Week 0 L01 §6 measured this exact thing.

**(c) [6]** Remove the parent's `setpgid`, keeping the child's. Run a foreground command a hundred times in a loop, checking its process group each time.

Report how many were wrong. **If none were, say so** — then explain what the race is and why every real shell does it in both processes anyway.

---

### Q5: What It Is Not (12 points)

**(a) [4]** Your tokeniser does not handle quoting. Give the command `echo "hello world"` to your shell and to `bash` and show both outputs.

Then say what part of your program would have to change — and, in one sentence, why that is a change to the *tokeniser* rather than to the executor.

**(b) [4]** Add `;` to the grammar so that `a ; b` runs both.

What changed in `struct cmd`? Then say — you need not implement it — what would have to change again for `a && b`, and why that is a bigger change than `;` was.

**(c) [4]** Name three things `bash` expands after tokenising and before executing. For each, say whether it could be done as a pass over the token list or needs the parse tree, and why.

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

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

---

*PROG 201 · Week 6 · PS 6 · © CSE Department*
