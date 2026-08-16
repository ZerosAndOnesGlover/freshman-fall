# PROG 101 · Programming I: Structured Programming in C
## Week 0 · Problem Set 0

**Released:** End of Week 0
**Due:** Before Week 1 Lecture 1 (start of next week)
**Submission:** Push to your Git repository; submit the commit hash on the course portal.
**Collaboration policy:** Discussion of concepts allowed; code must be written independently.
**Grading:** Each problem is graded on correctness (70%), code quality (20%), and documentation (10%).

---

## Setup

All your work this week goes in `~/prog101/week0/ps0/`.

```bash
mkdir -p ~/prog101/week0/ps0
cd ~/prog101/week0/ps0
```

Each problem should be in its own `.c` file. Submit a `Makefile` that builds all of them.

---

## Problem 1: The Compilation Pipeline Inspector (10 pts)

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

Sample output:
```
=== C Compilation Pipeline: hello.c ===

Stage 1 — Preprocessing:
  Output: hello.i
  Lines:  847
  Size:   22,341 bytes

Stage 2 — Compilation (C → Assembly):
  Output: hello.s
  Lines:  45
  Size:   1,023 bytes

Stage 3 — Assembly (Assembly → Object):
  Output: hello.o
  Size:   2,864 bytes

Stage 4 — Linking (Object → Executable):
  Output: hello
  Size:   16,128 bytes

=== Complete pipeline: OK ===
```

**Hints:**
- `wc -l file` counts lines; `wc -c file` counts bytes
- Use `$1` to access the first command-line argument in a shell script
- Use `${1%.c}` to strip the `.c` extension from the filename
- Make the script executable: `chmod +x pipeline.sh`

---

## Problem 2: Personal Info Printer (15 pts)

Write `info.c` — a program that:
1. Uses `#define` to define your name, student ID, and graduation year as constants
2. Prints a formatted information card using `printf`

Your output must look *exactly* like this (with your own information):

```
╔══════════════════════════════════════════════════╗
║             PROG 101 Student Profile             ║
╠══════════════════════════════════════════════════╣
║  Name:    Adebayo Glover                         ║
║  ID:      20260001                               ║
║  Year:    2026                                   ║
║  Course:  PROG 101 - Structured Programming in C ║
╚══════════════════════════════════════════════════╝
```

Requirements:
- Use `#define` for at least your name, ID, and year
- The box must be exactly 40 characters wide (including the border characters)
- Each field must be left-aligned within the box
- Compile clean with `-Wall -Wextra -Werror`

**Hint for the box characters:** These are UTF-8 characters. You can paste them directly into your string literals:
`╔ ═ ╗ ║ ╠ ╣ ╚ ╝`

---

## Problem 3: Temperature Conversion Table (20 pts)

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

---

## Problem 4: The Compilation Error Hunt (15 pts)

The file `broken.c` (provided below) contains **10 deliberate errors** — a mix of preprocessor, compilation, and linker issues.

Copy this exactly into `broken.c` (do not fix anything yet):

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

Your task:
1. Create `error_log.md`, document each error:
   - Error number (1-10)
   - The line and what is wrong
   - What category it is (preprocessor / compiler / linker / logic / undefined behavior)
   - What the fix is
1. Create `fixed.c`: the fully corrected version

Format your `error_log.md` like this:
```markdown
## Error 1
- **Location:** Line 1
- **Problem:** Missing closing `>` in `#include <stdio.h`
- **Category:** Preprocessor error
- **Fix:** Change to `#include <stdio.h>`
```

---

## Problem 5: GDB Investigation (20 pts)

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

---

## Problem 6: The Symbols Inspector (20 pts)

Write `symbols.c` containing:
- 3 global variables (one `int`, one `double`, one `char *`)
- 1 static global variable
- 2 functions that use them
- 1 function that is declared but never defined (to study linker errors)

Then use `nm` to inspect the symbol table and answer these questions in `symbols_report.md`:

1. What letter does `nm` use for defined global variables? Paste the relevant line.
2. What letter does `nm` use for undefined symbols? Paste the relevant line.
3. What letter does `nm` use for static (file-scoped) symbols?
4. What happens when you try to link a program that calls the undefined function? Paste the exact linker error.
5. How is the undefined function's symbol shown in `nm` output for `symbols.o`?
6. What is the difference between `nm symbols.o` and `nm symbols` (after linking without the missing function — how can you link without it)?

**Hint for question 6:** You can use `-Wl,--unresolved-symbols=ignore-all` to link despite undefined symbols (for educational purposes only).

---

## Makefile Requirement

Your `Makefile` must:
- Build all programs: `info`, `temptable`, `fixed`, `gdb_lab`, `symbols`
- Include a `clean` target
- Use `-Wall -Wextra -Werror -g -std=c11` flags
- Have a `test` target that runs quick sanity checks

```makefile
.PHONY: all clean test

all: info temptable fixed gdb_lab symbols

test: all
	@echo "Testing temptable..."
	@echo "Running: ./temptable 0 20"
	./temptable 0 20
	@echo "Testing info..."
	./info
	@echo "All tests passed."

clean:
	rm -f info temptable fixed gdb_lab symbols *.o
```

---

## Submission

```bash
cd ~/prog101/week0/ps0
git add .
git commit -m "PS0: complete — all 6 problems"
git log --oneline -1    # Copy this commit hash for submission
```

Submit on the course portal:
- Your commit hash
- A brief reflection (2-3 sentences): what was the most surprising thing you learned this week?

---

## Grading Rubric

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Pipeline Script | 10 | Correct output for any `.c` file |
| P2: Info Printer | 15 | Exact formatting, `#define` used |
| P3: Temp Table | 20 | Correct formulas, argument parsing, error handling |
| P4: Error Hunt | 15 | All 10 errors found, categories correct, clear explanations |
| P5: GDB Investigation | 20 | Accurate GDB session, correct observations |
| P6: Symbols Inspector | 20 | All 6 questions answered with evidence |
| **Total** | **100** | |

**Late policy:** 10% deducted per day late. No submissions accepted after 5 days.

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading Rubric above (100 points).
> All C below was compiled with `gcc 13.3.0 -Wall -Wextra -Werror -std=c11` and executed.

### ⚠️ Errata — CORRECTED in the text above

Three defects, all verified against `gcc 13.3.0` / GNU `nm` on x86-64 Linux. The first two **have
now been fixed in this document**; the third is a live inconsistency flagged for the author.

| Location | Was (wrong) | Now |
|---|---|---|
| P3 expected output, Kelvin column | `273.2`, `278.2` … `373.2`. The claim was restated in the spot-check line below the reference solution: "273.15 displays as 273.2 at one decimal". Both are wrong. `273.15` is not representable in binary — the stored double is `273.14999999999997726`, so `%.1f` correctly rounds **down**. The answer key's own reference solution prints `273.1`; it was never run against its own expected output. | Corrected to `273.1` … `373.1` for the six rows shown, matching what the reference solution actually prints. |
| P6 reference answer 6 | "after which the symbol remains `U` in the executable". It does not. After `gcc -Wl,--unresolved-symbols=ignore-all symbols.o -o symbols_ignored`, `nm symbols_ignored \| grep undefined_function` returns **nothing** — the symbol is dropped, not retained. | Reworded to state the symbol does not appear in the linked executable's symbol table, and that calling it still crashes at runtime. |
| P2 box width (**unresolved**) | The prose requirement says the box "must be exactly 40 characters wide", but the sample art in the same problem is **52** characters on every line, and the note formerly here asserted it was 40. The art was later widened to fit the full course title without the prose being updated. | Not auto-corrected — the author must choose. The art is self-consistent at 52; only the prose sentence and the deleted note disagreed. Accept either width until resolved, and grade alignment and `#define` usage rather than the constant. |

Students holding a pre-correction copy must not be penalised for a `273.2` Kelvin column or for a
40-character box.

---

### Problem 1 — Pipeline Script (10 pts)

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

### Problem 2 — Info Printer (15 pts)

*Grading: 5 pts `#define` used for name/ID/year (a `const char *` or literal in the `printf` earns 0 for this item — the requirement is the preprocessor), 6 pts exact 40-character box with correct alignment, 4 pts clean compile under `-Wall -Wextra -Werror`.*
*Alignment is best done with width specifiers, e.g. `printf("║  Name:    %-27s ║\n", NAME);`. Students who pad by hand with spaces get the right output for their own name but break for any other — mention it, deduct only if the output is actually misaligned.*
*Note: the box characters are multi-byte UTF-8. `strlen` on these lines returns **more** than 40 (bytes, not characters); a student who "verifies" width with `strlen` and panics is not wrong about the count — explain the distinction. This is worth a bonus mark if raised unprompted.*

### Problem 3 — Temperature Table (20 pts)

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

*Do not expect `273.2` here.* `273.15` has no exact binary representation — the stored double is
`273.14999999999997726`, marginally **below** the midpoint, so `%.1f` rounds down to `273.1`. This
is the correct and only output on any IEEE-754 platform, and the reference solution above produces
it. See the errata table. A student reporting `273.1` is right; a student who reports `273.2` has
almost certainly not run their program.

*Grading: 4 pts argc/argv handling, 4 pts conversion via `atof`/`strtod`, 4 pts both formulas correct, 4 pts error handling with non-zero exit, 4 pts table formatting.*
*`atof` is explicitly permitted by the prompt, but it **cannot** report failure — `atof("abc")` silently returns 0.0. A student using `strtod` with `endptr` validation has done strictly better; award the error-handling points fully and note it as good practice. A student using `atof` and claiming they validate input has not — deduct 2 unless they check separately.*
*Floating-point loop counters accumulate error; `c += 5.0` over a wide range can make the final row land at 99.99999. Accept it, but an integer loop counter with `c = start + 5.0*i` is the more robust answer and deserves a style bonus.*

### Problem 4 — The Compilation Error Hunt (15 pts)

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

### Problem 5 — GDB Investigation (20 pts)

*Grading: 7 pts breakpoint + step trace of `factorial(5)` showing `n` = 5,4,3,2,1,0 at successive frames; 7 pts a genuine `backtrace` for `fibonacci(6)` at the base case (should show a chain of `fibonacci` frames beneath `main`); 6 pts the `factorial(-1)` investigation.*
*Expected finding for `factorial(-1)`: with a base case of `if (n == 0) return 1;` the argument decrements away from zero forever, so it **does not terminate** — it recurses until the stack is exhausted and the program dies with `SIGSEGV` (stack overflow). In GDB this shows as a segfault with an enormous backtrace. The instructive fix is `if (n <= 0) return 1;` or rejecting negative input outright. Accept either "infinite recursion" or "stack overflow / segfault" as the observation, but require **evidence** from an actual session, not a prediction.*

### Problem 6 — Symbols Inspector (20 pts)

Reference answers (`nm` letters are case-significant: **uppercase = global/external, lowercase = local/static**):

1. **`D`** — initialised global in the data segment. (An uninitialised global is **`B`**, BSS; a `const` one is often **`R`**, read-only data.)
2. **`U`** — undefined: referenced here, must be supplied by another translation unit at link time.
3. **`d`/`b`/`t`** — the lowercase counterparts, indicating file scope (`static`). A `static` function is **`t`**; a non-static function is **`T`**.
4. Linking fails at the **linker** stage, not the compiler — the exact wording on GNU ld is along the lines of:
   `undefined reference to 'never_defined'` followed by `collect2: error: ld returned 1 exit status`.
5. In `nm symbols.o` the never-defined function appears with type **`U`** and no address — the object file records the dependency without resolving it.
6. `nm symbols.o` lists only this translation unit's symbols, with `U` entries still outstanding. `nm symbols` (the linked executable) shows those symbols **resolved to addresses**, plus everything pulled in from libc and the startup files — a much longer listing (verified: 9 symbols in the object file against 36 in the executable). Linking despite the missing symbol requires `-Wl,--unresolved-symbols=ignore-all`. Note that the unresolved symbol is then **absent from the executable's symbol table altogether** — `nm symbols_ignored | grep undefined_function` returns nothing, it does *not* survive as a `U` entry — and the call site is left aimed at an unrelocated PLT stub, so invoking it dies with `SIGSEGV` (verified: exit status 139).

*Grading: 3 pts each for Q1–Q3 and Q5–Q6, 2 pts Q4 — **pasted evidence is required** for Q1, Q2, and Q4; an answer stating the letter without the `nm` line earns half.*
*The key insight to look for across the whole problem: the compiler is happy to emit an object file full of `U` symbols. Only the **linker** demands they all resolve. This is why "undefined reference" errors look and read so differently from compiler errors.*

### Makefile

*Grading is folded into the per-problem marks; a submission whose `Makefile` does not build all five targets loses 2 points overall. Require `.PHONY` on `clean`/`test`/`all`, and the exact flag set `-Wall -Wextra -Werror -g -std=c11`.*

---

*PROG 101 · Week 0 · Problem Set 0 · © CSE Department*
