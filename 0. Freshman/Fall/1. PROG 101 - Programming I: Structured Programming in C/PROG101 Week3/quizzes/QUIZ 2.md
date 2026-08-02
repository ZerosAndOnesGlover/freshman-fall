# PROG 101 — Quiz 2
## Week 3, Tuesday — In-Class Assessment

**Administered:** start of Week 3, Lecture 1 (Tuesday)
**Covers:** Week 2 material
**Duration:** 10 minutes · Closed book · 20 points

---

## Section A — Multiple Choice (2 pts each)

**1.** A function receives a `char buffer[64]` as a parameter. Inside the function, what does `sizeof(buffer)` return?

- (A) 64
- (B) 1 (size of one char)
- (C) 8 (size of a pointer on 64-bit systems)
- (D) The actual length of the string stored in the buffer

---

**2.** What is the output of this code?

```c
void modify(int x) { x = 999; }
int main(void) {
    int a = 42;
    modify(a);
    printf("%d\n", a);
    return 0;
}
```

- (A) 999
- (B) 42
- (C) Undefined behavior
- (D) 0

---

**3.** What does `strlen("Hello\0World")` return?

- (A) 11
- (B) 10
- (C) 5
- (D) 6

---

**4.** Which statement correctly declares a function that takes a 2D array with 4 columns and returns nothing?

- (A) `void fn(int matrix[][], int rows);`
- (B) `void fn(int matrix[4][], int rows);`
- (C) `void fn(int matrix[][4], int rows);`
- (D) `void fn(int **matrix, int rows, int cols);`

---

**5.** A `static` local variable inside a function:

- (A) Is allocated on the stack and destroyed when the function returns
- (B) Is allocated in the data segment, initialized once, and persists between calls
- (C) Is the same as a `const` local variable
- (D) Cannot be read by the function on the second call

---

## Section B — Short Answer (2 pts each)

**6.** What is the exact content (every byte) stored in memory for this declaration?

```c
char s[] = "Hi!";
```

Write each character and its ASCII value in order:

```
Byte 0: char='__', ASCII=__
Byte 1: char='__', ASCII=__
Byte 2: char='__', ASCII=__
Byte 3: char='__', ASCII=__
Total bytes: __
```

---

**7.** This code has a bug. Identify it and explain the consequence:

```c
void fill(int arr[], int n, int value) {
    for (int i = 0; i <= n; i++) {
        arr[i] = value;
    }
}

int main(void) {
    int data[5];
    fill(data, 5, 0);
    return 0;
}
```

Bug: `_____________________________________________________`

Consequence: `________________________________________________`

Fix: `_______________________________________________________`

---

**8.** What does `strcmp("apple", "banana")` return — positive, negative, or zero? Why?

```
Return value: ______ (positive / negative / zero)
Why: ___________________________________________________________
```

---

**9.** Draw the call stack (frames from top to bottom, newest first) at the moment execution is inside `leaf()`:

```c
void leaf(void)     { /* HERE */ }
void middle(void)   { leaf(); }
void root(void)     { middle(); }
int main(void)      { root(); return 0; }
```

```
Stack (top = most recent):
┌──────────────────┐
│                  │  ← newest frame
├──────────────────┤
│                  │
├──────────────────┤
│                  │
├──────────────────┤
│                  │  ← oldest frame
└──────────────────┘
```

---

**10.** What is wrong with this approach to copying a string into a buffer, and what is the safe alternative?

```c
char src[] = "This is a very long string that might overflow the buffer";
char dest[10];
strcpy(dest, src);
```

Problem: `__________________________________________________`

Safe alternative (write the corrected code): 
```c



```

---

## Answer Key (Instructor Copy)

**1. (C) 8** — When an array is passed to a function, it decays to a pointer. The parameter `char buffer[64]` is actually `char *buffer` — a pointer, 8 bytes on 64-bit. `sizeof` gives the size of the pointer, not the array. This is one of C's most notorious gotchas.

**2. (B) 42** — Pass by value: `modify` receives a copy of `a`. Modifying `x` inside `modify` has no effect on `a` in `main`. The copy lives on `modify`'s stack frame and is discarded when the function returns.

**3. (C) 5** — `strlen` counts bytes until the first `'\0'`. The string `"Hello\0World"` has `'\0'` at position 5. `strlen` stops there and returns 5. The `"World"` part is in memory but invisible to `strlen`.

**4. (C) `void fn(int matrix[][4], int rows)`** — The first dimension can be omitted (it's passed separately as `rows`), but all subsequent dimensions must be specified so the compiler can compute element addresses. `matrix[i][j]` = `*(matrix + i*4 + j)`, which requires knowing 4 at compile time.

**5. (B) Data segment, initialized once, persists** — Static locals are like globals in storage duration but with local scope. They live in the data segment (not the stack), initialized exactly once (at program startup, to 0 if not explicitly initialized), and retain their value across calls. The function can read and modify them normally.

**6.**
```
Byte 0: char='H', ASCII=72
Byte 1: char='i', ASCII=105
Byte 2: char='!', ASCII=33
Byte 3: char='\0', ASCII=0
Total bytes: 4
```
The null terminator is always allocated and stored. `sizeof("Hi!")` = 4, `strlen("Hi!")` = 3.

**7.** Bug: loop condition is `i <= n` — should be `i < n`. With `n=5` and an array of size 5 (valid indices 0-4), the loop writes to `arr[5]` on the last iteration — one element past the end of the array. Consequence: undefined behavior — writes to memory just past the array, potentially corrupting an adjacent variable or the return address. Fix: change `i <= n` to `i < n`.

**8.** Negative. `strcmp` compares character by character. The first characters are `'a'` (97) and `'b'` (98). Since `'a'` < `'b'`, `strcmp` returns a negative value (specifically `'a' - 'b'` = `-1` in the implementation we studied, though the standard only guarantees the sign). "apple" comes before "banana" alphabetically.

**9.**
```
Stack (top = most recent):
┌──────────────────┐
│  leaf()          │  ← newest frame (currently executing)
├──────────────────┤
│  middle()        │
├──────────────────┤
│  root()          │
├──────────────────┤
│  main()          │  ← oldest frame
└──────────────────┘
```

**10.** Problem: `strcpy` has no length limit. It copies all bytes of `src` (57 characters + null = 58 bytes) into `dest` (10 bytes), overflowing the buffer by 48 bytes. This overwrites adjacent memory — undefined behavior, likely a crash or security vulnerability.

Safe alternative:
```c
char src[] = "This is a very long string that might overflow the buffer";
char dest[10];
snprintf(dest, sizeof(dest), "%s", src);
/* Or: */
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';   /* strncpy doesn't guarantee null-termination */
```
`snprintf` is preferred — it always null-terminates and is harder to misuse.
