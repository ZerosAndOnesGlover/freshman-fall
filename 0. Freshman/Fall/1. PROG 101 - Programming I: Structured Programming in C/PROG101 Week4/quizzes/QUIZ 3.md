# PROG 101 · Quiz 3
## Week 4, Tuesday — In-Class Assessment

**Administered:** start of Week 4, Lecture 1 (Tuesday)
**Covers:** Week 3 material
**Duration:** 10 minutes · Closed book · 20 points

---

## Section A — Multiple Choice (2 pts each)

**1.** What does `*p++` do (where `p` is an `int *`)?

- (A) Increments the value pointed to by `p`, then returns it
- (B) Dereferences `p` to get the value, then increments the pointer `p`
- (C) Increments `p` first, then dereferences the new location
- (D) This is undefined behavior

---

**2.** What is wrong with this function?

```c
int *get_answer(void) {
    int x = 42;
    return &x;
}
```

- (A) You cannot return a pointer from a function
- (B) `x` is destroyed when the function returns — the returned pointer is dangling
- (C) `&x` requires a cast to `int *` before returning
- (D) Nothing — this is valid C

---

**3.** After `free(p)`, which statement is correct?

- (A) `p` is automatically set to `NULL`
- (B) The memory is immediately zeroed out
- (C) `p` still holds the old address, but accessing `*p` is undefined behavior
- (D) The program aborts if you try to use `p` again

---

**4.** What does `malloc` return if it cannot allocate the requested memory?

- (A) A pointer to zeroed memory of the largest available block
- (B) `NULL`
- (C) `-1` cast to a pointer
- (D) It aborts the program with an error message

---

**5.** Which is the correct comparator for sorting `int` values in ascending order with `qsort`?

```c
/* Option A */
int cmp(const void *a, const void *b) { return (int)a - (int)b; }

/* Option B */
int cmp(const void *a, const void *b) { return *(int*)a - *(int*)b; }

/* Option C */
int cmp(const void *a, const void *b) {
    int x = *(int*)a, y = *(int*)b;
    return (x > y) - (x < y);
}

/* Option D */
int cmp(const void *a, const void *b) { return a - b; }
```

- (A) Option A
- (B) Option B
- (C) Option C
- (D) Both B and C are correct

---

## Section B — Short Answer (2 pts each)

**6.** What is the output? Trace carefully.

```c
int a = 1, b = 2, c = 3;
int *p = &a;
int *q = &c;

*p = 10;
p = &b;
*p += *q;

printf("%d %d %d\n", a, b, c);
```

Output: `______________________`

Show your trace:

---

**7.** Explain the difference between these two declarations:

```c
const int *p;
int * const p;
```

```
const int *p:   ___________________________________________________

int * const p:  ___________________________________________________
```

---

**8.** How many bytes does `malloc(n * sizeof(int))` allocate if `n = 10` on a system where `sizeof(int) = 4`? What value must you check in the return value, and what should you do if that check fails?

```
Bytes allocated: ______

Check: ____________________________________________________________

Action on failure: ________________________________________________
```

---

**9.** What is the bug in this code, and what error would Valgrind report?

```c
int main(void) {
    int *arr = malloc(5 * sizeof(int));
    for (int i = 0; i <= 5; i++)
        arr[i] = i;
    free(arr);
    return 0;
}
```

Bug: `______________________________________________________________`

Valgrind error type: `_____________________________________________`

---

**10.** Write a function `void swap(int *a, int *b)` that swaps the values at two pointer locations. Then show how to call it to swap variables `x` and `y`:

```c
/* Function: */
void swap(int *a, int *b) {



}

/* Call site: */
int x = 5, y = 9;

```

---

## Answer Key (Instructor Copy)

**1. (B)** — Postfix `++` has higher precedence than `*`. So `*p++` is `*(p++)`: the pointer `p` is incremented (as a side effect), but the dereference uses the original value of `p`. Net effect: read the current value, then advance the pointer. Very common in string/array iteration idioms.

**2. (B)** — `x` is a local variable on the stack of `get_answer`. When the function returns, its stack frame is popped and `x` ceases to exist. The returned pointer points to dead stack memory — a dangling pointer. Using it is undefined behavior (the memory will be reused by the next function call).

**3. (C)** — `free` returns the memory to the allocator but does not zero `p` or set it to NULL. `p` retains its old address value, but the memory it points to may have been given to another `malloc` call. Accessing `*p` after `free` is undefined behavior — it may read another allocation's data, corrupt it, or crash. Always set `p = NULL` after `free`.

**4. (B)** — `malloc` returns `NULL` on failure. It never aborts, never returns partial memory. The calling code is responsible for checking. Failing to check leads to a null pointer dereference crash when you try to use the result.

**5. (C)** — Option B is almost correct but has integer overflow risk: if `a = INT_MIN` and `b = 1`, then `*(int*)a - *(int*)b` overflows. Option C's `(x > y) - (x < y)` is branchless and overflow-safe: returns -1 if x<y, 0 if equal, 1 if x>y. Both B and C give correct sorting results for values that don't overflow, but C is the strictly correct answer. Answer D (D = both B and C) is accepted for partial credit.

**6.** Output: `10 5 3`
- `*p = 10` → `a = 10` (p points to a)
- `p = &b` → p now points to b  
- `*p += *q` → `b += c` → `b = 2 + 3 = 5`
- `a=10, b=5, c=3`

**7.**
- `const int *p`: pointer to const int — `p` can be changed to point elsewhere, but `*p` cannot be written through (the int it points to is read-only via this pointer)
- `int * const p`: const pointer to int — `p` cannot be changed to point elsewhere, but `*p` can be written (the int itself is modifiable)

**8.**
- Bytes: `10 × 4 = 40 bytes`
- Check: whether the return value is `NULL`
- Action: handle the error (print message, exit, or propagate error to caller) — never dereference a NULL pointer

**9.**
- Bug: loop condition `i <= 5` causes `arr[5] = 5` — writing to index 5 of a 5-element array (valid indices 0–4). This writes one `int` (4 bytes) past the end of the allocation.
- Valgrind error: **"Invalid write of size 4"** (heap buffer overrun / out-of-bounds write)

**10.**
```c
void swap(int *a, int *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int x = 5, y = 9;
swap(&x, &y);   /* x = 9, y = 5 */
```
