# PROG 101 — Week 8 Resources
## File I/O Quick Reference · Binary Record Patterns · Common Bugs

---

## Part 1: File Mode Cheat Sheet

| Mode | Read | Write | Creates if missing | Truncates existing | Position starts at |
|------|------|-------|---------------------|---------------------|---------------------|
| `"r"` | Yes | No | No | No | Start |
| `"w"` | No | Yes | Yes | **Yes** | Start |
| `"a"` | No | Yes | Yes | No | End (always writes at end) |
| `"r+"` | Yes | Yes | No | No | Start |
| `"w+"` | Yes | Yes | Yes | **Yes** | Start |
| `"a+"` | Yes | Yes | Yes | No | Start (reads), End (writes) |

Add `"b"` for binary: `"rb"`, `"wb"`, `"ab"`, `"rb+"`, `"wb+"`, `"ab+"`.

---

## Part 2: Core Function Reference

### Opening / Closing

```c
FILE *fopen(const char *path, const char *mode);   /* NULL on failure */
int   fclose(FILE *fp);                             /* 0 on success */
int   fflush(FILE *fp);                              /* force buffered writes out */
```

### Text Reading

```c
char *fgets(char *buf, int size, FILE *fp);
/* Reads at most size-1 chars, stops at newline (kept) or EOF.
 * Always null-terminates. Returns NULL at EOF/error. */

int   fscanf(FILE *fp, const char *format, ...);
/* Returns number of items successfully matched. ALWAYS check this. */

int   fgetc(FILE *fp);
/* Returns next byte as int, or EOF. MUST store in an int variable. */
```

### Text Writing

```c
int fprintf(FILE *fp, const char *format, ...);
int fputs(const char *s, FILE *fp);      /* does NOT add a newline */
int fputc(int c, FILE *fp);
```

### Binary I/O

```c
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *fp);
size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *fp);
/* Both return the number of COMPLETE elements transferred.
 * Check against nmemb to detect short reads/writes. */
```

### Positioning

```c
int  fseek(FILE *fp, long offset, int whence);
/* whence: SEEK_SET (from start), SEEK_CUR (from current), SEEK_END (from end) */

long ftell(FILE *fp);      /* current position, or -1 on error */
void rewind(FILE *fp);     /* == fseek(fp, 0, SEEK_SET), also clears error flags */
```

### Status Checking

```c
int feof(FILE *fp);        /* true if EOF was reached (check AFTER a failed read) */
int ferror(FILE *fp);      /* true if an error occurred */
void clearerr(FILE *fp);   /* reset error/EOF flags */
```

---

## Part 3: The Standard Idioms

### Safe Line Reading

```c
char line[256];
FILE *fp = fopen("file.txt", "r");
if (fp == NULL) { perror("fopen"); return 1; }

while (fgets(line, sizeof(line), fp) != NULL) {
    line[strcspn(line, "\n")] = '\0';   /* strip trailing newline */
    /* process line */
}
fclose(fp);
```

### Safe Character Reading

```c
int c;
while ((c = fgetc(fp)) != EOF) {
    /* process c — remember it's an int, cast to char if storing */
}
```

### Determine File Size

```c
fseek(fp, 0, SEEK_END);
long size = ftell(fp);
rewind(fp);
```

### Read Entire File Into Memory

```c
fseek(fp, 0, SEEK_END);
long size = ftell(fp);
rewind(fp);

char *buffer = malloc(size + 1);
if (buffer == NULL) { /* handle error */ }

size_t read = fread(buffer, 1, size, fp);
buffer[read] = '\0';   /* null-terminate if treating as a string */

/* ... use buffer ... */
free(buffer);
```

### Fixed-Record Binary Access

```c
#define RECORD_SIZE sizeof(MyStruct)

/* Read record i */
fseek(fp, (long)i * RECORD_SIZE, SEEK_SET);
fread(&record, RECORD_SIZE, 1, fp);

/* Write/update record i */
fseek(fp, (long)i * RECORD_SIZE, SEEK_SET);
fwrite(&record, RECORD_SIZE, 1, fp);
fflush(fp);

/* Append a new record */
fseek(fp, 0, SEEK_END);
fwrite(&record, RECORD_SIZE, 1, fp);

/* Count records */
fseek(fp, 0, SEEK_END);
long count = ftell(fp) / RECORD_SIZE;
```

### Zero Before Writing (Avoid Padding Garbage)

```c
MyStruct s;
memset(&s, 0, sizeof(s));   /* ALWAYS do this before filling fields */
s.field1 = value1;
s.field2 = value2;
fwrite(&s, sizeof(s), 1, fp);
```

### Copy a File

```c
char buf[4096];
size_t n;
while ((n = fread(buf, 1, sizeof(buf), src)) > 0) {
    fwrite(buf, 1, n, dst);
}
```

---

## Part 4: File I/O Error Handling Checklist

```
Before using any FILE *:
  [ ] Check fopen() return value against NULL

After every fread/fwrite:
  [ ] Check the return value against the expected nmemb

After every fscanf:
  [ ] Check the return value against the expected item count

When reading line-by-line:
  [ ] Use fgets in a while loop — NULL return signals EOF or error

When done with a file:
  [ ] Always fclose() — even on error paths (no leaked file descriptors)

When writing binary structs:
  [ ] memset the struct to zero before filling fields

When doing indexed access:
  [ ] Validate the index is >= 0 and < record count before fseek/fread
```

---

## Part 5: Common File I/O Bugs

```c
/* BUG 1: Not checking fopen for NULL */
FILE *fp = fopen("data.txt", "r");
fgets(line, sizeof(line), fp);   /* CRASH if fopen failed */
/* FIX: */
if (fp == NULL) { perror("fopen"); return 1; }

/* BUG 2: char instead of int for fgetc's result */
char c;
while ((c = fgetc(fp)) != EOF) { ... }   /* may loop forever or misbehave */
/* FIX: use int */
int c;

/* BUG 3: Forgetting the mode 'w' truncates */
FILE *fp = fopen("important_data.txt", "w");   /* ERASES existing content! */
/* FIX: use "a" to append, or "r+" to modify without truncating */

/* BUG 4: Not checking fread's return value */
fread(&record, sizeof(record), 1, fp);
printf("%d\n", record.id);   /* record may be UNINITIALIZED if fread failed/short-read */
/* FIX: */
if (fread(&record, sizeof(record), 1, fp) != 1) { /* handle error */ }

/* BUG 5: Writing uninitialized struct padding */
struct S { char a; int b; } s;
s.a = 'X'; s.b = 42;
fwrite(&s, sizeof(s), 1, fp);   /* padding bytes are garbage */
/* FIX: memset first */
memset(&s, 0, sizeof(s));

/* BUG 6: Off-by-one in fseek offset calculation */
fseek(fp, index * RECORD_SIZE, SEEK_SET);   /* int overflow risk for large files/indices */
/* FIX: cast to long (or off_t) before multiplying */
fseek(fp, (long)index * RECORD_SIZE, SEEK_SET);

/* BUG 7: Forgetting fflush before a critical read-back or crash-sensitive point */
fwrite(&record, sizeof(record), 1, fp);
/* If the program crashes here, the write might still be buffered, not on disk */
fflush(fp);   /* forces it to the OS immediately */

/* BUG 8: Using fclose on a NULL pointer */
FILE *fp = fopen("missing.txt", "r");  /* fp is NULL */
fclose(fp);   /* undefined behavior */
/* FIX: check for NULL before fclose, or structure code so this path is unreachable */
```

---

## Part 6: Text vs Binary Decision Guide

| Scenario | Format | Reason |
|----------|--------|--------|
| Config files a human edits | Text (INI/CSV) | Must be human-readable and editable |
| Log files | Text or binary | Text if tailed/grepped by humans; binary if very high volume |
| Application internal database | Binary, fixed-record | O(1) access, compact, fast |
| Data exchanged with another program/language | Text (CSV/JSON) or well-specified binary | Avoids struct-layout portability hazards |
| Small dataset, infrequent access | Text | Simplicity outweighs performance concerns |
| Large dataset, frequent indexed access | Binary, fixed-record | Performance matters at scale |
| Data that must survive across compilers/platforms | Text | Binary struct layout is not portable by default |

---

## Part 7: Debugging File I/O with Command-Line Tools

```bash
# Inspect a binary file's raw bytes
hexdump -C data.bin | head -20
xxd data.bin | head -20

# Watch a log file grow in real time (useful for append-only files)
tail -f app.log

# Check file size
ls -l data.bin
wc -c data.bin

# Compare two files byte-for-byte
diff file1.txt file2.txt
cmp file1.bin file2.bin

# Verify no leaked file descriptors after program runs (Linux)
lsof -p <pid>          # while program is running, before it exits
```
