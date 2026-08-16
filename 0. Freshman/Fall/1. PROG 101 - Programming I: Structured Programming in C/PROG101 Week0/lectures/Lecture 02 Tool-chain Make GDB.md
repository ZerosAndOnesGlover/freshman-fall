# PROG 101 · Programming I - Structured Programming in C
## Week 0 · Lecture 2: The Command Line, Make, and GDB

**Date:** Wednesday 19 August 2026 · 10:00–10:50 · Week 0

---

## Lecture Goals

By the end of this lecture you will:
- Navigate the filesystem and manipulate files from the terminal
- Compile C programs with GCC using meaningful flags
- Write a basic `Makefile` to automate your builds
- Start, step through, and inspect a running program with GDB

---

## 1. The Command Line is Your Primary Tool

A great engineer is *fluent* in the command line: not merely functional. The terminal gives you direct access to the OS, composable tools, and automation. Every professional development environment begins here.

This lecture is a tool orientation. You will use these tools every day for the rest of this course.

---

## 2. Essential Shell Commands

### Navigation

```bash
pwd                   # Print Working Directory — where am I?
ls                    # List files in current directory
ls -a                 # all, show hidden files (. refers to the current directory, .. refers to the parent directory)
ls -l                 # long, show detailed information (drwxr-xr-x 3 adebayo users 4096 Jun 26 18:00 projects)
ls -t                 # time, sort by time
cd /path/to/dir       # Change directory
cd ..                 # Go up one level (the parent directory)
cd ~                  # Go to home directory
cd -                  # Go back to previous directory
```

### File Operations

```bash
mkdir prog101         # Make directory
mkdir -p a/b/c        # Make nested directories
touch hello.c         # Create empty file (or update timestamp)
cp source dest        # Copy file
cp -r src/ dst/       # Copy directory recursively
mv old new            # Move/rename file
rm file.c             # Remove file (PERMANENT — no trash)
rm -rf dir/           # Remove directory recursively (dangerous, powerful)
```

### Reading Files

```bash
cat file.c            # Print entire file
less file.c           # Scrollable viewer (q to quit, /term to search)
head -20 file.c       # First 20 lines
tail -20 file.c       # Last 20 lines
wc -l file.c          # Count lines
grep "malloc" file.c  # Find lines containing "malloc"
```

### Piping and Redirection

```bash
# The pipe | sends stdout of one command to stdin of another
ls -la | grep ".c"         # List only .c files
cat file.c | wc -l         # Count lines in file

# Redirection
gcc -E hello.c > hello.i   # Write stdout to file
gcc 2> errors.txt          # Write stderr to file
gcc hello.c > out.txt 2>&1 # Write both stdout and stderr to same file
```

### Useful Shortcuts

```bash
Ctrl+C    # Kill running process
Ctrl+Z    # Suspend process (to background)
Ctrl+L    # Clear terminal
Ctrl+R    # Reverse search through command history
Tab       # Autocomplete filenames and commands
↑ ↓       # Navigate command history
!!        # Repeat last command
!gcc      # Repeat last command starting with 'gcc'
```

---

## 3. GCC: The Compiler Driver

`gcc` is not just a compiler: it is a **compiler driver** that runs the full toolchain (preprocessor → compiler → assembler → linker). The flags you pass control which stages run and how.

### Essential Flags

```bash
gcc hello.c                      # Compile + link → produces a.out
gcc hello.c -o hello             # Name the output 'hello'
gcc -o hello hello.c             # Same (-o can go anywhere)

# Compilation stages
gcc -E hello.c -o hello.i        # Preprocessor only (-E means "Expand")
gcc -S hello.i -o hello.s        # Compiler to assembly, (-S  "Assembly Source")
gcc -S hello.c -o hello.s        # Preprocessor + compiler (→ assembly)
gcc -c hello.s -o hello.o        # Assembler to machine code (0s and 1s) (-c means compiler)
gcc -c hello.c -o hello.o        # Preprocessor + compiler + assembler (→ object)
gcc hello.o -o hello             # Linker only

# Warnings (USE THESE ALWAYS)
gcc -Wall hello.c                # Enable most important warnings
gcc -Wextra hello.c              # Enable extra warnings
gcc -Wall -Wextra -Werror hello.c  # Treat warnings as errors (recommended)

# Debugging (USE DURING DEVELOPMENT)
gcc -g hello.c                   # Include debug symbols (required for GDB)
gcc -g3 hello.c                  # Maximum debug info

# Optimization (USE FOR PERFORMANCE TESTING)
gcc -O0 hello.c                  # No optimization (default, fastest compile)
gcc -O1 hello.c                  # Basic optimization
gcc -O2 hello.c                  # Standard optimization (production default)
gcc -O3 hello.c                  # Aggressive optimization

# Security/Safety (USE DURING DEVELOPMENT)
gcc -fsanitize=address hello.c   # AddressSanitizer: detects memory errors
gcc -fsanitize=undefined hello.c # UBSan: detects undefined behavior

# Combine common development flags:
gcc -Wall -Wextra -g -fsanitize=address,undefined hello.c -o hello
```

### Your Standard Development Command

During this course, compile with:
```bash
gcc -Wall -Wextra -Werror -g -std=c11 -o program program.c
```

- `-Wall -Wextra -Werror`: catch all warnings, treat as errors
- `-g`: debug symbols for GDB
- `-std=c11`: use the C11 standard (modern C)

---

## 4. Make: Build Automation

As soon as your project has more than one file, manual compilation becomes tedious. `make` automates builds by tracking dependencies, it only recompiles files that have changed.

### The Makefile

Create a file named exactly `Makefile` (capital M, no extension):

```makefile
# Variables
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

# Default target (runs when you type 'make')
hello: hello.o
	$(CC) $(CFLAGS) -o hello hello.o

# Compile source to object file
hello.o: hello.c
	$(CC) $(CFLAGS) -c hello.c -o hello.o

# Remove compiled files
clean:
	rm -f hello hello.o

# Declare non-file targets
.PHONY: clean
```

**CRITICAL:** The indentation before commands *must* be a **TAB character**, not spaces. This is a famous Make gotcha.

### Makefile Syntax

```makefile
target: dependency1 dependency2
[TAB]command to build target
```

Make reads: "To build `target`, first ensure `dependency1` and `dependency2` exist and are up to date. Then run the command."

### Running Make

```bash
make              # Build default target
make hello        # Build specific target
make clean        # Run the clean target
make -n           # Dry run: show what would happen without doing it
make -B           # Force rebuild everything
```

### A More Complete Makefile for This Course

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11
SANITIZE = -fsanitize=address,undefined

# Build all programs
all: hello calculator

# Individual targets
hello: hello.c
	$(CC) $(CFLAGS) $(SANITIZE) -o $@ $<

calculator: calculator.c
	$(CC) $(CFLAGS) $(SANITIZE) -o $@ $<

clean:
	rm -f hello calculator *.o

.PHONY: all clean
```

Special variables:
- `$@` = the target name
- `$<` = the first dependency
- `$^` = all dependencies

---

## 5. GDB: The GNU Debugger

GDB lets you pause your running program, inspect variables, step through code line by line, and examine memory. It is the single most powerful debugging tool you have.

**Prerequisite:** You must compile with `-g` to include debug symbols.

### Starting GDB

```bash
gcc -g -o hello hello.c     # Compile with debug symbols
gdb ./hello                  # Start GDB with your program
```

### The GDB Commands You Will Use Every Day

```
# Running
run                          # Start the program
run arg1 arg2               # Start with command-line arguments
quit                         # Exit GDB (or Ctrl+D)

# Breakpoints — pause execution at a location
break main                   # Break at start of main()
break hello.c:15             # Break at line 15 of hello.c
break add                    # Break at start of function 'add'
info breakpoints             # List all breakpoints
delete 1                     # Delete breakpoint #1
disable 2                    # Disable breakpoint #2
enable 2                     # Re-enable breakpoint #2

# Stepping — move through code
next    (n)                  # Execute next line (step OVER function calls)
step    (s)                  # Execute next line (step INTO function calls)
continue (c)                 # Resume until next breakpoint or end
finish                       # Run until current function returns

# Inspection — see what's happening
print x                      # Print value of variable x
print *ptr                   # Print value pointed to by ptr
print arr[0]                 # Print array element
print sizeof(x)              # Print sizeof
display x                    # Print x after every step
info locals                  # Print all local variables
info args                    # Print function arguments
backtrace  (bt)              # Print call stack (where am I?)
frame 2                      # Switch to stack frame #2

# Memory examination
x/10d ptr                   # Print 10 decimal integers starting at ptr
x/10x ptr                   # Print 10 hex values
x/s str                     # Print string at address str
x/i $rip                    # Print current assembly instruction

# Source display
list                         # Show source around current line
list main                    # Show source of function main
list 10,20                   # Show lines 10-20
```

### GDB Workflow Example

```bash
$ gcc -g -o buggy buggy.c
$ gdb ./buggy
(gdb) break main
Breakpoint 1 at 0x4005f6: file buggy.c, line 5.
(gdb) run
Starting program: ./buggy
Breakpoint 1, main () at buggy.c:5
5         int x = 10;
(gdb) next
6         int y = 0;
(gdb) next
7         int result = divide(x, y);
(gdb) step          # step INTO divide()
divide (a=10, b=0) at buggy.c:12
12        return a / b;
(gdb) print a
$1 = 10
(gdb) print b
$2 = 0              # AH HA — b is 0, we're about to divide by zero
(gdb) backtrace
#0  divide (a=10, b=0) at buggy.c:12
#1  0x400612 in main () at buggy.c:7
(gdb) quit
```

### GDB TUI Mode (Graphical Terminal)

```bash
gdb -tui ./hello    # Start in TUI mode
# Or press Ctrl+X Ctrl+A to toggle TUI in GDB
```

TUI shows your source code and the debugger prompt simultaneously — much easier to follow.

---

## 6. Git: Version Control

You must use Git for all assignments. Version control is not optional in professional engineering.

```bash
# First-time setup (do once)
git config --global user.name "Your Name"
git config --global user.email "you@email.com"

# Starting a repository
git init                     # Initialize new repo in current directory
git clone <url>              # Clone existing repo

# Daily workflow
git status                   # What has changed?
git diff                     # Show exact changes
git add hello.c              # Stage a file for commit
git add .                    # Stage all changed files
git commit -m "Add hello world program"   # Commit with message
git log                      # View commit history
git log --oneline            # Compact history

# Undoing
git checkout -- hello.c      # Discard unstaged changes to hello.c
git reset HEAD hello.c       # Unstage a file
git diff HEAD~1              # Compare with previous commit
```

### Your `.gitignore`

Create `.gitignore` in your repo root to tell Git to ignore compiled files:

```
# Compiled binaries
a.out
*.o
*.out

# Executables (no extension on Linux/Mac)
hello
calculator

# Editor files
.DS_Store
*.swp
*~
```

---

## 7. Your Development Setup Checklist

By end of Lab 0, you should have:

- [x] A Linux terminal (native Linux, WSL2 on Windows, or macOS Terminal)
- [x] GCC installed and working: `gcc --version`
- [x] GDB installed: `gdb --version`
- [x] Make installed: `make --version`
- [x] Valgrind installed (Linux only): `valgrind --version`
- [x] VS Code or your preferred editor with C syntax highlighting
- [x] Git configured with your name and email
- [x] A Git repository for this course created and cloned

---

## 8. The Programmer's Mindset

Here is something no tool tutorial will tell you: **the terminal is not about memorizing commands**. It is about understanding that:

1. **Everything is a file** (or a process). Every device, pipe, socket, and directory is accessed through the file interface.
2. **Tools compose**. Small programs that do one thing well can be piped together to do complex things.
3. **Text is the universal interface**. Programs communicate through text streams, which means any program can talk to any other program.

These are not Linux trivia: they are design principles that show up in network protocols, API design, and operating system internals. The command line is where you first encounter them.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Given this Makefile, state exactly which commands run for each scenario.

```make
CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -g

prog: main.o utils.o
\t$(CC) main.o utils.o -o prog

main.o: main.c utils.h
\t$(CC) $(CFLAGS) -c main.c

utils.o: utils.c utils.h
\t$(CC) $(CFLAGS) -c utils.c
```

(a) First build. (b) Edit `utils.c`, run `make`. (c) Edit `utils.h`, run `make`. (d) Run `make` again immediately.

**2. (Explain.)** You compile with `gcc -Wall -Wextra -std=c11 prog.c -o prog` and it runs but crashes. Describe the precise GDB session you would run to locate the fault, naming each command and what it tells you.

**3. (Build.)** Rewrite the Makefile above using automatic variables and a pattern rule, so adding a new `.c` file needs no new rule. Explain `$@`, `$<`, and `$^`.

**4. (Stretch.)** `gcc -Wall -Wextra` is standard practice. Name three additional flags worth enabling on a student project, say what each catches, and explain why `-Werror` is both recommended and occasionally a problem.


### Answers

**1.** **(a)** All three: compile `main.c`, compile `utils.c`, then link.

**(b)** `gcc … -c utils.c` then the link. `main.o` is untouched because `main.c` and `utils.h` are both older than `main.o`.

**(c)** **All three again.** Both object files list `utils.h` as a prerequisite, so both are now out of date. This is why headers must appear in the dependency lists — omit `utils.h` and editing a struct definition would leave `main.o` compiled against the *old* layout while `utils.o` uses the new one. The program links successfully and then behaves incomprehensibly, which is far worse than a compile error.

**(d)** `make: 'prog' is up to date.` Nothing runs.

The whole model is **timestamp comparison**: a target is rebuilt if any prerequisite is newer than it. Note the recipe lines must begin with a real **tab**, not spaces — the resulting `Makefile:5: *** missing separator` is the most common first Make error, and editors that expand tabs cause it silently.

**2.** First, **recompile with `-g`** — without debug symbols GDB can show addresses but not source lines:

```bash
gcc -Wall -Wextra -std=c11 -g prog.c -o prog
gdb ./prog
```

Then:

| Command | What it gives you |
|---|---|
| `run` | Executes until the crash. GDB prints the signal (`SIGSEGV`) and the line it died on |
| `backtrace` (`bt`) | The full call stack — *how* execution reached that line. Usually the single most informative command |
| `frame 1` | Move up to the caller, to inspect its locals |
| `print var` | Value of any variable in the selected frame. `print *ptr` dereferences; if it prints `Cannot access memory at address 0x0`, you have found a NULL dereference |
| `info locals` | Every local in the frame at once |
| `list` | Source around the current line |

For a fault you cannot reach directly, set a breakpoint before it — `break utils.c:42`, then `run`, then step with `next` (over calls) or `step` (into them), and `continue` to the next hit. `watch total` stops whenever a variable changes, which is how you find *who* corrupted a value rather than where it was read.

The habit worth forming: **`bt` first, always.** The crash line tells you where the program died; the backtrace tells you why it was there, and the bug is usually in a caller.

**3.**

```make
CC      = gcc
CFLAGS  = -Wall -Wextra -std=c11 -g
OBJS    = main.o utils.o

prog: $(OBJS)
\t$(CC) $^ -o $@

%.o: %.c
\t$(CC) $(CFLAGS) -c $< -o $@

$(OBJS): utils.h

.PHONY: clean
clean:
\trm -f $(OBJS) prog
```

The automatic variables:

- **`$@`** — the **target** being built (`prog`, or `main.o`).
- **`$<`** — the **first prerequisite** (`main.c`). Used in compile rules, where you want exactly the source file.
- **`$^`** — **all prerequisites**, space-separated and de-duplicated (`main.o utils.o`). Used in the link rule.

`%.o: %.c` is a **pattern rule**: it teaches Make how to build any `.o` from the matching `.c`, so adding `parser.c` needs only `parser.o` appended to `OBJS`.

The bare line `$(OBJS): utils.h` adds a prerequisite to existing rules without giving a recipe — the pattern rule still supplies the commands. For real projects, generate header dependencies automatically with `gcc -MMD -MP` and `-include $(OBJS:.o=.d)`, since maintaining them by hand does not scale.

`.PHONY` marks `clean` as a command rather than a file, so it still runs if a file named `clean` happens to exist.

**4.** **`-fsanitize=address`** (ASan) — instruments the binary to detect buffer overflows, use-after-free, and double-free **at the moment they happen**, with a full stack trace, rather than letting them corrupt memory silently. It costs about 2× runtime and is the single highest-value flag in this course. Pair with `-fsanitize=undefined` for signed overflow, bad shifts, and misaligned access.

**`-g`** — debug symbols, so GDB and sanitiser reports name source lines instead of hex addresses. Costs nothing at runtime.

**`-std=c11 -pedantic`** — rejects GCC extensions, so your code stays portable and you learn what is actually standard C rather than what happens to work on this compiler.

Also worth knowing: `-Wshadow` (a local hiding an outer variable), `-Wconversion` (implicit narrowing), and `-O2`, which enables warnings that depend on dataflow analysis and therefore catches uninitialised reads that `-O0` misses.

**`-Werror`** turns every warning into an error. It is recommended because warnings that are merely printed get scrolled past and accumulate until nobody reads any of them; making them fatal keeps the count at zero. It is occasionally a problem because warnings vary between compiler *versions* — code that builds cleanly on GCC 13 may emit a new warning on GCC 15 and fail to build at all. The usual resolution is `-Werror` in development and CI, but not in release builds that other people compile.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Shell** | The program that interprets your command-line input (bash, zsh) |
| **stdin/stdout/stderr** | Standard input, output, and error streams (file descriptors 0, 1, 2) |
| **Pipe** | Connects stdout of one process to stdin of another |
| **Makefile** | Configuration file that describes how to build a project |
| **Debug symbol** | Mapping from machine code addresses to source line numbers (added by `-g`) |
| **Breakpoint** | A pause point in your program where GDB stops execution |
| **Call stack** | The sequence of function calls that led to the current point |
| **Stack frame** | The memory region holding one function call's local variables and return address |

---

*Next: Lecture 3 — [[Lecture 03 Hello World Deep-Dive]]*
