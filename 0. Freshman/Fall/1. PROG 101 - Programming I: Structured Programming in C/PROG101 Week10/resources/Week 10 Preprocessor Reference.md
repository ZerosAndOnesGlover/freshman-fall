# PROG 101 · Week 10 Reference
## The Preprocessor and Macros

---

## Inspecting Expansions

```bash
gcc -E file.c            # full output
gcc -E -P file.c         # without line markers -- the readable form
gcc -dM -E - < /dev/null # every predefined macro
```

**When a macro misbehaves, look at the expansion.** Verified: a 2-line file including `<stdio.h>`
becomes **815** preprocessed lines.

---

## Directives

| Directive | Effect |
|---|---|
| `#include <f>` / `#include "f"` | System path / including file's directory first |
| `#define` / `#undef` | Define / remove a macro |
| `#if` / `#ifdef` / `#elif` / `#else` / `#endif` | Include or delete a region |
| `#error` | Stop with a message |

Directives end at the **newline**, not a semicolon. `#if` understands integer constants and
`defined()` — **not** `sizeof`, types, or floating point.

**An undefined name is 0 in `#if`.** Use `#ifdef` for "was it defined at all"; enable `-Wundef`.

---

## Include Guards

```c
#ifndef VEC_H
#define VEC_H
...
#endif /* VEC_H */
```

**Every header, without exception.** Without one, a transitively double-included header gives
`redefinition of 'struct X'`. `#pragma once` does the same job and is universal in practice, but is
not standard C.

### Headers hold declarations

| In a header | Not in a header |
|---|---|
| Function **declarations** | Function **bodies** → `multiple definition` at link |
| `struct` / `enum` / `typedef` | Variable definitions |
| `extern int x;` | `int x;` → `multiple definition` |

A header must **compile on its own**: `echo '#include "h.h"' > t.c && gcc -fsyntax-only t.c`.

---

## Macro Rules

**Parenthesise every parameter and the whole body.**

```c
#define SQUARE(x) ((x) * (x))
```

Verified failures without them:

| Written | Expands to | Gives | Should be |
|---|---|---|---|
| `SQUARE_BAD(2+3)` | `2+3 * 2+3` | **11** | 25 |
| `100/SQUARE_BAD(5)` | `100/5 * 5` | **100** | 4 |

**Double evaluation cannot be fixed with parentheses.** Verified: `MAX(i++, 3)` with `i = 5` returns
6 and leaves `i` at **7**. Any macro using a parameter twice has this. Write a `static inline`
function instead.

**Multi-statement macros need `do { } while (0)`.** A bare block leaves a stray `;` that breaks
`else`. GCC warns `-Wmultistatement-macros`.

**`#x` stringifies but does not expand.** Verified: `STR(VERSION)` gives `"VERSION"`;
`XSTR(VERSION)` gives `"42"`. Two levels are required.

**`a##b` pastes tokens.** Powerful, and it makes code ungreppable — comment it.

---

## When a Macro Is Right

| Use a macro | Use something else |
|---|---|
| Needs `__FILE__` / `__LINE__` from the **call site** | Ordinary logic → function |
| Needs the argument's **source text** (`#cond`) | Known types → `static inline` |
| Type-generic across several types | Integer constants → `enum` |
| Conditional compilation, header guards | Typed constants → `const` |

**Default: not a macro.**

---

## Assertions

```c
assert(index < length);                     /* runtime; disabled by -DNDEBUG */
_Static_assert(sizeof(int) >= 4, "msg");    /* compile time; free           */
```

**Never put side effects in `assert`** — `assert(scanf(...) == 1)` vanishes in release builds.

Use `assert` for **programmer errors**; use real error handling for conditions that can legitimately
occur (`malloc` failure, bad user input).

`_Static_assert` is strictly better for anything knowable at compile time. Verified: it catches a
desynchronised table with `error: static assertion failed`.

---

## X-Macros

```c
#define COLOURS  X(RED,"red") X(GREEN,"green") X(BLUE,"blue")

#define X(n,s) COLOUR_##n,
enum Colour { COLOURS COLOUR_COUNT };
#undef X

#define X(n,s) s,
static const char *names[] = { COLOURS };
#undef X
```

One list, many uses, cannot drift. `#undef X` between uses is **mandatory**.

**Use it when** the list is long, changes often, and is needed in three or more forms. Otherwise two
explicit tables plus a `_Static_assert` on their lengths is clearer and solves the same problem.

---

*PROG 101 · Week 10 · Reference · © CSE Department*
