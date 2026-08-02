# PROG 101 — Programming I: Structured Programming in C
## Week 7 · Problem Set 7

**Released:** End of Week 7 Thursday
**Due:** Before Week 8 Lecture 1
**Directory:** `~/prog101/week4/ps4/`
**Total:** 100 points

---

## Problem 1: Struct Design and Memory (15 pts)

### 1A: The Optimal Layout Challenge (8 pts)

Create `optimal_layout.c`. Given this poorly-ordered struct:

```c
struct Record {
    char    flag;       /* 1 byte */
    double  amount;      /* 8 bytes */
    char    category;    /* 1 byte */
    int     id;          /* 4 bytes */
    short   year;         /* 2 bytes */
    char    active;       /* 1 byte */
};
```

1. Compute `sizeof(struct Record)` as originally ordered. Draw the byte layout.
2. Reorder the fields to **minimize** total size. Compute the new `sizeof`.
3. Write both struct definitions in your file and verify both sizes with `printf`.
4. Compute the percentage memory savings. If you had an array of 1,000,000 such records, how many bytes would you save in total?

### 1B: Struct with Embedded Array (7 pts)

Create `embedded_array.c`. Define:

```c
#define MAX_NAME_LEN 32
#define MAX_TAGS 5

typedef struct {
    char   name[MAX_NAME_LEN];
    int    tags[MAX_TAGS];
    int    tag_count;
    double score;
} Item;
```

Implement:
```c
/* Initialize an item with a name and score, zero tags */
Item item_create(const char *name, double score);

/* Add a tag to the item. Returns 1 on success, 0 if tags array is full. */
int item_add_tag(Item *item, int tag);

/* Return 1 if item has the given tag, 0 otherwise */
int item_has_tag(const Item *item, int tag);

/* Print the item: "Name: Widget, Score: 9.5, Tags: [1, 3, 7]" */
void item_print(const Item *item);

/* Compare two items by score (for qsort). Ascending order. */
int item_compare_score(const void *a, const void *b);
```

Demonstrate with an array of 5 items, sorted by score using `qsort`.

---

## Problem 2: Tagged Unions — A Simple Calculator Value System (20 pts)

Create `calcvalue.h` and `calcvalue.c` — a tagged union representing values in a small calculator language that supports integers, floats, and errors.

```c
typedef enum {
    VAL_INT,
    VAL_FLOAT,
    VAL_ERROR
} ValueType;

typedef struct {
    ValueType type;
    union {
        long   ival;
        double fval;
        const char *error_msg;
    } data;
} Value;

/* Constructors */
Value value_int(long v);
Value value_float(double v);
Value value_error(const char *msg);

/* Predicates */
int value_is_error(const Value *v);
int value_is_numeric(const Value *v);

/* Arithmetic — if either operand is VAL_ERROR, propagate the error.
 * If either operand is VAL_FLOAT, the result is VAL_FLOAT (promote int to float).
 * Division by zero (int or float) produces VAL_ERROR with an appropriate message. */
Value value_add(Value a, Value b);
Value value_sub(Value a, Value b);
Value value_mul(Value a, Value b);
Value value_div(Value a, Value b);

/* Convert to double regardless of type (0.0 for errors) */
double value_to_double(const Value *v);

/* Print: "42" for int, "3.140000" for float, "ERROR: message" for error */
void value_print(const Value *v);
```

### Requirements

- All arithmetic must correctly propagate errors: `value_add(value_error("bad"), value_int(5))` must return the error unchanged
- Division by zero must produce a clear error message: `"Division by zero"`
- Mixed int/float arithmetic promotes to float (matching C's own usual arithmetic conversions)
- Write a `main()` that builds an expression tree evaluation demo:
  ```
  (5 + 3) * 2       → 16
  10 / 0            → ERROR: Division by zero
  (10 / 0) + 5      → ERROR: Division by zero  (propagated)
  3.5 + 2            → 5.500000  (int promoted to float)
  ```

---

## Problem 3: Complete Doubly Linked List (25 pts)

Build a full doubly linked list library — more capable than the singly linked list from lab, supporting O(1) operations at both ends and O(1) deletion given a node pointer.

### `dlinkedlist.h`

```c
#ifndef DLINKEDLIST_H
#define DLINKEDLIST_H

#include <stdbool.h>

typedef struct DNode {
    int data;
    struct DNode *next;
    struct DNode *prev;
} DNode;

typedef struct {
    DNode *head;
    DNode *tail;
    int    size;
} DList;

/* === Lifecycle === */
void  dlist_init(DList *list);
void  dlist_free(DList *list);   /* frees all nodes, resets to empty */

/* === O(1) operations at both ends === */
void  dlist_push_front(DList *list, int value);
void  dlist_push_back(DList *list, int value);
int   dlist_pop_front(DList *list);   /* assert non-empty */
int   dlist_pop_back(DList *list);    /* assert non-empty */

/* === O(1) deletion given a node pointer (the key advantage of doubly linked) === */
void  dlist_delete_node(DList *list, DNode *node);

/* === Search === */
DNode *dlist_find(const DList *list, int value);   /* NULL if not found */

/* === Insertion relative to a node === */
void  dlist_insert_before(DList *list, DNode *node, int value);
void  dlist_insert_after(DList *list, DNode *node, int value);

/* === Query === */
int   dlist_size(const DList *list);
bool  dlist_is_empty(const DList *list);

/* === Traversal helpers === */
void  dlist_print_forward(const DList *list);   /* head to tail */
void  dlist_print_backward(const DList *list);  /* tail to head, using prev */

/* === Advanced === */

/* Reverse the entire list in-place (swap next/prev for every node,
 * then swap head/tail). O(n) time, O(1) space. */
void  dlist_reverse(DList *list);

/* Remove all nodes with the given value. Returns count removed. */
int   dlist_remove_all(DList *list, int value);

/* Rotate the list left by k positions.
 * Example: [1,2,3,4,5] rotated left by 2 → [3,4,5,1,2] */
void  dlist_rotate_left(DList *list, int k);

#endif
```

### Design Requirements

- Maintain the `DList` struct's `head`, `tail`, and `size` fields consistently after **every** operation — this is the hardest part of doubly linked lists
- `dlist_delete_node` must correctly handle: deleting the head, deleting the tail, deleting the only node, and deleting a middle node — four distinct cases
- Draw out each case on paper before coding it (this is not optional — doubly linked list bugs are notoriously subtle)

### Required Test Coverage

Your `test_dlinkedlist.c` must specifically test:
1. Push/pop from both ends interleaved (push_front, push_back, pop_front, pop_back in varying order)
2. `dlist_delete_node` for each of the four cases listed above
3. `dlist_reverse` on empty, single-element, and multi-element lists — verify both forward and backward traversal after reversing
4. `dlist_rotate_left` with k=0, k=size (no-op cases), k > size (should wrap using modulo), and typical k
5. Full Valgrind-clean run

---

## Problem 4: A Student Record System (20 pts)

Build a complete student database using structs, arrays, and a linked list for one component. This problem integrates everything from Weeks 1–4.

Create `student_system.h` and `student_system.c`:

```c
#define MAX_NAME 50
#define MAX_COURSES 6

typedef struct {
    int    course_id;
    char   course_name[MAX_NAME];
    double grade;         /* 0.0 - 4.0 (GPA scale) */
} Course;

typedef struct Student {
    int    id;
    char   name[MAX_NAME];
    Course courses[MAX_COURSES];
    int    course_count;
    struct Student *next;   /* for linking into a roster list */
} Student;

/* === Student management (linked list of students) === */

Student *student_create(int id, const char *name);
Student *roster_add(Student *roster_head, Student *new_student);
Student *roster_find(Student *roster_head, int id);
void     roster_free(Student *roster_head);

/* === Course management (embedded array within a student) === */

int   student_add_course(Student *s, int course_id,
                         const char *course_name, double grade);
double student_gpa(const Student *s);   /* average of all course grades */

/* === Reporting === */

void  student_print(const Student *s);
void  roster_print_all(const Student *roster_head);

/* Return a pointer to the student with the highest GPA in the roster.
 * Returns NULL if roster is empty. */
Student *roster_top_student(Student *roster_head);

/* Return the number of students in the roster with GPA >= threshold */
int   roster_count_above_gpa(const Student *roster_head, double threshold);

/* Sort the roster (the linked list) by GPA descending, using any
 * O(n log n) or better algorithm applied to a linked list (merge sort
 * recommended — see list_merge_sorted pattern from lab).
 * Returns the new head of the sorted list. */
Student *roster_sort_by_gpa(Student *roster_head);
```

### Demo Program

Write a `main()` that:
1. Creates 5 students with 2-4 courses each and varying grades
2. Prints the full roster
3. Reports the top student
4. Reports how many students have GPA >= 3.0
5. Sorts the roster by GPA and prints it again
6. Frees everything and verifies clean under Valgrind

---

## Problem 5: Enum-Driven State Machine — Traffic Light Controller (20 pts)

Create `traffic_light.c`. Build a traffic light simulation using enums and structs (no OOP — pure C state machine).

```c
typedef enum {
    LIGHT_RED,
    LIGHT_YELLOW,
    LIGHT_GREEN
} LightState;

typedef struct {
    LightState state;
    int        seconds_in_state;
    int        red_duration;
    int        yellow_duration;
    int        green_duration;
    long       total_cars_passed;    /* only increments during GREEN */
} TrafficLight;

void       light_init(TrafficLight *light,
                      int red_sec, int yellow_sec, int green_sec);

/* Advance the simulation by one second. Handles state transitions:
 * RED → GREEN → YELLOW → RED → ...
 * When entering GREEN, reset seconds_in_state to 0.
 * cars_this_second: number of cars that pass in this tick
 *   (only counted if light is GREEN; ignored otherwise) */
void       light_tick(TrafficLight *light, int cars_this_second);

const char *light_state_name(LightState state);

void       light_print_status(const TrafficLight *light);

/* Run a full simulation for total_seconds, using a provided array
 * of "cars arriving" values per second (car_arrivals[0..total_seconds-1]).
 * Print the state at every transition (not every second).
 * Return the total number of cars that passed. */
long       light_simulate(TrafficLight *light, const int car_arrivals[],
                          int total_seconds);
```

### Requirements

- Use `-Wswitch` with no `default` case in your state transition logic
- The simulation demo must run at least 60 seconds with realistic timing (e.g., red=30s, yellow=5s, green=25s)
- Generate car arrivals using a simple pattern (e.g., 1-3 cars every few seconds) and show that cars only get counted during GREEN
- Print a summary at the end: total simulation time, total cars passed, cars per green-second average

---

## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -Wswitch -g -std=c11

PROGRAMS = optimal_layout embedded_array calcvalue_test \
           test_dlinkedlist student_system_test traffic_light

all: $(PROGRAMS)

calcvalue_test: calcvalue_test.o calcvalue.o
	$(CC) $(CFLAGS) -o $@ $^

test_dlinkedlist: test_dlinkedlist.o dlinkedlist.o
	$(CC) $(CFLAGS) -o $@ $^

student_system_test: student_system_test.o student_system.o
	$(CC) $(CFLAGS) -o $@ $^

%: %.c
	$(CC) $(CFLAGS) -o $@ $< -lm

clean:
	rm -f $(PROGRAMS) *.o

.PHONY: all clean
```

---

## Submission

```bash
cd ~/prog101/week4/ps4
git add .
git commit -m "PS4 complete: structs, unions, linked lists, enums"
```

Run `valgrind --leak-check=full` on every program with dynamic allocation before submitting.

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Struct design and memory | 15 | Correct layouts, correct savings computation |
| P2: Tagged union calculator | 20 | Error propagation, type promotion, correct arithmetic |
| P3: Doubly linked list | 25 | All 4 deletion cases correct, rotate/reverse correct, Valgrind-clean |
| P4: Student record system | 20 | Integrates structs+arrays+linked list correctly |
| P5: Traffic light state machine | 20 | Correct transitions, correct car counting, -Wswitch clean |
| **Total** | **100** | |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading table above (100 points).
> No errata found. Layouts below were measured with `offsetof` under `gcc 13.3.0` on x86-64 (LP64). Other ABIs will differ — grade the reasoning.

---

### Problem 1 — Struct Design and Memory (15 pts)

**1A Optimal Layout (8 pts).** Measured, not estimated:

**As given — `sizeof(struct Record) = 32`, alignment 8**

| Offset | Contents |
|---|---|
| 0 | `flag` (1) |
| 1–7 | **7 bytes padding** — `amount` needs 8-byte alignment |
| 8 | `amount` (8) |
| 16 | `category` (1) |
| 17–19 | **3 bytes padding** — `id` needs 4-byte alignment |
| 20 | `id` (4) |
| 24 | `year` (2) |
| 26 | `active` (1) |
| 27–31 | **5 bytes tail padding** — round up to a multiple of the struct's 8-byte alignment |

**Reordered largest-alignment-first — `sizeof = 24`**

| Offset | Contents |
|---|---|
| 0 | `amount` (8) |
| 8 | `id` (4) |
| 12 | `year` (2) |
| 14 | `flag` (1) |
| 15 | `category` (1) |
| 16 | `active` (1) |
| 17–23 | 7 bytes tail padding |

**Answers:** payload is 17 bytes; original 32; optimal **24**; saving **8 bytes per record = 25.0%**; across 1,000,000 records **8,000,000 bytes ≈ 7.63 MB**.

*Grading: 3 pts original size with a byte-level layout, 3 pts a reordering achieving 24, 2 pts the savings arithmetic. Accept any ordering that reaches 24 — several do.*
*Two things students get wrong: (i) forgetting **tail** padding, and answering 27 instead of 32 — the struct must be sized so that consecutive elements of an array stay aligned; (ii) assuming the optimum equals the 17-byte payload. It cannot: `amount` forces 8-byte alignment on the whole struct, so the size must be a multiple of 8, and 24 is the smallest multiple of 8 that is ≥ 17.*
*A student who notes that `#pragma pack(1)` would give exactly 17 at the cost of unaligned access has earned a bonus mark — but should also note it is non-standard and can be slow or fault on some architectures.*

**1B Embedded Array (7 pts).**
*`Item` contains its arrays **by value**, so `sizeof(Item)` is fixed and the whole struct copies on assignment and on pass-by-value — no heap, no ownership questions. Make sure students see that `item_create` returning `Item` by value is safe here, whereas returning a struct holding a `char *` to a local would not be.*
*`item_add_tag` must bounds-check against `MAX_TAGS` and return 0 when full — probe by adding 6 tags.*
*`item_create` must NUL-terminate: copying a name longer than `MAX_NAME_LEN-1` with `strncpy` leaves the buffer unterminated (verified behaviour — `strncpy` does not terminate when the source fills the destination). Require an explicit `name[MAX_NAME_LEN-1] = '\0'` or use of `snprintf`. Deduct 2 if absent; this is the same defect flagged in PS2 Problem 3.*
*`item_has_tag` should take `const Item *` — flag missing `const` on all read-only parameters.*

---

### Problem 2 — Tagged Unions (20 pts)

*The discipline being taught: **the tag is the only legitimate way to know which union member is live.** Reading a member that was not the one last written is undefined behaviour (type punning through a union is a common extension, but not what this problem is about).*
*Grade on: (i) every constructor sets the tag; (ii) every consumer `switch`es on the tag before touching the union; (iii) errors propagate — an operation with an error operand yields an error rather than reading a garbage payload; (iv) type promotion follows a documented rule (int ⊕ double → double).*
*Division by zero must produce the error variant, not a trap or a silent `inf`. Probe integer `1/0` (which would raise SIGFPE if actually executed) and floating `1.0/0.0` (which quietly yields `inf`) — both must be caught **before** the operation.*
*Compile with `-Wswitch` (implied by `-Wall`): a `switch` over the tag enum that omits a case warns, and under `-Werror` fails the build. That is the intended safety net — do not let students defeat it with a `default:` that silently swallows new variants.*

---

### Problem 3 — Doubly Linked List (25 pts)

*The four deletion cases named in the rubric — **empty, single-element, head, tail, middle** — are where marks are actually won and lost. Require a test for each; a submission that only tests middle-deletion will pass casually and corrupt `head`/`tail` in production.*

Deletion must fix **four** pointers, and the two boundary ones are conditional:

```c
if (node->prev) node->prev->next = node->next; else list->head = node->next;
if (node->next) node->next->prev = node->prev; else list->tail = node->prev;
free(node);
list->size--;
```

*Omitting either `else` branch leaves a dangling `head`/`tail` — valgrind reports `Invalid read` on the next traversal. Verify with:*

```bash
gcc -Wall -Wextra -Werror -g -std=c11 -o dll dll_test.c dlinkedlist.c
valgrind --leak-check=full --error-exitcode=1 ./dll
```

*A clean run reports `All heap blocks were freed -- no leaks are possible` and `ERROR SUMMARY: 0 errors`; the non-zero exit code makes it script-able. `list_destroy` must free **every** node — the classic leak is freeing the head then losing the rest, or iterating with `free(cur); cur = cur->next;` (use-after-free: save `next` **before** freeing).*
*`reverse` should relink by swapping each node's `prev`/`next` and then swapping `head`/`tail` — O(n), no allocation. `rotate` must handle rotation amounts ≥ size (take modulo) and rotation of an empty or single-element list without crashing.*

---

### Problem 4 — Student Record System (20 pts)

*This is the integration problem: structs inside a linked list, with arrays inside the structs. Grade primarily on **ownership clarity** — for every allocation, who frees it, and is that stated? A record removed from the list must have its heap fields freed too, not just the node.*
*Search/sort routines should take `const` pointers where they don't mutate. Any sort should reuse the generic comparator machinery from PS3 P5A rather than duplicating it — cross-reference and reward the reuse.*
*Must be valgrind-clean under the same command as Problem 3.*

---

### Problem 5 — Traffic Light State Machine (20 pts)

*`-Wswitch` clean is an explicit rubric item: switch on the enum **without** a `default:` so that adding a state later produces a compile-time warning naming every unhandled switch. A `default: break;` defeats this and should cost marks even though the program works — the point of the exercise is compiler-enforced exhaustiveness.*
*Do not compare enum values against raw integers, and do not rely on the numeric values of enumerators unless they are explicitly assigned.*
*Car counting is the correctness trap: cars should only pass on the state that permits it, and the count must not advance during the transition/amber state. Require the test output to show a full cycle with the running total, so an off-by-one in the tick loop is visible.*
*Transition table should be data (`struct { State from; Event ev; State to; }` or a 2-D array) rather than nested `if`s — same design point as PS3 P5B; award at most half the design credit for an `if` cascade.*

---

*PROG 101 · Week 7 · Problem Set 7 · © CSE Department*
