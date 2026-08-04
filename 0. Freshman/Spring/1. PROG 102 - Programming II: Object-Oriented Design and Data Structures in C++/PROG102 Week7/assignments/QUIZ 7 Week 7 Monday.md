# PROG 102 · Quiz 7
## Week 7 · Monday, start of lecture · 15 minutes · 20 points

**Covers Week 6** — Lectures 19–21: implementing a linked list, iterators, and a BST.

**Closed book. No devices.** Answer on this sheet.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* A doubly linked list can be built with `head`/`tail` pointers and nulls, or with a
**sentinel** node linking to itself.

**(a)** *(2)* How many cases does `insert` need in each design?

**(b)** *(1)* What is `end()` in the sentinel design?

<br><br><br>

---

**Q2.** *(3)* Your `List<T>` needed all five special members. Your `BST<T>` with `unique_ptr` children
needed none.

**Explain the difference in two sentences.**

<br><br><br>

---

**Q3.** *(4)* `std::iterator_traits` reads five member typedefs from your iterator.

**(a)** *(2)* Name any three.

**(b)** *(2)* `iterator_category` is a **tag type**. What is it used for, and at what time — compile
time or run time?

<br><br><br>

---

**Q4.** *(4)* `std::sort(l.begin(), l.end())` on your list fails with
`no match for 'operator-'`.

**(a)** *(1)* Is this a bug in your iterator?

**(b)** *(3)* You could add `operator-` by looping, and `std::sort` would then compile and produce
**correctly sorted output**. Give the measured complexity you would get, and say why adding it is
worse than leaving it out.

<br><br><br>

---

**Q5.** *(3)* A move constructor for `List<T>` steals the sentinel pointer.

**(a)** *(2)* What must it leave the moved-from list as? Be precise — "empty" is not precise enough.

**(b)** *(1)* What goes wrong if it does not?

<br><br><br>

---

**Q6.** *(3)* A chain of `unique_ptr`-linked nodes destroys fine at 500,000 nodes and **segfaults** at
1,000,000.

**(a)** *(2)* Why?

**(b)** *(1)* State the general rule, in one sentence. It should not mention `unique_ptr`.

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 7 · Quiz 7 · © CSE Department*
