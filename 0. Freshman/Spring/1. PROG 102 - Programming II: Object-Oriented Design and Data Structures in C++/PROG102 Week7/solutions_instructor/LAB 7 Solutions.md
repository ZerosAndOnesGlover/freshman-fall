# PROG 102 · Lab 7 — Solutions and Checkoff Notes
## Refactoring a Messy Hierarchy

**INSTRUCTOR / TA COPY — not for distribution**

---

## Before the Session

**This is the first lab with no measurement**, and students will notice. Say so at the start and say
what replaces it: a countable argument (Part A), a behavioural equivalence proof (Part C), and an
honest assessment (Part D).

**Distribute `notify.hpp` and `notify_demo.cpp` unmodified.** Confirm in front of the room that it
builds clean and produces correct output. **Say that it is not broken** — this is the first lab
artifact that is *working code*, and the exercise is improvement rather than repair.

**Budget:** A 25 min, B 50 min, C 15 min, D 20 min, 10 min slack. **Part D is worth only 4 points and
is the point of the lab** — protect the time for it.

**Watch for the two failure modes:**

1. Students who rewrite from scratch without reading the original. They will produce something that
   works and cannot answer A2 or D2.
2. Students who "refactor" by deleting the combination classes and leaving `make()` returning a raw
   pointer. **Part B2 explicitly requires `unique_ptr`.**

---

## Part A — Diagnose (12)

### A1 (4)

10 classes today. The arithmetic:

| features | $2^n$ | × 3 transports |
| --- | --- | --- |
| 3 | 8 | 24 |
| 4 | 16 | 48 |
| 5 | 32 | 96 |

*Marking: 4. Full marks require the working, not just the numbers.*

### A2 (4)

Expected, any three:

- **Class count grows as $2^n$** in features.
- **Combinations are fixed at compile time** — the set of behaviours is chosen by a class name, so a
  config file cannot request one that nobody anticipated.
- **`make()` returns a raw owning pointer** — the caller must `delete`, and nothing says so
  (Week 5 §L16 §6).
- **`make()` returns `nullptr`** for an unknown config, so a typo becomes a null dereference rather
  than an error.
- **Duplicated logic** — the `"[12:00] "` prefix appears in four classes; changing the format means
  finding all four.

*Marking: 4, with **at least one about ownership** as the sheet requires. A student listing three
class-count variations gets 2.*

### A3 (4)

**(a)** It does not say whether the caller owns the result. There is no way to tell from the signature
that a `delete` is required, and no way for the compiler to check.

**(b)** An unrecognised config returns `nullptr`; the demo calls `n->send(...)` on it. **A typo in a
config string becomes a null dereference at run time**, with no diagnostic.

*Marking: 2 + 2. **(b) must trace it to the caller's dereference** — "it returns null" alone is 1.*

---

## Part B — Refactor (18)

### B1 (10), B2 (4)

```cpp
struct Decorator : Notifier {
    std::unique_ptr<Notifier> inner;
    explicit Decorator(std::unique_ptr<Notifier> n) : inner(std::move(n)) {}
};
struct Timestamped : Decorator { using Decorator::Decorator;
    void send(const std::string& m) const override { inner->send("[12:00] " + m); } };
```

with `make()` parsing the config and wrapping in reverse order.

*Marking B1: 4 the Decorator base with `unique_ptr`, 3 the three features, 3 no raw `new`/`delete`.*
*Marking B2: 4 for `unique_ptr` return **and** config parsing rather than a lookup of pre-built
combinations.*

**A `make()` that maps `"ts+enc"` to a hard-coded pair of wraps has missed the point** — it is the same
$2^n$ table in a different shape. Deduct 2 and show them the parse.

**Wrapping order:** the config reads outermost-first, so the parse must wrap in **reverse**. Students
who wrap forwards get `ENC(ZIP(...))` where the original gave `ZIP(ENC(...))` and will fail Part C.
**That is a good failure** — it is caught by the diff, which is what Part C is for.

### B3 (4)

Adding a fourth feature: **one class, roughly four lines**, plus one registry entry.

The original would have needed **eight** new combination classes (going from 8 to 16), plus updating
`make()`.

*Marking: 4 for both counts.*

---

## Part C — Verify (6)

### C1 (4)

```
plain         console: hello
ts            console: [12:00] hello
enc           console: ENC(hello)
zip           console: ZIP(hello)
ts+enc        console: ENC([12:00] hello)
ts+enc+zip    console: ZIP(ENC([12:00] hello))
```

`diff` of the two programs' output is empty.

*Marking: 4. **Require the diff**, not a claim. This is the only objective check in the lab and it is
where the wrapping-order bug surfaces.*

### C2 (2)

Sanitizer-clean; zero `delete` in the caller.

*Marking: 1 + 1.*

---

## Part D — Judgement (4)

### D1 (2)

**10 classes before, 8 after.** At three features the improvement is marginal.

**The count is the wrong measure because it is a point on a curve.** The original grows as $2^n$ and
the refactored as $n$; at n = 3 the curves have barely separated. Adding a fourth feature takes the
original to 18 and the refactored to 9.

*Marking: 1 the honest numbers, 1 the derivative argument. **A student who reports the refactor as a
big win at n = 3 has not counted** — send them back to count.*

### D2 (2)

**There is a real answer and "never" earns nothing.** Acceptable:

- **The set of combinations is genuinely closed and small**, and each combination has genuinely
  *different* logic rather than composed logic. Then the explicit classes are clearer and the decorator
  indirection buys nothing.
- **The combinations are not independent** — if `Encrypted` and `Compressed` must interact (compress
  *then* encrypt, never the reverse, with a shared header), composing them independently is wrong and
  a class per valid combination is honest about that.
- **Debuggability at n = 2.** Two features, four classes, flat stack traces, no chain to walk.

*Marking: 2 for any argued case. **"Never" or an unargued answer: 0.***

---

## Checkoff Checklist

1. Original built and run **before** any changes.
2. A2 includes an ownership problem.
3. `make()` **parses** the config; it does not select a pre-built combination.
4. `diff` of both programs' output is empty.
5. Zero `delete` in the caller.
6. D1 reports **10 → 8** honestly.

---

## Marking Summary

| Part | Points |
| --- | --- |
| A | 12 |
| B | 18 |
| C | 6 |
| D | 4 |
| **Total** | **40** |

---

## Note for the Lab

Close on D1, and do not oversell it.

> **You took 10 classes to 8.** If that is all you had been shown, you would reasonably ask what the
> fuss was about.

Then the actual argument:

> **The win is not the count. It is the derivative.** Add a fourth feature: the original goes to 18 and
> yours goes to 9. The original grows exponentially and yours grows linearly, and at three features the
> two curves have barely separated.

And then the honest part, which is what D2 exists for:

> **That is the shape of most design arguments.** A better design usually looks marginal on today's
> requirements and decisive on next year's — **which is exactly why Lecture 22 insisted you name the
> change you expect.** If no fourth feature is ever coming, the code you were given was fine.

Finally, the point most students miss and which is worth thirty seconds out loud:

> **The class explosion was not even the worst problem in that file.** `make()` returned a raw owning
> pointer and returned `nullptr` for an unrecognised config — a leak the caller could not see and a
> crash waiting for a typo. **The pattern fixed the structure; `unique_ptr` fixed the bug**, and only
> one of those was this week's syllabus.

---

*PROG 102 · Week 7 · Lab 7 Solutions · © CSE Department*
