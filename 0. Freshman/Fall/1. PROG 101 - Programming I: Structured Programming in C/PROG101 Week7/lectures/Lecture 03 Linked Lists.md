# PROG 101 — Programming I: Structured Programming in C
## Week 7 · Lecture 3: Linked Lists — Structs and Pointers Combined

---

## Lecture Goals

By the end of this lecture you will:
- Understand why linked lists exist as an alternative to arrays
- Build a singly linked list from scratch: insert, delete, search, traverse
- Understand the pointer-to-pointer technique for clean insertion/deletion
- Build a doubly linked list and understand its tradeoffs
- Correctly manage memory for every node (no leaks, no dangling pointers)

---

## 1. Arrays vs Linked Lists

You've used arrays extensively. Arrays have two structural limitations:

1. **Fixed size** (unless you use a dynamic array, which still requires periodic O(n) reallocation)
2. **Expensive insertion/deletion in the middle** — O(n) because elements must shift

A **linked list** solves both by giving up something else: **direct indexing**. Elements are not contiguous in memory — each element (a **node**) holds a pointer to the next element.

```
Array:                          Linked List:
┌────┬────┬────┬────┬────┐      ┌────┬──┐   ┌────┬──┐   ┌────┬──┐
│ 10 │ 20 │ 30 │ 40 │ 50 │      │ 10 │ ●┼──▶│ 20 │ ●┼──▶│ 30 │NULL│
└────┴────┴────┴────┴────┘      └────┴──┘   └────┴──┘   └────┴──┘
Contiguous memory                Scattered memory, connected by pointers
arr[2] = O(1) direct access      Must walk from head: O(n) to reach node 2
Insert in middle: O(n) shift     Insert given a pointer to the spot: O(1)
```

| Operation | Array | Linked List |
|-----------|-------|-------------|
| Access element i | O(1) | O(n) |
| Insert/delete at front | O(n) | O(1) |
| Insert/delete at known position | O(n) | O(1) (given the pointer) |
| Insert/delete after search | O(n) | O(n) (search) + O(1) (insert) |
| Memory overhead | None | One pointer per element |
| Cache locality | Excellent | Poor (nodes scattered) |

**The engineering lesson:** there is no universally "better" data structure — only tradeoffs suited to different access patterns. Use arrays when you need random access and cache performance. Use linked lists when you need frequent insertion/deletion at arbitrary positions without shifting.

---

## 2. Defining a Node

```c
typedef struct Node {
    int data;
    struct Node *next;
} Node;
```

Recall from Lecture 1: this **must** use the tag `Node` inside the struct body (`struct Node *next`), because the typedef name `Node` doesn't exist yet at that point in the declaration.

A single node:

```c
Node *make_node(int value) {
    Node *n = malloc(sizeof(Node));
    if (n == NULL) {
        fprintf(stderr, "malloc failed\n");
        exit(1);
    }
    n->data = value;
    n->next = NULL;
    return n;
}
```

Building a list manually:

```c
Node *head = make_node(10);
head->next = make_node(20);
head->next->next = make_node(30);

/* head → [10] → [20] → [30] → NULL */
```

---

## 3. Traversal — Walking the List

```c
void print_list(const Node *head) {
    const Node *current = head;
    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\n");
}
```

**The traversal pattern is the single most important idiom in linked list code.** Memorize it:

```c
Node *current = head;
while (current != NULL) {
    /* process current->data */
    current = current->next;
}
```

Every linked list operation — search, count, sum, print — is a variation of this loop.

```c
int list_length(const Node *head) {
    int count = 0;
    for (const Node *cur = head; cur != NULL; cur = cur->next) {
        count++;
    }
    return count;
}

int list_sum(const Node *head) {
    int sum = 0;
    for (const Node *cur = head; cur != NULL; cur = cur->next) {
        sum += cur->data;
    }
    return sum;
}

Node *list_find(Node *head, int target) {
    for (Node *cur = head; cur != NULL; cur = cur->next) {
        if (cur->data == target) return cur;
    }
    return NULL;
}
```

---

## 4. Insertion

### Insert at the Front (O(1))

```c
Node *insert_front(Node *head, int value) {
    Node *n = make_node(value);
    n->next = head;    /* new node points to the old head */
    return n;          /* new node is the new head */
}

/* Usage: */
head = insert_front(head, 5);   /* MUST reassign head — the head may change */
```

**Why must the caller reassign `head`?** Because `head` is a local variable in `main` (or wherever it's declared) — pass-by-value applies to pointers too. `insert_front` receives a copy of the `head` pointer; it cannot change what the caller's `head` variable points to unless it returns the new value (or unless we pass `Node **`, covered below).

### Insert at the End (O(n) — must walk to find the end)

```c
Node *insert_end(Node *head, int value) {
    Node *n = make_node(value);

    if (head == NULL) {
        return n;    /* empty list — new node becomes the head */
    }

    Node *cur = head;
    while (cur->next != NULL) {
        cur = cur->next;
    }
    cur->next = n;
    return head;     /* head didn't change, but we return it for consistency */
}
```

### Insert After a Given Node (O(1) given the pointer)

```c
void insert_after(Node *prev, int value) {
    assert(prev != NULL);
    Node *n = make_node(value);
    n->next = prev->next;
    prev->next = n;
}
```

---

## 5. Deletion

Deletion is trickier than insertion because you must reconnect the list around the removed node **and** free its memory.

### Delete the Front Node

```c
Node *delete_front(Node *head) {
    if (head == NULL) return NULL;    /* nothing to delete */

    Node *old_head = head;
    head = head->next;    /* advance head to the second node */
    free(old_head);       /* free the removed node */
    return head;          /* caller MUST reassign: head = delete_front(head) */
}
```

### Delete a Node with a Specific Value

```c
Node *delete_value(Node *head, int target) {
    /* Case 1: list is empty */
    if (head == NULL) return NULL;

    /* Case 2: the head itself is the target */
    if (head->data == target) {
        Node *new_head = head->next;
        free(head);
        return new_head;
    }

    /* Case 3: target is somewhere after the head */
    Node *prev = head;
    Node *cur  = head->next;
    while (cur != NULL) {
        if (cur->data == target) {
            prev->next = cur->next;   /* unlink cur */
            free(cur);
            return head;              /* head unchanged */
        }
        prev = cur;
        cur  = cur->next;
    }

    return head;   /* target not found — list unchanged */
}
```

**The pattern to internalize:** to delete a node, you need a pointer to the **previous** node (to redirect its `next`), or special-case the head. This is why deletion code always tracks both `prev` and `cur`.

---

## 6. The Pointer-to-Pointer Technique — Eliminating Special Cases

The head-vs-rest special-casing above is common but can be eliminated entirely using a **pointer to the head pointer** (`Node **`). This is a more advanced but significantly cleaner technique:

```c
/* headp is a POINTER TO the variable that holds the head pointer.
 * This lets us modify the caller's head variable directly — no need
 * to return the new head, and no special case for deleting the head. */
void delete_value_v2(Node **headp, int target) {
    Node *cur = *headp;      /* dereference to get the actual head */

    /* pp always points to the pointer that must be updated to skip cur */
    Node **pp = headp;

    while (cur != NULL) {
        if (cur->data == target) {
            *pp = cur->next;   /* redirect: either headp or prev->next */
            free(cur);
            return;
        }
        pp  = &cur->next;      /* next iteration: update THIS node's next field */
        cur = cur->next;
    }
}

/* Usage: */
Node *head = ...;
delete_value_v2(&head, 30);   /* pass the ADDRESS of head */
/* head is updated automatically — no reassignment needed */
```

This technique is subtle on first encounter but immensely powerful: `pp` always points to "the pointer that currently points to `cur`" — whether that's the `head` variable itself or some previous node's `next` field. Setting `*pp = cur->next` correctly unlinks `cur` in every case, with zero special-casing.

**Master this pattern.** It appears throughout systems code (the Linux kernel uses this exact technique extensively) and is a genuine mark of C fluency.

---

## 7. Freeing the Entire List

Every node allocated with `malloc` must eventually be freed. Never lose the pointer to the next node before freeing the current one:

```c
void free_list(Node *head) {
    Node *cur = head;
    while (cur != NULL) {
        Node *next = cur->next;   /* save next BEFORE freeing cur */
        free(cur);
        cur = next;
    }
}
```

**The classic bug:**
```c
/* WRONG — use-after-free and lost pointer */
while (cur != NULL) {
    free(cur);
    cur = cur->next;   /* UNDEFINED BEHAVIOR: cur was just freed! */
}
```

Always save `next` before freeing `cur`.

---

## 8. Reversing a Linked List (In-Place)

A classic and instructive exercise — reverse the list by relinking pointers, using no extra memory:

```c
Node *reverse_list(Node *head) {
    Node *prev = NULL;
    Node *cur  = head;

    while (cur != NULL) {
        Node *next = cur->next;   /* save next before we overwrite it */
        cur->next  = prev;        /* reverse the link */
        prev = cur;                /* advance prev */
        cur  = next;                /* advance cur */
    }

    return prev;   /* prev is now the new head */
}
```

Trace through `[10]→[20]→[30]→NULL`:

| Step | prev | cur | next | Action |
|------|------|-----|------|--------|
| Start | NULL | 10 | — | |
| 1 | NULL | 10 | 20 | `10->next = NULL`; prev=10, cur=20 |
| 2 | 10 | 20 | 30 | `20->next = 10`; prev=20, cur=30 |
| 3 | 20 | 30 | NULL | `30->next = 20`; prev=30, cur=NULL |
| End | 30 | NULL | — | loop exits, return prev=30 |

Result: `[30]→[20]→[10]→NULL`. This O(n) time, O(1) space in-place reversal is a foundational algorithm — you will use this exact pattern (three pointers marching in lockstep) throughout your career.

---

## 9. Doubly Linked Lists — Preview

A doubly linked list adds a `prev` pointer, enabling O(1) backward traversal and simpler deletion (no need to track "previous" separately — it's stored in the node):

```c
typedef struct DNode {
    int data;
    struct DNode *next;
    struct DNode *prev;
} DNode;

void dlist_delete(DNode *node) {
    if (node->prev != NULL) node->prev->next = node->next;
    if (node->next != NULL) node->next->prev = node->prev;
    free(node);
}
```

The tradeoff: extra memory (one more pointer per node) and extra bookkeeping (both links must be kept consistent on every insert/delete). We will build a complete doubly linked list in the lab.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Trace this insertion function on an empty list, then explain why the caller's `head` is not updated.

```c
void push_front(struct Node *head, int v) {
    struct Node *n = malloc(sizeof *n);
    n->v = v; n->next = head;
    head = n;
}
```

**2. (Explain.)** The pointer-to-pointer technique eliminates the special case for deleting the head node. Explain how, comparing the two versions.

**3. (Build.)** Write `free_list`, and explain why the obvious loop is a use-after-free. Then write `list_reverse` in place.

**4. (Stretch.)** Compare an array and a linked list for: index access, insert at front, insert after a known node, memory per element, and cache behaviour. Then name a case where the linked list genuinely wins.


### Answers

**1.** After `push_front(head, 1)` the caller's `head` is **still `NULL`**, and the new node is leaked.

The parameter `head` is a **copy** of the caller's pointer. The function allocates a node, links it to the copy's target, and then assigns to the copy — which is destroyed on return. Nothing the caller can see was ever modified. This is the pass-by-value rule from Week 2 Lecture 1, applied to a pointer.

Two fixes. **Return the new head**, which the caller must remember to assign:

```c
struct Node *push_front(struct Node *head, int v) {
    struct Node *n = malloc(sizeof *n);
    if (!n) return head;
    n->v = v; n->next = head;
    return n;
}
/* list = push_front(list, 1); */
```

**Or take the address of the caller's pointer**, which cannot be misused:

```c
int push_front(struct Node **head, int v) {
    struct Node *n = malloc(sizeof *n);
    if (!n) return 0;
    n->v = v; n->next = *head;
    *head = n;
    return 1;
}
/* push_front(&list, 1); */
```

Prefer the second when the function may fail, since the return slot is then free to report it. The first has a real hazard: `push_front(list, 1);` with the result discarded compiles cleanly and silently leaks.

**2.** **With a special case:**

```c
void remove_value(struct Node **head, int v) {
    if (*head && (*head)->v == v) {           /* head case */
        struct Node *dead = *head;
        *head = dead->next;
        free(dead);
        return;
    }
    struct Node *cur = *head;                 /* interior case */
    while (cur && cur->next) {
        if (cur->next->v == v) {
            struct Node *dead = cur->next;
            cur->next = dead->next;
            free(dead);
            return;
        }
        cur = cur->next;
    }
}
```

**With pointer-to-pointer:**

```c
void remove_value(struct Node **head, int v) {
    struct Node **pp = head;
    while (*pp) {
        if ((*pp)->v == v) {
            struct Node *dead = *pp;
            *pp = dead->next;
            free(dead);
            return;
        }
        pp = &(*pp)->next;
    }
}
```

The insight is that **every node is pointed at by exactly one pointer** — either the caller's `head` or some node's `next` field. `pp` holds the *address of that pointer*, whatever it happens to be, so `*pp = dead->next` unlinks the node without needing to know which kind of pointer it was. The head stops being special because it was only ever special in the *type* of thing pointing at it, and `pp` erases that difference.

The result is half the code, one loop, no duplicated unlink logic, and no way for the two branches to drift apart. Linus Torvalds has cited exactly this transformation as the difference between understanding pointers and merely using them.

**3.**

```c
void free_list(struct Node *head) {
    while (head) {
        struct Node *next = head->next;   /* save BEFORE freeing */
        free(head);
        head = next;
    }
}

struct Node *list_reverse(struct Node *head) {
    struct Node *prev = NULL, *cur = head;
    while (cur) {
        struct Node *next = cur->next;    /* save before overwriting */
        cur->next = prev;
        prev = cur;
        cur = next;
    }
    return prev;            /* new head */
}
```

**The obvious loop is wrong:**

```c
while (head) { free(head); head = head->next; }   /* USE AFTER FREE */
```

`free(head)` releases the node, and `head->next` then reads from freed memory. It often appears to work, because `free` does not erase the bytes — the allocator merely marks the block available, and the `next` field usually survives until something else reuses it. Under ASan or Valgrind it is reported immediately as *heap-use-after-free*; without them it corrupts intermittently.

`list_reverse` needs the same discipline for the same reason: `cur->next = prev` destroys the only reference to the remainder of the list, so `next` must capture it first. Three pointers, one pass, **O(n) time and O(1) space**, and the final `return prev` matters — on exit `cur` is `NULL` and `prev` is the last node visited, which is the new head.

The shared lesson: **save what you are about to destroy.**

**4.** | Operation | Array | Linked list |
|---|---|---|
| Access by index | **O(1)** | O(n) |
| Insert at front | O(n) — shift everything | **O(1)** |
| Insert after a known node | O(n) — shift the tail | **O(1)** — two pointer writes |
| Memory per element | `sizeof(T)`, contiguous | `sizeof(T)` + 8 for `next` + allocator overhead (~16–32 bytes) |
| Cache behaviour | **Excellent** — sequential, prefetchable | Poor — each `next` is a potential cache miss |

The list's advantages are narrower than the table suggests, because "a known node" is doing heavy lifting: reaching an arbitrary position still costs an O(n) traversal, so *insert at position k* is O(k) for a list and O(n−k) for an array — and the array's shift is a `memmove` of contiguous bytes, while the list's traversal is k dependent memory loads. For elements smaller than a pointer the list can more than double memory use.

**Where the linked list genuinely wins:** when you already hold a reference to the node and must remove or splice it in O(1), and elements must not move. The **LRU cache** is the canonical case — a hash table maps keys to nodes, and every access unlinks a node from the middle and relinks it at the front. An array cannot do that without shifting; and because list nodes never move, external pointers to them stay valid, which an array's reallocation would invalidate.

Kernel data structures use intrusive lists for the same reason: an object can be on several lists at once, and removal from any of them is O(1) given the object itself.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Node** | A struct containing data and one or more pointers to other nodes |
| **Head** | The pointer to the first node of a linked list |
| **Traversal** | Walking the list from head to tail via `next` pointers |
| **Singly linked list** | Each node points only to the next node |
| **Doubly linked list** | Each node points to both the next and previous node |
| **`Node **`** | Pointer to a pointer — used to modify the caller's head pointer directly |
| **Dangling pointer** | A pointer to memory that has already been freed |

---

## Reading

- **K&R §6.5** — Self-referential Structures
- **King Ch. 17** — Dynamic Data Structures (Linked Lists)
- **CLRS Ch. 10** — Elementary Data Structures (linked lists, stacks, queues)

---

*Next: Lab 7 — Building a Complete Linked List Library*
