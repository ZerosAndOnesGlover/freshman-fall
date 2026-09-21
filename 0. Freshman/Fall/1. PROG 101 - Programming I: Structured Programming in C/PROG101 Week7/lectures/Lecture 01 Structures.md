# PROG 101 · Programming I: Structured Programming in C
## Week 7 · Lecture 1: Structures Composite Types and Memory Layout

**Date:** Tuesday 10 November 2026 · 10:00–10:50 · Week 7

---

## Lecture Goals

By the end of this lecture you will:
- Define and use `struct` types to group related data
- Understand exactly how structs are laid out in memory, including padding
- Use the `->` operator and understand what it means mechanically
- Pass structs by value vs by pointer, and know the tradeoffs
- Nest structs and build composite data types
- Use `typedef` to simplify struct usage

---

## 1. Why Structures Exist

Until now, related data has been scattered across separate variables:

```c
/* Awkward: three separate variables represent one "point" */
double point_x = 3.0;
double point_y = 4.0;

/* Even worse: representing multiple points */
double x1 = 1.0, y1 = 2.0;
double x2 = 3.0, y2 = 4.0;
double x3 = 5.0, y3 = 6.0;
/* What if we need 1000 points? This does not scale. */
```

A `struct` groups related fields into a single named type:

```c
struct Point {
    double x;
    double y;
};

struct Point p1 = {1.0, 2.0};
struct Point p2 = {3.0, 4.0};

/* Now an array of points is trivial: */
struct Point points[1000];
```

This is the foundational step toward every data structure you will build for the rest of your career: linked lists, trees, hash tables, graphs — all are structs connected by pointers.

---

## 2. Declaring and Using Structs

### Definition

```c
struct Point {
    double x;
    double y;
};
```

This defines a **type** named `struct Point`. No memory is allocated yet — this is like a blueprint, not a variable.

### Creating Variables

```c
struct Point p1;              /* uninitialized — fields contain garbage */
struct Point p2 = {1.0, 2.0}; /* initialized: p2.x=1.0, p2.y=2.0 */
struct Point p3 = {.y = 5.0}; /* designated initializer: p3.x=0.0, p3.y=5.0 */
```

### Accessing Fields: the `.` Operator

```c
struct Point p = {3.0, 4.0};

printf("%f\n", p.x);    /* 3.0 */
printf("%f\n", p.y);    /* 4.0 */

p.x = 10.0;             /* modify a field */

double distance = sqrt(p.x * p.x + p.y * p.y);
```

### Struct Assignment: Whole-Struct Copy

Unlike arrays, structs **can** be copied wholesale with `=`:

```c
struct Point a = {1.0, 2.0};
struct Point b = a;    /* COPIES all fields: b.x=1.0, b.y=2.0 */

b.x = 99.0;            /* only b changes; a is unaffected */
printf("%f\n", a.x);   /* still 1.0 */
```

This copies every byte of the struct. For large structs, this can be expensive — a reason to pass structs by pointer to functions (see below).

### Struct Comparison — There Is No `==`

```c
struct Point a = {1.0, 2.0};
struct Point b = {1.0, 2.0};

if (a == b) { ... }    /* COMPILE ERROR: structs cannot be compared with == */

/* You must write a comparison function yourself: */
int points_equal(struct Point a, struct Point b) {
    return a.x == b.x && a.y == b.y;
}
```

This is because structs may contain padding bytes (see below) whose values are unspecified — a byte-by-byte comparison (like `memcmp`) could report unequal even for "logically equal" structs.

---

## 3. Memory Layout: How Structs Are Actually Stored

This is where structs stop being an abstraction and become a concrete memory layout question.

```c
struct Example {
    char  a;    /* 1 byte */
    int   b;    /* 4 bytes */
    char  c;    /* 1 byte */
};

printf("%zu\n", sizeof(struct Example));   /* NOT 6! Usually 12. */
```

### Why Not 6 Bytes?

The CPU accesses memory more efficiently when data is **aligned** — stored at an address that is a multiple of its size. A 4-byte `int` should ideally start at an address divisible by 4.

The compiler inserts **padding** bytes to satisfy alignment:

```
Offset:  0    1    2    3    4    5    6    7    8    9   10   11
Field:  [a] [pad][pad][pad][------b------][c] [pad][pad][pad]
         char              int             char
```

- `a` at offset 0 (1 byte)
- 3 padding bytes (offsets 1-3) so `b` starts at offset 4 (a multiple of 4)
- `b` at offset 4 (4 bytes, ends at offset 7)
- `c` at offset 8 (1 byte)
- 3 padding bytes (offsets 9-11) so the **struct size itself** is a multiple of the largest alignment requirement (4, for the `int`) — this matters for arrays of structs

Total: 12 bytes, not 6.

### Field Order Matters

Reordering fields changes the padding:

```c
struct Reordered {
    int   b;    /* 4 bytes, offset 0 */
    char  a;    /* 1 byte,  offset 4 */
    char  c;    /* 1 byte,  offset 5 */
    /* 2 padding bytes to reach 8 (multiple of 4) */
};
printf("%zu\n", sizeof(struct Reordered));  /* 8 bytes! */
```

By grouping the smaller fields together, we reduced the size from 12 to 8 bytes. **Rule of thumb:** order struct fields from largest to smallest to minimize padding.

### Inspecting Layout with `offsetof`

```c
#include <stddef.h>   /* offsetof macro */

struct Example {
    char a;
    int  b;
    char c;
};

printf("offset of a: %zu\n", offsetof(struct Example, a));  /* 0 */
printf("offset of b: %zu\n", offsetof(struct Example, b));  /* 4 */
printf("offset of c: %zu\n", offsetof(struct Example, c));  /* 8 */
printf("total size:  %zu\n", sizeof(struct Example));       /* 12 */
```

Use this whenever you need to reason precisely about memory layout — for example, when reading binary file formats or network packets.

---

## 4. Passing Structs to Functions

### By Value — A Full Copy Is Made

```c
struct Point {
    double x, y;
};

/* Receives a COPY of the struct */
double distance_from_origin(struct Point p) {
    return sqrt(p.x * p.x + p.y * p.y);
}

/* Modifying p here does NOT affect the caller's struct */
void try_move(struct Point p) {
    p.x += 1.0;   /* modifies the local copy only */
}
```

For small structs (a few fields), pass-by-value is fine and even preferred (clearer, no aliasing concerns). For large structs (many fields, embedded arrays), copying is expensive — pass by pointer instead.

### By Pointer — No Copy, Can Modify

```c
/* Receives the ADDRESS of the caller's struct — no copy */
void move(struct Point *p, double dx, double dy) {
    p->x += dx;    /* modifies the caller's original struct */
    p->y += dy;
}

int main(void) {
    struct Point p = {0.0, 0.0};
    move(&p, 3.0, 4.0);
    printf("%f %f\n", p.x, p.y);   /* 3.0 4.0 — the original was modified */
    return 0;
}
```

### The `->` Operator

When you have a **pointer to a struct**, you must dereference before accessing a field. `p->field` is shorthand for `(*p).field`:

```c
struct Point *ptr = &p;

(*ptr).x = 5.0;    /* explicit dereference then access — valid but verbose */
ptr->x   = 5.0;    /* IDENTICAL meaning — the arrow operator */
```

**Rule:** use `.` when you have the struct itself; use `->` when you have a pointer to the struct.

### Const-Correctness with Struct Pointers

```c
/* This function promises not to modify the pointed-to struct */
double distance(const struct Point *p) {
    return sqrt(p->x * p->x + p->y * p->y);
}
```

Use `const struct Point *` for read-only access — avoids the cost of copying while preventing accidental modification.

---

## 5. Nested Structs

Structs can contain other structs:

```c
struct Point {
    double x, y;
};

struct Rectangle {
    struct Point top_left;
    struct Point bottom_right;
};

struct Rectangle r = {
    .top_left     = {0.0, 10.0},
    .bottom_right = {10.0, 0.0}
};

printf("%f\n", r.top_left.x);         /* 0.0 — chain the dot operator */

double width  = r.bottom_right.x - r.top_left.x;
double height = r.top_left.y - r.bottom_right.y;

/* With a pointer to the outer struct: */
struct Rectangle *rp = &r;
printf("%f\n", rp->top_left.x);       /* -> then . for the nested field */
```

---

## 6. Arrays of Structs

```c
struct Student {
    char name[50];
    int  id;
    double gpa;
};

struct Student class_roster[100];

/* Initialize one student */
strcpy(class_roster[0].name, "Alice");
class_roster[0].id  = 1001;
class_roster[0].gpa = 3.8;

/* Iterate all students */
for (int i = 0; i < 100; i++) {
    printf("%s: %d, %.2f\n",
           class_roster[i].name,
           class_roster[i].id,
           class_roster[i].gpa);
}

/* Find the student with the highest GPA */
int best = 0;
for (int i = 1; i < 100; i++) {
    if (class_roster[i].gpa > class_roster[best].gpa) {
        best = i;
    }
}
```

### Array of Struct Pointers vs Array of Structs

```c
/* Array of structs: contiguous memory, all data inline */
struct Student roster[100];        /* 100 * sizeof(struct Student) bytes, one block */

/* Array of pointers to structs: indirection, data scattered on heap */
struct Student *roster_ptrs[100];  /* 100 * 8 bytes (pointers), data elsewhere */
for (int i = 0; i < 100; i++) {
    roster_ptrs[i] = malloc(sizeof(struct Student));
}
```

Arrays of structs are more cache-friendly (data is contiguous). Arrays of pointers are useful when structs are large, when you need to share/alias structs, or when the array itself must hold heterogeneous or dynamically-sized data.

---

## 7. `typedef` — Naming Types

Writing `struct Point` every time is verbose. `typedef` creates an alias:

```c
typedef struct Point {
    double x, y;
} Point;

/* Now you can write: */
Point p1 = {1.0, 2.0};       /* instead of struct Point p1 */
Point *p2 = &p1;

/* Function signatures are cleaner too: */
double distance(const Point *p);
```

### The Anonymous Struct + typedef Pattern

The most common idiom in professional C code:

```c
typedef struct {
    double x, y;
} Point;
/* No tag name after 'struct' — the struct is anonymous,
   only accessible through the typedef name 'Point' */

Point p = {1.0, 2.0};
```

This is what you will use for the rest of the course. It is clean, standard, and what you'll see in every well-written C codebase.

### Self-Referential Structs Require a Tag

One case where you **must** use a tag: structs that contain a pointer to their own type (needed for linked lists, trees):

```c
typedef struct Node {
    int data;
    struct Node *next;    /* Must use 'struct Node' here — the typedef
                              name 'Node' doesn't exist yet at this point
                              in the declaration */
} Node;

Node n1 = {10, NULL};
Node n2 = {20, &n1};
```

We build on this pattern extensively in Lecture 3 (linked lists).

---

## 8. Structs and `sizeof` — Predicting Size

Practice predicting struct sizes before checking:

```c
struct A {
    char  a;   /* 1 */
    char  b;   /* 1 */
    int   c;   /* 4 */
};
/* Layout: a(0) b(1) [pad 2,3] c(4-7) → total 8 bytes */

struct B {
    int   a;   /* 4 */
    char  b;   /* 1 */
    short c;   /* 2 */
};
/* Layout: a(0-3) b(4) [pad 5] c(6-7) → total 8 bytes */

struct C {
    double a;  /* 8 */
    char   b;  /* 1 */
    int    c;  /* 4 */
};
/* Layout: a(0-7) b(8) [pad 9-11] c(12-15) → total 16 bytes
   (needs to be a multiple of 8, the alignment of 'double') */
```

**The alignment rule:** a struct's overall size must be a multiple of its largest member's alignment (usually its size, for basic types). This ensures arrays of the struct keep every element properly aligned.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict `sizeof` for each struct on a 64-bit system, and give the offset of every member. Verify with `offsetof` from `<stddef.h>`.

```c
struct A { char c; int i; char d; };
struct B { int i; char c; char d; };
```

**2. (Explain.)** Explain what happens when a struct is passed by value versus by pointer, and give the rule for choosing. Say why `const Big *` is usually better than `Big`.

**3. (Build.)** Define a `Student` struct with a name, id, and GPA, then write functions to create one, print one, and compare two by GPA for use with `qsort`. Use `typedef`.

**4. (Stretch.)** Explain the difference between `struct Node { ... } Node;` and `typedef struct Node { ... } Node;`, and why a self-referential struct must name itself in the `struct` tag.


### Answers

**1.** **`sizeof(struct A)` is 12**, offsets `c=0, i=4, d=8`.
**`sizeof(struct B)` is 8**, offsets `i=0, c=4, d=5`.

Same three members, same types — **33% smaller** purely from declaration order.

The rule is **alignment**: each member must sit at an offset that is a multiple of its own alignment (`_Alignof(int)` is 4), so the compiler inserts padding. In `A`, `c` occupies byte 0 and `i` cannot start until byte 4, wasting 3 bytes. Then `d` sits at 8, and the struct is padded to 12 so that its **total size is a multiple of its strictest member's alignment** — necessary so that `A arr[2]` keeps every element aligned.

In `B` the `int` leads, both `char`s pack into bytes 4 and 5, and only 2 bytes of tail padding are needed.

**Declare members in decreasing size order** and padding largely disappears. This is invisible for one struct and significant for an array of a million — 12 MB versus 8 MB, plus the cache traffic that follows. Note you may **not** assume any of this is portable: sizes and alignments differ by platform, which is why writing a struct to a file byte-for-byte is a portability hazard (Week 8 Lecture 3 §3).

**2.** **By value**, the entire struct is copied into the callee's frame — a 200-byte struct means a 200-byte copy on every call. The callee's changes are invisible to the caller, exactly like any other value.

**By pointer**, only 8 bytes are copied. The callee can reach the caller's object, so changes are visible — which is required for a mutating function and a hazard otherwise.

**The rule:** pass by value when the struct is small (roughly two words — a point, a complex number, a `div_t`) and the function does not need to modify the original. Pass a pointer when the struct is large or must be modified.

**`const Big *` beats `Big`** for large read-only parameters because it gets the cheap 8-byte pass *and* the compiler-enforced guarantee of no modification. You keep the safety property that pass-by-value gave you, without paying for the copy. It is the standard C signature for "read this large thing".

Two caveats. The `const` promise is shallow: `const struct { int *p; }` protects the pointer field, not what it points at. And passing by pointer introduces **aliasing** — if two parameters may point at the same object, the compiler must reload after every write, which can be slower than the copy it saved. Small structs really are better by value.

**3.**

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct {
    char   name[64];
    int    id;
    double gpa;
} Student;

Student student_make(const char *name, int id, double gpa) {
    Student s;
    snprintf(s.name, sizeof s.name, "%s", name);   /* always terminates */
    s.id = id;
    s.gpa = gpa;
    return s;
}

void student_print(const Student *s) {
    printf("%-20s #%-6d %.2f\n", s->name, s->id, s->gpa);
}

int student_cmp_gpa(const void *a, const void *b) {
    double x = ((const Student *)a)->gpa, y = ((const Student *)b)->gpa;
    return (x < y) - (x > y);          /* descending */
}
```

Four points. The name is a **fixed array**, not a `char *`, so the struct owns its storage and there is nothing to free — the alternative would require an ownership contract on every copy. `snprintf` bounds the copy and always terminates, unlike `strcpy` or `strncpy`.

`student_print` takes **`const Student *`**: cheap and read-only. Returning a `Student` by value from `student_make` is fine because the caller needs their own copy anyway.

The comparator uses `(x < y) - (x > y)` rather than subtraction — with doubles the concern is not overflow but that `return (int)(x - y)` **truncates**, so GPAs of 3.9 and 3.5 both yield 0 and compare as equal. Never cast a floating-point difference to `int` in a comparator. Note also that `NaN` compares false against everything, so both terms are 0 and the ordering silently breaks.

**4.**

```c
struct Node { int v; } Node;            /* defines a struct AND a variable called Node */
typedef struct Node { int v; } Node;    /* defines a struct and a type alias Node */
```

The first line is a **definition of a variable** named `Node` of type `struct Node` — almost certainly not what was intended, and it compiles silently. The second creates a **type alias**, so you can write `Node n;` instead of `struct Node n;`.

C keeps struct tags in a **separate namespace** from ordinary identifiers, which is why `typedef struct Node {...} Node;` is legal despite using `Node` twice — the tag `Node` and the type `Node` do not collide.

**A self-referential struct must have a tag**, because the alias does not exist until the `typedef` completes:

```c
typedef struct Node {
    int v;
    struct Node *next;   /* tag required — 'Node' isn't defined yet */
} Node;
```

Writing `Node *next;` inside fails with *unknown type name*. The forward-declaration alternative works too:

```c
typedef struct Node Node;      /* alias to an incomplete type */
struct Node { int v; Node *next; };
```

and this second form is what headers use for **opaque types** — the alias is public, the fields are private to one `.c` file. The pointer is legal despite the type being incomplete because every pointer has the same size regardless of what it points at.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Struct** | A composite type grouping named fields, possibly of different types |
| **Field / member** | One named component of a struct |
| **Padding** | Compiler-inserted unused bytes to satisfy alignment requirements |
| **Alignment** | Requirement that data be stored at addresses that are multiples of a value |
| **`.` operator** | Access a field of a struct value |
| **`->` operator** | Access a field through a pointer to a struct: `p->f` = `(*p).f` |
| **`typedef`** | Creates an alias for a type, commonly used to shorten `struct Name` |
| **`offsetof`** | Macro returning the byte offset of a field within a struct |
| **Self-referential struct** | A struct containing a pointer to its own type (needs a tag name) |

---

## Reading

- **K&R Chapter 6** — Structures (the whole chapter — essential)
- **King Ch. 16** — Structures, Unions, and Enumerations
- **CS:APP §3.9.3** — Data Structures in Machine Code

---

*Next: Lecture 2 — Unions, Enumerations, and Bit Fields*
