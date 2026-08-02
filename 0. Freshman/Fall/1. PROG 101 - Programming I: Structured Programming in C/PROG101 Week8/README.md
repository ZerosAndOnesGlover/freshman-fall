# PROG 101 · Week 8: File I/O and the UNIX File Model
## Persisting Data · Text and Binary Files · Building a Real Database

---

## Week Overview

Week 8 takes everything you've built — structs, arrays, linked lists — and gives it a place to live beyond a single program run: **the file system**. You will learn the `FILE *` abstraction for portable text and binary I/O, the lower-level Unix file descriptor model that underlies it, and how to build a genuine fixed-record binary database with O(1) indexed access, tombstone deletion, and compaction — the same fundamental techniques real database engines use.

---

## Schedule

| Day | Event | Topic | Duration |
|-----|-------|-------|----------|
| Tuesday | Lecture 1 | File I/O Basics: fopen, fread, fwrite | 50 min |
| Wednesday | Lecture 2 | The UNIX File Model: File Descriptors | 50 min |
| Thursday | Lecture 3 | Binary Files and Struct Serialization | 50 min |
| Monday | **Lab 8** | Persistent Student Record Database | 2 hours |

---

## Files in This Package

```
PROG101_Week5/
├── README.md
├── lectures/
│   ├── Lecture 01 File IO Basics.md              ← FILE*, fopen modes, fgets/fscanf, stdin/stdout/stderr, buffering
│   ├── Lecture 02 Unix File Model.md              ← File descriptors, open/read/write/close, fseek, redirection, pipes
│   └── Lecture 03 Binary Files Serialization.md   ← fread/fwrite, padding/endianness hazards, fixed-record databases, tombstones
├── lab/
│   └── LAB 8 File IO Studentdb.md                  ← CSV import + binary basics + complete persistent student database
├── assignments/
│   └── Problem Set 8.md                           ← 5 problems: text utilities, config parser, log analyzer, binary inventory, key-value store
├── quizzes/
│   └── QUIZ 5.md                                  ← 10 questions + full answer key
└── resources/
    └── Week 8 File IO Reference.md                 ← Mode cheat sheet, idiom library, error checklist, common bugs, text-vs-binary guide
```

---

## Learning Objectives

After Week 8, you will be able to:

- [ ] Open, read, write, and close files correctly with `FILE *`, checking every error
- [ ] Choose the correct `fopen` mode for a given task
- [ ] Read text files line-by-line (`fgets`), word-by-word (`fscanf`), and byte-by-byte (`fgetc`)
- [ ] Explain why `fgetc`'s result must be stored in an `int`, not a `char`
- [ ] Distinguish `stdout` from `stderr` and know when to use each
- [ ] Explain the "everything is a file" Unix philosophy and what a file descriptor is
- [ ] Use `open`/`read`/`write`/`close` and know when to prefer them over `FILE *`
- [ ] Use `fseek`/`ftell`/`rewind` for random access and determining file size
- [ ] Explain how shell redirection and pipes work at the file descriptor level
- [ ] Serialize structs to binary files correctly, including zeroing padding bytes
- [ ] Build a fixed-record binary file with O(1) indexed access
- [ ] Implement tombstone deletion and file compaction
- [ ] Choose between text and binary serialization for a given engineering scenario

---

## Textbook Reading

| Lecture | K&R | King | Other |
|---------|-----|------|-------|
| L1: File I/O Basics | Ch. 7 §7.1–7.5 | Ch. 22 | — |
| L2: Unix File Model | — | — | CS:APP §10.1–10.6 |
| L3: Binary Serialization | §7.5 | Ch. 22 (binary sections) | — |

---

## The Key Insights of This Week

### On `FILE *` vs File Descriptors
`FILE *` is a convenient, buffered, portable layer built entirely on top of the raw integer file descriptors the OS actually provides. Understanding both levels — knowing that `fprintf(stdout, ...)` ultimately becomes a `write(1, ...)` system call — is what separates "I can call `printf`" from "I understand what a program actually does when it talks to the outside world."

### On Buffering
Output is not immediately visible just because you called `printf`. It sits in a buffer until the buffer fills, the program exits, or you explicitly `fflush`. This single fact explains a huge class of confusing bugs: "why didn't my status message print before the crash?" — because it was still in the buffer when the crash happened.

### On Binary Serialization
Writing a struct's raw bytes to disk is fast and simple, but it inherits every hazard from Week 7's struct layout discussion: uninitialized padding leaks garbage, and the layout itself isn't guaranteed portable across compilers or architectures. Fixed-record binary files trade portability for the genuinely powerful property of O(1) indexed access — the same trade every real embedded database makes.

---

## Common Week 8 Mistakes

**Forgetting mode `"w"` truncates:**
```c
FILE *fp = fopen("important.txt", "w");   /* ERASES existing content immediately */
```

**Not checking `fopen` for NULL:**
```c
FILE *fp = fopen("maybe_missing.txt", "r");
fgets(buf, sizeof(buf), fp);   /* CRASH if fopen failed */
```

**Using `char` instead of `int` for `fgetc`'s result:**
```c
char c;   /* WRONG on some platforms */
while ((c = fgetc(fp)) != EOF) { ... }
```

**Writing a struct without zeroing padding first:**
```c
struct S { char a; int b; } s;
s.a = 'X'; s.b = 42;
fwrite(&s, sizeof(s), 1, fp);   /* padding bytes are uninitialized garbage */
```

**Not checking `fread`/`fwrite` return values:**
```c
fread(&record, sizeof(record), 1, fp);   /* did this actually succeed? */
```

**Off-by-one / overflow in fseek offset arithmetic:**
```c
fseek(fp, index * RECORD_SIZE, SEEK_SET);        /* int overflow for large files */
fseek(fp, (long)index * RECORD_SIZE, SEEK_SET);  /* correct */
```

---

## Challenge Problems (Optional)

1. **Implement `wc` fully** — replicate the real Unix `wc` command including `-l`, `-w`, `-c`, `-m` flags, reading from stdin if no filename is given (so it works with pipes: `cat file | ./wc -l`).

2. **A simple B-tree-lite index** — extend the Week 8 binary database with a separate in-memory sorted array of `{id, index}` pairs, rebuilt on load, enabling O(log n) lookup by id via binary search instead of the linear scan `sdb_find_by_id` currently uses.

3. **Crash-safe writes** — modify the student database so that `sdb_update_gpa` writes to a temporary shadow location first, then atomically renames it into place (or uses a write-ahead log pattern), ensuring a crash mid-write never corrupts a record. This is a simplified taste of the ARIES recovery algorithm covered in Year 3's Database Systems course.

4. **A tiny `tar`-like archiver** — write a program that packs multiple files into one archive file (storing each file's name, size, and content sequentially) and a second program that unpacks the archive back into individual files.
