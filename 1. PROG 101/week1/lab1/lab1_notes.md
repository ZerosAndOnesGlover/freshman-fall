# PROG 101 · Lab 1 — Memory and Representation, Seen Through GDB

**Name:** Adebayo Glover · **Lab:** Week 1 Lab 1 (Memory and Representation)
**Tools:** `gcc 15.2.0`, GDB 17.1, x86-64 Linux (LP64). Built with `make` (`-Wall -Wextra -g -O0 -std=c11`).

All values below are real output from `sizes.c` and from a GDB session on `explore.c`
(`gdb -batch -ex "break 20" -ex run ...`). Stack addresses differ per run; the byte values do not.

---

## Part 1 — What `sizeof` and the Bytes Say

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

| type | `sizeof` |
|---|---|
| `char` | 1 |
| `short` | 2 |
| `int` | 4 |
| `long` | 8 |
| `long long` | 8 |
| `float` | 4 |
| `double` | 8 |
| `long double` | 16 |

### 1B — Bytes of `i` (`i = 0x12345678`)

```
(gdb) x/4xb &i
0x7fffffffd45c: 0x78  0x56  0x34  0x12
```

The **lowest address holds `0x78`** — the **least significant byte** of `0x12345678`. Storing the
least-significant byte first is **little-endian**. (Big-endian would read `0x12 0x34 0x56 0x78`.)

---

## Part 2 — Two's Complement, Directly

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

### 2A — Why `sc` and `uc` print the same bits

`sc` is `signed char -42` and `uc` is `unsigned char 214`. A negative value is stored in two's
complement: `−42` becomes `256 − 42 = 214`, and `214` in 8-bit binary is `11010110`. So both variables
hold the identical byte `11010110`; only the **type's interpretation** of that byte differs (signed →
−42, unsigned → 214).

### 2B — What decides whether `0xfffffffe` means −2 or 4294967294

The **type**. The 32 bits are the same in both variables. Read as `int` (signed, two's complement)
`0xfffffffe` is −2; read as `unsigned` it is 4294967294. That `neg == (int)u` prints `1` confirms the
bits are equal once both are treated as `int` — the bit pattern is the value's identity, the type is
the lens.

### 2C — Defined vs. implementation-defined

* `(unsigned char)-1` → **defined**: converting to an unsigned type reduces modulo 2ⁿ, so
  `−1 mod 256 = 255` on every conforming implementation.
* `(signed char)200` → **implementation-defined**: 200 is out of range for `signed char`, so the
  standard lets the implementation choose. Here (gcc) it wraps to **−56**.

---

## Part 3 — Floating Point in Memory

```
(gdb) x/4xb &f      0x00  0x00  0x80  0x3f                          = 0x3f800000   (1.0f)
(gdb) x/4xb &tenth  0xcd  0xcc  0xcc  0x3d                          = 0x3dcccccd   (0.1f)
(gdb) x/8xb &d      0x9a  0x99  0x99  0x99  0x99  0x99  0xb9  0x3f  = 0x3fb999999999999a  (0.1)
```

Reading each back to front (little-endian) gives a single hex number. `1.0f` = `0x3f800000`, as the
lab says.

### 3A — The repeating pattern and why `0.1` is not exact

The bytes of `0.1` are dominated by **repeating `cc…` (`0.1f`) and `99…` (`0.1`)**. That is `0.1`'s
**repeating binary expansion** — `0.1 = 0.00011001100110011…₂`, with the `0011` block repeating
forever. A finite mantissa (23 bits for `float`, 52 for `double`) cannot hold an infinite repeating
expansion, so the stored value is **truncated and rounded**: the final byte is `cd` (not `cc`) and
`9a` (not `99`), the rounding-up of the cut-off tail. Hence `0.1` cannot be represented exactly.

### 3B — Which is closer to 0.1

Program output:

```
tenth=0.1000000015   (%.10f of the float)
d=0.10000000000000000555   (%.20f of the double)
```

The **`double` is closer** to 0.1 — its error is far smaller. Roughly, the `float` stays accurate to
about **7 significant decimal digits** (`0.1000000015` diverges at the 8th/9th digit), while the
`double` stays accurate to about **16** (`0.10000000000000000555` diverges around the 17th digit).

---

## Deliverables checked

* `sizes.c`, `explore.c`, `Makefile` (builds both with `-g -O0`), and this `lab1_notes.md`.
* Show-your-TA command (real output):

```
$ gdb -batch -ex "break 20" -ex run -ex "x/4xb &i" ./explore
Breakpoint 1 at 0x1208: file explore.c, line 20.
Breakpoint 1, main () at explore.c:20
20      return 0;
0x7fffffffd45c: 0x78  0x56  0x34  0x12
```

---

*PROG 101 · Week 1 · Lab 1 · Adebayo Glover*
