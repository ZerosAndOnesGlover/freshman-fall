# PROG 101 · Programming I: Structured Programming in C
## Week 11 · Problem Set 11: The C Standard Library and Generic Programming

**Released:** Friday, Week 11 · **Due:** Friday, Week 12 at 17:00
**Total:** 100 points
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --error-exitcode=1`

---
## Problem 1: Function Pointers and Dispatch (25 pts)

### 1A: Generic Sorting Framework (10 pts)

Create `generic_sort.c`. Implement these sorting functions, all using the same comparator convention as `qsort`:

```c
typedef int (*Comparator)(const void *, const void *);

/* Insertion sort — stable, O(n²), good for small/nearly-sorted arrays */
void isort(void *base, size_t n, size_t size, Comparator cmp);

/* Selection sort — unstable, O(n²), minimizes swaps */
void ssort(void *base, size_t n, size_t size, Comparator cmp);

/* Bubble sort — stable, O(n²), terminates early if already sorted */
void bsort(void *base, size_t n, size_t size, Comparator cmp);
```

These work on arrays of any element type (like `qsort`) using `void *` and element `size`. Use `memcpy` to swap elements of arbitrary size.

Test by sorting:
- `int` arrays (ascending and descending)
- `double` arrays
- `char *` arrays (lexicographic order)
- Struct arrays sorted by a field

```c
/* Example comparators to write and use */
int cmp_int_asc(const void *a, const void *b);
int cmp_int_desc(const void *a, const void *b);
int cmp_double_asc(const void *a, const void *b);
int cmp_str_asc(const void *a, const void *b);
```

### 1B: State Machine via Function Pointers (15 pts)

Create `vending.c` — a vending machine simulator using a function-pointer state machine.

**States:** `IDLE`, `HAS_MONEY`, `DISPENSING`, `RETURNING_CHANGE`
**Events:** `INSERT_COIN(amount)`, `SELECT_ITEM(price)`, `CANCEL`, `DISPENSE_DONE`

```c
typedef enum {
    STATE_IDLE,
    STATE_HAS_MONEY,
    STATE_DISPENSING,
    STATE_RETURNING_CHANGE,
    NUM_STATES
} State;

typedef enum {
    EVENT_INSERT_COIN,
    EVENT_SELECT_ITEM,
    EVENT_CANCEL,
    EVENT_DISPENSE_DONE,
    NUM_EVENTS
} Event;

typedef struct {
    int balance;    /* cents currently inserted */
    int price;      /* price of selected item */
} MachineContext;

/* A state handler processes an event and returns the next state */
typedef State (*StateHandler)(MachineContext *ctx, int event_data);

/* Transition table: handlers[state][event] → next state */
StateHandler handlers[NUM_STATES][NUM_EVENTS];
```

Implement handler functions for every valid (state, event) pair. Invalid combinations should print an error and stay in the current state.

```
Sample session:
INSERT_COIN 100  → [HAS_MONEY]  Balance: $1.00
INSERT_COIN 50   → [HAS_MONEY]  Balance: $1.50
SELECT_ITEM 125  → [DISPENSING] Dispensing item ($1.25). Change: $0.25
DISPENSE_DONE    → [RETURNING_CHANGE] Returning $0.25
(auto-transition) → [IDLE]  Balance: $0.00

INSERT_COIN 50   → [HAS_MONEY]  Balance: $0.50
SELECT_ITEM 100  → [HAS_MONEY]  Insufficient funds (need $0.50 more)
CANCEL           → [RETURNING_CHANGE] Returning $0.50
(auto-transition) → [IDLE]  Balance: $0.00
```

---

---

## Problem 2: Comparators That Are Actually Correct (20 pts)

Write `compare.c` providing comparators for `qsort` and `bsearch`.

```c
int cmp_int_asc (const void *a, const void *b);
int cmp_int_desc(const void *a, const void *b);
int cmp_str     (const void *a, const void *b);   /* for an array of char*  */
int cmp_rec     (const void *a, const void *b);   /* score DESC, then name ASC */
```

where `typedef struct { char *name; int score; } Rec;`.

### Requirements

1. **`cmp_int_asc` must be correct for every pair of `int`s, including `INT_MIN` and `INT_MAX`.**
   Demonstrate this with a test on `{INT_MAX, -2}`. In `answers.md`, explain why `return *a - *b;`
   fails and what the standard says about it.
2. `cmp_int_desc` must be implemented **without duplicating** the comparison logic.
3. `cmp_str` operates on an array of `char *`. Get the level of indirection right — say in
   `answers.md` what type `qsort` actually hands the comparator here.
4. `cmp_rec` is a **multi-key** comparator: score descending, ties broken by name ascending.
5. Write tests that sort with each and verify the resulting order.

### Marking

| Component | Points |
|---|---|
| `cmp_int_asc` correct for all inputs, with the `INT_MAX` demonstration | 6 |
| The `a - b` explanation names undefined behaviour | 3 |
| `cmp_int_desc` without duplicated logic | 3 |
| `cmp_str` indirection correct and explained | 4 |
| `cmp_rec` multi-key with correct tie-break | 4 |

---

## Problem 3: A Generic `find_if` (20 pts)

`qsort` and `bsearch` take a comparator. Write the searching equivalent, taking a **predicate and a
context pointer**.

```c
typedef int (*Pred)(const void *elem, void *ctx);

void  *find_if (void *base, size_t n, size_t elem_size, Pred p, void *ctx);
size_t count_if(const void *base, size_t n, size_t elem_size, Pred p, void *ctx);
```

### Requirements

1. `find_if` returns a pointer to the **first** matching element, or NULL.
2. Both must work on **any** element type — test with `int` and with `Rec`.
3. The `ctx` pointer is passed through untouched; the functions must never inspect it.
4. Use it to answer "first record scoring at least *t*" where *t* comes from `ctx`.
5. In `answers.md`, explain **why the context pointer is necessary** — what would you be forced to do
   without it, and why is that worse?

---

## Problem 4: A Dispatch-Table State Machine (25 pts)

Replace a `switch`-based state machine with an array of function pointers.

```c
typedef enum { S_IDLE, S_RUN, S_DONE, S_COUNT } State;
typedef State (*Handler)(int input);

extern Handler transition[S_COUNT];
State step(State s, int input);
```

### Requirements

1. One handler per state; `transition[s](input)` returns the next state.
2. `S_DONE` is absorbing — every input leaves it in `S_DONE`.
3. `step` must **bounds-check** `s` against `S_COUNT` and handle an invalid state explicitly.
4. Add a fourth state `S_PAUSED` by editing **one row of the table and adding one handler** — show
   the dispatch code itself does not change.
5. Write a driver that runs the input sequence `0,1,1,0,1` from `S_IDLE` and prints each transition.
6. In `answers.md`: give one thing this design makes **easier** than a `switch`, and one thing it
   makes **harder**. Be specific.

### Marking

| Component | Points |
|---|---|
| Table and handlers correct; `S_DONE` absorbing | 8 |
| `step` bounds-checks the state | 4 |
| Adding `S_PAUSED` touches only the table and one handler | 5 |
| Driver output correct | 4 |
| The easier/harder analysis | 4 |

---

## Problem 5: Reading `qsort`'s Contract (10 pts)

Answer in `answers.md`. *(2 pts each.)*

**(a)** `qsort` takes four parameters. Three of them exist to replace information that `void *`
destroyed. Name all three and say what each replaces.

**(b)** Is `qsort` guaranteed stable? What does the standard say, and what should you do if you need
stability?

**(c)** What are the three requirements for `bsearch` to work, and what happens if the first is
violated?

**(d)** A comparator that is *inconsistent* — say, one returning random values — does more than
mis-sort. State what the standard says about it and what can happen in practice.

**(e)** `qsort` sorts an array of `char *`. What is the static type of the pointer the comparator
receives, and what is the correct way to obtain the string from it?

---

## Grading

| Problem | Topic | Points |
|---|---|---|
| 1 | Function Pointers and Dispatch | 25 |
| 2 | Comparators That Are Actually Correct | 20 |
| 3 | A Generic `find_if` | 20 |
| 4 | A Dispatch-Table State Machine | 25 |
| 5 | Reading `qsort`'s Contract | 10 |
| **Total** | | **100** |

---

## Answer Key (Instructor Copy)

### Problem 1 — Function Pointers and Dispatch (25 pts)

**5A Generic Sort (10 pts).**
*The `qsort`-style signature `int cmp(const void *, const void *)` is the point. Two things to check: (i) comparators must cast through the correct type before dereferencing — `*(const int *)a`; (ii) the comparator must return the **sign** of the difference, not the difference itself.*

*`return x - y;` is signed overflow (UB) for far-apart operands. Verified directly — comparing `INT_MIN` against `1`, where the truth is "less":*

```
x-y  comparator returns  2147483647  -> claims GREATER   (wrong)
sign comparator returns          -1  -> claims less      (correct)
```

*The correct branchless form is `(x > y) - (x < y)`. Note the failure is **latent**: sorting `{INT_MIN, 1, 0}` with the broken comparator still produced correctly sorted output on glibc, because `qsort` never happened to compare that particular pair in a way that mattered. So a submission can pass casual testing and still be wrong — test the **comparator directly** on extreme operands rather than only checking sorted output. This exact issue appears in the Week 3 lecture and the Week 3 quiz; expect it and mark it.*
*For strings the comparator receives `char **`, not `char *` — dereference once to get the `char *`, then `strcmp`. Getting this wrong is the most common failure in the "works for string" requirement.*

**5B State Machine (15 pts).**
*A table of function pointers (`typedef void (*Handler)(void);` plus an array indexed by state, or an array of `{state, event, handler, next_state}`) is what the problem is teaching — a `switch` cascade is functionally correct but sidesteps the exercise. Award at most 8 of 15 for a pure `switch`, and say why.*
*Require that every state is reachable and every transition exercised by the test output; an unreachable state is the usual sign of an incomplete table. Guard the dispatch index against out-of-range states — an unchecked `table[state]()` on a bad state is an arbitrary-code-execution bug, and saying so lands the security point of the exercise.*

---

*PROG 101 · Week 3 · Problem Set 3 · © CSE Department*

### Problem 2 — Comparators That Are Actually Correct (20 pts)

```c
int cmp_int_asc(const void *a, const void *b)
{
    int l = *(const int *)a, r = *(const int *)b;
    return (l > r) - (l < r);          /* no arithmetic on the values */
}

int cmp_int_desc(const void *a, const void *b) { return cmp_int_asc(b, a); }

int cmp_str(const void *a, const void *b)
{
    const char *const *l = a, *const *r = b;   /* element IS a char*, so a is char** */
    return strcmp(*l, *r);
}

int cmp_rec(const void *a, const void *b)
{
    const Rec *x = a, *y = b;
    int c = (y->score > x->score) - (y->score < x->score);   /* score DESC */
    return c ? c : strcmp(x->name, y->name);                 /* name ASC   */
}
```

**Verified:** ascending, descending, string and multi-key sorts all produce the expected order.
The multi-key case on `{ada 91, zoe 91, ken 84, bob 91}` gives **ada, bob, zoe, ken** — scores
descending, names ascending within the tie.

**Marking notes.**

- **Requirement 1 (6 pts) is the core.** `return *a - *b;` performs **signed subtraction**, which
  **overflows** when the true difference exceeds `INT_MAX` — and signed overflow is **undefined
  behaviour**, not merely a wrong value. Verified: sorting `{INT_MAX, -2}` with the subtracting
  comparator leaves the array **unsorted**, and UBSan reports
  `signed integer overflow: 2147483647 - -2 cannot be represented in type 'int'`.
  The idiom `(l > r) - (l < r)` performs no arithmetic on the values at all and is correct for every
  input. *3 of the 6 require the demonstration, not just the assertion.*
- **Requirement 2 (3 pts):** `return cmp_int_asc(b, a);` — swapping the arguments reverses the order
  with no duplicated logic. A copy-pasted body with `<` and `>` exchanged scores 1.
- **Requirement 3 (4 pts):** `qsort` passes the **address of the element**. When the element is
  itself a `char *`, that address has type `char **`. Passing it straight to `strcmp` compares the
  *pointer bytes* as text. The correct answer must state the type.
- **Requirement 4 (4 pts):** the early `return c ? c : …` is load-bearing — without it the tie-break
  overwrites the primary key.

### Problem 3 — A Generic `find_if` (20 pts)

```c
void *find_if(void *base, size_t n, size_t elem_size, Pred p, void *ctx)
{
    for (size_t i = 0; i < n; i++) {
        void *e = (char *)base + i * elem_size;    /* char* for byte arithmetic */
        if (p(e, ctx)) return e;
    }
    return NULL;
}

size_t count_if(const void *base, size_t n, size_t elem_size, Pred p, void *ctx)
{
    size_t c = 0;
    for (size_t i = 0; i < n; i++)
        if (p((const char *)base + i * elem_size, ctx)) c++;
    return c;
}
```

**Verified** on both `int` and `Rec` arrays: "first record scoring ≥ 90" returns `ada`; with a
threshold of 100 it returns NULL.

**Marking notes.**

- **`(char *)base + i * elem_size` (5 pts).** `sizeof(char)` is 1 by definition, so `char *`
  arithmetic counts bytes. Arithmetic on `void *` is a GNU extension and `-pedantic` rejects it.
- **Requirement 5 (6 pts) — why the context pointer.** Without it, the predicate could only be a
  function of the element, so any additional information (the threshold) would have to live in a
  **global**. That makes the code non-reentrant, untestable in parallel, and impossible to use twice
  with different thresholds at once. The `ctx` pointer is C's explicit stand-in for a closure: the
  function pointer is the code, `ctx` is the captured environment.
- **The function must never inspect `ctx`** — it only passes it through. A version that assumes a
  particular type has defeated the genericity.

### Problem 4 — A Dispatch-Table State Machine (25 pts)

```c
static State h_idle(int in) { return in ? S_RUN  : S_IDLE; }
static State h_run (int in) { return in ? S_RUN  : S_DONE; }
static State h_done(int in) { (void)in; return S_DONE; }     /* absorbing */

Handler transition[S_COUNT] = { h_idle, h_run, h_done };

State step(State s, int input)
{
    if (s < 0 || s >= S_COUNT) return S_DONE;    /* or report an error */
    return transition[s](input);
}
```

**Verified driver output** for inputs `0,1,1,0,1` from `S_IDLE`:

```
IDLE -0-> IDLE -1-> RUN -1-> RUN -0-> DONE -1-> DONE
```

`S_DONE` is absorbing: `transition[S_DONE](1)` returns `S_DONE`.

**Marking notes.**

- **Requirement 3 (4 pts).** Indexing `transition[s]` with an out-of-range `s` reads outside the
  array and calls through whatever garbage it finds — a wild jump, and one of the nastiest bugs in
  C. The bounds check is not defensive padding; it is the thing that makes the table safe.
- **`(void)in` in `h_done`** silences `-Wunused-parameter` under `-Wextra` without changing
  behaviour.
- **Requirement 4 (5 pts):** adding `S_PAUSED` must touch the enum, one new handler, and one table
  row — and **`step` must not change at all**. That invariance is the whole argument for the design.
- **Requirement 6 (4 pts).** *Easier:* adding a state is local and the dispatch code is untouched;
  the state set becomes data and could be built at run time. *Harder:* every handler must fit one
  signature, so a state needing extra arguments forces a redesign; and the behaviour is scattered
  across functions rather than visible in one `switch`. Reject vague answers — "it's cleaner" scores 0.

### Problem 5 — Reading `qsort`'s Contract (10 pts)

**(a)** `nmemb` replaces the **element count**, `size` replaces the **element size**, and `compar`
replaces the **ordering** — all three erased by `void *`, which retains only an address.

**(b)** **Not guaranteed stable.** The C standard says nothing about the relative order of equal
elements. *(glibc's implementation happens to be stable when it can allocate a merge buffer — but
that is not a guarantee and does not hold under memory pressure.)* If you need stability, **encode
it**: add the original index as a final tie-break key, which turns the comparator into a total order.

**(c)** The array must be **sorted by the same comparator**; you must pass the **address** of the key,
not the key; and the return is a **pointer**, not an index. Violating the first does not produce an
error — `bsearch` silently returns the wrong answer, usually NULL.

**(d)** The standard says the behaviour is **undefined**. In practice an inconsistent comparator can
drive the sort **out of bounds** — glibc's introsort relies on the ordering being a valid total order
to bound its partitioning, and violating it can corrupt memory rather than merely producing a
mis-sorted array.

**(e)** The comparator receives a `const void *` that actually points at a `char *` element, so the
correct static type is **`const char *const *`**. Obtain the string by dereferencing once:
`const char *const *p = a; strcmp(*p, …)`.

---

*PROG 101 · Week 11 · Problem Set 11 · © CSE Department*
