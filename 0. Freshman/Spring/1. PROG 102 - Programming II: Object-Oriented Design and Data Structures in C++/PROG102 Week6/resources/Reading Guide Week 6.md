# PROG 102 · Week 6 · Reading Guide
## Building Containers, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| ***C++ Primer*** | **§9.2, §9.3** (revisit) | Read the container operations again **as a specification you must satisfy** |
| ***C++ Primer*** | **§10.5, §16.1** | Iterator adaptors; class templates revisited |
| **cppreference** | `std::list`, `iterator_traits`, *named requirements: LegacyBidirectionalIterator* | **The actual contract.** Primary source this week |
| **Stroustrup** | **§31.4, §33.1–33.2** | Reference for container and iterator design |
| **Meyers** | Item 13 (`cbegin`/`cend`) | Short, and directly relevant to L20 §4 |

> **This is the week cppreference becomes the primary text.** Week 3 said learning to read it was a
> course objective; this week it is a requirement. The page **"named requirements:
> LegacyBidirectionalIterator"** lists exactly what your iterator must provide, and it is the
> specification PS 6 Part B is marked against.

---

## Reading `std::list` as a Specification

Open cppreference's `std::list` page and work through it as though you had to implement it.

**Guiding questions:**

1. Every member function has a **Complexity** line. Find one that is $O(1)$ and would be $O(n)$ in a
   `vector`, and one that `list` does not provide at all. **Why is the second one absent?**
2. `std::list` has `sort`, `merge`, `splice`, `remove` and `unique` as **members**, duplicating
   algorithm names. **Give the reason for each** — they are not all the same reason.
3. Find the **iterator invalidation** section. Compare it with what you derived in L19 §5. Did you get
   it right from the implementation alone?
4. `std::list::size()` is $O(1)$ in C++11 and later. **What must the implementation store to promise
   that, and what does it cost on every insert and erase?**
5. `splice` is the operation a list exists for. **Read its complexity carefully** — one overload is
   $O(1)$ and another is $O(n)$. Which, and why?

---

## Reading the Iterator Requirements

**Guiding questions:**

1. `LegacyBidirectionalIterator` refines `LegacyForwardIterator`, which refines
   `LegacyInputIterator`. **List the operations added at each level.**
2. What does `LegacyForwardIterator` require that `LegacyInputIterator` does not? *(The answer is
   "multi-pass" — say what that means for a stream.)*
3. `iterator_traits` has five member typedefs. **What is each one for?** For `difference_type`
   specifically: which algorithm needs it, and why is `std::ptrdiff_t` the right choice?
4. Look at `std::advance` and `std::distance`. **Both work on any iterator, but with different
   complexity depending on the category.** How is that implemented? *(Tag dispatch — L20 §3.1.)*

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux.** Structural results are exact; timings are not.

### L19 §6 — The list working

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined list_test.cpp -o lt && ./lt
```

**Expect:** forward and backward traversal, deep copy independence, self-assignment, all
sanitizer-clean, and `T = std::string` working.

### L20 §3, §7 — The iterator protocol and the payoff

```
g++ -std=c++17 -Wall -Wextra traits.cpp -o traits && ./traits
```

**Expect:** category bidirectional, matching `std::list<int>::iterator`, and `accumulate` = 26,
`max_element` = 9, `count_if` = 1, `reverse` and `copy` working.

### L20 §5.1 — `std::sort` correctly refusing

```
g++ -std=c++17 -c sortref.cpp -o /dev/null 2>&1 | head -3
```

**Expect:** `no match for 'operator-'`, about 25 lines. **This failing is the pass condition.**

### L20 §5.2 — What lying costs

```
g++ -std=c++17 -O2 lie.cpp -o lie && ./lie
```

**Expect:** `std::sort` compiles, sorts **correctly**, and takes 8.6 / 39.4 / 194.4 ms at n = 1,000 /
2,000 / 4,000 — about 4.8× per doubling.

### L21 §3 — The BST

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined bst_test.cpp -o bt && ./bt
```

**Expect:** size 7 (duplicate rejected), height 2, sorted traversal, empty-tree height **−1**, and
sorted input giving height 9 of 10.

### L21 §4 — The destructor that only fails at scale

```
g++ -std=c++17 -O2 recur.cpp -o recur
for n in 1000 100000 500000 1000000; do ./recur $n; done
ulimit -s
g++ -std=c++17 -O2 recur_fix.cpp -o recur_fix && ./recur_fix 5000000
```

**Expect:** fine to 500,000, **segfault at 1,000,000** on an 8 MB stack, and the iterative version
handling 5,000,000.

### Lab 6 — The comparison

```
g++ -std=c++17 -O2 bench.cpp -o bench && ./bench
g++ -std=c++17 -O2 three.cpp -o three && ./three
```

**Expect:** your list within ~15% of `std::list`, and `std::vector` 7–10× faster than both at
traversal.

---

## A Warning About Your Own Test Code

While building this week's material, a test contained this line:

```cpp
std::is_sorted(t.inorder().begin(), t.inorder().end())
```

It looks fine. **It calls `inorder()` twice**, producing two different temporary vectors, and then
compares an iterator from the first against an iterator from the second. AddressSanitizer caught it as
a heap-buffer-overflow, and the fix was to name the temporary:

```cpp
auto v = t.inorder();
std::is_sorted(v.begin(), v.end());
```

**The bug was in the test, not the container.** That is worth stating because this week you will write
more test code than implementation code, and **a wrong test can convince you a correct container is
broken — or, far worse, a broken one is fine.**

Run your tests under the sanitizers too. They are code.

---

## The Habit, in Its Sixth Form

- **W0:** do not believe a claim you have not seen a compiler make.
- **W1:** advice can be fifteen years out of date.
- **W2:** a correct measurement can carry a wrong explanation.
- **W3:** a correct theory can answer a different question.
- **W4:** your benchmark may measure something other than what you named it.
- **W5:** the optimizer can delete the thing you are measuring.

**Week 6 adds the one with no tool behind it:** *a program can be correct, pass every test, trip no
sanitizer, and still be wrong.*

L20 §5.2's lying iterator sorted correctly every time and was a thousand times too slow. L21 §4's
recursive destructor worked on every input anyone would test and died at a million. **Neither is
detectable by the tooling this course has taught you.**

What catches them is the thing the whole week is about: **an interface that tells the truth about what
it can do, and a habit of asking what happens when the input gets big.**

---

## Before Week 7

1. Lectures 19–21 read; cppreference's `std::list` and `LegacyBidirectionalIterator` worked through.
2. **PS 6 Parts A and B started** — they are Project 1's foundation.
3. **Project 1's specification read**, even though it is due in Week 9. It tells you which decisions are
   yours.
4. Week 7 is **design patterns**, and it is a change of gear: less measurement, more judgement. The
   Iterator you built this week is one of the patterns, which is the best possible argument that
   patterns describe things that work rather than things somebody invented.

---

*PROG 102 · Week 6 · Reading Guide · © CSE Department*
