# PROG 101 · Programming I: Structured Programming in C
## Week 3 · Lecture 2: The Call Stack and Scope

**Date:** Wednesday 9 September 2026 · 10:00–10:50 · Week 3

---

## Lecture Goals

By the end of this lecture you can:

- Describe what happens in memory when a function is called and when it returns
- Explain why a local variable's address becomes invalid the moment its function returns
- Apply C's scope and storage-duration rules, including `static` locals and shadowing
- Recognise stack overflow and dangling-pointer bugs from their symptoms

---

## 1. The Call Stack Is Real

Lecture 1 treated a function as an interface: arguments in, a value out. That model is enough to
*use* functions. It is not enough to debug them.

Underneath, every call allocates a **stack frame** — a contiguous block holding that call's
parameters, local variables, and the address to return to. Frames stack up as calls nest and unwind
as they return.

Verified, with three nested functions each printing the address of a local:

```
a_fn       frame local at 0x7ffec98be594   (depth 1)
b_fn       frame local at 0x7ffec98be584   (depth 2)
c_fn       frame local at 0x7ffec98be574   (depth 3)
```

Two facts fall straight out of those numbers:

**The stack grows downward.** Each nested call sits at a *lower* address — `...594`, then `...584`,
then `...574`. This is the convention on x86-64 and most architectures, though the standard does not
require it.

**Frames here are 16 bytes apart.** That is this compiler's frame size for these trivial functions;
it depends on how many locals there are, alignment, and optimisation level. Do not memorise the
number — memorise that the spacing is *constant and small*.

### What a frame contains

| Part | Purpose |
|---|---|
| Return address | Where to resume in the caller |
| Saved frame pointer | The caller's frame base, so unwinding can find it |
| Parameters | Copies of the arguments (Lecture 1's pass-by-value) |
| Local variables | The function's own storage |
| Padding | Alignment |

On x86-64 the first several arguments arrive in *registers* rather than on the stack, and the
compiler may keep locals in registers too. So the frame is often smaller than the source suggests.
The model stays correct; the details are an optimisation.

### Call and return

**On call:** push the return address, allocate the frame, copy arguments in, jump to the function.

**On return:** the return value goes into a designated register, the frame is deallocated, execution
resumes at the return address.

"Deallocated" means only that the stack pointer moves back. **The bytes are not cleared.** They sit
there, stale, until the next call overwrites them — which is exactly what makes the next section's
bug so treacherous.

---

## 2. The Dangling Pointer

Here is the single most important consequence of §1:

```c
int *bad_ptr(void)
{
    int local = 42;
    return &local;      /* the frame dies at return */
}
```

`local` lives in `bad_ptr`'s frame. The moment `bad_ptr` returns, that frame is gone and the pointer
names memory that no longer belongs to anyone.

**GCC catches this one:**

```
warning: function returns address of local variable [-Wreturn-local-addr]
```

Under the course's `-Werror` it is a build failure. But the warning only fires for the obvious shape;
route the address through another variable or a struct field and the compiler loses track.

### What actually happens is worse than a stale value

The intuitive model is "you get a pointer to memory that now holds garbage." Verified behaviour is
stranger:

```
bad_ptr() returned (nil)
```

**GCC compiled the function to return a null pointer.** Not a stale address — `NULL`. Because
returning the address of a local is undefined behaviour, the compiler is entitled to do anything, and
what it chose was to discard the code entirely.

This is the Week 2 lesson made concrete. UB is not "whatever the hardware happens to do." The
*compiler* transforms your program on the assumption that UB never occurs, and the result can bear no
resemblance to what you wrote. A program that reads through that pointer then crashes on a null
dereference — with a stack trace pointing at the caller, not at `bad_ptr`.

### The correct alternatives

```c
/* 1. Return by value -- the frame's contents are COPIED out */
int good_value(void) { int local = 42; return local; }

/* 2. Let the caller supply the storage */
void fill(int *out) { *out = 42; }

/* 3. Allocate on the heap -- outlives the frame (Week 6) */
int *make(void) { int *p = malloc(sizeof *p); if (p) *p = 42; return p; }

/* 4. static storage -- see 4 below */
```

Option 2 is the dominant C idiom, and it is why so many standard functions take an output pointer.

---

## 3. Stack Depth Is Finite

The stack has a fixed size — typically **8 MB** on Linux (`ulimit -s` reports it). Divide by the
frame size and you get the maximum nesting depth: at roughly 64 bytes per frame, about 130,000
levels.

Exceed it and you get a **stack overflow**, which on Linux arrives as a segmentation fault. Two
common causes:

```c
int f(int n) { return f(n + 1); }        /* runaway recursion: no base case */

void g(void) { int buf[1000000]; }       /* one frame demanding 4 MB */
```

The second is worth noting: a single large local array can blow the stack without any recursion.
Large buffers belong on the heap.

**Recursion depth is a real design constraint.** A recursive tree walk is fine for a balanced tree of
a million nodes (depth ~20), and unsafe for a linked list of a million nodes treated recursively
(depth 1,000,000). Week 9 returns to this.

---

## 4. Storage Duration

C separates *where a name is visible* (scope) from *how long the object lives* (storage duration).
Confusing them causes real bugs.

| Duration | Lifetime | Declared as |
|---|---|---|
| **Automatic** | Until the enclosing block exits | An ordinary local |
| **Static** | The whole program run | `static`, or any file-scope variable |
| **Allocated** | Until you `free` it | `malloc` (Week 6) |

### `static` locals

```c
int counter(void)
{
    static int n = 0;    /* initialised ONCE, survives across calls */
    return ++n;
}
```

Verified — called in a loop, it yields `5 6 7` continuing from earlier calls. The variable is
*visible* only inside `counter`, but it *lives* for the whole program.

Two details that matter:

- **The initialiser runs once**, before `main`, not on every call.
- **Static objects are zero-initialised by default**; automatic locals are **not** and contain
  garbage until you assign them.

> **A live demonstration of Week 2.** Printing four calls in one statement —
> `printf("%d %d %d %d", counter(), counter(), counter(), counter())` — produced:
>
> ```
> counter(): 4 3 2 1
> ```
>
> Not `1 2 3 4`. Argument evaluation order is **unspecified**, and GCC evaluated right to left. The
> function is correct; the *printing* is what lied. Sequence the calls into separate statements when
> the order matters.

---

## 5. Scope

Scope is lexical: determined by where a name appears in the source, not by the call chain.

```c
int g = 100;                    /* file scope: visible in this file after this point */

void f(void)
{
    int x = 1;                  /* block scope: this function */
    if (x) {
        int y = 2;              /* block scope: this if-block only */
        printf("%d\n", y);
    }
    /* y is not in scope here */
}
```

**A block is any `{ }`**, including a loop body or a bare pair of braces. A `for` loop's declaration
is scoped to the loop:

```c
for (int i = 0; i < n; i++) { ... }
/* i is not in scope here */
```

### Shadowing

An inner declaration hides an outer one of the same name:

```c
int g = 100;
void shadow(void) { int g = 5; printf("%d\n", g); }    /* prints 5 */
```

Verified: the inner `g` is 5; the outer `g` is untouched and still 100.

Shadowing is legal and occasionally useful, but it is a common source of confusion — you edit what
you think is the outer variable and change nothing. **`-Wshadow` warns about it**; it is not in
`-Wall -Wextra`, so enable it explicitly if you want the check.

### Scope vs. lifetime, side by side

| | Scope | Lifetime |
|---|---|---|
| Ordinary local | Its block | Its block |
| `static` local | Its block | Whole program |
| File-scope variable | Rest of the file | Whole program |
| `static` file-scope | Rest of the file *only* | Whole program |
| Heap allocation | Wherever the pointer reaches | Until `free` |

The `static` local is the interesting row: **narrow scope, long lifetime.** That combination is what
makes it useful for a call counter or a cached value, and what makes it dangerous in multi-threaded
code, where every thread shares the one object.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| Stack frame | Per-call storage: parameters, locals, return address |
| Grows downward | Verified: nested frames at decreasing addresses, 16 bytes apart here |
| Frame dies at return | The bytes are not cleared, merely abandoned |
| **Returning `&local`** | **Dangling pointer** — GCC warns `-Wreturn-local-addr` |
| What UB really did | GCC compiled the function to **return NULL**, not a stale address |
| Correct alternatives | Return by value, caller-supplied output pointer, heap, or `static` |
| Stack is finite | ~8 MB; runaway recursion *or* one huge local array overflows it |
| Automatic duration | Uninitialised by default — contains garbage |
| `static` local | Initialised once, zero by default, narrow scope + program lifetime |
| Shadowing | Legal; `-Wshadow` is not in `-Wall`, enable it deliberately |
| Scope ≠ lifetime | The two are independent, and `static` locals prove it |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** Give the output, and state the maximum number of frames alive at once.

```c
void c(void) { printf("c "); }
void b(void) { printf("b "); c(); printf("B "); }
void a(void) { printf("a "); b(); printf("A "); }
int main(void) { a(); printf("done\n"); return 0; }
```

**2. (Explain.)** Why is returning `&local` a bug but returning `local` fine? Answer in terms of what
happens to the frame.

**3. (Fix.)** Three bugs.

```c
char *greet(const char *name)
{
    char buf[64];
    snprintf(buf, sizeof buf, "Hello, %s", name);
    return buf;
}

int next_id(void) { int n = 0; return ++n; }

int sum(int *a, int n) { int total; for (int i=0;i<n;i++) total += a[i]; return total; }
```

**4. (Stretch.)** A recursive function crashes with a segfault for large inputs but works for small
ones, and there is no pointer arithmetic anywhere in it. Explain the cause, describe how you would
confirm it, and give two fixes with different trade-offs.

### Answers

**1.** Output: **`a b c B A done`**

Maximum frames alive: **4** — `main`, `a`, `b`, `c`, all live simultaneously at the moment `c` runs
its `printf`.

The trace:

| Event | Frames alive |
|---|---|
| `main` starts | main |
| `a()` prints `a`, calls `b` | main, a |
| `b()` prints `b`, calls `c` | main, a, b |
| `c()` prints `c`, returns | main, a, b, **c** ← peak |
| `b()` prints `B`, returns | main, a |
| `a()` prints `A`, returns | main |

The interleaving of lowercase (on the way down) and uppercase (on the way back up) is the shape of
every stack trace you will ever read.

**2.** The difference is **when the copy happens.**

`return local;` copies the *value* out of the frame and into the return register **before** the frame
is destroyed. The caller receives a copy that lives in the caller's own storage. Nothing points into
the dead frame.

`return &local;` copies the *address* out. The address is still valid at the instant of return, but
it names storage inside the frame that is being abandoned in the same operation. The caller receives
a perfectly-formed pointer to memory it does not own.

Put another way: the value survives because it is duplicated; the address does not survive because
the thing it refers to is not.

**3.**

- **`greet` returns a pointer to a local array.** `buf` lives in `greet`'s frame; the returned
  pointer dangles. GCC warns `-Wreturn-local-addr`. Fixes: have the caller pass the buffer in
  (idiomatic C), or `malloc` it and document that the caller frees it.
  ```c
  void greet(char *out, size_t cap, const char *name)
  { snprintf(out, cap, "Hello, %s", name); }
  ```
- **`next_id` re-initialises `n` on every call** and always returns 1. The variable needs *static
  duration*: `static int n = 0;`. This is the scope/lifetime distinction from §5 — the author wanted
  a narrow scope and a long lifetime, and got a narrow scope and a short one.
- **`sum` never initialises `total`.** Automatic locals are **not** zero-initialised, so it starts
  with garbage and the result is meaningless. → `int total = 0;`. GCC's `-Wmaybe-uninitialized`
  usually catches this at `-O1` or higher — but *not* at `-O0`, which is a good reason to compile at
  `-O2` even while developing.

**4.** The cause is **stack overflow**: each recursive call adds a frame, and past ~8 MB of frames
the stack hits its guard page and the OS delivers SIGSEGV. Small inputs stay under the limit; large
ones do not. No pointer arithmetic is involved, which is why it looks mysterious.

**How to confirm it:**

- Run under a debugger and look at the backtrace — thousands of identical frames is conclusive.
  `gdb`'s `bt -20` shows the repetition immediately.
- Print the recursion depth, or the address of a local, at each level; a steadily marching address
  with no return is the signature.
- Raise the limit temporarily (`ulimit -s unlimited`) and see whether the crash moves to a larger
  input. If it does, it is depth, not corruption.
- ASan reports `stack-overflow` explicitly rather than a bare SEGV.

**Two fixes with different trade-offs:**

| Fix | Trade-off |
|---|---|
| **Convert to iteration** with an explicit stack (a heap-allocated array or your own stack structure) | Heap is far larger than 8 MB and growable, so depth stops being a limit. Costs readability — the recursive version is usually much clearer, and you now manage the stack by hand |
| **Bound the depth**: add a depth parameter and fail cleanly past a threshold | Small change, keeps the recursive structure, turns a crash into a diagnosable error. But it does not let you *solve* the large input — it only refuses it politely |

*A third answer worth credit:* if the recursion is **tail recursive**, compiling at `-O2` may let GCC
turn it into a loop, eliminating the frames entirely. But this is not guaranteed by the standard and
must be verified per compiler and flag — it is an optimisation you can observe, not a language
feature you can rely on.

---

## Reading

- **K&R, §1.10, §4.3–4.6** — scope, storage duration, and `static`
- **`ulimit -s`** — check your own stack limit
- **`gdb`: `bt`, `frame`, `info locals`** — walk a live stack; the fastest way to make this concrete
- **C11 §6.2.1** — scopes of identifiers; **§6.2.4** — storage durations

---

*PROG 101 · Week 3 · Lecture 2 · © CSE Department*
