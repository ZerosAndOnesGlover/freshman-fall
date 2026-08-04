# PROG 102 · Problem Set 7 — Solutions and Marking Notes
## Factory Method and Decorator

**INSTRUCTOR COPY — not for distribution**

---

## Before Marking

**Reference environment:** g++ 13.3.0, x86-64 Linux. Class counts and the $2^n$ table are exact;
timings are not.

**This set is largely marked on argument**, which makes it slower to mark and easier to mark
inconsistently. **Parts A3, B4, C3 and all of D are prose**, and the rubric below gives the substance
expected rather than the words.

**Be generous where a student argues a defensible position well and strict where they assert without
argument.** D3 in particular is marked on the quality of the case *against* their own view.

---

## Part A — Factory Method (24)

### A1 (8)

```cpp
std::unique_ptr<Shape> make_shape(const std::string& kind, double dim) {
    if (kind == "circle") return std::make_unique<Circle>(dim);
    ...
    throw std::invalid_argument("unknown shape: " + kind);
}
```

**The return type says three things:** you own it; the concrete type is hidden; you cannot leak it.

*Marking: 5 the factory with three shapes and the throw, 3 the three promises. **All three required for
full marks** — most students give ownership and forget type-hiding.*

### A2 (6)

Adding a shape: a new class, plus **one line** in the factory. **Zero call sites.**

*Marking: 3 the counts, 3 the sentence. The sentence must be about call sites being untouched.*

### A3 (6) — the assessed question

Expected substance:

> L15 objected to a type-switch **scattered across the codebase**, where adding a type means finding
> and editing every chain. This is **one** switch, at the boundary where external input becomes
> concrete types. That mapping must exist somewhere; confining it to a single function is precisely
> what makes every other site type-agnostic.

*Marking: 6. **The distinction between one boundary switch and many scattered ones is the whole
answer.** "It's fine because it's a factory" is 2.*

### A4 (4)

A `std::map<std::string, std::function<std::unique_ptr<Shape>(double)>>`.

**Both answers earn full marks.** The `if`-chain is simpler and adequate for a closed set; the registry
is right when types are added by plugins or at run time.

*Marking: 3 working registry, 1 the judgement. **Deduct nothing for preferring the if-chain** if the
reason is "the set of shapes is closed" — that is the better answer for most programs.*

---

## Part B — Decorator (34)

### B1 (10)

Three decorators over one interface, composed with `unique_ptr` and `std::move`. Reference:

```
Buffered(Encrypted(Compressed(File(data.bin))))
buffered<decrypted<inflated<raw-bytes-of(data.bin)>>>
```

*Marking: 4 the interface and base, 4 three working decorators, 2 runtime composition with `std::move`.*

**A `Decorator` base holding the `unique_ptr` is expected but not required** — three independent
decorators each holding their own is equally correct.

### B2 (6)

Eight compositions printed, and:

| n | $2^n$ | $n$ |
| --- | --- | --- |
| 1 | 2 | 1 |
| 3 | 8 | 3 |
| 5 | 32 | 5 |
| 8 | 256 | 8 |
| 10 | **1024** | **10** |

*Marking: 3 the eight compositions, 3 the table with the subclass names written out. **The names
matter** — `BufferedEncryptedCompressedFileSource` makes the point in a way the number does not.*

### B3 (10)

Reference, 10⁷ calls:

| depth | per call |
| --- | --- |
| 0 | 2.06 ns |
| 1 | 2.41 ns |
| 2 | 2.98 ns |
| 4 | 4.14 ns |
| 8 | 6.70 ns |

**Marginal: $(6.70 - 2.06)/8 \approx 0.58$ ns per layer.**

**Why it is *below* Week 4's ~2 ns:** the targets in a decorator chain are perfectly predictable — the
same object, the same vtable entry, every iteration — so the branch predictor learns them and GCC
speculatively devirtualizes (L14 §6). Week 4's figure came from a benchmark controlled to defeat
exactly that.

*Marking: 5 the table with a marginal figure, 5 the comparison. **The comparison must invoke prediction
or devirtualization**; "it's just faster" is 1 of the 5. Accept a student whose marginal figure is
*higher* than 2 ns if they investigated and reported honestly.*

### B4 (8)

**(a) (4)** Runtime composition. The expected demonstration is building the chain from **data** — a
config string, a command-line flag — which the subclassing version cannot do at all without a switch
over $2^n$ cases.

**(b) (4)** Two disadvantages, at least one about debugging:

- **A stack trace through a deep chain is unreadable** — fourteen frames of `Decorator::read` and no
  indication of which layer is misbehaving.
- Identity is lost: the outermost object is not the one you created, so `dynamic_cast` to the concrete
  source fails, and pointer comparison does not work. *(This is the GoF's own "Consequences" note.)*
- Order matters and is invisible: `Encrypted(Compressed(x))` and `Compressed(Encrypted(x))` are both
  legal and only one is correct.

*Marking: 4 + 4. **(b) must include a debugging point** as the sheet requires. Any two of the above, or
anything equally concrete.*

---

## Part C — Singleton (22)

### C1 (6)

Five calls, one construction. Defeating it: without `= delete`, `Config c = Config::instance();`
copy-constructs a second.

*Marking: 4 the demonstration, 2 defeating it. **A student who says "you can't defeat it" has not tried
the copy** — that is the entire reason the deletion is there.*

### C2 (8)

```
16 threads raced to initialise a 50 ms constructor
constructions = 1
all threads got the same address: yes
```

```
__cxa_guard_acquire
__cxa_guard_release
__cxa_guard_abort
```

**Meaning:** the compiler emits a real lock around first-time initialization. The first caller takes
it; later callers test a flag and skip. **The thread safety is a language guarantee implemented by
runtime machinery, not an accident.**

*Marking: 4 the threading result, 4 the guard functions with an interpretation. **The interpretation
must say the compiler emits locking** — pasting the symbols without comment is 2 of the 4.*

### C3 (8)

**(a) (4)** Every function that touched `Config::instance()` now takes a `Config&` — and the list is
usually longer than the student expected, because the singleton was reachable from places that did not
advertise the dependency.

**(b) (4)** Expected substance:

> The signatures now **state the dependency**. You can see from a declaration whether a function uses
> configuration, you can pass a different `Config` in a test, and you can have two. What you gave up is
> convenience — the parameter has to be threaded through intermediate functions that do not use it
> themselves, which is a real cost and the honest reason people reach for singletons.

*Marking: 4 the list, 4 the trade. **Full marks require naming what was given up.** An answer that is
purely anti-singleton gets 2 — the threading-through cost is real and the question asks for it.*

---

## Part D — Judgement (20)

### D1 (8)

Acceptable answers include: **Adapter** (`std::stack`, `std::queue` over a container — but these were
named, so require others), **Strategy** (`std::sort`'s comparator; `unique_ptr`'s deleter),
**Template Method** (`std::sort` itself), **Facade** (`std::string`'s interface over a buffer),
**Factory** (`std::make_shared`, `std::make_unique`), **Type Erasure / Bridge** (`std::function`),
**Proxy** (`std::vector<bool>::reference` — a good answer connecting to Week 3), **Observer**
(nothing in the standard library; a student claiming one should be checked).

*Marking: 2 per pattern up to 6, plus 2 for the "what varies" sentences being accurate. **Reject
Iterator and `std::stack`** — the sheet excludes them.*

### D2 (6)

*Marking: 3 for a specific, plausible application; 3 for a specific case where a pattern would make it
worse. **Both must name a pattern and a class from their own code.** Generic answers get half.*

### D3 (6) — the assessed writing

The objection is easy: one implementation, no change in two years, an interface and a virtual call
bought nothing, and L22 §6.2's test fails.

**The case in favour is what is being marked.** Strong versions:

- **Testing.** An interface lets you substitute a fake shape in tests without linking the real one.
- **A known, dated requirement** — "we are adding polygons next quarter" — makes the option cheap now
  and expensive later.
- **Compilation firewall.** Callers depend on the interface header, so changing the concrete class does
  not recompile the world. In a large codebase this is a real, measurable benefit.
- **API boundary.** If this ships as a library, an interface preserves ABI stability across versions in
  a way a concrete class does not.

*Marking: 2 the objection, 4 the case in favour. **A straw man earns 0 of the 4.** The last two
bullets are the strong arguments and a student who finds either has done the exercise properly.*

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 24 |
| B | 34 |
| C | 22 |
| D | 20 |
| **Total** | **100** |

---

## What to Watch For

1. **"It's fine because it's a factory"** (A3) instead of the boundary argument.
2. **B3's marginal figure omitted** — students report totals and skip the subtraction.
3. **"It's just faster"** as the whole of B3's comparison.
4. **A purely anti-singleton answer to C3(b)** that never names the cost of dependency injection.
5. **A straw-man D3.** The most common failure in the set and the one worth feedback.

---

## Feeding Into Week 8

Week 8 is behavioural patterns and ends by showing that **Strategy and Command are nearly obsolete in
modern C++** — a lambda does both in one line.

**Set that up on Monday** using B3: students have just measured a decorator layer at 0.58 ns and seen
that indirection is cheap. Week 8's point is different — not that patterns are slow, but that **some of
them were working around the absence of a language feature that now exists.**

---

*PROG 102 · Week 7 · PS 7 Solutions · © CSE Department*
