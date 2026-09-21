# PROG 101 · Programming I: Structured Programming in C
## Week 7 · Lab 7: Structs, Unions, and a Complete Linked List Library

**Graded: 20 points**
**Duration:** 2 hours
**Date:** Monday 16 November 2026 · 15:00–16:50 · Lab Section (Week 8) — covers Week 7 (Lectures 01–03)
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
- `list_copy` allocates new nodes; `list_reverse` and `list_remove_duplicates` only relink existing ones
  (freeing the removed duplicates)

### `test_linkedlist.c`

Write comprehensive tests. Structure similar to previous weeks' test suites:

```c
#include <stdio.h>
#include "linkedlist.h"

static int passed = 0, failed = 0;

static void check(const char *desc, int cond) {
    if (cond) { printf("  PASS: %s\n", desc); passed++; }
    else      { printf("  FAIL: %s\n", desc); failed++; }
}

void test_insertion(void) {
    printf("=== Insertion ===\n");
    Node *head = NULL;
    head = list_insert_front(head, 30);
    head = list_insert_front(head, 20);
    head = list_insert_front(head, 10);
    /* head: 10 -> 20 -> 30 */
    check("length after 3 inserts", list_length(head) == 3);
    check("first element", list_get_at(head, 0) == 10);
    check("last element",  list_get_at(head, 2) == 30);

    head = list_insert_end(head, 40);
    check("insert_end works", list_get_at(head, 3) == 40);

    head = list_insert_at(head, 2, 25);
    /* head: 10 -> 20 -> 25 -> 30 -> 40 */
    check("insert_at middle", list_get_at(head, 2) == 25);
    check("length after insert_at", list_length(head) == 5);

    head = list_free(head);
    check("head is NULL after free", head == NULL);
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

void test_copy_and_duplicates(void) {
    /* TODO: copy a list, change the original, verify the copy is unchanged;
     * remove duplicates from {3, 1, 3, 2, 1} -> {3, 1, 2}, and from an empty list */
}

int main(void) {
    test_insertion();
    test_deletion();
    test_reverse();
    test_copy_and_duplicates();

    printf("\n=== Results: %d passed, %d failed ===\n", passed, failed);
    return failed > 0 ? 1 : 0;
}
```

### Valgrind Requirement

```bash
valgrind --leak-check=full ./test_linkedlist
```

Must report **0 errors, 0 leaks**.

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
| 3: Linked list implementation | 6 | All functions correct, including the empty-list cases |
| 3: Test suite | 4 | Comprehensive coverage, all tests pass |
| 3: Valgrind clean | 2 | 0 errors, 0 leaks |
| **Total** | **20** | |
