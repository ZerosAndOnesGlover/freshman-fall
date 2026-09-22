# PROG 102 · Week 3 · Reading Guide
## *C++ Primer* Chapters 9–11, and Reproducing the Measurements

---

## What to Read

| Source | Sections | Why |
| --- | --- | --- |
| ***C++ Primer*** | **Ch. 9** | Sequence containers. The core reading. |
| ***C++ Primer*** | **Ch. 10, §10.1–10.3** | Algorithms and lambdas. |
| ***C++ Primer*** | **§11.1–11.3** | Associative containers. |
| **Stroustrup** | **Ch. 31–33** | The reference for containers, algorithms, iterators. **Look things up.** |
| **cppreference** | any container's page | The complexity guarantees are stated exactly there |

> **Read cppreference for this week, not the books.** Every container page has a **Complexity** line for
> every operation and an **Iterator invalidation** table. Those two things are what you actually need,
> and no textbook presents them as compactly. Learning to read those pages is a course objective.

---

## Chapter 9 — Sequence Containers

**Guiding questions:**

1. §9.1 — the book's table of container operations. **Find the row for "insert in the middle" and the
   row for "random access".** Now look at Lecture 11 §4. Which of those two rows predicted the
   measurement, and which did not?
2. §9.2.1 — iterator ranges. Why is `end()` one past the last element? Give three consequences.
3. §9.3.6 — the book warns that container operations may invalidate iterators. **Write down, from
   memory, which containers invalidate on insertion.** Then check §9.3.6 and Lecture 11 §6.1.
4. §9.4 — `capacity` and `reserve`. The book explains the growth strategy. **What growth factor does it
   say libraries use, and what did you measure?**
5. §9.5 — `std::string`. Skim. It is a container and most of Chapter 9 applies to it.

---

## Chapter 10 — Algorithms

**Guiding questions:**

1. §10.1 — the book stresses that algorithms operate on iterators, not containers. **What is the
   consequence for `std::remove`?** Answer before reading §10.2.
2. §10.2.3 — write-only algorithms and the danger of writing past the end. Compare with Lecture 12
   §4's warning about `transform`'s output range.
3. §10.3 — lambdas. **This is the reading that matters most for Week 11.** Work through §10.3.2 and
   §10.3.3 properly, especially capture lists.
4. §10.4 — iterator adaptors: `back_inserter`, stream iterators. **Why is `back_inserter` an
   iterator?** It has no element to point at.
5. §10.5 — the book explains that `std::list` has its own `sort`, `remove` and `unique`. **Give the
   reason**, then check it against Lecture 10 §5.1.

---

## Chapter 11 — Associative Containers

**Guiding questions:**

1. §11.2.2 — the key type's requirements. `map` needs `<`. **What did Lecture 04 §6.1 say happens if
   your `operator<` is not a strict weak ordering?**
2. §11.3.4 — the return type of `map::insert`. Why is it a `pair<iterator,bool>`, and what is the
   `bool`? *(PS 3 A2 uses exactly this.)*
3. §11.3.5 — subscripting a `map` **inserts** if the key is absent. When is that convenient, and when
   is it a bug? **Which operation should you use on a `const map`?**
4. §11.4 — unordered containers. The book covers hashing your own types. Note what you must provide;
   Week 6 needs it.

---

## Reproducing This Week's Measurements

**g++ 13.3.0, x86-64 Linux, `-O2`.** Ratios should reproduce; absolute times will not.

### L10 §3 — Iterator categories

```
g++ -std=c++17 -O2 algos.cpp -o algos && ./algos
```

**Expect:** vector/deque random access; list/set/map bidirectional.

### L10 §5 — `std::sort` on a list

```
g++ -std=c++17 -c sortlist.cpp -o /dev/null 2>&1 | wc -l          # 25
g++ -std=c++17 -c sortlist.cpp -o /dev/null 2>&1 | grep -m1 error
```

**Expect:** `no match for 'operator-' (operand types are 'std::_List_iterator<int>' and ...)`.

### L11 §3.1, §4 — The container measurements

```
g++ -std=c++17 -O2 containers.cpp -o containers && ./containers
```

**Expect:** list 6.3× slower to traverse; vector 178× faster at sorted insertion; list 128× faster at
front insertion.

### L11 §5.3 — map vs unordered_map

```
g++ -std=c++17 -O2 assoc.cpp -o assoc && ./assoc
```

**Expect:** lookup 6.5× faster unordered; growth factor 2.0; 21 capacity changes per million.

### L12 §2 — `std::sort` vs `qsort`

```
g++ -std=c++17 -O2 sortcmp.cpp -o sortcmp && ./sortcmp
```

**Expect:** roughly 2×, and identical results.

### L12 §4.1, §5, §6 — The traps

```
g++ -std=c++17 -O2 eraseremove.cpp -o er && ./er
g++ -std=c++17 -O1 -g -fsanitize=undefined overflow.cpp -o ovf && ./ovf
g++ -std=c++17 -c vb.cpp -o /dev/null            # bool& error
```

---

## A Note on Reading Complexity Guarantees

The standard specifies complexity for every container operation, and cppreference states it plainly.
**Read those lines. Then remember what Lab 3 measured.**

Both of these are true at once:

- `std::list::insert` is $O(1)$ and the standard guarantees it.
- Inserting 50,000 elements in sorted order into a `list` took **178× longer** than into a `vector`.

There is no contradiction. The guarantee is about **one operation in isolation**; the measurement is
about a **program**, which also had to find the position, on hardware where where-the-memory-is matters
as much as how-many-operations.

> **A complexity guarantee tells you how a cost scales. It does not tell you what the cost is.**

This is why the course asks you to do both — read the guarantee *and* run the benchmark. Neither one
substitutes for the other, and the interesting engineering is almost always in the gap between them.

---

## Before Week 4

1. Lectures 10–12 read.
2. *C++ Primer* Ch. 9 and §10.1–10.3 worked through. **§10.3 on lambdas especially** — you need it for
   PS 3 and it is the foundation of Week 11.
3. **PS 3 Part A started.** Ten problems takes longer than it looks, mostly spent finding the right
   algorithm — which is the intended work.
4. **Week 4 is the first midterm-relevant week.** Midterm 1 covers Weeks 0–4 and is sat on Tuesday 2 March (Week 6).
   The revision guide arrives with Week 4's materials; do not wait for it to start reviewing Weeks 0–2.

---

*PROG 102 · Week 3 · Reading Guide · © CSE Department*
