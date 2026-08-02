# PROG 101 · Programming I: Structured Programming in C
## Week 7 · Lab 7: Structs, Unions, and a Complete Linked List Library

**Graded: 20 points**
**Duration:** 2 hours
**Submission:** Push to Git, show TA before leaving

---

## Overview

- **Part 1:** Struct memory layout investigation
- **Part 2:** Tagged union shape system (from Lecture 2)
- **Part 3:** Complete singly linked list library — the main deliverable

---

## Part 1: Struct Layout Investigation (4 pts)

Create `layout_investigation.c`. For each struct below:
1. Predict `sizeof` by hand (draw the byte layout with offsets)
2. Verify using `sizeof` and `offsetof`
3. If your prediction was wrong, explain why

```c
#include <stdio.h>
#include <stddef.h>

struct S1 {
    char  a;
    char  b;
    int   c;
    char  d;
};

struct S2 {
    double a;
    char   b;
    double c;
};

struct S3 {
    char   a;
    short  b;
    char   c;
    int    d;
};

struct S4 {
    int    arr[3];
    char   c;
};

/* A struct containing another struct */
struct Inner {
    char x;
    int  y;
};
struct Outer {
    char        tag;
    struct Inner inner;
};

int main(void) {
    printf("S1: predicted=__, actual=%zu\n", sizeof(struct S1));
    printf("  offsets: a=%zu b=%zu c=%zu d=%zu\n",
           offsetof(struct S1, a), offsetof(struct S1, b),
           offsetof(struct S1, c), offsetof(struct S1, d));

    /* TODO: repeat the pattern for S2, S3, S4, Outer */

    return 0;
}
```

In `LAB 7 Structs Linkedlist.md`, for each struct: draw an ASCII diagram of the byte layout (like in the lecture), showing which bytes are data and which are padding.

**Bonus question:** Reorder the fields of `S1` to minimize its size. What is the new size?

---

## Part 2: Tagged Union Shape System (4 pts)

Extend the Shape system from Lecture 2 with additional shapes and operations.

Create `shapes.h` and `shapes.c`:

```c
/* shapes.h */
#ifndef SHAPES_H
#define SHAPES_H

typedef enum {
    SHAPE_CIRCLE,
    SHAPE_RECTANGLE,
    SHAPE_TRIANGLE,
    SHAPE_SQUARE      /* NEW: add square as a 4th shape type */
} ShapeType;

typedef struct {
    ShapeType type;
    union {
        struct { double radius; } circle;
        struct { double width, height; } rectangle;
        struct { double base, height; } triangle;
        struct { double side; } square;
    } data;
} Shape;

/* Constructors — return an initialized Shape by value */
Shape shape_make_circle(double radius);
Shape shape_make_rectangle(double width, double height);
Shape shape_make_triangle(double base, double height);
Shape shape_make_square(double side);

/* Compute the area of any shape */
double shape_area(const Shape *s);

/* Compute the perimeter of any shape */
double shape_perimeter(const Shape *s);

/* Return a human-readable name for the shape's type */
const char *shape_type_name(const Shape *s);

/* Print a one-line description: "Circle(r=5.00): area=78.54, perimeter=31.42" */
void shape_print(const Shape *s);

/* Given an array of shapes, return the index of the one with the largest area.
 * Returns -1 if n == 0. */
int shape_find_largest(const Shape shapes[], int n);

/* Return the sum of all shapes' areas in the array */
double shape_total_area(const Shape shapes[], int n);

#endif
```

**Requirements:**
- Use `-Wswitch` and write switch statements WITHOUT a `default` case, so the compiler catches any missing shape type
- Every function must correctly handle all 4 shape types
- `shape_perimeter` formulas: circle = 2πr, rectangle = 2(w+h), triangle = base + two other sides (assume isoceles: two sides of length `sqrt((base/2)² + height²)`), square = 4×side

Write a test `main()` demonstrating an array of 5 mixed shapes, printing each, and reporting the largest and total area.

---

## Part 3: Singly Linked List Library (12 pts)

This is the main deliverable. Build a complete, memory-safe linked list library.

### `linkedlist.h`

```c
#ifndef LINKEDLIST_H
#define LINKEDLIST_H

#include <stdbool.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

/* === Construction === */

/* Allocate and initialize a new node. Exits on malloc failure. */
Node *node_create(int value);

/* === Insertion (all return the possibly-new head) === */

Node *list_insert_front(Node *head, int value);
Node *list_insert_end(Node *head, int value);

/* Insert value at position i (0-indexed). If i >= length, insert at end.
 * If i <= 0, insert at front. */
Node *list_insert_at(Node *head, int i, int value);

/* Insert value in a SORTED list, maintaining sorted order.
 * Precondition: the list is already sorted ascending. */
Node *list_insert_sorted(Node *head, int value);

/* === Deletion (all return the possibly-new head) === */

Node *list_delete_front(Node *head);
Node *list_delete_end(Node *head);

/* Delete the first node with the given value. No-op if not found. */
Node *list_delete_value(Node *head, int value);

/* Delete the node at position i (0-indexed). No-op if out of range. */
Node *list_delete_at(Node *head, int i);

/* === Query === */

int  list_length(const Node *head);
bool list_contains(const Node *head, int value);
int  list_index_of(const Node *head, int value);   /* -1 if not found */
int  list_get_at(const Node *head, int i);          /* asserts i is valid */
int  list_sum(const Node *head);
int  list_max(const Node *head);                    /* asserts non-empty */
int  list_min(const Node *head);                    /* asserts non-empty */

/* === Transformation (return the new head) === */

/* Reverse the list in-place. O(n) time, O(1) space. */
Node *list_reverse(Node *head);

/* Remove all duplicate values, keeping only the first occurrence of each. */
Node *list_remove_duplicates(Node *head);

/* Return a deep copy of the list (new nodes, same values, same order). */
Node *list_copy(const Node *head);

/* Merge two SORTED lists into one sorted list. Consumes both input lists
 * (their nodes are reused, not copied) — do not use list_a or list_b after this call. */
Node *list_merge_sorted(Node *head_a, Node *head_b);

/* Detect if the list contains a cycle (Floyd's cycle detection). */
bool list_has_cycle(const Node *head);

/* Find the middle node of the list (slow/fast pointer technique).
 * For even length, return the FIRST of the two middle nodes. */
Node *list_find_middle(Node *head);

/* === Cleanup === */

/* Free every node in the list. Returns NULL (the new, empty head). */
Node *list_free(Node *head);

/* === Utility === */

void list_print(const Node *head);   /* Prints: 10 -> 20 -> 30 -> NULL */

#endif
```

### Implementation Notes

- Every insertion/deletion function must correctly handle the empty-list case
- `list_free` must not leak any node — verify with Valgrind
- `list_merge_sorted` must not allocate any new nodes — it relinks existing nodes
- `list_has_cycle` and `list_find_middle` use the classic slow/fast (tortoise and hare) two-pointer technique:

```c
bool list_has_cycle(const Node *head) {
    const Node *slow = head, *fast = head;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;   /* they met — cycle detected */
    }
    return false;   /* fast reached NULL — no cycle */
}
```

### `test_linkedlist.c`

Write comprehensive tests. Structure similar to previous weeks' test suites:

```c
#include <stdio.h>
#include "linkedlist.h"

static int passed = 0, failed = 0;

#define CHECK(desc, cond) do { \
    if (cond) { printf("  PASS: %s\n", desc); passed++; } \
    else      { printf("  FAIL: %s\n", desc); failed++; } \
} while (0)

void test_insertion(void) {
    printf("=== Insertion ===\n");
    Node *head = NULL;
    head = list_insert_front(head, 30);
    head = list_insert_front(head, 20);
    head = list_insert_front(head, 10);
    /* head: 10 -> 20 -> 30 */
    CHECK("length after 3 inserts", list_length(head) == 3);
    CHECK("first element", list_get_at(head, 0) == 10);
    CHECK("last element",  list_get_at(head, 2) == 30);

    head = list_insert_end(head, 40);
    CHECK("insert_end works", list_get_at(head, 3) == 40);

    head = list_insert_at(head, 2, 25);
    /* head: 10 -> 20 -> 25 -> 30 -> 40 */
    CHECK("insert_at middle", list_get_at(head, 2) == 25);
    CHECK("length after insert_at", list_length(head) == 5);

    head = list_free(head);
    CHECK("head is NULL after free", head == NULL);
}

void test_deletion(void) {
    /* TODO: comprehensive deletion tests, including:
     *   - delete from empty list (no crash)
     *   - delete_front on single-element list
     *   - delete_value not found (list unchanged)
     *   - delete_at out of range
     *   - delete_at(0), delete_at(last)
     */
}

void test_reverse(void) {
    /* TODO: test reverse on empty, single-element, and multi-element lists */
}

void test_merge_sorted(void) {
    /* TODO: build two sorted lists, merge, verify single sorted result */
}

void test_cycle_detection(void) {
    /* TODO: build a list WITHOUT a cycle — verify has_cycle returns false.
     * Build a list WITH a manually-constructed cycle — verify true.
     * WARNING: after testing a cyclic list, you cannot safely list_free it
     *          with a naive loop (it would loop forever). Break the cycle
     *          first, then free, OR write the test to leak intentionally
     *          with a comment explaining why (acceptable for THIS test only).
     */
}

void test_find_middle(void) {
    /* TODO: test odd length (5 elements), even length (4 elements),
     * single element, and verify against the "first of two middles" rule */
}

int main(void) {
    test_insertion();
    test_deletion();
    test_reverse();
    test_merge_sorted();
    test_cycle_detection();
    test_find_middle();

    printf("\n=== Results: %d passed, %d failed ===\n", passed, failed);
    return failed > 0 ? 1 : 0;
}
```

### Valgrind Requirement

```bash
valgrind --leak-check=full ./test_linkedlist
```

Must report **0 errors, 0 leaks** (except intentionally in the cycle test, which you must document — or better, break the cycle before freeing to keep the whole suite clean).

---

## Deliverables

```
week4/lab4/
├── layout_investigation.c
├── shapes.h
├── shapes.c
├── shapes_test.c            # your test main() for Part 2
├── linkedlist.h
├── linkedlist.c
├── test_linkedlist.c
├── Makefile
└── LAB 7 Structs Linkedlist.md            # struct diagrams + bonus answer
```

**Makefile:**
```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -Wswitch -g -std=c11

all: layout_investigation shapes_test test_linkedlist

shapes_test: shapes_test.o shapes.o
	$(CC) $(CFLAGS) -o $@ $^ -lm

test_linkedlist: test_linkedlist.o linkedlist.o
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f layout_investigation shapes_test test_linkedlist *.o

.PHONY: all clean
```

---

## Grading

| Part | Points | Criteria |
|------|--------|---------|
| 1: Struct layout investigation | 4 | Correct predictions/diagrams for all 5 structs |
| 2: Shape system | 4 | All 4 shape types, correct area/perimeter, -Wswitch clean |
| 3: Linked list implementation | 6 | All functions correct including cycle/middle detection |
| 3: Test suite | 4 | Comprehensive coverage, all tests pass |
| 3: Valgrind clean | 2 | 0 errors, 0 leaks |
| **Total** | **20** | |
