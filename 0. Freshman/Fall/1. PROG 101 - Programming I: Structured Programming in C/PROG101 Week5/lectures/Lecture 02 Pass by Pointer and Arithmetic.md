# PROG 101 · Programming I: Structured Programming in C
## Week 5 · Lecture 2: Pass-by-Pointer and Pointer Arithmetic

---

## Lecture Goals

By the end of this lecture you can:

- Use pointer parameters to let a function modify its caller's variables
- Predict exactly how far `p + 1` moves, for any pointer type
- Explain the relationship between arrays and pointers, including where it breaks down
- Say why `&arr` and `&arr[0]` are the same address but different types

---

## 1. Write-Back: The First Reason Pointers Exist

Week 3 established that C passes **everything** by value. A function receives copies, so this cannot
work:

```c
void swap_bad(int a, int b) { int t = a; a = b; b = t; }

int x = 1, y = 2;
swap_bad(x, y);
```

Verified: `after swap_bad: x=1 y=2` — **unchanged**. The function swapped its own two copies and
then discarded them.

Pass the addresses instead:

```c
void swap_ok(int *a, int *b) { int t = *a; *a = *b; *b = t; }

swap_ok(&x, &y);
```

Verified: `after swap_ok: x=2 y=1` — **swapped**.

Nothing about pass-by-value changed. `swap_ok` still receives copies — copies of two *addresses*. But
a copy of an address points at the same object the original did, so writing through it reaches the
caller's variable.

> **The rule, stated once:** to let a function modify a `T` belonging to the caller, pass a `T *`.
> This is the whole of it, and it scales — Week 5 Lecture 1's `int **` is just this rule applied when
> `T` is itself `int *`.

### The other write-back idiom: returning two things

C functions return one value. When you need two, one comes back through a pointer:

```c
int divide(int a, int b, int *remainder)
{
    if (b == 0) return -1;          /* error signalled by return value */
    *remainder = a % b;             /* second result via pointer       */
    return a / b;
}
```

This shape — status as the return value, results through output pointers — is pervasive in C and in
every OS API you will meet.

### Avoiding copies

A second reason to pass a pointer: a large struct copied by value costs real time.

```c
void process(const struct Record *r);   /* passes 8 bytes, not sizeof(Record) */
```

**Note the `const`.** It says "I need the address for efficiency, not because I intend to modify
anything." That distinction is worth stating in the type, and Lecture 3 covers how.

---

## 2. Pointer Arithmetic Scales by Type

This is the rule that makes pointers useful for arrays, and the one people get wrong.

**`p + 1` does not add one byte. It advances by one *element*.**

Verified:

```
int*    p, p+1 differ by 4 bytes
char*   p, p+1 differ by 1 bytes
double* p, p+1 differ by 8 bytes
```

The compiler multiplies by `sizeof(*p)` for you. So for `int a[4]`:

```c
int *p = a;
p + 0   /* &a[0] */
p + 1   /* &a[1] -- 4 bytes along */
p + 3   /* &a[3] */
```

The operations available:

| Expression | Meaning |
|---|---|
| `p + n`, `p - n` | Move `n` elements |
| `p++`, `p--` | Move one element |
| `p2 - p1` | **Number of elements** between them |
| `p1 < p2`, `p1 == p2` | Relational comparison |

Note there is no `p1 + p2` — adding two addresses is meaningless and does not compile.

### Difference yields elements, not bytes

Verified:

```
&ai[3] - &ai[0] = 3 elements   (not 12 bytes)
```

The type of that difference is `ptrdiff_t`, from `<stddef.h>`. Print it with `%td`.

This is the inverse of the scaling rule and it is consistent: if `+1` moves one element, then a
difference must count elements.

### Where arithmetic is legal

C permits pointer arithmetic **only within an array** (and one past its end). Specifically:

```c
int a[4];
int *p = a + 4;      /* LEGAL: one past the end -- may be compared, not dereferenced */
int *q = a + 5;      /* UNDEFINED BEHAVIOUR, even without dereferencing */
int *r = a - 1;      /* UNDEFINED BEHAVIOUR */
```

The "one past the end" allowance is what makes the standard loop idiom legal:

```c
for (int *p = a; p != a + 4; p++) ...
```

Forming `a + 4` is fine; dereferencing it is not. Going one *before* the start has no such
exemption — which is why a backwards loop must be written carefully:

```c
for (int *p = a + 4; p-- != a; ) ...    /* test-then-decrement, never forms a-1 */
```

---

## 3. Arrays and Pointers

The relationship is close enough to be confusing and different enough to matter.

### `a[i]` is defined as `*(a + i)`

Not "similar to" — *defined as*. The subscript operator is syntactic sugar for pointer arithmetic.

Verified, all four printing 30 for `int ai[4] = {10,20,30,40}`:

```
ai[2]=30   *(ai+2)=30   *(2+ai)=30   2[ai]=30
```

**`2[ai]` is legal C.** Since `a[i]` means `*(a+i)` and addition commutes, `i[a]` means `*(i+a)`,
which is the same thing. Never write it — but understanding why it compiles tells you the subscript
operator is not doing anything special.

### Decay

In most expressions, an array name **decays** to a pointer to its first element. That is why this
works:

```c
int a[4];
int *p = a;        /* no & needed: a decays to &a[0] */
```

And why array parameters are really pointers:

```c
void f(int a[10]);    /* the 10 is documentation; the parameter is int * */
void f(int a[]);      /* identical */
void f(int *a);       /* identical -- this is what all three mean */
```

**This is why `sizeof` inside a function lies.** Verified:

```
sizeof(ai) = 16   (the array, where it is declared)
sizeof(p)  = 8    (a pointer)
```

You met the consequence in Week 4: a function receiving a buffer must also receive its size, because
`sizeof` on the parameter gives 8.

### Where decay does *not* happen

Three contexts keep the array as an array:

| Context | Result |
|---|---|
| `sizeof a` | Size of the whole array |
| `&a` | Pointer **to the array**, type `int (*)[4]` |
| A string literal initialising an array | `char s[] = "hi";` copies, no decay |

The `&a` case produces the clearest demonstration. Verified:

```
&ai    = 0x7ffeb38fb2e0
&ai[0] = 0x7ffeb38fb2e0     <- same address
ai+1   = 0x7ffeb38fb2e4     (+4 bytes)
&ai+1  = 0x7ffeb38fb2f0     (+16 bytes = the whole array)
```

`&ai` and `&ai[0]` are the **same address with different types**. `ai + 1` moves one `int`; `&ai + 1`
moves one *array of four ints*. The arithmetic follows the type, exactly as §2 says — the types are
just less familiar.

### So is an array a pointer?

**No.** An array is a block of contiguous storage. A pointer is a variable holding an address. The
array *converts* to a pointer in most expressions, which is why they seem interchangeable, but:

- `sizeof` distinguishes them
- an array is not assignable (`a = b;` does not compile for arrays)
- `&a` has a different type from `&a[0]`

The decay is a conversion, not an identity.

---

## 4. Walking an Array

Two idioms, both correct:

```c
/* index */
for (size_t i = 0; i < n; i++) total += a[i];

/* pointer */
for (const int *p = a; p != a + n; p++) total += *p;
```

The pointer form was once meaningfully faster. **It is not any more** — compilers turn both into the
same machine code, and you should verify rather than assume if it matters. Choose on clarity: the
index form is usually clearer, and the pointer form reads better when you are advancing through a
buffer with no natural index.

Note `p != a + n` rather than `p < a + n`. Both work for arrays; `!=` expresses the intent (stop at
exactly this position) and is the convention that generalises to structures with no ordering, such as
linked lists.

---

## 5. Summary

| Idea | Takeaway |
|---|---|
| Everything is passed by value | Including pointers — but a copied address still points at the original |
| Write-back | To modify a caller's `T`, take a `T *` |
| Status + output pointers | The standard C shape for returning more than one thing |
| `p + 1` | Advances **one element**, scaled by `sizeof(*p)` — verified 4/1/8 bytes |
| `p2 - p1` | Yields **element count**, type `ptrdiff_t`, print with `%td` |
| Legal range | Within the array, plus one past the end; `a - 1` is UB |
| `a[i]` **is** `*(a + i)` | Which is why `2[a]` compiles |
| Decay | Array becomes a pointer to its first element in most expressions |
| Array parameters | `int a[10]`, `int a[]`, `int *a` are the same declaration |
| `sizeof(a)` vs `sizeof(p)` | 16 vs 8 — the reason functions need an explicit length |
| `&a` vs `&a[0]` | Same address, different types: `&a + 1` jumps the **whole array** |
| An array is not a pointer | It converts to one; `sizeof`, assignability and `&` all distinguish them |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** For `double d[5];` with `d` at address 1000, give the address of: (a) `d + 1`
(b) `&d[3]`  (c) `&d + 1`  (d) the value of `&d[4] - &d[1]`

**2. (Explain.)** Why does `sizeof(a)` give 40 inside `main` for `int a[10]`, but 8 inside
`void f(int a[10])`? Name the mechanism.

**3. (Fix.)** Three bugs.

```c
void scale(int a[], int n, int factor)
{
    for (int i = 0; i <= n; i++) a[i] *= factor;
}
int total(int a[]) { int s = 0; for (size_t i = 0; i < sizeof(a)/sizeof(a[0]); i++) s += a[i]; return s; }
```

**4. (Stretch.)** Write `void reverse(int *a, size_t n)` using **only pointers**, no integer indices.
Then explain why the obvious loop condition `left < right` is correct here but would be undefined
behaviour if you instead walked off the front of the array.

### Answers

**1.** `sizeof(double)` is 8, and the array is 5 × 8 = 40 bytes at address 1000.

| | Address / value | Why |
|---|---|---|
| **(a)** `d + 1` | **1008** | One `double` along |
| **(b)** `&d[3]` | **1024** | 1000 + 3 × 8 |
| **(c)** `&d + 1` | **1040** | `&d` has type `double (*)[5]`, so +1 moves the whole 40-byte array |
| **(d)** `&d[4] - &d[1]` | **3** | Difference is in **elements**, not bytes (24 bytes / 8) |

(c) is the discriminating one. If you answered 1008, you treated `&d` as `double *`; it is not.

**2.** The mechanism is **array-to-pointer decay** in the parameter declaration.

Inside `main`, `a` names an actual array object of 10 `int`s, so `sizeof` reports its real extent: 40.

In a parameter list, C **adjusts** the declared type: `int a[10]` becomes `int *a`. The `10` is
discarded entirely — it is documentation for the reader and nothing more. So `sizeof(a)` inside `f`
is `sizeof(int *)`, which is 8 on this machine and 4 on a 32-bit build.

The consequence is that **array length is never passed with an array in C**, which is why every
function taking an array also takes a count. GCC will warn with `-Wsizeof-array-argument` if you
write `sizeof` on such a parameter.

**3.**

- **`i <= n` is an off-by-one.** For `n` elements the valid indices are `0 … n-1`, so `a[n]` is one
  past the end — an out-of-bounds write, which is undefined behaviour and in practice corrupts
  whatever follows. → `i < n`.
- **`total` takes no length**, and computes it as `sizeof(a)/sizeof(a[0])`. After decay, `sizeof(a)`
  is 8 and `sizeof(a[0])` is 4, so the loop runs **exactly 2 iterations** regardless of the real
  length. → the function must take `size_t n` and use it.
- **`total`'s signature should be `const int *`.** It does not modify the array, and saying so in the
  type both documents the contract and lets the compiler catch an accidental write.

```c
void scale(int *a, size_t n, int factor)
{
    for (size_t i = 0; i < n; i++) a[i] *= factor;
}

int total(const int *a, size_t n)
{
    int s = 0;
    for (size_t i = 0; i < n; i++) s += a[i];
    return s;
}
```

**4.**

```c
void reverse(int *a, size_t n)
{
    if (n < 2) return;
    int *left  = a;
    int *right = a + n - 1;
    while (left < right) {
        int t = *left; *left = *right; *right = t;
        left++;
        right--;
    }
}
```

**Why `left < right` is safe here.** Both pointers stay within `[a, a + n - 1]` for the whole loop.
`left` only advances while it is strictly below `right`, and `right` only retreats while it is
strictly above `left`, so they meet or cross in the interior and the loop stops. No pointer is ever
formed outside the array.

**Why walking off the front would be different.** C permits forming a pointer anywhere in the array
**and one position past the end** — but grants no such allowance before the start. So this is UB:

```c
for (int *p = a + n - 1; p >= a; p--)   /* UB on the final decrement */
```

On the last iteration `p` is `a`, and `p--` forms `a - 1`, which is undefined **even though it is
never dereferenced**. The comparison `p >= a` then reads a pointer that the standard says has no
value.

In practice this usually "works", which is why the bug persists. But on a segmented architecture, or
under an optimiser that assumes pointers stay in range, it need not. The safe backwards form tests
before decrementing:

```c
for (int *p = a + n; p-- != a; ) ...   /* never forms a - 1 */
```

*This is the same shape as the `size_t` downward loop from Week 1* — test-then-decrement — and for
the same underlying reason: the boundary value below the start does not exist.

---

## Reading

- **K&R, §5.3–5.5** — pointers and arrays, address arithmetic
- **C11 §6.5.6 ¶8** — the additive operators; the "one past the end" rule stated precisely
- **C11 §6.3.2.1 ¶3** — array-to-pointer conversion (decay)
- **`gdb`: `p a`, `p &a`, `p a+1`, `p &a+1`** — watch the types differ on a live program

---

*PROG 101 · Week 5 · Lecture 2 · © CSE Department*
