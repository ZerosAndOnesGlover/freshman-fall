# PROG 101 · Week 8
## LAB 8 Solutions — INSTRUCTOR ONLY

> **Every implementation below compiles under `gcc -Wall -Wextra -Werror -std=c11` and runs clean
> under `-fsanitize=address,undefined`.** Where the lab requires it, Valgrind output is quoted
> verbatim. Reject any submission that does not build warning-free — `-Werror` is not negotiable in
> this course.

---

## Part 1 — CSV Grade Importer

Parsing requirements:

- `fgets` in a loop, checking the return value. **Never `while (!feof(f))`** — it miscounts in a
  data-dependent way (4 lines for a 3-line file with a trailing newline, 1 for an empty file). See
  the Week 8 Lecture 1 exercises for the measured table.
- `strcspn(line, "\n")` to strip the newline `fgets` retains.
- `strtok` splits on delimiters but **collapses consecutive ones**, so it cannot represent an empty
  field — `a,,b` yields two tokens, not three. For real CSV, scan manually with `strchr`, or accept
  `strtok` with the limitation documented.
- Convert with `strtod`/`strtol` and **check the `endptr`**, not `atoi`, which returns 0 for both
  `"0"` and `"abc"` and gives you no way to tell them apart.
- Every `fopen` result checked; `perror(path)` on failure.

---

## Part 2 — Binary Struct Persistence

```c
struct Rec { int id; double score; char name[8]; };
sizeof(struct Rec) == 24        /* 4 (id) + 4 PADDING + 8 (score) + 8 (name) */
```

The members total 20 bytes; 4 are padding, because `double` needs 8-byte alignment so `score`
cannot start at offset 4. Writing the struct produces a **24-byte** file, verified with
`fseek(f, 0, SEEK_END); ftell(f)`.

**`fwrite` writes the padding too** — including its contents, which are indeterminate and may hold
leftover stack data. Zero the struct with `= {0}` or `memset` before filling it, or a record file
can leak bytes that were never part of the record.

**`fread`/`fwrite` return an ITEM count, not a byte count.** Check `== 1`, not `== sizeof r`.

### The four portability hazards

| Hazard | Fix |
|---|---|
| Padding/alignment differ between compilers and architectures | Serialise **field by field** |
| Endianness (x86 little, network big) | Fixed byte order — `htonl`/`ntohl` or explicit shifts |
| Type sizes (`long` is 8 on Linux, 4 on Windows) | `int32_t`, `uint64_t` from `<stdint.h>` |
| Floating-point representation | Write the bit pattern as a fixed-width integer, or use text |

Always open binary files with `"b"` (`"rb"`, `"wb"`). On Linux it changes nothing; on Windows text
mode translates `\n` ↔ `\r\n` and silently corrupts binary data.

Add a **magic number and a version field** at the head of any real format, so a future reader can
reject a file it does not understand rather than misinterpret it.

---

## Part 3 — `studentdb`

### Random access is the whole point of fixed-size records

```c
int db_read_record(FILE *f, long n, Student *out) {
    if (n < 0) return 0;
    if (fseek(f, n * (long)sizeof *out, SEEK_SET) != 0) return 0;
    return fread(out, sizeof *out, 1, f) == 1;
}
```

Record `n` begins at offset `n * sizeof(Student)` — a multiplication, no scanning. Reading record
50,000 costs one seek and one read regardless of file size: **O(1)**, the same reasoning that makes
array indexing O(1). A variable-length text format cannot do this without a separate index.

Cast to `long` before multiplying: `n * sizeof *out` with an `int` `n` overflows past ~89 million
records, and `fseek` takes a `long` offset. Use `fseeko`/`off_t` for files beyond 2 GB.

### Deletion

Two designs, both acceptable if documented:

- **Tombstone** — set an `active` flag to 0. O(1), but the file never shrinks and every scan must
  skip dead records. This is what real databases do.
- **Swap with last and truncate** — O(1) but destroys record order, which invalidates any stored
  record numbers held elsewhere.

**Shifting all subsequent records is O(n) per delete and should lose marks** unless the handout
demands stable ordering.

### Grading

- Every `fopen`, `fread`, `fwrite`, `fseek` return checked.
- `fclose` on every path, including error paths — the commonest leak in this lab is a file
  descriptor, not memory, and Valgrind will not report it. Check by reading the code.
- Buffers filled with `snprintf`, never `strcpy`, and never `strncpy` without a manual terminator.
- **Valgrind: 0 errors, 0 leaks.**

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

*PROG 101 · Week 8 · Lab Solutions · Instructor Copy · © CSE Department*
