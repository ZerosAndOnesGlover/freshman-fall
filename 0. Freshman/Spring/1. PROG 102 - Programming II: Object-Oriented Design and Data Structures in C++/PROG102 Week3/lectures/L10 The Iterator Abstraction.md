# PROG 102 · Lecture 10
## The Iterator Abstraction

**Week 3 · Monday · 50 minutes**
**Reading:** *C++ Primer* §3.4, §9.2.1, Ch. 10 intro · **Reference:** Stroustrup Ch. 33
**Assumes:** Week 2 entire — templates are the mechanism this lecture is built on

---

## 1. The Problem the STL Solves

You have $C$ containers and $A$ algorithms. Sorting a vector, sorting a list, sorting an array;
searching each of them; reversing each of them.

**Written directly, that is $C \times A$ functions.** Ten containers and a hundred algorithms is a
thousand functions, each maintained separately, each a place for a bug.

The STL has about **15 containers and 100 algorithms**, and does not have 1,500 functions. It has
$C + A$, because of one idea in between.

---

## 2. An Iterator Is Not a Type

**An iterator is anything that behaves like a pointer.**

That is not an analogy. Think about what a pointer into an array can do:

```c
int a[5] = {1,2,3,4,5};
int* p = a;        /* point at the first  */
*p;                /* read what it points at */
++p;               /* move to the next    */
p != a + 5;        /* compare with the end */
```

Four operations: **dereference, advance, compare, and a notion of "one past the end"**. Every loop you
wrote in PROG 101 used exactly these.

The STL's move is to say: *those four operations are the interface.* Anything providing them can be
used by any algorithm written against them — and a pointer into a `std::list` node can provide them
just as well as a pointer into an array.

```cpp
std::vector<int> v{1,2,3};
for (auto it = v.begin(); it != v.end(); ++it) std::printf("%d ", *it);
```

`it` is not a pointer. It is an object of type `std::vector<int>::iterator` with `operator*`,
`operator++` and `operator!=` — which you now know how to write, because that was Week 1.

> **This is why Week 1 and Week 2 came first.** An iterator is a class with overloaded operators
> (Week 1), generated per container by a template (Week 2). The STL is not a new language feature. It
> is the two you already have, used well.

### 2.1 Half-Open Ranges

Every STL range is `[begin, end)` — **`end` is one past the last element**, and dereferencing it is
undefined.

This convention is not arbitrary. It gives you three properties for free:

- **An empty range is `begin == end`.** No special case.
- **The size is `end - begin`.** No off-by-one.
- **Splitting a range at `mid` gives `[begin, mid)` and `[mid, end)`** with no element lost or
  duplicated.

C arrays already worked this way — `a + 5` for a five-element array is a valid pointer you may compare
but not dereference. The STL made the convention universal.

---

## 3. Iterator Categories

Not every container can support every operation. A `std::list` node has a pointer to the next node, so
`++` is easy — but `it + 500` would mean following 500 pointers, and offering it would hide that cost
behind syntax that looks like $O(1)$.

So iterators come in **categories**, each a superset of the previous:

| Category | Adds | Provided by |
| --- | --- | --- |
| **Input** | `*` (read), `++`, `==` | streams |
| **Forward** | multi-pass — you may re-traverse | `forward_list`, `unordered_*` |
| **Bidirectional** | `--` | **`list`, `set`, `map`** |
| **Random access** | `+ n`, `- n`, `it2 - it1`, `<`, `[]` | **`vector`, `deque`, arrays** |

Measured, by inspecting `std::iterator_traits`:

```
vector : random access
deque  : random access
list   : bidirectional
set    : bidirectional
map    : bidirectional
```

**The category is a promise about cost, not merely about syntax.** Random access means `it + n` is
$O(1)$. A list *could* provide `+` by looping; it deliberately does not, because then
`std::sort` would compile and run in $O(n^2 \log n)$ while looking correct.

> **This is the single best piece of interface design in the standard library**, and it is worth
> stating as a principle: **an operation your data structure cannot do efficiently should be absent,
> not slow.** Week 6 asks you to apply it.

---

## 4. What This Buys: One Algorithm, Every Container

```cpp
std::vector<int> v{5,3,8,1,9,2};
std::list<int>   l{5,3,8,1,9,2};

std::accumulate(v.begin(), v.end(), 0);      // 28
std::accumulate(l.begin(), l.end(), 0);      // 28
*std::max_element(l.begin(), l.end());       // 9
std::count_if(v.begin(), v.end(), [](int x){ return x % 2 == 0; });   // 2
```

Verified — all four produce the values shown. `accumulate` was written once and works on both, because
it needs only **input** iterators: read, advance, compare.

`std::find` needs input iterators too. `std::reverse` needs bidirectional. `std::sort` needs random
access.

**You can predict whether an algorithm compiles for a container by comparing two categories**, without
reading either implementation. That is what the abstraction bought.

---

## 5. When the Contract Is Broken

```cpp
std::list<int> l{3,1,2};
std::sort(l.begin(), l.end());
```

This does not compile. **25 lines of error**, and the one that matters is:

```
/usr/include/c++/13/bits/stl_algo.h:1948:50: error: no match for 'operator-'
    (operand types are 'std::_List_iterator<int>' and 'std::_List_iterator<int>')
```

Read it against §3. `std::sort` needs random access. Random access includes `it2 - it1` — the distance
between two iterators, which `sort` needs to pick a pivot and to decide when a range is small enough
for insertion sort. **A list iterator has no `operator-`**, so the instantiation fails.

The error names the exact missing operation. It is buried in `stl_algo.h`, and finding it is precisely
the skill from **Week 2 §L09 §5**: read the first error, look for the line naming a type you recognise.

### 5.1 The Fix, and What It Tells You

```cpp
l.sort();          // member function -- works
```

`std::list` provides its own `sort` as a **member**, because sorting a linked list is a genuinely
different algorithm: you relink nodes instead of moving values, and a merge sort on pointers is
$O(n \log n)$ with no random access needed.

> **When a container provides a member function that duplicates an algorithm name, use the member.**
> It exists because the generic version is either impossible or worse. The other examples:
> `list::remove`, `map::find`, `set::count`, `unordered_map::find`. **`std::find` on a `std::map` is
> $O(n)$; `m.find(k)` is $O(\log n)$** — the generic algorithm cannot know the container is sorted.

---

## 6. `begin`, `end`, and `const`

Every container provides:

```cpp
c.begin();   c.end();      // iterator        -- may modify elements
c.cbegin();  c.cend();     // const_iterator  -- may not
```

and on a `const` container, `begin()` returns a `const_iterator` anyway. This is Lecture 03's
`const`-correctness reappearing: a `const std::vector<int>&` parameter gives you `const_iterator`s, so
an algorithm that tries to write through them will not compile.

**Prefer `cbegin()`/`cend()` when you are only reading.** It documents intent and it lets the compiler
catch an accidental write.

### 6.1 Range-Based `for` Is Iterators

```cpp
for (int x : v) { ... }
```

is, near enough:

```cpp
for (auto it = v.begin(), e = v.end(); it != e; ++it) { int x = *it; ... }
```

Which is why **anything with `begin()` and `end()` works with range-`for`** — including the container
you write in Week 6, and including plain C arrays.

Recall Lecture 00 §10's three forms. Now they have a reason:

| Form | What it does |
| --- | --- |
| `for (T x : c)` | copies each element — `int x = *it` |
| `for (T& x : c)` | binds a reference — may modify |
| `for (const T& x : c)` | binds a `const` reference. **The default choice** |

---

## 7. Iterators Are Not Only for Containers

Two examples worth knowing, because they show the abstraction is not container-specific.

**Stream iterators** turn input into a range:

```cpp
std::vector<int> nums{std::istream_iterator<int>(std::cin),
                      std::istream_iterator<int>()};
```

**Insert iterators** turn assignment into insertion:

```cpp
std::copy(src.begin(), src.end(), std::back_inserter(dest));
```

`back_inserter(dest)` returns an object whose `operator=` calls `dest.push_back`. It is an "iterator"
that writes rather than reads, and `std::copy` cannot tell the difference.

> **This is the abstraction paying off in a way its designers had to work for.** `std::copy` was
> written for pointers, and it works on network input and on growing containers, because both were
> made to satisfy the same four operations.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| $C \times A$ becomes $C + A$ | The reason the STL is small |
| An iterator is an **interface**, not a type | `*`, `++`, `==`, and one-past-the-end |
| Half-open `[begin, end)` | Empty is `begin == end`; size is `end - begin` |
| Categories | input ⊂ forward ⊂ bidirectional ⊂ random access |
| Measured | `vector`/`deque` random access; `list`/`set`/`map` bidirectional |
| Categories promise **cost** | An inefficient operation is absent, not slow |
| `std::sort` on a `list` | Fails on `operator-` — the contract, made visible |
| Member beats generic when it exists | `l.sort()`, `m.find()` — the container knows more |
| `cbegin`/`cend` | `const`-correctness from L03, applied to traversal |
| Range-`for` is iterators | So it works on anything with `begin()` and `end()` |
| Stream and insert iterators | The abstraction is not about containers |

---

## 9. Exercises

**1.** Print the iterator category of `vector`, `deque`, `list`, `set` and `forward_list` using
`std::iterator_traits`. **Predict each before running.**

**2.** Call `std::sort` on a `std::list` and paste the error. **Quote the line naming the missing
operation**, and say why `sort` needs it.

**3.** `std::reverse` needs bidirectional iterators. Predict whether it compiles for `vector`, `list`,
`set` and `forward_list`. **Verify all four.** One of them will surprise you — explain it.

**4.** Write a function `template <class It> auto total(It first, It last)` that sums a range. Call it
with a `vector`, a `list`, and a plain C array. **What is the weakest iterator category it requires?**

**5.** Use `std::back_inserter` to copy a `list` into an empty `vector`. Then do it without
`back_inserter` and explain what goes wrong.

**6.** `std::find` on a `std::set` is $O(n)$; `s.find()` is $O(\log n)$. **Measure both** on 100,000
elements and report the ratio. Why can the generic algorithm not do better?

**7.** Write a range-`for` over a plain C array `int a[5]`. It works. **Explain why**, in terms of §6.1.

---

## 10. Next

**Lecture 11** is the containers themselves: what each one is, what it costs, and how to choose. It
ends with a measurement where the complexity table gives the wrong answer by a factor of 178.

---

*PROG 102 · Week 3 · Lecture 10 · © CSE Department*
