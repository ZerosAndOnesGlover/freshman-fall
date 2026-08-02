# PROG 101 — Week 1 Resources
## Two's Complement Worksheet + Bit Manipulation Reference

---

## Part 1: Two's Complement Practice Worksheet

Complete this worksheet by hand before checking with a program.

### Section A: Identify the Decimal Value

For each 8-bit pattern, compute the signed (two's complement) decimal value.

```
1. 00000000  = ____    (Hint: all zeros)
2. 00000001  = ____
3. 01111111  = ____    (Hint: maximum positive 8-bit value)
4. 10000000  = ____    (Hint: most negative 8-bit value)
5. 10000001  = ____
6. 11111111  = ____    (Hint: what is -1 in two's complement?)
7. 11111110  = ____
8. 11110000  = ____    (Hint: -128 + 64 + 32 + 16)
9. 10101010  = ____
10. 01010101 = ____
```

### Section B: Convert Decimal to 8-bit Two's Complement

```
1.   0  = ________
2.   1  = ________
3.  -1  = ________   (Hint: flip 00000001, add 1)
4.  42  = ________
5. -42  = ________
6. 127  = ________
7. -128 = ________
8.  -5  = ________
9.  64  = ________
10. -64 = ________
```

### Section C: Predict Addition Results (8-bit signed)

For each addition, predict:
- The bit pattern of the result
- The signed decimal value
- Whether overflow occurred

```
1.  00000001 + 00000001  =  ________  (decimal: ____ , overflow: yes/no)
2.  01111111 + 00000001  =  ________  (decimal: ____ , overflow: yes/no)
3.  10000000 + 11111111  =  ________  (decimal: ____ , overflow: yes/no)
4.  11111111 + 00000001  =  ________  (decimal: ____ , overflow: yes/no)
5.  01000000 + 01000000  =  ________  (decimal: ____ , overflow: yes/no)
```

### Section D: Answers

**Section A:**
1. 0  2. 1  3. 127  4. -128  5. -127  6. -1  7. -2  8. -16  9. -86  10. 85

**Section B:**
1. 00000000  2. 00000001  3. 11111111  4. 00101010  5. 11010110
6. 01111111  7. 10000000  8. 11111011  9. 01000000  10. 11000000

**Section C:**
1. 00000010 (2, no overflow)
2. 10000000 (-128, YES OVERFLOW — two positives summed to negative)
3. 01111111 (127, no overflow — -128 + (-1) wraps but: -128 in 8-bit is 10000000, -1 is 11111111, sum is 01111111 = 127 — YES OVERFLOW, two negatives summed to positive)
4. 00000000 (0, no overflow — this is -1 + 1 = 0, correct)
5. 10000000 (-128, YES OVERFLOW — 64 + 64 = 128, overflows to -128)

---

## Part 2: Bit Manipulation Reference Card

### The Essential Patterns

```c
/* === SINGLE BIT OPERATIONS === */

/* SET bit n: force bit n to 1 */
x |= (1u << n);

/* CLEAR bit n: force bit n to 0 */
x &= ~(1u << n);

/* TOGGLE bit n: flip bit n */
x ^= (1u << n);

/* TEST bit n: check if bit n is 1 */
int is_set = (x >> n) & 1;        /* result is 0 or 1 */
int is_set = !!(x & (1u << n));   /* alternative */

/* === MULTI-BIT (FIELD) OPERATIONS === */

/* EXTRACT bits [high..low] */
uint32_t mask = (1u << (high - low + 1)) - 1;
uint32_t field = (x >> low) & mask;

/* SET bits [high..low] to value */
uint32_t mask = (1u << (high - low + 1)) - 1;
x = (x & ~(mask << low)) | ((value & mask) << low);

/* === USEFUL TRICKS === */

/* Is x a power of 2? (x must be > 0) */
int pow2 = x && !(x & (x - 1));

/* Clear the lowest set bit */
x &= (x - 1);

/* Isolate the lowest set bit */
uint32_t lowest = x & (-x);       /* or x & (~x + 1) */

/* Round up to next power of 2 */
x--;
x |= x >> 1;
x |= x >> 2;
x |= x >> 4;
x |= x >> 8;
x |= x >> 16;
x++;

/* Count set bits (Kernighan's method) */
int count = 0;
while (x) {
    x &= (x - 1);    /* clears lowest set bit each time */
    count++;
}

/* Swap two variables without a temp (XOR swap) */
a ^= b;
b ^= a;
a ^= b;
/* Note: only works if a and b are different variables! */

/* Arithmetic right shift vs logical right shift */
int  signed_x   = -8;
int  arith_shr  = signed_x >> 1;    /* implementation-defined; usually -4 */
unsigned int u  = (unsigned int)signed_x;
unsigned int logical_shr = u >> 1;  /* defined: fills with 0s */

/* === MASK CONSTRUCTION === */
/* Mask of n ones:  (1u << n) - 1 */
uint32_t mask_4  = (1u << 4) - 1;   /* 0b00001111 = 0x0F */
uint32_t mask_8  = (1u << 8) - 1;   /* 0b11111111 = 0xFF */
uint32_t mask_16 = (1u << 16) - 1;  /* 0x0000FFFF */

/* Byte extraction */
uint8_t byte0 = (x >> 0)  & 0xFF;   /* least significant byte */
uint8_t byte1 = (x >> 8)  & 0xFF;
uint8_t byte2 = (x >> 16) & 0xFF;
uint8_t byte3 = (x >> 24) & 0xFF;   /* most significant byte */

/* Byte assembly */
uint32_t val = ((uint32_t)byte3 << 24) |
               ((uint32_t)byte2 << 16) |
               ((uint32_t)byte1 << 8)  |
               ((uint32_t)byte0 << 0);
```

### Common Bit Masks (Memorize These)

| Mask | Hex | Binary | Use |
|------|-----|--------|-----|
| Low nibble | `0x0F` | `00001111` | Extract/set bits 3-0 |
| High nibble | `0xF0` | `11110000` | Extract/set bits 7-4 |
| Low byte | `0xFF` | `11111111` | Extract/set byte 0 |
| Low 16 bits | `0xFFFF` | `0000...11111111` | Extract/set word |
| Alternating | `0x55555555` | `0101...` | Even bits |
| Alternating | `0xAAAAAAAA` | `1010...` | Odd bits |

### Bitwise Truth Tables

```
a | b | a&b | a|b | a^b | ~a
--+---+-----+-----+-----+----
0 | 0 |  0  |  0  |  0  |  1
0 | 1 |  0  |  1  |  1  |  1
1 | 0 |  0  |  1  |  1  |  0
1 | 1 |  1  |  1  |  0  |  0
```

**Memory aids:**
- AND: both must be 1 → use to **mask/clear** bits
- OR: either can be 1 → use to **set** bits
- XOR: must be different → use to **toggle/detect differences**
- NOT: flip everything → use to **invert a mask**

### Hex-Binary Quick Reference

```
0 = 0000    4 = 0100    8 = 1000    C = 1100
1 = 0001    5 = 0101    9 = 1001    D = 1101
2 = 0010    6 = 0110    A = 1010    E = 1110
3 = 0011    7 = 0111    B = 1011    F = 1111
```

One hex digit = 4 bits (one nibble). This is why hex is natural for binary data: `0xFF = 11111111`, `0xA5 = 10100101`.

---

## Part 3: Control Flow Reference

### Loop Selection Guide

```
Need to execute body at least once?
  YES → do-while
  NO  →
    Know the iteration count (or index-based)?
      YES → for
      NO  → while
```

### Loop Invariant Template

When writing a loop, document its invariant:

```c
/* INVARIANT: [describe what is true at the top of the loop body] */
/* EXAMPLE: max == maximum of arr[0..i-1] */
int max = arr[0];
int i = 1;
while (i < n) {
    /* Invariant holds here: max is max of arr[0..i-1] */
    if (arr[i] > max) max = arr[i];
    i++;
    /* Invariant holds here: max is max of arr[0..i-1] (now i is one larger) */
}
/* Loop exit: i == n */
/* Invariant + exit: max is max of arr[0..n-1] = max of whole array */
```

### Common Loop Bugs Checklist

Before submitting any loop, ask:
- [ ] **Off-by-one:** Is the loop condition `< n` or `<= n`? Which is correct?
- [ ] **Infinite loop:** Does the loop variable always move toward termination?
- [ ] **Uninitialized:** Is the accumulator initialized before the loop?
- [ ] **Empty input:** What happens if n = 0?
- [ ] **Single element:** What happens if n = 1?
- [ ] **Overflow:** Can the accumulator overflow? Is it the right type?
- [ ] **Side effects in condition:** Is the condition free of side effects?

---

## Part 4: Type Conversion Quick Reference

### Conversion Hierarchy (automatic promotions go upward)

```
long double
    ↑
double
    ↑
float
    ↑
unsigned long long / long long
    ↑
unsigned long / long
    ↑
unsigned int / int
    ↑
unsigned short / short (these are first promoted to int)
    ↑
unsigned char / char / signed char (these are first promoted to int)
```

### Safe Comparison Rule

Mixing signed and unsigned in a comparison is dangerous:
```c
int    i = -1;
unsigned u = 1;
if (i < u)      // WRONG: i is converted to unsigned → (UINT_MAX < 1) → false!
    ...

/* SAFE: cast to signed */
if (i < (int)u)   // OK if u fits in int
```

**Rule of thumb:** Prefer signed integers for arithmetic. Use unsigned only for:
1. Bit manipulation
2. Sizes and counts (where negative is meaningless)
3. Hash values and CRC values
4. When you explicitly need modular arithmetic

---

## Part 5: Recommended Tools for Week 1

### Compiler Explorer (godbolt.org)
- Type C code → see assembly output in real time
- Compare -O0 vs -O2 optimization
- Try different compilers (GCC, Clang)
- **This week:** Paste your loops and see exactly what the compiler generates

### Python as a Binary Calculator
When checking your two's complement arithmetic:
```python
>>> bin(42)              # '0b101010'
>>> bin(-42 & 0xFF)      # See 8-bit two's complement of -42: '0b11010110'
>>> int('11010110', 2)   # Convert binary string to decimal: 214
>>> 214 - 256            # Interpret as signed 8-bit: -42
```

### C Program for Bit Visualization
```c
void show_bits(unsigned int x) {
    printf("0x%08X = ", x);
    for (int i = 31; i >= 0; i--) {
        printf("%d", (x >> i) & 1);
        if (i % 8 == 0 && i > 0) printf(" ");
    }
    printf(" (%u)\n", x);
}
```
