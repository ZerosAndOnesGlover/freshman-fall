# PROG 101 · C Quick Reference Card
## Week 0 Edition

Keep this open while coding. It grows with you each week.

---

## Compilation Commands

```bash
# Standard development compilation (use this always)
gcc -Wall -Wextra -Werror -g -std=c11 -o program source.c

# With memory/UB error detection
gcc -Wall -Wextra -Werror -g -std=c11 -fsanitize=address,undefined -o program source.c

# Pipeline stages
gcc -E source.c -o source.i    # Preprocess only
gcc -S source.c -o source.s    # Compile to assembly
gcc -c source.c -o source.o    # Compile to object file
gcc source.o -o program        # Link only
```

---

## GDB Quick Reference

```bash
gdb ./program              # Start GDB
gdb -tui ./program         # Start with source view

# Breakpoints
break main                 # Break at main
break file.c:20            # Break at line 20
break function_name        # Break at function
delete 1                   # Delete breakpoint 1
info breakpoints           # List all

# Run and control
run                        # Start
run arg1 arg2              # Start with args
next     (n)               # Step over
step     (s)               # Step into
continue (c)               # Continue
finish                     # Run to return
quit                       # Exit

# Inspect
print expr                 # Print value
print *ptr                 # Dereference pointer
info locals                # All local variables
backtrace  (bt)            # Call stack
frame N                    # Switch to frame N
list                       # Show source

# Memory
x/Nd addr                  # N decimal values at addr
x/Nx addr                  # N hex values
x/s addr                   # String at addr
```

---

## C Data Types (64-bit Linux/macOS)

| Type | Size | Range |
|------|------|-------|
| `char` | 1 byte | -128 to 127 |
| `unsigned char` | 1 byte | 0 to 255 |
| `short` | 2 bytes | -32,768 to 32,767 |
| `int` | 4 bytes | -2,147,483,648 to 2,147,483,647 |
| `long` | 8 bytes | -9.2×10¹⁸ to 9.2×10¹⁸ |
| `long long` | 8 bytes | Same as `long` on 64-bit |
| `float` | 4 bytes | ≈ 7 decimal digits precision |
| `double` | 8 bytes | ≈ 15 decimal digits precision |
| `pointer` | 8 bytes | Addresses 0 to 2⁶⁴-1 |

**Portable exact-width types** (`#include <stdint.h>`):
```c
int8_t    int16_t    int32_t    int64_t
uint8_t   uint16_t   uint32_t   uint64_t
```

---

## printf Format Specifiers

| Specifier | Type | Example |
|-----------|------|---------|
| `%d`, `%i` | int | `printf("%d", 42)` → `42` |
| `%u` | unsigned int | `printf("%u", 42u)` → `42` |
| `%ld` | long | `printf("%ld", 1L)` → `1` |
| `%f` | double | `printf("%f", 3.14)` → `3.140000` |
| `%.2f` | double (2 dp) | `printf("%.2f", 3.14)` → `3.14` |
| `%e` | double (sci) | `printf("%e", 3.14)` → `3.140000e+00` |
| `%g` | double (short) | `printf("%g", 3.14)` → `3.14` |
| `%c` | char | `printf("%c", 'A')` → `A` |
| `%s` | char* | `printf("%s", "hi")` → `hi` |
| `%p` | pointer | `printf("%p", ptr)` → `0x...` |
| `%x` | unsigned hex | `printf("%x", 255)` → `ff` |
| `%X` | unsigned HEX | `printf("%X", 255)` → `FF` |
| `%%` | literal % | `printf("100%%")` → `100%` |

**Width & precision:**
```
%10d    right-align in 10 chars
%-10d   left-align in 10 chars
%010d   zero-pad to 10 chars
%.3f    3 decimal places
%8.2f   width 8, 2 decimal places
```

---

## scanf Format Specifiers

| Specifier | Type             | Note                              |
| --------- | ---------------- | --------------------------------- |
| `%d`      | `int *`          | `scanf("%d", &x)`                 |
| `%u`      | `unsigned int *` |                                   |
| `%ld`     | `long *`         |                                   |
| `%f`      | `float *`        | (not `%lf` — that's double)       |
| `%lf`     | `double *`       | **Use `%lf` for double in scanf** |
| `%c`      | `char *`         | Single character                  |
| `%s`      | `char *`         | String (unsafe — use `%Ns`)       |
| `%49s`    | `char[50]`       | Safe: max 49 chars + null         |

---

## Escape Sequences

| Sequence | Meaning | ASCII |
|----------|---------|-------|
| `\n` | Newline | 10 |
| `\t` | Tab | 9 |
| `\r` | Carriage return | 13 |
| `\0` | Null character | 0 |
| `\\` | Backslash | 92 |
| `\'` | Single quote | 39 |
| `\"` | Double quote | 34 |
| `\a` | Bell | 7 |
| `\b` | Backspace | 8 |

---

## Program Structure Template

```c
/* filename.c — brief description
 * Author: Your Name
 * Date:   Week X
 */

#include <stdio.h>
#include <stdlib.h>

/* Constants */
#define MAX_SIZE 100

/* Type definitions (when needed) */

/* Function prototypes */
int do_something(int x, int y);
void print_result(int result);

/* Main entry point */
int main(int argc, char *argv[]) {
    /* Variable declarations */
    int x = 0;
    int y = 0;
    int result;

    /* Input */
    printf("Enter two integers: ");
    if (scanf("%d %d", &x, &y) != 2) {
        fprintf(stderr, "Error: expected two integers\n");
        return 1;
    }

    /* Processing */
    result = do_something(x, y);

    /* Output */
    print_result(result);

    return 0;  /* 0 = success */
}

/* Function definitions */
int do_something(int x, int y) {
    return x + y;
}

void print_result(int result) {
    printf("Result: %d\n", result);
}
```

---

## Makefile Template

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11
SANITIZE = -fsanitize=address,undefined

# Add target name to 'all' list
all: program1 program2

program1: program1.c
	$(CC) $(CFLAGS) $(SANITIZE) -o $@ $<

program2: program2.c
	$(CC) $(CFLAGS) $(SANITIZE) -o $@ $<

clean:
	rm -f program1 program2 *.o

.PHONY: all clean
```

---

## Key Errors and Their Meaning

| Error | Stage | Meaning |
|-------|-------|---------|
| `error: expected ';'` | Compiler | Missing semicolon |
| `error: use of undeclared identifier 'x'` | Compiler | Used `x` before declaring it |
| `warning: implicit declaration of function 'foo'` | Compiler | Called `foo()` without a prototype |
| `undefined reference to 'foo'` | **Linker** | `foo` declared but never defined |
| `multiple definition of 'foo'` | Linker | `foo` defined in two `.o` files |
| `Segmentation fault` | Runtime | Invalid memory access |
| `*** missing separator` | Make | TAB required, spaces found |

---

## Command Line Workflow

```bash
# Start a new project ($PROG101 is set in ~/.bashrc -- see Lab 0)
mkdir -p "$PROG101/weekN/ps"
cd "$PROG101/weekN/ps"

# Edit-compile-test cycle
$EDITOR program.c          # Write/edit
make program               # Compile
./program                  # Run
make clean && make         # Full rebuild

# Debug
gdb ./program              # Debug
valgrind ./program         # Memory check (Linux)

# Commit progress
git add .
git commit -m "descriptive message"
```

---

## Recommended Resources

- **K&R** — The C Programming Language (read cover to cover)
- **cppreference.com** — Best online C/C++ reference
- **godbolt.org** — Compile C and view assembly interactively (Compiler Explorer)
- **pythontutor.com** — Visualize C program execution and memory (supports C)
- **man pages** — `man 3 printf`, `man 3 malloc`, etc.
- **CS:APP** — Bryant & O'Hallaron (deep understanding of C and the machine)
