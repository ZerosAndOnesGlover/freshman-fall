# PROG 101 · Relocated Problems
## Removed from Week 0 Problem Set 0 · Awaiting re-filing

═════════════════════════════════════════════════════════════

> **Why this file exists.** These four problems were removed from PS 0 on 2026-08-16 because they
> tested material from Weeks 2–10 in a Week 0 set (see [[Year1 - Freshman/PREREQUISITE AUDIT|PREREQUISITE AUDIT]], findings #1, #2,
> #4, #5, #6, #9, #10). **They are good problems.** Nothing here is deprecated — every answer key
> below was verified against `gcc 13.3.0 -Wall -Wextra -Werror -std=c11` on x86-64 Linux and
> should be re-filed intact into the week that teaches its content.
>
> This file is a holding pen, not course material. It is not assigned and not graded.

## Re-filing Plan

| Problem | Original pts | Requires | Re-file under |
|---|---|---|---|
| P1 Pipeline Script | 10 | shell scripting (`$1`, `${1%.c}`, `chmod`) | **Never taught in PROG 101.** Either add a shell segment to Week 0 Lab, or retire. See note below. |
| P3 Temperature Table | 20 | loops (W2), `argc`/`argv`, `strtod` | **Week 2** — Operators, Expressions, and Control Flow |
| P4 Error Hunt (original) | 15 | arrays (W4), pointers (W5), `malloc`/double-free (W6), macro double-evaluation (W10) | **Week 10** — The C Preprocessor and Macros |
| P5 GDB Investigation | 20 | recursion (W9), stack frames | **Week 9** — Recursion in C and Stack Mechanics |

**On P1.** Shell scripting appears nowhere in the PROG 101 docx schedule — not in Week 0, not
later. The problem is therefore homeless: it cannot be re-filed without first adding shell
scripting to a lecture. Options are (a) extend Lab 0 with a short shell segment and restore this
problem to Week 0, or (b) retire it. Deferred pending that decision.

**On P4.** The original planted ten defects across four topic areas. A Week 10 version should keep
the `SQUARE(3+1)` macro defect as its centrepiece — that is precisely the Week 10 lesson — and can
keep the `malloc`/double-free pair, which by Week 10 is four weeks in the past.

═════════════════════════════════════════════════════════════

## P1 — The Compilation Pipeline Inspector (10 pts)

Write a shell script `pipeline.sh` that automates the full manual pipeline from Lab 0:

```bash
#!/bin/bash
# pipeline.sh — run all four stages of C compilation and report sizes

# Usage: ./pipeline.sh <source.c>
```

Your script should:
1. Accept a `.c` filename as its first argument
2. Run each of the four compilation stages separately
3. Print the file size (in bytes) of the output of each stage
4. Print the number of lines of the output of each stage (where applicable)
5. Finally, run the complete compilation with `gcc -Wall -g -std=c11`

**Hints:**
- `wc -l file` counts lines; `wc -c file` counts bytes
- Use `$1` to access the first command-line argument in a shell script
- Use `${1%.c}` to strip the `.c` extension from the filename
- Make the script executable: `chmod +x pipeline.sh`

### Answer key

```bash
#!/bin/bash
# pipeline.sh — run all four stages of C compilation and report sizes
set -e
if [ $# -ne 1 ]; then echo "Usage: $0 <source.c>" >&2; exit 1; fi
src="$1"; base="${1%.c}"
[ -f "$src" ] || { echo "No such file: $src" >&2; exit 1; }

echo "=== C Compilation Pipeline: $src ==="; echo
gcc -E "$src" -o "$base.i"
printf "Stage 1 — Preprocessing:\n  Output: %s.i\n  Lines:  %s\n  Size:   %s bytes\n\n" \
       "$base" "$(wc -l < "$base.i")" "$(wc -c < "$base.i")"
gcc -S "$base.i" -o "$base.s"
printf "Stage 2 — Compilation (C → Assembly):\n  Output: %s.s\n  Lines:  %s\n  Size:   %s bytes\n\n" \
       "$base" "$(wc -l < "$base.s")" "$(wc -c < "$base.s")"
gcc -c "$base.s" -o "$base.o"
printf "Stage 3 — Assembly (Assembly → Object):\n  Output: %s.o\n  Size:   %s bytes\n\n" \
       "$base" "$(wc -c < "$base.o")"
gcc "$base.o" -o "$base"
printf "Stage 4 — Linking (Object → Executable):\n  Output: %s\n  Size:   %s bytes\n\n" \
       "$base" "$(wc -c < "$base")"
gcc -Wall -g -std=c11 "$src" -o "$base"
echo "=== Complete pipeline: OK ==="
```

*Grading: 2 pts argument handling (count + file exists), 6 pts all four stages invoked **separately** with correct flags (`-E`, `-S`, `-c`, link), 2 pts sizes/line counts reported.*
*Accept any exact byte counts — they vary by gcc version, libc, and architecture. The sample numbers in the prompt are illustrative, not targets. Do **not** mark down a student whose `hello.i` is 800 or 30,000 lines.*

═════════════════════════════════════════════════════════════

## P3 — Temperature Conversion Table (20 pts)

Write `temptable.c` — a program that prints a conversion table for temperatures.

The program should:
1. Accept two command-line arguments: start temperature and end temperature (in Celsius)
2. Print a formatted table with columns: Celsius | Fahrenheit | Kelvin
3. Increment by 5°C each row
4. Handle invalid input gracefully

```bash
./temptable 0 100
```

Expected output:
```
╔═══════════╦═══════════╦═══════════╗
║  Celsius  ║  Fahrenh  ║  Kelvin   ║
╠═══════════╬═══════════╬═══════════╣
║      0.0  ║     32.0  ║   273.1   ║
║      5.0  ║     41.0  ║   278.1   ║
║     10.0  ║     50.0  ║   283.1   ║
║     15.0  ║     59.0  ║   288.1   ║
║     20.0  ║     68.0  ║   293.1   ║
║     ...   ║     ...   ║   ...     ║
║    100.0  ║    212.0  ║   373.1   ║
╚═══════════╩═══════════╩═══════════╝
```

Requirements:
- Use `argc` and `argv` to read command-line arguments
- Use `atof()` or `strtod()` to convert string arguments to doubles
- Print an error and exit with code 1 if wrong number of arguments or invalid values
- Formulas: F = (C × 9/5) + 32 ; K = C + 273.15

**Hints:**
- `int main(int argc, char *argv[])` gives you access to command-line arguments
- `argc` is the argument count (program name counts as argument 0)
- `argv[1]` is the first argument (as a string), `argv[2]` is the second
- `atof(argv[1])` converts a string to double

### Answer key

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <start_C> <end_C>\n", argv[0]);
        return 1;
    }
    char *end1, *end2;
    double start = strtod(argv[1], &end1);      /* strtod, not atof: detects junk */
    double stop  = strtod(argv[2], &end2);
    if (*end1 != '\0' || *end2 != '\0' || end1 == argv[1] || end2 == argv[2]) {
        fprintf(stderr, "Error: arguments must be numeric\n");
        return 1;
    }
    if (start > stop) { fprintf(stderr, "Error: start must not exceed end\n"); return 1; }

    printf("╔═══════════╦═══════════╦═══════════╗\n");
    printf("║  Celsius  ║  Fahrenh  ║  Kelvin   ║\n");
    printf("╠═══════════╬═══════════╬═══════════╣\n");
    for (double c = start; c <= stop; c += 5.0)
        printf("║ %8.1f  ║ %8.1f  ║ %8.1f  ║\n", c, c * 9.0 / 5.0 + 32.0, c + 273.15);
    printf("╚═══════════╩═══════════╩═══════════╝\n");
    return 0;
}
```

Spot-check against the prompt's table: 0 °C → 32.0 °F / **273.1** K ✓; 100 °C → 212.0 °F / **373.1** K ✓.

> **⚠️ Erratum, carried from PS 0.** *Do not expect `273.2` here.* `273.15` has no exact binary
> representation — the stored double is `273.14999999999997726`, marginally **below** the midpoint,
> so `%.1f` rounds down to `273.1`. This is the correct and only output on any IEEE-754 platform,
> and the reference solution above produces it. The original prompt's expected output said `273.2`
> and was never run against its own reference solution. A student reporting `273.1` is right; a
> student who reports `273.2` has almost certainly not run their program.

*Grading: 4 pts argc/argv handling, 4 pts conversion via `atof`/`strtod`, 4 pts both formulas correct, 4 pts error handling with non-zero exit, 4 pts table formatting.*
*`atof` is explicitly permitted by the prompt, but it **cannot** report failure — `atof("abc")` silently returns 0.0. A student using `strtod` with `endptr` validation has done strictly better; award the error-handling points fully and note it as good practice. A student using `atof` and claiming they validate input has not — deduct 2 unless they check separately.*
*Floating-point loop counters accumulate error; `c += 5.0` over a wide range can make the final row land at 99.99999. Accept it, but an integer loop counter with `c = start + 5.0*i` is the more robust answer and deserves a style bonus.*

═════════════════════════════════════════════════════════════

## P4 — The Compilation Error Hunt, original version (15 pts)

The file `broken.c` contains **10 deliberate errors** — a mix of preprocessor, compilation, and
linker issues.

```c
#include <stdio.h
#include <stdlib.h>

#define MAX_SIZE 10
#define SQUARE(x) x * x

int compute_sum(int arr, int n);

int main(void) {
    int numbers[MAX_SIZE] = {1, 2, 3, 4, 5};
    int total = compute_sum(numbers, 5)
    double pi = 3.14159;

    printf("Sum: %d\n" total);
    printf("Pi: %d\n", pi);
    printf("Square of 3+1: %d\n", SQUARE(3+1));

    int *ptr = malloc(sizeof(int) * 5);
    free(ptr);
    free(ptr);

    return;
}

int compute_sum(int *arr, int n) {
    int sum = 0
    for (int i = 0; i <= n; i++) {
        sum += arr[i];
    }
    return sum;
}
```

### Answer key

The ten planted defects, verified against `gcc 13.3.0`:

| # | Line | Problem | Category | Fix |
|---|---|---|---|---|
| 1 | 1 | `#include <stdio.h` — missing `>` | Preprocessor | `#include <stdio.h>` |
| 2 | 5 | `#define SQUARE(x) x * x` — unparenthesised | Preprocessor / logic | `#define SQUARE(x) ((x) * (x))` |
| 3 | 7 | Prototype says `int arr`; definition uses `int *arr` | Compiler (conflicting types) | Declare `int compute_sum(const int *arr, int n);` |
| 4 | 11 | Missing `;` after the `compute_sum(...)` call | Compiler (syntax) | Add `;` |
| 5 | 14 | `printf("Sum: %d\n" total)` — missing comma | Compiler (syntax) | `printf("Sum: %d\n", total);` |
| 6 | 15 | `%d` used to print a `double` | Undefined behavior | `printf("Pi: %f\n", pi);` |
| 7 | 19–20 | `free(ptr)` called twice | Undefined behavior | Free once; set `ptr = NULL` after |
| 8 | 22 | `return;` inside `int main(void)` | Compiler | `return 0;` |
| 9 | 26 | `int sum = 0` — missing `;` | Compiler (syntax) | Add `;` |
| 10 | 27 | `for (i = 0; i <= n; i++)` — off-by-one | Logic / UB | `i < n` |

**gcc's actual first diagnostics** (parsing stops early, so students must fix iteratively — mention this in the debrief):

```
broken.c:1:18: error: missing terminating > character
broken.c:11:29: warning: passing argument 1 of 'compute_sum' makes integer from pointer without a cast
broken.c:12:5:  error: expected ',' or ';' before 'double'
broken.c:14:23: error: expected ')' before 'total'
```

**Two subtleties worth raising in class:**
- **Error 2 is observable:** `SQUARE(3+1)` expands to `3+1*3+1` = **7**, not 16. Verified by compiling both forms. This is why macro parameters *and* the whole body need parentheses.
- **Error 10 is masked here.** `numbers[MAX_SIZE]` declares **10** ints but initialises only 5, so the remainder are zero-filled; reading `arr[5]` returns 0 and the sum is **15 either way**. Verified. Against a tightly-sized `int tight[5]`, the same loop reads past the end — genuine UB. A student who reports "the off-by-one doesn't change the answer" is *right about this program* and should get full credit plus a bonus for noticing; the bug is still real.

*Grading: 1.5 pts per error (location + category + fix). Accept "logic error" or "undefined behavior" interchangeably for #10. A student finding the unchecked `malloc` as an 11th issue deserves bonus credit — it is a genuine defect the prompt did not count.*

═════════════════════════════════════════════════════════════

## P5 — GDB Investigation (20 pts)

Write `gdb_lab.c` — a program with these three functions:

```c
int factorial(int n);           // Returns n! recursively
int fibonacci(int n);           // Returns nth Fibonacci number recursively
void print_powers(int base, int limit);  // Prints base^0, base^1, ... up to limit
```

Then, in `gdb_session.md`, document a GDB session in which you:

1. Set a breakpoint at `factorial` and trace a call to `factorial(5)` step by step, printing the value of `n` at each recursive call
2. Set a breakpoint at `fibonacci` and use `backtrace` after reaching the base case for `fibonacci(6)` — paste the complete backtrace
3. Inspect what happens when you call `factorial(-1)` — does it terminate? Use GDB to figure out what happens.

Your `gdb_session.md` should show the actual GDB input/output for each investigation. Use code blocks.

### Answer key

*Grading: 7 pts breakpoint + step trace of `factorial(5)` showing `n` = 5,4,3,2,1,0 at successive frames; 7 pts a genuine `backtrace` for `fibonacci(6)` at the base case (should show a chain of `fibonacci` frames beneath `main`); 6 pts the `factorial(-1)` investigation.*
*Expected finding for `factorial(-1)`: with a base case of `if (n == 0) return 1;` the argument decrements away from zero forever, so it **does not terminate** — it recurses until the stack is exhausted and the program dies with `SIGSEGV` (stack overflow). In GDB this shows as a segfault with an enormous backtrace. The instructive fix is `if (n <= 0) return 1;` or rejecting negative input outright. Accept either "infinite recursion" or "stack overflow / segfault" as the observation, but require **evidence** from an actual session, not a prediction.*

═════════════════════════════════════════════════════════════

*PROG 101 · Relocated Problems · not assigned · © CSE Department*
