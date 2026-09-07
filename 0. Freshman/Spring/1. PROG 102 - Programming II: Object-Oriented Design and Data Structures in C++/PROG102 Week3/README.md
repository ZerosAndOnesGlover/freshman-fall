# PROG 102 · Programming II — Object-Oriented Design and Data Structures in C++
## Week 3: The Standard Template Library

**Credits:** 4 (3 lecture + 1 lab) · **Prerequisites:** PROG 101 (C), CS 101
**Assessment for this course (overall):** Labs 20%, Problem Sets 30%, Midterms 25%, Final 15%, Projects 10%
**This week's deliverables:** PS 3, Lab 3, Quiz 3 (Monday, covers Week 2)

---

### Why This Week Exists

You spent three weeks building `IntStack`, then `Roster`, then `Stack<T>`. **All of it already
existed, and the existing version is better.**

That is not a wasted three weeks — it is the only order in which this week makes sense. You now know
what `std::vector` is doing, because you wrote it. You know why its definitions are in the header,
because Lecture 08 §3 made you hit the linker error. You know why it has both `size()` and
`capacity()`, and you know what `new T[n]` cost you that `vector` refuses to pay.

**This week is about the design, not the API.** The API you can look up. The design is the thing worth
a week: **algorithms and containers know nothing about each other**, and the reason that works is a
single abstraction — the iterator.

### Learning Objectives

By the end of Week 3, you should be able to:

1. Explain what an iterator is in terms of the operations it supports, not the type it has.
2. Name the iterator categories, say which containers provide which, and **predict from that alone**
   which algorithms will compile.
3. Read the error from `std::sort` on a `std::list` and say what it proves about the contract.
4. Choose between `vector`, `deque` and `list` from the operations required — and know when the
   complexity table gives the wrong answer.
5. Choose between `map` and `unordered_map`, and say what ordering costs.
6. Use `sort`, `find`, `transform`, `accumulate`, `count_if` and friends, and prefer them to raw loops.
7. State when each container invalidates iterators, and demonstrate the resulting bug.
8. Explain why `std::vector<bool>` is the standard library's most famous mistake.
9. **Measure** container performance and explain results the complexity table does not predict.

### This Week's Materials

| File | Purpose |
| --- | --- |
| [[L10 The Iterator Abstraction]] | Why algorithms and containers are separate, and what makes that possible |
| [[L11 The Containers]] | Sequence, associative, adaptors — and how to choose |
| [[L12 The Algorithms]] | `sort`, `find`, `transform`, `accumulate`, and `vector<bool>` |
| [[PS 3 Ten Problems With the STL]] | Due Friday of Week 4 |
| [[PROG102 Week3/assignments/QUIZ 3 Week 3 Monday\|QUIZ 3 Week 3 Monday]] | 15 minutes, covers Week 2 |
| [[LAB 3 Profiling STL Containers]] | Measure the containers and find where the complexity table lies |
| [[PROG102 Week3/resources/Reading Guide Week 3\|Reading Guide Week 3]] | *C++ Primer* Ch. 9–11, and every command to reproduce this week |
| [[PROG102 Week3/solutions_instructor/PS 3 Solutions\|PS 3 Solutions]] | Instructor only |
| [[PROG102 Week3/solutions_instructor/LAB 3 Solutions\|LAB 3 Solutions]] | Instructor only |

### The One Thing to Take From This Week

**`std::sort` has never heard of `std::vector`.**

It takes two iterators. It requires that they support `*`, `++`, `--`, `+`, `-` and comparison — the
*random access* category — and nothing else. It works on a `vector`, on a `deque`, on a plain C array,
and on any container you write in Week 6 that provides the right iterator.

That decoupling is why the STL is roughly 100 algorithms and 15 containers rather than 1,500 functions.
It is also why **your** containers get the algorithms for free, which is the point of Week 6.

### The Measurement That Contradicts the Table

Every data structures course teaches that `list` insertion is $O(1)$ and `vector` insertion is $O(n)$.
Lab 3 measures it, and the answer depends entirely on a word the table leaves out.

| Task | vector | list | winner |
| --- | --- | --- | --- |
| Insert keeping sorted order, N=50,000 | 45 ms | 8,086 ms | **vector, 178×** |
| Insert at a position you already have | 446 ms | 3.5 ms | **list, 128×** |

**Both are real.** The first has to *find* the position, and finding it in a list means chasing 50,000
pointers through scattered memory. The second is handed the position.

The complexity table describes the insertion. It says nothing about the search — and in real code the
search is almost always there. This is the week's central engineering lesson and Lab 3 is built on it.

### Assessment Reminder

**Quiz 3 is Monday and covers Week 2** — templates, deduction, instantiation, specialization, and what
templates cost.

### Connections

**Back:** **Week 2** is the machinery. `std::vector<T>` is a class template; `std::sort` is a function
template; the iterator categories are tag types dispatched on at compile time. The 78-line error you
measured in **L09 §5** came from `std::sort`, and this week you will understand what it was complaining
about.

**Forward:** **Week 6** implements a container with real iterators, so that STL algorithms work on it.
**Week 8**'s Iterator pattern is this abstraction described in Gang-of-Four terms. **Week 11**'s lambdas
are what you pass to `count_if` and `transform`. **Week 12** returns to Lab 3's measurements and
explains them with cache lines.

---

*PROG 102 · Week 3 · © CSE Department*
