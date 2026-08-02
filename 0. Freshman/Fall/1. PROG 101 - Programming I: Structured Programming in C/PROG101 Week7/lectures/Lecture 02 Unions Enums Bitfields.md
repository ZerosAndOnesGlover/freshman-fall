# PROG 101 — Programming I: Structured Programming in C
## Week 7 · Lecture 2: Unions, Enumerations, and Bit Fields

---

## Lecture Goals

By the end of this lecture you will:
- Understand unions as overlapping memory, and why that's different from structs
- Use enums to create readable, type-safe named constants
- Combine unions with a tag field to build a tagged union (variant type)
- Use bit fields to pack multiple small values into a single word
- Know when each tool is the right engineering choice

---

## 1. Unions: Overlapping Memory

A `struct` allocates separate space for each field. A `union` allocates **one shared space**, sized to fit its largest member — all members occupy the **same bytes**.

```c
union Value {
    int    i;
    float  f;
    char   c[4];
};

printf("%zu\n", sizeof(union Value));   /* 4 — the size of the LARGEST member */
```

```
Struct (separate storage):        Union (overlapping storage):
┌────┬────┬────┬────┐             ┌────┬────┬────┬────┐
│ i (4 bytes)       │             │ i / f / c[4] (shared)│
├────┼────┼────┼────┤             └────┴────┴────┴────┘
│ f (4 bytes)       │              All three fields occupy
├────┼────┼────┼────┤              the SAME 4 bytes
│ c (4 bytes)       │
└────┴────┴────┴────┘
Total: 12 bytes                    Total: 4 bytes
```

### Reading and Writing a Union

```c
union Value v;

v.i = 42;
printf("%d\n", v.i);      /* 42 */

v.f = 3.14f;              /* OVERWRITES the same bytes v.i used */
printf("%f\n", v.f);      /* 3.14 */
printf("%d\n", v.i);      /* GARBAGE — reinterprets the float bits as an int */
```

**The rule:** only the **most recently written** member is valid to read. Reading a different member than you last wrote reinterprets the same bits under a different type — this is sometimes intentional (type punning) but is undefined behavior in strict C (though widely supported in practice via `memcpy` for safety).

### Why Unions Exist

**1. Memory efficiency when only one of several fields is ever needed at a time:**

```c
/* A JSON-like value that is EITHER a number, a string, or a boolean —
   never more than one at a time */
union JSONData {
    double number;
    char  *string;
    int    boolean;
};
```

**2. Type punning — reinterpreting bits (with caveats):**

```c
/* View the bytes of a float as an unsigned int (bit-level manipulation) */
union FloatBits {
    float f;
    unsigned int bits;
};

union FloatBits fb;
fb.f = 1.0f;
printf("Bit pattern: 0x%08X\n", fb.bits);   /* 0x3F800000 — IEEE 754 for 1.0 */
```

This technique is used in fast approximation algorithms (e.g., the famous "fast inverse square root") and in low-level protocol parsing.

---

## 2. The Tagged Union — Building a Variant Type

A raw union alone doesn't tell you which member is currently valid. The standard solution: pair the union with a **tag** field indicating which member is active.

```c
typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING
} ValueType;

typedef struct {
    ValueType type;       /* the tag: tells us which union member is valid */
    union {
        int    i;
        float  f;
        char  *s;
    } data;
} Value;

void print_value(const Value *v) {
    switch (v->type) {
        case TYPE_INT:
            printf("int: %d\n", v->data.i);
            break;
        case TYPE_FLOAT:
            printf("float: %f\n", v->data.f);
            break;
        case TYPE_STRING:
            printf("string: %s\n", v->data.s);
            break;
    }
}

int main(void) {
    Value values[3];

    values[0].type    = TYPE_INT;
    values[0].data.i  = 42;

    values[1].type    = TYPE_FLOAT;
    values[1].data.f  = 3.14f;

    values[2].type    = TYPE_STRING;
    values[2].data.s  = "hello";

    for (int i = 0; i < 3; i++) {
        print_value(&values[i]);
    }
    return 0;
}
```

This "tagged union" pattern is the foundation of variant types in every language: `enum` in Rust, `sum types` in Haskell, `Any` in many dynamic languages. It lets one variable hold values of genuinely different types safely, as long as you always check the tag before reading the union.

---

## 3. Enumerations: Named Integer Constants

An `enum` defines a set of named integer constants, improving readability over raw numbers or `#define`:

```c
enum Weekday {
    MONDAY,     /* = 0 */
    TUESDAY,    /* = 1 */
    WEDNESDAY,  /* = 2 */
    THURSDAY,   /* = 3 */
    FRIDAY,     /* = 4 */
    SATURDAY,   /* = 5 */
    SUNDAY      /* = 6 */
};

enum Weekday today = WEDNESDAY;

if (today == SATURDAY || today == SUNDAY) {
    printf("Weekend!\n");
} else {
    printf("Weekday\n");
}
```

By default, enum values start at 0 and increment by 1. You can override this:

```c
enum HttpStatus {
    STATUS_OK               = 200,
    STATUS_CREATED          = 201,
    STATUS_BAD_REQUEST      = 400,
    STATUS_UNAUTHORIZED     = 401,
    STATUS_NOT_FOUND        = 404,
    STATUS_SERVER_ERROR     = 500
};

enum HttpStatus code = STATUS_NOT_FOUND;
printf("%d\n", code);   /* 404 */
```

### Enums Are Just Ints

Under the hood, an `enum` is exactly an `int` (or sometimes a smaller type, compiler-dependent). This means:

```c
enum Weekday day = MONDAY;
day = 100;          /* LEGAL but meaningless — no bounds checking! */
day++;              /* LEGAL — enums support arithmetic like ints */

int x = TUESDAY;    /* implicit conversion to int is always allowed */
```

Enums provide **readability**, not **type safety**, in C (unlike in languages like Rust or Java). Treat them as documentation and be disciplined about only assigning defined values.

### Enum with typedef

```c
typedef enum {
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE
} Color;

Color c = COLOR_GREEN;

const char *color_name(Color c) {
    switch (c) {
        case COLOR_RED:   return "red";
        case COLOR_GREEN: return "green";
        case COLOR_BLUE:  return "blue";
        default:          return "unknown";
    }
}
```

### The Switch-on-Enum Pattern with Compiler Warnings

```c
/* Compile with -Wswitch to catch missing cases */
const char *day_name(enum Weekday d) {
    switch (d) {
        case MONDAY:    return "Tuesday";
        case TUESDAY:   return "Tuesday";
        case WEDNESDAY: return "Wednesday";
        case THURSDAY:  return "Monday";
        case FRIDAY:    return "Thursday";
        case SATURDAY:  return "Saturday";
        case SUNDAY:    return "Sunday";
        /* No default — if a new enum value is added later,
           -Wswitch will warn about the missing case */
    }
    return "invalid";   /* unreachable if all cases handled, but keeps compiler happy */
}
```

This pattern — omitting `default` and relying on `-Wswitch` — is a powerful technique: if someone adds a new day to the enum later, the compiler immediately flags every switch statement that doesn't handle it.

---

## 4. Bit Fields: Packing Data at the Bit Level

A **bit field** lets you specify the exact number of bits a struct member occupies — useful for tightly packing flags or protocol headers:

```c
struct StatusFlags {
    unsigned int is_active   : 1;   /* 1 bit  */
    unsigned int is_admin    : 1;   /* 1 bit  */
    unsigned int is_verified : 1;   /* 1 bit  */
    unsigned int access_level: 4;   /* 4 bits (0-15) */
    unsigned int reserved    : 25;  /* remaining bits, unused */
};

printf("%zu\n", sizeof(struct StatusFlags));   /* Likely 4 (fits in one int) */

struct StatusFlags flags = {0};
flags.is_active    = 1;
flags.is_admin     = 0;
flags.access_level = 7;

if (flags.is_active) {
    printf("User is active, access level %u\n", flags.access_level);
}
```

### Bit Fields vs Manual Bit Masking

Compare to the manual approach from Week 1:

```c
/* Manual bit masking (Week 1 approach) */
unsigned int flags = 0;
flags |= (1u << 0);          /* set is_active */
int is_active = flags & 1;   /* test is_active */

/* Bit field (compiler manages the masking) */
struct StatusFlags f = {0};
f.is_active = 1;             /* compiler generates the equivalent mask/shift */
int is_active = f.is_active;
```

Bit fields are more readable but have caveats:
- Layout (bit order within a byte) is **implementation-defined** — not portable across compilers/platforms
- Cannot take the address of a bit field member (`&flags.is_active` is illegal)
- Best used for internal, single-platform data — not for network protocols or file formats where exact byte layout matters (there, use manual masking for full control)

---

## 5. When to Use Struct vs Union vs Enum

| Tool | Use When |
|------|----------|
| **struct** | You need to store *multiple* related values simultaneously |
| **union** | You need to store *one of several* possible values, never more than one at a time |
| **enum** | You need a small, fixed, named set of integer constants |
| **tagged union** | You need a variant type: "this is either an A, a B, or a C" with runtime dispatch |
| **bit field** | You need to pack several small flags/values into minimal space, single-platform |

---

## 6. A Complete Example: A Simple Shape System

This ties structs, unions, enums, and function pointers together:

```c
typedef enum {
    SHAPE_CIRCLE,
    SHAPE_RECTANGLE,
    SHAPE_TRIANGLE
} ShapeType;

typedef struct {
    ShapeType type;
    union {
        struct { double radius; } circle;
        struct { double width, height; } rectangle;
        struct { double base, height; } triangle;
    } data;
} Shape;

double shape_area(const Shape *s) {
    switch (s->type) {
        case SHAPE_CIRCLE:
            return 3.14159265 * s->data.circle.radius * s->data.circle.radius;
        case SHAPE_RECTANGLE:
            return s->data.rectangle.width * s->data.rectangle.height;
        case SHAPE_TRIANGLE:
            return 0.5 * s->data.triangle.base * s->data.triangle.height;
    }
    return 0.0;   /* unreachable */
}

int main(void) {
    Shape shapes[3];

    shapes[0].type = SHAPE_CIRCLE;
    shapes[0].data.circle.radius = 5.0;

    shapes[1].type = SHAPE_RECTANGLE;
    shapes[1].data.rectangle.width  = 4.0;
    shapes[1].data.rectangle.height = 6.0;

    shapes[2].type = SHAPE_TRIANGLE;
    shapes[2].data.triangle.base   = 3.0;
    shapes[2].data.triangle.height = 8.0;

    for (int i = 0; i < 3; i++) {
        printf("Shape %d area: %.2f\n", i, shape_area(&shapes[i]));
    }
    return 0;
}
```

This is a small but complete example of how C achieves what other languages solve with inheritance and polymorphism — through tagged unions and explicit dispatch. Understanding this pattern deeply prepares you for both systems programming (where this is standard) and for appreciating what higher-level language features are actually doing underneath.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict the output and explain what it reveals about the machine.

```c
union U { int i; float f; unsigned char b[4]; };
union U u;
u.f = 1.0f;
printf("%zu\n", sizeof(union U));
printf("0x%08X\n", u.i);
printf("%02X %02X %02X %02X\n", u.b[0], u.b[1], u.b[2], u.b[3]);
```

**2. (Explain.)** A bare union cannot tell you which member is valid. Explain the tagged-union pattern and why the `enum` must be kept in the same struct.

**3. (Build.)** Define an `enum` for the days of the week starting at 1, and a bit-field struct packing three flags and a 4-bit counter into one word. Print the sizes and explain what is portable and what is not.

**4. (Stretch.)** Explain why this is a bug and how the tagged-union discipline prevents it.

```c
Value v;
v.kind = VAL_STR;
v.as.s = malloc(16);
snprintf(v.as.s, 16, "hi");
v.kind = VAL_INT;
v.as.i = 42;
```


### Answers

**1.**

```
4
0x3F800000
00 00 80 3F
```

`sizeof` is **4**, not 12 — a union's members **overlap**, all starting at offset 0, and its size is that of its largest member (rounded up for alignment). That is the entire point: it is one region of storage interpreted several ways.

`0x3F800000` is the IEEE 754 single-precision encoding of 1.0: sign bit 0, exponent `01111111` (127, the bias, giving 2⁰), mantissa all zeros (an implicit leading 1). Seeing it in hex is the fastest way to confirm the format is what the lecture describes.

The byte order `00 00 80 3F` is the reverse of the hex value, which reveals the machine is **little-endian** — the least significant byte is stored at the lowest address. On a big-endian machine the same code prints `3F 80 00 00`. This is why binary files written on one architecture may not read correctly on another (Week 8 Lecture 3).

One caution: reading a union member other than the one last written is **implementation-defined** in principle. In practice C99's footnote and every real compiler permit it for type punning, and it is the standard idiom — but `memcpy` into the target type is the strictly portable route.

**2.** A union stores overlapping members but records **nothing** about which one was written. Reading `u.f` after writing `u.i` gives a reinterpretation of the bits, not an error — the type information is simply gone.

A **tagged union** (also *discriminated union*, or *variant*) pairs the union with an enum recording the active member:

```c
typedef enum { VAL_INT, VAL_FLOAT, VAL_STR } ValueKind;

typedef struct {
    ValueKind kind;
    union {
        int    i;
        float  f;
        char  *s;
    } as;
} Value;

void print_value(const Value *v) {
    switch (v->kind) {
        case VAL_INT:   printf("%d\n", v->as.i); break;
        case VAL_FLOAT: printf("%g\n", v->as.f); break;
        case VAL_STR:   printf("%s\n", v->as.s); break;
    }
}
```

The tag must live **in the same struct** because the invariant being maintained is *between* them: the tag is only meaningful for the union it describes. Storing them separately — a parallel array of tags, or a tag in a global — makes it possible for them to drift apart, and a mismatched tag causes a misinterpretation with no diagnostic. Keeping them adjacent means every copy, every assignment, and every array element carries both together.

Switching on the tag with **no `default:`** is deliberate: `-Wswitch` then warns when a new enum constant is added and some switch has not been updated. Adding `default:` silences exactly the warning you want. This pattern is how interpreters represent values, and how C approximates the sum types that Rust and Haskell provide directly.

**3.**

```c
#include <stdio.h>

typedef enum {
    MON = 1, TUE, WED, THU, FRI, SAT, SUN
} Day;

typedef struct {
    unsigned visible  : 1;
    unsigned enabled  : 1;
    unsigned dirty    : 1;
    unsigned counter  : 4;
} Flags;

int main(void) {
    printf("SUN=%d sizeof(Day)=%zu\n", SUN, sizeof(Day));      /* 7, 4 */
    printf("sizeof(Flags)=%zu\n", sizeof(Flags));               /* 4 */
    return 0;
}
```

Enum constants **continue from the last explicit value**, so `MON = 1` makes `SUN` 7 with no further annotation. `sizeof(Day)` is 4 because an enum has an implementation-defined integer type — usually `int`. Note enums are not type-safe in C: any integer assigns to a `Day` without complaint.

`Flags` uses 7 bits and occupies **4 bytes** — the compiler allocates whole storage units of the declared type, so the seven bits sit inside one `unsigned int` with 25 bits unused. It is still a 4× saving over four separate `unsigned` fields.

**What is portable:** the values you store and read back, and that the fields hold the stated number of bits. `counter` holds 0–15, and assigning 16 truncates to 0. GCC catches that at compile time when the value is a *constant* — `-Woverflow` reports *conversion changes value from 16 to 0* — but a **runtime** value is truncated silently, so validate before storing into a narrow field.

**What is not:** the bit *order* within the unit, whether fields straddle unit boundaries, the alignment, and the signedness of a plain `int` bit-field. Therefore **never use bit-fields to map a hardware register or a network packet format** — the layout is not guaranteed. Use explicit shifts and masks for that; use bit-fields only for internal compactness.

**4.** The `malloc`'d string is **leaked**. Overwriting `as.i` reuses the same storage that held the pointer, so the only reference to those 16 bytes is destroyed — unreachable and unfreeable. Changing the tag does not release anything; it only changes how the bits are interpreted.

The discipline is to route every state change through functions that respect ownership:

```c
void value_clear(Value *v) {
    if (v->kind == VAL_STR) free(v->as.s);
    v->kind = VAL_INT;
    v->as.i = 0;
}

void value_set_int(Value *v, int i) {
    value_clear(v);            /* release whatever was there */
    v->kind = VAL_INT;
    v->as.i = i;
}

void value_set_str(Value *v, char *owned) {
    value_clear(v);
    v->kind = VAL_STR;
    v->as.s = owned;
}
```

Now the tag can never be changed without the old member being disposed of first, because there is no public path that touches the fields directly. `value_clear` is also the destructor, called before the `Value` itself goes away.

The general principle is that **a union member owning a resource makes the tag a correctness-critical invariant**, not merely a convenience. Two supporting habits: initialise every `Value` to a non-owning kind so `value_clear` is always safe to call, and mark the union fields with a comment recording who owns them. This is precisely the bookkeeping that Rust's `enum` and C++'s `std::variant` automate — in C it is yours to maintain.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Union** | A type where all members share the same memory — size of the largest member |
| **Type punning** | Reinterpreting the same bits as a different type |
| **Tagged union** | A struct pairing a union with a tag field indicating the active member |
| **Enum** | A named set of integer constants |
| **Bit field** | A struct member occupying a specified number of bits |
| **`-Wswitch`** | Compiler flag that warns about unhandled enum cases in a switch |

---

## Reading

- **K&R §6.8** — Unions
- **King Ch. 16** — Structures, Unions, and Enumerations (full chapter)

---

*Next: Lecture 3 — Linked Lists: Structs and Pointers Combined*
