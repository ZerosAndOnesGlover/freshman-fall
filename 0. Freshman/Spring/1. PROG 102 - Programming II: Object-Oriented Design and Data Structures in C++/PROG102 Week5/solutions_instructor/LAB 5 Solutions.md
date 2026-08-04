# PROG 102 · Lab 5 — Solutions and Checkoff Notes
## Leak Detection with AddressSanitizer

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**Midterm 1 is this week.** This lab is deliberately lighter than Labs 2–4 and should finish inside the
session. **Do not let it run over** — students are revising, and a lab that spills into the evening is
a bad trade.

**Say two things at the start:**

1. **The faults are ordered.** Fixing one reveals the next. Work in order and record before fixing —
   a student who "fixes everything at once" from reading the code has skipped the lab and will not have
   the Part A transcripts.
2. **Part B is not "add the missing `delete`s".** It is "change the types so the `delete`s are not
   needed". A repaired file containing `delete` has missed the point, even if it is leak-free.

**Distribute `registry.cpp` unmodified.** Confirm in front of the room that it compiles silently:

```
g++ -std=c++17 -Wall -Wextra -pedantic -c registry.cpp -o /dev/null
```

Then say: *five memory faults, no warnings.*

**Budget:** A 35 min, B 45 min, C 20 min, 20 min slack.

---

## The Five Faults

| # | Fault | Where | Surfaces as |
| --- | --- | --- | --- |
| 5 | `delete dup;` twice | `main` | `heap-use-after-free` |
| 1 | `delete banner` for a `new[]` | `~Registry` | `alloc-dealloc-mismatch` |
| 2 | sessions never deleted | `~Registry` | leak |
| 3 | `close()` erases the pointer without deleting | `Registry::close` | leak |
| 4 | `make_orphan` returns a raw owning pointer | free function | leak |

**Faults 2, 3 and 4 are the same fault three times:** a raw pointer that owns something, with no type
saying so. That is the observation Part C wants.

---

## Part A — Find Them (14)

### A1 (3)

```
ERROR: AddressSanitizer: heap-use-after-free
    ... in Session::~Session()  registry.cpp:11
```

The double `delete dup;` runs `~Session` twice; the second `delete[] user` reads a freed pointer.

*Marking: 2 transcript, 1 naming the line in `main`. **The error names `~Session`, not `main`** — a
student who reports the destructor as the bug has read the message but not the cause; give 2 and
explain.*

### A2 (3)

```
ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete)
```

The disagreeing functions: `new char[64]` in the constructor and `delete banner` in the destructor.

*Marking: 2 transcript, 1 naming both.*

### A3 (4)

```
Direct leak of 16 byte(s) in 1 object(s)   (x3)
SUMMARY: AddressSanitizer: 65 byte(s) leaked in 6 allocations.
```

**65 bytes = three `Session` objects at 16 bytes (48) + their strings: `"ada"` 4, `"grace"` 6,
`"orphan"` 7 = 17.** Six allocations: three objects, three strings.

*Marking: 2 the figures, 2 the accounting. **The accounting is the assessed half** — it requires
understanding that each `Session` is two allocations.*

### A4 (4)

- **destructor**: `~Registry` deletes `banner` but never the `Session*`s in the vector.
- **`close()`**: erases the pointer from the vector without deleting the object — the vector forgets it
  and nothing else remembers it.
- **`make_orphan`**: returns `Session*`. **The signature does not say the caller owns it**, so the
  caller has no way to know it must delete, and does not.

*Marking: 1 each plus 1 for the third being a **signature** problem rather than a missing `delete`. The
sheet flags this; a student who writes "the caller forgot to delete" has the symptom, not the fault —
give 3 of the 4.*

---

## Part B — Repair by Retyping (18)

### B1 (6)

```cpp
struct Session { std::string user; int id;
    Session(std::string u, int i) : user(std::move(u)), id(i) {} };
```

**Zero of the five.** `std::string` manages itself, so the compiler-generated destructor, copy and move
operations are all correct — **the Rule of Zero**.

*Marking: 4 the rewrite, 2 the answer "none, by the Rule of Zero". A student who keeps a hand-written
destructor loses 2 and should be asked what it is for.*

### B2 (6)

```cpp
std::vector<std::unique_ptr<Session>> sessions;
std::string banner;
void close(int i) {
    sessions.erase(std::remove_if(sessions.begin(), sessions.end(),
        [i](const auto& s){ return s->id == i; }), sessions.end());
}
```

Erasing now destroys, because the vector owns `unique_ptr`s and destroying one deletes the `Session`.

*Marking: 4 both members retyped, 2 demonstrating that `close()` destroys. **Accept an index loop
instead of erase-remove** — Week 3's idiom is nice but not required here.*

### B3 (6)

```cpp
std::unique_ptr<Session> make_orphan();   // signature now says "yours"
Session* find(int i);                     // or Session& / std::optional
```

**`find()` must not return `unique_ptr`** — that would transfer ownership out of the registry, which
still needs the session. A raw pointer (nullable, non-owning) is correct here, and this is the
legitimate use of a raw pointer that L17 §7 item 3 describes.

*Marking: 3 `make_orphan`, 3 `find` **with the reason `unique_ptr` is wrong**. This is the assessed
half — the lab has spent 90 minutes saying "raw pointers bad", and the answer here is that a raw
*non-owning* pointer is exactly right. A student who returns `unique_ptr` from `find` gets 1.*

**The repaired file must contain no `new`, no `delete`, no user-declared destructor.**

---

## Part C — Compare With Lab 1 (8)

### C1 (4)

Lab 1's `Roster` repair: a deep copy constructor, a `noexcept` swap, a copy-swap `operator=`, and a
corrected destructor — roughly **25–30 lines**, and **4 of the 5** special members.

Lab 5's `Registry` repair: **three member declarations changed**, and **0 of the 5**.

*Marking: 4 for both counts with the special-member tally.*

### C2 (4)

**(a) (2)** `Registry`. It became possible because every member now manages its own resource —
`std::string`, `std::vector`, `unique_ptr` — so the generated special members are correct.

**(b) (2)** **Accept any argued position.** The expected answer is *no*: you cannot recognise when the
Rule of Zero does not apply unless you have written the code it replaces, and Week 6 is precisely that
case. But a student arguing that the ordering could be reversed, with reasons, has engaged with the
question and should get both marks.

*Marking: 2 + 2. **Award nothing for "yes it was a waste" with no argument**, and full marks for a
well-argued version of the same view.*

---

## Checkoff Checklist

1. Part A transcripts **in order**, one fault at a time.
2. A3 accounts for the 65 bytes.
3. Repaired file has **no `new`, no `delete`, no destructor**.
4. `find()` returns a non-owning pointer or reference, **not** `unique_ptr`.
5. C1 gives both line counts.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 14 |
| B | 18 |
| C | 8 |
| **Total** | **40** |

---

## Note for the Lab

The closing point is the comparison, and it should be made carefully because the glib version is wrong.

> **In Lab 1 you fixed four bugs with thirty lines of careful code. Today you fixed five with three
> declarations.**

The glib conclusion is "so always use the library types". The accurate one has two halves:

**First**, those three declarations *are* Lab 1's repair — written once, by people who got it right,
and reused. `std::string`'s copy constructor is the deep copy you wrote. `unique_ptr`'s deleted copy
constructor is the double-free you watched. **You did not skip the work; you inherited it.**

**Second, and the part worth the last five minutes:** you can now tell when it does not apply. B3's
`find()` is the small version — after ninety minutes of "raw owning pointers are the enemy", the
correct return type is a **raw pointer**, because non-owning is a real and useful thing to be.

**Week 6 is the large version.** They will build a linked list, and there is no library type to inherit
the work from, because *they are writing the library type.* The Rule of Zero applies to code that uses
resources. Week 6 is code that provides them.

Say that on the way out — it prevents a week of students trying to build a linked list out of
`std::vector`.

---

*PROG 102 · Week 5 · Lab 5 Solutions · © CSE Department*
