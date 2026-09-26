# PROG 101 · Problem Set 11 Solutions
## INSTRUCTOR ONLY — DO NOT DISTRIBUTE

*Moved 2026-09-26 out of the student handout, where it had been printed below the questions.*

---

*(Revised 2026-09-26: old Problem 1 is no longer asked. Old 2 → 1 (25), 3 → 2 (25), 4 → 3 (30), 5 → 4 (20, 4 per
part).)*

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
