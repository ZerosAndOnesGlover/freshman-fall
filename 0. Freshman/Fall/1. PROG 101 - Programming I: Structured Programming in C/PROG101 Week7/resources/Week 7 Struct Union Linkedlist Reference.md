# PROG 101 — Week 7 Resources
## Struct Layout Reference · Linked List Pattern Library · Common Bugs

---

## Part 1: Struct Layout Quick Reference

### Alignment Rules

| Type | Typical Alignment (64-bit) |
|------|---------------------------|
| `char` | 1 |
| `short` | 2 |
| `int`, `float` | 4 |
| `long`, `double`, pointers | 8 |
| `struct` | alignment of its largest member |

**Rule 1:** Each field is placed at an offset that is a multiple of its own alignment.
**Rule 2:** The overall struct size is padded to be a multiple of its largest member's alignment (so arrays of the struct keep every element aligned).

### Field Ordering Strategy

```c
/* WORSE: 24 bytes (lots of padding) */
struct Bad {
    char   a;    /* 1 + 7 padding */
    double b;    /* 8 */
    char   c;    /* 1 + 7 padding */
};

/* BETTER: 16 bytes (fields ordered largest to smallest) */
struct Good {
    double b;    /* 8 */
    char   a;    /* 1 */
    char   c;    /* 1 + 6 padding (to reach multiple of 8) */
};
```

**Rule of thumb:** order fields from largest alignment requirement to smallest to minimize padding.

### Inspecting Any Struct

```c
#include <stddef.h>   /* offsetof */

#define PRINT_LAYOUT(type, ...) do { \
    printf("sizeof(%s) = %zu\n", #type, sizeof(type)); \
} while(0)

printf("offset of field: %zu\n", offsetof(struct MyStruct, field_name));
```

---

## Part 2: Struct/Union/Enum Syntax Cheat Sheet

```c
/* === STRUCT === */
struct Tag {
    int field;
};
struct Tag var;                      /* must write "struct Tag" every time */

typedef struct Tag {
    int field;
} TypedefName;
TypedefName var;                     /* clean, no "struct" needed */

typedef struct {                     /* anonymous struct + typedef (most common) */
    int field;
} Point;
Point p;

/* === SELF-REFERENCING STRUCT (needs the tag) === */
typedef struct Node {
    int data;
    struct Node *next;               /* MUST use "struct Node" here */
} Node;

/* === UNION === */
union Tag {
    int    i;
    float  f;
};
union Tag u;

typedef union {
    int    i;
    float  f;
} Value;
Value v;

/* === ENUM === */
enum Color { RED, GREEN, BLUE };     /* RED=0, GREEN=1, BLUE=2 */
enum Color c = GREEN;

typedef enum {
    STATUS_OK = 0,
    STATUS_ERROR = -1
} Status;
Status s = STATUS_OK;

/* === TAGGED UNION (the variant type pattern) === */
typedef struct {
    enum { TAG_A, TAG_B } tag;
    union {
        int    a_data;
        double b_data;
    } payload;
} Variant;
```

---

## Part 3: Linked List Pattern Library

### The Universal Traversal Pattern

```c
for (Node *cur = head; cur != NULL; cur = cur->next) {
    /* process cur->data */
}
```

### Insert at Front

```c
Node *insert_front(Node *head, int value) {
    Node *n = node_create(value);
    n->next = head;
    return n;
}
```

### Insert at End

```c
Node *insert_end(Node *head, int value) {
    Node *n = node_create(value);
    if (head == NULL) return n;
    Node *cur = head;
    while (cur->next != NULL) cur = cur->next;
    cur->next = n;
    return head;
}
```

### Delete by Value (Standard Two-Pointer Approach)

```c
Node *delete_value(Node *head, int target) {
    if (head == NULL) return NULL;
    if (head->data == target) {
        Node *new_head = head->next;
        free(head);
        return new_head;
    }
    Node *prev = head, *cur = head->next;
    while (cur != NULL) {
        if (cur->data == target) {
            prev->next = cur->next;
            free(cur);
            return head;
        }
        prev = cur;
        cur = cur->next;
    }
    return head;
}
```

### Delete by Value (Pointer-to-Pointer, No Special Cases)

```c
void delete_value_pp(Node **headp, int target) {
    Node **pp = headp;
    while (*pp != NULL) {
        if ((*pp)->data == target) {
            Node *dead = *pp;
            *pp = dead->next;
            free(dead);
            return;
        }
        pp = &(*pp)->next;
    }
}
```

### Free the Entire List

```c
void free_list(Node *head) {
    while (head != NULL) {
        Node *next = head->next;   /* save BEFORE freeing */
        free(head);
        head = next;
    }
}
```

### Reverse In-Place

```c
Node *reverse(Node *head) {
    Node *prev = NULL, *cur = head;
    while (cur != NULL) {
        Node *next = cur->next;
        cur->next = prev;
        prev = cur;
        cur = next;
    }
    return prev;
}
```

### Slow/Fast Pointer Technique (Floyd's Algorithm)

```c
/* Find the middle node */
Node *find_middle(Node *head) {
    Node *slow = head, *fast = head;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;   /* slow is at the middle */
}

/* Detect a cycle */
bool has_cycle(Node *head) {
    Node *slow = head, *fast = head;
    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}
```

### Merge Two Sorted Lists

```c
Node *merge_sorted(Node *a, Node *b) {
    Node dummy;              /* dummy node simplifies edge cases */
    Node *tail = &dummy;
    dummy.next = NULL;

    while (a != NULL && b != NULL) {
        if (a->data <= b->data) {
            tail->next = a;
            a = a->next;
        } else {
            tail->next = b;
            b = b->next;
        }
        tail = tail->next;
    }
    tail->next = (a != NULL) ? a : b;   /* attach remaining nodes */

    return dummy.next;
}
```

The **dummy node** technique is extremely useful: it eliminates the need to special-case "is this the first node in the result?" by giving you a guaranteed starting point to append after.

---

## Part 4: Common Linked List Bugs

```c
/* BUG 1: Use-after-free during traversal */
while (cur != NULL) {
    free(cur);
    cur = cur->next;    /* WRONG: cur was just freed */
}
/* FIX: save next first */
while (cur != NULL) {
    Node *next = cur->next;
    free(cur);
    cur = next;
}

/* BUG 2: Forgetting to update head after insert/delete */
insert_front(head, 5);   /* WRONG: return value discarded, head unchanged */
head = insert_front(head, 5);   /* CORRECT */

/* BUG 3: Losing the rest of the list when inserting */
void bad_insert_after(Node *node, int value) {
    Node *n = node_create(value);
    node->next = n;          /* WRONG: lost the old node->next! */
}
void good_insert_after(Node *node, int value) {
    Node *n = node_create(value);
    n->next = node->next;    /* connect new node to the rest FIRST */
    node->next = n;          /* THEN link previous node to new node */
}

/* BUG 4: Memory leak — orphaning a node without freeing it */
head = head->next;   /* If this was the only reference to the old head,
                        its memory is now unreachable and leaked */
/* FIX: */
Node *old = head;
head = head->next;
free(old);

/* BUG 5: Dereferencing NULL when checking an empty list */
if (head->data == target)   /* CRASH if head is NULL */
/* FIX: check for NULL first */
if (head != NULL && head->data == target)

/* BUG 6: Double-free from aliased pointers */
Node *a = head;
Node *b = head;
free(a);
free(b);   /* UNDEFINED BEHAVIOR: a and b point to the same freed memory */
```

---

## Part 5: Struct/Array/Linked List Decision Guide

| Need | Use |
|------|-----|
| Fixed number of related fields, known at compile time | `struct` |
| One of several possible types, only one active at a time | `union` |
| Small set of named constant values | `enum` |
| "This is either an A or a B" with runtime dispatch | tagged union (struct + enum + union) |
| Fast random access, cache-friendly | array |
| Frequent insert/delete at arbitrary positions | linked list |
| Need O(1) access to both ends, O(1) arbitrary deletion | doubly linked list |
| Fixed-size collection of records | array of structs |
| Growing collection whose size isn't known upfront | linked list, or dynamic array (Week 6) |

---

## Part 6: Debugging Structs and Linked Lists with GDB

```bash
gdb ./program
```

```
(gdb) break main
(gdb) run
(gdb) print my_struct              # print entire struct contents
(gdb) print my_struct.field        # print one field
(gdb) print *my_pointer            # dereference and print struct
(gdb) print my_pointer->field      # print field through pointer
(gdb) print head                   # print head pointer's address
(gdb) print *head                  # print first node's contents
(gdb) print *head->next            # print second node's contents

# Walk a linked list manually in GDB:
(gdb) set $p = head
(gdb) print *$p
(gdb) set $p = $p->next
(gdb) print *$p
(gdb) set $p = $p->next
(gdb) print *$p
# ... repeat until $p is NULL

# Or, in a single command with GDB's printf:
(gdb) print head->data
(gdb) print head->next->data
(gdb) print head->next->next->data
```
