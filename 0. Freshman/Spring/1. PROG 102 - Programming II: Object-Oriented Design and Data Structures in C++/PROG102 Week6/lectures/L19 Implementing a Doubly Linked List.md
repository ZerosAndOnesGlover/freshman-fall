# PROG 102 · Lecture 19
## Implementing a Doubly Linked List

*“One can even conjecture that Lisp owes its survival specifically to the fact that its programs are lists, which everyone, including me, has regarded as a disadvantage.”* — John McCarthy, "History of Lisp" (1979)

**Week 6 · Tuesday · 50 minutes**
**Reading:** *C++ Primer* §9.2 (revisit), Ch. 13 · **Reference:** Stroustrup §31.4
**Assumes:** Weeks 1, 2 and 5 — Rule of Five, templates, `unique_ptr`

**Date:** Tuesday 2 March 2027 · 10:00–10:50 · Week 6

**Coursework:** 📊 **Quiz 6** today 10:00–10:15 · 📋 **Project 1** released today 10:00, due Fri 26 Mar 17:00 · 📘 **Midterm 1** today 18:00–19:30 · 📝 **PS 5** due Fri 5 Mar 17:00 · 📝 **PS 6** released Fri 5 Mar 10:00, due Fri 12 Mar 17:00 · 🔬 **Lab 6** Mon 8 Mar 15:00–16:50

---

## 1. Why You Are Writing This

`std::list` exists. It is faster than what you will write, better tested, and already installed.

**The reason to implement one is that using a container never asks you the questions that building one
does.** By Friday you will have answered:

- Why does `std::list` keep a **sentinel** node?
- Why does its iterator have `++` but not `+`?
- Why does inserting into a `vector` invalidate iterators and inserting into a `list` not?

Those are not trivia. They are the three design decisions that define what a linked list *is*, and
each one is forced on you the moment you try to write `insert`.

---

## 2. The Node

```cpp
template <typename T>
class List {
    struct Node {
        T     value;
        Node* prev;
        Node* next;
    };
    Node*       sentinel;
    std::size_t count;
};
```

`Node` is **private and nested**. It is an implementation detail: no user of `List<T>` should ever name
one, and nesting it means the name cannot collide with anything.

### 2.1 Raw Pointers Here Are Correct

After Week 5 this may look like a regression. It is not.

**The list owns its nodes**, and it says so by having a destructor that deletes them. The `prev` and
`next` pointers are **not** ownership — they are the structure. Making them `unique_ptr` would claim
that each node owns the next one, which is both false (`prev` would then be an aliasing pointer) and
catastrophic at scale (**Lecture 21 §4**).

> **This is Week 5 §L17 §7's item 3, at its most important.** A raw pointer that does not own is a
> correct and necessary thing. What Week 5 objected to was raw pointers that *do* own, with no type
> saying so — and here the owner is the `List`, unambiguously.

---

## 3. The Sentinel

The obvious design is `Node* head; Node* tail;` with null at both ends. Try writing `insert` for it:

```cpp
// insert before position p
if (p == head)      { /* new head: no prev to update */ }
else if (p == nullptr) { /* append at tail: no next to update */ }
else                { /* the general case */ }
if (empty())        { /* head and tail are both the new node */ }
```

**Four cases, and every one of them is a place to get a pointer wrong.**

Now add one node that holds no value and links to itself:

```cpp
Node() : value(), prev(this), next(this) {}      // the sentinel
```

The list becomes a **circular** structure with the sentinel as the join. `sentinel->next` is the first
element, `sentinel->prev` is the last, and an empty list is one where both are the sentinel itself.

```cpp
iterator insert(const_iterator pos, T value) {
    Node* at = pos.node();
    Node* fresh = new Node(at->prev, at, std::move(value));
    at->prev->next = fresh;
    at->prev       = fresh;
    ++count;
    return iterator(fresh);
}
```

**One case. No null checks. No special handling for head, tail or empty**, because there are no nulls
anywhere in the structure.

`erase` is the same:

```cpp
iterator erase(const_iterator pos) {
    Node* victim = pos.node();
    Node* nxt = victim->next;
    victim->prev->next = victim->next;
    victim->next->prev = victim->prev;
    delete victim; --count;
    return iterator(nxt);
}
```

> **That is what the sentinel buys: it converts four cases into one** by guaranteeing that every node
> has a real `prev` and a real `next`. It costs one node's worth of memory per list — and for a
> container whose elements are already one allocation each, that is nothing.
>
> **This is the answer to "why does `std::list` store a sentinel node?"** and you have now derived it
> rather than been told it.

### 3.1 And It Makes `end()` Meaningful

```cpp
iterator begin() { return iterator(sentinel->next); }
iterator end()   { return iterator(sentinel); }
```

`end()` is the sentinel. It is a real, dereferenceable-in-principle node that simply must not be
dereferenced — which is exactly what "one past the end" means (L10 §2.1). Incrementing the last
iterator lands on it naturally, because the structure is circular.

**Without a sentinel, `end()` would have to be a null iterator**, and `--end()` — which must give you
the last element — would be impossible.

---

## 4. The Rule of Five

`List` owns nodes. It manages a resource no library type manages for it. **The Rule of Zero does not
apply**, and all five must be written.

```cpp
List() { init(); }

List(const List& o) { init(); for (const T& v : o) push_back(v); }        // deep copy

List(List&& o) noexcept : sentinel(o.sentinel), count(o.count) { o.init(); }

List& operator=(List o) noexcept { swap(o); return *this; }               // copy-and-swap

~List() { clear(); delete sentinel; }

void swap(List& o) noexcept { std::swap(sentinel, o.sentinel); std::swap(count, o.count); }
```

Each line is a Week 1–5 idea:

- **Copy constructor**: deep — allocate fresh nodes. Note it iterates `o` using the iterator you are
  about to write, which is why the iterator comes first in practice.
- **Move constructor**: steal the sentinel pointer, then **`o.init()`** — the moved-from list must be a
  *valid empty list*, not a wreck (L18 §4.1). Giving it a fresh sentinel is what makes it usable again.
- **Copy-and-swap assignment**: by value, swap, return (L06 §2). Handles self-assignment and gives the
  strong guarantee, for free, once more.
- **`swap` is `noexcept`** and swaps every member (L06 §3).
- **Destructor**: `clear()` then delete the sentinel. **The sentinel is not an element** and `clear()`
  will not touch it.

> **A move constructor that leaves `o.sentinel` dangling is the classic bug here.** `~List` will then
> run on the moved-from object and delete a sentinel that the new owner is using. **`o.init()` is not
> optional.**

---

## 5. Iterator Invalidation, Derived

You now have the implementation, so the rules are not memorisation — they are consequences.

**Inserting into a `list` invalidates nothing.** `insert` allocates a new node and rewires two
pointers. Every existing node keeps its address, so every existing iterator still points at the same
element.

**Erasing invalidates only the erased element's iterator**, because only that node is deleted.

**Contrast `std::vector`**, whose elements live in one array: growing means allocating a bigger array
and moving everything, so every iterator, pointer and reference into the old array dangles (L11 §6).

> **This is the third question answered.** The invalidation rules in Week 3's table were not arbitrary
> library policy; they fall out of where the elements live. **A node-based container cannot invalidate
> on insertion, and a contiguous one cannot avoid it.**

---

## 6. What It Looks Like Working

```cpp
List<int> l{5,3,8,1,9};
```

```
size=5 front=5 back=9
forward : 5 3 8 1 9
backward: 9 1 8 3 5
```

The backward traversal is the sentinel earning its keep: `--end()` is the last element, and the loop
terminates at `begin()` with no null checks.

And with `std::string`, exercising a `T` that owns its own resource:

```
strings : alan ada grace
deep copy: s=3 s2=2
assign+self: 3
```

Sanitizer-clean. **The `std::string` case is the one that matters** — it proves the container never
assumed anything about `T` beyond copy/move-constructibility, which is what makes it a container rather
than a list of ints.

---

## 7. What Is Deliberately Missing

Your list has no `operator[]`, no `at()`, and no `sort` member. That is correct.

- **No `operator[]`** — random access on a linked list is $O(n)$, and an interface that looks like
  indexing must be $O(1)$. **Lecture 20 §5** develops this.
- **No `sort`** — `std::list::sort` exists because the generic `std::sort` cannot work on bidirectional
  iterators (L10 §5). Writing it is a merge sort on pointers, and it is one of Project 1's optional
  extensions.

**An interface is defined as much by what it refuses as by what it offers.**

---

## 8. Summary

| Idea | The point |
| --- | --- |
| Node is private and nested | An implementation detail with no external name |
| `prev`/`next` are raw pointers | They are structure, not ownership. **The list owns the nodes** |
| The sentinel | Converts four insertion cases into **one** |
| `end()` is the sentinel | A real node that must not be dereferenced — the half-open range |
| Rule of **Five**, not Zero | You are the resource wrapper; there is nothing to delegate to |
| Move must leave a valid list | `o.init()`, or the moved-from destructor deletes a live sentinel |
| Copy-and-swap assignment | Self-assignment and the strong guarantee, again for free |
| Invalidation is a **consequence** | Node-based cannot invalidate on insert; contiguous cannot avoid it |
| No `operator[]` | An honest interface refuses what it cannot do efficiently |

---

## 9. Exercises

**1.** Write `insert` for a `head`/`tail`/null design and count the cases. Then write it for the
sentinel design. **Report both line counts.**

**2.** Implement the sentinel list and verify forward and backward traversal on `{5,3,8,1,9}`.

**3.** Write the move constructor **without** `o.init()`. Move from a list, then let both go out of
scope. **Paste the sanitizer report** and explain it.

**4.** Test your list with `T = std::string`. Copy one, modify the copy, and show the original is
unchanged. **Why is this a better test than `T = int`?**

**5.** Take an iterator to the third element. Insert ten elements before it and erase two elsewhere.
**Is your iterator still valid?** Justify from your implementation, not from a table.

**6.** Add `operator[]` to your list, implemented by looping. It will work. **Give two reasons not to
ship it**, one about complexity and one about what the caller can see.

**7.** Your `clear()` calls `pop_front()` repeatedly. **Is that $O(n)$ or $O(n^2)$?** Justify, then
check by timing at 10⁴, 10⁵ and 10⁶ elements.

---

## 10. Next

**Lecture 20** writes the iterator the copy constructor above already assumed. It is the part that
makes your container a *container* rather than a data structure — the point at which
`std::accumulate`, `std::find` and `std::reverse` start working on something you wrote.

---

*PROG 102 · Week 6 · Lecture 19 · © CSE Department*
