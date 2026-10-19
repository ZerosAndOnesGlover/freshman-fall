---
assessment: Lab 1
course: PROG 101
component: Labs
possible: 20
score: 20
status: graded
started: 2026-10-05
submitted: 2026-10-05
graded: 2026-10-05
source: "LAB 1 Memory and Representation.md"
---

# PROG 101 · Lab 1
## Answer Sheet — Memory and Representation, Seen Through GDB

**Assessment:** `LAB 1 Memory and Representation.md`
**Points available:** 20 (completion + correctness)

Code and full transcript live in `1. PROG 101/week1/lab1/`:
`sizes.c`, `explore.c`, `Makefile` (builds both with `-g -O0`), `lab1_notes.md`.

Tools: `gcc 15.2.0`, GDB 17.1, x86-64 Linux (LP64). All values below are real GDB output.

---

## Part 1 — What `sizeof` and the Bytes Say  (6 points)

### 1A — `sizes.c`

```
char        1
short       2
int         4
long        8
long long   8
float       4
double      8
long double 16
```

### 1B — Bytes of `i` (`i = 0x12345678`)

```
(gdb) x/4xb &i
0x7fffffffd45c: 0x78  0x56  0x34  0x12
```

The **lowest address holds `0x78`**, the **least-significant byte** of `0x12345678`. Storing the
LSB first means this machine is **little-endian** (a big-endian machine would show `0x12 0x34 0x56 0x78`).

*Marks: 6 / 6*

---

## Part 2 — Two's Complement, Directly  (8 points)

| Command | Recorded |
|---|---|
| `p/t sc` | `11010110` |
| `p/t uc` | `11010110` |
| `p/x s` | `0xffff` |
| `p/x neg` | `0xfffffffe` |
| `p/x u` | `0xfffffffe` |
| `p neg == (int)u` | `1` |
| `p/d (signed char)200` | `-56` |
| `p/u (unsigned char)-1` | `255` |

**2A.** `−42` is stored in two's complement as `256 − 42 = 214 = 11010110`, which is *exactly* the byte
`uc` holds (`uc` = 214). The bits are identical; only the **type's reading** of them differs (signed →
−42, unsigned → 214).

**2B.** The **type** decides. The 32 bits `0xfffffffe` are −2 read as `int` and 4294967294 read as
`unsigned`; `neg == (int)u` printing `1` confirms the bit patterns are equal.

**2C.** `(unsigned char)-1` is **defined** by the standard (reduce modulo 256 → 255).
`(signed char)200` is **implementation-defined** (out of range for `signed char`; gcc gives −56).

*Marks: 8 / 8*

---

## Part 3 — Floating Point in Memory  (6 points)

```
(gdb) x/4xb &f      0x00  0x00  0x80  0x3f                          = 0x3f800000   (1.0f)
(gdb) x/4xb &tenth  0xcd  0xcc  0xcc  0x3d                          = 0x3dcccccd   (0.1f)
(gdb) x/8xb &d      0x9a  0x99  0x99  0x99  0x99  0x99  0xb9  0x3f  = 0x3fb999999999999a  (0.1)
```

**3A.** The bytes of `0.1` show a **repeating `cc…` / `99…` pattern** — that is `0.1`'s repeating binary
expansion (`0.00011001100110011…₂`, block `0011` repeating). A finite mantissa (23 bits for `float`,
52 for `double`) cannot hold an infinite expansion, so the value is truncated and rounded (the final
bytes `cd` / `9a` are the round-up of the cut-off tail). Hence `0.1` cannot be stored exactly.

**3B.** Output: `tenth=0.1000000015` (`%.10f`) and `d=0.10000000000000000555` (`%.20f`). The **`double`
is closer** to 0.1: the `float` is accurate to about **7** significant decimal digits and the `double`
to about **16**.

*Marks: 6 / 6*

---

## Grading Summary

| | |
|---|---|
| **Score** | 20 / 20 |
| **Percent** | 100% |
| **Graded** | 2026-10-05 |

**Feedback:**
Complete and correct. `sizes.c` reproduces the exact table (`long double` = 16 included); the byte dump
of `i` is read correctly as little-endian with the LSB at the lowest address. Part 2 records every GDB
value and pinpoints the two's-complement identity of `−42`/`214` and the role of type in reading
`0xfffffffe`, correctly separating the defined unsigned conversion from the implementation-defined
signed one. Part 3 reads all three hex patterns, explains the repeating binary expansion as the reason
`0.1` is inexact, and quantifies float vs. double accuracy (≈7 vs ≈16 digits). `Makefile` builds both
programs with `-g -O0`; the show-your-TA command was demonstrated.
