# CS 101 · Week 7: Data Structures I — Lists, Stacks, and Queues

---

## Contents

```
CS101_Week7/
│
├── README.md                                    ← You are here
│
├── lectures/
│   ├── L22 ADTs and Dynamic Arrays.md           ← Wed: ADT vs implementation, Python
│   │                                                 lists as dynamic arrays, why lst[i]
│   │                                                 is O(1), why insert(0,x)/pop(0) are
│   │                                                 O(n), tuples vs lists
│   ├── L23 Linked Lists.md                      ← Thu: Node/pointer model, singly linked
│   │                                                 list built from scratch, tail-pointer
│   │                                                 optimization, doubly linked lists,
│   │                                                 memory overhead analysis
│   └── L24 Stacks Queues and Deques.md          ← Fri: Stack ADT (array + linked impls),
│                                                     Queue ADT (why raw list is wrong,
│                                                     deque is right), full deque coverage,
│                                                     bracket matching, round-robin scheduling
│
├── lab/
│   ├── LAB 7 Memory Profiling.md                 ← Tue of W8: sys.getsizeof deep dive, build all
│   │                                                 4 structures, empirical memory + speed
│   │                                                 comparison, bracket matcher, undo/redo
│   └── data_structures_starter.py               ← Lab starter — Node/LinkedList/DLL/Stack/
│                                                     Queue scaffolds + full test suite
│
├── assignments/
│   ├── QUIZ 7 Week 7 Wednesday.md                    ← In-class quiz (covers Week 6)
│   ├── PS 7 Stacks and Queues.md                 ← Problem Set 7 (due Friday Week 8)
│   ├── ps7_starter.py                           ← Full scaffold: array/linked stack+queue,
│   │                                                 extended LL ops, benchmark, 2-stack
│   │                                                 expression evaluator
│   └── PROJECT 1 Data Analysis Tool.md           ← Project 1 (assigned this week,
│                                                     due Week 9) — full spec + rubric
│
├── resources/
│   ├── weather_data.csv                         ← Messy sample dataset for Project 1
│   │                                                (missing values, malformed rows,
│   │                                                duplicates, implausible values)
│   └── Reading Guide Week 7.md                   ← 3 experimentation sessions, full
│                                                      complexity reference card, self-test
│
└── solutions_instructor/
    └── LAB 7 Solutions.md                        ← Expected answers and marking notes
```

---

## Week 7 at a Glance

**Theme:** The first data structures week. Everything you've written so far has used Python's built-in `list` without asking *why* its operations have the complexity they do. This week opens the hood — first on arrays, then on the pointer-based alternative — and gives you the vocabulary (Abstract Data Types) to reason about *any* data structure you'll ever encounter.

| Day | Event | Topic |
|-----|-------|-------|
| Wed | Lecture 22 + Quiz 7 | ADTs vs implementations; Python lists as dynamic arrays; O(1) vs O(n) operations |
| Thu | Lecture 23 | Linked lists from scratch: singly linked, tail-pointer optimization, doubly linked |
| Fri | Lecture 24 + PS7 released | Stack and Queue ADTs; array vs linked implementations; deques; real applications |
| Tue (W8) | Lab 7 (graded) | Build every structure; profile memory; benchmark operations; build applications |

**📌 Project 1 was assigned this week** (due Week 9) — see [[PROJECT 1 Data Analysis Tool]]. Start early; it requires synthesizing nearly everything from Weeks 0–7.

---

## Your To-Do List

### Before Wednesday
- [ ] Read Guttag Ch. 5.1–5.2 (tuples, lists, mutability)
- [ ] Review Week 6 — Quiz 7 covers Big-O, recurrences, Master Theorem

### Wednesday
- [ ] Quiz 7 (10 min — covers Week 6)
- [ ] Notes for L22

### Before Thursday
- [ ] REPL Session A from Reading Guide (feel the list resize behavior)
- [ ] REPL Session B (measure the front/back asymmetry directly)

### Thursday
- [ ] Notes for L23
- [ ] REPL Session C (nested-tuple linked list intuition)

### Tuesday Lab, Week 8 (Required, Graded)
- [ ] Complete memory profiling exercises (Part 1)
- [ ] Implement all 4 structures in `data_structures.py` — full test suite passes
- [ ] Run empirical memory and speed comparisons
- [ ] Build the bracket matcher and undo/redo applications
- [ ] TA checkoff

### Friday
- [ ] Notes for L24
- [ ] Read PS7 completely; **also read Project 1 in full**

### Weekend
- [ ] Start PS7 — at minimum A1–A2 (written) and B1–B2 (array/linked stack+queue)
- [ ] **Start Project 1** — at minimum, write `load_data` and `validate_record` against the provided `weather_data.csv`

---

## The Central Ideas of Week 7

**1. An Abstract Data Type separates "what" from "how."**
A Stack is defined by push/pop/LIFO — nothing about arrays or linked lists. Any implementation satisfying that contract is a valid Stack. This separation lets you choose implementations based on performance needs without changing any code that *uses* the ADT.

**2. Python's list is a dynamic array of pointers, not a "raw" array.**
This explains everything: O(1) indexing (direct address computation), O(1) amortized append (over-allocated capacity), and O(n) front operations (must shift every element).

**3. Linked lists trade array strengths for array weaknesses — precisely.**
No O(1) random access (must follow pointers from the head). But O(1) insertion/removal at the head, because there's no shifting — just re-pointing.

**4. Small extra bookkeeping eliminates entire complexity classes.**
A tail pointer turns O(n) append into O(1). A prev pointer (doubly linked) turns O(n) tail-removal into O(1). This pattern — spend a little memory, save a lot of time — recurs throughout data structure design.

**5. The SAME ADT can have wildly different implementations — and the "obviously correct" choice is sometimes wrong.**
A Stack backed by a Python list works beautifully if you use the *end* as the top. A Queue backed by a raw Python list is a performance trap (`pop(0)` is O(n)) — you need `collections.deque` instead.

**6. Real applications make these abstractions concrete.**
Bracket matching (compilers), undo/redo (every editor you've ever used), round-robin scheduling (operating systems) — all directly implement the Stack/Queue ADTs you built this week.

---

## Quick Self-Check

Without notes:

1. What is an ADT? Give the Stack ADT's specification in one sentence.
2. Why is `lst[i]` O(1) for a Python list? Give the address formula.
3. Why is `lst.insert(0, x)` O(n)?
4. What does a tail pointer optimize in a singly linked list? From what complexity to what?
5. What does a prev pointer (doubly linked) optimize that a tail pointer alone cannot?
6. Which end of a Python list should back a Stack? Why?
7. Why is `collections.deque` the right choice for a Queue, but a raw Python list is not?
8. Is indexing into the middle of a `deque` O(1)? Why or why not?
9. Name the two-stack algorithm used to evaluate a fully-parenthesized expression.
10. Name one real ADT application from Friday's lecture and the operations it relies on.

*(Answers: 1. specification of behavior, independent of implementation; push/pop/LIFO. 2. address = base + i×pointer_size; O(1) arithmetic. 3. must shift every existing element right by one. 4. append; O(n)→O(1). 5. removal from the tail; O(n)→O(1). 6. the end — append/pop are both O(1) there. 7. deque gives O(1) at both ends; list's pop(0) is O(n). 8. No, O(n) — deque is internally block-linked, not one contiguous array. 9. the operand-stack/operator-stack shunting algorithm. 10. e.g. bracket matching via Stack; push openers, pop-and-check on closers.)*

---

## Algorithms and Patterns Introduced This Week

| Pattern | Complexity | Key Idea |
|---------|-----------|----------|
| Dynamic array indexing | O(1) | Direct address computation from base + offset |
| Dynamic array append | O(1) amortized | Over-allocation; occasional O(n) resize averages out |
| Linked list prepend | O(1) | New node just points to old head; no shifting |
| Linked list append (with tail) | O(1) | Tail pointer eliminates the traversal-to-find-end |
| Doubly linked tail removal | O(1) | prev pointer eliminates the traversal-to-find-new-tail |
| Stack via array | O(1) all ops | Use array's END as the top |
| Queue via deque | O(1) all ops | Enqueue right, dequeue left — both native O(1) |
| Bracket matching | O(n) | Stack-based; push openers, match on closers |
| Two-stack expression evaluation | O(n) | Operand stack + operator stack; classic shunting-yard simplification |

---

*CS 101 · Week 7 · © CSE Department*
