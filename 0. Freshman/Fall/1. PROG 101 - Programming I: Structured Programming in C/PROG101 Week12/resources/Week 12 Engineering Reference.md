# PROG 101 Week 12 Reference
## Style, Testing, Debugging

---

## Style

**Code is read far more often than written.** Every rule below follows from that.

| Rule | Because |
|---|---|
| Name length scales with scope | `i` in a 3-line loop is clear; at file scope it is not |
| Booleans read as assertions | `file_is_open(f)` not `check_file(f)` |
| Functions named for the return value | `list_insert` returning a **status**, not the value |
| **Consistency beats preference** | Two styles in one file is worse than either alone |
| Comments say **why** | The code already says what; a repeating comment will drift and lie |
| Delete commented-out code | Version control remembers it |
| One job per function | So it can be named accurately |
| Boolean parameters | Usually two functions in disguise — `save(r,1)` tells the reader nothing |
| Guard clauses | Keep the main path at one indentation level |
| `goto cleanup` | Idiomatic in C — one exit path, one copy of the cleanup |
| `static` on internals | Shrinks the interface; prevents coupling |
| Prefix consistently | C has no namespaces |

---

## Testing

C provides no framework. `assert` is not one: it aborts on first failure and **is disabled by
`-DNDEBUG`**.

```c
#define CHECK(cond)                                              \
    do {                                                         \
        checks_run++;                                            \
        if (!(cond)) {                                           \
            checks_failed++;                                     \
            fprintf(stderr, "  %s:%d: FAIL: %s\n",               \
                    __FILE__, __LINE__, #cond);                  \
        }                                                        \
    } while (0)
```

**It must be a macro** — only a macro sees the caller's `__FILE__`/`__LINE__` and can stringify the
condition with `#cond`.

**Copy arguments into temporaries** in comparison macros, or `CHECK_EQ_INT(i++, 1)` evaluates twice.

### Choosing cases

| Case | |
|---|---|
| **n = 0** | The most productive test case there is |
| n = 1 | Often a different path |
| n = 2 | Smallest case where order matters |
| n at capacity / past capacity | Forces growth |
| 0, 1, −1, `INT_MAX`, `INT_MIN` | Numeric boundaries |
| `""`, one char, exactly full, one longer, byte > 127 | Strings |

**Test behaviour, not internals.** `CHECK(vec_size(v) == 5)`, not `CHECK(v->cap == 8)`.

### Coverage

```bash
gcc --coverage -O0 -o test test.c code.c && ./test && gcov code.c
```

`#####` marks never-executed lines — **that** is the useful output, not the percentage.

**High coverage ≠ correct.** `divide(a,b)` has 100% coverage from `divide(6,2)` and is undefined for
`b == 0`. **Low coverage ⇒ untested**; the implication runs one way.

**Testing shows the presence of bugs, never their absence.**

---

## Debugging

**The method:** reproduce → reduce the input → hypothesise something testable → change one thing →
fix the *cause* → add a test.

```bash
gcc -Wall -Wextra -g -O0 prog.c -o prog
gdb ./prog
```

| Command | Effect |
|---|---|
| `run`, `bt` | Start; **backtrace** — run this first on any crash |
| `frame N`, `info locals`, `print x` | Inspect |
| `break f`, `break file.c:42` | Breakpoints |
| `next`, `step`, `continue` | Step over / into / resume |
| `watch x` | **Stop at the instruction that changes `x`** |

Verified crash output — note the **argument value**, which names the real culprit:

```
#0  0x... in deref (p=0x0) at crash.c:2
#1  0x... in main () at crash.c:3
```

### Tool by symptom

| Symptom | First tool |
|---|---|
| Segfault at a consistent line | GDB `bt` |
| Crash far from the bug | ASan |
| Works `-O0`, breaks `-O2` | **UBSan** — the signature of UB |
| Memory grows | Valgrind `--leak-check=full` |
| Wrong answer, no crash | **Tests + `gcov`** — no sanitizer will fire |
| Variable becomes wrong | GDB `watch` |
| Uninitialised value | **Valgrind** — ASan misses these |

### `-O0` works, `-O2` breaks

**Almost never a compiler bug. Almost always undefined behaviour.**

1. `-fsanitize=address,undefined -g -O1`
2. Valgrind if the sanitizers are silent
3. `-Wshadow -Wconversion -Wundef`
4. Bisect: `-fno-strict-aliasing` (type punning) or `-fno-strict-overflow` (signed overflow)

**Step 4 is a diagnosis, not a fix.** Shipping with the flag hides the bug.

---

*PROG 101 · Week 12 · Reference · © CSE Department*
