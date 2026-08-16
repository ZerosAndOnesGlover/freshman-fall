# PROG 102 · Lecture 20
## Implementing Iterators

**Week 6 · Wednesday · 50 minutes**
**Reading:** *C++ Primer* §9.2.1, §10.5 · **Reference:** cppreference, *iterator_traits*
**Assumes:** L10 (iterator categories), L19, Week 2 (templates)

**Date:** Wednesday 24 February 2027 · 10:00–10:50 · Week 6

---

## 1. What Makes a Container a Container

Your `List<T>` from Lecture 19 stores things and gives them back. It is a data structure.

**It is not yet a container in the STL's sense**, because none of the hundred algorithms in
`<algorithm>` can touch it. This lecture fixes that, and the fix is about forty lines.

The goal, concretely:

```cpp
List<int> l{5,3,8,1,9};
std::accumulate(l.begin(), l.end(), 0);                              // 26
*std::max_element(l.begin(), l.end());                               // 9
std::count_if(l.begin(), l.end(), [](int x){ return x%2==0; });      // 1
std::reverse(l.begin(), l.end());
std::copy(l.begin(), l.end(), std::back_inserter(some_vector));
```

**All of that, on a container you wrote, with no changes to the algorithms.** That is the payoff of
Week 3's abstraction and it is worth doing once by hand.

---

## 2. The Operations

Lecture 10 §2 said an iterator is anything that behaves like a pointer. For a **bidirectional**
iterator, that is:

| Operation | Meaning |
| --- | --- |
| `*it` | the element |
| `it->m` | member access |
| `++it`, `it++` | advance |
| `--it`, `it--` | retreat |
| `it == other`, `it != other` | compare |
| copy, assign, default-construct | it is a value type |

For a list, all of these are one or two lines over a `Node*`:

```cpp
reference operator*()  const { return n->value; }
pointer   operator->() const { return &n->value; }
Iter& operator++()    { n = n->next; return *this; }
Iter  operator++(int) { Iter t = *this; n = n->next; return t; }
Iter& operator--()    { n = n->prev; return *this; }
bool operator==(const Iter& o) const { return n == o.n; }
```

> **The post-increment `operator++(int)` takes an unused `int` parameter.** That is the language's
> trick for distinguishing `++it` from `it++` — there is no other difference in the declaration. Note
> it returns a **copy of the old value**, which is why `++it` should be preferred in loops: `it++`
> constructs a temporary that is usually discarded.

---

## 3. The `iterator_traits` Protocol

Algorithms need to ask questions *about* your iterator: what does it point at? how far apart can two of
them be? what can it do?

They ask through `std::iterator_traits`, which by default reads five member typedefs:

```cpp
using iterator_category = std::bidirectional_iterator_tag;
using value_type        = T;
using difference_type   = std::ptrdiff_t;
using pointer           = T*;
using reference         = T&;
```

**Provide these five and your iterator is a first-class citizen.** Omit them and you get several
hundred lines of error from the first algorithm that tries.

Verified on the finished iterator:

```
our category is bidirectional? yes
value_type is int?             yes
reference is int&?             yes
std::list's category matches?  yes
```

**The last line is the one to notice.** Our iterator declares the same category as `std::list`'s, which
means every algorithm makes the same decisions about both.

### 3.1 The Category Is a Promise

`iterator_category` is a **tag type** — an empty struct whose only job is to be a distinct type that
overload resolution can dispatch on. That is how `std::distance` can be $O(1)$ for a vector and $O(n)$
for a list with no runtime check:

```cpp
std::distance(l.begin(), l.end());   // 3   -- walks, because we said bidirectional
std::advance(it, 2);                 // 2   -- loops, for the same reason
```

Both compiled to the linear version **because of the tag**, chosen at compile time. Declare
`random_access_iterator_tag` without providing `+` and `-` and you get a compile error; declare it and
*provide* them by looping, and you get silently quadratic algorithms.

> **The tag is a promise about cost, and lying about it is the worst thing you can do here** — it does
> not fail loudly, it just makes everything slow.

---

## 4. `const_iterator` Without Writing It Twice

A container needs two iterators: one that permits modification and one that does not (L10 §6). Writing
them separately means maintaining two nearly identical classes.

Parameterise on constness instead:

```cpp
template <bool Const>
class Iter {
    Node* n;
public:
    using pointer   = std::conditional_t<Const, const T*, T*>;
    using reference = std::conditional_t<Const, const T&, T&>;
    // ...
    Iter(const Iter<false>& o) : n(o.node()) {}      // non-const converts to const
};
using iterator       = Iter<false>;
using const_iterator = Iter<true>;
```

`std::conditional_t<B, X, Y>` is `X` when `B` is true and `Y` otherwise — a compile-time `if` over
types (Week 2's machinery, doing real work).

**The converting constructor is essential.** Without it:

```cpp
List<int>::const_iterator ci = l.begin();   // begin() returns iterator -- error
```

Every container in the standard library permits `iterator` → `const_iterator` and forbids the reverse,
and the one-line constructor above is how.

> **Note it is not marked `explicit`.** This is one of the rare cases where an implicit conversion is
> correct: it is always safe (you are only adding a restriction), and requiring a cast would make
> `const`-correct code more verbose than the sloppy kind — which is exactly the wrong incentive.

---

## 5. Why `++` and Not `+`

Your iterator has no `operator+`, no `operator[]`, no `operator<`, and no `operator-`.

**A list could provide them.** `it + 500` is a loop. Five lines.

**It must not**, and this is the design lesson of the week:

> **`it + n` on a random-access iterator is $O(1)$. Providing it for a list would make an $O(n)$
> operation wear $O(1)$ syntax**, and the caller has no way to see the difference.

The consequence is that generic code — written against the *syntax* — would silently become quadratic.
`std::sort` picks its pivot with `first + (last - first)/2`; give a list those operators and `sort`
compiles and runs in $O(n^2 \log n)$ while looking correct.

### 5.1 The Proof That You Got It Right

```cpp
List<int> l{3,1,2};
std::sort(l.begin(), l.end());
```

```
error: no match for 'operator-' (operand types are 'List<int>::Iter<false>' and ...)
```

**25 lines of error, and that is the correct outcome.** Compare Lecture 10 §5, where `std::sort` on a
`std::list` failed with the same message for the same reason.

> **Your container is refused by exactly the algorithms that should refuse it.** That is the test.
> **A container that compiles with every algorithm has lied about one of them.**

### 5.2 What Lying Actually Costs

This is not hypothetical. Declaring `random_access_iterator_tag` and implementing `+`, `-`, `<` and
`[]` by looping takes about seven lines, and then `std::sort` compiles.

Measured on the resulting container:

| n | `std::sort` | ratio per doubling |
| --- | --- | --- |
| 1,000 | 8.58 ms | — |
| 2,000 | 39.44 ms | **4.6×** |
| 4,000 | 194.39 ms | **4.9×** |

**Every result was correctly sorted.** `is_sorted` returned true every time.

A doubling ratio near 4.8 is $O(n^2 \log n)$ — quadratic work with a logarithmic factor on top, which
is exactly what a linear `it + n` inside an $O(n \log n)$ algorithm produces. For scale, `std::sort` on
4,000 elements in a `std::vector` takes well under a millisecond.

> **Nothing failed.** It compiled, it ran, it gave the right answer, and it was roughly three orders of
> magnitude too slow. **That is the failure mode the tag system exists to prevent**, and it is why
> declaring a category you cannot honour is worse than declaring none: an absent operator is a compile
> error you fix in a minute, and a dishonest tag is a performance bug you find in production.

---

## 6. Making Range-`for` Work

Nothing extra. Range-`for` needs `begin()` and `end()` returning something with `!=`, `*` and `++`
(L10 §6.1) — which you have:

```cpp
for (const auto& x : l) { ... }
```

works the moment the iterator exists. So does structured binding over a container of pairs, and so does
`std::back_inserter`.

**You did not implement range-`for` support. You implemented an iterator, and range-`for` support is a
consequence** — which is what a good protocol looks like.

---

## 7. The Payoff

Verified, on the `List<T>` from Lecture 19 with the iterator from this one:

```
accumulate      = 26
*max_element    = 9
count_if even   = 1
find(8) ok      = yes
after reverse   : 9 1 8 3 5
copied to vector: 5 elements
```

**None of those algorithms was modified.** They were written decades ago against a protocol, and your
container satisfies the protocol.

That is Week 3 §L10's $C + A$ instead of $C \times A$, from the other side: **you added one container
and got a hundred algorithms**, and the STL's authors did not have to know you existed.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| Iterator = a class with overloaded operators | Week 1's material, doing structural work |
| `operator++(int)` | The unused `int` distinguishes post- from pre-increment |
| The five typedefs | `iterator_traits` reads them; omit one and algorithms fail loudly |
| The category is a **tag type** | Compile-time dispatch — `distance` is $O(n)$ for us by choice |
| Lying about the category | Compiles, and silently makes algorithms quadratic |
| `template <bool Const>` | One iterator class, two types |
| `iterator` → `const_iterator` | A non-`explicit` converting constructor. Essential |
| No `+`, `-`, `[]`, `<` | An $O(n)$ operation must not wear $O(1)$ syntax |
| `std::sort` refuses it | **The proof you got it right** |
| Range-`for` | A consequence of `begin()`/`end()`, not a feature you add |
| A hundred algorithms | For about forty lines |

---

## 9. Exercises

**1.** Implement `Iter<Const>` for your list and verify with `static_assert` that
`iterator_traits<iterator>::iterator_category` is `bidirectional_iterator_tag` and that it **matches
`std::list<int>::iterator`'s**.

**2.** Delete one of the five typedefs and try to call `std::accumulate`. **Report the error's length**
and find the line naming the missing member.

**3.** Get these working and paste the output: `accumulate`, `max_element`, `count_if`, `find`,
`reverse`, and `copy` into a `std::vector` via `back_inserter`.

**4.** Call `std::sort` on your list. **Paste the error and quote the missing operator.** Explain why
this is the correct behaviour in two sentences.

**5.** Now *lie*: declare `random_access_iterator_tag` and implement `+`, `-` and `<` by looping. Get
`std::sort` to compile. **Time it at n = 1,000 and n = 10,000** and report the ratio. What complexity
did you get?

**6.** Remove the `Iter<false>` → `Iter<true>` converting constructor. Write a function taking
`const List<int>&` that calls `std::find`. **Paste the error.**

**7.** Write `const` and non-`const` `begin()`/`end()` plus `cbegin()`/`cend()`. Then write a function
taking `const List<int>&` that tries to modify an element through an iterator. **Confirm it does not
compile**, and say which typedef stopped it.

---

## 10. Next

**Lecture 21** builds a binary search tree — where the children genuinely *are* owned, so `unique_ptr`
is right. And where the obvious implementation contains a bug that only appears above about half a
million nodes.

---

*PROG 102 · Week 6 · Lecture 20 · © CSE Department*
