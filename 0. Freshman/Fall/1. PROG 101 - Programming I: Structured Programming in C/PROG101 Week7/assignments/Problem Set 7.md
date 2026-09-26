# PROG 101 · Programming I: Structured Programming in C
## Week 7 · Problem Set 7

**Released:** Thursday 12 November 2026, 11:00 (after Week 7 Lecture 3)
**Due:** Tuesday 17 November 2026, 10:00 (start of Week 8 Lecture 1) — late penalty from 10:01
**Directory:** `"$PROG101/week7/ps7"` in the Freshman Fall repo
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: Lab 7, on Monday 16 November, does the struct-layout investigation and a tagged-union
system, so old 1A and Problem 2 are now only in the lab. 1B no longer sorts with `qsort`: its comparator is a
function pointer, which is Week 11. The roster's sorted insertion was removed too. The answer key moved out
of this handout.)*

**What this uses:** Weeks 0–7 — structs, layout and padding, `typedef`, unions and tagged unions, enums and
bit fields, singly linked lists with insertion, deletion and the pointer-to-pointer technique (Lecture 03).
**Not needed:** a doubly linked list (Lecture 03 only previews it), sorting a linked list (merge sort is
Week 9), function pointers (Week 11).

---

## Problem 1: A Struct with an Embedded Array (20 pts)


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
```

Demonstrate with an array of 5 items: print them all, then find and print the one with the highest score.

---

## Problem 2: A Student Record System (45 pts)

Build a complete student database using structs, arrays, and a linked list for one component. This problem integrates everything from Weeks 1–7.

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
```

### Demo Program

Write a `main()` that:
1. Creates 5 students with 2-4 courses each and varying grades
2. Prints the full roster
3. Reports the top student
4. Reports how many students have GPA >= 3.0
5. Frees everything and verifies clean under Valgrind

---

## Problem 3: Enum-Driven State Machine — Traffic Light Controller (35 pts)

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

PROGRAMS = embedded_array student_system_test traffic_light

all: $(PROGRAMS)

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
cd "$PROG101/week7/ps7"
git add .
git commit -m "PROG 101 PS 7: structs, unions, linked lists, enums"
```

Run `valgrind --leak-check=full` on every program with dynamic allocation before submitting.

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Struct with an embedded array | 20 | Correct bounds on names and tags |
| P2: Student record system | 45 | Structs + arrays + linked list; Valgrind-clean |
| P3: Traffic light state machine | 35 | Correct transitions, correct car counting, -Wswitch clean |
| **Total** | **100** | |

---

*PROG 101 · Week 7 · Problem Set 7 · Due Tuesday 17 November 2026, 10:00 · © CSE Department*
