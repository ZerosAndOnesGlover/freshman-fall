# PROG 101 · Programming I: Structured Programming in C
## Week 9 · Lecture 1: Recursion Fundamentals

**Date:** Tuesday 20 October 2026 · 10:00–10:50 · Week 9

---

## Lecture Goals

By the end of this lecture you will:
- Understand recursion as mathematical induction implemented in code
- Identify the base case and recursive case of any recursive function
- Trace recursive calls precisely using the call stack model from Week 3
- Convert between recursive and iterative implementations
- Understand tail recursion and why C compilers may or may not optimize it
- Recognize when recursion is the right engineering choice, and when it isn't

---

## 1. Recursion Is Not a Trick: It Is Mathematical Induction

A recursive definition defines something in terms of a **simpler version of itself**. This is precisely the structure of mathematical induction (which you will formalize in a discrete mathematics course, but you can understand its computational form right now).

The factorial function has a natural recursive definition:
```
0! = 1                    (base case)
n! = n × (n-1)!  for n>0   (recursive case: reduce to a simpler problem)
```

This translates directly into code:
```c
long factorial(int n) {
    if (n <= 0) return 1;               /* base case */
    return n * factorial(n - 1);         /* recursive case */
}
```

**Every correct recursive function has exactly this structure:**
1. **Base case(s):** the simplest input(s), solved directly without further recursion
2. **Recursive case:** the problem is reduced to one or more *strictly simpler* subproblems, and the function calls itself to solve them

If you cannot identify both parts clearly, you do not yet understand the recursion you're about to write. Write them down as comments before writing any code:

```c
long factorial(int n) {
    /* Base case: 0! = 1! = 1 */
    if (n <= 1) return 1;
    /* Recursive case: n! = n * (n-1)! */
    return n * factorial(n - 1);
}
```

---

## 2. Why Recursion Terminates (Or Doesn't)

For recursion to terminate, the recursive case must move **strictly closer** to a base case on every call. If it doesn't, you get infinite recursion — which manifests as a **stack overflow** (Week 3's stack frames, pushed without bound, eventually exhaust the fixed-size stack memory region).

```c
/* BROKEN: never reaches a base case for n < 0 */
long factorial_broken(int n) {
    if (n == 0) return 1;
    return n * factorial_broken(n - 1);
}
factorial_broken(-1);   /* -1, -2, -3, ... forever → stack overflow, SIGSEGV */
```

```c
/* CORRECT: base case catches n <= 1, covering all descending paths */
long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

**Discipline:** before writing any recursive function, ask explicitly: *"Does every possible recursive call strictly decrease toward a base case, and does the base case actually get reached for all valid inputs?"*

---

## 3. Tracing Recursion: The Call Stack in Action

Recall from Week 3: every function call pushes a stack frame containing its parameters and local variables. Recursive calls are no different — each one gets its **own independent frame**, with its own copy of `n`.

Tracing `factorial(4)`:

```
factorial(4)
│  n = 4
│  calls factorial(3), waits for result
│
├─▶ factorial(3)
│   │  n = 3
│   │  calls factorial(2), waits for result
│   │
│   ├─▶ factorial(2)
│   │   │  n = 2
│   │   │  calls factorial(1), waits for result
│   │   │
│   │   ├─▶ factorial(1)
│   │   │   │  n = 1
│   │   │   │  BASE CASE: returns 1 immediately
│   │   │   └─▶ returns 1
│   │   │
│   │   └─▶ 2 * 1 = 2, returns 2
│   │
│   └─▶ 3 * 2 = 6, returns 6
│
└─▶ 4 * 6 = 24, returns 24
```

At the deepest point (inside `factorial(1)`), the call stack holds **four separate frames simultaneously** — one for each of `factorial(4)`, `factorial(3)`, `factorial(2)`, `factorial(1)` — each with its own `n`. This is exactly the mechanism (Week 2's stack frames) that makes recursion work: each call's local state is preserved on its own frame while it waits for its recursive call to return.

### The Trace Table Method

For any recursive function, build a trace table before you trust your intuition:

| Call | n | Base case? | Computation | Returns |
|------|---|-----------|-------------|---------|
| `factorial(4)` | 4 | No | `4 * factorial(3)` | 24 |
| `factorial(3)` | 3 | No | `3 * factorial(2)` | 6 |
| `factorial(2)` | 2 | No | `2 * factorial(1)` | 2 |
| `factorial(1)` | 1 | **Yes** | — | 1 |

Fill in a table like this by hand for every non-trivial recursive function you write until it becomes automatic.

---

## 4. Recursion vs Iteration

Every recursive function can be rewritten iteratively, and vice versa. They are equally expressive — the choice is an engineering judgment, not a fundamental capability difference.

```c
/* Recursive: elegant, mirrors the mathematical definition directly */
long factorial_rec(int n) {
    if (n <= 1) return 1;
    return n * factorial_rec(n - 1);
}

/* Iterative: no function call overhead, no stack growth, same result */
long factorial_iter(int n) {
    long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}
```

| Factor | Recursion | Iteration |
|--------|-----------|-----------|
| Clarity for naturally recursive problems (trees, divide-and-conquer) | Excellent | Often awkward |
| Memory cost | O(depth) stack frames | O(1) extra memory |
| Function call overhead | Present on every call | None |
| Risk of stack overflow | Yes, for deep recursion | No |
| Clarity for naturally sequential problems | Often awkward | Excellent |

**Rule of thumb:** use recursion when the problem's structure is naturally recursive (trees, divide-and-conquer algorithms, backtracking search). Use iteration when the problem is naturally a sequential loop and depth could be large. When in doubt for performance-critical code with bounded, shallow recursion, recursion's clarity usually outweighs its modest overhead.

---

## 5. The Classic Recursive Patterns

### Pattern 1: Linear Recursion (One Recursive Call)

```c
/* Sum of digits of a non-negative integer */
int digit_sum(int n) {
    if (n < 10) return n;                    /* base case: single digit */
    return (n % 10) + digit_sum(n / 10);      /* recursive case: last digit + rest */
}

/* Length of a string (avoiding strlen, for illustration) */
size_t my_strlen(const char *s) {
    if (*s == '\0') return 0;                 /* base case: end of string */
    return 1 + my_strlen(s + 1);              /* recursive case: 1 + rest of string */
}

/* Sum of an array */
int array_sum(const int arr[], int n) {
    if (n == 0) return 0;                     /* base case: empty array */
    return arr[0] + array_sum(arr + 1, n - 1); /* recursive case: first + rest */
}
```

### Pattern 2: Binary/Multiple Recursion (More Than One Recursive Call)

```c
/* Fibonacci — TWO recursive calls per invocation */
long fib(int n) {
    if (n <= 1) return n;                     /* base case */
    return fib(n - 1) + fib(n - 2);           /* TWO recursive calls */
}
```

**Warning:** naive Fibonacci recomputes the same subproblems exponentially many times. `fib(5)` calls `fib(4)` and `fib(3)`; `fib(4)` itself calls `fib(3)` again — the same subproblem is solved twice, and this compounds exponentially. `fib(n)` performs O(2ⁿ) calls total. This is your first encounter with the cost of naive recursion, formally addressed by **memoization** and **dynamic programming** in later algorithms courses.

```c
/* Memoized version: cache results to avoid recomputation */
long memo[100] = {0};
int computed[100] = {0};

long fib_memo(int n) {
    if (n <= 1) return n;
    if (computed[n]) return memo[n];          /* already solved — reuse */
    long result = fib_memo(n - 1) + fib_memo(n - 2);
    memo[n] = result;
    computed[n] = 1;
    return result;
}
/* Now O(n) calls total instead of O(2^n) */
```

### Pattern 3: Recursion with an Accumulator (Tail Recursion)

```c
/* Non-tail-recursive: work happens AFTER the recursive call returns */
long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);   /* multiplication happens after the call returns */
}

/* Tail-recursive: the recursive call is the LAST operation, nothing left to do after */
long factorial_tail(int n, long accumulator) {
    if (n <= 1) return accumulator;
    return factorial_tail(n - 1, n * accumulator);   /* nothing happens after this call */
}
long factorial_tail_wrapper(int n) {
    return factorial_tail(n, 1);   /* start the accumulator at 1 */
}
```

**Tail recursion** means the recursive call is the very last action in the function — its result is returned immediately, with no pending computation waiting for it. In principle, a compiler *could* transform this into a loop (reusing the same stack frame instead of pushing a new one) — this is called **tail call optimization (TCO)**.

**Important for C specifically:** unlike languages such as Scheme (which *guarantee* TCO), C compilers perform tail call optimization only **opportunistically**, typically at `-O2` or higher, and only for genuinely tail-recursive calls. **Do not rely on TCO in C** — if deep recursion is a real risk, convert to an explicit loop or an explicit stack-based iterative algorithm.

```bash
# See whether your compiler actually applied TCO:
gcc -O2 -S factorial_tail.c -o factorial_tail.s
# Inspect the assembly: a genuinely optimized tail call becomes a jump (jmp),
# not a call (call) — meaning no new stack frame is pushed.
```

---

## 6. Recursion on Arrays and Strings — Shrinking the Problem

The recursive case must operate on a **smaller instance of the same problem** — for arrays and strings, this typically means passing a smaller length or an advanced pointer.

```c
/* Reverse a string in-place, recursively */
void reverse_helper(char *s, int left, int right) {
    if (left >= right) return;                /* base case: pointers have met/crossed */
    char tmp = s[left];
    s[left] = s[right];
    s[right] = tmp;
    reverse_helper(s, left + 1, right - 1);    /* recursive case: shrink the range */
}
void reverse_string(char *s) {
    reverse_helper(s, 0, (int)strlen(s) - 1);
}

/* Check if a string is a palindrome, recursively */
int is_palindrome_helper(const char *s, int left, int right) {
    if (left >= right) return 1;               /* base case: crossed or met — palindrome */
    if (s[left] != s[right]) return 0;         /* mismatch — not a palindrome */
    return is_palindrome_helper(s, left + 1, right - 1);
}

/* Binary search, recursively */
int binary_search_rec(const int arr[], int lo, int hi, int target) {
    if (lo > hi) return -1;                    /* base case: not found */
    int mid = lo + (hi - lo) / 2;
    if (arr[mid] == target) return mid;        /* base case: found */
    if (arr[mid] < target)
        return binary_search_rec(arr, mid + 1, hi, target);   /* search right half */
    else
        return binary_search_rec(arr, lo, mid - 1, target);   /* search left half */
}
```

---

## 7. Common Recursion Mistakes

```c
/* MISTAKE 1: missing or unreachable base case → infinite recursion */
long bad(int n) {
    return n * bad(n - 1);   /* NO base case at all — crashes eventually */
}

/* MISTAKE 2: base case exists but is never reached for some inputs */
long bad2(int n) {
    if (n == 0) return 1;
    return n * bad2(n - 2);   /* skips by 2 — never hits exactly 0 for odd n! */
}

/* MISTAKE 3: recursive case doesn't actually shrink the problem */
long bad3(int n) {
    if (n <= 0) return 1;
    return n * bad3(n);       /* BUG: should be bad3(n-1) — infinite recursion */
}

/* MISTAKE 4: forgetting to return the recursive call's result */
int count_bad(const int arr[], int n, int target) {
    if (n == 0) return 0;
    if (arr[0] == target) {
        count_bad(arr + 1, n - 1, target);   /* BUG: result discarded, not returned/added */
    }
    return 0;   /* always returns 0 — wrong! */
}
/* FIX: */
int count_good(const int arr[], int n, int target) {
    if (n == 0) return 0;
    int rest = count_good(arr + 1, n - 1, target);
    return (arr[0] == target) ? rest + 1 : rest;
}
```

---

## 8. When Recursion Is the Right Choice

Recursion shines when a problem has a naturally recursive structure:
- **Trees and hierarchical data** (next lecture): a tree is defined in terms of smaller trees
- **Divide-and-conquer algorithms** (merge sort, quicksort — Lecture 2): split, recurse, combine
- **Backtracking search** (permutations, combinations, puzzle solving — Lecture 2): try, recurse, undo
- **Problems with a recursive mathematical definition**: factorial, Fibonacci, Ackermann function, GCD

Recursion is a poor choice when:
- The recursion depth could be very large (risk of stack overflow) and the problem is simple to express iteratively
- Performance is critical and the overhead of repeated function calls matters (embedded systems, tight inner loops)
- The problem has overlapping subproblems without memoization (exponential blowup, as in naive Fibonacci)

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Instrument the naive recursive Fibonacci with a call counter. Report the counts for n = 5, 10, 15, 20 and find the closed form.

**2. (Explain.)** State the two conditions a recursive function needs to terminate. Then explain why this one crashes, and what error you see.

```c
int countdown(int n) {
    if (n == 0) return 0;
    return countdown(n - 1);
}
/* called as countdown(-1) */
```

**3. (Build.)** Write recursive versions of: `gcd(a, b)` by Euclid's algorithm, and `power(base, exp)` in O(log exp). Give the recurrence for each.

**4. (Stretch.)** Convert this recursive function to an iterative one, and explain the general rule for when the conversion is trivial.

```c
long sum_to(int n) {
    if (n <= 0) return 0;
    return n + sum_to(n - 1);
}
```


### Answers

**1.** `fib(5)` → **15** calls, `fib(10)` → **177**, `fib(15)` → **1,973**, `fib(20)` → **21,891**.

```c
static long calls;
static long fib(int n) {
    calls++;
    return n < 2 ? n : fib(n-1) + fib(n-2);
}
```

The closed form is **calls(n) = 2·fib(n+1) − 1**. Check: `fib(6) = 8`, and 2·8 − 1 = 15 ✓; `fib(21) = 10946`, and 2·10946 − 1 = 21891 ✓.

The reason is structural: each call returning a base case contributes 1 to the result, so there are exactly `fib(n)` leaves in the recursion tree. In a binary tree where every internal node has two children, internal nodes number one fewer than leaves, giving 2·fib(n) − 1 nodes under the corresponding base-case convention.

Since `fib(n)` grows as φⁿ/√5 with φ ≈ 1.618, the call count is **Θ(φⁿ)**. That is the measurable cost of recomputing overlapping subproblems: `fib(40)` needs over 300 million calls and takes about a second, while the iterative version is instant. Note this is *not* an argument against recursion — Hanoi and tree traversal are recursive and efficient. It is an argument against recursion **on overlapping subproblems** without memoisation.

**2.** The two conditions are:

1. **A base case that is actually reachable** from every legal input.
2. **Each recursive call moves strictly toward it** — a *variant*, bounded below and decreasing.

`countdown(-1)` satisfies neither. `n` decreases forever, so the second condition holds in the sense that it moves, but it moves **away** from the base case; and `n == 0` is never reached because `n` starts below it and only decreases.

The result is unbounded recursion. Each call pushes a stack frame, the 8 MB stack fills after a few hundred thousand frames, and the next push touches the guard page — **SIGSEGV, "Segmentation fault"**. There is no message about recursion, because nothing is counting; the hardware notices, not the language. Under `-fsanitize=address` you instead get an explicit *stack-overflow* report with a backtrace, which is far more useful.

**The fix is an inequality:** `if (n <= 0) return 0;`.

This generalises. An `==` base case assumes the parameter lands exactly on the target value, which fails for any step that can overshoot — decrementing by 2, dividing, or subtracting a computed amount. **Prefer `<=` or `>=`, and state the variant explicitly**: here it would be `n`, bounded below by 0 — which is precisely the assumption `-1` violates. A `precondition: n >= 0` comment plus an `assert` documents it.

**3.**

```c
int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}

long power(long base, int exp) {
    if (exp == 0) return 1;
    long half = power(base, exp / 2);
    return (exp % 2) ? half * half * base : half * half;
}
```

**`gcd`** — `gcd(48, 18)` = 6, `gcd(17, 5)` = 1. Its recurrence is not a simple T(n/b): each step replaces `(a, b)` with `(b, a mod b)`, and the worst case is **consecutive Fibonacci numbers**, giving **O(log min(a,b))** steps. Lamé's theorem makes this precise, and it is the first non-trivial complexity bound in the history of algorithms.

**`power`** — T(n) = T(n/2) + O(1), so **O(log exp)**. `power(2, 10)` = 1024, `power(3, 5)` = 243. The trick is exponentiation by squaring: computing `half` **once** and reusing it. Writing `power(base, exp/2) * power(base, exp/2)` looks identical and is **O(exp)**, because the two calls are evaluated separately — the same overlapping-subproblem trap as Fibonacci, in a place where it is easy to miss.

Both are naturally **tail-recursive or nearly so**, and GCC at `-O2` compiles `gcd` into a loop with no stack growth. Do not rely on that: it is an optimisation, not a guarantee, and it disappears at `-O0`.

Note `power` will overflow `long` for modest inputs — `power(2, 63)` is undefined behaviour. Real implementations compute modulo something, which is exactly what RSA needs.

**4.**

```c
long sum_to(int n) {
    long total = 0;
    for (int i = 1; i <= n; i++) total += i;
    return total;
}
```

The rule: **conversion is trivial exactly when the recursion is in tail position** — when nothing remains to be done after the recursive call returns. Then the call is just "start over with different values", which is what a loop is, and no stack is needed.

The function above is *not* quite tail-recursive as written: `n + sum_to(n - 1)` must add `n` **after** the call returns, so each frame has pending work. Adding an accumulator moves the work before the call and makes it a genuine tail call:

```c
long sum_to_acc(int n, long acc) {
    if (n <= 0) return acc;
    return sum_to_acc(n - 1, acc + n);      /* nothing pending */
}
```

and that form maps to the loop mechanically: the accumulator becomes a local, the call becomes the next iteration, the base case becomes the exit.

**Non-tail recursion needs an explicit stack** to hold the pending work — which is what tree traversal and backtracking require, and why they are genuinely harder to convert. The amount of state the stack must carry equals the work pending after the call.

For this particular function there is a third answer: `n * (n + 1) / 2`, in O(1). Recognising a closed form beats optimising the loop.



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Base case** | The simplest input(s), solved directly without recursion |
| **Recursive case** | The step that reduces the problem to a strictly simpler subproblem |
| **Stack overflow** | Exhausting the stack by pushing too many frames — the failure mode of unterminated/too-deep recursion |
| **Tail recursion** | A recursive call that is the last operation performed, with nothing pending afterward |
| **Tail call optimization (TCO)** | Compiler transformation reusing a stack frame for a tail call instead of pushing a new one |
| **Memoization** | Caching results of subproblems to avoid redundant recomputation |
| **Overlapping subproblems** | When a naive recursive algorithm solves the same subproblem multiple times |

---

## Reading

- **K&R** does not cover recursion extensively — refer to **King Ch. 18** — Recursion (full chapter)
- **CLRS Ch. 4** — Divide-and-Conquer (mathematical treatment of recursive algorithm analysis)
- **SICP §1.2** — Procedures and the Processes They Generate (recursive vs iterative processes — a classic exposition)

---

*Next: Lecture 2 — Recursive Algorithms: Divide-and-Conquer and Backtracking*
