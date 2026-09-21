# PROG 101 · Week 1
## LAB 1 Solutions: INSTRUCTOR ONLY

> Lab sat Monday 5 October 2026. Rebuilt 2026-09-21: the old lab needed bit operators and loops (Week 2),
> arrays and `%p` pointers (Weeks 4–5) and a function library (Week 3). Everything below was run with
> gcc 13.3 / GDB on x86-64 Linux; stack addresses differ between machines, byte values do not.

---

## Part 1 (6)

`sizes.c`: `char 1, short 2, int 4, long 8, long long 8, float 4, double 8, long double 16`.

`x/4xb &i` → `0x78 0x56 0x34 0x12`. The least significant byte (`0x78`) is at the lowest address:
**little-endian**. *(3 + 3)*

## Part 2 (8)

```
p/t sc  → 11010110        p/t uc  → 11010110
p/x s   → 0xffff
p/x neg → 0xfffffffe      p/x u   → 0xfffffffe
p neg == (int)u → 1
p/d (signed char)200 → -56
p/u (unsigned char)-1 → 255
```

2A: −42 is stored as `256 − 42 = 214` = `11010110`; the bits are identical, only the type's reading
differs. 2B: the **type** — the same 32 bits are −2 as `int` and 4294967294 as `unsigned`. 2C:
`(unsigned char)-1` is defined (reduce modulo 256 → 255); `(signed char)200` is implementation-defined
(gcc gives −56). *(3 / 3 / 2)*

## Part 3 (6)

```
x/4xb &f      → 0x00 0x00 0x80 0x3f                      = 0x3f800000  (1.0f)
x/4xb &tenth  → 0xcd 0xcc 0xcc 0x3d                      = 0x3dcccccd  (0.1f)
x/8xb &d      → 0x9a 0x99 0x99 0x99 0x99 0x99 0xb9 0x3f  = 0x3fb999999999999a (0.1)
```

The repeating `cc…`/`99…` is 0.1's repeating binary expansion (`0.000110011…`), cut off and rounded
(the last byte `cd`/`9a` shows the rounding up). A repeating expansion cannot fit a finite mantissa.
Output line: `tenth=0.1000000015`, `d=0.10000000000000000555` — the `float` is good to about 7
significant digits, the `double` to about 16. *(3 + 3)*

---

*PROG 101 · Week 1 · Lab 1 Solutions · Instructor only*
