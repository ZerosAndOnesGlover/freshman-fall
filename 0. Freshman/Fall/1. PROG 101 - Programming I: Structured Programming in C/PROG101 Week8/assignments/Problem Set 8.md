# PROG 101 · Programming I: Structured Programming in C
## Week 8 · Problem Set 8

**Released:** Thursday 19 November 2026, 11:00 (after Week 8 Lecture 3)
**Due:** Tuesday 24 November 2026, 10:00 (start of Week 9 Lecture 1) — late penalty from 10:01
**Directory:** `"$PROG101/week8/ps8"` in the Freshman Fall repo
**Total:** 100 points · **Expected time:** about 4 hours

**What this uses:** Weeks 0–8 — this week's `FILE *` I/O, `fgets`/`fprintf`, `argc`/`argv` as the Lecture 01 and
Lecture 02 examples use them, low-level descriptors, `fseek`/`ftell`, and binary records with `fread`/`fwrite`.
(Revised 2026-09-21: the key-value store problem was removed to fit the five-day window.)

---

## Problem 1: Text File Utilities (25 pts)

Create `text_utils.c`. Implement a small suite of command-line text file tools, dispatched by `argv[1]`:

```bash
./text_utils count <file>              # line, word, char counts (like `wc`)
./text_utils grep <pattern> <file>     # print lines containing pattern
./text_utils numbered <file>           # print with line numbers
./text_utils tail <n> <file>           # print last n lines
./text_utils uniq <file>               # remove consecutive duplicate lines
```

### Requirements

```c
/* Print: "  <lines>  <words>  <chars> <filename>" (matches `wc` format) */
void cmd_count(const char *filename);

/* Print every line containing the substring pattern (case-sensitive,
 * simple substring match — no regex needed).
 * Prefix each match with the line number: "42: matching line text" */
void cmd_grep(const char *pattern, const char *filename);

/* Print every line prefixed with its 1-based line number, right-aligned
 * in a 4-character field: "   1  first line\n   2  second line\n" */
void cmd_numbered(const char *filename);

/* Print the last n lines of the file.
 * Approach: read the whole file into memory (assume it fits), track the
 * last n lines using a circular buffer of line start pointers/offsets. */
void cmd_tail(int n, const char *filename);

/* Print each line, but suppress consecutive duplicate lines
 * (matches Unix `uniq` behavior — only ADJACENT duplicates are collapsed). */
void cmd_uniq(const char *filename);
```

### Error Handling

- If the file cannot be opened, print `Error: cannot open '<filename>': <reason>` to stderr and exit with code 1
- If the command is unrecognized, print a usage message listing all 5 subcommands and exit with code 1
- If required arguments are missing, print a usage message for that specific subcommand

Provide a test file `sample.txt` (at least 20 lines, some duplicated, some containing a testable pattern) and demonstrate all 5 subcommands against it.

---

## Problem 2: A Configuration File Parser (20 pts)

Create `config_parser.c`/`config_parser.h`. Parse simple INI-style configuration files:

```ini
# This is a comment
name = MyApplication
version = 2.5
debug = true

[server]
host = localhost
port = 8080

[database]
host = db.example.com
port = 5432
max_connections = 100
```

```c
#define MAX_KEY_LEN 64
#define MAX_VALUE_LEN 256
#define MAX_ENTRIES 100

typedef struct {
    char section[MAX_KEY_LEN];   /* "" for entries before any [section] */
    char key[MAX_KEY_LEN];
    char value[MAX_VALUE_LEN];
} ConfigEntry;

typedef struct {
    ConfigEntry entries[MAX_ENTRIES];
    int         count;
} Config;

/* Parse the file into a Config structure. Returns 0 on success, -1 on failure. */
int  config_load(const char *filename, Config *cfg);

/* Look up a value by section and key. Returns NULL if not found.
 * Use section = "" for top-level keys (before any [section]). */
const char *config_get(const Config *cfg, const char *section, const char *key);

/* Convenience wrappers with type conversion and a default value if not found */
int    config_get_int(const Config *cfg, const char *section,
                      const char *key, int default_val);
double config_get_double(const Config *cfg, const char *section,
                         const char *key, double default_val);
int    config_get_bool(const Config *cfg, const char *section,
                       const char *key, int default_val);

/* Print the entire parsed configuration in a readable format for debugging */
void   config_print(const Config *cfg);
```

### Parsing Rules

- Lines starting with `#` (after optional leading whitespace) are comments — ignore entirely
- Blank lines are ignored
- `[section]` lines start a new section (persists until the next `[section]` or EOF)
- `key = value` lines: trim whitespace around both key and value
- Lines that don't match any pattern: print a warning to stderr with the line number, but continue parsing

Provide a sample `.ini` file matching the example above and demonstrate every accessor function.

---

## Problem 3: Log File Analyzer (30 pts)

Create `log_analyzer.c`. Process a server log file with this format (one entry per line):

```
2024-01-15 08:23:11 INFO Request served in 45ms
2024-01-15 08:23:15 ERROR Database connection failed
2024-01-15 08:23:16 WARNING Retrying connection
2024-01-15 08:23:20 INFO Request served in 120ms
2024-01-15 08:24:01 ERROR Timeout waiting for response
```

Format: `YYYY-MM-DD HH:MM:SS SEVERITY message text...`

```c
typedef struct {
    char year[5], month[3], day[3];
    char hour[3], minute[3], second[3];
    char severity[10];
    char message[200];
} LogEntry;

/* Parse a single log line into a LogEntry. Returns 0 on success, -1 on
 * malformed line. */
int  parse_log_line(const char *line, LogEntry *entry);

/* Read the whole file, count occurrences of each severity level.
 * Fills counts[0]=INFO, counts[1]=WARNING, counts[2]=ERROR, counts[3]=other.
 * Returns the total number of valid lines parsed, or -1 on file error. */
int  count_by_severity(const char *filename, int counts[4]);

/* Extract all "Request served in Nms" messages and compute:
 * min, max, average response time in milliseconds.
 * Returns the count of such messages found. Stores results via pointers. */
int  analyze_response_times(const char *filename,
                            int *min_ms, int *max_ms, double *avg_ms);

/* Print all ERROR-severity lines, in order, to stdout. */
void print_all_errors(const char *filename);

/* Find the hour (00-23) with the most ERROR entries.
 * Returns the hour (0-23), or -1 if there are no errors. */
int  find_worst_hour(const char *filename);

/* Generate a summary report to a new file:
 *   === Log Summary ===
 *   Total entries: N
 *   INFO: N (X%)
 *   WARNING: N (X%)
 *   ERROR: N (X%)
 *   Response times: min=Xms max=Xms avg=X.Xms
 *   Worst hour for errors: HH:00
 */
void generate_report(const char *log_filename, const char *report_filename);
```

### Requirements

- Provide a `sample.log` fixture with at least 40 entries spanning multiple hours, all three severities, and at least 15 "Request served in Nms" style INFO messages
- Malformed lines must be skipped (not crash the program) with a warning to stderr including the line number
- All percentage calculations formatted to 1 decimal place

---

## Problem 4: Binary Inventory System (25 pts)

Build a complete fixed-record binary inventory management system — similar structure to the Lab 8 student database, but for a different domain, demonstrating you can apply the pattern independently.

### `inventory.h`

```c
#ifndef INVENTORY_H
#define INVENTORY_H

#include <stdio.h>

typedef struct {
    int    sku;
    char   name[64];
    int    quantity;
    double unit_price;
    int    is_deleted;
} InventoryItem;

FILE  *inv_open(const char *filename);
void   inv_close(FILE *fp);

int    inv_add(FILE *fp, int sku, const char *name, int qty, double price);
int    inv_read(FILE *fp, int index, InventoryItem *out);
int    inv_update_quantity(FILE *fp, int index, int new_qty);
int    inv_update_price(FILE *fp, int index, double new_price);
int    inv_remove(FILE *fp, int index);   /* tombstone */

int    inv_find_by_sku(FILE *fp, int sku);
long   inv_total_items(FILE *fp);          /* including tombstoned */
long   inv_active_items(FILE *fp);

/* Sell 'amount' units of the item at the given index.
 * Decreases quantity by amount. Returns 0 on success.
 * Returns -1 if amount > current quantity (insufficient stock — no change made)
 * or if the record doesn't exist/is deleted. */
int    inv_sell(FILE *fp, int index, int amount);

/* Restock: increase quantity by amount. Returns 0 on success. */
int    inv_restock(FILE *fp, int index, int amount);

/* Compute total inventory value: sum of (quantity * unit_price) 
 * across all active items. */
double inv_total_value(FILE *fp);

/* Find all items with quantity below the given threshold.
 * Fills out_indices[] with matching indices (caller provides array with
 * capacity max_results). Returns the count found (may exceed max_results,
 * in which case only the first max_results are filled — but the full
 * count is still returned so the caller knows if results were truncated). */
int    inv_find_low_stock(FILE *fp, int threshold,
                          int out_indices[], int max_results);

void   inv_print_all(FILE *fp);

#endif
```

### Demo Program Requirements

Write `main()` in a separate `inventory_demo.c` that:
1. Creates an inventory with 10 different products
2. Simulates 15 sell transactions (some may fail due to insufficient stock — handle gracefully, print a message, continue)
3. Simulates 5 restock transactions
4. Prints the full inventory
5. Reports total inventory value
6. Finds and reports all items with quantity below 5
7. Removes 2 discontinued items (tombstone)
8. Prints final active inventory
9. Verifies everything is Valgrind-clean

---

## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = text_utils config_test log_analyzer inventory_demo

all: $(PROGRAMS)

config_test: config_test.o config_parser.o
	$(CC) $(CFLAGS) -o $@ $^

inventory_demo: inventory_demo.o inventory.o
	$(CC) $(CFLAGS) -o $@ $^

%: %.c
	$(CC) $(CFLAGS) -o $@ $< -lm

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(PROGRAMS) *.o *.bin *.db *.log

.PHONY: all clean
```

---

## Submission

```bash
cd "$PROG101/week8/ps8"
git add .
git commit -m "PS5 complete: file I/O, binary records, key-value store"
```

All programs performing dynamic allocation or binary file writes must be Valgrind-clean before submission.

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Text file utilities | 25 | All 5 subcommands correct, matches Unix tool behavior |
| P2: Config parser | 20 | Correct section/key/value parsing, type conversions |
| P3: Log analyzer | 30 | Correct parsing, all analytics correct, malformed lines handled |
| P4: Binary inventory | 25 | All CRUD + business logic correct, Valgrind-clean |
| **Total** | **100** | |

---

## Answer Key (Instructor Copy)

> **Do not distribute to students.** Totals follow the Grading table above (100 points).
> No errata found. Compile/verify with `gcc 13.3.0 -Wall -Wextra -Werror -g -std=c11`; memory claims under `valgrind --leak-check=full --error-exitcode=1`.

---

### Cross-cutting file-I/O criteria (apply to every problem)

These recur in all five problems and are where most marks are lost. Check each explicitly:

1. **Every `fopen` is checked.** `if (!fp) { perror(path); return ...; }`. An unchecked `fopen` followed by `fgets` is a NULL dereference. Deduct 2 per occurrence.
2. **Every successful `fopen` has a matching `fclose` on every exit path**, including error returns. This is the most common leak in this problem set and valgrind will *not* always flag it (the OS reclaims fds at exit) — read the code, don't rely on the tool.
3. **Read with `fgets`, never `gets`** (removed from C11) and never bare `scanf("%s")`. `fgets` keeps the trailing `'\n'` — it must be stripped, and code that assumes it was stripped breaks on the final line of a file with no terminating newline.
4. **Check the return of every write.** `fprintf`/`fwrite` can fail (disk full, closed pipe); silently ignoring this loses data.
5. **Binary files must be opened with `"rb"`/`"wb"`.** On Linux this is a no-op, so a student omitting it will see no failure — award the point only if present, and explain that it matters on Windows where `"r"` performs CRLF translation and corrupts binary records.
6. **`feof()` is not a loop condition.** `while (!feof(fp)) { fgets(...); n++; }` reads one time too many, because EOF is only set *after* a read has already failed. The correct idiom is `while (fgets(...))` or `while (fread(...) == 1)`.

   The trap is that **the bug is data-dependent** — verified line counts for the same code:

   | Input | correct (`fgets`) | `feof` loop | |
   |---|---|---|---|
   | 3 lines, trailing newline | 3 | **4** | overcounts |
   | 3 lines, no trailing newline | 3 | 3 | *happens to be right* |
   | empty file | 0 | **1** | overcounts |

   So a submission using `feof` can pass a test fixture that lacks a final newline and still be wrong on ordinary input. **Test with a trailing-newline file and an empty file**, not just whatever the student supplied.

---

### Problem 1 — Text File Utilities (25 pts)

*Behaviour should match the Unix tools it imitates. The boundary cases that separate a working implementation from an approximate one: an **empty file** (0 lines, 0 words, 0 bytes — not 1 line); a file whose **last line lacks a newline** (still counts as a line); **CRLF** input (`\r` must not be counted as a word character); and lines longer than the read buffer (must not be silently truncated or counted twice).*
*`wc`-style counting: a "word" is a maximal run of non-whitespace. The usual bug is counting *transitions into* whitespace, which miscounts when the file ends mid-word or begins with whitespace.*

### Problem 2 — Configuration File Parser (20 pts)

*Grade the parsing rules as a spec: comments, blank lines, `[section]` headers, `key = value` with surrounding whitespace trimmed on **both** key and value, and values containing `=` (only the **first** `=` separates). That last one is the discriminating test — `url = http://x/?a=b` must keep the whole RHS.*
*Type conversion must **detect failure**, not silently yield 0 — `strtol`/`strtod` with `endptr` checking, as in PS0 Problem 3. A config reader that turns a typo into 0 is worse than one that errors.*
*Unterminated `[section` and duplicate keys need a documented policy (error vs last-wins). Either is fine; silence is not.*

### Problem 3 — Log File Analyzer (30 pts)

*"Malformed lines handled" is an explicit rubric item: the analyzer must skip or report bad lines and continue, never abort or miscount. Seed the test data with a truncated line, an empty line, and a line with the wrong field count.*
*Fixed-width `%s` in `sscanf` is mandatory — `sscanf(line, "%s", buf)` with an unbounded `buf` is an exploitable overflow. Require `%31s` style width limits matched to the buffer, and check the **return value** of `sscanf` against the expected field count; that return is how malformed lines are detected in the first place.*
*Counting/aggregation should be exact: verify totals against a hand-computed fixture rather than eyeballing.*

### Problem 4 — Binary Inventory System (25 pts)

*The core lesson is that a binary record file is an **array on disk**: record *i* lives at byte offset `i * sizeof(Record)`, so `fseek(fp, i * sizeof(Record), SEEK_SET)` gives O(1) random access — versus a text format where finding record *i* requires scanning. Require the student to state this.*
*Portability caveat worth a bonus mark if raised: `fwrite`ing a struct directly embeds this platform's **padding, endianness, and type sizes**. The file is not portable to a different ABI. (Cross-reference PS4 P1A — the same padding that cost 8 bytes per record is now baked into the file format.) Serialising field-by-field avoids it.*
*Never `fwrite` a struct containing a **pointer** — the address is meaningless once reloaded. If any record holds a `char *`, the design is wrong; it must be a fixed `char[N]`.*
*Deletion policy must be explicit — tombstone flag vs. compaction — and CRUD must round-trip: write, close, reopen, read, and compare. Valgrind-clean is a rubric item.*

*PROG 101 · Week 8 · Problem Set 8 · © CSE Department*
