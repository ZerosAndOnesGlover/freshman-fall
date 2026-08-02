# PROG 101 Programming I: Structured Programming in C
## Week 8 · Lecture 1: File I/O Basics (`fopen`, `fread`, `fwrite`, and Text Processing)

---

## Lecture Goals

By the end of this lecture you will:
- Understand the `FILE *` abstraction and what it represents
- Open, read, write, and close files correctly, checking every error
- Distinguish text mode from binary mode and know when each matters
- Read files line-by-line, word-by-word, and character-by-character
- Understand buffering and why `fflush` sometimes matters

---

## 1. The File Abstraction

Every file operation in the C standard library revolves around a single type: `FILE *`, defined in `<stdio.h>`. A `FILE *` is an opaque pointer to a structure the library uses internally to track the file's position, buffer, and state. You never access its fields directly — you only pass it to library functions.

```c
#include <stdio.h>

FILE *fp = fopen("data.txt", "r");
if (fp == NULL) {
    perror("fopen");     /* prints a system-specific error message */
    return 1;
}
/* ... use fp ... */
fclose(fp);
```

**The golden rule, identical to `malloc`/`free`:** every `fopen` must have exactly one matching `fclose`.

---

## 2. Opening Files: The Mode String

```c
FILE *fopen(const char *filename, const char *mode);
```

| Mode | Meaning | File must exist? | Truncates? |
|------|---------|-------------------|------------|
| `"r"` | Read | Yes | No |
| `"w"` | Write | No (created if absent) | **Yes** — existing content erased |
| `"a"` | Append | No (created if absent) | No — writes go to the end |
| `"r+"` | Read + write | Yes | No |
| `"w+"` | Read + write | No | **Yes** |
| `"a+"` | Read + append | No | No |

Add `b` for binary mode: `"rb"`, `"wb"`, `"ab"`, `"rb+"`, etc.

```c
FILE *fp = fopen("output.txt", "w");   /* overwrites if it exists! */
FILE *fp = fopen("log.txt", "a");      /* appends — safe for logs */
FILE *fp = fopen("data.bin", "rb");    /* binary read */
```

**Always check the return value.** `fopen` returns `NULL` on failure — file doesn't exist (for `"r"`), permission denied, disk full, path invalid, etc.

```c
FILE *fp = fopen("nonexistent.txt", "r");
if (fp == NULL) {
    fprintf(stderr, "Error opening file: %s\n", strerror(errno));
    return 1;
}
```

`perror("context")` and `strerror(errno)` both translate the OS's `errno` value into a human-readable message — `perror` prints directly, `strerror` returns a string you can format yourself.

---

## 3. Reading Text: Line by Line (the Standard Idiom)

`fgets` is the safe, standard way to read a line of text:

```c
char line[256];
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) { perror("fopen"); return 1; }

while (fgets(line, sizeof(line), fp) != NULL) {
    /* line contains one line INCLUDING the trailing '\n' (if it fit) */
    line[strcspn(line, "\n")] = '\0';   /* strip the newline */
    printf("Read: '%s'\n", line);
}

fclose(fp);
```

`fgets` returns `NULL` at end-of-file or on error — this is what terminates the loop naturally. It never overflows the buffer: it reads at most `size - 1` characters, always null-terminating.

### Reading Formatted Data: `fscanf`

```c
FILE *fp = fopen("scores.txt", "r");
char name[50];
int score;

/* Assume file format: "Alice 92\nBob 85\n..." */
while (fscanf(fp, "%49s %d", name, &score) == 2) {
    printf("%s scored %d\n", name, score);
}
fclose(fp);
```

`fscanf` returns the number of items successfully matched and assigned. **Always check this return value** — a malformed line will cause a mismatch, and continuing to read without checking leads to silently wrong results or infinite loops.

### Reading Character by Character

```c
FILE *fp = fopen("data.txt", "r");
int c;   /* MUST be int, not char — to hold EOF (which is often -1) */

while ((c = fgetc(fp)) != EOF) {
    putchar(c);
}
fclose(fp);
```

**Why `int c`, not `char c`?** `EOF` is typically `-1`, represented as `int`. If `c` were `char` (and `char` is unsigned on your platform, or the byte value happens to equal the pattern of `-1` interpreted as unsigned char, `0xFF` = 255), a valid byte could be misinterpreted as `EOF`, terminating the loop early. This is one of the most common subtle C bugs.

---

## 4. Writing Text

```c
FILE *fp = fopen("output.txt", "w");
if (fp == NULL) { perror("fopen"); return 1; }

fprintf(fp, "Name: %s, Score: %d\n", "Alice", 92);
fputs("A plain line of text\n", fp);
fputc('X', fp);

fclose(fp);
```

`fprintf` works exactly like `printf`, but writes to a `FILE *` instead of stdout. In fact, `printf(...)` is equivalent to `fprintf(stdout, ...)`.

### The Standard Streams

Three `FILE *` streams are always open, without calling `fopen`:

```c
stdin    /* standard input  — normally the keyboard */
stdout   /* standard output — normally the terminal, buffered */
stderr   /* standard error  — normally the terminal, UNbuffered */
```

```c
fprintf(stdout, "Normal output\n");    /* same as printf(...) */
fprintf(stderr, "Error: %s\n", msg);   /* goes to stderr, not stdout */
```

**Why separate stdout and stderr?** They can be redirected independently:
```bash
./program > output.txt              # stdout to file, stderr still shows on screen
./program 2> errors.txt             # stderr to file, stdout still shows
./program > out.txt 2> err.txt      # both redirected separately
./program > all.txt 2>&1            # both redirected to the same file
```

This is why diagnostic/error messages should always go to `stderr`, not `stdout` — it keeps them separable from a program's actual data output.

---

## 5. Text Mode vs Binary Mode

On Unix-like systems (Linux, macOS), text mode and binary mode behave **identically** — a byte is a byte.

On Windows, text mode performs a translation: `\n` (line feed) is translated to `\r\n` (carriage return + line feed) on write, and `\r\n` is translated back to `\n` on read. This is invisible and usually harmless for text files, but **catastrophic** for binary data (images, serialized structs, executables) — the translation would corrupt bytes that happen to match `\r` or `\n` patterns.

**The rule:** always open binary data with `"b"` in the mode string (`"rb"`, `"wb"`), even on Unix where it currently makes no difference — this makes your code portable and correct if it ever runs on Windows.

```c
FILE *fp = fopen("image.bin", "rb");   /* binary — correct for non-text data */
FILE *fp = fopen("notes.txt", "r");    /* text — correct for human-readable text */
```

---

## 6. Buffering: Why `fflush` Sometimes Matters

`FILE *` streams are **buffered** by default: writes accumulate in memory and are only actually sent to the OS (and then to disk/terminal) when the buffer fills, the stream is closed, or you explicitly flush it.

```c
printf("Processing...");   /* may sit in the buffer, not visible yet! */
sleep(5);                  /* 5-second delay — user sees nothing during this */
printf(" done.\n");        /* buffer flushes now (newline often triggers it) */
```

```c
printf("Processing...");
fflush(stdout);            /* force the buffer to be written NOW */
sleep(5);
printf(" done.\n");
```

**When to flush explicitly:**
- Before a long-running operation, so status messages actually appear
- Before reading interactive input (some platforms don't auto-flush stdout before stdin reads)
- When writing to a log file that another process is tailing in real time

`fclose` always flushes automatically — this is one more reason to always close your files.

---

## 7. Checking for Errors and End-of-File

```c
FILE *fp = fopen("data.txt", "r");
if (fp == NULL) { perror("fopen"); return 1; }

int c;
while ((c = fgetc(fp)) != EOF) {
    /* process c */
}

if (ferror(fp)) {
    fprintf(stderr, "Error reading file\n");
} else if (feof(fp)) {
    printf("Reached end of file normally\n");
}

fclose(fp);
```

`feof(fp)` returns true once the end-of-file has been reached (only reliable **after** a read has failed due to EOF — don't use it to control your loop; use the return value of the read function itself for that).
`ferror(fp)` returns true if a read/write error occurred (distinct from simply reaching the end).

---

## 8. A Complete Example: Word Frequency Counter

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <errno.h>

#define MAX_WORDS 1000
#define MAX_WORD_LEN 50

typedef struct {
    char word[MAX_WORD_LEN];
    int  count;
} WordCount;

int find_or_add(WordCount table[], int *n, const char *word) {
    for (int i = 0; i < *n; i++) {
        if (strcmp(table[i].word, word) == 0) return i;
    }
    strncpy(table[*n].word, word, MAX_WORD_LEN - 1);
    table[*n].word[MAX_WORD_LEN - 1] = '\0';
    table[*n].count = 0;
    return (*n)++;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL) {
        fprintf(stderr, "Error: cannot open '%s': %s\n", argv[1], strerror(errno));
        return 1;
    }

    WordCount table[MAX_WORDS];
    int n = 0;
    char word[MAX_WORD_LEN];
    int len = 0;
    int c;

    while ((c = fgetc(fp)) != EOF) {
        if (isalpha(c)) {
            if (len < MAX_WORD_LEN - 1) {
                word[len++] = (char)tolower(c);
            }
        } else if (len > 0) {
            word[len] = '\0';
            int idx = find_or_add(table, &n, word);
            table[idx].count++;
            len = 0;
        }
    }
    if (len > 0) {   /* handle a word at end-of-file with no trailing punctuation */
        word[len] = '\0';
        int idx = find_or_add(table, &n, word);
        table[idx].count++;
    }

    fclose(fp);

    for (int i = 0; i < n; i++) {
        printf("%-20s %d\n", table[i].word, table[i].count);
    }

    return 0;
}
```

This program demonstrates the complete pattern: argument validation, error-checked file opening, character-by-character processing, and clean resource release.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** This line-counting loop is wrong. Run it against three files and explain why the error is *data-dependent*.

```c
while (!feof(f)) {
    fgets(buf, sizeof buf, f);
    count++;
}
```

**2. (Explain.)** Explain each mode string, and what happens to an existing file in each case: `"r"`, `"w"`, `"a"`, `"r+"`, `"w+"`, `"a+"`.

**3. (Build.)** Write a program that counts the lines, words, and characters in a file named on the command line — a minimal `wc`. Handle a missing argument and an unopenable file.

**4. (Stretch.)** Explain why output sometimes does not appear when a program crashes, and give three ways to force it out. Explain the difference between the buffering of `stdout` and `stderr`.


### Answers

**1.** | File | `feof` loop | Correct |
|---|---|---|
| 3 lines, trailing newline | **4** | 3 |
| 3 lines, no trailing newline | **3** | 3 |
| empty file | **1** | 0 |

`feof` reports whether a **previous read already hit end-of-file** — it is not a lookahead. With a trailing newline, the third `fgets` consumes the last line and stops exactly at the end *without* attempting a read past it, so EOF is not yet set. The loop runs a fourth time, `fgets` fails and leaves `buf` untouched, and `count` is incremented anyway.

With **no** trailing newline, the third `fgets` reads to the end and sets EOF in the same call, so the loop happens to stop correctly. That is why the bug is data-dependent and survives casual testing — the same code is right or wrong depending on whether the file ends in `\n`.

The empty file gives the clearest signal: one iteration, one phantom line, and `buf` holds stale garbage.

**The correct idiom tests the read itself:**

```c
while (fgets(buf, sizeof buf, f)) count++;
```

`fgets` returns `NULL` on both EOF and error, so if you must distinguish them, call `feof(f)` or `ferror(f)` **after** the loop — which is what `feof` is actually for. The same rule applies to `fscanf`, `fread`, and `getchar`: **check the return value of the read, never a separate EOF flag.**

**2.** | Mode | If the file exists | If it does not | Read | Write | Position |
|---|---|---|---|---|---|
| `"r"` | opened | **fails**, returns `NULL` | ✓ | ✗ | start |
| `"w"` | **truncated to zero** | created | ✗ | ✓ | start |
| `"a"` | opened | created | ✗ | ✓ | **always end** |
| `"r+"` | opened | **fails** | ✓ | ✓ | start |
| `"w+"` | **truncated to zero** | created | ✓ | ✓ | start |
| `"a+"` | opened | created | ✓ | ✓ | reads anywhere, writes **always at end** |

The one to be careful with is **`"w"`: it destroys the file's contents immediately on open**, before you write a single byte. Opening a file for writing to "check something" has already deleted it. If you need to avoid clobbering, open with `"r"` first and check for `NULL`, or use C11's `"wx"`, which fails if the file exists.

**`"a"` forces every write to the end**, regardless of any `fseek` — the seek affects reads only. That makes it the right mode for log files, and it is atomic enough that concurrent appends from multiple processes do not interleave within a single small write.

Add `"b"` (`"rb"`, `"wb"`) for binary. On Linux it changes nothing; on Windows, text mode translates `\n` to `\r\n` on write and back on read, which silently corrupts binary data. **Always use `"b"` for non-text**, so the code is portable even if your machine does not need it.

**3.**

```c
#include <stdio.h>
#include <ctype.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s FILE\n", argv[0]);
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (!f) {
        perror(argv[1]);
        return 1;
    }

    long lines = 0, words = 0, chars = 0;
    int c, in_word = 0;

    while ((c = fgetc(f)) != EOF) {
        chars++;
        if (c == '\n') lines++;
        if (isspace(c)) in_word = 0;
        else if (!in_word) { in_word = 1; words++; }
    }

    if (ferror(f)) { perror(argv[1]); fclose(f); return 1; }
    fclose(f);

    printf("%ld %ld %ld %s\n", lines, words, chars, argv[1]);
    return 0;
}
```

**`c` must be `int`, not `char`.** `fgetc` returns a value in 0–255 *or* `EOF`, which is −1 — 257 distinct values that do not fit in a `char`. With `char c`, byte 0xFF would compare equal to `EOF` on a signed-char platform and truncate the file early. This is the single most common `fgetc` bug.

`perror` prints your message plus the system's description of `errno` — *No such file or directory*, *Permission denied* — which is far more useful than a generic failure line.

The word counter is a two-state machine: a word begins at each transition from whitespace to non-whitespace. Checking `ferror` after the loop distinguishes a genuine read error from a normal EOF, since both end the loop identically.

**4.** `stdout` is **buffered**: `printf` writes into a buffer in your process, and the data only reaches the OS when the buffer fills, when the stream is flushed, or at normal exit via `fclose`/`exit`. A crash — SIGSEGV, `abort`, or a kill — bypasses that cleanup, so **buffered output is lost**. The result is deeply misleading during debugging: the last line you see is not the last line that ran, and it looks like the crash happened earlier than it did.

The buffering mode depends on the destination. To a **terminal**, `stdout` is *line*-buffered — flushed at each `\n`. Redirected to a **file or pipe**, it becomes *fully* buffered, typically 4 KB. This is why `./prog` shows output but `./prog | grep x` seems to hang: same code, different buffering.

**`stderr` is unbuffered** by definition, precisely so that diagnostics appear immediately and in order even when the program is about to die. That alone is a strong reason to send error messages there.

Three ways to force output:

1. **`fflush(stdout);`** after the writes you need to see — targeted and explicit.
2. **`setvbuf(stdout, NULL, _IONBF, 0);`** at the top of `main`, making `stdout` unbuffered for the whole run. Slow, but ideal while hunting a crash.
3. **Print diagnostics to `stderr`** with `fprintf(stderr, ...)`, which needs no flushing at all.

A fourth, better option: use a debugger. Buffered output vanishing is a symptom that `printf`-debugging has reached its limit.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **`FILE *`** | Opaque pointer representing an open file stream |
| **`fopen`/`fclose`** | Open/close a file stream — must be paired |
| **Mode string** | `"r"`, `"w"`, `"a"`, etc. — controls read/write/append behavior |
| **`fgets`** | Safe line-reading function — bounds-checked |
| **`fscanf`/`fprintf`** | Formatted read/write to a stream |
| **`stdin`/`stdout`/`stderr`** | The three always-open standard streams |
| **Buffering** | Accumulating output in memory before an actual write to the OS |
| **`fflush`** | Force buffered output to be written immediately |
| **Text mode vs binary mode** | Whether newline translation occurs (matters on Windows) |
| **`EOF`** | Sentinel value (`int`, typically -1) signaling end-of-file or read error |

---

## Reading

- **K&R Chapter 7** — Input and Output (§7.1–7.5)
- **King Ch. 22** — Input/Output
- **man pages:** `man 3 fopen`, `man 3 fgets`, `man 3 fscanf`

---

*Next: Lecture 2 — The UNIX File Model: File Descriptors and Low-Level I/O*
