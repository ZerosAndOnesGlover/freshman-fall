# PROG 101 · Programming I: Structured Programming in C
## Week 4 · Lecture 2: Strings in Depth — Processing, Searching, Building

---

## Lecture Goals

By the end of this lecture you will:
- Implement core string functions from scratch to understand them deeply
- Parse and process strings character by character
- Handle string I/O safely with `fgets` and `sscanf`
- Build strings with `sprintf` and `snprintf`
- Write functions that produce correct output for all inputs, including edge cases

---

## 1. The String Mental Model

A C string is **nothing more** than:
1. A sequence of `char` values in memory
2. Terminated by a `'\0'` byte
3. Accessed through a pointer (usually `char *`) to the first character

```
"Hello" in memory:

Index:   0     1     2     3     4     5
Char:   'H'   'e'   'l'   'l'   'o'  '\0'
Hex:    0x48  0x65  0x6C  0x6C  0x6F  0x00
         ↑
    char *s points here
```

There is no "string type" in C. There is no length stored alongside the characters. The null terminator IS the length information.

**Implication:** Every string operation that reads a C string must eventually check for `'\0'` to know where to stop. If `'\0'` is missing or misplaced, the function reads garbage (or crashes).

---

## 2. Implementing `strlen` from Scratch

Understanding string functions means implementing them. Let's build the standard library:

```c
/* my_strlen — count characters up to (but not including) '\0' */
size_t my_strlen(const char *s) {
    /* Precondition: s points to a null-terminated string */
    size_t len = 0;
    while (s[len] != '\0') {
        len++;
    }
    return len;
}

/* Equivalently, using pointer arithmetic */
size_t my_strlen_ptr(const char *s) {
    const char *end = s;
    while (*end != '\0') end++;
    return (size_t)(end - s);   /* pointer subtraction gives element count */
}
```

What happens on the empty string `""`?
- `s[0]` is `'\0'` immediately
- Loop body never executes
- Returns 0 ✓

What happens on `NULL`? Undefined behavior — never pass NULL to strlen without checking first.

---

## 3. Implementing `strcpy`, `strncpy`, and Why `strncpy` Is Subtle

```c
/* my_strcpy — copy src (including '\0') into dest */
char *my_strcpy(char *dest, const char *src) {
    /* Precondition: dest has room for strlen(src)+1 bytes */
    char *d = dest;
    while ((*d++ = *src++) != '\0')
        ;   /* loop body is the assignment itself */
    return dest;
}
```

The expression `(*d++ = *src++)` is C idiom: copy the character, advance both pointers, test if the copied char was `'\0'`.

**`strncpy` is NOT a safe version of `strcpy`:**

```c
char *my_strncpy(char *dest, const char *src, size_t n) {
    size_t i;
    for (i = 0; i < n && src[i] != '\0'; i++)
        dest[i] = src[i];
    /* WEIRD BEHAVIOR: if src was shorter than n, pad with '\0' to n */
    for (; i < n; i++)
        dest[i] = '\0';
    /* If src was LONGER than n, dest is NOT null-terminated! */
    return dest;
}
```

`strncpy` does not guarantee null-termination if `src` is longer than `n`. It was designed for fixed-width fields, not safe string copying.

**The safe copy idiom in modern C:**
```c
/* CORRECT safe copy pattern */
void safe_strcpy(char *dest, size_t dest_size, const char *src) {
    if (dest_size == 0) return;
    size_t i;
    for (i = 0; i < dest_size - 1 && src[i] != '\0'; i++)
        dest[i] = src[i];
    dest[i] = '\0';   /* Always null-terminate */
}

/* Or use snprintf, which always null-terminates: */
snprintf(dest, dest_size, "%s", src);
```

---

## 4. Implementing `strcmp`

```c
/* my_strcmp — compare two strings lexicographically
 * Returns: 0 if equal, <0 if s1 < s2, >0 if s1 > s2
 */
int my_strcmp(const char *s1, const char *s2) {
    while (*s1 != '\0' && *s1 == *s2) {
        s1++;
        s2++;
    }
    /* At this point: either one of them hit '\0', or they differ */
    return (unsigned char)*s1 - (unsigned char)*s2;
}
```

Why `(unsigned char)` cast? Because `char` may be signed. If the string contains bytes > 127 (e.g., UTF-8), comparing signed chars gives wrong ordering. Casting to `unsigned char` gives correct lexicographic order.

The return value:
- `0`: strings are equal
- `< 0`: first differing char in `s1` has smaller value than in `s2`
- `> 0`: first differing char in `s1` has larger value

**Common bug:**
```c
if (strcmp(s1, s2))     /* TRUE when NOT equal — often confusing */
if (strcmp(s1, s2) == 0) /* TRUE when equal — much clearer */
```

---

## 5. Character-by-Character Processing

The core skill: writing a loop that processes each character of a string.

### Pattern: Classify and Transform

```c
#include <ctype.h>   /* tolower, toupper, isalpha, isdigit, isspace */

/* Convert string to uppercase in-place */
void str_to_upper(char *s) {
    for (int i = 0; s[i] != '\0'; i++) {
        s[i] = toupper((unsigned char)s[i]);
    }
}

/* Count vowels in a string */
int count_vowels(const char *s) {
    int count = 0;
    for (int i = 0; s[i] != '\0'; i++) {
        char c = tolower((unsigned char)s[i]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u')
            count++;
    }
    return count;
}

/* Check if a string is a palindrome */
int is_palindrome(const char *s) {
    int len = (int)strlen(s);
    for (int i = 0, j = len - 1; i < j; i++, j--) {
        if (s[i] != s[j]) return 0;
    }
    return 1;
}
```

### The `<ctype.h>` Functions

Always cast to `unsigned char` before passing to ctype functions — they have undefined behavior for negative values (signed `char`):

```c
int isalpha(int c)   /* Is c a letter? */
int isdigit(int c)   /* Is c a decimal digit? */
int isalnum(int c)   /* Is c a letter or digit? */
int isspace(int c)   /* Is c whitespace (' ', '\t', '\n', '\r', '\f', '\v')? */
int islower(int c)   /* Is c a lowercase letter? */
int isupper(int c)   /* Is c an uppercase letter? */
int ispunct(int c)   /* Is c punctuation? */
int isprint(int c)   /* Is c printable (not a control character)? */
int tolower(int c)   /* Convert to lowercase (unchanged if not a letter) */
int toupper(int c)   /* Convert to uppercase */
```

---

## 6. String Searching and Parsing

### Finding Substrings

```c
/* Find first occurrence of character c in string s */
/* Returns pointer to found char, or NULL */
char *my_strchr(const char *s, int c) {
    while (*s != '\0') {
        if (*s == (char)c) return (char *)s;
        s++;
    }
    if (c == '\0') return (char *)s;   /* also matches the terminator */
    return NULL;
}

/* Find last occurrence */
char *my_strrchr(const char *s, int c) {
    const char *last = NULL;
    while (*s != '\0') {
        if (*s == (char)c) last = s;
        s++;
    }
    return (char *)last;
}
```

### Splitting Strings (Tokenizing)

`strtok` splits a string into tokens by delimiter:

```c
char line[] = "Alice,30,Engineer,New York";
char *token = strtok(line, ",");    /* First call: pass the string */
while (token != NULL) {
    printf("Token: '%s'\n", token);
    token = strtok(NULL, ",");      /* Subsequent calls: pass NULL */
}
/* Output:
   Token: 'Alice'
   Token: '30'
   Token: 'Engineer'
   Token: 'New York'
*/
```

**Warning:** `strtok` **modifies** the original string (replaces delimiters with `'\0'`) and is **not thread-safe** (uses internal static state). Use `strtok_r` in multithreaded code.

### Parsing Numbers from Strings

```c
/* Convert string to int */
int n = atoi("42");          /* Returns 42. No error checking! */
int m = atoi("abc");         /* Returns 0 — but can't distinguish from "0" */

/* Better: strtol — detects errors */
char *endptr;
long val = strtol("42abc", &endptr, 10);
if (endptr == str)           /* No digits converted */
    fprintf(stderr, "Not a number\n");
else if (*endptr != '\0')    /* Trailing non-numeric characters */
    printf("Converted %ld, remainder: '%s'\n", val, endptr);
else
    printf("Converted: %ld\n", val);    /* Full conversion */

/* strtod for doubles */
double d = strtod("3.14", NULL);
```

---

## 7. String I/O — The Safe Approach

### Reading Strings

```c
char buffer[100];

/* DANGEROUS: gets() — no bounds checking — NEVER USE */
gets(buffer);   /* Removed from C11! */

/* SAFE: fgets — reads at most size-1 characters + newline + null */
fgets(buffer, sizeof(buffer), stdin);
/* Note: fgets KEEPS the newline '\n' if the line fits */

/* Remove the trailing newline from fgets: */
size_t len = strlen(buffer);
if (len > 0 && buffer[len-1] == '\n')
    buffer[len-1] = '\0';

/* scanf %s — reads a word (stops at whitespace), no spaces allowed */
scanf("%99s", buffer);    /* %99s: at most 99 chars + null = 100 bytes max */

/* scanf with format — for structured input */
char name[50];
int age;
sscanf("Alice 30", "%49s %d", name, &age);   /* Parse from a string */
```

### Writing Strings

```c
char buffer[100];

/* printf — to stdout */
printf("Hello, %s! You are %d years old.\n", name, age);

/* fprintf — to a file or stderr */
fprintf(stderr, "Error: %s\n", error_message);

/* sprintf — writes into a string buffer (DANGEROUS if buffer too small) */
sprintf(buffer, "%s is %d years old", name, age);

/* snprintf — SAFE: limits to n-1 chars + null */
snprintf(buffer, sizeof(buffer), "%s is %d years old", name, age);
/* Always null-terminates. Returns the number of chars that WOULD have been
   written (excluding null) — if >= sizeof(buffer), output was truncated */

int written = snprintf(buffer, sizeof(buffer), "Very long: %s...", long_string);
if (written >= (int)sizeof(buffer)) {
    printf("Warning: output was truncated\n");
}
```

**Rule:** Use `snprintf` whenever writing to a fixed-size buffer. Never use `sprintf`.

---

## 8. Building Strings Incrementally

A common pattern: building a string piece by piece:

```c
/* Build a CSV row from an array of strings */
void build_csv(const char *fields[], int n, char *out, size_t out_size) {
    out[0] = '\0';   /* Start with empty string */
    
    for (int i = 0; i < n; i++) {
        if (i > 0) {
            strncat(out, ",", out_size - strlen(out) - 1);
        }
        strncat(out, fields[i], out_size - strlen(out) - 1);
    }
}
/* This is O(n²) because strncat scans to the end each time */

/* More efficient: track current position */
void build_csv_fast(const char *fields[], int n, char *out, size_t out_size) {
    size_t pos = 0;
    
    for (int i = 0; i < n && pos < out_size - 1; i++) {
        if (i > 0 && pos < out_size - 1) {
            out[pos++] = ',';
        }
        /* snprintf returns chars that WOULD be written — use this to advance pos */
        int written = snprintf(out + pos, out_size - pos, "%s", fields[i]);
        if (written < 0) break;
        pos += (size_t)written;
        if (pos >= out_size) { pos = out_size - 1; break; }
    }
    out[pos] = '\0';
}
```

---

## 9. Practical String Processing Examples

### Word Count

```c
/* Count words in a string (words separated by whitespace) */
int word_count(const char *s) {
    int count = 0;
    int in_word = 0;
    
    for (int i = 0; s[i] != '\0'; i++) {
        if (!isspace((unsigned char)s[i])) {
            if (!in_word) {
                count++;
                in_word = 1;
            }
        } else {
            in_word = 0;
        }
    }
    return count;
}
```

### String Reverse

```c
/* Reverse a string in-place */
void str_reverse(char *s) {
    int len = (int)strlen(s);
    for (int i = 0, j = len - 1; i < j; i++, j--) {
        char tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }
}
```

### Check Prefix/Suffix

```c
/* Does s start with prefix? */
int starts_with(const char *s, const char *prefix) {
    while (*prefix != '\0') {
        if (*s == '\0' || *s != *prefix) return 0;
        s++;
        prefix++;
    }
    return 1;
}

/* Does s end with suffix? */
int ends_with(const char *s, const char *suffix) {
    size_t slen = strlen(s);
    size_t suflen = strlen(suffix);
    if (suflen > slen) return 0;
    return strcmp(s + slen - suflen, suffix) == 0;
}
```

### Trim Whitespace

```c
/* Remove leading and trailing whitespace from s (modifies in-place) */
void str_trim(char *s) {
    /* Trim leading whitespace */
    int start = 0;
    while (isspace((unsigned char)s[start])) start++;
    
    /* Shift the string left */
    int len = (int)strlen(s);
    memmove(s, s + start, len - start + 1);   /* +1 includes '\0' */
    
    /* Trim trailing whitespace */
    len = (int)strlen(s);
    while (len > 0 && isspace((unsigned char)s[len - 1])) {
        s[--len] = '\0';
    }
}
```

---

## 10. String Gotchas Summary

```c
/* GOTCHA 1: Comparing strings with == compares addresses, not content */
if (s1 == s2)           /* WRONG: checks if same memory location */
if (strcmp(s1, s2) == 0) /* CORRECT: checks content equality */

/* GOTCHA 2: strlen returns size_t (unsigned) — subtraction can wrap */
if (strlen(s) - 1 >= 0)  /* ALWAYS TRUE: size_t can't be negative */
if (strlen(s) > 0)        /* CORRECT: check before subtracting */

/* GOTCHA 3: String literals are immutable */
char *s = "Hello";
s[0] = 'h';               /* UNDEFINED BEHAVIOR */
char s[] = "Hello";
s[0] = 'h';               /* OK: s is a local array copy */

/* GOTCHA 4: Array and pointer not the same for sizeof */
char arr[] = "Hello";
char *ptr = arr;
sizeof(arr)   /* 6: total bytes of the array including '\0' */
sizeof(ptr)   /* 8: size of a pointer (not the string!) */

/* GOTCHA 5: fgets includes the newline */
fgets(buf, sizeof(buf), stdin);
printf("'%s'\n", buf);   /* Prints 'Hello\n' — note the newline */
/* Strip it: */
buf[strcspn(buf, "\n")] = '\0';   /* Elegant one-liner */
```

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict each value and explain the two that differ from naive expectation.

```c
char arr[] = "hi";
char *ptr  = "hi";

strlen("hi")
sizeof("hi")
sizeof(arr)
sizeof(ptr)
```

**2. (Explain.)** `strncpy` is widely believed to be the safe version of `strcpy`. Show precisely how it fails to guarantee termination, and what it does when the source is short.

**3. (Build.)** Implement `strlen`, `strcmp`, and a safe `copy_string` from scratch. Explain the return-value contract of `strcmp` precisely — including what it does *not* promise.

**4. (Stretch.)** Write a function that reverses the words in a sentence in place — `"the quick brown fox"` becomes `"fox brown quick the"` — using O(1) extra space. Explain the algorithm.


### Answers

**1.** `2`, **`3`**, **`3`**, `8`.

**`sizeof("hi")` is 3** because a string literal is a `char` array containing `'h'`, `'i'`, and the terminating `'\0'`. `strlen` counts characters *before* the terminator and gives 2. The relationship is always `sizeof(literal) == strlen(literal) + 1`, and confusing them is the direct cause of most off-by-one buffer bugs — a buffer sized `strlen(s)` has no room for the terminator.

**`sizeof(arr)` is 3** because `char arr[] = "hi"` **copies** the literal into a local array of size 3. `sizeof(ptr)` is 8 because `ptr` is a pointer.

The `arr` / `ptr` distinction matters beyond size. `arr` is a modifiable copy — `arr[0] = 'H'` is fine. `ptr` points into **read-only** memory (the `.rodata` section), so `ptr[0] = 'H'` compiles without complaint and **segfaults at runtime**. This is why string literals should be declared `const char *ptr = "hi";` — the `const` moves the error from runtime to compile time, and modern compilers warn with `-Wwrite-strings`.

Also note `strlen` is **O(n)**: it scans for the terminator every call. `for (size_t i = 0; i < strlen(s); i++)` is therefore O(n²). Hoist it.

**2.** `strncpy(dst, src, n)` copies at most `n` bytes. Two separate surprises follow.

**If `strlen(src) >= n`, no terminator is written.** `dst` is left as an unterminated character array, and every subsequent `strlen`, `printf("%s")`, or `strcat` runs off the end into whatever follows.

```c
char buf[6];
strncpy(buf, "abcdefgh", 5);   /* copies 'a'..'e' — no '\0' */
buf[5] = '\0';                    /* YOU must add it */
```

**If `strlen(src) < n`, it pads the remainder with `'\0'`** — all the way to `n` bytes. So `strncpy(b2, "ab", 8)` writes `'a' 'b'` then **six** zero bytes, which is wasted work on a large buffer and surprising if you expected one terminator.

The reason for both behaviours is historical: `strncpy` was designed for fixed-width, non-terminated fields in early UNIX directory entries, not for strings. It is not a safe `strcpy`; it is a different function that happens to look like one.

**Use `snprintf` instead**, which always terminates and is portable:

```c
snprintf(dst, sizeof dst, "%s", src);
```

It returns the length it *would* have written, so `>= sizeof dst` detects truncation. (`strlcpy` is cleaner still but is not in standard C.)

**3.**

```c
#include <stddef.h>

size_t my_strlen(const char *s) {
    const char *p = s;
    while (*p) p++;
    return (size_t)(p - s);
}

int my_strcmp(const char *a, const char *b) {
    while (*a && *a == *b) { a++; b++; }
    return (unsigned char)*a - (unsigned char)*b;
}

int copy_string(char *dst, size_t cap, const char *src) {
    size_t i = 0;
    while (i + 1 < cap && src[i]) { dst[i] = src[i]; i++; }
    if (cap) dst[i] = '\0';
    return src[i] == '\0';        /* 1 = complete, 0 = truncated */
}
```

**`strcmp` promises only the *sign*:** negative if `a` sorts before `b`, zero if equal, positive otherwise. It does **not** promise −1/0/+1, and it does not promise the numeric difference between the characters — glibc returns the difference, but other implementations return ±1, and a SIMD implementation may return anything with the right sign. So `if (strcmp(a, b) == -1)` is a real bug that works on your machine and fails elsewhere. Always compare against 0: `if (strcmp(a, b) < 0)`.

The **`(unsigned char)` casts** matter. Plain `char` is signed on x86, so comparing a byte ≥ 128 (a UTF-8 continuation byte, say) against an ASCII byte would give the wrong sign. The standard specifies that `strcmp` compares as `unsigned char`.

`copy_string` reserves a byte for the terminator via `i + 1 < cap`, always terminates when `cap > 0`, and reports truncation — the three things `strncpy` does not do.

**4.**

```c
#include <string.h>

static void reverse_range(char *a, char *b) {   /* b points at last char */
    while (a < b) { char t = *a; *a++ = *b; *b-- = t; }
}

void reverse_words(char *s) {
    size_t n = strlen(s);
    if (n == 0) return;

    reverse_range(s, s + n - 1);               /* 1. reverse the whole string */

    char *start = s;                           /* 2. reverse each word back */
    for (char *p = s; ; p++) {
        if (*p == ' ' || *p == '\0') {
            reverse_range(start, p - 1);
            if (*p == '\0') break;
            start = p + 1;
        }
    }
}
```

The algorithm is the **double-reversal trick**. Reversing the entire string puts the words in the right order but spells each one backwards: `"the quick"` → `"kciuq eht"`. Reversing each word individually then repairs the letters while leaving the word order alone. Two linear passes, **O(n) time and O(1) space** — no second buffer, no allocation.

The same trick rotates an array by k: reverse the first k, reverse the rest, reverse the whole thing.

Note the loop treats `'\0'` as a word terminator alongside `' '`, which handles the final word without duplicating the reversal code after the loop — the `break` comes *after* the reversal, deliberately. Test it on the empty string, a single word, and a string with a trailing space; those three cases catch essentially every bug this function can have.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **String** | Null-terminated character array — no separate length field |
| **Null terminator** | `'\0'` (byte value 0) — marks the end of a string |
| **Buffer overflow** | Writing characters past the end of a character array |
| **Lexicographic order** | Dictionary ordering: character by character by ASCII value |
| **Token** | A piece of a string delimited by a separator |
| **`snprintf`** | Safe formatted string building — always null-terminates, never overflows |
| **`fgets`** | Safe line reading — reads at most n-1 chars, always null-terminates |

---

## Reading

- **K&R §5.5** — Character Pointers and Functions
- **King Ch. 13** — Strings (implement your own versions of the standard functions)
- **Man pages:** `man 3 strlen`, `man 3 strcpy`, `man 3 strcat`, `man 3 snprintf`

---

*Next: Lab 2 — Building a String Processing Library*
