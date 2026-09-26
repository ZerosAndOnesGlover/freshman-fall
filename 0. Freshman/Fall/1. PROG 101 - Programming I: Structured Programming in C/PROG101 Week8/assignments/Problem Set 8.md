# PROG 101 · Programming I: Structured Programming in C
## Week 8 · Problem Set 8

**Released:** Thursday 19 November 2026, 11:00 (after Week 8 Lecture 3)
**Due:** Tuesday 24 November 2026, 10:00 (start of Week 9 Lecture 1) — late penalty from 10:01
**Directory:** `"$PROG101/week8/ps8"` in the Freshman Fall repo
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: cut from about four hours to three. Lab 8, on Monday 23 November, builds a binary struct
database, so the binary inventory (old Problem 4) is now only in the lab. `tail`, `uniq`, `find_worst_hour` and
`generate_report` were removed, and the log fixture is smaller. The answer key moved out of this handout.)*

**What this uses:** Weeks 0–8 — this week's `FILE *` I/O, `fgets`/`fprintf`, `argc`/`argv` as the Lecture 01 and
Lecture 02 examples use them, low-level descriptors, `fseek`/`ftell`, and binary records with `fread`/`fwrite`.
(Revised 2026-09-21: the key-value store problem was removed to fit the five-day window.)

---

## Problem 1: Text File Utilities (30 pts)

Create `text_utils.c`. Implement a small suite of command-line text file tools, dispatched by `argv[1]`:

```bash
./text_utils count <file>              # line, word, char counts (like `wc`)
./text_utils grep <pattern> <file>     # print lines containing pattern
./text_utils numbered <file>           # print with line numbers
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
```

### Error Handling

- If the file cannot be opened, print `Error: cannot open '<filename>': <reason>` to stderr and exit with code 1
- If the command is unrecognized, print a usage message listing all 3 subcommands and exit with code 1
- If required arguments are missing, print a usage message for that specific subcommand

Provide a test file `sample.txt` (at least 20 lines, some containing a testable pattern) and demonstrate all 3 subcommands against it.

---

## Problem 2: A Configuration File Parser (30 pts)

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

## Problem 3: Log File Analyzer (40 pts)

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
```

### Requirements

- Provide a `sample.log` fixture with at least 20 entries covering all three severities, and at least 8 "Request served in Nms" style INFO messages
- Malformed lines must be skipped (not crash the program) with a warning to stderr including the line number

---

## Makefile

```makefile
CC     = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

PROGRAMS = text_utils config_test log_analyzer

all: $(PROGRAMS)

config_test: config_test.o config_parser.o
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
git commit -m "PS 8 complete: text utilities, config parser, log analyzer"
```

All programs performing dynamic allocation must be Valgrind-clean before submission.

---

## Grading

| Problem | Points | Key Criteria |
|---------|--------|-------------|
| P1: Text file utilities | 30 | All 3 subcommands correct, matches Unix tool behavior |
| P2: Config parser | 30 | Correct section/key/value parsing, type conversions |
| P3: Log analyzer | 40 | Correct parsing, all analytics correct, malformed lines handled |
| **Total** | **100** | |

---

*PROG 101 · Week 8 · Problem Set 8 · Due Tuesday 24 November 2026, 10:00 · © CSE Department*
