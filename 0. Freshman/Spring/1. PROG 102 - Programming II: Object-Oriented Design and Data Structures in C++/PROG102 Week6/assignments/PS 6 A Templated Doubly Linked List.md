# PROG 102 · Problem Set 6
## A Templated Doubly Linked List

**Week 6 · Released Friday Week 6 · Due Friday Week 7, 17:00 · 100 points**
**Covers:** Lectures 19–21

> **Project 1 was also assigned this week and is due Week 9.** This problem set is the foundation for
> it — a good `List<T>` here is most of Project 1's Part A. **Do not throw this code away.**

---

## Before You Start

```
g++ -std=c++17 -Wall -Wextra -pedantic -g -fsanitize=address,undefined prog.cpp -o prog
```

**Deliverables:** `list.hpp`, `list_test.cpp`, `bst.hpp`, `bst_test.cpp`, `ANSWERS.md`.
Name collaborators and state any generative-tool use.

**You may not use `std::list`, `std::forward_list`, `std::map` or `std::set`** in your implementations.
You may — and should — use them in your *tests*, as a reference to compare against.

---

## Part A — The List (34 pts)

**A1.** *(10)* `List<T>` with a **sentinel node**, private nested `Node`, and:

```
empty()  size()  front()  back()
begin()  end()  cbegin()  cend()
insert(const_iterator, T)   erase(const_iterator)
push_back  push_front  pop_back  pop_front  clear
```

`insert` and `erase` must have **no special cases** for head, tail or empty. If yours do, you have not
used the sentinel properly.

**A2.** *(8)* The full **Rule of Five**: destructor, copy constructor, move constructor,
copy-and-swap assignment, and a `noexcept` `swap`.

**Your class must contain no `this == &other` comparison.**

**A3.** *(8)* Write the move constructor **without** resetting the moved-from list to a valid empty
state. Move from a list and let both go out of scope.

**Paste the sanitizer report.** Then fix it and explain in two sentences what the moved-from object must
be left as, and why.

**A4.** *(8)* Test with `T = int` and `T = std::string`. For each: build, traverse forward **and
backward**, copy, modify the copy, and show the original unchanged. Self-assign.

**In one line, say why the `std::string` test is the one that matters.**

---

## Part B — The Iterator (30 pts)

**B1.** *(10)* Implement `Iter<bool Const>` with all five `iterator_traits` typedefs, both increment
and decrement forms, `*`, `->`, `==`, `!=`, and the **`iterator` → `const_iterator` converting
constructor**.

**B2.** *(6)* Verify with `static_assert` that your `iterator_category` is
`bidirectional_iterator_tag`, and that it **matches `std::list<int>::iterator`'s**.

Then remove one typedef and call `std::accumulate`. **Report the error's line count** and find the line
naming the missing member.

**B3.** *(8)* Get all of these working on your list and paste the output:

```
accumulate   max_element   count_if   find   reverse   copy (via back_inserter)
```

**B4.** *(6)* Call `std::sort` on your list.

- **(a)** *(2)* Paste the error and **quote the missing operator.**
- **(b)** *(4)* This is the correct outcome. **Explain why in three sentences**, referring to what the
  iterator category promises.

---

## Part C — The BST (24 pts)

**C1.** *(8)* `BST<T, Compare = std::less<T>>` with `unique_ptr` children, and `insert`, `contains`,
`inorder`, `height`, `size`.

**Height is in edges: empty = −1, single node = 0.**

Verify on `{5,3,8,1,4,7,9,3}` that `size()` is **7**, `height()` is **2**, and the traversal is sorted.

**C2.** *(6)* Show it working for `T = std::string` and for
`BST<int, std::greater<int>>`.

**How many of the five special members did your BST need? Why is that different from your List?**

**C3.** *(10)* Measure height against insertion order for n = 10, 100, 1,000 and 10,000, both
**sorted** and **shuffled** (at least 100 trials for the shuffled case).

Tabulate both against $\log_2 n$, and report the ratio of the random height to $\log_2 n$ at each size.
**Is that ratio constant? Which way does it drift?**

Then state in one sentence what `std::map` provides that your BST does not.

---

## Part D — The Bug at Scale (12 pts)

**D1.** *(6)* Build a chain of `unique_ptr`-linked nodes:

```cpp
struct Node { int v; std::unique_ptr<Node> next; };
```

Destroy chains of 1,000, 100,000, 500,000 and 1,000,000 nodes. **Report where it breaks and what your
stack limit is** (`ulimit -s`).

**D2.** *(6)* Fix it with an iterative destructor and confirm 5,000,000 works.

Then answer both:

- **(a)** *(3)* **Does AddressSanitizer help you diagnose the original?** Report what it says and why
  that is unhelpful.
- **(b)** *(3)* State the general rule this is an instance of, in one sentence. It should be about
  recursion and input data, not about `unique_ptr`.

---

## Marking

| Part | Points | Focus |
| --- | --- | --- |
| A | 34 | A correct sentinel list with the Rule of Five |
| B | 30 | An iterator that satisfies the protocol — **and is refused by `std::sort`** |
| C | 24 | A templated BST, and what balancing would have bought |
| D | 12 | The recursive destructor, and the rule behind it |
| **Total** | **100** | |

**Where the marks actually are:** B is the largest part and B4 is the one students find strangest — you
are marked for your container *failing* to compile with an algorithm. That is the week's central idea
and it is worth 6 points on its own.

---

## Submission Checklist

1. Clean build; sanitizer-clean except where A3 and D1 deliberately provoke reports.
2. `insert`/`erase` have **no** head/tail/empty special cases.
3. No `this == &other` anywhere.
4. Part B tested with **all six** algorithms.
5. Part C states the height convention it uses.
6. Collaborators named; generative-tool use stated.

---

*PROG 102 · Week 6 · Problem Set 6 · © CSE Department*
