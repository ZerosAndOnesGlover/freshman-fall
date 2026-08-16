# PROG 102 · Lecture 28
## Exceptions and Stack Unwinding

**Week 9 · Tuesday · 50 minutes**
**Reading:** *C++ Primer* §5.6, Ch. 18.1 · **Reference:** Meyers Item 8 (destructors and exceptions)
**Assumes:** Week 5 (RAII), Week 1 (copy-and-swap)

**Date:** Tuesday 16 March 2027 · 10:00–10:50 · Week 9

---

## 1. The Problem With Return Codes

You wrote this in PROG 101:

```c
int result = do_something();
if (result != 0) { /* handle it */ }
```

It works, and it has three well-known failures:

- **It can be ignored.** `do_something();` compiles, and the error vanishes.
- **It cannot cross a constructor.** A constructor has no return value, so a C-style class needs a
  separate `init()` returning a code — which is the problem Lecture 02 §1 opened with.
- **It muddles the two paths.** The code that does the work and the code that handles failure are
  interleaved, and the common case is the one that gets harder to read.

Exceptions separate them: the normal path reads normally, and failure travels up to whoever can deal
with it.

```cpp
double divide(double a, double b) {
    if (b == 0) throw std::domain_error("division by zero");
    return a / b;
}
```

---

## 2. Stack Unwinding

When a `throw` happens, control leaves the function immediately and the runtime walks back up the call
stack looking for a matching `catch`. **On the way, it destroys every automatic object** in each frame
it leaves. That walk is **stack unwinding**.

```cpp
void deep()   { Noisy c("deep");   throw std::runtime_error("boom"); }
void middle() { Noisy b("middle"); deep(); }
void outer()  { Noisy a("outer");  middle(); }
```

```
+ outer
+ middle
+ deep
- deep
- middle
- outer
caught: boom
```

**Every destructor ran, innermost first**, and the code after the `deep()` call in `middle` never
executed.

> **This is the entire mechanism behind RAII's usefulness**, and Week 5 stated it without proof.
> A destructor is your only guaranteed cleanup hook, because it is the only thing the language runs on
> the way out of a frame it is abandoning.

### 2.1 What Unwinding Does *Not* Clean Up

```cpp
try { int* p = new int[100]; throw std::runtime_error("x"); }
catch (const std::exception&) { /* p is gone; the array is not */ }
```

```
Direct leak of 400 byte(s) in 1 object(s)
```

**Unwinding destroys objects, not allocations.** The pointer `p` was an automatic object and was
destroyed; the 400 bytes it pointed at were not, because a raw pointer's destructor does nothing.

The same code with `unique_ptr`:

```
+ owned-by-unique_ptr
- owned-by-unique_ptr
caught -- and the Noisy above was destroyed
```

> **This is why Week 5 §L16 §5.3 measured `unique_ptr` as "cheaper than free".** The exception
> landing pads it generates are the machinery that makes this work, and the raw version's missing
> cleanup is not a hypothetical.
>
> **Every naked `new` is a leak waiting for the next exception**, including exceptions thrown by code
> you did not write.

---

## 3. `try`, `catch`, `throw`

```cpp
try {
    risky();
}
catch (const std::out_of_range& e) { /* most specific first */ }
catch (const std::exception& e)    { std::printf("%s", e.what()); }
catch (...)                        { /* anything at all */ }
```

**Rules worth memorising:**

- **Catch by `const` reference.** Catching by value **slices** (L15 §3) — a `std::out_of_range` caught
  as `catch (std::exception e)` loses everything derived. This is Week 4's slicing bug in its most
  damaging location.
- **Order matters.** The first matching handler wins, so derived types must come before their bases.
  Reverse them and the derived handler is unreachable — GCC warns.
- **`catch (...)` catches everything** and tells you nothing. Use it to clean up and rethrow with a
  bare `throw;`, not to swallow.
- **Rethrow with `throw;`, not `throw e;`.** The bare form preserves the original type; `throw e;`
  slices it.

---

## 4. The `std::exception` Hierarchy

```
std::exception
├── std::logic_error          — a bug: the caller violated a precondition
│   ├── std::invalid_argument
│   ├── std::domain_error
│   ├── std::length_error
│   └── std::out_of_range
├── std::runtime_error        — a condition detectable only at run time
│   ├── std::range_error
│   ├── std::overflow_error
│   └── std::underflow_error
└── std::bad_alloc, std::bad_cast, ...
```

Verified:

```
caught as logic_error:   index          // threw std::out_of_range
caught as exception:     std::bad_alloc // threw std::bad_alloc
```

**A handler catches the type and everything derived from it**, which is why `catch (const
std::exception&)` is the sensible outermost net.

### 4.1 `logic_error` vs `runtime_error`

The distinction is worth taking seriously because it tells the caller whose fault it is:

- **`logic_error`** — the program is wrong. An index out of range, an argument that violates a
  documented precondition. **In principle preventable by the caller.** Lecture 30 argues most of these
  should be assertions instead.
- **`runtime_error`** — the world is wrong. A file is missing, a socket closed, memory ran out.
  **Not preventable by inspection.**

### 4.2 Your Own Exception Types

```cpp
class ParseError : public std::runtime_error {
    std::size_t line_;
public:
    ParseError(std::string msg, std::size_t line)
        : std::runtime_error(std::move(msg)), line_(line) {}
    std::size_t line() const noexcept { return line_; }
};
```

**Derive from `std::runtime_error` or `std::logic_error`**, not from `std::exception` directly — you
get `what()` for free, and callers with an existing `catch (const std::exception&)` keep working.

**Define your own when the handler needs data**, as `line()` does here. If the handler only needs a
message, `std::runtime_error` is enough.

---

## 5. What Exceptions Cost

"C++ exceptions are zero-cost" is the slogan. Here is what is actually true, measured on **identical
source** compiled with and without exception support.

### 5.1 Time, When Nothing Throws

| | ns per call |
| --- | --- |
| with exceptions | 1.53–1.66 |
| `-fno-exceptions` | 1.49–1.60 |

**Indistinguishable.** The modern implementation is *table-driven*: the compiler emits side tables
describing how to unwind each frame, and the normal path executes no extra instructions at all. There
is no flag to set, no cost per `try` block entered.

**This half of the slogan is true.**

### 5.2 Space, Always

| | text |
| --- | --- |
| with exceptions | **240 bytes** |
| `-fno-exceptions` | **88 bytes** |

**2.7× the code**, for a trivial function — the unwind tables. On a large binary the ratio is much
smaller, but it is never zero, and it is the reason embedded projects compile with `-fno-exceptions`.

**This half of the slogan is false.**

### 5.3 Time, When It Throws

**About 1.68 µs per throw** — roughly **a thousand times** a normal function call. Unwinding involves
consulting those tables, running destructors, and matching handler types, and none of it is fast.

> **So the honest version is: exceptions cost nothing in time on the path where nothing goes wrong,
> cost code size always, and cost about a microsecond when they fire.**
>
> **That pricing tells you what they are for.** A microsecond is nothing for a failure that happens
> once. It is catastrophic for one that happens per element. **Do not use exceptions for control flow**
> — not because it is inelegant, but because you have just seen the number.

### 5.4 A Benchmarking Note

The first version of §5.1 compared an exception-throwing function against an error-code function with
an out-parameter. It reported **1.5×** — and it was measuring two different APIs doing different work,
not the cost of exception support.

**The comparison that answers the question is the same source built two ways**, which is what §5.1 is.
*(Week 4 §L14 §5.1's three attempts, again.)*

---

## 6. Summary

| Idea | The point |
| --- | --- |
| Unwinding | Destroys automatic objects, innermost first — verified |
| It destroys **objects**, not allocations | A raw `new[]` leaked 400 bytes; `unique_ptr` did not |
| Catch by `const&` | By value **slices** |
| `throw;` not `throw e;` | The bare form preserves the type |
| `logic_error` vs `runtime_error` | Your fault vs the world's fault |
| Derive from `runtime_error` | Not from `exception` — you get `what()` |
| **Time, happy path** | 1.53–1.66 vs 1.49–1.60 ns — **free** |
| **Code size** | **240 vs 88 bytes — not free** |
| **Time, throwing** | **~1.68 µs**, ~1000× a call |
| Therefore | Failures, not control flow |

---

## 7. Exercises

**1.** Build the three-deep unwinding example and confirm destructors run innermost-first. **Then add a
`catch` in `middle` that rethrows with `throw;`** and report what changes.

**2.** Reproduce §2.1: leak an array by throwing past a raw `new[]`, and confirm with ASan. Then fix it
with `unique_ptr` and show the report disappears.

**3.** Catch a `std::out_of_range` **by value** as `std::exception`. Print `what()`. **Then catch it by
`const&`.** Report the difference and name the phenomenon.

**4.** Write two `catch` blocks in the wrong order — base before derived. **Paste the warning** and say
which handler becomes unreachable.

**5.** Reproduce §5.1 and §5.2: the same source with and without `-fno-exceptions`. **Report both the
times and the `size` output.** Which half of "zero-cost" does your data support?

**6.** Measure the cost of an actual throw over at least 100,000 throws. **Express it as a multiple of
a normal call**, using your own measurement of both.

**7.** Define a `ParseError` carrying a line number. Catch it as `std::exception`, then as
`ParseError`. **Show what the first handler cannot do.**

---

## 8. Next

**Lecture 29** answers the question this lecture has set up: an exception left your function halfway
through. **What is the object's state now?** There are exactly four answers, three of them have names,
and Lab 8's `publish()` provides the fourth.

---

*PROG 102 · Week 9 · Lecture 28 · © CSE Department*
