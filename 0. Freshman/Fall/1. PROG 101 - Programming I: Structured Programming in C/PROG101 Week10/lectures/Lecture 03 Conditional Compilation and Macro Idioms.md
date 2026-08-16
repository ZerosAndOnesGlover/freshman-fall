# PROG 101 · Programming I: Structured Programming in C
## Week 10 · Lecture 3: Conditional Compilation and Macro Idioms

**Date:** Thursday 29 October 2026 · 10:00–10:50 · Week 10

---

## Lecture Goals

By the end of this lecture you can:

- Use `#if` / `#ifdef` to build one source for several configurations
- Write debug logging that compiles to nothing in a release build
- Use `assert` and `_Static_assert` in the right places
- Recognise the X-macro pattern, and judge when the cleverness is worth it

---

## 1. Conditional Compilation

The preprocessor can delete regions of text before the compiler sees them.

```c
#if defined(DEBUG) && DEBUG > 1
    puts("verbose debug");
#elif defined(DEBUG)
    puts("debug");
#else
    puts("release");
#endif
```

Verified, same source, three builds:

| Command | Output |
|---|---|
| `gcc prog.c` | `release` |
| `gcc -DDEBUG prog.c` | `debug` |
| `gcc -DDEBUG=2 prog.c` | `verbose debug` |

The deleted branches are not compiled, not optimised away, not present in the binary — the compiler
never sees them.

### The directives

| Directive | Meaning |
|---|---|
| `#ifdef NAME` | Is `NAME` defined? (Shorthand for `#if defined(NAME)`) |
| `#ifndef NAME` | Is it *not* defined? |
| `#if expr` | Evaluate a constant integer expression |
| `#elif expr` | Else-if |
| `#else` / `#endif` | |

`#if` evaluates integer constant expressions only. It understands arithmetic, comparisons, `&&`,
`||`, and `defined(X)`. It does **not** understand `sizeof`, types, variables, or floating point
(Lecture 1).

> **An undefined macro is 0 in `#if`.** So `#if FOO` is false when `FOO` is undefined *and* when it
> is defined as 0 — the two are indistinguishable. Use `#ifdef FOO` when you mean "was it defined at
> all". GCC's `-Wundef` warns when an undefined name is used this way, and it is worth enabling.

### Portability

```c
#ifdef __linux__
    /* Linux-specific */
#elif defined(_WIN32)
    /* Windows-specific */
#endif

#ifdef __GNUC__
    /* GCC or Clang extensions available */
#endif
```

Verified: `__GNUC__` is 13 on this machine. Predefined macros identify compiler, platform, and
standard version — `__STDC_VERSION__` was `201112` for C11.

**Isolate the conditionals.** Scatter `#ifdef` through your logic and the code becomes unreadable and
untestable — only one branch compiles, so the others rot silently. Confine platform differences to a
small number of functions, and keep the rest of the program portable:

```c
/* platform.h -- the ONLY file with #ifdef __linux__ */
int platform_mkdir(const char *path);
```

---

## 2. Debug Logging That Costs Nothing

The canonical use of conditional compilation:

```c
#ifdef DEBUG
#  define DBG(...) fprintf(stderr, __VA_ARGS__)
#else
#  define DBG(...) ((void)0)
#endif
```

Verified: without `-DDEBUG` the calls produce no output and no code; with `-DDEBUG` they log.

Two details make this work properly:

**`((void)0)` rather than nothing.** An empty replacement leaves a bare `;`, which is a null
statement — usually fine, but it breaks in an unbraced `if`/`else` exactly as in Lecture 2. `(void)0`
is a valid expression statement, so `DBG("x");` remains one statement everywhere.

**The arguments are not evaluated in a release build.** `DBG("%d", expensive())` costs nothing when
disabled, because the whole call is textually removed. That is the advantage over
`if (debug) fprintf(...)`, where the argument is still evaluated and the branch still exists.

The trade-off: the disabled code is **never compiled**, so it can rot. A `DBG` line referring to a
variable you renamed will not break the release build and will break the debug build months later.
Some projects therefore prefer a runtime flag with `if (debug_enabled)`, accepting the small cost to
keep the code compiling. Both are defensible; know which you chose.

### Variadic macros

`__VA_ARGS__` holds the trailing arguments. Verified:

```c
#define LOG(fmt, ...) fprintf(stderr, "[%s:%d] " fmt "\n", __FILE__, __LINE__, __VA_ARGS__)

LOG("value is %d", 42);      /* [l3.c:33] value is 42 */
```

Note `"[%s:%d] " fmt "\n"` — adjacent string literals concatenate at compile time, so the caller's
format string is spliced into a larger one.

**C11 requires at least one argument for `__VA_ARGS__`**, so `LOG("no args")` is technically invalid.
GCC accepts `, ##__VA_ARGS__` as an extension that swallows the comma; C23 standardises
`__VA_OPT__`. In portable C11, provide a separate zero-argument macro, as verified above.

---

## 3. `assert` and `_Static_assert`

### Runtime: `assert`

```c
#include <assert.h>
assert(index < length);
```

On failure it prints the file, line, and condition text, then calls `abort()`. Verified:

```
a0: as.c:3: main: Assertion `x==1' failed.
```

**`assert` is disabled by `-DNDEBUG`.** Verified: the same program with `-DNDEBUG` runs straight
through. That has a consequence people get wrong:

```c
assert(scanf("%d", &n) == 1);     /* BUG: the scanf vanishes in release */
```

**Never put anything with a side effect inside `assert`.** The expression disappears entirely when
`NDEBUG` is defined, taking your input, allocation, or increment with it.

Use `assert` for **programmer errors** — invariants that should be impossible if the code is correct.
Use ordinary error handling for **runtime conditions** that can legitimately occur:

| Situation | Use |
|---|---|
| Index out of range in your own loop | `assert` — a bug |
| A user typed a bad number | `if` + error message — not a bug |
| `malloc` returned NULL | `if` — can genuinely happen |
| A function's precondition violated by its caller | `assert` |

### Compile time: `_Static_assert`

C11 added assertions the compiler checks:

```c
_Static_assert(sizeof(int) >= 4, "int must be at least 32 bits");
_Static_assert(CHAR_BIT == 8, "byte must be 8 bits");
```

Verified: both pass here, and a failing one stops the build:

```
error: static assertion failed: "int too small"
```

This is strictly better than a runtime check for anything knowable at compile time — it costs nothing
and cannot be missed by a test that never ran. Use it to pin assumptions your code depends on:
structure sizes, enum ranges, type widths.

*(`<assert.h>` provides `static_assert` as a macro spelling of `_Static_assert`. C23 makes the short
form a keyword.)*

---

## 4. The X-Macro Pattern

A genuinely useful trick, and a genuinely divisive one.

**The problem:** you have a list — of colours, error codes, opcodes — and you need it in several
forms: an `enum`, an array of names, a `switch`. Keeping three copies in sync by hand fails the first
time someone adds an entry.

**The solution:** write the list once, and process it differently each time.

```c
#define COLOURS        \
    X(RED,   "red")    \
    X(GREEN, "green")  \
    X(BLUE,  "blue")

/* use 1: build the enum */
#define X(name, str) COLOUR_##name,
enum Colour { COLOURS COLOUR_COUNT };
#undef X

/* use 2: build the name table */
#define X(name, str) str,
static const char *colour_names[] = { COLOURS };
#undef X
```

Verified:

```
COLOUR_COUNT = 3
  0 -> red
  1 -> green
  2 -> blue
```

Adding a colour means adding **one line** to `COLOURS`. The enum, the count, and the name table all
update, and they cannot drift apart.

Note `COLOUR_COUNT` sitting after the list — since every `X` emits a trailing comma, the last enum
member is a free count of the entries. That idiom is worth knowing on its own.

### The honest assessment

**For:** it eliminates a real class of bug — parallel lists that fall out of sync — and that bug is
common and annoying.

**Against:** it is hard to read for anyone who has not seen it, `grep` for `COLOUR_RED` finds
nothing, and compiler errors inside the expansion are cryptic. The `#undef X` between uses is
mandatory and easy to forget.

**When to use it:** when the list is long, changes often, and is needed in three or more forms. For
a three-entry list used twice, write it out twice — the cleverness costs more than it saves.

This is a judgement call, and being able to *make* the judgement — rather than always reaching for
the clever tool or always avoiding it — is what this lecture is really teaching.

---

## 5. Summary

| Idea | Takeaway |
|---|---|
| `#if` deletes text | Untaken branches are never compiled at all |
| Verified | One source, three builds: `release` / `debug` / `verbose debug` |
| `#if` understands | Integer constants, comparisons, `defined()` — **not** `sizeof` or types |
| Undefined name in `#if` | Evaluates to 0; use `#ifdef` for "is it defined"; enable `-Wundef` |
| Isolate platform `#ifdef`s | One file, not scattered — untaken branches rot silently |
| `DBG(...)` → `((void)0)` | Not empty, or it breaks unbraced `if`/`else` |
| Disabled logging is free | Arguments are not evaluated; the code is removed |
| …but it rots | Never-compiled code breaks silently — know the trade-off |
| `__VA_ARGS__` | C11 needs ≥1 argument; provide a zero-arg variant |
| `assert` | For **programmer errors**; disabled by `-DNDEBUG` |
| **Never** side effects in `assert` | `assert(scanf(...) == 1)` vanishes in release |
| `_Static_assert` | Compile-time, free, cannot be missed by an unrun test |
| X-macros | One list, many uses; cannot drift — but ungreppable |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Trace.)** Given `#define LEVEL 0`, which branch is taken by each, and why do they differ?

```c
#if LEVEL          /* (a) */
#ifdef LEVEL       /* (b) */
#if defined(LEVEL) && LEVEL > 0    /* (c) */
```

**2. (Explain.)** Why is `assert(p = malloc(100));` a serious bug, and what are the *two* separate
defects in that line?

**3. (Fix.)** Three problems.

```c
#ifdef DEBUG
#define TRACE(msg) printf("%s\n", msg)
#endif

void work(void) {
    TRACE("starting");
    assert(setup() == 0);
    /* ... */
}
```

**4. (Stretch.)** Use an X-macro to define an error-code `enum`, a `const char *` message table, and
a `const char *error_name(int)` function that returns the identifier's own text. Then state one
concrete situation where you would reject this pattern in review.

### Answers

**1.**

| | Result | Why |
|---|---|---|
| **(a)** `#if LEVEL` | **False** | `LEVEL` expands to `0`, and `#if 0` is false |
| **(b)** `#ifdef LEVEL` | **True** | Asks only whether the name is *defined*, not its value |
| **(c)** `#if defined(LEVEL) && LEVEL > 0` | **False** | Defined, but `0 > 0` is false |

They differ because **`#ifdef` tests existence and `#if` tests value.** The trap is that
`#if UNDEFINED_NAME` is also false — an undefined identifier is replaced by `0` — so (a) cannot
distinguish "defined as 0" from "never defined". If that distinction matters, use `#ifdef`, and
enable `-Wundef` to catch accidental reliance on the substitution.

**2.** Two defects, and they compound.

**Defect 1 — the assignment vanishes in release.** `assert` is removed entirely when `NDEBUG` is
defined. The `malloc` call is *inside* the assertion, so in a release build no allocation happens at
all and `p` is never assigned. The program then uses an uninitialised pointer. This is the
side-effect rule: **never put anything with an effect inside `assert`.**

**Defect 2 — `assert` is the wrong mechanism for allocation failure.** `malloc` returning NULL is a
*runtime condition*, not a programmer error. It can legitimately happen and deserves real handling —
an error return, a message, a cleanup path. `assert` calls `abort()`, which terminates without
unwinding, closing files, or flushing buffers.

```c
p = malloc(100);
if (p == NULL) { /* handle it */ }
```

*(A third, minor point: `assert(p = ...)` uses `=` where a reader expects `==`, which GCC flags with
`-Wparentheses`. Even if the semantics were fine, the line is a readability trap.)*

**3.**

- **`TRACE` is defined only when `DEBUG` is.** Without `-DDEBUG` the macro does not exist and
  `TRACE("starting")` is an undefined identifier — a compile error, not a silent no-op. Every
  conditional macro needs an `#else` branch:
  ```c
  #ifdef DEBUG
  #  define TRACE(msg) printf("%s\n", msg)
  #else
  #  define TRACE(msg) ((void)0)
  #endif
  ```
- **`assert(setup() == 0)` has a side effect.** In a release build `setup()` is never called, so the
  program skips its initialisation entirely and fails in some distant, confusing way.
  ```c
  int rc = setup();
  assert(rc == 0);        /* or: if (rc != 0) { handle } */
  ```
- **`TRACE` is a single statement here but is not wrapped in `do { } while (0)`.** It happens to be
  safe as written, but the moment someone adds a second statement to the debug version it breaks
  unbraced `if`/`else` (Lecture 2). Wrap it now.

**4.**

```c
#define ERRORS                                   \
    X(OK,        "no error")                     \
    X(NOMEM,     "out of memory")                \
    X(NOTFOUND,  "not found")                    \
    X(PERM,      "permission denied")

#define X(name, msg) ERR_##name,
enum Error { ERRORS ERR_COUNT };
#undef X

#define X(name, msg) msg,
static const char *error_messages[] = { ERRORS };
#undef X

#define X(name, msg) #name,
static const char *error_identifiers[] = { ERRORS };
#undef X

const char *error_message(int e)
{
    return (e >= 0 && e < ERR_COUNT) ? error_messages[e] : "unknown error";
}

const char *error_name(int e)
{
    return (e >= 0 && e < ERR_COUNT) ? error_identifiers[e] : "ERR_UNKNOWN";
}
```

The third use combines `#` (stringify, Lecture 2) with the X-macro, so `ERR_NOMEM` yields the string
`"NOMEM"` without anyone typing it twice. `ERR_COUNT` comes free from the trailing comma and bounds
both lookups.

Adding an error is **one line**. The enum, both tables, and the count stay consistent by construction.

**When I would reject it in review:** when the list is short and stable.

For four entries that have not changed in two years, the X-macro costs more than it saves. A reader
who has not seen the pattern must decode three `#define X` / `#undef X` cycles to learn what
`ERR_NOMEM` is; `grep ERR_NOMEM` returns nothing useful; and a typo inside the expansion produces an
error message pointing at the `enum` line with no indication which entry is at fault.

The break-even is roughly: **three or more parallel uses, and a list that actually changes.** Below
that, two explicit tables and a comment saying "keep in sync" are more maintainable — and if the
worry is drift, a `_Static_assert` comparing the array length to `ERR_COUNT` catches it at compile
time with none of the obscurity:

```c
_Static_assert(sizeof error_messages / sizeof error_messages[0] == ERR_COUNT,
               "error_messages is out of sync with enum Error");
```

*That last point deserves full credit on its own* — it solves the original problem directly, and it is
the answer a good reviewer would suggest.

---

## Reading

- **C11 §6.10.1** — conditional inclusion
- **C11 §7.2** — `<assert.h>`; note what `NDEBUG` does
- **`man 3 assert`** — short, and the NDEBUG paragraph is the whole story
- **`gcc -dM -E - < /dev/null`** — list every macro GCC predefines; there are hundreds

---

*PROG 101 · Week 10 · Lecture 3 · © CSE Department*
