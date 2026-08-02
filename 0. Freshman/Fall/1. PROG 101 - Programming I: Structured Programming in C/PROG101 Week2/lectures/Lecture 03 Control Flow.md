# PROG 101 · Programming I: Structured Programming in C
## Week 2 · Lecture 3: Control Flow — if, switch, while, for

---

## Lecture Goals

By the end of this lecture you will:
- Write correct and idiomatic `if/else if/else` chains
- Use `switch` appropriately and understand fallthrough
- Master `while`, `do-while`, and `for` loops
- Understand `break` and `continue`
- Trace any loop by hand using a variable table
- Know when each loop construct is the right choice

---

## 1. The Three Control Structures (Böhm-Jacopini Theorem)

In 1966, mathematicians Böhm and Jacopini proved something profound: **any computable algorithm can be expressed using only three control structures:**

1. **Sequence** — one statement after another
2. **Selection** — choose between paths (`if/else`, `switch`)
3. **Iteration** — repeat (`while`, `for`, `do-while`)

This is why `goto` is unnecessary (not just ugly — mathematically superfluous). Every modern language — Python, Java, Rust — is built on these three structures. C makes them explicit and close to the machine.

---

## 2. Selection: `if`, `else if`, `else`

### Basic Syntax

```c
if (condition) {
    /* executed if condition is non-zero (true) */
} else if (another_condition) {
    /* executed if first was false AND this is non-zero */
} else {
    /* executed if all conditions above were false */
}
```

Braces `{}` are technically optional for single statements, but **always use them**:

```c
// DANGEROUS — without braces, only one line is in the if:
if (x < 0)
    printf("negative\n");
    x = 0;           // This ALWAYS executes, regardless of condition!

// CORRECT — braces make the block explicit:
if (x < 0) {
    printf("negative\n");
    x = 0;
}
```

This bug (Apple's "goto fail" SSL bug in 2014) caused a critical security vulnerability that was in production code for years. Always use braces.

### Conditions in C

Any expression that produces a non-zero value is "true" in C:

```c
int x = 5;
if (x)          // true: x is non-zero
if (x - 5)      // false: 5-5 = 0
if (x = 10)     // true: assigns 10 to x, then tests 10 (non-zero)
if (x == 10)    // true: compares x to 10
```

### Nesting and Dangling Else

The `else` clause always belongs to the **nearest** `if`:

```c
if (a > 0)
    if (b > 0)
        printf("both positive\n");
else               // This belongs to 'if (b > 0)', NOT 'if (a > 0)'
    printf("b is not positive\n");
```

This is the "dangling else" problem. Use braces to make intent explicit:

```c
if (a > 0) {
    if (b > 0) {
        printf("both positive\n");
    }
} else {
    printf("a is not positive\n");    // Now clearly belongs to if(a > 0)
}
```

### Practical Patterns

```c
/* Pattern: guard clause — return early on invalid input */
int divide(int a, int b) {
    if (b == 0) {
        fprintf(stderr, "Error: division by zero\n");
        return -1;    /* Early return — avoid deep nesting */
    }
    return a / b;
}

/* Pattern: clamp a value to a range */
if (x < MIN) x = MIN;
else if (x > MAX) x = MAX;

/* Pattern: categorize */
if (score >= 90)      grade = 'A';
else if (score >= 80) grade = 'B';
else if (score >= 70) grade = 'C';
else if (score >= 60) grade = 'D';
else                  grade = 'F';
```

---

## 3. Selection: `switch`

`switch` tests an integer expression against a series of constant cases:

```c
switch (expression) {
    case constant1:
        /* code */
        break;
    case constant2:
        /* code */
        break;
    case constant3:
    case constant4:    /* fall through: both cases run same code */
        /* code */
        break;
    default:
        /* code when no case matches */
        break;
}
```

### The `break` Requirement

Without `break`, execution **falls through** to the next case:

```c
int x = 2;
switch (x) {
    case 1:
        printf("one\n");
    case 2:
        printf("two\n");    // Prints "two"
    case 3:
        printf("three\n");  // Also prints "three" — FALLTHROUGH!
    default:
        printf("other\n");  // Also prints "other"!
}
// Output: two, three, other
```

This is almost always a bug. Always include `break` unless fallthrough is intentional (and document it):

```c
switch (op) {
    case '+':
        result = a + b;
        break;
    case '-':
        result = a - b;
        break;
    case '*':
        result = a * b;
        break;
    case '/':
        if (b == 0) {
            fprintf(stderr, "Division by zero\n");
            return -1;
        }
        result = a / b;
        break;
    default:
        fprintf(stderr, "Unknown operator: %c\n", op);
        return -1;
}
```

### When to Use `switch` vs `if/else if`

Use `switch` when:
- Testing a single integer/char/enum against many specific values
- The values are constants (known at compile time)
- Readability improves over a long `if/else if` chain

Use `if/else if` when:
- Testing ranges (`x > 10 && x < 20`)
- Testing different variables or expressions
- Testing non-integer types (floats — switch doesn't work)

### `switch` on Characters

```c
char cmd;
scanf(" %c", &cmd);    /* note the space before %c: skips whitespace */

switch (cmd) {
    case 'q': case 'Q':
        printf("Quit\n");
        break;
    case 'h': case 'H':
        printf("Help\n");
        break;
    default:
        printf("Unknown command: %c\n", cmd);
}
```

---

## 4. Iteration: `while`

```c
while (condition) {
    /* body — executed while condition is non-zero */
}
```

The condition is checked **before** each iteration. If false initially, the body never executes.

```c
/* Count down from 10 */
int n = 10;
while (n > 0) {
    printf("%d\n", n);
    n--;
}
/* After the loop: n == 0 */

/* Read until valid input */
int x;
printf("Enter a positive integer: ");
while (scanf("%d", &x) != 1 || x <= 0) {
    printf("Invalid. Try again: ");
    /* Clear invalid input from buffer */
    while (getchar() != '\n');  /* inner loop: discard line */
}
```

### Loop Invariants

A **loop invariant** is a property that is:
1. True **before** the loop begins
2. True **after each iteration**
3. Combined with the exit condition, implies the loop's correctness

This is how you *prove* a loop is correct — not by testing it, but by reasoning about it.

```c
/* Find the maximum element in an array */
int max = arr[0];    // INVARIANT: max is the maximum of arr[0..i-1]
int i = 1;

while (i < n) {
    /* At this point: max is max of arr[0..i-1] */
    if (arr[i] > max) {
        max = arr[i];
    }
    i++;
    /* At this point: max is max of arr[0..i-1] (one element larger range) */
}
/* Loop exit: i == n */
/* Invariant + exit condition: max is max of arr[0..n-1] = max of entire array */
```

The invariant tells you *why* the loop is correct, not just *that* it produces correct output on your test cases.

---

## 5. Iteration: `do-while`

```c
do {
    /* body — executed at least once */
} while (condition);
```

The condition is checked **after** each iteration. The body always runs at least once.

Use `do-while` when the body must execute before the condition can be evaluated:

```c
/* Menu loop — always show menu first, then check choice */
int choice;
do {
    printf("\n=== Menu ===\n");
    printf("1. New game\n");
    printf("2. Load game\n");
    printf("3. Quit\n");
    printf("Choice: ");
    scanf("%d", &choice);
} while (choice < 1 || choice > 3);

/* Digit sum — process at least one digit */
int n = 12345;
int digit_sum = 0;
do {
    digit_sum += n % 10;    /* extract last digit */
    n /= 10;                 /* remove last digit */
} while (n > 0);
```

---

## 6. Iteration: `for`

The `for` loop is syntactic sugar for a `while` loop with initialization and increment in the header:

```c
for (initialization; condition; increment) {
    /* body */
}

/* Equivalent while: */
initialization;
while (condition) {
    /* body */
    increment;
}
```

```c
/* Standard counting loop */
for (int i = 0; i < 10; i++) {
    printf("%d\n", i);
}

/* Counting down */
for (int i = 9; i >= 0; i--) {
    printf("%d\n", i);
}

/* Step by 2 */
for (int i = 0; i <= 100; i += 2) {
    printf("%d\n", i);
}

/* Multiple variables (comma operator) */
for (int i = 0, j = 10; i < j; i++, j--) {
    printf("i=%d, j=%d\n", i, j);
}
```

Any part of the `for` header can be omitted:

```c
/* Infinite loop */
for (;;) {
    /* runs forever — must break out */
    if (some_condition) break;
}

/* No initialization (variable declared outside) */
int i = 0;
for (; i < n; i++) { ... }

/* No increment (done in body) */
for (int i = 0; i < n; ) {
    if (arr[i] == target) break;
    i++;    /* conditional increment in body */
}
```

### When to Use Which Loop

| Loop | Best For |
|------|----------|
| `for` | Counting loops, known iteration count |
| `while` | Loop while a condition holds, unknown iteration count |
| `do-while` | Body must execute at least once (menus, input validation) |

---

## 7. `break` and `continue`

### `break` — Exit the Loop

`break` immediately exits the **innermost** enclosing loop or `switch`:

```c
/* Search for a value */
int found = -1;
for (int i = 0; i < n; i++) {
    if (arr[i] == target) {
        found = i;
        break;    /* Stop searching once found */
    }
}

/* Nested loops: break only exits the innermost */
for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
        if (matrix[i][j] < 0) {
            break;    /* Only exits the j-loop, not the i-loop */
        }
    }
}
```

To break out of nested loops, use a flag variable or a labeled approach:

```c
int done = 0;
for (int i = 0; i < rows && !done; i++) {
    for (int j = 0; j < cols && !done; j++) {
        if (matrix[i][j] < 0) {
            done = 1;
        }
    }
}
```

### `continue` — Skip to Next Iteration

`continue` skips the rest of the loop body and jumps to the next iteration:

```c
/* Print only positive numbers */
for (int i = 0; i < n; i++) {
    if (arr[i] <= 0) continue;    /* skip negatives and zero */
    printf("%d\n", arr[i]);
}

/* Process only lines starting with '#' (comments) */
while (fgets(line, sizeof(line), file)) {
    if (line[0] != '#') continue;
    process_comment(line);
}
```

---

## 8. Tracing Loops by Hand

The most important debugging skill for loops: trace execution manually using a variable table.

**Example:** Trace this loop for `n = 5`:

```c
int sum = 0;
for (int i = 1; i <= n; i++) {
    sum += i;
}
```

| Iteration | `i` (before) | condition `i <= 5` | `sum += i` | `i` (after `i++`) |
|-----------|-------------|-------------------|------------|-------------------|
| 0 (init) | 1 | true | 0+1=1 | 2 |
| 1 | 2 | true | 1+2=3 | 3 |
| 2 | 3 | true | 3+3=6 | 4 |
| 3 | 4 | true | 6+4=10 | 5 |
| 4 | 5 | true | 10+5=15 | 6 |
| 5 | 6 | false | — loop exits — | — |

Final: `sum = 15 = 1+2+3+4+5` ✓

Trace every loop you write during this course until you can do it in your head. It is the only way to develop intuition for loop correctness.

---

## 9. Common Loop Patterns

```c
/* Sum all elements */
int sum = 0;
for (int i = 0; i < n; i++) sum += arr[i];

/* Count elements satisfying a condition */
int count = 0;
for (int i = 0; i < n; i++)
    if (arr[i] > 0) count++;

/* Find minimum */
int min = arr[0];
for (int i = 1; i < n; i++)
    if (arr[i] < min) min = arr[i];

/* Linear search — return index or -1 */
int linear_search(int arr[], int n, int target) {
    for (int i = 0; i < n; i++)
        if (arr[i] == target) return i;
    return -1;
}

/* Reverse an array in-place */
for (int i = 0, j = n-1; i < j; i++, j--) {
    int tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
}

/* Print multiplication table */
for (int i = 1; i <= 10; i++) {
    for (int j = 1; j <= 10; j++) {
        printf("%4d", i * j);
    }
    printf("\n");
}
```

---

## 10. The Infinite Loop and When to Use It

```c
/* Server main loop */
while (1) {
    int client = accept(server_fd, NULL, NULL);
    if (client < 0) {
        perror("accept");
        continue;
    }
    handle_client(client);
}

/* Event loop */
for (;;) {
    Event e = get_next_event();
    if (e.type == EVENT_QUIT) break;
    handle_event(e);
}
```

Infinite loops with explicit `break` conditions are valid and common in systems programming. They are not a sign of bad code — they are the appropriate structure for programs that run until told to stop.

---

## Practice Exercises

Work these before the next lecture. Each set moves from *trace* (predict what happens) through *explain* (say why) to *build* (write it yourself) and finally *stretch* (a step past the lecture). Answers are at the end of the section — attempt each exercise before reading them.

**1. (Trace.)** Predict the output. It is not what the indentation suggests.

```c
int x = 5;
switch (x) {
    case 5:
        printf("five\n");
    case 6:
        printf("six\n");
        break;
    case 7:
        printf("seven\n");
}
```

**2. (Explain.)** Explain the dangling-else problem using the code below. State which `if` the `else` binds to, and give the rule.

```c
if (a > 0)
    if (b > 0)
        printf("both\n");
else
    printf("else branch\n");
```

**3. (Build.)** Write three loops that print the integers 1 to 10: one `while`, one `do-while`, one `for`. Then state the one situation where `do-while` is genuinely the right choice.

**4. (Stretch.)** Each loop below has a bug. Identify it and give the fix.

```c
/* A */ for (int i = 0; i < 10; i++);
            sum += i;

/* B */ int i = 0;
        while (i < 10) {
            if (arr[i] < 0) continue;
            total += arr[i];
            i++;
        }

/* C */ for (double d = 0.0; d != 1.0; d += 0.1) count++;
```


### Answers

**1.**

```
five
six
```

`case` labels are **entry points, not blocks.** Control jumps to `case 5:` and then runs straight through every following statement until it meets a `break` or the closing brace. `case 6:` is just a label along the way and does not stop anything, so `six` prints too. `seven` does not, because the `break` after it comes first.

This is **fall-through**, and it is deliberate — it makes grouped cases natural:

```c
case 'a': case 'e': case 'i': case 'o': case 'u':
    vowels++;
    break;
```

But unintentional fall-through is a common bug, so mark the intentional ones. GCC's `-Wimplicit-fallthrough` (in `-Wextra`) warns unless you annotate with `__attribute__((fallthrough))` or a `/* fall through */` comment; C23 standardises `[[fallthrough]]`.

Two related rules worth knowing: `default:` may appear anywhere, not only last, and it also falls through. And declaring a variable directly after a `case` label without braces is an error — `case 1: int y = 0;` needs `case 1: { int y = 0; }`.

**2.** The `else` binds to the **inner** `if (b > 0)`, despite the indentation.

The rule is that **an `else` attaches to the nearest preceding unmatched `if`** within the same block. Indentation is whitespace and carries no meaning in C; the parser sees only the token sequence. So with `a = 1, b = -1` this prints `else branch`, and with `a = -1` it prints **nothing at all** — which is usually the opposite of what the author intended.

The fix is unconditional: **always brace the bodies.**

```c
if (a > 0) {
    if (b > 0) {
        printf("both\n");
    }
} else {
    printf("else branch\n");
}
```

Now the binding is explicit and the indentation is honest.

This is not a hypothetical hazard. Apple's 2014 "goto fail" TLS vulnerability was a duplicated unbraced line that made the certificate-verification result unreachable, and every affected iOS and OS X device accepted forged certificates. GCC's `-Wmisleading-indentation` (in `-Wall`) exists specifically to catch code whose layout disagrees with its parse, and it would have flagged that bug.

**3.**

```c
/* while */
int i = 1;
while (i <= 10) { printf("%d ", i); i++; }

/* do-while */
int j = 1;
do { printf("%d ", j); j++; } while (j <= 10);

/* for */
for (int k = 1; k <= 10; k++) printf("%d ", k);
```

`do-while` is right when **the body must run at least once before the condition can be evaluated** — typically because the condition depends on something the body produces. Input validation is the canonical case:

```c
int value;
do {
    printf("Enter a positive number: ");
    if (scanf("%d", &value) != 1) { /* clear the bad input */ while (getchar() != '\n'); value = -1; }
} while (value <= 0);
```

You cannot test `value` before reading it, so a `while` loop would need the read duplicated above the loop.

Otherwise prefer `for` when the iteration count or range is known, since it gathers initialisation, test, and update on one line where they can be checked against each other — most off-by-one errors are visible at a glance in a `for` header and scattered across ten lines in a `while`. Note the C99 form `for (int k = ...)` scopes `k` to the loop, which is why `k` is unavailable afterwards while `i` and `j` leak into the enclosing block.

**4.** **A — stray semicolon.** `for (...);` has an **empty body**, so the loop spins ten times doing nothing and `sum += i` runs once afterwards. Worse, with C99 scoping `i` does not exist outside the loop, so this is also a compile error — which is lucky, because the pre-C99 version compiled and silently did the wrong thing. `-Wempty-body` warns. Fix: delete the semicolon and brace the body.

**B — `continue` skips the increment.** When `arr[i]` is negative, `continue` jumps to the condition test with `i` unchanged, so the loop spins forever on that element. This is the classic `continue` bug, and it exists because the increment is at the *bottom* of the body. Fix: increment before the `continue`, or use a `for` loop, whose update runs even on `continue`.

**C — floating-point equality.** `0.1` is not exactly representable in binary, so the accumulated sum steps over `1.0` without ever equalling it and the loop runs essentially forever (until `d` grows large enough that adding 0.1 changes nothing). Fix: use an **integer** counter and derive the double — `for (int n = 0; n < 10; n++) { double d = n * 0.1; ... }` — which also avoids accumulating rounding error. If you must compare floats, use `fabs(a - b) < epsilon`, never `==`.

All three share a theme: **the loop's termination depends on something the author assumed rather than checked.**



---

## Key Vocabulary

| Term | Definition |
|------|-----------|
| **Selection** | Control structure that chooses between paths: `if`, `switch` |
| **Iteration** | Control structure that repeats: `while`, `for`, `do-while` |
| **Fallthrough** | Execution continues past a `case` without a `break` |
| **Loop invariant** | A property true before, during, and after every loop iteration |
| **Guard clause** | An early `return`/`break` that handles edge cases before the main logic |
| **Short-circuit** | `&&` and `\|\|` skip right operand when result is determined by left |
| **`break`** | Immediately exits the innermost loop or switch |
| **`continue`** | Skips to the next loop iteration |
| **Dangling else** | Ambiguity when an `else` could match multiple `if` statements |
| **Böhm-Jacopini** | Theorem: all algorithms expressible with sequence, selection, iteration |

---

## Reading

- K&R §2.6–2.9 (Relational and Logical Operators, Increment/Decrement)
- K&R §3.1–3.8 (Control Flow — the entire chapter)
- King Ch. 5 (Selection), Ch. 6 (Loops)

---

*Next: Lab 1 — Bit Manipulation and Loop Tracing*
