# PROG 101 · Programming I: Structured Programming in C
## Week 8 · Lab 8: Building a Persistent Student Record Database

**Graded: 20 points**
**Duration:** 2 hours
**Lab session:** Monday of Week 9 — sat after this week's Tue–Thu lectures, and covers Week 8.
**Submission:** Push to Git, show TA before leaving

---

## Overview

- **Part 1:** Text file processing — a CSV-based grade importer
- **Part 2:** Binary file basics — struct persistence and random access
- **Part 3:** A complete fixed-record binary database (the main deliverable)

---

## Part 1: CSV Grade Importer (5 pts)

Create `csv_import.c`. You are given a CSV file `grades.csv` with the format:

```
name,course,grade
Alice,PROG101,92
Bob,PROG101,78
Alice,MATH141,88
Charlie,PROG101,95
Bob,MATH141,81
```

Implement:

```c
typedef struct {
    char name[50];
    char course[20];
    int  grade;
} GradeEntry;

/* Read all entries from a CSV file. Returns the count read,
 * fills entries[] (caller provides array with max_entries capacity).
 * Returns -1 on file open failure. */
int csv_read_grades(const char *filename, GradeEntry entries[], int max_entries);

/* Compute the average grade for a given student name across all their entries. */
double average_for_student(const GradeEntry entries[], int n, const char *name);

/* Compute the average grade for a given course across all students. */
double average_for_course(const GradeEntry entries[], int n, const char *course);

/* Write a summary report to a new file: one line per unique student,
 * showing their average across all courses.
 * Format: "Alice: 90.00\n" */
void write_summary(const char *filename, const GradeEntry entries[], int n);
```

Requirements:
- Skip the header line (`name,course,grade`)
- Handle malformed lines gracefully (skip them, print a warning to stderr with the line number)
- The main program takes the CSV filename as `argv[1]` and an output filename as `argv[2]`
- Provide `grades.csv` as a test fixture with at least 15 rows across 3 students and 3 courses

---

## Part 2: Binary Struct Persistence Basics (5 pts)

Create `binary_basics.c`. Demonstrate and verify each of these operations:

```c
typedef struct {
    int    id;
    char   title[64];
    double price;
} Product;

/* Write an array of products to a binary file in one call */
int products_save(const char *filename, const Product products[], int n);

/* Load all products from a binary file. Returns the count loaded
 * (determined from file size / record size), fills products[]
 * (caller-provided array, must have capacity for the loaded count —
 * use products_count first to determine required size). */
int products_load(const char *filename, Product products[], int max_products);

/* Return how many product records are in the file, without loading them. */
long products_count(const char *filename);

/* Update the price of the product at the given index (0-based) in the file.
 * Uses fseek to modify in place — does NOT rewrite the whole file. */
int products_update_price(const char *filename, int index, double new_price);
```

Requirements:
- Zero every struct with `memset` before filling fields (avoid uninitialized padding — verify with Valgrind that no "uninitialised value" warnings occur)
- `products_update_price` must be O(1) — use `fseek` to the exact byte offset, not rewrite-the-whole-file
- Demonstrate: save 5 products, load them back and verify contents match, update one product's price using `products_update_price`, reload and verify only that product changed

---

## Part 3: The Student Database (10 pts)

Build a complete, persistent, fixed-record student database. This is a file-backed extension of the in-memory student system from PS4.

### `studentdb.h`

```c
#ifndef STUDENTDB_H
#define STUDENTDB_H

#include <stdio.h>

#define SDB_NAME_LEN 50

typedef struct {
    int    id;
    char   name[SDB_NAME_LEN];
    double gpa;
    int    is_deleted;    /* tombstone flag: 0 = active, 1 = deleted */
} StudentRecord;

/* === Database lifecycle === */

/* Open (creating if necessary) the database file. Returns NULL on failure. */
FILE *sdb_open(const char *filename);

/* Close the database file. */
void  sdb_close(FILE *fp);

/* === CRUD operations === */

/* Append a new student record. Returns the new record's index, or -1 on failure. */
int   sdb_create(FILE *fp, int id, const char *name, double gpa);

/* Read the record at the given index. Returns 0 on success, -1 on failure
 * (including if the record is out of range). Does NOT check is_deleted —
 * caller should check out->is_deleted if needed. */
int   sdb_read(FILE *fp, int index, StudentRecord *out);

/* Update the gpa of the record at the given index. Returns 0 on success. */
int   sdb_update_gpa(FILE *fp, int index, double new_gpa);

/* Mark the record at the given index as deleted (tombstone). Returns 0 on success. */
int   sdb_delete(FILE *fp, int index);

/* === Queries === */

/* Return the total number of records in the file (including tombstoned). */
long  sdb_total_records(FILE *fp);

/* Return the number of ACTIVE (non-deleted) records. */
long  sdb_active_count(FILE *fp);

/* Find the index of the first active record with the given id.
 * Returns -1 if not found. */
int   sdb_find_by_id(FILE *fp, int id);

/* Print all active records in a formatted table. */
void  sdb_print_all(FILE *fp);

/* Compute the average GPA across all active records.
 * Returns 0.0 if there are no active records. */
double sdb_average_gpa(FILE *fp);

/* Find the index of the active record with the highest GPA.
 * Returns -1 if there are no active records. */
int   sdb_top_student(FILE *fp);

/* === Maintenance === */

/* Compact the database: rewrite it to a new file containing only
 * active records, removing all tombstones. Returns the count of
 * records written, or -1 on failure.
 * After calling this, the caller should close the old fp, delete the
 * old file, and rename the new file (or sdb_open the new file directly). */
int   sdb_compact(FILE *fp, const char *new_filename);

#endif
```

### Implementation Requirements

- Every record read/write must go through `fseek` to the correct byte offset (`index * sizeof(StudentRecord)`) — no full-file scanning except where explicitly required (e.g., `sdb_print_all`, `sdb_find_by_id`, which must scan by nature)
- `sdb_open` should open in `"rb+"` mode if the file exists, or create it with `"wb+"` if it doesn't (hint: try `"rb+"` first; if it fails, use `"wb+"`)
- Always `memset` a `StudentRecord` to zero before filling it, to avoid writing uninitialized padding
- `sdb_compact` must correctly rebuild indices — after compaction, the first active record becomes index 0, etc.

### `test_studentdb.c`

Write a thorough test program that:

1. Creates a fresh database file (delete any existing test file first)
2. Adds 8 students with varying GPAs
3. Verifies `sdb_total_records` and `sdb_active_count` both equal 8
4. Reads back several students by index and verifies contents
5. Updates one student's GPA and verifies the change persisted (close and reopen the file to prove it wasn't just an in-memory change)
6. Deletes 2 students (tombstone)
7. Verifies `sdb_active_count` is now 6 while `sdb_total_records` is still 8
8. Finds a student by id and verifies correctness
9. Computes and verifies the average GPA (across active records only)
10. Finds and verifies the top student
11. Compacts the database and verifies the new file has exactly 6 records, all active
12. Cleans up: removes test files

Print clear PASS/FAIL output for each check, following the pattern from previous weeks' test suites.

### Valgrind Requirement

```bash
valgrind --leak-check=full ./test_studentdb
```

Must report 0 errors, 0 leaks, and **no "uninitialised value" warnings** (this specifically catches forgetting to `memset` before writing).

---

## Deliverables

```
week5/lab5/
├── csv_import.c
├── grades.csv                # test fixture, at least 15 rows
├── binary_basics.c
├── studentdb.h
├── studentdb.c
├── test_studentdb.c
├── Makefile
└── LAB 8 File IO Studentdb.md             # brief notes on any design decisions
```

**Makefile:**
```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

all: csv_import binary_basics test_studentdb

test_studentdb: test_studentdb.o studentdb.o
	$(CC) $(CFLAGS) -o $@ $^

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f csv_import binary_basics test_studentdb *.o *.bin *.db

.PHONY: all clean
```

---

## Grading

| Part | Points | Criteria |
|------|--------|---------|
| 1: CSV import | 5 | Correct parsing, malformed line handling, correct averages |
| 2: Binary basics | 5 | Correct save/load/update, O(1) update, zeroed padding |
| 3: Student database | 10 | All CRUD operations correct, tombstone/compact correct, Valgrind-clean |
| **Total** | **20** | |
