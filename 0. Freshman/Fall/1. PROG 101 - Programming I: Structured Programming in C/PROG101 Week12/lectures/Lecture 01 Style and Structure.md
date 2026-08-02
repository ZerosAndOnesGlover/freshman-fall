# PROG 101 Programming I: Structured Programming in C
## Week 12 · Lecture 1: Style, Readability, and Structure

---

## Lecture Goals

By the end of this lecture you can:

- Justify a style rule by what it does for the *reader*, not by taste
- Choose names that carry information, and say why a comment is not a substitute
- Organise a C project into modules with deliberate interfaces
- Recognise the specific structural defects that make C code hard to change

---

## 1. Why This Is the Last Week

Eleven weeks taught you what C *does*. This week is about what you should do with it — and it comes
last because style rules are meaningless until you have written enough code to have been hurt by
their absence.

The premise, and everything else follows from it:

> **Code is read far more often than it is written.** Every line you write, you or someone else will
> read many times — debugging it, extending it, deciding whether it can be deleted.

That reframes every style question. "Which brace style is better?" is unanswerable. "Which brace
style does this project already use?" has an answer, and it is the one that matters.

---

## 2. Names

Naming is the cheapest documentation available and the most often wasted.

**Length should scale with scope.**

```c
for (int i = 0; i < n; i++)      /* fine: i lives for three lines */
int i;                            /* at file scope: theft from the reader */
```

A one-letter name in a three-line loop is clear. The same name spanning 200 lines forces the reader
to search for its declaration.

**Say what it *is*, not what type it is.**

```c
int  iCount;          /* Hungarian notation -- the compiler knows the type */
int  count;           /* better                                            */
int  retry_count;     /* better still: count of what?                      */
```

**Booleans read as assertions.**

```c
if (check_file(f))    /* checks it for... what? and returns what?  */
if (file_is_open(f))  /* the call site now reads as English         */
```

**Functions are verbs; the name should predict the return value.**

```c
size_t list_length(const List *l);      /* returns a length     */
int    list_insert(List *l, int v);     /* returns a STATUS     */
```

That second one matters. A caller who assumes `list_insert` returns the inserted value will not
check for failure.

### Consistency beats preference

In an existing codebase, **match the surrounding style even where you would have chosen otherwise**.
A file with two conventions is harder to read than a file with either one consistently. This is the
single most useful style rule and the one most often ignored by newcomers.

---

## 3. Comments

**Comments should say *why*, not *what*.**

```c
i += 1;                      /* increment i        -- worthless   */
i += 1;                      /* skip the header row -- the reason  */
```

The code already states what happens. Only you know why.

The comments genuinely worth writing:

| Comment | Why it earns its place |
|---|---|
| `/* CALLER MUST FREE. */` | The ownership contract exists nowhere else |
| `/* Retry once: the API returns EAGAIN on first call after idle. */` | A scar; deleting the retry re-creates the outage |
| `/* O(n²) but n <= 8 here. */` | Pre-empts a "fix" that would add complexity for nothing |
| `/* Assumes `a` is sorted -- see caller. */` | A precondition the type cannot express |

**A comment that repeats the code is worse than none**, because it must be maintained and will
eventually contradict the code. When they disagree, readers believe the comment and are wrong.

**Commented-out code should be deleted.** Version control remembers it; the file should not.

---

## 4. Functions

**One function, one job** — because a function that does one thing can be *named* accurately, and an
accurate name means the next reader need not read the body.

Signs a function is doing too much:

- You cannot name it without "and"
- It needs a comment to explain its sections
- It takes a boolean parameter that selects between two behaviours

That last one is worth expanding:

```c
void save(const Record *r, int as_binary);    /* two functions wearing a trenchcoat */

void save_text(const Record *r);              /* clearer at every call site */
void save_binary(const Record *r);
```

`save(r, 1)` tells the reader nothing. `save_binary(r)` tells them everything.

**Length is a symptom, not the disease.** A 60-line function that does one thing linearly is fine. A
20-line function with four nested conditionals and three responsibilities is not. Judge by
cohesion, not line count.

**Return early to reduce nesting.**

```c
int process(const char *path)          /* guard clauses first */
{
    if (!path)          return -1;
    FILE *f = fopen(path, "r");
    if (!f)             return -1;
    /* the main work, at one level of indentation */
    fclose(f);
    return 0;
}
```

The alternative — wrapping the body in `if (path) { if (f) { … } }` — pushes the interesting code
rightward and puts the error handling far from the check.

**Caveat:** early returns and manual cleanup interact badly. Once a function holds two resources, the
`goto cleanup` idiom is usually clearer than repeating `fclose(f)` in four branches:

```c
int process(const char *path)
{
    int rc = -1;
    FILE *f = fopen(path, "r");
    if (!f) goto done;
    char *buf = malloc(1024);
    if (!buf) goto close_f;
    /* work */
    rc = 0;
    free(buf);
close_f:
    fclose(f);
done:
    return rc;
}
```

This is one of the few places `goto` is idiomatic C, and it exists because C has no destructors.

---

## 5. Modules

A module is a `.h`/`.c` pair with a deliberate interface.

**The header is the interface; the `.c` file is the implementation.** Everything not in the header
should be `static`:

```c
/* vec.c */
static void grow(Vec *v);        /* file-private: not in vec.h */
int vec_push(Vec *v, int x);     /* public: declared in vec.h  */
```

`static` at file scope means *internal linkage* — the name is invisible to other translation units.
It shrinks your interface, prevents accidental coupling, and lets the compiler optimise more
aggressively because it knows every caller.

**Design the header first.** If the interface is awkward to use, the implementation cannot rescue it.
Write the calls you *want* to make, then make them work.

### Naming across a module

C has no namespaces, so prefix consistently:

```c
vec_init, vec_push, vec_at, vec_free
```

The prefix is the namespace. It also makes the module greppable, which matters more than it sounds.

---

## 6. What Good Structure Buys

The concrete payoff, in the terms this course has used all term:

| Practice | What it prevents |
|---|---|
| One job per function | The 200-line `main` nobody dares touch |
| `static` on internals | Another file depending on something you meant to change |
| Ownership in a comment | Week 6's leaks and double frees |
| Consistent prefixes | Name collisions, and unfindable code |
| Guard clauses | Deep nesting that hides the error paths |
| `goto cleanup` | The Week 6 error-path leak |

None of this is aesthetic. Every item on that list corresponds to a bug you have already met.

---

## 7. Summary

| Idea | Takeaway |
|---|---|
| The premise | Code is read far more than written |
| Name length | Scales with scope |
| Boolean names | Read as assertions: `file_is_open` |
| Function names | Predict the return value |
| **Consistency** | Beats personal preference in an existing codebase |
| Comments | Say **why**; a comment repeating the code will drift and lie |
| Delete commented-out code | Version control remembers it |
| One job per function | So it can be named accurately |
| Boolean parameters | Usually two functions in disguise |
| Guard clauses | Keep the main path at one indentation level |
| `goto cleanup` | Idiomatic in C precisely because there are no destructors |
| `static` on internals | Shrinks the interface; prevents coupling |
| Prefixes | C has no namespaces |

---

## Practice Exercises

**1. (Critique.)** Give three specific defects, each with a fix.

```c
int p(char *s, int f) {
    int r = 0;
    if (s != NULL) { if (strlen(s) > 0) { if (f == 1) { r = strlen(s); } else { r = 1; } } }
    return r;
}
```

**2. (Explain.)** Why is `void save(const Record *r, int as_binary)` usually worse than two
functions? Answer in terms of the **call site**.

**3. (Build.)** Design the header for a `Stack` module holding `int`s. Give the type, four
operations, and the ownership contract. Do not implement it.

**4. (Stretch.)** A colleague argues that `goto` should never appear in C. Give the strongest case
for the `goto cleanup` idiom, the strongest case against, and say what you would do.

### Answers

**1.** Three of several:

- **Names carry no information.** `p`, `s`, `f`, `r` tell the reader nothing. → `str_length_or_flag`
  is still bad because the *function* does two things; see below.
- **The function does two unrelated things** selected by a flag. `f == 1` returns the length,
  otherwise 1. That is two functions. → split them.
- **Triple nesting for what are guard conditions.** → invert into early returns.
- *(Also acceptable:* `strlen` is called twice, and the parameter should be `const char *`.)

```c
size_t nonempty_length(const char *s)
{
    if (s == NULL) return 0;
    return strlen(s);            /* an empty string already gives 0 */
}
```

**2.** Because at the **call site**, `save(r, 1)` is unreadable. The reader must find the declaration
to learn what `1` means, and nothing stops them writing `save(r, 2)`. `save_binary(r)` states the
intent where it is used, cannot be passed a meaningless value, and lets the compiler catch a
misspelling.

The general rule: **a boolean parameter moves information out of the call site and into the
declaration**, which is exactly the wrong direction.

**3.**

```c
#ifndef STACK_H
#define STACK_H

#include <stddef.h>

typedef struct Stack Stack;          /* opaque: callers cannot see the fields */

/* Returns a new empty stack, or NULL on allocation failure.
   CALLER MUST call stack_free. */
Stack *stack_new(void);

/* Pushes v. Returns 0 on success, -1 on allocation failure. */
int    stack_push(Stack *s, int v);

/* Pops into *out. Returns 0 on success, -1 if the stack is empty. */
int    stack_pop(Stack *s, int *out);

/* Number of elements. */
size_t stack_size(const Stack *s);

/* Frees the stack. Safe to call with NULL. */
void   stack_free(Stack *s);

#endif /* STACK_H */
```

**The marking points:** the include guard; the **opaque type** (`typedef struct Stack Stack;` with
the definition hidden in the `.c`, so callers cannot depend on the layout); `const` on the read-only
operation; status returns rather than values, so failure is reportable; and the ownership contract
stated in comments. `stack_pop` returning through an out-parameter is the Week 5 write-back idiom —
it keeps the return value free to signal emptiness.

**4. For:** C has no destructors and no exceptions. A function acquiring several resources must
release them on every exit path, and without `goto` you either duplicate the cleanup in each branch
— where one copy will eventually be wrong or missing — or nest the body so deeply it becomes
unreadable. `goto cleanup` gives **one** exit path with **one** copy of the cleanup, in reverse
acquisition order. It is used throughout the Linux kernel and glibc for exactly this reason.

**Against:** `goto` can express arbitrary control flow, and the arguments that killed it in the 1960s
were about jumping backwards and into blocks. Once a codebase accepts `goto` for cleanup, the door
is open to less disciplined uses, and reviewers must judge each case rather than applying a rule.
C also restricts it — you cannot jump over a variable's initialisation — so it interacts awkwardly
with declarations mid-block.

**What I would do:** allow `goto` for **forward jumps to a cleanup label at the end of the same
function**, and forbid every other use. That is the narrow, well-understood pattern; it is checkable
in review by a single question ("does it jump forward to a cleanup label?"); and it solves a real
problem that the alternatives solve worse. A blanket ban trades a genuine class of resource-leak
bugs for adherence to a rule whose original justification does not apply.

---

## Reading

- **Kernighan & Pike, *The Practice of Programming*, Ch. 1** — style; short and unmatched
- **Linux kernel `Documentation/process/coding-style.rst`** — opinionated, and §7 is on `goto`
- **Ousterhout, *A Philosophy of Software Design*** — on interfaces and complexity

---

*PROG 101 · Week 12 · Lecture 1 · © CSE Department*
