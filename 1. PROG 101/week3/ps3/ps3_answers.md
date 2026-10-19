# PROG 101 · Week 3 · Problem Set 3 — Written Answers

**Name:** Adebayo Glover · **Set:** Problem Set 3 (Functions, the Call Stack, and Structured Programming)
**Build:** `gcc 15.2.0`, `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`. Outputs are real.

Multi-file library in this folder: `stats.h`, `stats.c`, `main.c`, `Makefile`.

---

## Problem 1 — Functions and Pass-by-Value (22 pts)

### 1.1 Declaration vs. definition (10 pts)

* **Declaration** — gives a name and its type (a *promise* that the thing exists). It generates no code,
  e.g. `double stats_mean(void);`.
* **Definition** — provides the body (functions) or the storage (objects), e.g. the full
  `double stats_mean(void) { ... }`.

A program is **valid with only a declaration visible** at the point of use: `main.c` compiles a call to
`stats_mean()` with just `stats.h`'s declaration, because the compiler only needs the type to emit the
call and check the arguments. The **definition must exist by link time** — when all the object files
are combined. If it never does, the compiler is happy but the *linker* fails with `undefined reference`.

### 1.2 Can the caller observe the change? (12 pts)

| Case | Observable? | Why |
|---|---|---|
| (a) assigns to its `int` parameter | **No** | The parameter is a *copy* in the callee's own frame; writing it never touches the caller's variable. |
| (b) assigns to a `static` local | **Not directly**, but its value **persists** into the next call | The name is invisible outside the function, but the object lives for the whole run, so the update is still there on the next call (e.g. a call counter). |
| (c) assigns to a global | **Yes** | There is exactly one file-scope object; any function assigning it changes what every other function sees. |
| (d) returns a value the caller assigns | **Yes** | The change travels back **through the returned value only** — the caller must capture it. |

---

## Problem 2 — Scope and Storage Duration (10 pts)

| Declaration | Scope | Storage duration | Initialised to |
|---|---|---|---|
| `int x;` inside a function | **block** (the function) | **automatic** (created/destroyed each call) | **indeterminate** (garbage) |
| `static int x;` inside a function | **block** (unchanged) | **static** (whole program run) | **0** |
| `static int x;` at file level | **file**, with **internal linkage** | **static** | **0** |
| `int x;` at file level | **file**, with **external linkage** | **static** | **0** |

The two `static` rows that matter: at block scope, `static` changes the **storage duration** (not the
scope); at file scope, `static` changes the **linkage** (internal, so other translation units cannot
see it). Objects with static storage duration are zero-initialised before `main` runs; automatic
objects are not.

---

## Problem 3 — A Multi-File Program (40 pts)

### 3.1 / 3.3 — Implementation and driver

`stats.c` keeps a `count`, a running `sum`, a running `sum_sq`, and the smallest/largest values, all in
**file-level `static`** variables (private to the file, alive for the whole run). It has one file-private
helper `square`. `main.c` feeds the eight values one at a time (no arrays yet) and prints 6 dp:

```
count    8
mean     5.000000
variance 4.571429
stddev   2.138090
min      2.000000
max      9.000000
```

These match the expected values exactly (and Python's `statistics.variance` for the same data).

### 3.2 — `stats.h` and the include guard (6 pts)

`stats.h` wraps the declarations in

```c
#ifndef STATS_H
#define STATS_H
/* ... declarations ... */
#endif
```

**What breaks without it:** if a translation unit includes the header twice — directly *and* via another
header — every declaration is processed twice. For mere function declarations that is usually harmless,
but for anything with a definition (a `struct`, an `enum`, a `static inline` function, a `#define`
object) it is a hard `redefinition` error. The guard makes the second inclusion a no-op. (Demonstrated:
a header with `struct point { ... };` included twice gives `error: redefinition of 'struct point'`;
with the guard it compiles clean.)

### 3.4 — `Makefile` dependencies (8 pts)

```
stats: main.o stats.o
	$(CC) $(CFLAGS) -o $@ main.o stats.o -lm
main.o:  main.c  stats.h
	$(CC) $(CFLAGS) -c main.c -o $@
stats.o: stats.c stats.h
	$(CC) $(CFLAGS) -c stats.c -o $@
```

Both objects list `stats.h` as a prerequisite. Demonstrated:

* `touch stats.h; make` → **both** `main.c` and `stats.c` recompile, then relink:
  ```
  gcc ... -c main.c  -o main.o
  gcc ... -c stats.c -o stats.o
  gcc ... -o stats main.o stats.o -lm
  ```
* `touch main.c; make` → **only** `main.o` recompiles, then relink:
  ```
  gcc ... -c main.c -o main.o
  gcc ... -o stats main.o stats.o -lm
  ```
* unchanged → `make: 'stats' is up to date.`

---

## Problem 4 — Contracts and Defensive Programming (14 pts)

### 4.1 Precondition, postcondition, invariant (8 pts)

For `stats_mean`:

* **Precondition:** `count > 0` — at least one value has been added since the last reset.
* **Postcondition:** the function returns `sum / count` (the arithmetic mean of the values added).

**Invariant between calls:** `count` values have been added since the last reset; `sum` is their total
and `sum_sq` the total of their squares; so `mean == sum / count`, and with `count > 0`,
`lowest ≤ mean ≤ highest`. (These are written as comments in `stats.c`.)

### 4.2 Assertion vs. not (6 pts)

* **Should be an assertion:** `count > 0` in `stats_mean` (and `stats_min`/`stats_max`), plus
  `count > 1` in `stats_variance`. Asking for the mean of an empty set is a **programmer error** — the
  code is wrong, and there is no sensible recovery.
* **Should NOT be an assertion:** handling a **non-numeric value typed by a user** at runtime. That is
  an *expected* condition, not a bug: it needs real error handling and must still work in a `-DNDEBUG`
  (release) build, where assertions are compiled out entirely. (Likewise, never put code with a **side
  effect** inside an `assert` — `-DNDEBUG` deletes the whole expression.)

---

## Problem 5 — Structured Programming (14 pts)

### 5.1 The Böhm–Jacopini theorem (7 pts)

The theorem states that **every computable function can be expressed using only three control
structures: sequence, selection (`if`/`switch`), and iteration (`while`/`for`/`do`)**. Its consequence
for `goto`: since these three suffice, unrestricted `goto` is **never necessary** — any `goto` program
can be rewritten without it. This is the theoretical basis of structured programming.

### 5.2 Rewrite using only sequence, selection, iteration (7 pts)

```c
int total = 0;
for (int i = 0; i < n; i++) {
    if (i % 3 == 0) {
        continue;
    }
    total += i;
}
printf("%d\n", total);
```

The `goto loop`/`goto done` becomes a `for` (iteration), and `if (i % 3 == 0) goto skip` becomes an
`if` + `continue` (selection). Verified for `n = 10`: `1 + 2 + 4 + 5 + 7 + 8 = 27`, identical to the
`goto` version.

---

*PROG 101 · Week 3 · Problem Set 3 · Adebayo Glover*
