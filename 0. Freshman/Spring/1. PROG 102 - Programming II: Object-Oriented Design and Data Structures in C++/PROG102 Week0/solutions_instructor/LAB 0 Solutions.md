# PROG 102 · Lab 0 — Solutions and Checkoff Notes
## Porting C to C++

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Part A is the reason this lab is in Week 0, and it is not administrative filler.** Every semester a
handful of students cannot build with `-fsanitize=thread`, and every semester the ones who do not
check now discover it in **Week 10** — a midterm week, in a lab that is entirely ThreadSanitizer.

**Run Part A first, as a room.** Ask for hands on any tool that failed, and deal with those students
before anyone starts Part B. Twenty minutes here saves a bad Week 10.

**Known environment issues:**

| Symptom | Cause | Fix |
| --- | --- | --- |
| **TSan builds, then dies at startup** with `FATAL: ThreadSanitizer: unexpected memory mapping` | ASLR entropy on some Linux kernels | **`setarch $(uname -m) -R ./prog`**. Verified: TSan is fully functional under it — it detects a real race and correctly reports none on a thread-safe magic static. **This is the most likely failure in A1** and it is invisible if you only check the build. |
| `perf` refuses to run | `kernel.perf_event_paranoid` | Lab machines are configured; on personal Linux, `sudo sysctl kernel.perf_event_paranoid=1`. **Week 12 only** — do not let it block today. |
| ASan and TSan both fail | Sanitizer runtime not installed | Package is usually `libasan`/`libtsan` alongside gcc |
| macOS: no ThreadSanitizer | Apple clang ships it; `-fsanitize=thread` works | Accept clang for this course; note the version |
| Windows | Native MSVC lacks these | Direct to WSL or the lab machines **today**, not in Week 10 |

`stack.c` is distributed with the lab. **Students must not modify it** — the diff in Part C is
meaningless if they do.

---

## Part A — Toolchain (8)

### A1 (4)

Reference environment:

```
g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
valgrind-3.22.0
```

*Marking: 4 for a complete table with six rows. **Award full marks for a tool that is missing if the
student identified it and raised it.** The objective is knowing the state of your machine, not having
a perfect machine. A blank row with no comment is 0 for that row.*

### A2 (2)

**`__cplusplus = 201703`** under `-std=c++17`.

*A student reporting `201402` has a default-standard build and did not pass `-std=c++17`. Worth
catching now — it will silently break Week 5's `unique_ptr` work. Award 1 and correct them on the
spot.*

### A3 (2)

Both build lines run. **The `-O2` line is the one for timing**, because AddressSanitizer costs a large
constant factor and would make every measurement meaningless.

*Marking: 1 both transcripts, 1 the correct choice with a reason. "Because it's optimised" is
acceptable; "because ASan is slow" is better and is what the syllabus says.*

---

## Part B — The Port (16)

### B1 (10)

```cpp
class IntStack {
    int* data;
    int  count;
    int  cap;
public:
    explicit IntStack(int capacity)
        : data(new int[capacity]), count(0), cap(capacity) {}
    ~IntStack() { delete[] data; }

    void push(int v) {
        if (count == cap) {
            int  newcap = cap * 2;
            int* bigger = new int[newcap];
            std::copy(data, data + count, bigger);
            delete[] data;
            data = bigger; cap = newcap;
        }
        data[count++] = v;
    }
    int  pop()            { return data[--count]; }
    int  size()  const    { return count; }
    bool empty() const    { return count == 0; }
    int  capacity() const { return cap; }
};
```

*Marking: 3 constructor + destructor, 2 correct growth, 2 `const` on exactly `size`/`empty`/`capacity`,
1 `bool` from `empty()`, 1 private data, 1 `explicit`.*

**Common faults:**

- **`realloc` on the `new[]` array.** Undefined behaviour — mixing allocators. Deduct 2 and explain;
  they will meet the real reason (constructors do not run) in Week 6.
- **`pop()` marked `const`.** It modifies `count`. The compiler catches it; a student who submitted it
  did not build with the stated line.
- **A manual copy loop instead of `std::copy`.** Fine, full marks. `std::copy` is Week 3 material and
  is not required here.
- **Forgetting `delete[] data` in the growth path.** ASan catches it. Deduct 1 — it is a leak, not a
  crash, and the student almost certainly did not run the sanitizer build.

### B2 (3)

Reference output, byte-identical to the C version:

```
size=5 cap=8
25 16 9 4 1
```

*Marking: 2 identical output, 1 **no cleanup call in `main`**. The second is the assessed half — a
student who wrote a `destroy()` method and called it has ported the syntax and missed the lab.*

### B3 (3)

Clean build, clean run.

*Marking: 2 no warnings, 1 sanitizer-clean. Deduct all 3 if they only pasted the `-O2` build — the
sanitizer transcript is the evidence being asked for.*

---

## Part C — Prove Nothing Changed (8)

### C1 (4)

`diff` produces **no output**.

*Marking: 4. A student with a difference should be debugged live — the usual causes are a trailing
space, `std::endl` versus `"\n"`, or printing `cap` before the final push.*

### C2 (4)

`cap=8`. Starting at 2 and doubling: 2 → 4 → 8, reached on the fifth push.

*Marking: 2 for the number, 2 for having checked their growth policy against it. As the sheet says, a
student who reports `cap=5` because they grew by exact-fit is **not wrong about C++** — award 3 and
note that the lab specified this program.*

---

## Part D — What the Port Bought (8)

### D1 (4)

```
Direct leak of 32 byte(s) in 1 object(s) allocated from:
SUMMARY: AddressSanitizer: 32 byte(s) leaked in 1 allocation(s).
```

32 bytes = capacity 8 × 4 bytes per `int`.

*Marking: 3 transcript, 1 explaining the 32. **A student who reports 8 or 20 bytes has a different
growth policy** and should be marked against their own C2 answer, not against 32.*

### D2 (4)

**(a) (2)** There is no line to delete because **the destructor is called by the language at scope
exit, not by a statement in `main`.** Cleanup is a property of the type, not of the call site.

**(b) (2)** Eliminated: **forgetting to release**, on every path including early returns and (from
Week 9) exceptions. **Not eliminated:** everything else. The class still calls `new[]`/`delete[]` by
hand, so it can still leak inside `push`, still mismatch `delete`/`delete[]`, and — as Lecture 02 §6
showed and PS 0 Part E demonstrated — **still double-free if it is copied**, because the compiler
generated a shallow copy constructor.

*Marking: (a) 2, must name the destructor and scope exit. (b) 2 — **1 for what was eliminated, 1 for a
concrete surviving bug.** "C++ is memory-safe now" scores 0 for (b) and is worth correcting out loud;
it is the misconception this lab is most likely to create.*

---

## Checkoff Checklist

1. Part A run **first**, all six tools, gaps reported.
2. `stack.c` unmodified.
3. `main` in `stack.cpp` contains **no cleanup call**.
4. Sanitizer transcript present, not just the `-O2` build.
5. D2(b) names a memory bug that **survives** the port.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 8 |
| B | 16 |
| C | 8 |
| D | 8 |
| **Total** | **40** |

---

## Note for the Lab

The line worth saying out loud, once, at the end:

> **The port bought nothing at runtime.** Same output, same speed, same memory. What changed is that
> the C version frees its buffer because `main` remembers to, and the C++ version frees it because an
> `IntStack` cannot exist without eventually being destroyed.

Students consistently expect the answer to be about syntax or performance. It is neither.
**Correctness moved out of the caller and into the type**, and that is the only thing that happened.

Then immediately undercut it with D2(b), because the opposite misconception is worse: this class is
still one copy away from a double-free, and they will see exactly that in PS 0 Part E over the
weekend. **Week 1 opens on it.**

---

*PROG 102 · Week 0 · Lab 0 Solutions · © CSE Department*
