# PROG 101 · Programming I: Structured Programming in C
## Week 4 · Lecture 1: Arrays — The First Data Structure

**Date:** Tuesday 15 September 2026 · 10:00–10:50 · Week 4

---

## Lecture Goals

By the end of this lecture you will:
- Understand arrays as contiguous memory blocks, not abstract containers
- Know why array indexing starts at 0 (it is not arbitrary)
- Pass arrays to functions correctly
- Understand multidimensional arrays and row-major layout
- Know about strings as null-terminated character arrays
- Identify and avoid buffer overflows

---

## 1. What Is an Array?

An array is a **contiguous block of memory** holding multiple values of the same type.

When you declare:
```c
int arr[5];
```

The compiler allocates `5 × sizeof(int)` = `5 × 4` = **20 contiguous bytes** on the stack and associates the name `arr` with the address of the first byte.

```
Memory layout of int arr[5]:
                                                    
Address: 1000  1004  1008  1012  1016
         ┌─────┬─────┬─────┬─────┬─────┐
         │arr[0]│arr[1]│arr[2]│arr[3]│arr[4]│
         └─────┴─────┴─────┴─────┴─────┘
         ↑
         arr (the name 'arr' refers to this address)
```

This layout is not incidental — it is the defining property of an array. Elements are adjacent in memory with no gaps between them.

---

## 2. Why Indexing Starts at 0

This confuses beginners. There is a precise reason.

`arr[i]` is not magic syntax — it is equivalent to `*(arr + i)`:

```
arr[i] computes: address_of_arr + i * sizeof(element_type)
```

So `arr[0]` = `address_of_arr + 0 * 4` = `address_of_arr` — the first element.
`arr[1]` = `address_of_arr + 1 * 4` — 4 bytes past the first element.
`arr[i]` = `address_of_arr + i * 4` — i elements past the first.

If indexing started at 1, `arr[1]` would compute `address + 0 * sizeof` = `address` — the first element. But `arr[n]` would need `address + (n-1) * sizeof`. The formula is more complex.

**With 0-based indexing:** `arr[i]` = `address + i * size` — elegant, simple, maps directly to hardware.

This is not a historical accident. Dijkstra wrote a famous note arguing that 0-based indexing is the mathematically natural choice. Every CPU instruction set uses 0-based offset addressing.

---

## 3. Array Declaration and Initialization

```c
/* Uninitialized — contains garbage (stack allocation) */
int arr[5];

/* Initialized with explicit values */
int primes[5] = {2, 3, 5, 7, 11};

/* Partial initialization — unspecified elements are zero */
int arr2[5] = {1, 2};    /* {1, 2, 0, 0, 0} */

/* Zero-initialize all elements */
int zeros[100] = {0};    /* All 100 elements set to 0 */
int also_zeros[100] = {}; /* C99: same effect */

/* Compiler determines size from initializer */
int auto_size[] = {10, 20, 30, 40};   /* size = 4, inferred */

/* Designated initializers (C99) */
int sparse[10] = {[0] = 1, [5] = 42, [9] = 100};
/* Unspecified elements are 0 */

/* Character array (string) */
char greeting[] = "Hello";   /* {'H','e','l','l','o','\0'} — 6 bytes */
char greeting2[6] = "Hello"; /* Same, explicit size */
```

### The Array Length Macro

```c
/* Get the number of elements — use this instead of hardcoding */
#define ARRAY_LEN(arr) (sizeof(arr) / sizeof((arr)[0]))

int primes[] = {2, 3, 5, 7, 11};
printf("Length: %zu\n", ARRAY_LEN(primes));   /* 5 */
```

This works because `sizeof(arr)` gives total bytes, and `sizeof(arr[0])` gives bytes per element.

**CRITICAL:** This only works when `arr` is an actual array declaration — not a pointer to an array. We'll see why in Lecture 3 (pointers).

---

## 4. Accessing and Iterating Arrays

```c
int scores[5] = {88, 72, 95, 61, 84};

/* Read an element */
int first = scores[0];    /* 88 */
int last  = scores[4];    /* 84 */

/* Write an element */
scores[2] = 100;

/* Iterate — the standard pattern */
int n = ARRAY_LEN(scores);
for (int i = 0; i < n; i++) {
    printf("scores[%d] = %d\n", i, scores[i]);
}

/* Common operations */

/* Sum */
int sum = 0;
for (int i = 0; i < n; i++) sum += scores[i];

/* Maximum */
int max = scores[0];
for (int i = 1; i < n; i++)
    if (scores[i] > max) max = scores[i];

/* Reverse in-place */
for (int i = 0, j = n-1; i < j; i++, j--) {
    int tmp = scores[i];
    scores[i] = scores[j];
    scores[j] = tmp;
}
```

---

## 5. The Bounds Check That C Does Not Do

C **never** checks array bounds at runtime. If you access `arr[10]` on an array of 5 elements, the compiler generates code that reads or writes memory 10 elements past the start of `arr` — whatever happens to be there.

```c
int arr[5] = {1, 2, 3, 4, 5};
printf("%d\n", arr[5]);     /* Out of bounds: undefined behavior */
printf("%d\n", arr[-1]);    /* Out of bounds: undefined behavior */
arr[5] = 99;                /* Writes to memory beyond arr — may corrupt
                               another variable, the return address, etc. */
```

This is the **buffer overflow** — the most exploited class of vulnerability in C programs. Writing past the end of an array can:
- Corrupt adjacent variables (producing wrong results)
- Overwrite the function's return address (allowing code injection)
- Crash the program with a segmentation fault

**The rule:** Always ensure your loop bounds are correct. Always pass the array size to any function that takes an array. Use AddressSanitizer during development:

```bash
gcc -fsanitize=address -g program.c
./a.out   # Immediately reports out-of-bounds accesses with exact location
```

---

## 6. Passing Arrays to Functions

Here is one of C's most important and confusing rules:

**When you pass an array to a function, it decays to a pointer to its first element.**

```c
void print_array(int arr[], int n) {
    /* Inside here, arr is a POINTER (int *), not an array */
    /* sizeof(arr) would give sizeof(int *) = 8, not sizeof the array */
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main(void) {
    int scores[5] = {88, 72, 95, 61, 84};
    print_array(scores, 5);   /* Passes pointer to scores[0], and the count */
    return 0;
}
```

This is why you **always pass the array size separately**. The function cannot determine the array length from the pointer alone.

The two declarations below are **identical** — both receive a pointer:
```c
void fn(int arr[], int n);    /* Looks like an array, is really a pointer */
void fn(int *arr, int n);     /* Explicit pointer — same meaning */
```

We will understand the pointer mechanics fully in Week 5. For now, follow the rule: **always pass the length**.

### Modifying Arrays in Functions

Because the function receives a pointer to the original array (not a copy), modifications inside the function **do** affect the original:

```c
void fill_zeros(int arr[], int n) {
    for (int i = 0; i < n; i++)
        arr[i] = 0;   /* Modifies the original array through the pointer */
}

int main(void) {
    int data[5] = {1, 2, 3, 4, 5};
    fill_zeros(data, 5);
    /* data is now {0, 0, 0, 0, 0} */
    return 0;
}
```

This is the exception to pass-by-value. Arrays are not copied — a pointer is passed. This is efficient (no copying 1000-element arrays), but means the function can modify your data.

---

## 7. Multidimensional Arrays

A 2D array in C is an array of arrays:

```c
int matrix[3][4];   /* 3 rows, 4 columns — 12 ints total, 48 bytes */
```

Memory layout — **row-major order**:
```
matrix[0][0] matrix[0][1] matrix[0][2] matrix[0][3]
matrix[1][0] matrix[1][1] matrix[1][2] matrix[1][3]
matrix[2][0] matrix[2][1] matrix[2][2] matrix[2][3]
```

All 12 elements are stored contiguously in memory, row by row.

```c
/* Initialization */
int matrix[3][4] = {
    {1,  2,  3,  4},    /* row 0 */
    {5,  6,  7,  8},    /* row 1 */
    {9, 10, 11, 12}     /* row 2 */
};

/* Access: row i, column j */
int val = matrix[1][2];   /* row 1, col 2 = 7 */

/* Iterate all elements */
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 4; j++) {
        printf("%3d ", matrix[i][j]);
    }
    printf("\n");
}
```

### Row-Major Order and Cache Performance

Because rows are contiguous in memory, iterating row-by-row is **cache-friendly**:

```c
/* FAST: accesses matrix row by row — sequential memory access */
int sum = 0;
for (int i = 0; i < ROWS; i++)
    for (int j = 0; j < COLS; j++)
        sum += matrix[i][j];

/* SLOW: accesses matrix column by column — jumps COLS*sizeof(int) bytes each step */
int sum = 0;
for (int j = 0; j < COLS; j++)
    for (int i = 0; i < ROWS; i++)
        sum += matrix[i][j];
```

For large matrices, the cache-friendly version can be 10× faster because it avoids cache misses. This is not theoretical — it is measurable.

### Passing 2D Arrays to Functions

```c
/* Must specify all dimensions except the first */
void print_matrix(int matrix[][4], int rows) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < 4; j++)
            printf("%3d ", matrix[i][j]);
        printf("\n");
    }
}

/* Called with: */
print_matrix(matrix, 3);
```

The compiler needs all dimensions except the first to compute element addresses. This is an important limitation — for fully generic 2D array functions, we need pointers (Week 5).

---

## 8. Strings: Arrays of Characters

In C, a string is simply a `char` array with a **null terminator** (`'\0'`) at the end:

```c
char name[] = "Alice";
/* Stored as: {'A', 'l', 'i', 'c', 'e', '\0'} — 6 bytes, not 5 */
```

The null terminator is how C functions know where the string ends. `strlen("Alice")` walks the array byte by byte until it finds `'\0'`, counting steps.

### Key String Operations

```c
#include <string.h>

char s1[] = "Hello";
char s2[20];

/* Length — does NOT include the null terminator */
size_t len = strlen(s1);    /* 5, not 6 */

/* Copy — DANGEROUS without bounds checking */
strcpy(s2, s1);             /* Copies "Hello\0" into s2 */
strncpy(s2, s1, sizeof(s2)); /* Safer: limits to sizeof(s2) chars */

/* Concatenate */
strcat(s2, " World");       /* s2 becomes "Hello World" — must have room! */
strncat(s2, " World", sizeof(s2) - strlen(s2) - 1);  /* Safer */

/* Compare */
int cmp = strcmp(s1, "Hello");   /* 0 if equal, <0 or >0 otherwise */
/* Do NOT use s1 == "Hello" — this compares addresses, not contents! */

/* Search */
char *p = strchr(s1, 'l');   /* Pointer to first 'l', or NULL if not found */
char *q = strstr(s1, "ll");  /* Pointer to first "ll", or NULL */
```

### The Buffer Overflow Classic

```c
char buffer[8];
/* User types "Hello World" — 11 chars + null = 12 bytes into an 8-byte buffer */
scanf("%s", buffer);   /* DANGEROUS: no length limit */

/* strcpy overflows similarly: */
char buf[5];
strcpy(buf, "Hello World");   /* Writes 12 bytes into a 5-byte buffer — CRASH */
```

The fix: always know your buffer size and enforce it:
```c
char buffer[8];
scanf("%7s", buffer);            /* Read at most 7 chars + null = 8 bytes max */
fgets(buffer, sizeof(buffer), stdin);   /* Preferred: reads a full line safely */
```

### String Literals

```c
char *s = "Hello";    /* s points to a string literal in read-only memory */
s[0] = 'h';           /* UNDEFINED BEHAVIOR: modifying read-only memory */

char arr[] = "Hello"; /* arr is a local array initialized with "Hello" */
arr[0] = 'h';         /* OK: arr is a modifiable copy */
```

Always use `char arr[] = "..."` when you need to modify a string. Use `const char *s = "..."` when you won't.

---

## 9. Variable-Length Arrays (VLAs) — Use with Caution

C99 allows arrays whose size is determined at runtime:

```c
void process(int n) {
    int arr[n];    /* VLA: size determined by n at runtime */
    /* ... */
}
```

VLAs are allocated on the stack. They are useful but:
- Cannot be initialized with an initializer list
- Size cannot be 0 (undefined behavior)
- Large VLAs can cause stack overflow
- C11 made them optional (some compilers disable them)

**Recommendation:** For small, known-size arrays, use fixed-size arrays. For large or truly variable-size data, use dynamic allocation (`malloc` — Week 9).

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict both printed sizes and explain the difference.

```c
#include <stdio.h>
void show(int a[10]) {
    printf("inside: %zu\n", sizeof a);
}
int main(void) {
    int a[10];
    printf("main:   %zu\n", sizeof a);
    show(a);
    return 0;
}
```

**2. (Explain.)** C performs no bounds checking. Explain what actually happens on `a[15]` for `int a[10]`, why it may not crash, and what tool you should use to catch it.

**3. (Build.)** Write functions to (a) sum an `int` array, (b) find its maximum, and (c) reverse it in place. Each must take the length explicitly. Explain your `const` choices.

**4. (Stretch.)** Explain how a 2D array `int m[3][4]` is laid out in memory. Then explain why `void f(int m[][4])` compiles but `void f(int m[][])` does not.


### Answers

**1.**

```
main:   40
inside: 8
```

In `main`, `a` is a genuine array of 10 `int`s, so `sizeof a` is 40.

Inside `show` it is **8** — the size of a pointer. This is **array decay**: an array used as a function argument is converted to a pointer to its first element. The parameter declaration `int a[10]` is a lie the compiler accepts and silently rewrites to `int *a`; the `10` is ignored entirely, and `void show(int a[999])` behaves identically. GCC warns with `-Wsizeof-array-argument`.

The consequence is the central fact about C arrays: **a function receiving an array cannot know its length.** The idiom `sizeof a / sizeof a[0]` works only in the scope where the array was declared. So every array-taking function must accept the length explicitly:

```c
void show(const int *a, size_t n);
```

Decay also explains why `a` and `&a[0]` are interchangeable, why `a[i]` is defined as `*(a + i)` — and hence why the bizarre `2[a]` is legal and equals `a[2]`, since addition commutes. Note `&a` is *not* the same: it has type `int (*)[10]` and `&a + 1` skips 40 bytes, not 4.

**2.** `a[15]` compiles to `*(a + 15)` — the address of `a` plus 60 bytes — and the CPU reads or writes there unconditionally. Nothing checks the index because **nothing knows the length**; the array's size exists only at compile time in the declaring scope, and even there C chooses not to spend the instruction.

It usually does not crash because those 60 bytes are almost certainly still inside your process's mapped memory — other locals, the saved frame pointer, padding. A segfault requires touching an *unmapped page*, which needs a much wilder index. So the realistic outcome is **silent corruption**: another variable changes value for no visible reason, and the symptom appears far from the cause. Writing past a local array onto the saved return address is the mechanism behind stack-smashing exploits.

**Use AddressSanitizer:**

```bash
gcc -fsanitize=address -g prog.c -o prog
./prog
```

ASan places poisoned *redzones* around every allocation and reports the exact line, the array, and the offset the moment the access happens — turning an invisible corruption into a precise diagnostic. It costs about 2× runtime, which is nothing during development.

Valgrind's memcheck finds heap overruns well but is weak on stack arrays; ASan covers both. Use `-fsanitize=address,undefined` as your default debug build in this course.

**3.**

```c
#include <stddef.h>

long sum(const int *a, size_t n) {
    long total = 0;
    for (size_t i = 0; i < n; i++) total += a[i];
    return total;
}

int max(const int *a, size_t n) {          /* precondition: n > 0 */
    int best = a[0];
    for (size_t i = 1; i < n; i++)
        if (a[i] > best) best = a[i];
    return best;
}

void reverse(int *a, size_t n) {
    for (size_t i = 0, j = n - 1; i < j; i++, j--) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
}
```

`sum` and `max` take **`const int *`** because they only read. This is not decoration: it documents the contract in the signature, lets the compiler reject an accidental write, and — practically — allows callers to pass a `const` array. `reverse` mutates, so it cannot be `const`.

`sum` returns **`long`**, not `int`: summing 10,000 values near `INT_MAX` overflows a 32-bit result, and signed overflow is undefined behaviour rather than a wrap.

`reverse` is safe on `n == 0` despite `n - 1` wrapping to `SIZE_MAX`, because `i < j` is then `0 < SIZE_MAX`… which is **true** — so it would run and read out of bounds. Add `if (n == 0) return;`, or write the loop as `for (size_t i = 0; i + 1 < n - i; i++)`. This is exactly the unsigned-underflow trap from Week 1, and it is worth the guard.

**4.** `int m[3][4]` is **row-major and fully contiguous**: 12 `int`s in one block, laid out as `m[0][0] m[0][1] m[0][2] m[0][3] m[1][0] …`. There are no pointers anywhere — it is not an array of pointers to rows, which is what `int **` would be, and the two are not interchangeable.

The address of `m[i][j]` is `base + (i * 4 + j) * sizeof(int)`. Note the compiler needs the **column count** to compute this, and does not need the row count at all.

That asymmetry is the whole answer to the second question. `int m[][4]` decays to `int (*)[4]` — pointer to an array of 4 `int`s — and stepping it by one advances 16 bytes, which is exactly what indexing needs. `int m[][]` would decay to a pointer to an array of *unknown* size, so `m[i]` has no computable stride and the type is incomplete. **The first dimension may be omitted; no later one may.**

One practical consequence: because rows are adjacent, iterating `for i { for j { m[i][j] } }` walks memory sequentially and is cache-friendly, while swapping the loops strides by 16 bytes and can be several times slower on a large matrix. Same operations, same complexity, very different runtime — the locality point from CS 101 L23, made concrete.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Array** | Contiguous block of memory holding elements of the same type |
| **Index** | 0-based offset of an element from the start of the array |
| **Array decay** | Arrays convert to pointers to their first element when used in expressions |
| **Null terminator** | `'\0'` byte that marks the end of a C string |
| **Buffer overflow** | Writing past the end of an array — undefined behavior |
| **Row-major order** | 2D array stored row by row — consecutive row elements are adjacent in memory |
| **VLA** | Variable-Length Array — size determined at runtime (C99) |

---

## Reading

- **K&R Chapter 5** — §5.1–5.3 (Pointers and Addresses) — starts explaining why arrays work the way they do
- **K&R Chapter 6** — Strings (character arrays) — all of it
- **King Ch. 8** — Arrays
- **King Ch. 13** — Strings

---

*Next: Lecture 3 — Strings in Depth: Processing, Searching, and Building*
