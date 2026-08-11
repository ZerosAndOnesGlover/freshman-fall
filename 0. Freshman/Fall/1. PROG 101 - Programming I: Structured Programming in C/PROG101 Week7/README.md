# PROG 101 · Week 7: Structures, Unions, and Linked Lists
## Composite Types · Tagged Unions · Building Real Data Structures

---

## Week Overview

Week 7 is where C stops being about individual values and starts being about **data structures**. Structs let you group related fields. Unions let you represent "one of several possibilities." Combined with the pointers from Week 5 and heap allocation from Week 6, you can now build the linked list — the first genuine data structure of your career, and the gateway to trees, graphs, and every dynamic structure that follows.

---

## Schedule

| Day | Event | Topic | Duration |
|-----|-------|-------|----------|
| Tuesday | Lecture 1 | Structures: Composite Types and Memory Layout | 50 min |
| Wednesday | Lecture 2 | Unions, Enumerations, and Bit Fields | 50 min |
| Thursday | Lecture 3 | Linked Lists: Structs and Pointers Combined | 50 min |
| Monday (Week 8) | **Lab 7** | Struct Layout + Tagged Unions + Linked List Library | 2 hours |

---

## Files in This Package

```
PROG101 Week7/
├── README.md
├── lectures/
│   ├── Lecture 01 Structures.md                    ← Structs, padding, ->, nested structs, typedef
│   ├── Lecture 02 Unions Enums Bitfields.md         ← Unions, tagged unions, enums, bit fields
│   └── Lecture 03 Linked Lists.md                   ← Nodes, traversal, insert/delete, reversal, cycles
├── lab/
│   └── LAB 7 Structs Linkedlist.md                   ← Layout investigation + shapes + full linked list
├── assignments/
│   └── Problem Set 7.md                             ← 5 problems: layout, tagged unions, doubly linked list, student system, state machine
├── quizzes/
│   └── QUIZ 6.md                                    ← 10 questions + full answer key (sat Tuesday, covers Week 6)
├── resources/
│   └── Week 7 Struct Union Linkedlist Reference.md   ← Layout rules, syntax cheat sheet, pattern library, common bugs
└── solutions_instructor/
    └── LAB 7 Solutions.md                           ← Instructor only
```

---

## Learning Objectives

After Week 7, you will be able to:

- [ ] Define structs and predict their memory layout including padding
- [ ] Reorder struct fields to minimize memory footprint
- [ ] Use `.` and `->` correctly and know when each applies
- [ ] Pass structs by value vs by pointer, understanding the copy cost tradeoff
- [ ] Build nested structs and arrays of structs
- [ ] Use `typedef` idiomatically, including the anonymous-struct pattern
- [ ] Explain why unions share memory and predict `sizeof` for any union
- [ ] Build a tagged union (variant type) with a tag + union pattern
- [ ] Use enums for readable named constants and leverage `-Wswitch`
- [ ] Implement a complete singly linked list: insert, delete, search, reverse
- [ ] Use the pointer-to-pointer technique to eliminate special-case logic
- [ ] Apply the slow/fast pointer technique for cycle detection and finding the middle
- [ ] Manage linked list memory correctly with zero leaks (Valgrind-verified)

---

## Textbook Reading

| Lecture | K&R | King | Other |
|---------|-----|------|-------|
| L1: Structures | Ch. 6 (through §6.4) | Ch. 16 | CS:APP §3.9.3 |
| L2: Unions/Enums | §6.8 | Ch. 16 | — |
| L3: Linked Lists | §6.5 | Ch. 17 | CLRS Ch. 10 |

---

## The Key Insights of This Week

### On Structs
A struct's `sizeof` is not the sum of its fields — the compiler inserts padding to satisfy alignment requirements. This is not an implementation detail you can ignore: field order changes memory footprint, and at scale (millions of records), that difference is real memory and real cache performance.

### On Unions
A union is not "a struct that's more flexible" — it is **literally the same bytes** interpreted differently depending on which member you access. Reading a member you didn't just write reinterprets bits, which is either a deliberate technique (type punning) or a bug (forgetting to check the tag).

### On Linked Lists
The linked list is your first encounter with a genuine trade-off in data structure design: you give up O(1) random access to gain O(1) insertion/deletion at arbitrary positions (given a pointer to the location). Every data structure course you take from here forward is a variation on this theme — trading one operation's efficiency for another's.

---

## Common Week 7 Mistakes

**Forgetting padding when predicting struct size:**
```c
struct S { char a; int b; };
/* sizeof is 8, not 5 — 3 padding bytes after 'a' to align 'b' */
```

**Comparing structs with `==`:**
```c
if (p1 == p2)   /* COMPILE ERROR — write a comparison function instead */
```

**Reading the wrong union member:**
```c
union U u;
u.i = 42;
printf("%f\n", u.f);   /* garbage — reads the int's bits as a float */
```

**Using `Node` instead of `struct Node` inside a self-referential typedef:**
```c
typedef struct {
    int data;
    Node *next;   /* ERROR: 'Node' doesn't exist yet at this point */
} Node;
/* FIX: use a tag */
typedef struct Node {
    int data;
    struct Node *next;   /* CORRECT */
} Node;
```

**Use-after-free while freeing a list:**
```c
while (cur) { free(cur); cur = cur->next; }   /* WRONG */
while (cur) { Node *n = cur->next; free(cur); cur = n; }   /* CORRECT */
```

**Forgetting to reassign `head` after insert/delete:**
```c
list_insert_front(head, 5);         /* WRONG: return value discarded */
head = list_insert_front(head, 5);  /* CORRECT */
```

---

## Challenge Problems (Optional)

1. **In-place linked list sort** — implement merge sort on a singly linked list (split into two halves using slow/fast pointers, recursively sort each half, merge). O(n log n) time, O(log n) space (recursion stack only — no array conversion allowed).

2. **LRU Cache** — combine a doubly linked list with a hash table (conceptually — you can use a simple array-based lookup for this exercise) to implement a Least Recently Used cache with O(1) `get` and `put`.

3. **Polynomial as a Linked List** — represent a polynomial as a linked list of `{coefficient, exponent}` nodes sorted by descending exponent. Implement addition and multiplication of two polynomials.

4. **Union-Based Small Vector Optimization** — design a struct that stores up to 4 integers inline (in a union with a fixed array) but falls back to a heap-allocated array for more than 4 — a simplified version of "small vector optimization" used in real C++ standard libraries.
