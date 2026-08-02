# PROG 101 · Programming I: Structured Programming in C
## Week 11 · Lecture 1: Function Pointers — Code as Data

---

## Lecture Goals

By the end of this lecture you can:

- Read and write function-pointer declarations without guessing
- Explain why `int *f(int)` and `int (*f)(int)` are completely different things
- Build a dispatch table and say when it beats a `switch`
- Pass a function to a function, which is the foundation of everything in Weeks 8–9

---

## 1. The Idea

You have spent seven weeks moving **data** around with pointers. A pointer holds an address; the
address names a byte in memory; you dereference to get the value.

Functions also live in memory. They are sequences of machine instructions at some address. So a
pointer can name a function just as easily as it can name an `int`.

That single fact is what lets C do things it otherwise could not:

- `qsort` sorts *anything*, because you hand it the comparison
- A state machine dispatches through a table instead of a 40-case `switch`
- A library calls *your* code without its author ever knowing your function's name

In Week 7 you built linked lists that held `int`. Today begins the work of building one list that
holds anything, and by Lecture 3 you will have it.

---

## 2. Declaration Syntax

Here is the declaration that trips everyone:

```c
int (*p)(int, int);
```

`p` is a **pointer to a function taking two `int`s and returning `int`**.

The parentheses around `*p` are load-bearing. Remove them:

```c
int *f(int, int);     /* a FUNCTION taking two ints, returning int*  */
int (*p)(int, int);   /* a POINTER to a function returning int       */
```

These declare entirely different things. The first is a function; the second is a variable.

### The right-left rule

Start at the identifier, go **right** when you can, **left** when you must, and let parentheses
override:

```
int (*p)(int, int);
      ^              start at p
     (*p)            p is a pointer          (parens force us left first)
        (int,int)    ... to a function taking (int, int)
int                  ... returning int
```

Apply it to the other one:

```
int *f(int, int);
     ^               start at f
      (int,int)      f is a function taking (int, int)   (go right first)
int *                ... returning int*
```

**The rule never fails.** When a declaration confuses you, walk it.

### Assigning and calling

```c
static int add(int a, int b) { return a + b; }

int (*p)(int, int) = add;    /* no & needed */
printf("%d\n", p(3, 4));     /* 7  -- call through the pointer   */
printf("%d\n", (*p)(3, 4));  /* 7  -- also legal, same thing     */
```

Verified output:

```
p(3,4)    = 7
(*p)(3,4) = 7   <- both legal, identical
p == add  : 1
p == &add : 1   <- for functions, f and &f are the same
```

A function name in an expression **decays to a pointer to that function**, exactly as an array name
decays to a pointer to its first element (Week 4). So `add`, `&add`, and `*add` all yield the same
pointer, and `p(...)`, `(*p)(...)`, and `(**p)(...)` all call it. Most code writes `add` and
`p(...)`; both forms are correct, and you will read both.

### Make it readable with `typedef`

```c
typedef int (*BinOp)(int, int);

BinOp p = add;               /* far easier to read              */
static int apply(BinOp f, int a, int b) { return f(a, b); }
```

Use a `typedef` whenever a function-pointer type appears more than once. A function taking a
function pointer and returning one is otherwise close to unreadable:

```c
int (*compose(int (*f)(int), int (*g)(int)))(int);   /* don't */
typedef int (*IntFn)(int);
IntFn compose(IntFn f, IntFn g);                     /* do    */
```

---

## 3. Dispatch Tables

Here is the payoff. An array of function pointers turns a branch into an index.

```c
typedef int (*BinOp)(int, int);

static int add(int a, int b) { return a + b; }
static int sub(int a, int b) { return a - b; }
static int mul(int a, int b) { return a * b; }

BinOp ops[]        = { add, sub, mul };
const char *names[] = { "add", "sub", "mul" };

for (size_t i = 0; i < sizeof ops / sizeof ops[0]; i++)
    printf("  %-3s(10,3) = %d\n", names[i], ops[i](10, 3));
```

Verified output:

```
add(10,3) = 13
sub(10,3) = 7
mul(10,3) = 30
```

### When a table beats a `switch`

| Use a `switch` | Use a dispatch table |
|---|---|
| A handful of cases, each doing different work inline | Many cases, each calling one function |
| The cases are unlikely to change | Cases are added and removed often |
| Behaviour is fixed at compile time | Behaviour must be selected at run time |
| The reader benefits from seeing all cases together | The set of handlers is data, possibly loaded from config |

A `switch` compiles to a jump table anyway when the cases are dense, so this is **not** primarily a
speed argument. It is a *structure* argument: with a table, adding an operation means adding one row,
and the dispatch code never changes.

That is the same idea as your the Hashtables appendix hash table: replace a search with an index.

### A worked example: a command table

```c
typedef struct {
    const char *name;
    int (*handler)(int argc, char **argv);
    const char *help;
} Command;

static const Command commands[] = {
    { "add",    cmd_add,    "add a record"    },
    { "list",   cmd_list,   "list records"    },
    { "delete", cmd_delete, "delete a record" },
};

static int dispatch(const char *name, int argc, char **argv)
{
    for (size_t i = 0; i < sizeof commands / sizeof commands[0]; i++)
        if (strcmp(name, commands[i].name) == 0)
            return commands[i].handler(argc, argv);
    fprintf(stderr, "unknown command: %s\n", name);
    return 1;
}
```

Adding a command is one line in the table. `dispatch` never changes, and the `help` text cannot drift
out of sync with the handler list because they live in the same row.

---

## 4. What a Function Pointer Is Not

**It is not a closure.** A function pointer is *only* an address. It captures nothing. If your
callback needs extra information, you must pass it explicitly — that is Lecture 3's context-pointer
pattern.

**It cannot portably be converted to `void *`.** Verified sizes on this machine:

```
sizeof(void *)         = 8
sizeof(void (*)(void)) = 8
```

They are equal here, but **C11 does not require it.** The standard guarantees round-tripping for
*object* pointers only (6.3.2.3). Historically, machines existed where code and data pointers
differed in size. POSIX adds the guarantee separately, precisely because `dlsym()` returns a
`void *` that you must call — a documented extension to C, not part of it.

**It has no arithmetic.** `p + 1` is meaningless and does not compile. Functions are not an array.

**Calling through a null or wrong-typed pointer is undefined behaviour.** Check before calling if the
pointer is optional:

```c
if (v->destroy) v->destroy(elem);
```

You will write exactly that line in Lecture 3.

---

## 5. Summary

| Idea | Takeaway |
|---|---|
| Functions have addresses | A pointer can name code as well as data |
| `int (*p)(int)` | Pointer to function; the parentheses are load-bearing |
| `int *f(int)` | A *function* returning `int *` — completely different |
| Right-left rule | Start at the identifier, right when you can, left when you must |
| `add` == `&add` | Function names decay to pointers, like arrays |
| `typedef` | Use it as soon as the type appears twice |
| Dispatch table | Turns a branch into an index; a structure win, not a speed win |
| Not a closure | Captures nothing — pass context explicitly (Lecture 3) |
| Not portably `void *` | C guarantees round-trip for *object* pointers only |

---

## Practice Exercises

Attempt each before reading the answers.

**1. (Read.)** Say in English what each declares:
(a) `void (*a)(void);`
(b) `void *b(void);`
(c) `int (*c[5])(char);`
(d) `int (*d(int))(int);`

**2. (Fix.)** This does not compile. Say why, and fix it.

```c
int apply(int f(int, int), int a, int b) { return f(a, b); }
double (*p)(int, int) = add;      /* add returns int */
```

**3. (Build.)** Write a `typedef` for a pointer to a function taking `const char *` and returning
`int`, then build a table of three such functions and a loop that calls each on `"hello"`.

**4. (Stretch.)** Rewrite this `switch` as a dispatch table, and state one thing that becomes easier
and one that becomes harder.

```c
switch (op) {
    case '+': r = add(a, b); break;
    case '-': r = sub(a, b); break;
    case '*': r = mul(a, b); break;
    default:  return -1;
}
```

### Answers

**1.**

| | Reading |
|---|---|
| **(a)** | `a` is a **pointer to a function** taking no arguments and returning nothing |
| **(b)** | `b` is a **function** taking no arguments and returning `void *` |
| **(c)** | `c` is an **array of 5 pointers to functions** taking `char` and returning `int` |
| **(d)** | `d` is a **function** taking `int` and returning **a pointer to a function** taking `int` and returning `int` |

Walk (c) with the rule: start at `c`, parentheses force `(*c[5])` first — go right inside them,
`c[5]` is an array of 5; go left, of pointers. Then outside: right gives `(char)`, a function taking
`char`; left gives `int`, returning `int`.

For (d): start at `d`, go right — `d(int)` is a function taking `int`; go left — returning a pointer;
then the outer `(int)` and `int` finish it. This is the declaration that motivates `typedef`.

**2.** Two separate problems.

**The parameter is fine.** `int f(int, int)` as a *parameter* is automatically adjusted to
`int (*f)(int, int)`, exactly as an array parameter adjusts to a pointer (Week 4). It compiles and
works. Writing the pointer explicitly is clearer, but the original is legal:

```c
int apply(int (*f)(int, int), int a, int b) { return f(a, b); }
```

**The second line is the real error.** `p` is a pointer to a function returning `double`; `add`
returns `int`. These are incompatible types. There is no implicit conversion between
function-pointer types — and there must not be, because calling through the wrong type is undefined
behaviour: the machine would interpret an `int` return register as a `double`.

Note what GCC actually does here, because it matters:

```
warning: initialization of 'double (*)(int, int)' from incompatible
         pointer type 'int (*)(int, int)' [-Wincompatible-pointer-types]
```

**A warning, not an error.** Left alone, this compiles and produces a program that calls `add` and
reads garbage as a `double`. It is a hard error only because we build with `-Werror` — which is
exactly why the course mandates those flags. Fix by matching the type:

```c
int (*p)(int, int) = add;
```

*Marking note for yourself:* if you "fixed" this with a cast, you silenced the compiler and kept the
bug.

**3.**

```c
typedef int (*StrFn)(const char *);

static int len(const char *s)   { return (int)strlen(s); }
static int first(const char *s) { return s[0]; }
static int count_l(const char *s) {
    int n = 0;
    for (; *s; s++) if (*s == 'l') n++;
    return n;
}

StrFn table[] = { len, first, count_l };
const char *names[] = { "len", "first", "count_l" };

for (size_t i = 0; i < sizeof table / sizeof table[0]; i++)
    printf("%-8s(\"hello\") = %d\n", names[i], table[i]("hello"));
```

Gives `len=5`, `first=104` (`'h'`), `count_l=2`.

**4.**

```c
typedef struct { char op; int (*fn)(int, int); } Entry;

static const Entry table[] = {
    { '+', add }, { '-', sub }, { '*', mul },
};

static int calc(char op, int a, int b, int *out)
{
    for (size_t i = 0; i < sizeof table / sizeof table[0]; i++)
        if (table[i].op == op) { *out = table[i].fn(a, b); return 0; }
    return -1;                       /* the old `default` */
}
```

**Easier:** adding an operator is one row, and `calc` never changes. The set of operators becomes
*data*, so it could be extended at run time — registered by another module, or read from a config
file. That is impossible with a `switch`.

**Harder:** you can no longer write case-specific code inline. Every operation must fit the one
signature `int(int,int)`, so an operation needing a third argument, or one that should short-circuit,
does not fit the table and forces a redesign. The `switch` also shows all behaviour in one place,
which is easier to read when there are only three cases.

*Also acceptable:* the table costs a linear scan where a dense `switch` compiles to a jump table —
though for three entries this is noise, and the honest reason to choose the table is structure, not
speed.

---

## Reading

- **K&R, §5.11** — pointers to functions; the original treatment, still the clearest
- **C11 standard §6.3.2.3** — pointer conversions; read paragraph 1 and note that it covers *object*
  pointers
- **`man 3 qsort`** — read the signature before Lecture 2; you will implement its comparator

---

*PROG 101 · Week 11 · Lecture 1 · © CSE Department*
