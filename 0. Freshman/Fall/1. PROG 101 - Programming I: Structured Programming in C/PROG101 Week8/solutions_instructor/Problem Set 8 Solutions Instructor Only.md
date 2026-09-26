# PROG 101 · Problem Set 8 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: Problem 4 (binary inventory), `tail`, `uniq`, `find_worst_hour` and `generate_report` are no
longer asked. Points: P1 30, P2 30, P3 40.)*

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
