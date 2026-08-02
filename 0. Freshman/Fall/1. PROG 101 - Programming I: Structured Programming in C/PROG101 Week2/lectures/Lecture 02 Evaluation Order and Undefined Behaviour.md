# PROG 101 · Programming I: Structured Programming in C
## Week 2 · Lecture 2: Evaluation Order and Undefined Behaviour

---

## Lecture Goals

By the end of this lecture you can:

- Distinguish **undefined**, **unspecified**, and **implementation-defined** behaviour, and say why
  the difference matters
- Predict which parts of an expression have a guaranteed evaluation order and which do not
- Recognise the classic sequence-point bugs before the compiler warns you
- Explain why "it worked on my machine" is not evidence that code is correct

---

## 1. Three Kinds of "It Depends"

Lecture 1 gave you operators. This lecture is about what the standard promises when you combine
them — and, more importantly, what it refuses to promise.

C defines three distinct categories, and conflating them is the source of endless confusion:

| Category | The standard says | Example | Can you rely on it? |
|---|---|---|---|
| **Implementation-defined** | Each implementation must **choose and document** a behaviour | Whether `char` is signed | Yes, *for one compiler*, if you read its docs |
| **Unspecified** | Two or more behaviours are allowed; no documentation required, and it may differ between two occurrences in the same program | Argument evaluation order | **No** |
| **Undefined** | **No requirements whatsoever** | Signed overflow, `i = i++` | **Absolutely not** |

The gradient runs from "portable if you check" through "never rely on it" to "your program has no
meaning."

**Undefined behaviour is the dangerous one**, and not for the reason most people assume. The danger
is not that you get a wrong value. It is that the compiler is *entitled to assume UB never happens*,
and optimises on that assumption. You saw this in Week 1: an overflow check written as
`if (x + 1 < x)` gets deleted entirely, because in a program without UB it could never be true.

A program with UB does not have "a bug in one place." It has no defined meaning at all, and the
consequences can appear arbitrarily far from the cause.

---

## 2. Evaluation Order Is Mostly Unspecified

Here is the fact that surprises people. Given:

```c
printf("%d %d %d\n", f(), g(), h());
```

**C does not specify the order in which `f`, `g`, and `h` are called.**

Verified on this machine, with each function logging when it runs:

```
f=10 g=20 h=30
actual call order was: 3 2 1        <- h, then g, then f
```

GCC evaluated the arguments **right to left**. That is entirely conforming. Another compiler — or
the same compiler at a different optimisation level — may choose left to right.

Now the same functions in a different context:

```c
int r = f() + g();
```

```
f() + g() = 30, evaluated in order: 1 2      <- left to right
```

**Different order, same program.** This is exactly what "unspecified" permits: no consistency is
required, not even within one compilation.

> **This is not a hypothetical hazard.** A test harness written for this course once printed
> `ht_remove(t,"a")` and `ht_remove(t,"b")` in a single `printf`, and reported the results in the
> wrong order — because the arguments were evaluated right to left while the output columns were
> labelled left to right. The bug was in the *test*, and it looked exactly like a bug in the hash
> table.

**The rule to internalise:** if two subexpressions have side effects, do not put them in one
expression. Sequence them into separate statements:

```c
int a = ht_remove(t, "a");     /* now the order is yours, not the compiler's */
int b = ht_remove(t, "b");
printf("%d %d\n", a, b);
```

---

## 3. What *Is* Guaranteed

Four operators impose a guaranteed order. Memorise them; everything else is unspecified.

| Operator | Guarantee |
|---|---|
| `&&` | Left operand fully evaluated first; right operand **not evaluated** if left is false |
| `\|\|` | Left operand first; right **not evaluated** if left is true |
| `?:` | Condition first; **exactly one** branch evaluated |
| `,` (comma operator) | Left fully evaluated and discarded, then right |

Verified:

```
'0 && f()' called f?  NO       <- short-circuit guaranteed
'1 || f()' called f?  NO       <- short-circuit guaranteed
comma (f(), g()) = 20, order: 1 2   <- left-to-right guaranteed
```

### Short-circuit is a correctness tool, not an optimisation

This idiom depends entirely on the guarantee:

```c
if (p != NULL && *p == 5) { ... }
```

Verified: with `p == NULL`, the dereference **does not happen**. If `&&` evaluated both sides, this
would crash. The same shape appears everywhere:

```c
if (i < n && a[i] == target)          /* bounds check before access */
if (node != NULL && node->next != NULL)
if (denom != 0 && total / denom > 1)  /* avoid division by zero */
```

**Order matters and cannot be swapped.** Writing `if (*p == 5 && p != NULL)` is a null dereference
with a useless check after it.

### `sizeof` does not evaluate its operand

```c
size_t sz = sizeof(f());     /* f is NEVER called */
```

Verified: `sizeof(f())` yields 4 and `f` is not called. `sizeof` needs only the *type* of the
expression, which is known at compile time. So `sizeof(a++)` does not increment `a` — a genuine trap
if you expect it to.

*(The one exception is a variable-length array type, where the size expression is evaluated at run
time. You will not meet that until Week 4.)*

---

## 4. Sequence Points and the Classic Bugs

A **sequence point** is a moment where all side effects so far are complete. They occur at the end of
a full statement (`;`), at `&&`, `||`, `?:`, `,`, and before a function call's body runs.

> **A note on terminology.** C11 replaced "sequence point" with a more precise *sequenced-before*
> relation. The older term is still what everyone says, and it is what GCC's warning is called
> (`-Wsequence-point`), so it is worth knowing both.

The rule: **modifying an object more than once between sequence points, or modifying it and
separately reading it, is undefined behaviour.**

### The classics

```c
int i = 5;
i = i++ + 1;          /* UNDEFINED: i modified twice */
a[i] = i++;           /* UNDEFINED: i read and modified, no sequencing */
f(i++, i++);          /* UNDEFINED */
i = i++;              /* UNDEFINED */
```

These are not "produces a surprising value." They are undefined — the program has no meaning.
Compilers have been known to produce `6`, `7`, or code that does something else entirely.

**GCC catches the common forms.** Verified:

```
warning: operation on 'i' may be undefined [-Wsequence-point]
    i = i++ + 1;
warning: operation on 'i' may be undefined [-Wsequence-point]
    a[i] = i++;
```

Note the wording: *may be* undefined. The compiler cannot always prove it, so the warning is
best-effort — it will not catch every case, particularly through pointers or across function
boundaries. **`-Wall -Wextra -Werror` turns the ones it does catch into build failures**, which is
precisely why this course mandates them.

### What is perfectly fine

```c
i++;  j = i;          /* separate statements: sequenced by ; */
a[j] = i++;           /* different objects: fine */
f(i); i++;            /* sequenced */
x = i++ + j++;        /* fine: i and j are distinct objects */
```

The rule is about **the same object** being touched twice without sequencing. Two different variables
in one expression are no problem.

---

## 5. Undefined Behaviour You Have Already Met

A partial inventory, to make the pattern visible:

| Operation | Why it is UB |
|---|---|
| Signed integer overflow | Week 1 — the compiler assumes it cannot happen |
| Integer division by zero | No meaningful result exists |
| `INT_MIN / -1`, `-INT_MIN` | The result is not representable |
| Shifting by ≥ the width | `x << 32` on a 32-bit `int` |
| Shifting a negative left | `-1 << 1` |
| Reading an uninitialised variable | Its value is indeterminate |
| Dereferencing NULL or a dangling pointer | Week 5 |
| Array access out of bounds | Week 4 |
| Modifying a string literal | `char *s = "hi"; s[0] = 'H';` |
| Falling off the end of a non-`void` function | No return value exists |

Note that **floating-point division by zero is *not* UB** — verified, `1.0/0.0` is `inf`, defined by
IEEE 754. Integer division by zero is. The asymmetry catches people.

### The tools

You cannot rely on reading code carefully; UB is designed to be invisible.

```bash
gcc -Wall -Wextra -Werror -pedantic -std=c11 prog.c    # compile-time
gcc -fsanitize=undefined -g prog.c                     # run-time (UBSan)
gcc -fsanitize=address -g prog.c                       # memory errors (ASan)
valgrind --leak-check=full ./prog                      # leaks and bad accesses
```

UBSan reports at the exact line:

```
runtime error: signed integer overflow: 2147483647 - -2 cannot be represented in type 'int'
```

**Use them from the start of every assignment**, not after something breaks. UB that happens to work
today breaks when you change optimisation level, compiler, or platform — and by then you will have
forgotten the code.

---

## 6. Why "It Worked" Proves Nothing

The deepest lesson of the lecture.

A program with undefined behaviour can:

- work correctly for years, then break when you upgrade the compiler
- work at `-O0` and fail at `-O2`
- work on x86 and fail on ARM
- work in the test and fail in the caller

None of these are the compiler "breaking your code." The code had no defined meaning; one
interpretation happened to match your intent, and then it stopped.

**Testing cannot establish the absence of UB.** A test exercises one path with one input on one
build. UB is a property of the *program text*, not of any particular run. This is why the sanitizers
matter: they check the property directly rather than sampling behaviours.

You will meet the formal version of this limit much later — that no tool can decide all program
properties. For now, the practical version suffices: **turn on every check the compiler offers, and
treat a warning as a defect.**

---

## 7. Summary

| Idea | Takeaway |
|---|---|
| Implementation-defined | Documented per compiler; portable if you check |
| Unspecified | Several behaviours allowed, may differ between occurrences |
| **Undefined** | **No meaning at all**; the compiler assumes it cannot happen |
| Argument order | **Unspecified** — verified right-to-left here for `printf` |
| Same program, different order | `f()+g()` went left-to-right; nothing is consistent |
| Guaranteed order | `&&`, `\|\|`, `?:`, `,` — and nothing else |
| Short-circuit | A **correctness** tool: `p && *p` is the standard null guard |
| `sizeof` | Does not evaluate its operand |
| Sequence-point rule | Do not modify an object twice, or read-and-modify, without sequencing |
| `-Wsequence-point` | Catches the common forms; "may be undefined" means best-effort |
| Float ÷ 0 | Defined (`inf`); **integer ÷ 0 is UB** |
| "It worked" | Not evidence — UB is a property of the text, not the run |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Classify.)** For each, say undefined, unspecified, or implementation-defined:
(a) whether `char` is signed  (b) the order `f()` and `g()` are called in `f() + g()`
(c) `INT_MAX + 1`  (d) the size of `int`  (e) `arr[10]` on a 10-element array

**2. (Trace.)** What does this print, and what is wrong with the question?

```c
int i = 0;
printf("%d %d\n", i++, i++);
```

**3. (Fix.)** Three problems.

```c
int i = 0, a[5] = {0};
a[i] = i++;
if (a[i] != 0 && i < 5) process(a[i]);
int n = 10, d = 0;
printf("%d\n", n / d);
```

**4. (Stretch.)** This function looks correct and is not. Find the undefined behaviour, explain why a
test would likely pass, and fix it.

```c
int sum_to(int n)
{
    int total = 0;
    for (int i = 1; i <= n; i++) total += i;
    return total;
}
```

### Answers

**1.**

| | Category | Why |
|---|---|---|
| **(a)** `char` signedness | **Implementation-defined** | Each compiler chooses and documents it. Signed on x86 GCC, unsigned on ARM |
| **(b)** order of `f()`, `g()` | **Unspecified** | Several orders allowed, no documentation required, may differ between occurrences |
| **(c)** `INT_MAX + 1` | **Undefined** | Signed overflow — no requirements at all |
| **(d)** `sizeof(int)` | **Implementation-defined** | Must be documented; minimum range guaranteed |
| **(e)** `arr[10]` on 10 elements | **Undefined** | Out-of-bounds access |

The (a)/(d) vs (b) distinction is the point: implementation-defined facts are *stable and knowable*
for your compiler; unspecified ones are not stable even within one program.

**2.** **The question is unanswerable, and that is the answer.**

`i++` appears twice with no sequence point between them, so `i` is modified twice between sequence
points — **undefined behaviour**. The program has no defined output.

You may observe `0 1`, or `1 0`, or `0 0`, or something else. Two separate mistakes are possible in
reasoning about it: assuming a left-to-right argument order (unspecified, §2), *and* assuming the
increments are sequenced at all (they are not, §4). Even knowing the evaluation order would not make
this defined.

GCC warns: `operation on 'i' may be undefined`.

The fix is to sequence explicitly:

```c
int a = i++;
int b = i++;
printf("%d %d\n", a, b);
```

**3.**

- **`a[i] = i++;` is undefined.** `i` is read (to index `a`) and modified in the same expression with
  no sequencing. → split it:
  ```c
  a[i] = i;
  i++;
  ```
  *(Or `a[0] = 0; i = 1;` — but the point is to sequence, not to guess the intended value.)*

- **The `&&` operands are in the wrong order.** `a[i]` is evaluated *before* `i < 5` is checked, so
  the bounds test happens too late and cannot protect anything. → `if (i < 5 && a[i] != 0)`.
  This is the §3 idiom: **the guard must come first.**

- **`n / d` with `d == 0` is undefined** — integer division by zero, unlike the floating-point case.
  → check first:
  ```c
  if (d != 0) printf("%d\n", n / d);
  else        printf("undefined\n");
  ```

**4.** The UB is **signed integer overflow** in `total += i`.

For `n` around 65,536 the sum exceeds `INT_MAX` (2,147,483,647) — since the sum is n(n+1)/2, overflow
begins near n = 65,536. Beyond that, `total += i` overflows and the function has no defined meaning.

**Why a test passes.** Nobody tests `sum_to` with 70,000. The natural tests are `sum_to(10) == 55`,
`sum_to(100) == 5050`, maybe `sum_to(0) == 0`. All correct, all far below the threshold. The function
looks obviously right — it *is* the textbook loop — and the bug lives only in a range nobody thinks
to try.

Worse, the overflow is not merely a wrong number: the compiler may optimise assuming it cannot occur,
so behaviour at `-O2` can differ from `-O0`, and a debug build may "pass" while the release build
does not.

**Fixes**, in increasing order of rigour:

```c
long long sum_to(int n)                    /* 1. widen the accumulator */
{
    long long total = 0;
    for (int i = 1; i <= n; i++) total += i;
    return total;
}

int sum_to(int n, int *out)                /* 2. detect and report */
{
    int total = 0;
    for (int i = 1; i <= n; i++)
        if (__builtin_add_overflow(total, i, &total)) return -1;
    *out = total;
    return 0;
}
```

*Also worth noting:* the closed form `n*(n+1)/2` is O(1) instead of O(n) — but it overflows *sooner*,
because `n*(n+1)` exceeds `INT_MAX` around n = 46,341, before the sum itself would. Replacing a loop
with a formula does not remove the overflow question; it moves it.

*Full marks require identifying that the test suite would pass.* The exercise is about why UB
survives testing, not about spotting an overflow.

---

## Reading

- **C11 §3.4** — the definitions of undefined, unspecified, and implementation-defined
- **C11 §6.5 ¶2** — the sequencing rule for modifying objects
- **Annex J** — the standard's own catalogue of UB. Skim it; the length is the lesson
- **Regehr, "A Guide to Undefined Behavior in C and C++"** — all three parts, genuinely readable

---

*PROG 101 · Week 2 · Lecture 2 · © CSE Department*
