# PROG 101 · Week 5 Reference
## Pointers I

---

## The Two Operators

```c
int  x = 42;
int *p = &x;      /* & : address-of      */
int  y = *p;      /* * : dereference     */
*p = 99;          /* writes THROUGH p -- x becomes 99 */
```

`*(&x)` is always `x`. Write the `*` next to the **name**: `int *a, *b;` — because `int* a, b;`
declares one pointer and one plain `int`.

---

## What the Type Controls

**All object pointers are the same size.** Verified: `char*`, `int*`, `double*`, `struct*` are all
**8 bytes** here. The type instead controls:

1. How many bytes a dereference touches
2. How far `p + 1` moves
3. What the compiler permits

| Pointer type | `p + 1` advances |
|---|---|
| `char *` | **1** byte |
| `int *` | **4** bytes |
| `double *` | **8** bytes |

All verified.

---

## Arrays and Pointers

| | |
|---|---|
| `a[i]` | **Defined as** `*(a + i)` — hence `2[a]` compiles |
| `a` in an expression | **Decays** to `&a[0]` |
| `sizeof a` | The array, only where declared (40 for `int a[10]`) |
| `sizeof p` | The pointer (**8**) |
| `&a[0]` | Type `int *` |
| `&a` | Type `int (*)[10]` |

**Verified on `int a[10]`:** `a+1` advances **4** bytes; `&a+1` advances **40** — the whole array.
Same address, different types.

`p2 - p1` yields an **element count** (type `ptrdiff_t`, print with `%td`), not bytes.

### Legal range

Within the array, **plus one past the end**. `a + n` may be formed and compared but not
dereferenced. `a - 1` is **undefined even without dereferencing** — which is why backwards loops use
test-then-decrement:

```c
for (int *p = a + n; p-- != a; ) ...      /* never forms a - 1 */
```

---

## Write-Back

C passes everything by value, so:

```c
void swap_bad(int a, int b);      /* cannot change the caller's variables */
void swap_ok (int *a, int *b);    /* can                                   */
```

**The rule: to modify a caller's `T`, take a `T *`.** Applied when `T` is itself `int *`, that gives
`int **` — needed whenever a function must change the caller's *pointer*, such as an allocator.

---

## `const` — Four Combinations

| Declaration | Repoint? | Modify target? |
|---|---|---|
| `int *p` | ✅ | ✅ |
| `const int *p` | ✅ | ❌ |
| `int *const p` | ❌ | ✅ |
| `const int *const p` | ❌ | ❌ |

All four verified against the compiler.

**Reading rule:** `const` qualifies whatever is immediately to its **left**, unless it is leftmost, in
which case it qualifies what is to its right.

**Use `const T *` for any parameter you read but do not modify.** It documents the contract, catches
accidental writes, and lets callers pass `const` objects.

`const` constrains **the access route**, not the object — another name for the same object may still
modify it.

---

## NULL and the Classic Errors

```c
int *p = NULL;
if (p != NULL) *p = 5;      /* or: if (p) */
```

Prints as `(nil)`; `p == 0` is true. **Dereferencing NULL is undefined behaviour.**

Check every returning-pointer call: `malloc`, `fopen`, `strchr`, `strstr`, `bsearch`.

| Error | Symptom |
|---|---|
| Uninitialised pointer | Writes to an arbitrary address |
| Returning `&local` | Dangling — GCC compiles it to `return NULL` |
| Off-by-one | Corrupts an adjacent variable; crash appears elsewhere |
| Null dereference | Immediate, consistent segfault |
| Unchecked `strchr` | NULL deref when the character is absent |

**Guard order matters:** `p && *p`, never `*p && p` — `&&` guarantees left-to-right (Week 2).

---

## Tooling

```bash
gcc -Wall -Wextra -Werror -pedantic -std=c11 -g prog.c -o prog
gcc -fsanitize=address,undefined -g prog.c -o prog_san
valgrind --leak-check=full --error-exitcode=1 ./prog
```

| Flag / tool | Catches |
|---|---|
| `-Wreturn-local-addr` | Returning a local's address |
| `-Wmaybe-uninitialized` | Uninitialised use — **only at `-O1`+, silent at `-O0`** |
| `-Wsizeof-array-argument` | `sizeof` on a decayed array parameter |
| `-pedantic` | `%p` without a `(void *)` cast |
| ASan | Out-of-bounds, use-after-free |
| Valgrind | The above **plus uninitialised reads**, which ASan misses |

---

*PROG 101 · Week 5 · Reference · © CSE Department*
