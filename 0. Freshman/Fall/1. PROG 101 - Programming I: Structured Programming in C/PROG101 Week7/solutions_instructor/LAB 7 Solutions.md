# PROG 101 · Week 7
## LAB 7 Solutions — INSTRUCTOR ONLY

> **Every implementation below compiles under `gcc -Wall -Wextra -Werror -std=c11` and runs clean
> under `-fsanitize=address,undefined`.** Where the lab requires it, Valgrind output is quoted
> verbatim. Reject any submission that does not build warning-free — `-Werror` is not negotiable in
> this course.

---

## Part 1 — Struct Layout Investigation

Verified on x86-64:

| Struct | `sizeof` | Offsets |
|---|---|---|
| `struct { char c; int i; char d; }` | **12** | c=0, i=4, d=8 |
| `struct { int i; char c; char d; }` | **8** | i=0, c=4, d=5 |

Same three members, **33% smaller** from declaration order alone.

Each member must sit at an offset that is a multiple of its own alignment (`_Alignof(int)` = 4), so
the compiler inserts padding. In the first struct, `c` occupies byte 0 and `i` cannot start until
byte 4 — three bytes wasted — then `d` sits at 8 and the struct is padded to 12 so that **the total
size is a multiple of the strictest member's alignment**, which is required for arrays to keep every
element aligned.

**Rule: declare members in decreasing size order.** Students should verify with `offsetof` from
`<stddef.h>` rather than guessing, and should note that none of this is portable — which is exactly
why Week 8 warns against `fwrite`-ing a struct.

---

## Part 2 — Tagged Union Shape System

```c
typedef enum { SHAPE_CIRCLE, SHAPE_RECT, SHAPE_TRIANGLE } ShapeKind;

typedef struct {
    ShapeKind kind;                 /* the TAG — must live in the same struct */
    union {
        struct { double r; } circle;
        struct { double w, h; } rect;
        struct { double b, h; } triangle;
    } as;
} Shape;

double shape_area(const Shape *s) {
    switch (s->kind) {                          /* no default: — see below */
        case SHAPE_CIRCLE:   return 3.14159265358979 * s->as.circle.r * s->as.circle.r;
        case SHAPE_RECT:     return s->as.rect.w * s->as.rect.h;
        case SHAPE_TRIANGLE: return 0.5 * s->as.triangle.b * s->as.triangle.h;
    }
    return 0.0;                                 /* unreachable; silences -Wreturn-type */
}
```

**Two things to grade:**

1. **The tag must be inside the same struct as the union.** A union records nothing about which
   member is live; reading the wrong one is a reinterpretation of the bits, not an error. Storing
   the tag separately makes it possible for the two to drift apart, with no diagnostic.
2. **Omit `default:` from the switch.** With all enum constants handled and no `default`, GCC's
   `-Wswitch` (in `-Wall`) warns the moment a new shape is added and some switch is not updated.
   Adding `default:` silences exactly the warning you want. This is a genuine engineering technique,
   not a style preference.

---

## Part 3 — `linkedlist` Reference Implementation

**Valgrind-clean: 32 allocs, 32 frees, 0 errors.** Full verified transcript:

```
built:                [10, 20, 30, 40, 50]
insert_front(5):      [5, 10, 20, 30, 40, 50]
insert_at(3,25):      [5, 10, 20, 25, 30, 40, 50]
insert_at(999,99):    [5, 10, 20, 25, 30, 40, 50, 99]     (i >= length -> append)
length=8 sum=279 max=99 min=5
delete_value(25):     [5, 10, 20, 30, 40, 50, 99]
delete_front:         [10, 20, 30, 40, 50, 99]
delete_end:           [10, 20, 30, 40, 50]
delete_at(1):         [10, 30, 40, 50]
delete_at(999) noop:  [10, 30, 40, 50]
reverse:              [50, 40, 30, 10]
dup list [3,1,3,2,1,3] -> dedup [3, 1, 2]
merge_sorted([0,2,4,6],[1,3,5,7]) -> [0, 1, 2, 3, 4, 5, 6, 7]
insert_sorted -> [7, 14, 21, 28, 35]
has_cycle=0 ; after linking tail->head: has_cycle=1
empty list: length=0 contains=0 index_of=-1; deletes on empty survived
```

### The pointer-to-pointer technique

Every insertion and deletion below uses `Node **`, which **eliminates the head special case**:

```c
Node *list_delete_value(Node *head, int value) {
    Node **pp = &head;
    while (*pp) {
        if ((*pp)->value == value) {
            Node *dead = *pp;
            *pp = dead->next;      /* works whether pp points at head or at some ->next */
            free(dead);
            return head;
        }
        pp = &(*pp)->next;
    }
    return head;
}

Node *list_insert_sorted(Node *head, int value) {
    Node **pp = &head;
    while (*pp && (*pp)->value < value) pp = &(*pp)->next;
    Node *n = node_create(value);
    n->next = *pp; *pp = n;
    return head;
}
```

**Every node is pointed at by exactly one pointer** — either the caller's `head` or some node's
`next`. `pp` holds the *address of that pointer*, so unlinking works without knowing which kind it
was. Accept a version with an explicit head special case, but award the method marks to the
pointer-to-pointer form and show it at checkoff.

```c
Node *list_reverse(Node *head) {
    Node *prev = NULL;
    while (head) {
        Node *next = head->next;   /* SAVE before destroying the link */
        head->next = prev;
        prev = head;
        head = next;
    }
    return prev;                   /* prev, not head — head is NULL at exit */
}

bool list_has_cycle(const Node *head) {          /* Floyd's tortoise and hare */
    const Node *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}
```

### The six defects to grade for

1. **`free_list` reading after free.** `while (h) { free(h); h = h->next; }` is a use-after-free.
   Save `next` first. It usually *appears* to work because `free` does not erase the bytes.
2. **`list_reverse` returning `head` instead of `prev`.** At exit `head` is `NULL`, so the caller
   gets an empty list. Three pointers are required — `next` must capture the remainder before
   `head->next = prev` destroys the only reference to it.
3. **`list_copy` must be a deep copy.** Verified: mutating the copy leaves the original unchanged.
   A version returning the same nodes will double-free at cleanup.
4. **`list_merge_sorted` consumes both inputs** — the handout says so explicitly. Using `list_a`
   after the call is a use-after-free, and freeing both inputs *and* the result is a double free.
   Check the test file for this.
5. **`list_remove_duplicates` must free the removed nodes**, not merely unlink them.
6. **A cycle makes `list_free` loop forever.** The test that creates a cycle must break it before
   freeing — the reference does exactly that.

Empty-list behaviour is mandatory on every function: `list_length(NULL) == 0`,
`list_index_of(NULL, x) == -1`, and the three delete functions must be no-ops rather than crashes.

---

## Marking Scheme

Points follow the allocation printed on the handout. Within each part:

- **Correctness (≈50%).** Passes the required test cases *and* the edge cases listed above.
- **Memory discipline (≈30%).** No leaks, no invalid reads/writes, every `malloc` checked, every
  owner documented. For labs with a Valgrind requirement this is pass/fail: **0 errors, 0 leaks.**
- **Method (≈20%).** Required technique actually used, bounds asserted, `const` applied where the
  function only reads.

**Automatic deductions, regardless of output:**
- Any compiler warning under `-Wall -Wextra`.
- Unchecked `malloc`/`realloc` return.
- `realloc` result assigned directly back to the original pointer (leaks the block on failure).
- A buffer function that can leave its output unterminated.

**Carry-through.** One wrong helper used consistently downstream costs marks once.

---

*PROG 101 · Week 7 · Lab Solutions · Instructor Copy · © CSE Department*
