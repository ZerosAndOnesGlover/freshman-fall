# PROG 101 · Programming I: Structured Programming in C
## Week 10 · Lecture 1: The Preprocessor

---

## Lecture Goals

By the end of this lecture you can:

- Describe what the preprocessor does and, more importantly, what it does **not** do
- Trace `#include` and explain why headers need guards
- Inspect preprocessor output with `gcc -E` and read what comes back
- Structure a header so it can be included any number of times, in any order

---

## 1. A Text Substitution Engine

Week 0 introduced the four-stage pipeline: **preprocess → compile → assemble → link**. This week
returns to the first stage and takes it seriously.

The critical fact:

> **The preprocessor does not understand C.** It manipulates *tokens* — it knows nothing about types,
> scopes, expressions, or functions.

It runs before the compiler ever sees your code, and it produces a single expanded text file called a
**translation unit**. Everything it does is textual: paste in a file, replace a name with some
tokens, delete a region.

Every bug in Lecture 2 comes from that one sentence. A macro that looks like a function is not a
function, and the differences are exactly the places where "text substitution" and "C semantics"
disagree.

### What it actually does

| Directive | Effect |
|---|---|
| `#include` | Paste the named file in, verbatim |
| `#define` | Define a macro (Lecture 2) |
| `#undef` | Remove a macro definition |
| `#if` / `#ifdef` / `#else` / `#endif` | Include or delete a region of text (Lecture 3) |
| `#error` | Stop compilation with a message |
| `#pragma` | Implementation-specific instruction |

Directives start with `#` as the first non-whitespace character on a line, and — unlike C statements
— they end at the newline, not a semicolon. That difference matters more than it sounds.

---

## 2. `#include` Is Literal Insertion

```c
#include <stdio.h>      /* search the system include path */
#include "myheader.h"   /* search the current directory first, then the system path */
```

`#include` pastes the entire contents of the named file at that point. That is all it does. There is
no import mechanism, no namespace, no module — just text.

The consequences are easy to underestimate. Verified, on a two-line program:

```c
#include <stdio.h>
int main(void){ printf("hi"); return 0; }
```

```
source lines:                     2
after preprocessing:            815
after removing blanks and #lines: 303
```

**Two lines became 815.** `stdio.h` pulled in type definitions, other headers, function
declarations, and macro definitions — all of which the compiler must then parse. This is why C builds
get slow: every translation unit re-parses every header it includes.

### Inspect it yourself

```bash
gcc -E file.c            # full preprocessor output
gcc -E -P file.c         # without the line-marker directives
gcc -E -P file.c | less  # readable
gcc -dM -E file.c        # just the macro definitions in effect
```

`gcc -E` is the single most useful debugging tool for macro problems. When a macro misbehaves, look
at what it actually expanded to rather than reasoning about what you meant.

### `<>` versus `""`

| Form | Search order |
|---|---|
| `#include <file.h>` | System include directories only |
| `#include "file.h"` | The including file's directory first, then the system directories |

Use `""` for your own headers and `<>` for library headers. This is convention rather than a strict
rule — but the convention carries information for the reader, so follow it.

---

## 3. Include Guards

If `#include` is literal insertion, what happens when a header arrives twice?

```c
#include "thing.h"
#include "thing.h"     /* the same declarations, again */
```

For function declarations, nothing — C permits repeated identical declarations. For a **type
definition**, it is an error. Verified:

```
error: redefinition of 'struct Thing'
```

And you rarely include a header twice on purpose. It happens *transitively*: `a.h` includes
`common.h`, `b.h` includes `common.h`, and your file includes both. With any real header graph,
duplicates are certain.

### The guard

```c
#ifndef THING_H          /* if THING_H is not defined... */
#define THING_H          /* ...define it, so the next time this is skipped */

struct Thing { int x; };
int  thing_value(void);

#endif /* THING_H */
```

The first inclusion defines `THING_H` and processes the body. Every later inclusion finds `THING_H`
already defined and skips to `#endif`, emitting nothing.

Verified: with the guard in place, including the same header twice compiles cleanly under
`-Wall -Wextra -Werror -pedantic`.

**Every header you write gets a guard. Without exception.**

Naming: use something that cannot collide — the file name in upper case with underscores, optionally
with a project prefix. `THING_H`, `PROG101_THING_H`. A guard named `H` or `HEADER` will eventually
collide with someone else's, and the symptom is a header that silently vanishes.

### `#pragma once`

```c
#pragma once
```

One line, does the same job, supported by GCC, Clang, and MSVC. It is **not standard C**, though it
is nearly universal in practice.

The trade-off is real but small: `#pragma once` relies on the compiler identifying the same file
reliably, which can misfire with symlinks or hard links across build systems. Traditional guards are
guaranteed by the standard and work everywhere.

**Use traditional guards in this course.** Recognise `#pragma once` when you read it.

---

## 4. What Belongs in a Header

A header declares an interface. It should contain:

| Belongs in a header | Does **not** belong |
|---|---|
| Function **declarations** (prototypes) | Function **definitions** (bodies) |
| `struct` / `union` / `enum` definitions | Variable definitions |
| `typedef`s | `static` functions |
| Macro definitions that are part of the interface | Anything only one `.c` file needs |
| `extern` declarations of globals | |

The distinction that causes linker errors:

```c
/* thing.h */
int counter;            /* WRONG: this DEFINES a variable in every .c that includes it */
extern int counter;     /* right: declares it; one .c file defines it */
```

Including the first version from two `.c` files gives *multiple definition* at link time. Week 3's
Lecture 3 covered declaration versus definition; here is where it bites.

Likewise a function body in a header gets compiled into every translation unit that includes it, and
the linker rejects the duplicates. The exceptions are `static` functions (each unit gets its own
private copy — wasteful but legal) and `inline`, which has its own rules.

### The self-contained rule

**A header should compile on its own.** If `thing.h` uses `size_t`, it must include `<stddef.h>`
itself rather than assuming the includer did. Test it:

```bash
echo '#include "thing.h"' > /tmp/t.c && gcc -fsyntax-only /tmp/t.c
```

A header that only works when included after something else creates ordering dependencies, and those
break the moment someone reorders their includes alphabetically.

---

## 5. Where the Preprocessor Ends

Some things look like preprocessing and are not:

| Feature | Handled by |
|---|---|
| `#define MAX 100` | **Preprocessor** |
| `const int MAX = 100;` | Compiler — a real, typed object |
| `enum { MAX = 100 };` | Compiler — a real, typed constant |
| `#include` | Preprocessor |
| `sizeof` | **Compiler** — the preprocessor cannot compute it |
| `__func__` | **Compiler** — a variable, not a macro |

That `sizeof` row matters. This does **not** work:

```c
#if sizeof(int) == 4      /* ERROR: the preprocessor has no idea what sizeof is */
#endif
```

The preprocessor runs before types exist. Test for size using the limits macros instead:

```c
#include <limits.h>
#if INT_MAX == 2147483647
    /* int is 32-bit */
#endif
```

Similarly `__func__` is specified as a *variable* declared implicitly in every function, not a macro —
so it cannot be pasted or stringified the way `__FILE__` can. Verified: it prints `main` inside
`main`.

---

## 6. Summary

| Idea | Takeaway |
|---|---|
| The preprocessor does not understand C | It manipulates tokens; no types, no scopes |
| Output | A single expanded **translation unit** |
| Directives end at the newline | Not at a semicolon |
| `#include` | Literal text insertion — verified 2 lines → **815** |
| `gcc -E -P` | Look at the expansion instead of guessing |
| `<>` vs `""` | System path vs including file's directory first |
| Double inclusion | Fine for declarations, an **error** for type definitions |
| Include guard | `#ifndef X / #define X / … / #endif` — on every header, no exceptions |
| `#pragma once` | Equivalent, universal in practice, **not standard** |
| Headers hold declarations | Definitions there cause *multiple definition* at link time |
| `int counter;` in a header | Defines it in every unit — use `extern` |
| Headers must be self-contained | Test with `gcc -fsyntax-only` |
| `sizeof` in `#if` | Impossible — the preprocessor predates types |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** Given `a.h` includes `common.h`; `b.h` includes `common.h`; and `main.c` includes
both `a.h` and `b.h`. How many times is `common.h`'s text inserted, with and without a guard?

**2. (Explain.)** Why does putting `int counter;` in a header cause a link error when two `.c` files
include it, while `int add(int, int);` does not?

**3. (Fix.)** Four problems.

```c
/* vec.h */
#include "vec.h"
struct Vec { int *data; size_t len; };
int vec_len(struct Vec *v) { return (int)v->len; }
Vec *vec_new(void);
```

**4. (Stretch.)** A colleague proposes replacing all include guards with `#pragma once` project-wide,
arguing it is shorter and cannot be mistyped. Give the strongest argument for the change, the
strongest against, and say what you would actually do.

### Answers

**1.** **Without a guard: twice.** `#include` is literal insertion and performs no bookkeeping — the
text arrives once via `a.h` and once via `b.h`. If `common.h` defines any type, the second copy is a
redefinition error.

**With a guard: the text is inserted twice, but only processed once.** This distinction is worth
being precise about. The preprocessor still reads `common.h` both times; on the second pass the
`#ifndef` is false, so the body is skipped and nothing is emitted. The *file access* happens twice —
which is why include guards do not fully solve the build-speed problem, and why some compilers apply
a "multiple include optimisation" to skip re-reading a file whose entire contents are wrapped in a
guard.

**2.** Because one is a **definition** and the other is a **declaration**.

`int counter;` at file scope is a *tentative definition* — it allocates storage. After preprocessing,
each `.c` file that included the header contains its own `int counter;`, so each object file defines
a symbol named `counter`. The linker finds two definitions of the same global and reports *multiple
definition*.

`int add(int, int);` is only a declaration — it says a function with that name and type exists
somewhere. Declarations allocate nothing, and C explicitly permits a declaration to be repeated as
often as you like, so multiple copies are harmless.

The fix is `extern int counter;` in the header (declaration only) with exactly one `int counter;` in
one `.c` file (the definition).

*(Note: GCC historically allowed the multiple-tentative-definition case via "common symbols". Since
GCC 10 the default is `-fno-common`, so it is now an error — which is an improvement.)*

**3.**

- **No include guard.** Add `#ifndef VEC_H / #define VEC_H … #endif`.
- **The header includes itself.** `#include "vec.h"` inside `vec.h` is infinite recursion; the
  compiler stops at a nesting limit with a confusing error. Delete it.
- **`size_t` is used but `<stddef.h>` is not included.** The header is not self-contained — it
  compiles only if the includer happened to include `<stddef.h>` first.
- **A function body in a header.** `vec_len`'s definition is compiled into every translation unit
  that includes the file, giving *multiple definition* at link time. Move it to `vec.c` and leave a
  declaration.
- **`Vec *vec_new(void);` uses an undeclared type name.** The struct is `struct Vec`; there is no
  `typedef`. Either write `struct Vec *vec_new(void);` or add `typedef struct Vec Vec;`.

```c
/* vec.h */
#ifndef VEC_H
#define VEC_H

#include <stddef.h>

typedef struct Vec { int *data; size_t len; } Vec;

int  vec_len(const Vec *v);
Vec *vec_new(void);

#endif /* VEC_H */
```

**4. Strongest argument for `#pragma once`:** it eliminates a whole class of real bugs. A mistyped or
copy-pasted guard macro — `#ifndef VEC_H` at the top and `#define VECTOR_H` below, or two headers
that both chose `UTIL_H` — silently causes the header to be included twice or never. The failure is
confusing and can lie dormant. `#pragma once` cannot be mistyped and cannot collide, and it is one
line instead of three.

**Strongest argument against:** it is **not in the C standard**. Its behaviour depends on the
compiler correctly deciding that two paths refer to the same file, which is a filesystem question,
not a language one. Symlinks, bind mounts, hard links, and build systems that reach the same header
by two different paths can defeat it — and when it fails, it fails by silently including twice, which
is exactly the bug it was meant to prevent. Traditional guards are guaranteed by the standard and
depend on nothing outside the text.

**What I would actually do:** use both.

```c
#pragma once
#ifndef VEC_H
#define VEC_H
...
#endif
```

This is common in production code. `#pragma once` gives the fast path and the multiple-include
optimisation on every mainstream compiler; the guard gives the standards-guaranteed fallback if the
pragma is unsupported or defeated. The cost is two extra lines per header.

*Also fully acceptable:* stick to traditional guards alone and enforce the naming convention with a
lint rule or a script, which addresses the mistyping risk directly rather than by changing mechanism.
The answer to reject is one that treats this as obvious in either direction — it is a genuine
trade-off between guaranteed behaviour and eliminated human error.

---

## Reading

- **K&R, §4.11** — the preprocessor
- **C11 §5.1.1.2** — translation phases; note that preprocessing is phase 4 of 8
- **C11 §6.10** — preprocessing directives, in full
- **`gcc -E`, `gcc -dM -E`** — run them on your own code today

---

*PROG 101 · Week 10 · Lecture 1 · © CSE Department*
