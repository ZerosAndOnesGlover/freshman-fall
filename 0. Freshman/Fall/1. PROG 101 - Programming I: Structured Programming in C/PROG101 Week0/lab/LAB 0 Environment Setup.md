# PROG 101 · Programming I: Structured Programming in C
## Week 0 · Lab 0: Environment Setup

**Not graded: completion required before Problem Set 0**
**Duration:** 2 hours
**Lab session:** Friday of Week 0 — the Week 0 orientation lab slot. From Lab 1 onward labs meet Monday.

---

## Overview

This lab gets your development environment working correctly. Every subsequent lab and assignment depends on this. Do not skip steps. If anything doesn't work, ask your TA before leaving.

You will:
1. Install and verify the C toolchain
2. Compile and run Hello World
3. Set up Git and create your course repository
4. Trace the compilation pipeline manually
5. Run your first GDB session

---

## Part 1: Install the Toolchain

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install build-essential gdb valgrind git
```

`build-essential` installs GCC, Make, and standard headers.

### macOS

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install GDB and Valgrind alternatives
brew install gcc gdb
# Note: Valgrind has limited macOS support. Use AddressSanitizer instead:
# gcc -fsanitize=address program.c
```

### Windows (WSL2 — Strongly Recommended)

```powershell
# In PowerShell (as Administrator):
wsl --install

# Restart, then open Ubuntu terminal and run:
sudo apt update && sudo apt install build-essential gdb valgrind git
```

### Verify Everything Works

```bash
gcc --version          # Should show GCC 11.x or later
gdb --version          # Should show GDB 12.x or later
make --version         # Should show GNU Make 4.x or later
git --version          # Should show git 2.x or later
valgrind --version     # Should show valgrind-3.x (Linux only)
```

If any command fails, resolve it before continuing. Ask your TA.

---

## Part 2: Hello World: Manual Pipeline

This exercise makes the compilation stages concrete. You will run each stage separately and inspect the output.

### Step 1: Write the source

Your coursework does not live in your home directory. It lives in the Academic Registry, next to
this course's answer sheets:

```
5. Academic Registry/4. Submissions/Year1 Freshman/Fall/1. PROG 101/
```

That path has spaces in it, so name it once. Add this to `~/.bashrc` — the registry's
[[4. Submissions/README|README]] carries the full block, covering every course:

```bash
export ACADEMICS=~/"Documents/1. Academics/0. Computer Science and Engineering (B.Sc)"
export PROG101="$ACADEMICS/5. Academic Registry/4. Submissions/Year1 Freshman/Fall/1. PROG 101"
```

Open a new terminal, make a directory for Week 0, and write the program:

```bash
mkdir -p "$PROG101/week0"
cd "$PROG101/week0"
```

**Quote `"$PROG101"` every time** — unquoted, the spaces in it split into five arguments and the
command fails.

Create `hello.c` with this exact content:

```c
/* hello.c — Week 0, Lab 0 */
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");
    printf("I am a C programmer.\n");
    return 0;
}
```

### Step 2: Run the preprocessor

```bash
gcc -E hello.c -o hello.i
wc -l hello.c           # How many lines is your source? - 8 lines
wc -l hello.i           # How many lines after preprocessing? - 821 lines
```

Open `hello.i` and scan through it. You'll see the contents of `stdio.h` at the top. Scroll to the end: your actual code is there.

**Checkpoint question (answer in your lab notebook):**
> What is the first line of YOUR code in `hello.i`? What line number is it at?    Line - 817

### Step 3: Run the compiler

```bash
gcc -S hello.i -o hello.s      # Or: gcc -S hello.c -o hello.s
cat hello.s
```

Read the assembly. Find the `main` label. Find the `call printf` (or similar).

**Checkpoint question:**
> What assembly instruction is generated for the `return 0;` statement?

### Step 4: Run the assembler

```bash
gcc -c hello.s -o hello.o      # Or: gcc -c hello.c -o hello.o
file hello.o                    # Show what kind of file this is
ls -la hello.o                  # How big is it?
nm hello.o                      # Show symbol table
```

`nm` shows the symbol table. Look for:
- `T main` — the `T` means the symbol is defined in the text (code) section
- `U printf` — the `U` means the symbol is *undefined* (used but not defined here — the linker will find it)

**Checkpoint question:**
> What does the `U` before `printf` mean? Why is it U and not T?

### Step 5: Link

```bash
gcc hello.o -o hello
./hello                # Run your program
echo $?                # Print exit code — should be 0
```

### Step 6: Full pipeline in one command

```bash
gcc -Wall -Wextra -g -std=c11 -o hello_full hello.c
./hello_full
```

Both produce the same output. Now you understand what that single command actually does.

---

## Part 3: Explore Assembly

Compile your program and view the compiler's assembly output:

```bash
gcc -S -O0 -fverbose-asm hello.c -o hello_O0.s   # No optimization
gcc -S -O2 -fverbose-asm hello.c -o hello_O2.s   # Optimized

diff hello_O0.s hello_O2.s    # Compare them
```

`-fverbose-asm` adds comments explaining what each assembly instruction came from.

**Checkpoint question:**
> List two differences you observe between the `-O0` and `-O2` assembly. What do you think the optimizer changed and why?

---

## Part 4: Your First Makefile

Create `Makefile` in `$PROG101/week0/` (remember: TAB indentation, not spaces):

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

all: hello temperature

hello: hello.c
	$(CC) $(CFLAGS) -o $@ $<

temperature: temperature.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f hello temperature *.o *.i *.s

.PHONY: all clean
```

Test it:
```bash
make                # Build everything
./hello             # Run hello
make clean          # Remove compiled files
make hello          # Build only hello
touch hello.c       # Update timestamp of hello.c
make                # Notice: only hello is recompiled
```

**Checkpoint question:**
> Run `make` twice without changing any file. What does Make print the second time? Why?

---

## Part 5: Write temperature.c

Create `temperature.c` — a Celsius to Fahrenheit converter:

```c
/* temperature.c — temperature converter */
#include <stdio.h>

double celsius_to_fahrenheit(double celsius);

int main(void) {
    double c;

    printf("Enter temperature in Celsius: ");
    if (scanf("%lf", &c) != 1) {
        fprintf(stderr, "Error: invalid input\n");
        return 1;
    }

    printf("%.1f°C = %.1f°F\n", c, celsius_to_fahrenheit(c));
    return 0;
}

double celsius_to_fahrenheit(double celsius) {
    return (celsius * 9.0 / 5.0) + 32.0;
}
```

Compile and test:
```bash
make temperature
echo "100" | ./temperature     # Should print 100.0°C = 212.0°F
echo "0"   | ./temperature     # Should print 0.0°C = 32.0°F
echo "-40" | ./temperature     # Should print -40.0°C = -40.0°F
```

---

## Part 6: Your First GDB Session

We will intentionally introduce a bug and debug it with GDB.

Create `buggy.c`:

```c
/* buggy.c — intentionally buggy program */
#include <stdio.h>

int sum_array(int arr[], int n);

int main(void) {
    int numbers[] = {10, 20, 30, 40, 50};
    int total;

    /* BUG: n should be 5, not 6 — off by one */
    total = sum_array(numbers, 6);

    printf("Sum: %d\n", total);
    return 0;
}

int sum_array(int arr[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}
```

Compile with debug symbols and AddressSanitizer:
```bash
gcc -Wall -g -fsanitize=address -std=c11 -o buggy buggy.c
./buggy
```

AddressSanitizer will detect the out-of-bounds read and print an error report.

Now debug with GDB:
```bash
gcc -Wall -g -std=c11 -o buggy buggy.c     # Without sanitizer for GDB
gdb ./buggy
```

In GDB:
```
(gdb) break main
(gdb) run
(gdb) next                    # Step to sum_array call
(gdb) step                    # Step into sum_array
(gdb) print n                 # What is n?
(gdb) print arr[4]            # Last valid element
(gdb) print arr[5]            # Out-of-bounds read — what do you see?
(gdb) continue
(gdb) quit
```

Fix the bug (change `6` to `5`), recompile, and verify.

**Checkpoint question:**
> What was the value of `arr[5]`? Is it consistent between runs? What does this tell you about uninitialized memory?
> Yes, 5 was consistent between runs, it was a garbage value:

``` gdb
(gdb) print arr[5]
$8 = 32767
(gdb) print arr[5]
$9 = 32767
(gdb) print arr[5]
$10 = 32767
```

---

## Part 7: Set Up Git Repository

`$PROG101` is its own repository with its own remote, kept deliberately out of the vault's git repo
— so PROG 101 gets committed from inside `$PROG101`, never from the vault root. Every course you
take gets its own repo the same way.

```bash
cd "$PROG101"
git init
git config user.name "Your Name"
git config user.email "your.email@university.edu"

# Create .gitignore
cat > .gitignore << 'EOF'
# Compiled binaries
a.out
*.o
hello
temperature
buggy

# Build artifacts
*.i
*.s

# Editor files
.DS_Store
*.swp
*~
EOF

# Add and commit
git add .
git commit -m "Week 0: initial setup — hello world, temperature, buggy"
git log --oneline
```

---

## Part 8: Exploration Challenges

These are optional but highly recommended. They deepen your understanding.

**Challenge 1:** What happens when you try to compile a C++ file with the C compiler?
```bash
# Create test.cpp with a C++ specific feature (like 'class')
echo 'class Foo {}; int main() { return 0; }' > test.cpp
gcc test.cpp       # What error do you get?
g++ test.cpp       # Try the C++ compiler
```

**Challenge 2:** Inspect a compiled binary:
```bash
gcc -o hello hello.c
file hello                    # What type of file?
strings hello                 # Find human-readable strings inside the binary
hexdump -C hello | head -30   # View raw bytes
readelf -h hello              # ELF header
```

**Challenge 3:** Find printf in the C library:
```bash
nm -D /lib/x86_64-linux-gnu/libc.so.6 | grep " printf"
# Or on macOS:
nm /usr/lib/libc.dylib | grep printf
```

---

## Lab Deliverables

By end of lab, you should have:

- [x] All tools installed and verified (`gcc`, `gdb`, `make`, `git`)
- [x] `hello.c` compiles and runs correctly
- [x] `temperature.c` passes all three test cases
- [x] `buggy.c` bug found, fixed, and documented with a comment
- [x] `Makefile` working (builds and cleans)
- [x] Git repository initialized with first commit
- [x] Answers to all Checkpoint Questions in your lab notebook

**Show your TA:** Run `make clean && make && ./hello && ./temperature <<< "100"` and show the output.

---

## Lab Notebook

Write your answers to checkpoint questions here (or in a separate `LAB 0 Environment Setup.md`):

1. First line of YOUR code in `hello.i`: ___
2. Assembly instruction for `return 0;`: ___
3. Meaning of `U` before `printf` in `nm` output: ___
4. Two differences between `-O0` and `-O2` assembly: ___
5. What Make prints on second run (and why): ___
6. Value of `arr[5]` in GDB, and what it means: ___
