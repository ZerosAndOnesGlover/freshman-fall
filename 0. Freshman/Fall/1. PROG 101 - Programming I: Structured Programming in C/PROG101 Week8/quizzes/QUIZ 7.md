# PROG 101 · Quiz 7
## Week 8, Tuesday — In-Class Assessment

**Date:** Tuesday 17 November 2026 · 10:00–10:10 (start of Week 8, Lecture 1)
**Covers:** Week 7 material
**Duration:** 10 minutes · Closed book · 20 points

---

## Section A — Multiple Choice (2 pts each)

**1.** Given:
```c
struct P { char a; int b; char c; };
```
On a typical 64-bit system, what is `sizeof(struct P)` most likely to be?

- (A) 6
- (B) 8
- (C) 12
- (D) 16

---

**2.** What is the size of this union?

```c
union U {
    char   c;
    int    i;
    double d;
};
```

- (A) 1 (smallest member)
- (B) 4 (sum of char and int)
- (C) 8 (size of largest member)
- (D) 13 (sum of all members)

---

**3.** Given `struct Point *p;`, which correctly accesses the field `x`?

- (A) `p.x`
- (B) `p->x`
- (C) `*p.x`
- (D) `p*.x`

---

**4.** Why must a self-referential struct like a linked list node use a tag name?

```c
typedef struct ____ {
    int data;
    struct ____ *next;
} Node;
```

- (A) `typedef` doesn't support pointers
- (B) The typedef name `Node` doesn't exist yet at the point where `next` is declared
- (C) C requires all structs to have tag names
- (D) It's a style convention with no technical requirement

---

**5.** In the pointer-to-pointer deletion technique (`Node **headp`), what does `*pp = cur->next;` accomplish?

- (A) It frees the current node
- (B) It redirects whichever pointer currently points to `cur` (either `head` or a previous node's `next`) to skip over `cur`
- (C) It advances `cur` to the next node
- (D) It sets `cur` itself to point to the next node

---

## Section B — Short Answer (2 pts each)

**6.** Draw the byte layout (with offsets) for this struct, showing all padding:

```c
struct Mixed {
    short s;   /* 2 bytes */
    char  c;   /* 1 byte  */
    int   i;   /* 4 bytes */
};
```

```
Offset: 0    1    2    3    4    5    6    7
Field:  [    ][    ][    ][    ][    ][    ][    ][    ]
```

`sizeof(struct Mixed)` = ______

---

**7.** What is wrong with this code, and what will Valgrind report?

```c
Node *cur = head;
while (cur != NULL) {
    free(cur);
    cur = cur->next;
}
```

Bug: `_________________________________________________________________`

Fix: `_________________________________________________________________`

---

**8.** Trace the reversal of this list. Show the state of `prev`, `cur`, `next` at each step.

```c
/* List: [5] -> [10] -> [15] -> NULL */
Node *reverse_list(Node *head) {
    Node *prev = NULL;
    Node *cur  = head;
    while (cur != NULL) {
        Node *next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
    }
    return prev;
}
```

| Step | prev | cur | next |
|------|------|-----|------|
| Start | | | |
| 1 | | | |
| 2 | | | |
| 3 | | | |

Final list order: `___________________________________________________`

---

**9.** What does this tagged union pattern guarantee, and what happens if you forget to check the tag?

```c
typedef struct {
    enum { TYPE_A, TYPE_B } tag;
    union { int a_val; double b_val; } data;
} Variant;
```

```
Guarantee: __________________________________________________________

If you read data.b_val when tag == TYPE_A: ___________________________
```

---

**10.** Why is a doubly linked list's `dlist_delete_node(list, node)` operation O(1), while a singly linked list needs O(n) to delete an arbitrary node given only a pointer to it?

```
_____________________________________________________________________

_____________________________________________________________________
```

---

## Answer Key (Instructor Copy)

**1. (C) 12** — Layout: `a` at offset 0 (1 byte), 3 padding bytes to align `b` at offset 4, `b` at offset 4-7 (4 bytes), `c` at offset 8 (1 byte), then 3 padding bytes to make total size a multiple of 4 (the alignment of the largest member, `int`). Total: 12 bytes.

**2. (C) 8** — A union's size equals its largest member. `double` is 8 bytes, which exceeds `char` (1) and `int` (4). All members share the same 8 bytes of storage.

**3. (B) `p->x`** — `p` is a pointer to a struct, so the arrow operator dereferences and accesses in one step. `p.x` is a compile error (`.` requires a struct value, not a pointer). `*p.x` is also wrong due to operator precedence (`.` binds tighter than `*`).

**4. (B)** — At the point `struct ____ *next;` is being parsed, the `typedef` statement is not yet complete — the name `Node` does not exist as a type yet. The tag name (e.g., `struct Node`) is visible immediately upon the opening of the struct body, so it can be used for the self-reference. The typedef name only becomes usable after the full declaration (including the closing `} Node;`) is processed.

**5. (B)** — `pp` is a pointer to whichever pointer variable currently "points at" `cur` — this could be the `head` variable itself (if `cur` is the first node) or some earlier node's `next` field. Setting `*pp = cur->next` updates that variable to skip over `cur`, correctly unlinking it in every case without needing separate head/non-head logic.

**6.**
```
Offset: 0    1    2    3    4    5    6    7
Field:  [--s--][ c ][pad][------i------]
```
`s` occupies offsets 0-1 (short, 2 bytes). `c` at offset 2 (1 byte). 1 padding byte at offset 3 (to align `i` on a 4-byte boundary). `i` occupies offsets 4-7. Total size: **8 bytes**.

**7.** Bug: `free(cur)` is called, then `cur->next` is accessed — but `cur` was just freed, so `cur->next` reads freed memory (use-after-free, undefined behavior). Fix:
```c
Node *cur = head;
while (cur != NULL) {
    Node *next = cur->next;   /* save BEFORE freeing */
    free(cur);
    cur = next;
}
```
Valgrind would report: "Invalid read of size 8" (reading the `next` pointer field from freed memory).

**8.**
| Step | prev | cur | next |
|------|------|-----|------|
| Start | NULL | 5 | — |
| 1 | 5 | 10 | 10 (next saved as 10 before relink) |
| 2 | 10 | 15 | 15 |
| 3 | 15 | NULL | NULL |

Final list order: `[15] -> [10] -> [5] -> NULL`

(Exact intermediate table values may vary in presentation, but the key trace: after step 1, `5->next = NULL`, prev=5, cur=10; after step 2, `10->next=5`, prev=10, cur=15; after step 3, `15->next=10`, prev=15, cur=NULL; loop exits, return prev=15.)

**9.**
- Guarantee: the tag (`TYPE_A` or `TYPE_B`) tells you which union member was most recently written and is therefore valid to read.
- If you read `data.b_val` when `tag == TYPE_A`: you are reinterpreting the bits that were written as an `int` as if they were a `double` instead — this produces a meaningless/garbage value (or in strict terms, is undefined behavior), because the two types have completely different bit representations.

**10.** In a doubly linked list, each node stores a `prev` pointer directly, so deleting `node` only requires reading `node->prev` and `node->next` to relink the surrounding nodes — no search needed, O(1). In a singly linked list, nodes do not know their predecessor; to delete a given node you must first find the node whose `next` field points to it, which requires walking from the head — O(n) in the worst case.
