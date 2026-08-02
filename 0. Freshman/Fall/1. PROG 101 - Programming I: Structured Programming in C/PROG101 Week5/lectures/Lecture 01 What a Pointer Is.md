# PROG 101 Programming I: Structured Programming in C
## Week 5 · Lecture 1: What a Pointer Is

---

## Lecture Goals

By the end of this lecture you can:

- State precisely what a pointer holds and what its *type* controls
- Use `&` and `*` correctly, and read a declaration containing both
- Explain why all object pointers are the same size but not interchangeable
- Say what a pointer's type does and does not affect

---

## 1. A Pointer Is an Address

Every object in a running program lives at some address in memory. A **pointer is a variable whose
value is an address.**

```c
int  x = 42;
int *p = &x;      /* p holds the address of x */
```

That is the entire concept. Everything else in Weeks 5 and 6 is a consequence.

The declaration reads right to left: `p` is a pointer (`*`) to `int`. The `*` binds to the
*variable*, not the type, which is why this bites:

```c
int* a, b;     /* a is int*, b is a PLAIN int -- almost never what you meant */
int *a, *b;    /* both are pointers */
```

Write the `*` next to the name. The type-side spelling `int* a` reads nicely for one variable and
lies the moment you declare two.

---

## 2. The Two Operators

| Operator | Name | Effect |
|---|---|---|
| `&x` | address-of | Produces a pointer to `x` |
| `*p` | dereference / indirection | Produces the object `p` points to |

They are inverses: `*(&x)` is `x`, always.

```c
int  x = 42;
int *p = &x;

printf("%d\n", x);    /* 42 -- the value          */
printf("%p\n", (void*)p);  /* an address          */
printf("%d\n", *p);   /* 42 -- through the pointer */

*p = 99;              /* writes THROUGH p */
printf("%d\n", x);    /* 99 -- x changed  */
```

The last two lines are the point of pointers: `*p = 99` modified `x` without naming `x`. That
capability is what Lecture 2 turns into a way for functions to change their caller's variables.

> **`%p` requires `void *`.** `printf("%p", p)` with an `int *` is undefined behaviour, because `%p`
> is specified for `void *` and the compiler does not insert the conversion for a variadic argument.
> Always cast: `printf("%p", (void *)p)`.
>
> **`-Wall -Wextra` will not tell you.** Verified: neither flag warns, and neither does `-Wformat=2`.
> Only **`-pedantic`** reports it:
>
> ```
> warning: format '%p' expects argument of type 'void *', but argument 2 has type 'int *'
> ```
>
> This is one of the specific reasons the course build line includes `-pedantic`. In practice the
> two pointer types have the same representation on every mainstream machine, so the code "works" —
> which is exactly what makes it easy to leave in.

### Reading declarations with both

```c
int   x = 42;
int  *p = &x;      /* p points to x       */
int **q = &p;      /* q points to p       */

**q == 42          /* two hops to the value */
```

`q` is a pointer to a pointer to `int`. You will meet these in Week 6, when a function must modify a
caller's *pointer* rather than the thing it points to.

---

## 3. What the Type Controls

Here is a fact that surprises people. Verified on this machine:

```
char* 8   int* 8   double* 8   struct* 8
```

**Every object pointer is the same size** — 8 bytes on x86-64, because that is the size of an
address. A `char *` is not smaller than a `double *`.

So what does the type do? Three things, none of them the size of the pointer itself:

1. **How many bytes to read or write on dereference.** `*p` on an `int *` touches 4 bytes; on a
   `char *`, 1 byte; on a `double *`, 8.
2. **How far `p + 1` moves.** This is Lecture 2's subject, and it is entirely determined by the
   pointed-to type.
3. **What the compiler will let you do.** Assigning an `int *` to a `double *` is a type error, and
   for good reason — dereferencing it would misinterpret the bytes.

**The pointer's size is uniform; its behaviour is not.** That is why C has distinct pointer types at
all rather than one universal address type.

### `void *` — the exception

```c
void *v = &x;     /* any object pointer converts to void*, no cast needed */
int  *back = v;   /* and back again, no cast needed */
```

`void *` is the generic object pointer. It can hold any object address, and C11 §6.3.2.3 guarantees
the round trip. What it cannot do is be dereferenced (`*v` is meaningless — how many bytes?) or take
part in arithmetic (`v + 1` — how far?). GCC permits `void *` arithmetic as an extension treating it
as 1 byte; `-pedantic` rejects it and it is not portable.

You will use `void *` heavily in Week 11 for generic containers. For now, know that it exists and
that it is the one pointer type that deliberately discards the information the others carry.

### Function pointers are different

`void *` is guaranteed to round-trip **object** pointers only. Function pointers are a separate
family, and C does not guarantee you can convert between the two. They are Week 11's topic.

---

## 4. Uninitialised Pointers

```c
int *p;        /* p holds GARBAGE -- not NULL, not anything useful */
*p = 42;       /* UNDEFINED BEHAVIOUR: writing to an arbitrary address */
```

An uninitialised pointer is not zero. Like any automatic variable (Week 3), it contains whatever
happened to be in that stack slot. Dereferencing it writes to an address chosen at random by
history.

**Always initialise.** If you have nothing to point at yet, say so explicitly:

```c
int *p = NULL;
```

`NULL` is a value you can *test for*, which garbage is not. Lecture 3 covers null pointers properly.

GCC's `-Wmaybe-uninitialized` catches the obvious cases at `-O1` and above — but recall from Week 3
that it reports **nothing at `-O0`**, so develop at `-O2`.

---

## 5. Why Pointers Exist

Four reasons, each developed later:

| Reason | Where |
|---|---|
| Let a function modify its caller's variables | Lecture 2 |
| Pass large objects without copying them | Lecture 2 |
| Walk arrays efficiently | Lecture 2 |
| Build data structures whose size is not known at compile time | Week 6, Week 7 |

The fourth is the one that changes what you can write. A linked list, a tree, a hash table — none can
exist without a way to refer to memory obtained at run time. That is Week 6.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| A pointer holds an **address** | That is the whole concept |
| `int *p` | Write the `*` next to the name; `int* a, b` declares one pointer and one `int` |
| `&x` and `*p` | Inverses: `*(&x)` is always `x` |
| `*p = v` | Writes **through** the pointer, changing the pointed-to object |
| `%p` | Requires a `(void *)` cast — otherwise UB |
| All object pointers | Same **size** (8 bytes here); different **behaviour** |
| The type controls | Bytes touched on deref, distance of `+1`, and what the compiler allows |
| `void *` | Generic object pointer; cannot deref, cannot do arithmetic |
| Uninitialised pointer | Garbage, **not** NULL — initialise to `NULL` if you have nothing |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** Give the output.

```c
int  x = 10, y = 20;
int *p = &x;
*p = 15;
p = &y;
*p = 25;
printf("%d %d\n", x, y);
```

**2. (Explain.)** `sizeof(char *)` and `sizeof(double *)` are both 8 here. If the type does not
change the pointer's size, what does it change? Give three distinct answers.

**3. (Fix.)** Three bugs.

```c
int *a, b;
int  v = 5;
a = v;
printf("%p\n", a);
*b = 7;
```

**4. (Stretch.)** `int **q = &p;` declares a pointer to a pointer. Give a concrete situation where a
function genuinely needs `int **` as a parameter, and explain why `int *` cannot do the job.

### Answers

**1.** Output: **`15 25`**

| Step | Effect |
|---|---|
| `p = &x` | `p` points at `x` |
| `*p = 15` | writes **through** `p` → `x` becomes 15 |
| `p = &y` | `p` now points at `y`; `x` is untouched and keeps 15 |
| `*p = 25` | writes through `p` → `y` becomes 25 |

The distinction to internalise: `p = &y` changes **the pointer**; `*p = 25` changes **the thing
pointed to**. Confusing the two is the most common early pointer error.

**2.** Three things, from §3:

1. **How many bytes a dereference touches.** `*p` on a `char *` reads 1 byte; on a `double *`, 8.
   The pointer is the same size; the *access* is not.
2. **How far `p + 1` moves.** Verified: `+1` on an `int *` advances 4 bytes, on a `char *` 1 byte, on
   a `double *` 8. Arithmetic is in units of the pointed-to type.
3. **What assignments the compiler permits.** `int *` and `double *` are incompatible types; assigning
   one to the other is a constraint violation, because dereferencing the result would reinterpret the
   bytes as the wrong type.

*Also acceptable:* it determines whether the pointer can be dereferenced at all — `void *` cannot.

**3.**

- **`int *a, b;` declares `b` as a plain `int`, not a pointer.** Almost certainly not the intent.
  → `int *a, *b;`
- **`a = v;` assigns an `int` to an `int *`.** The address-of operator is missing; this treats the
  *value* 5 as an address. GCC: `warning: assignment to 'int *' from 'int' makes pointer from integer
  without a cast`. → `a = &v;`
- **`printf("%p\n", a)` passes an `int *` where `%p` requires `void *`** — undefined behaviour for a
  variadic argument. → `printf("%p\n", (void *)a);`
- **`*b = 7;` dereferences `b`,** which after the first fix is an uninitialised pointer holding
  garbage — undefined behaviour. Initialise it before use: `b = &v;` or `int *b = NULL;` and only
  dereference once it points somewhere real.

*(Four defects, in three lines. That density is normal for pointer code and is exactly why the
compiler flags must be on.)*

**4.** A function needs `int **` whenever it must **modify the caller's pointer itself**, not merely
the object the pointer refers to.

The canonical case is allocation:

```c
int alloc_buffer(int **out, size_t n)
{
    int *p = malloc(n * sizeof *p);
    if (!p) return -1;
    *out = p;                 /* writes the caller's POINTER variable */
    return 0;
}

int *buf = NULL;
if (alloc_buffer(&buf, 100) == 0) { /* buf now points at the block */ }
```

**Why `int *` cannot do it.** Parameters are passed by value (Week 3), including pointers. Given
`int *p`, the function receives a *copy* of the caller's pointer. Assigning `p = malloc(...)` changes
only the copy; the caller's variable still holds its old value, and the allocation leaks. To change
the caller's pointer you must be handed that pointer's address — which is exactly `int **`.

The rule generalises: **to modify a `T` in the caller, take a `T *`.** When `T` is itself `int *`,
that means `int **`. Nothing special is happening; it is the same rule applied to a pointer type.

*Other legitimate answers:* freeing and nulling in one call (`void release(int **p) { free(*p);
*p = NULL; }`), a linked-list insert that may replace the head pointer, or an array of strings
(`char **argv`) — though that last one is an array of pointers rather than a pointer to a pointer, a
distinction worth drawing out.

---

## Reading

- **K&R, §5.1–5.2** — pointers and addresses; pointers and function arguments
- **C11 §6.3.2.3** — pointer conversions, including the `void *` guarantee
- **`gdb`: `p &x`, `p p`, `p *p`, `x/4xb &x`** — inspect addresses and raw bytes on a live program

---

*PROG 101 · Week 5 · Lecture 1 · © CSE Department*
