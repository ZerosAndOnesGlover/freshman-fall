# PROG 101 · Quiz 8
## Week 9, Tuesday — In-Class Assessment

**Administered:** start of Week 9, Lecture 1 (Tuesday)
**Covers:** Week 8 material
**Duration:** 10 minutes · Closed book · 20 points

---

## Section A — Multiple Choice (2 pts each)

**1.** What does `fopen("data.txt", "w")` do if `data.txt` already exists and contains data?

- (A) Appends new data to the end, preserving existing content
- (B) Returns `NULL` — refuses to open an existing file
- (C) Truncates the file to zero length, erasing all existing content
- (D) Opens in read-only mode automatically

---

**2.** Why must the character variable used to hold the result of `fgetc` be declared as `int`, not `char`?

- (A) `fgetc` is faster when returning an `int`
- (B) `EOF` is a value outside the range of `char` on some platforms, and using `char` risks misinterpreting a valid byte as EOF
- (C) `char` cannot be compared with `!=`
- (D) There is no real reason; `char` works identically

---

**3.** What is the key advantage of a fixed-record binary file over a text (CSV) file for a database-like use case?

- (A) Binary files are always smaller
- (B) Binary files allow O(1) random access to any record by index via `fseek`
- (C) Binary files don't need error checking
- (D) Binary files are portable across all platforms without any caveats

---

**4.** Which of these correctly determines a file's size in bytes using `FILE *`?

- (A) `fscanf(fp, "%d", &size);`
- (B) `size = fread(fp, 1, 1, NULL);`
- (C) `fseek(fp, 0, SEEK_END); size = ftell(fp); rewind(fp);`
- (D) `size = sizeof(fp);`

---

**5.** Why should you `memset` a struct to zero before writing it to a binary file with `fwrite`?

- (A) It's required by the C standard or `fwrite` will fail
- (B) It makes the write faster
- (C) It ensures padding bytes (which are otherwise uninitialized garbage) don't leak arbitrary memory contents into the file
- (D) It converts the struct to network byte order

---

## Section B — Short Answer (2 pts each)

**6.** What is the difference between `stdout` and `stderr`, and why does it matter for error messages?

```
stdout: _____________________________________________________________

stderr: _____________________________________________________________

Why it matters: _____________________________________________________
```

---

**7.** Given this code, what will be printed, and why?

```c
FILE *fp = fopen("nonexistent_file.txt", "r");
printf("%d\n", fp == NULL);
fclose(fp);
```

Printed: ______

What happens at `fclose(fp)`, and why is this a bug? `_______________________________`

---

**8.** Explain the "tombstone" pattern used in fixed-record binary databases. Why not just shift all subsequent records left when deleting one?

```
Tombstone pattern: __________________________________________________

Why not shift: ______________________________________________________
```

---

**9.** In the Unix file model, what three file descriptors are open by default when a program starts, and what do they correspond to?

```
fd 0: _______________________________________________________________
fd 1: _______________________________________________________________
fd 2: _______________________________________________________________
```

---

**10.** Given a fixed-record binary file where each record is `sizeof(Record)` bytes, write the `fseek` call needed to position the file pointer at the start of record index `5` (0-indexed), ready to `fread` it.

```c
FILE *fp = fopen("data.bin", "rb");
/* Your fseek call here: */


fread(&record, sizeof(Record), 1, fp);
```

---

## Answer Key (Instructor Copy)

**1. (C) Truncates the file to zero length** — Mode `"w"` always creates a fresh, empty file if opening succeeds, discarding any prior content. Use `"a"` (append) to preserve existing content while adding new data, or `"r+"` to modify without truncating.

**2. (B)** — `EOF` is typically defined as `-1` (an `int`). If the return of `fgetc` were stored in a `char`, and `char` happens to be unsigned on the platform, then a byte value of `0xFF` (255) read from the file could be indistinguishable from -1 truncated into an unsigned char range, or comparisons could behave incorrectly across implementations. Using `int` avoids this entirely since `EOF` and every possible `unsigned char` value (0-255) are all distinguishable within `int`'s range.

**3. (B)** — Because every record occupies the same number of bytes, the byte offset of record `i` is `i * sizeof(Record)`, computable without reading anything. `fseek` jumps directly there. Text/CSV files have variable-length lines, so finding record `i` requires scanning from the start, counting lines — O(n).

**4. (C)** — Seek to the end (`SEEK_END`, offset 0), then `ftell` reports the current position, which equals the total byte count since we're at the end. `rewind` resets the position back to the start for subsequent reads. This is the standard idiom for determining file size with `FILE *`.

**5.** (C) — Struct padding bytes inserted by the compiler for alignment are never automatically initialized. If you fill in only the named fields and then `fwrite` the whole struct, the padding bytes retain whatever garbage was previously in that memory (potentially leftover stack/heap data from unrelated prior use, which could theoretically include sensitive leftover values). `memset(&s, 0, sizeof(s))` zeroes every byte, including padding, before you fill in the real fields, ensuring deterministic, safe output.

**6.**
- `stdout`: the standard output stream — normally connected to the terminal, used for a program's primary/expected output; buffered.
- `stderr`: the standard error stream — also normally connected to the terminal, used for diagnostic/error messages; unbuffered (or line-buffered) by default.
- Why it matters: they can be redirected independently (`./prog > out.txt 2> err.txt`). Sending errors to `stderr` keeps them separate from a program's actual data output, so error messages don't corrupt piped/redirected data, and users/scripts can filter or capture them separately.

**7.** Printed: `1` (fopen returned NULL because the file doesn't exist, so `fp == NULL` is true, which prints as 1). The bug: `fclose(fp)` is then called on a `NULL` pointer — this is undefined behavior (though many implementations handle it gracefully by doing nothing or returning an error, it is not guaranteed by the standard and should never be relied upon). The correct code must check `if (fp == NULL) { ...handle error, return early... }` before ever calling `fclose`.

**8.** Tombstone pattern: instead of physically removing a deleted record, you mark it with a flag (e.g., `is_deleted = 1`) and leave it in place; readers/scanners skip over tombstoned records. Why not shift: shifting all subsequent records left after a deletion requires rewriting every record after the deleted one — an O(n) operation for a single delete, and it invalidates the O(1) direct-index-to-byte-offset mapping that fixed-record files rely on (record `i`'s position would change). Tombstoning keeps deletion O(1) at the cost of wasted space, which can later be reclaimed via compaction.

**9.**
- fd 0: `stdin` — standard input (normally the keyboard, or whatever is redirected)
- fd 1: `stdout` — standard output (normally the terminal)
- fd 2: `stderr` — standard error (normally the terminal)

**10.**
```c
fseek(fp, 5 * (long)sizeof(Record), SEEK_SET);
```
This moves the file position to byte offset `5 * sizeof(Record)` from the beginning of the file (`SEEK_SET`), which is exactly the start of the 6th record (index 5, 0-indexed).
