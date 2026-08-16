# PROG 102 · Lecture 12
## The Algorithms

**Week 3 · Thursday · 50 minutes**
**Reading:** *C++ Primer* Ch. 10, §10.3 · **Reference:** Stroustrup Ch. 32
**Assumes:** L10, L11

**Date:** Thursday 4 February 2027 · 10:00–10:50 · Week 3

---

## 1. What They Are

About **100 function templates** in `<algorithm>` and `<numeric>`. Every one takes an iterator range
and knows nothing about containers.

```cpp
std::sort(v.begin(), v.end());
std::find(v.begin(), v.end(), 8);
std::count_if(v.begin(), v.end(), [](int x){ return x % 2 == 0; });
std::transform(v.begin(), v.end(), out.begin(), [](int x){ return x * x; });
std::accumulate(v.begin(), v.end(), 0);
```

**Learn the ten you will use constantly**, and know that a reference exists for the rest. The ten:
`sort`, `find`, `find_if`, `count_if`, `transform`, `accumulate`, `copy`, `remove_if`, `max_element`,
`all_of`/`any_of`.

---

## 2. `std::sort`, and Why Week 2 Mattered

C has had a general sort since 1978:

```c
void qsort(void* base, size_t n, size_t size, int (*cmp)(const void*, const void*));
```

C++ has:

```cpp
template <class RandomIt> void sort(RandomIt first, RandomIt last);
```

Both sort anything. Measured on **2,000,000 random `int`s**, three runs:

| | run 1 | run 2 | run 3 |
| --- | --- | --- | --- |
| `qsort` (function pointer) | 302.2 ms | 312.1 ms | 302.9 ms |
| `std::sort` (template) | 157.7 ms | 152.2 ms | 156.2 ms |
| **ratio** | 1.92× | 2.05× | 1.94× |

**`std::sort` is about twice as fast**, and produces an identical result.

### 2.1 Why

`qsort` receives a **function pointer**. For every one of roughly $n \log n \approx 4 \times 10^7$
comparisons it must:

- make an **indirect call** through the pointer, which cannot be inlined because the target is unknown
  at compile time;
- pass `const void*` arguments, so the comparator casts them back and dereferences;
- and, having no type information, `qsort` moves elements with `memcpy` of a runtime-supplied size.

`std::sort` is a **template**. The comparison is `operator<` on a known type, and the compiler inlines
it into the loop — the comparison becomes a single `cmp` instruction rather than a call. Element moves
are typed assignments the optimizer understands.

> **This is Week 2's zero-overhead claim paying a dividend.** It is not that C++ has a better
> algorithm — both are introsort-family quicksorts. It is that **the generic version knows the type at
> compile time and the C version does not.** Genericity through templates costs compile time;
> genericity through `void*` and function pointers costs *runtime, forever*.

### 2.2 Custom Comparators

```cpp
std::sort(v.begin(), v.end(), std::greater<int>());              // descending
std::sort(v.begin(), v.end(), [](const P& a, const P& b) {       // by field
    return a.score > b.score;
});
```

The comparator must be a **strict weak ordering** (L04 §6.1). Violating it is undefined behaviour and
`std::sort` can run off the end of the array — a real crash, not a wrong order.

**`std::stable_sort`** preserves the relative order of equivalent elements, at the cost of extra
memory. Use it when "equal" elements are distinguishable and the input order means something.

---

## 3. Searching

| Algorithm | Requires | Complexity |
| --- | --- | --- |
| `std::find`, `find_if` | input iterators | $O(n)$ |
| `std::binary_search`, `lower_bound`, `upper_bound` | **a sorted range** | $O(\log n)$ on random access |
| `c.find(k)` (member) | an associative container | $O(\log n)$ or $O(1)$ |

**`lower_bound` is the one to know.** It returns the first position where a value could be inserted
without breaking the order — which is both "find it" and "where does it go", and is what makes the
sorted-`vector` insertion in L11 §4.1 fast.

And from L11 §5.4: **on a `std::set`, `std::find` was measured 6,000× slower than `s.find`.** Generic
does not mean best; it means *works everywhere*.

---

## 4. Transforming and Reducing

```cpp
std::vector<int> v{5,3,8,1,9,2};
std::vector<int> sq(v.size());
std::transform(v.begin(), v.end(), sq.begin(), [](int x){ return x*x; });
// sq: 25 9 64 1 81 4
```

**`transform`'s output range must already be big enough.** Writing into an empty vector is a buffer
overrun — use `std::back_inserter(sq)` (L10 §7) if you want it to grow.

```cpp
std::accumulate(a.begin(), a.end(), 0);                          // 10
std::accumulate(a.begin(), a.end(), 1, std::multiplies<int>());  // 24
std::accumulate(s.begin(), s.end(), std::string(""));            // "abc"
```

`accumulate` is a general fold, not just a sum.

### 4.1 The `accumulate` Trap

```cpp
std::vector<double> d{0.5, 0.5, 0.5};
std::accumulate(d.begin(), d.end(), 0);      // ???
```

**The answer is 0.**

```
accumulate(d,0)   = 0
accumulate(d,0.0) = 1.5
```

The accumulator's type is deduced from the **initial value**, not from the elements. `0` is an `int`,
so the running total is an `int`, and each `0.5` is truncated on the way in.

> **No warning. No error. A silently wrong number.** This is the most common STL bug in numeric code
> and it is worth carrying: **the initial value determines the type.** Write `0.0`, or `0.0L`, or
> `std::int64_t{0}` when summing `int`s that might overflow.
>
That last case is real. Summing **one million `int`s of one million each**:

```
init 0        -> -727379968   (type: int, 4 bytes)
init int64{0} -> 1000000000000
true sum      -> 1000000000000
```

**A million positive numbers summed to a negative one.** The `0` made the accumulator an `int`, and it
wrapped.

> **This one your build line does catch.** Under `-fsanitize=undefined`:
>
> ```
> stl_numeric.h:141:9: runtime error: signed integer overflow:
>                      1000000 + 2147000000 cannot be represented in type 'int'
> ```
>
> The truncation case in the table above is **not** caught, because converting `0.5` to `int` is
> perfectly well-defined — it is merely not what you meant. **UBSan finds undefined behaviour, not
> wrong answers**, and that distinction is worth holding onto.

---

## 5. `std::remove` Does Not Remove

The most surprising name in the library.

```cpp
std::vector<int> v{1,2,3,2,4,2,5};
auto newend = std::remove(v.begin(), v.end(), 2);
```

Measured:

```
original                  size=7 : 1 2 3 2 4 2 5
after std::remove(...,2)  size=7 : 1 3 4 5 4 2 5
                                   4 elements are 'live'
after v.erase(newend,end) size=4 : 1 3 4 5
```

**The size did not change.** `remove` shuffled the surviving elements to the front and returned an
iterator to the new logical end. The tail (`4 2 5` here) is unspecified leftovers.

**It cannot do better.** An algorithm only has iterators — it can read and write elements, but it has
no way to change a container's size, because it has never heard of the container. **Only the container
can erase.**

### 5.1 The Erase-Remove Idiom

```cpp
v.erase(std::remove(v.begin(), v.end(), 2), v.end());                        // by value
u.erase(std::remove_if(u.begin(), u.end(), [](int x){ return x%3==0; }), u.end());  // by predicate
```

Verified: `1 3 4 5`, and `1 2 4 5 7 8 10` for dropping multiples of 3.

**Memorise this shape.** It is ubiquitous in C++17 code and it looks bizarre until you know why the
algorithm cannot do it alone.

*(C++20 adds `std::erase` and `std::erase_if` as free functions that do both. Not available to you
here, and worth knowing the idiom regardless — you will read a great deal of code that uses it.)*

---

## 6. `std::vector<bool>`

The standard library's most instructive mistake.

`std::vector<bool>` is a **specialization** (Week 2 §L09 §2) that packs elements one per *bit*. Eight
booleans per byte instead of one per byte.

That is a genuine space win, and it broke the type.

```cpp
std::vector<bool> vb{true,false,true};
std::vector<int>  vi{1,0,1};
```

Measured:

```
sizeof(vector<bool>)=40  sizeof(vector<int>)=24
decltype(vb[0]) is bool? NO   (it is a proxy: std::_Bit_reference)
decltype(vi[0]) is int&? yes
```

And so:

```cpp
int&  ri = vi[0];    // fine
bool& rb = vb[0];    // error: cannot bind non-const lvalue reference of type 'bool&'
                     //        to an rvalue of type 'bool'
```

**`vb[0]` does not return a `bool&`, because there is no such thing as a reference to a bit.** It
returns a proxy object that remembers which bit it refers to and forwards assignment.

### 6.1 Why It Matters Beyond `bool`

`std::vector<bool>` **is not a container** by the standard's own definition — it fails the requirement
that `&c[0]` yields a pointer to the element type. So generic code like:

```cpp
template <typename T>
void process(std::vector<T>& v) { T& first = v[0]; ... }
```

works for every `T` **except `bool`**, and fails with an error that mentions `_Bit_reference` and
appears to have nothing to do with your code.

> **The lesson is about specialization, not about `bool`.** Week 2 §L09 §2.3 said: use specialization
> when a type needs different *logic*, not to make one type faster at the cost of behaving differently.
> `vector<bool>` is what the second one looks like, and it has been unfixable for thirty years because
> too much code depends on it.
>
> **If you need bits, use `std::bitset` (fixed size) or `std::vector<char>` (dynamic).** If you need a
> vector of booleans that behaves like a vector, `std::vector<char>` or `std::deque<bool>`.

---

## 7. Prefer Algorithms to Loops

```cpp
// raw loop
int count = 0;
for (std::size_t i = 0; i < v.size(); ++i) if (v[i] % 2 == 0) ++count;

// algorithm
auto count = std::count_if(v.begin(), v.end(), [](int x){ return x % 2 == 0; });
```

The second is better for reasons that are not about elegance:

- **It says what, not how.** A reader recognises `count_if` instantly; the loop must be read.
- **The off-by-one errors are gone**, along with the index type. `int i` versus `std::size_t` is a real
  warning under `-Wextra` and a real bug on large containers.
- **It works on any container**, including ones with no `operator[]`.
- **It is at least as fast**, and sometimes faster — the library version may be specialised for the
  iterator category or vectorised.

**When a raw loop is right:** when no algorithm fits, when you need to break early in a way
`find_if` cannot express, or when the loop body does several unrelated things. Do not contort a
computation to avoid a loop. **But check whether the algorithm exists first** — the usual reason people
write the loop is not knowing that `std::rotate` or `std::partition` was right there.

---

## 8. Summary

| Idea | The point |
| --- | --- |
| ~100 algorithms, all on iterator ranges | None of them knows about containers |
| `std::sort` vs `qsort` | **~2× faster**, measured, same result |
| Why | Templates inline the comparison; function pointers cannot be inlined |
| Comparator must be a strict weak ordering | Violating it is UB, not a wrong order |
| `lower_bound` | "Find it" and "where does it go" in one, $O(\log n)$ |
| Member `find` beats `std::find` | ~6,000× on a set |
| `accumulate`'s type comes from the **init value** | `accumulate(doubles, 0)` returns **0** |
| `std::remove` does not remove | It cannot — only a container can change its size |
| Erase-remove idiom | `v.erase(std::remove(...), v.end())` |
| `vector<bool>` | A specialization that broke the contract, permanently |
| Prefer algorithms to loops | Intent, correctness, generality — and no slower |

---

## 9. Exercises

**1.** Reproduce the `qsort` vs `std::sort` measurement at N = 2,000,000, three runs each. **Report
your ratio.** Then explain in two sentences why the C version cannot close the gap.

**2.** Sort a `vector` of structs by one field descending using a lambda. Then use `std::stable_sort`
and construct an input where the two give **different** output.

**3.** Run `std::accumulate` over `{0.5, 0.5, 0.5}` with initial value `0`, then `0.0`. **Report both.**
Then sum a million `int`s of about a million each with initial value `0` and report what happens.

**4.** Demonstrate that `std::remove` does not change `size()`. Print the whole vector afterwards,
**including the tail**, and say what is in it.

**5.** Write the erase-remove idiom to delete every element failing a predicate. Then write the same
thing as a raw loop **that erases while iterating**. Get it wrong first, run it under
`-fsanitize=address`, then fix it.

**6.** Show that `bool& b = vb[0];` fails while `int& i = vi[0];` succeeds. **Quote both the error and
`decltype(vb[0])`.** Then write a function template that works for `std::vector<T>` for every `T`
except `bool`, and show it failing.

**7.** Replace three raw loops in your PS 2 code with algorithms. **For each, say which is clearer and
why** — and if one is worse as an algorithm, say so and keep the loop.

---

## 10. Next

**Week 4** turns from generic programming to **object-oriented** programming proper: inheritance,
virtual functions, and the vtable. Where a template resolves everything at compile time and costs
nothing, a virtual call resolves at **run** time and costs one indirection.

You will measure that indirection, and Lab 4 will have you inspect the vtable by hand in GDB.

---

*PROG 102 · Week 3 · Lecture 12 · © CSE Department*
