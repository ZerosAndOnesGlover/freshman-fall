# PROG 101 · Programming I: Structured Programming in C
## Week 3 · Problem Set 3: Functions, the Call Stack, and Structured Programming

**Released:** Friday, Week 3 · **Due:** Friday, Week 4 at 17:00
**Total:** 100 points

**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`

---

## Problem 1: Functions and Pass-by-Value (20 pts)

**1.1** *(6)* Explain the difference between a function **declaration** and a **definition**. Give an
example of a program that is valid with only a declaration visible, and say when the definition must
exist.

**1.2** *(6)* This function does not do what its name suggests:

```c
void swap(int a, int b) { int t = a; a = b; b = t; }
```

Demonstrate the failure with a `main` that prints the addresses of the caller's variables and of the
parameters. Explain the failure **using those addresses**. Do not attempt to fix it — the fix needs
Week 5.

**1.3** *(8)* For each, state whether the caller can observe the change, and why:

(a) a function that assigns to its `int` parameter
(b) a function that assigns to a `static` local
(c) a function that assigns to a global
(d) a function that returns a value the caller assigns

---

## Problem 2: The Call Stack, Scope, and Storage Duration (25 pts)

**2.1** *(8)* Write `frames.c` with four nested functions, each printing the address of one local.
Tabulate the addresses, state whether the stack grows up or down on your machine, and give the
distance between consecutive frames.

**2.2** *(6)* Complete this table:

| Declaration | Scope | Storage duration | Initialised to |
|---|---|---|---|
| `int x;` inside a function | | | |
| `static int x;` inside a function | | | |
| `static int x;` at file level | | | |
| `int x;` at file level | | | |

**2.3** *(6)* `counter()` below returns 1, 2, 3, 4 on successive calls while `automatic()` returns 1
every time. `n` is invisible outside both functions. State precisely what `static` changed.

```c
int counter(void)   { static int n = 0; return ++n; }
int automatic(void) {        int n = 0; return ++n; }
```

**2.4** *(5)* Stack depth is finite. Write a program that recurses without a base case, run it, and
report how it terminates and at roughly what depth. Then state why an infinite *loop* does not fail
the same way.

---

## Problem 3: A Multi-File Program (30 pts)

Build a `stats` library across translation units.

**`stats.h`** must declare exactly:

```c
double mean(const double *v, int n);
double variance(const double *v, int n);
double stddev(const double *v, int n);
int    minmax(const double *v, int n, double *out_min, double *out_max);
```

**3.1** *(12)* Implement `stats.c`. `variance` must use the **two-pass** algorithm (compute the mean,
then sum squared deviations), and must be a **sample** variance with denominator `n - 1`.
`minmax` returns `0` on success and `-1` if `n <= 0`.

**3.2** *(4)* Write `stats.h` with a correct include guard. Explain what breaks without it.

**3.3** *(6)* Make at least one helper in `stats.c` `static`. Then write a separate file that
declares that helper and calls it. Compile and link; record the **exact** error and state which
build stage produced it.

**3.4** *(4)* Write `main.c` exercising all four functions on the dataset
`{2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0}`, printing results to 6 decimal places.

**3.5** *(4)* Write a `Makefile` with correct dependencies so that touching `stats.h` rebuilds both
objects but touching `main.c` rebuilds only one. Demonstrate both cases.

---

## Problem 4: Contracts and Defensive Programming (15 pts)

**4.1** *(5)* State a **precondition**, a **postcondition**, and a **loop invariant** for your
`mean` function, and add them as comments.

**4.2** *(5)* Add `assert` for the preconditions of `mean` and `variance`. Show one firing, and show
that `-DNDEBUG` removes it.

**4.3** *(5)* Assertions are for programmer errors, not user errors. Give one condition in your
`stats` library that **should** be an assertion and one that should **not**, and justify each.

---

## Problem 5: Structured Programming (10 pts)

**5.1** *(5)* State the Böhm–Jacopini theorem and explain what it claims about `goto`.

**5.2** *(5)* Rewrite this using only sequence, selection, and iteration:

```c
int i = 0;
loop:
    if (i >= n) goto done;
    if (a[i] < 0) goto skip;
    total += a[i];
skip:
    i++;
    goto loop;
done:
    return total;
```

---

## Grading

| Problem | Points | Focus |
|---|---|---|
| 1: Functions and pass-by-value | 20 | The most important rule in C |
| 2: Call stack, scope, storage duration | 25 | Where variables live and for how long |
| 3: Multi-file program | 30 | Header discipline, linkage, separate compilation |
| 4: Contracts | 15 | Assertions as executable documentation |
| 5: Structured programming | 10 | Why three control structures suffice |
| **Total** | **100** | |

**Automatic deductions:** any compiler warning (−3 each); a header without an include guard (−5).

---

*PROG 101 · Week 3 · Problem Set 3 · © CSE Department*
