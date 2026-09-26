# PROG 101 · Programming I: Structured Programming in C
## Week 11 · Problem Set 11: The C Standard Library and Generic Programming

**Released:** Friday 11 December 2026, 10:00 · Week 11 (after Thursday's Lecture 3)
**Due:** Friday 18 December 2026, 17:00 · Week 12 — late penalty from 17:01
**Total:** 100 points · **Expected time:** about 3 hours

*(Revised 2026-09-26: old Problem 1 went. Its comparators (1A) were Problem 2's comparators again, and its
vending-machine state machine (1B) repeated Problem 4's dispatch table. The answer key moved out of this
handout.)*
**Build with:** `gcc -Wall -Wextra -Werror -pedantic -std=c11 -g`
**Check with:** `valgrind --leak-check=full --error-exitcode=1`

---
## Problem 1: Comparators That Are Actually Correct (25 pts)

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
| `cmp_int_asc` correct for all inputs, with the `INT_MAX` demonstration | 7 |
| The `a - b` explanation names undefined behaviour | 3 |
| `cmp_int_desc` without duplicated logic | 4 |
| `cmp_str` indirection correct and explained | 5 |
| `cmp_rec` multi-key with correct tie-break | 6 |

---

## Problem 2: A Generic `find_if` (25 pts)

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

## Problem 3: A Dispatch-Table State Machine (30 pts)

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
| Table and handlers correct; `S_DONE` absorbing | 10 |
| `step` bounds-checks the state | 5 |
| Adding `S_PAUSED` touches only the table and one handler | 6 |
| Driver output correct | 4 |
| The easier/harder analysis | 5 |

---

## Problem 4: Reading `qsort`'s Contract (20 pts)

Answer in `answers.md`. *(4 pts each.)*

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
| 1 | Comparators That Are Actually Correct | 25 |
| 2 | A Generic `find_if` | 25 |
| 3 | A Dispatch-Table State Machine | 30 |
| 4 | Reading `qsort`'s Contract | 20 |
| **Total** | | **100** |

---

*PROG 101 · Week 11 · Problem Set 11 · Due Friday 18 December 2026, 17:00 · © CSE Department*
