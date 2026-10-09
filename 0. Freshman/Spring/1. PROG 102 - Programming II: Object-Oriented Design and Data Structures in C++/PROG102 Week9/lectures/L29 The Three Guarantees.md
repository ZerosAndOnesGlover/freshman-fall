# PROG 102 · Lecture 29
## The Three Guarantees

*“There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies, and the other way is to make it so complicated that there are no obvious deficiencies. The first method is far more difficult.”* — C. A. R. Hoare, "The Emperor's Old Clothes" (Turing Award lecture, 1980)

**Week 9 · Wednesday · 50 minutes**
**Reading:** Meyers, *Effective C++* Item 29 · **Reference:** Sutter, *Exceptional C++*
**Assumes:** L28, Week 1 (copy-and-swap), Week 5 (RAII)

**Date:** Wednesday 24 March 2027 · 10:00–10:50 · Week 9

**Coursework:** 📋 **Project 1** due Fri 26 Mar 17:00 · 📝 **PS 8** due Fri 26 Mar 17:00 · 📝 **PS 9** released Fri 26 Mar 10:00, due Fri 2 Apr 17:00 · 🔬 **Lab 9** Mon 29 Mar 15:00–16:50 · 📊 **Quiz 10** Tue 30 Mar 10:00–10:15 · 📘 **Midterm 2** Tue 30 Mar 18:00–19:30

---

## 1. The Question

An exception left your function halfway through. **What is the object's state now?**

"Exception-safe" is not an answer. There are four, and three of them have names.

| Guarantee | The promise |
| --- | --- |
| **Nothrow** | This operation will not throw. |
| **Strong** | It succeeds completely, or the state is exactly as it was. |
| **Basic** | The state may have changed, but the object is **valid** and **nothing leaked**. |
| *(none)* | Anything may have happened. |

**Every function you write provides one of these.** The only question is whether you know which, and
whether you wrote it down.

---

## 2. The Fourth One

Lab 8's event bus:

```cpp
void publish(const std::string& topic, const std::string& payload) {
    for (auto& sub : subscribers) sub.handler(payload);      // one of these throws
}
```

**What state is the bus in?** Some subscribers were notified and some were not. If the loop was also
pruning dead entries, the list is half-pruned. The exception escaped to a caller who has no way to know
how far it got.

**That is not basic, strong or nothrow. It is none of the three**, and it is where most code sits by
default — not through carelessness, but because *doing two things in sequence* is the natural way to
write a loop, and it has no guarantee unless you arrange one.

> **Naming this is the point of the lecture.** "It's not exception-safe" is a shrug. **"It provides no
> guarantee; a caller cannot know how many subscribers were notified"** is a defect report, and it
> suggests its own fix.

---

## 3. Basic

> **The object is valid, its invariants hold, and nothing leaked. Its value may have changed and you
> do not know to what.**

```cpp
struct BasicGuarantee {
    std::vector<Fragile> data;
    void add_all(const std::vector<Fragile>& xs) {
        for (const auto& x : xs) data.push_back(x);      // may throw part-way
    }
};
```

Measured — a container holding 2 items, appending 4 more, with the third copy throwing:

```
before: size=2
caught: copy failed
after : size=4   <- valid, but CHANGED
```

**The container is perfectly usable.** You can read it, add to it, destroy it — every invariant holds
and nothing leaked. **You just cannot say how many elements it has** without asking.

**This is the minimum acceptable guarantee**, and most of the standard library provides at least this
for everything.

> **Basic is achieved almost for free by RAII.** If every resource is owned by an object, unwinding
> releases everything and you cannot leak. The work in providing basic is making sure your *invariants*
> still hold — that a `size` member matches the actual contents, that a pointer is not dangling.

---

## 4. Strong

> **Commit or roll back. Either the operation completed, or nothing happened.**

```cpp
struct StrongGuarantee {
    std::vector<Fragile> data;
    void add_all(const std::vector<Fragile>& xs) {
        std::vector<Fragile> tmp = data;                 // 1. copy
        for (const auto& x : xs) tmp.push_back(x);       // 2. do the risky work on the copy
        data.swap(tmp);                                  // 3. commit -- cannot throw
    }
};
```

Identical scenario:

```
before: size=2
caught: copy failed
after : size=2   <- UNCHANGED
```

**The caller can retry, or give up, and either way the object is exactly as it was.**

### 4.1 The Recipe

**Do everything that can fail first, on a copy. Then commit with an operation that cannot fail.**

That is one sentence and it is the whole technique. The commit step is almost always `swap`, because
swapping pointers cannot throw — which is why L06 §3 insisted `swap` be `noexcept` and deferred the
reason to this week.

**You have written this before.** Copy-and-swap assignment (L06 §2) is exactly this recipe:

```cpp
Buffer& operator=(Buffer o) { swap(o); return *this; }
```

The copy happens in the parameter — before anything is modified. The swap commits. **You had the
strong guarantee in Week 1 and now you have its name.**

### 4.2 What It Costs

The copy. `add_all` above duplicates the entire container to append four elements — $O(n)$ work and
$O(n)$ memory for an operation that should be $O(k)$.

**That is why the standard library does not promise strong everywhere.** `std::vector::push_back` is
strong (it can roll back a single append), but `std::vector::insert` in the middle is only basic,
because guaranteeing strong would mean copying the vector on every insert.

> **Strong is not free and is not always right.** Offer it when the operation is rare and the rollback
> matters — assignment, a transaction, a configuration reload. **For an operation in a hot loop, basic
> is the honest choice**, and documenting it as basic is better than pretending.

---

## 5. Nothrow

> **This operation will not throw. Ever.**

Declared with `noexcept` (L30), and required of:

- **destructors** — the language assumes it, and Meyers Item 8 explains why a throwing destructor
  during unwinding calls `std::terminate`;
- **`swap`** — because it is the commit step of every strong-guarantee operation;
- **move constructors** — or containers will copy instead (L18 §5);
- **anything a strong-guarantee operation depends on for its commit.**

**Nothrow is achievable for exactly the operations that only shuffle existing resources.** Swapping
pointers, changing an integer, releasing memory. Anything that *acquires* — allocates, opens, connects
— cannot promise it.

---

## 6. How to Test for a Guarantee

**A claim about exception safety is testable, and if you have not tested it you do not know.**

The technique is an element type that throws on demand:

```cpp
struct Fragile {
    static int throw_on_copy;                       // 0 = never; n = throw on the n-th copy
    Fragile(const Fragile& o) : v(o.v) {
        if (throw_on_copy && --throw_on_copy == 0) throw std::runtime_error("copy failed");
    }
};
```

Then, for each operation, and for **each** *n*:

1. record the state;
2. arm the failure at copy *n*;
3. run the operation inside a `try`;
4. check what you claimed:
   - **strong** → the state equals the recorded state;
   - **basic** → the object is valid, invariants hold, and a leak checker is silent;
   - **nothrow** → no exception escaped at all.

**Sweeping *n* across every failure point is the part people skip**, and it is where the bugs are — an
operation is usually strong for a failure in the first step and not in the third.

> **This is PS 9 and it is the week's real skill.** Anyone can write `try`/`catch`. Producing evidence
> that your container does what you claim under failure is what separates a documented guarantee from
> an aspiration.

---

## 7. What the Standard Library Promises

Worth knowing, because it is the model:

| Operation | Guarantee |
| --- | --- |
| `vector::push_back` | **Strong** |
| `vector::insert` (middle) | **Basic** |
| `vector::pop_back` | **Nothrow** |
| `vector::swap` | **Nothrow** |
| `vector::operator[]` | **Nothrow** (no check) |
| `vector::at` | **Strong** (throws, changes nothing) |
| Any op, if an element's copy/move throws | at least **Basic** |

**Every one of these is specified.** cppreference states the guarantee for each container operation,
and it is one of the most useful things on those pages.

> **Note `push_back` is strong and middle `insert` is not.** That is not an oversight — it is §4.2's
> cost being paid where it is affordable and declined where it is not.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| Four states, three names | Nothrow, strong, basic — and **none** |
| **None** is the default | Lab 8's `publish()`; any loop doing two things in sequence |
| **Basic** | Valid, no leaks, value unspecified. **Verified: size 2 → 4** |
| Basic is nearly free with RAII | The work is preserving invariants |
| **Strong** | Commit or rollback. **Verified: size 2 → 2** |
| The recipe | Risky work on a copy; commit with `swap` |
| You wrote it in Week 1 | Copy-and-swap *is* the strong guarantee |
| Strong costs a copy | Which is why `insert` is only basic |
| **Nothrow** | Only for operations that shuffle, never acquire |
| Testing it | A throw-on-demand element, swept across every failure point |

---

## 9. Exercises

**1.** Build the `Fragile` element type. Then take your Week 6 `List<T>` and determine, **by testing**,
which guarantee `push_back` provides. Sweep the failure point across every copy.

**2.** Reproduce §3 and §4: the same scenario against a basic and a strong `add_all`. **Report both
sizes** and confirm no leaks.

**3.** Take the basic version and upgrade it to strong. **Measure what it cost** — time and peak
memory — for an append of 4 elements to a container of 10,000.

**4.** Lab 8's `publish()` provides no guarantee. **Give it the basic guarantee** and say what you had
to decide about the throwing handler.

**5.** Then try to give it the **strong** guarantee. *(This is harder than it looks — the handlers have
already had side effects.)* **Report whether you could, and why.**

**6.** Look up `std::vector::insert` on cppreference and quote its exception-safety clause. **Explain
why it is not strong**, in terms of §4.2.

**7.** Write an operation that is strong for a failure in its first step and only basic for a failure in
its third. **Demonstrate both** by sweeping the failure point.

---

## 10. Next

**Lecture 30** covers `noexcept` — what it promises, where the library depends on it, and what happens
when you lie — and then the question this week has been circling: **when should a failure be an
exception at all, and when should it be an assertion?**

---

*PROG 102 · Week 9 · Lecture 29 · © CSE Department*
