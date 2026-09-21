# PROG 101 · Programming I: Structured Programming in C
## Week 1 · Lab 1: Memory and Representation, Seen Through GDB

**Graded: 20 points (completion + correctness)**
**Date:** Monday 5 October 2026 · 15:00–16:50 · Lab Section (Week 2) — covers Week 1 (Lectures 01–03)
**Submission:** Commit to the Freshman Fall repo under `"$PROG101/week1/lab1"`; show your TA before leaving

**Tools used:** Weeks 0–1 only — `gcc`, `make`, GDB (Week 0 Lecture 02), types, `sizeof`, two's complement,
conversions and floating point (Week 1). The C you write is straight-line `main` code: no `if`, loops,
functions, arrays or pointers. GDB does the looking: `p/t` prints a value in binary, `p/x` in hex, and
`x/4xb &name` shows the four bytes stored at a variable's address.

---

## Setup

```bash
mkdir -p "$PROG101/week1/lab1"
cd "$PROG101/week1/lab1"
```

Copy `explore.c` from this lab's `starter/` folder. Build it for debugging:

```bash
gcc -Wall -Wextra -g -O0 -std=c11 -o explore explore.c
./explore
gdb ./explore
(gdb) break 20          # the  return 0;  line — every variable has its value by now
(gdb) run
```

---

## Part 1: What `sizeof` and the Bytes Say (6 pts)

**1A (3 pts).** Write `sizes.c`: one `printf` per type — `char`, `short`, `int`, `long`, `long long`,
`float`, `double`, `long double` — printing its `sizeof` with `%zu`. Record the table.

**1B (3 pts).** In GDB, run `x/4xb &i` (where `i = 0x12345678`). Write down the four bytes in the order
shown. Which byte is at the lowest address? What does that tell you about this machine's byte order
(Lecture 01 §2)?

---

## Part 2: Two's Complement, Directly (8 pts)

In the same GDB session:

| Command | Record |
|---|---|
| `p/t sc` | `sc` is `signed char -42` |
| `p/t uc` | `uc` is `unsigned char 214` |
| `p/x s` | `s` is `short -1` |
| `p/x neg` and `p/x u` | `neg` is `int -2`, `u` is `unsigned 4294967294` |
| `p neg == (int)u` | |
| `p/d (signed char)200` | |
| `p/u (unsigned char)-1` | |

**2A (3 pts).** `sc` and `uc` print the same bits. Explain why, using `256 − 42` (Lecture 02 §2).
**2B (3 pts).** `neg` and `u` have the same hex. What decides whether `0xfffffffe` means −2 or 4294967294?
**2C (2 pts).** Which of the last two conversions is defined by the standard, and which is
implementation-defined?

---

## Part 3: Floating Point in Memory (6 pts)

**3A (3 pts).** Run `x/4xb &f` (`f = 1.0f`), `x/4xb &tenth` (`tenth = 0.1f`) and `x/8xb &d` (`d = 0.1`).
Read each back to front (little-endian) into a single hex number: `1.0f` should give `3f800000`. What
patterns repeat in the bytes of `0.1`, and why does that mean `0.1` cannot be stored exactly (Lecture 03 §2)?

**3B (3 pts).** Look at the program's output line: `tenth` printed with `%.10f` and `d` with `%.20f`.
Which is closer to 0.1, and by roughly how many decimal digits does each stay accurate?

---

## Deliverables

- `sizes.c`, `explore.c`, and `lab1_notes.md` with every recorded value and answer
- A `Makefile` that builds both programs with `-g -O0`

Show your TA: `make && gdb -batch -ex "break 20" -ex run -ex "x/4xb &i" ./explore`.

## Grading

| Part | Points |
|---|---|
| 1 sizeof and bytes | 6 |
| 2 Two's complement | 8 |
| 3 Floating point | 6 |
| **Total** | **20** |

---

*PROG 101 · Week 1 · Lab 1 · Monday 5 October 2026*
