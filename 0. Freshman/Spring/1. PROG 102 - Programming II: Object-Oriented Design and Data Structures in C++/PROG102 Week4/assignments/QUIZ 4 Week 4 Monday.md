# PROG 102 · Quiz 4
## Week 4 · Tuesday, start of lecture · 15 minutes · 20 points

**Covers Week 3** — Lectures 10–12: iterators, containers, algorithms.

**Closed book. No devices.** Answer on this sheet.

Name: ________________________  Section: ______  Date: ____________

---

**Q1.** *(3)* `std::sort(l.begin(), l.end())` on a `std::list<int>` does not compile. The error is
`no match for 'operator-'`.

**(a)** *(1)* Which iterator category does `std::sort` require?

**(b)** *(1)* Which does `std::list` provide?

**(c)** *(1)* What should you call instead?

<br><br><br>

---

**Q2.** *(3)* Fill in the iterator category:

| Container | Category |
| --- | --- |
| `std::vector` | |
| `std::list` | |
| `std::map` | |

<br><br>

---

**Q3.** *(4)* Measured: inserting 50,000 random integers **in sorted order** was **178× faster** into a
`vector` than into a `list`. Inserting 100,000 elements **at the front** was **128× faster** into a
`list`.

**(a)** *(2)* Both results are correct. Explain why they point in opposite directions.

**(b)** *(2)* What does a complexity table describe, and what does it leave out?

<br><br><br>

---

**Q4.** *(3)* `std::accumulate(v.begin(), v.end(), 0)` where `v` is `std::vector<double>{0.5,0.5,0.5}`
returns **0**, not 1.5.

**(a)** *(2)* Why?

**(b)** *(1)* What is the fix?

<br><br><br>

---

**Q5.** *(3)* After `std::remove(v.begin(), v.end(), 2)` on `{1,2,3,2,4,2,5}`:

**(a)** *(1)* What is `v.size()`?

**(b)** *(1)* Why can the algorithm not do better?

**(c)** *(1)* Write the idiom that actually removes the elements.

<br><br><br>

---

**Q6.** *(2)* `std::find(s.begin(), s.end(), k)` on a 100,000-element `std::set` was measured about
**6,000×** slower than `s.find(k)`.

**Why can the generic algorithm not do better?**

<br><br>

---

**Q7.** *(2)* `int& i = vi[0];` compiles for `std::vector<int>`. `bool& b = vb[0];` does not compile
for `std::vector<bool>`.

**In one sentence, why?**

<br><br>

---

**Total: 20 points**

*PROG 102 · Week 4 · Quiz 4 · © CSE Department*
