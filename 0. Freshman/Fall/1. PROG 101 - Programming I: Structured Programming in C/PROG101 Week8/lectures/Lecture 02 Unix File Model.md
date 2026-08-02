# PROG 101 Programming I: Structured Programming in C
## Week 8 · Lecture 2: The UNIX File Model — File Descriptors and Low-Level I/O

---

## Lecture Goals

By the end of this lecture you will:
- Understand the "everything is a file" philosophy of Unix
- Know what a file descriptor is and how it differs from `FILE *`
- Use the low-level system calls `open`, `read`, `write`, `close`
- Understand the relationship between `FILE *` streams and file descriptors
- Use `lseek` to move within a file, and understand random access
- Understand redirection and pipes at the file descriptor level

---

## 1. "Everything Is a File" — The Unix Philosophy

One of Unix's most powerful design decisions: files, terminals, pipes, network sockets, and devices are all accessed through the **same interface** — `open`, `read`, `write`, `close`. A program that processes text doesn't need to know whether that text comes from a real file, a keyboard, or another program's output — the interface is identical.

This uniformity is why you can do:
```bash
./my_program < input.txt        # read from a file instead of the keyboard
./my_program | grep "error"     # feed output into another program
cat file.txt | ./my_program     # read from another program's output
```

Your program's code doesn't change at all — it always reads from `stdin` using the same functions. The **shell** decides what `stdin` actually connects to before your program even starts.

---

## 2. File Descriptors — The Kernel-Level Handle

A **file descriptor** is a small non-negative integer that the operating system uses to identify an open file (or socket, or pipe) for a running process. It is an index into a per-process table maintained by the kernel.

```
Every process starts with three file descriptors already open:

  fd 0  →  stdin   (standard input)
  fd 1  →  stdout  (standard output)
  fd 2  →  stderr  (standard error)
```

When you call `open()`, the kernel finds a free slot in this table and returns its index:

```c
#include <fcntl.h>    /* open, O_RDONLY, etc. */
#include <unistd.h>   /* read, write, close */

int fd = open("data.txt", O_RDONLY);
if (fd == -1) {
    perror("open");
    return 1;
}
/* fd is typically 3 (0,1,2 are already taken) */
```

---

## 3. The Low-Level System Calls

```c
#include <fcntl.h>
#include <unistd.h>

int    open(const char *pathname, int flags, ...);
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
int    close(int fd);
```

### Opening

```c
int fd = open("data.txt", O_RDONLY);                       /* read only */
int fd = open("out.txt",  O_WRONLY | O_CREAT | O_TRUNC, 0644);  /* write, create, truncate */
int fd = open("log.txt",  O_WRONLY | O_CREAT | O_APPEND, 0644); /* append */
```

The third argument (permissions, e.g., `0644`) is only used when `O_CREAT` is specified — it sets the Unix file permission bits (owner read/write, group read, others read, in octal).

| Flag | Meaning |
|------|---------|
| `O_RDONLY` | Read only |
| `O_WRONLY` | Write only |
| `O_RDWR` | Read and write |
| `O_CREAT` | Create the file if it doesn't exist |
| `O_TRUNC` | Truncate to zero length if it exists |
| `O_APPEND` | Writes always go to the end |

### Reading and Writing

```c
char buf[256];
ssize_t n = read(fd, buf, sizeof(buf));
/* n = number of bytes actually read (may be less than requested!)
   n = 0 means end-of-file
   n = -1 means error (check errno) */

ssize_t written = write(fd, buf, n);
/* written = number of bytes actually written (may be less than requested!)
   written = -1 means error */
```

**Critical:** `read` and `write` may transfer *fewer* bytes than requested — this is not an error, just how the system call contract works (especially for pipes, sockets, or interrupted calls). Robust code loops until all bytes are handled:

```c
ssize_t write_all(int fd, const void *buf, size_t count) {
    const char *p = buf;
    size_t remaining = count;
    while (remaining > 0) {
        ssize_t written = write(fd, p, remaining);
        if (written == -1) {
            if (errno == EINTR) continue;   /* interrupted — retry */
            return -1;                       /* real error */
        }
        p += written;
        remaining -= (size_t)written;
    }
    return (ssize_t)count;
}
```

### Closing

```c
if (close(fd) == -1) {
    perror("close");
}
```

---

## 4. `FILE *` vs File Descriptor — The Relationship

`FILE *` (from `<stdio.h>`) is a **higher-level abstraction built on top of** file descriptors. Every `FILE *` internally wraps an `int` file descriptor and adds:
- A memory buffer (for efficiency — fewer system calls)
- Formatted I/O support (`fprintf`, `fscanf`)
- Convenient line/character reading (`fgets`, `fgetc`)
- Automatic EOF/error tracking

```c
FILE *fp = fopen("data.txt", "r");
int fd = fileno(fp);            /* extract the underlying file descriptor */
printf("Underlying fd: %d\n", fd);
```

**When to use which:**

| Use `FILE *` (`fopen`/`fread`/`fprintf`) | Use raw fd (`open`/`read`/`write`) |
|-------------------------------------------|--------------------------------------|
| General text/data processing | Low-level systems programming |
| You want buffering (fewer syscalls) | You need precise control over I/O timing |
| Portable, standard C | Unix-specific (POSIX) system programming |
| Most application code | OS/networking/high-performance code |

For this course, **prefer `FILE *`** for nearly everything — it's portable, safer, and sufficient for almost all tasks. Understanding file descriptors is essential background knowledge (especially for PROG 201 / systems programming later), but day-to-day C application code uses `stdio.h`.

---

## 5. Random Access — `fseek` and `ftell`

Files aren't only read sequentially from start to end — you can jump to an arbitrary position.

```c
FILE *fp = fopen("data.bin", "rb");

fseek(fp, 0, SEEK_END);          /* move to end of file */
long size = ftell(fp);            /* current position = file size in bytes */
fseek(fp, 0, SEEK_SET);          /* move back to the beginning */

fseek(fp, 100, SEEK_SET);        /* jump to byte offset 100 */
fseek(fp, 50, SEEK_CUR);         /* move 50 bytes forward from current position */
fseek(fp, -20, SEEK_END);        /* move to 20 bytes before the end */

long pos = ftell(fp);            /* query the current position */
rewind(fp);                       /* equivalent to fseek(fp, 0, SEEK_SET); clears errors too */
```

| `whence` value | Meaning |
|-----------------|---------|
| `SEEK_SET` | Offset is relative to the beginning of the file |
| `SEEK_CUR` | Offset is relative to the current position |
| `SEEK_END` | Offset is relative to the end of the file |

### The Idiom: Determine File Size

```c
FILE *fp = fopen("data.bin", "rb");
fseek(fp, 0, SEEK_END);
long size = ftell(fp);
rewind(fp);

/* Now you know exactly how many bytes to allocate/read */
char *buffer = malloc(size);
fread(buffer, 1, size, fp);
```

The raw file descriptor equivalent is `lseek`:
```c
#include <unistd.h>
off_t lseek(int fd, off_t offset, int whence);

off_t size = lseek(fd, 0, SEEK_END);
lseek(fd, 0, SEEK_SET);
```

---

## 6. Redirection — What the Shell Actually Does

When you run:
```bash
./program < input.txt > output.txt 2> errors.txt
```

Before your program's `main` even starts, the shell:
1. `fork()`s a child process
2. In the child, closes fd 0 (stdin), opens `input.txt`, and the OS assigns it fd 0 (the lowest free number)
3. Closes fd 1 (stdout), opens `output.txt` for writing, OS assigns it fd 1
4. Closes fd 2 (stderr), opens `errors.txt` for writing, OS assigns it fd 2
5. `exec()`s your program

Your program never knows the difference — it reads from fd 0 and writes to fd 1/2 exactly as if they were the terminal. This is the elegance of the file descriptor abstraction: **redirection is entirely the shell's responsibility**, invisible to your code.

### Pipes — Connecting Two Programs

```bash
./producer | ./consumer
```

The shell creates a **pipe** (an in-memory, one-directional byte channel with two file descriptor ends: a read end and a write end), then:
- In `producer`'s process: fd 1 (stdout) is redirected to the pipe's write end
- In `consumer`'s process: fd 0 (stdin) is redirected to the pipe's read end

`producer`'s output bytes flow directly into `consumer`'s input — again, with zero awareness in either program's code. Both just read/write their standard streams normally.

---

## 7. A Practical Pattern: Copying a File

Using `FILE *` (recommended for this course):

```c
int copy_file(const char *src_path, const char *dst_path) {
    FILE *src = fopen(src_path, "rb");
    if (src == NULL) { perror("fopen src"); return -1; }

    FILE *dst = fopen(dst_path, "wb");
    if (dst == NULL) {
        perror("fopen dst");
        fclose(src);
        return -1;
    }

    char buffer[4096];
    size_t n;
    while ((n = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        if (fwrite(buffer, 1, n, dst) != n) {
            fprintf(stderr, "Write error\n");
            fclose(src);
            fclose(dst);
            return -1;
        }
    }

    fclose(src);
    fclose(dst);
    return 0;
}
```

Note the buffered chunked copy (4096 bytes at a time) — this is far more efficient than copying byte-by-byte (which would issue one system call per byte at the raw fd level, or incur significant function-call overhead even with buffered stdio).

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict the file offset and contents after each step.

```c
FILE *f = fopen("t.txt", "w+");
fputs("Hello World", f);
fseek(f, 6, SEEK_SET);
fputs("C!", f);
fseek(f, 0, SEEK_END);
long n = ftell(f);
```

**2. (Explain.)** Explain the relationship between a file descriptor and a `FILE *`. Which is the OS's and which is the C library's? When would you use each?

**3. (Build.)** Write a file-copy program using only the low-level calls `open`, `read`, `write`, `close`. Explain why `write` must be called in a loop.

**4. (Stretch.)** Explain what the shell does for `./prog > out.txt 2>&1`, in terms of file descriptors. Why does the order of the two redirections matter?


### Answers

**1.** After `fputs("Hello World", f)` the offset is 11 and the file holds `Hello World`.

`fseek(f, 6, SEEK_SET)` moves to byte 6 — the `W`.

`fputs("C!", f)` **overwrites** bytes 6 and 7, giving `Hello C!rld`. The offset is 8.

`fseek(f, 0, SEEK_END)` then `ftell` gives **`n = 11`**.

The essential point: **writing in the middle of a file overwrites; it never inserts.** A file is a flat byte array, not a list, so making room requires copying everything after the insertion point — which is why text editors read, modify, and rewrite whole files rather than patching them.

The three origins are `SEEK_SET` (from the start), `SEEK_CUR` (from the current position, and the offset may be negative), and `SEEK_END` (from the end; `fseek(f, -4, SEEK_END)` reads the last four bytes).

One rule specific to `"+"` modes: between a read and a write on the same stream you **must** call `fseek`, `fsetpos`, or `rewind`, even if the position is already correct. Without it the behaviour is undefined, because the library's buffer state is ambiguous. Also note `ftell` on a text-mode stream returns an opaque value on some platforms — use binary mode when you rely on the number.

**2.** A **file descriptor** is a small non-negative `int` — an index into the kernel's per-process table of open files. It is the **operating system's** handle, used by the raw system calls `open`, `read`, `write`, `close`, `lseek`. Descriptors 0, 1, and 2 are always stdin, stdout, and stderr.

A **`FILE *`** is a pointer to a C library struct that **wraps** a descriptor and adds buffering, position tracking, an EOF flag, an error flag, and formatted I/O. It is the **C standard library's** handle, used by `fopen`, `fread`, `fprintf`, `fgets`.

You can move between them: `fileno(f)` extracts the descriptor from a `FILE *`, and `fdopen(fd, "r")` wraps a descriptor in a stream.

**Use `FILE *` by default.** It is standard C and therefore portable; it gives you `printf`-style formatting; and its buffering means a thousand `fputc` calls become a handful of system calls, which matters enormously — a system call costs on the order of a microsecond, a buffered write a few nanoseconds.

**Drop to file descriptors** when you need something the stream layer does not expose: `select`/`poll` on sockets and pipes, `dup2` for redirection, `fcntl` for locking or non-blocking mode, `mmap`, or precise control over when bytes hit the disk. Also when you must avoid buffering entirely, since mixing buffered and raw I/O on the same file gives interleaving you cannot predict.

The layering is worth remembering generally: **`FILE *` is a portable convenience built on a platform-specific primitive**, and every high-level I/O API you meet later has the same shape.

**3.**

```c
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s SRC DST\n", argv[0]);
        return 1;
    }

    int in = open(argv[1], O_RDONLY);
    if (in < 0) { perror(argv[1]); return 1; }

    int out = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (out < 0) { perror(argv[2]); close(in); return 1; }

    char buf[8192];
    ssize_t n;
    while ((n = read(in, buf, sizeof buf)) > 0) {
        ssize_t written = 0;
        while (written < n) {
            ssize_t w = write(out, buf + written, (size_t)(n - written));
            if (w < 0) { perror("write"); close(in); close(out); return 1; }
            written += w;
        }
    }
    if (n < 0) { perror("read"); close(in); close(out); return 1; }

    close(in);
    close(out);
    return 0;
}
```

**`write` may perform a partial write** — it returns the number of bytes actually written, which can be less than requested. On a regular file this is rare, but on a pipe, socket, or terminal it is routine, and a signal can interrupt a large write at any time. Ignoring the return value silently truncates data. The inner loop is not defensive padding; it is the contract.

`read` similarly returns *at most* the requested count; `> 0` means data, `0` means EOF, `< 0` means error. The third argument to `open` is the permission mode, used only when `O_CREAT` creates the file, and it is further masked by the process `umask`.

The 8 KB buffer amortises the system-call cost — copying byte by byte would issue millions of syscalls and run orders of magnitude slower.

**4.** The shell forks, and **in the child, before `exec`**, it rearranges the descriptor table:

1. `> out.txt` — open `out.txt` (creating/truncating), then `dup2(fd, 1)`, making descriptor **1** refer to the file. `dup2` closes the old 1 first.
2. `2>&1` — `dup2(1, 2)`, making descriptor **2** a copy of whatever 1 currently is: the file.

Then it `exec`s `./prog`, which inherits the table. The program writes to descriptors 1 and 2 knowing nothing about any of this — **the redirection is entirely outside the program**, which is why every Unix tool supports it without a line of code.

**Order matters because `2>&1` copies wherever 1 points *at that moment*.** Reversed:

```bash
./prog 2>&1 > out.txt
```

descriptor 2 is first made a copy of 1 — which is still the **terminal** — and only then is 1 redirected to the file. The result is stdout in the file and stderr on the terminal, the opposite of what most people intend. `2>&1` means "send 2 where 1 goes *now*", not "keep 2 tied to 1".

The same mechanism underlies pipes: `a | b` creates a pipe, `dup2`s the write end onto `a`'s descriptor 1 and the read end onto `b`'s descriptor 0. This is the concrete meaning of "everything is a file" — because a program only ever sees numbered descriptors, the same code works against a file, a pipe, a socket, or a terminal.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **File descriptor** | Small non-negative integer identifying an open file within a process |
| **`open`/`read`/`write`/`close`** | Low-level POSIX system calls operating on file descriptors |
| **`fileno`** | Extracts the underlying file descriptor from a `FILE *` |
| **`fseek`/`ftell`** | Move to / query the current position within a file stream |
| **`lseek`** | Low-level equivalent of `fseek` for raw file descriptors |
| **Redirection** | Shell mechanism connecting a program's stdin/stdout/stderr to files |
| **Pipe** | An in-memory channel connecting one program's stdout to another's stdin |
| **`SEEK_SET`/`SEEK_CUR`/`SEEK_END`** | Reference points for `fseek`/`lseek` offsets |

---

## Reading

- **CS:APP §10.1–10.6** — System-Level I/O (excellent depth on this exact topic)
- **The Linux Programming Interface, Ch. 4–5** — File I/O: The Universal I/O Model
- **man pages:** `man 2 open`, `man 2 read`, `man 2 write`, `man 3 fseek`

---

*Next: Lecture 3 — Binary Files and Struct Serialization*
