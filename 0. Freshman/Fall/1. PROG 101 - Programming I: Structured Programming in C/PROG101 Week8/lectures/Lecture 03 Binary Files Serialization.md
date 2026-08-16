# PROG 101 · Programming I: Structured Programming in C
## Week 8 · Lecture 3: Binary Files and Struct Serialization

**Date:** Thursday 15 October 2026 · 10:00–10:50 · Week 8

---

## Lecture Goals

By the end of this lecture you will:
- Use `fread`/`fwrite` to persist raw binary data, including whole structs
- Understand the portability hazards of binary serialization (padding, endianness)
- Build a simple binary record file with fixed-size records and random access
- Implement append, update, and delete operations on a binary record store
- Know when to use binary format vs text format (CSV, JSON-like)

---

## 1. `fread` and `fwrite` — Raw Binary Transfer

```c
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);
size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream);
```

Both functions transfer `nmemb` elements of `size` bytes each — a total of `size * nmemb` bytes — between memory and the file, copying raw bytes with **no interpretation whatsoever**.

```c
int numbers[10] = {1,2,3,4,5,6,7,8,9,10};

FILE *fp = fopen("numbers.bin", "wb");
fwrite(numbers, sizeof(int), 10, fp);   /* writes 40 raw bytes */
fclose(fp);

int loaded[10];
fp = fopen("numbers.bin", "rb");
size_t count = fread(loaded, sizeof(int), 10, fp);
/* count = number of COMPLETE elements read (may be less if file was shorter) */
fclose(fp);
```

**Always check the return value.** `fread` returns fewer than `nmemb` if the file was shorter than expected or an error occurred — silently proceeding with uninitialized/partial data is a common source of bugs.

---

## 2. Writing an Entire Struct

```c
typedef struct {
    int    id;
    char   name[50];
    double gpa;
} StudentRecord;

StudentRecord s = {1001, "Alice", 3.8};

FILE *fp = fopen("student.bin", "wb");
fwrite(&s, sizeof(StudentRecord), 1, fp);   /* write ONE struct */
fclose(fp);

StudentRecord loaded;
fp = fopen("student.bin", "rb");
fread(&loaded, sizeof(StudentRecord), 1, fp);
fclose(fp);

printf("%d %s %.2f\n", loaded.id, loaded.name, loaded.gpa);
```

Because `fwrite` copies exactly `sizeof(StudentRecord)` bytes — including any padding bytes the compiler inserted (Week 7) — the entire in-memory representation, byte for byte, is written to disk.

---

## 3. The Portability Hazards of Binary Serialization

Binary serialization is fast and simple but has three real hazards you must understand:

### Hazard 1: Padding Bytes Are Undefined

```c
struct Record {
    char a;    /* offset 0 */
    int  b;    /* offset 4 (3 padding bytes at offset 1-3) */
};
```

The 3 padding bytes are **never initialized** by the compiler — they contain whatever garbage was on the stack/heap at allocation time. When you `fwrite` this struct, those garbage bytes are written to disk too. This is harmless for simple use (you'll never read them meaningfully), but:
- It can leak sensitive data (uninitialized stack/heap contents) into files
- Valgrind will flag `fwrite`ing an uninitialized struct as "uninitialised value used"

**Fix:** zero the struct before filling it in.
```c
struct Record r;
memset(&r, 0, sizeof(r));   /* zero EVERYTHING including padding */
r.a = 'X';
r.b = 42;
fwrite(&r, sizeof(r), 1, fp);
```

### Hazard 2: Struct Layout Differs Across Compilers/Platforms

If you compile the same struct definition with different compilers, different optimization flags, or on different architectures, the padding and even field ordering **may differ**. A binary file written by one build may not read correctly on another.

**This matters for this course when:** you write a binary file with one program and read it with another — always compile both with the same flags/compiler for binary compatibility (fine for this course's assignments, which run on one system).

**In production systems**, this hazard is solved with explicit serialization formats (Protocol Buffers, a hand-written byte-level format with `#pragma pack` or manual field-by-field writes) rather than raw struct dumps — beyond this course's scope but important to know exists.

### Hazard 3: Endianness

Multi-byte values (`int`, `long`, `double`) are stored in a specific byte order (endianness — Week 1). If you write a binary file on a little-endian machine (x86, the near-universal case today) and read it on a big-endian machine, multi-byte values will be scrambled.

**For this course:** you can assume a consistent little-endian x86-64 environment. Just know that this hazard exists — it is why network protocols (Week-later courses) define **network byte order** (big-endian) explicitly, with conversion functions (`htonl`, `ntohl`) at the boundary.

---

## 4. Building a Fixed-Record Binary Database

The killer feature of fixed-size binary records: **O(1) random access to any record by index**, without reading the whole file.

```c
#define RECORD_SIZE sizeof(StudentRecord)

/* Read record number 'index' (0-based) directly, without scanning */
int read_record(FILE *fp, int index, StudentRecord *out) {
    if (fseek(fp, index * (long)RECORD_SIZE, SEEK_SET) != 0) {
        return -1;
    }
    size_t n = fread(out, RECORD_SIZE, 1, fp);
    return (n == 1) ? 0 : -1;
}

/* Overwrite record number 'index' in place */
int write_record(FILE *fp, int index, const StudentRecord *rec) {
    if (fseek(fp, index * (long)RECORD_SIZE, SEEK_SET) != 0) {
        return -1;
    }
    size_t n = fwrite(rec, RECORD_SIZE, 1, fp);
    fflush(fp);
    return (n == 1) ? 0 : -1;
}

/* Append a new record at the end */
int append_record(FILE *fp, const StudentRecord *rec) {
    if (fseek(fp, 0, SEEK_END) != 0) return -1;
    size_t n = fwrite(rec, RECORD_SIZE, 1, fp);
    fflush(fp);
    return (n == 1) ? 0 : -1;
}

/* Count total records in the file */
long count_records(FILE *fp) {
    fseek(fp, 0, SEEK_END);
    long size = ftell(fp);
    return size / (long)RECORD_SIZE;
}
```

This is precisely the technique real database engines use at a much larger scale (Week 3 Year 3 of the CSE curriculum covers B+ trees built on exactly this foundation): fixed-size (or page-aligned) records enable direct-offset access, avoiding a full linear scan.

### "Deleting" a Record — the Tombstone Pattern

Deleting a record from the middle of a fixed-record file is expensive if you try to shift every subsequent record. The standard technique: mark it as deleted (a **tombstone**) instead of physically removing it.

```c
typedef struct {
    int    id;
    char   name[50];
    double gpa;
    int    is_deleted;   /* 0 = active, 1 = tombstoned */
} StudentRecord;

int delete_record(FILE *fp, int index) {
    StudentRecord rec;
    if (read_record(fp, index, &rec) != 0) return -1;
    rec.is_deleted = 1;
    return write_record(fp, index, &rec);
}

/* When scanning, skip tombstoned records */
void print_all_active(FILE *fp) {
    long total = count_records(fp);
    StudentRecord rec;
    for (long i = 0; i < total; i++) {
        read_record(fp, (int)i, &rec);
        if (!rec.is_deleted) {
            printf("%d %s %.2f\n", rec.id, rec.name, rec.gpa);
        }
    }
}
```

---

## 5. Text-Based Serialization: CSV

For human-readable, portable, cross-platform-safe persistence, text formats like CSV avoid all three binary hazards at the cost of speed and larger file size.

```c
/* Write a student to a CSV line */
void write_csv_line(FILE *fp, const StudentRecord *s) {
    fprintf(fp, "%d,%s,%.2f\n", s->id, s->name, s->gpa);
}

/* Read one student from a CSV line */
int read_csv_line(FILE *fp, StudentRecord *s) {
    char line[256];
    if (fgets(line, sizeof(line), fp) == NULL) return -1;   /* EOF */

    char *token = strtok(line, ",");
    if (token == NULL) return -1;
    s->id = atoi(token);

    token = strtok(NULL, ",");
    if (token == NULL) return -1;
    strncpy(s->name, token, sizeof(s->name) - 1);
    s->name[sizeof(s->name) - 1] = '\0';

    token = strtok(NULL, ",\n");
    if (token == NULL) return -1;
    s->gpa = atof(token);

    return 0;
}
```

**CSV hazards to be aware of** (beyond this course's assignments, but good to know): fields containing commas, quotes, or newlines require escaping — real CSV parsers handle quoted fields (`"Smith, John"`) — the naive `strtok`-based approach above breaks on such input. For this course's controlled data, the simple approach is fine.

### When to Use Binary vs Text

| Factor | Binary | Text (CSV/etc.) |
|--------|--------|-------------------|
| Speed | Fast (no parsing) | Slower (parse every field) |
| File size | Compact | Larger (numbers as ASCII digits) |
| Human-readable | No | Yes |
| Portable across platforms/compilers | Fragile | Robust |
| Random access by record index | O(1) with fixed records | O(n) — must scan |
| Debuggable with a text editor | No | Yes |

**Engineering judgment:** use binary for performance-critical or large-scale internal storage; use text for configuration, logs, interchange between different programs/languages, or anything a human needs to inspect or edit directly.

---

## 6. A Complete Worked Example: Append-Only Log with Binary Records

```c
#include <stdio.h>
#include <string.h>
#include <time.h>

typedef struct {
    time_t timestamp;
    int    severity;      /* 0=INFO, 1=WARNING, 2=ERROR */
    char   message[200];
} LogEntry;

void log_write(FILE *fp, int severity, const char *message) {
    LogEntry entry;
    memset(&entry, 0, sizeof(entry));   /* zero padding too */
    entry.timestamp = time(NULL);
    entry.severity  = severity;
    strncpy(entry.message, message, sizeof(entry.message) - 1);

    fseek(fp, 0, SEEK_END);
    fwrite(&entry, sizeof(entry), 1, fp);
    fflush(fp);
}

void log_print_all(FILE *fp) {
    LogEntry entry;
    const char *severity_names[] = {"INFO", "WARNING", "ERROR"};

    rewind(fp);
    while (fread(&entry, sizeof(entry), 1, fp) == 1) {
        char timebuf[64];
        strftime(timebuf, sizeof(timebuf), "%Y-%m-%d %H:%M:%S",
                 localtime(&entry.timestamp));
        printf("[%s] %-7s %s\n", timebuf,
               severity_names[entry.severity], entry.message);
    }
}

int main(void) {
    FILE *fp = fopen("app.log", "ab+");
    if (fp == NULL) { perror("fopen"); return 1; }

    log_write(fp, 0, "Application started");
    log_write(fp, 1, "Configuration file not found, using defaults");
    log_write(fp, 2, "Failed to connect to database");

    log_print_all(fp);

    fclose(fp);
    return 0;
}
```

This example ties together random access (`fseek` to end), binary struct persistence, memory zeroing to avoid uninitialized-padding issues, and a realistic append-only log pattern used throughout systems programming (exactly the write-ahead logging concept that reappears in Year 3's Database Systems course).

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict `sizeof(struct Rec)` and the on-disk size after `fwrite`. Explain the gap.

```c
struct Rec { int id; double score; char name[8]; };
struct Rec r = { 42, 3.5, "abc" };
FILE *f = fopen("db.bin", "wb");
fwrite(&r, sizeof r, 1, f);
fclose(f);
```

**2. (Explain.)** List the four things that make a raw `fwrite` of a struct non-portable, and give the standard fix for each.

**3. (Build.)** Write `read_record(FILE *f, int n, struct Rec *out)` for a fixed-record binary file, returning 1 on success and 0 on failure. Explain how random access works.

**4. (Stretch.)** Compare binary and CSV serialisation for a table of a million records, on five dimensions. Say which you would choose for a program's own save file and which for exported data.


### Answers

**1.** `sizeof(struct Rec)` is **24**, and the file is **24 bytes**.

The members total 4 + 8 + 8 = 20, so 4 bytes are **padding**: `double` requires 8-byte alignment, so `score` cannot start at offset 4 and is placed at offset 8, leaving bytes 4–7 unused. `name` follows at 16, and 24 is already a multiple of 8, so no tail padding is needed.

The important consequence is that **`fwrite` writes the padding too** — including its contents, which are whatever happened to be in that memory. Those bytes are **indeterminate**: they may be leftover stack data. Writing a struct to a file or a socket can therefore leak information that was never part of the record, and it makes byte-for-byte comparison of two "equal" records unreliable. Zero the struct with `memset` or `= {0}` before filling it if either matters.

`fwrite` returns the number of **items** written, not bytes — so check `== 1`, not `== sizeof r`. The same for `fread`, where a short read returns a smaller item count.

Also note `"abc"` fills `name[0..2]` plus a terminator, and the remaining 4 bytes are zeroed only because the initialiser list zero-fills the rest of the array — a rule specific to initialisation, not to assignment.

**2.** **1. Padding and alignment.** Different compilers and architectures insert different padding, so the record length itself changes. *Fix:* serialise **field by field**, never the whole struct.

**2. Endianness.** x86 and ARM are little-endian; network protocols and some architectures are big-endian, so the same 4 bytes read as a different integer. *Fix:* pick one byte order and convert — `htonl`/`ntohl` for a defined network order, or explicit shifts and masks.

**3. Type sizes.** `long` is 8 bytes on 64-bit Linux and 4 on 64-bit Windows; `int` has been 16 and 64 bits on real systems. *Fix:* use the fixed-width types from `<stdint.h>` — `int32_t`, `uint64_t` — in anything written to a file or a wire.

**4. Floating-point representation.** IEEE 754 is near-universal today but not required by C, and `long double` genuinely varies (80-bit on x86, 128-bit on ARM). *Fix:* write floats as a fixed-width integer bit pattern, or as text.

Two habits cover most of this: **fixed-width types with explicit byte order**, or **a text format** (CSV, JSON) when the volume permits, since text sidesteps all four at the cost of size and parse time.

For a real format, add a **magic number and a version field** at the head of the file, so a future reader can reject a file it does not understand rather than misinterpret it. `struct`-dumping is fine for a cache or scratch file your own program rewrites, and wrong for anything that outlives the binary that wrote it.

**3.**

```c
int read_record(FILE *f, int n, struct Rec *out) {
    if (n < 0) return 0;
    if (fseek(f, (long)n * (long)sizeof *out, SEEK_SET) != 0) return 0;
    return fread(out, sizeof *out, 1, f) == 1;
}

int write_record(FILE *f, int n, const struct Rec *in) {
    if (n < 0) return 0;
    if (fseek(f, (long)n * (long)sizeof *in, SEEK_SET) != 0) return 0;
    return fwrite(in, sizeof *in, 1, f) == 1;
}
```

Random access works because **every record occupies exactly the same number of bytes**, so record `n` begins at offset `n * sizeof(struct Rec)` — a multiplication, with no scanning. Reading record 50,000 costs one seek and one read regardless of file size: **O(1)**, the same reasoning that makes array indexing O(1).

This is the whole reason fixed-width records exist, and the reason variable-length text formats cannot do it — finding line 50,000 of a CSV requires reading 49,999 lines, or building a separate index of offsets.

Checking `fread(...) == 1` distinguishes success from both EOF and error; a short read returns 0 items and leaves `out` partially written, which is why the caller must not use it on failure. The `long` casts matter: `n * sizeof *out` on a 32-bit `int` `n` overflows past ~89 million records, and `fseek` takes a `long` offset — `fseeko` with `off_t` is the portable route past 2 GB.

**4.** | | Binary (fixed record) | CSV / text |
|---|---|---|
| **Size** | Compact and predictable; 24 B/record here | Larger — digits cost more than the number, plus delimiters |
| **Write/read speed** | Very fast — a `memcpy` | Slower — formatting and parsing every field |
| **Random access** | **O(1)** by offset | O(n) — must scan for line boundaries |
| **Portability** | Poor — padding, endianness, type sizes | **Excellent** — any language, any machine |
| **Human inspection / repair** | Needs a hex editor or a custom tool | **Trivial** — any text editor, `grep`, `awk` |

**For a program's own save file: binary**, provided it is versioned. The program controls both writer and reader, the speed and random access are real wins, and nobody needs to read it by hand.

**For exported data: CSV**, without hesitation. Export exists so that *other* software can consume it, and every one of binary's advantages is irrelevant while its portability problem becomes the whole story.

Two qualifications. CSV is deceptively hard to get right — quoting, embedded commas and newlines, encodings, and a locale that writes decimals with a comma have all caused real data loss. Use a library rather than `strtok`. And the middle ground is often best in practice: a self-describing binary format like Protocol Buffers, SQLite, or Parquet, which keeps the speed and adds schema evolution. The choice is really "who reads this, and do I control them?"



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Serialization** | Converting in-memory data into a storable/transmittable byte sequence |
| **`fread`/`fwrite`** | Raw binary transfer of bytes between memory and a file stream |
| **Fixed-record file** | A binary file where every record occupies the same number of bytes, enabling O(1) indexed access |
| **Tombstone** | A flag marking a record as logically deleted without physically removing it |
| **Endianness hazard** | Multi-byte values may be stored in different byte orders on different systems |
| **CSV** | Comma-Separated Values — a simple human-readable text serialization format |

---

## Reading

- **K&R §7.5** — File Access (binary file examples)
- **King Ch. 22** — Input/Output (binary I/O sections)
- **CS:APP §10.1** — Unix I/O (for the deeper systems view)

---

*Next: Lab 8 — Building a Persistent Student Record Database*
