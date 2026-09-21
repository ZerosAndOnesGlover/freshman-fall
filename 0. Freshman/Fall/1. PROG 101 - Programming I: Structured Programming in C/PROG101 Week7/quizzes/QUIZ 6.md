# PROG 101 · Quiz 6
## Week 7, Tuesday — In-Class Assessment

**Date:** Tuesday 10 November 2026 · 10:00–10:10 (start of Week 7, Lecture 1)
**Covers:** Week 6 material — dynamic memory, ownership, Valgrind
**Duration:** 10 minutes · **Format:** Written, closed book · **Total: 20 points**

---

## Section A — Multiple Choice (2 pts each)

**A1.** `malloc(16)` returns a non-NULL pointer. The 16 bytes are:

&nbsp;&nbsp;(a) all zero (b) indeterminate (c) all `0xFF` (d) copied from the previous allocation

**A2.** `realloc(p, n)` returns NULL. What is the state of the original block?

&nbsp;&nbsp;(a) freed (b) still allocated and valid (c) partially freed (d) undefined

**A3.** `free(NULL)` is:

&nbsp;&nbsp;(a) undefined behaviour (b) a crash (c) a guaranteed no-op (d) implementation-defined

**A4.** Which does `calloc(n, size)` do that `malloc(n * size)` does not?

&nbsp;&nbsp;(a) allocate faster (b) zero the memory and check the multiplication for overflow
(c) allow resizing later (d) register the block for automatic release

**A5.** A growable array doubling its capacity gives an amortised append cost of:

&nbsp;&nbsp;(a) O(log n) (b) O(1) (c) O(n) (d) O(n log n)

---

## Section B — Short Answer (2 pts each)

**B1.** Explain in one sentence why `p = realloc(p, n);` is wrong, and write the correct form.

&nbsp;

&nbsp;

**B2.** After `free(p);`, why is `p = NULL;` worth writing? Name the two bugs it converts into
loud failures.

&nbsp;

&nbsp;

**B3.** A container holds structs that each own a `malloc`'d string. `free(v->data)` alone leaks.
Explain why, and state what else must happen.

&nbsp;

&nbsp;

**B4.** Give the Valgrind message for a leaked block, and the message for a double free.

&nbsp;

&nbsp;

**B5.** Name one class of bug Valgrind detects that AddressSanitizer does not.

&nbsp;

&nbsp;

---

**Total: 20 points**

---

## Answer Key (Instructor Copy)

**A1 (b).** Indeterminate. Verified: a fresh `malloc(16)` had 5 of 16 bytes nonzero on one run.
Reading before writing is undefined behaviour, and Valgrind reports it.

**A2 (b).** Still allocated and valid — which is precisely why assigning the result back to `p`
loses it.

**A3 (c).** A guaranteed no-op, so cleanup paths need no guard.

**A4 (b).** Both, and the overflow check is the security-relevant half: verified,
`SIZE_MAX/4 + 1` times 4 wraps to **exactly 0**, so `malloc` would allocate nothing and the caller
would write far past it.

**A5 (b).** O(1) amortised. Total copying is under 2n — verified at 28 elements copied over 30
pushes, and 131,068 over 100,000.

**B1.** On failure `realloc` returns NULL **and leaves the original allocated**, so assigning back
destroys the only reference — a leak plus loss of the data.

```c
void *tmp = realloc(p, n);
if (!tmp) { /* p still valid */ }
else        p = tmp;
```

**B2.** `free` receives a *copy* of the pointer and cannot null the caller's variable, so `p` is left
dangling. Setting it to NULL converts **use-after-free** into an immediate null dereference at the
right line, and **double free** into a safe no-op.

*Both bugs are required for the 2 marks.*

**B3.** The container's buffer holds the structs, but each struct's `name` pointer was a **separate
allocation**. Freeing the buffer releases the structs and leaks every string — Valgrind reports one
*definitely lost* block per element. A `destroy` callback must run over every element **before**
`free(v->data)`.

*Accept "iterate and free each string first".*

**B4.** Leak: `N bytes in 1 blocks are definitely lost in loss record 1 of 1`.
Double free: `Invalid free() / delete / delete[] / realloc()`.

*Both verified. Accept close paraphrases; the point is recognising them on sight.*

**B5.** **Reads of uninitialised memory** — `Conditional jump or move depends on uninitialised
value(s)`. ASan does not detect these, which is why both tools are run.

---

*PROG 101 · Week 7 · Quiz 6 · © CSE Department*
