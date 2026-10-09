# PROG 201 · Systems Programming in C
## Week 6 · Lecture 1 of 3
### The Shell's Read-Eval-Print Loop

*“A good system can't have a weak command language.”* — Alan Perlis, "Epigrams on Programming" (1982), #22

---

**Reading:** APUE §8.10, §9.1–9.3 · CS:APP §8.4 · TLPI Ch. 27 · `man 1 dash`, `man 3 execvp` · **Previous:** L18 · **Next:** L20 — process groups and the terminal

**Coursework:** 📊 **Quiz 6** today · 📝 **PS 6** released Wed this week, due Fri of Week 7 17:00 · 📋 **Project 1** released Fri this week, due Fri of Week 9 17:00 · 📝 **PS 5** due Fri this week 17:00 · 🔬 **Lab 5** Fri this week 16:00–17:50 · 🔬 **Lab 6** Mon of Week 7 15:00–16:50

---

## 1. You Have Already Written Most of a Shell

Every mechanism a shell needs, you have built:

| Week | What you built | Where the shell uses it |
| --- | --- | --- |
| 0 | `fork`, `exec`, `waitpid`, status words, signals | running a command, reporting how it ended |
| 1 | descriptors, `dup2`, the three tables | `<`, `>`, `>>`, `2>` |
| 2 | `pipe`, and the closes that make EOF arrive | `\|` |
| 5 | nothing — but the parsing habit | tokenising a line |

**Lab 1 was `ls | grep | wc` with no shell. This week is the shell around it.** What is new is not a system call; it is the *structure* — a loop, a parser, a job table, and one genuinely new idea, which is what happens when the user presses Ctrl-C (L20).

The loop, in full:

```
for (;;) {
    report anything that finished since last time
    print a prompt
    read a line
    tokenize it
    parse it into a command
    if it is a builtin, run it here
    otherwise fork, exec, and wait (or not, if it ends in &)
}
```

Everything else is detail. **The detail is where the term's work is**, and Project 1 is that detail.

---

## 2. Tokenising

A tokeniser turns `ls -l /etc | grep host > out` into a list of words and operators. The rules the shell uses are not the rules a C compiler uses, and the differences matter:

- **Whitespace separates words**, and any amount of it is one separator.
- **Operators separate words too**, without whitespace. `ls>out` is three tokens, and a tokeniser that splits only on spaces gets `ls>out` as one word and then cannot explain why the shell does something different.
- **The longest operator wins.** `>>` is one token, not two `>`; `2>` is one token. Check the two-character operators first.

The whole tokeniser, working, in twenty lines:

```c
static int tokenize(char *line, char *tok[], int max)
{
    int n = 0;
    char *p = line;
    while (*p && n < max - 1) {
        while (*p == ' ' || *p == '\t') p++;
        if (!*p) break;
        if (!strncmp(p, ">>", 2)) { tok[n++] = ">>"; p += 2; continue; }
        if (!strncmp(p, "2>", 2)) { tok[n++] = "2>"; p += 2; continue; }
        if (strchr("<>|&", *p)) { /* one-character operators */ ... p++; continue; }
        char *start = p;
        while (*p && !strchr(" \t<>|&", *p)) p++;
        if (*p) *p++ = 0;                      /* terminate the word in place */
        tok[n++] = start;
    }
    tok[n] = NULL;
    return n;
}
```

**It writes into the line.** Each word is terminated where it ends, so the tokens point into the buffer you read and nothing is allocated. That is how every small shell does it, and it means **you must keep the original line if you want to print it later** — a job table wants the command line, and by the time you have tokenised it, it is full of NULs.

What a real shell does that this does not: quoting (`"a b"` is one word), escapes (`a\ b`), variable expansion (`$HOME`), globbing (`*.c`), command substitution, `;`, `&&`, `||`, subshells. **Every one of those is a change to the tokeniser or a layer above it, and none is a change to the executor.** That separation is the reason to write the two parts separately.

---

## 3. Parsing Into a Command

A tokeniser gives you a flat list. The executor needs a structure, and for the language above it is small enough to write down:

```
pipeline := stage ( '|' stage )*  redirection*  '&'?
stage    := word+
```

which becomes:

```c
struct stage { char *argv[MAXARG]; int argc; };

struct cmd {
    struct stage stage[MAXSTAGE];
    int   nstage;
    char *infile, *outfile, *errfile;
    int   append;
    int   background;
};
```

**The redirections belong to the pipeline, not to the stage**, because `a | b > out` sends *b*'s output to the file and `a < in | b` reads *a*'s input from it. Put them in the `stage` and you will implement `>` on the wrong process and not understand why. (Real shells allow a redirection per stage; this grammar is the simplification worth starting from, and PS 6 asks you to say what it costs.)

Parsing is one pass over the token list with three cases — `|` starts a new stage, `&` sets a flag and must be last, a redirection operator consumes the next token as a filename — and everything else is a word appended to the current stage.

**Reject what you cannot run, at parse time, with a message.** `ls |`, `> out`, `ls > `, `& ls`: each is a syntax error, and a shell that discovers them after forking has already done something visible to the user. The list of things your parser rejects is a specification, and PS 6 asks you to write it down.

---

## 4. Builtins, and Why Some Commands Have To Be

Two reasons a command is built into the shell.

**Because it cannot work any other way.** `cd` changes the shell's current directory. A child cannot do that — Week 0 L01 §3: the working directory is per-process, and a child's `chdir` dies with the child. **This is not an optimisation; `/bin/cd` cannot exist.** The same is true of `exit`, `export`, `fg`, `bg`, `jobs`, and anything that touches the shell's own state.

**Because forking is expensive.** Measured, `cmdcost.c`:

| | per command |
| --- | --- |
| `fork` + `_exit` + `wait` | **127.1 µs** |
| `fork` + `exec /bin/true` + `wait` | **779.2 µs** |
| the same via `execlp` (PATH search) | 745.3 µs |
| `fork` + `exec /bin/sh -c exit` + `wait` | 919.2 µs |

And through the shell itself, 2,000 commands each way:

| | total | per command |
| --- | --- | --- |
| `cd /` (builtin) | under 10 ms | **under 5 µs** |
| `/bin/true` (external) | 1.91 s | **955 µs** |

**Two hundred times.** That is why `echo`, `test` and `[` are builtins in every shell despite `/bin/echo` existing, and it is why a shell script that loops a million times calling `expr` is slow in a way that has nothing to do with the shell being interpreted.

Notice also that `fork` is only 127 µs of the 779 µs. **The other 650 µs is `exec`**: reading the ELF header, mapping the segments, and running the dynamic linker. Take the linker out:

| | per command |
| --- | --- |
| a trivial **dynamically** linked binary | 679.3 µs |
| the same binary, **statically** linked | **532.4 µs** |

**147 µs, 22%, is the dynamic linker starting up** — and that is Week 8's subject arriving as a number.

---

## 5. Executing a Pipeline

This is Lab 1's program with a loop around it. The shape, per stage:

```c
for (int s = 0; s < c->nstage; s++) {
    int fd[2], last = (s == c->nstage - 1);
    if (!last) pipe(fd);

    pid_t k = fork();
    if (k == 0) {
        /* stdin: the file, or the previous pipe, or nothing */
        if (s == 0 && c->infile)      { open, dup2, close }
        else if (in != STDIN_FILENO)  { dup2(in, 0); close(in); }

        /* stdout: the file, or this pipe, or nothing */
        if (last && c->outfile)       { open, dup2, close }
        else if (!last)               { close(fd[0]); dup2(fd[1], 1); close(fd[1]); }

        execvp(argv[0], argv);
        fprintf(stderr, "tsh: %s: %s\n", argv[0], strerror(errno));
        _exit(127);
    }
    if (in != STDIN_FILENO) close(in);          /* the parent's copy */
    if (!last) { close(fd[1]); in = fd[0]; }
}
```

**Week 1 L06 §4's rule is the whole of the difficulty**: a pipe reports EOF when the last write-end descriptor *in every process* is closed. Miss one `close` in the parent and the reader never finishes, and the process that hangs is not the one with the bug.

Two shell-specific details Lab 1 did not have:

**`execvp` failing must report the command and exit 127.** `command not found` is 127 by convention, and the message must name what failed — a shell that says nothing when a command does not exist is unusable.

**The exit status of a pipeline is the exit status of the last stage.** `false | true` succeeds. That is POSIX, it surprises people, and `bash`'s `set -o pipefail` exists to change it.

---

## 6. Reporting How It Ended

Week 0 L02's status word, in its natural home:

```c
if (WIFEXITED(st))        status = WEXITSTATUS(st);
else if (WIFSIGNALED(st)) status = 128 + WTERMSIG(st);
else if (WIFSTOPPED(st))  /* the job stopped -- L21 */ ;
```

**`128 + signal` is where that convention comes from.** A shell has one byte to report a result in, `$?` is that byte, and a process killed by `SIGINT` (2) shows as 130. It is why `echo $?` after Ctrl-C prints 130, and why 137 means `SIGKILL` (128 + 9) — the number you will read in a container's logs when the OOM killer has been at it.

And the reason `WIFSTOPPED` is in that list at all is the subject of L21: a shell that only asks "did it exit?" cannot implement Ctrl-Z.

---

## 7. What This Shell Is Not

The shell you build this term is about 400 lines and runs real pipelines. What it leaves out, and why each is a different kind of work:

| Missing | Where it belongs |
| --- | --- |
| Quoting, escapes | the tokeniser — a state machine, not a `strchr` |
| `$VAR`, `$(cmd)` | between tokenising and parsing: **expansion**, a pass of its own |
| `*.c` globbing | expansion again. `glob(3)` does it for you |
| `;`, `&&`, `\|\|`, `()` | the **grammar** — the parse tree stops being a list |
| Functions, `if`, `while` | a real parser and an interpreter over the tree |
| A per-stage redirection | the grammar again (§3) |
| History, completion, editing | a line editor. `readline(3)`, and it is bigger than your shell |

**The order of that table is the order a shell actually grows in**, and the boundary worth noticing is between the first three rows and the rest: expansion is a *pipeline of passes over a flat token list*, and control flow is where you need a tree. `dash` is 15,000 lines and `bash` is 200,000, and the difference is almost entirely above this line.

---

## Summary

- A shell is `fork`, `exec`, `wait`, `dup2` and `pipe` — **all of which you already have** — with a loop, a parser and a job table around them.
- Tokenise on **whitespace and operators**, longest operator first, in place. **Keep a copy of the line** — the tokeniser destroys it.
- The grammar is `pipeline := stage ('|' stage)* redirection* '&'?`. **Redirections belong to the pipeline, not the stage.**
- Reject bad syntax **before** forking, and write down what you reject.
- `cd` is a builtin because it **cannot be anything else**; `echo` is one because an external command costs **955 µs against under 5 µs** — 200×.
- Of that 955 µs, `fork` is **127 µs** and `exec` is the rest; **147 µs of it is the dynamic linker**, which is Week 8.
- Pipeline execution is Lab 1 in a loop, and **the closes are still the hard part**.
- A pipeline's status is its **last** stage's; a signalled child reports as **128 + signal**.

---

## Exercises

1. Tokenise `a>b|c` and `a > b | c` with your tokeniser. Do they produce the same tokens? Should they?
2. Add `;` to the grammar. What changes in `struct cmd`, and what does that tell you about where `&&` would have to go?
3. Make `echo` a builtin. Time 10,000 `echo x` through your shell with and without it, and compare with §4's numbers.
4. Run `ls | head -1` on a large directory. What does `ls` do when `head` exits, and what is the pipeline's exit status? Now explain `set -o pipefail`.
5. Implement a per-stage redirection: `a > f1 | b > f2`. What did you have to move, and what does the shell now do with `a > f1 > f2`?
6. `strace -f -e trace=execve,clone your_shell` running `ls -l | wc -l`. Map every line to a line of §5.
7. Compare your shell's startup against `dash -c true` and `bash -c true`. Where does the difference go? *(Some of it is §4's last table.)*

---

*PROG 201 · Week 6 · L19 · © CSE Department*
