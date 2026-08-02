# PROG 101 · Week 2 Reference
## Operator Precedence · Evaluation Order · Control Flow

---

## Part 1: Operator Precedence (highest to lowest)

| Level | Operators | Associativity |
|---|---|---|
| 1 | `()` `[]` `.` `->` postfix `++ --` | left → right |
| 2 | prefix `++ --` `+ -` `! ~` `(cast)` `*` `&` `sizeof` | right → left |
| 3 | `*` `/` `%` | left → right |
| 4 | `+` `-` | left → right |
| 5 | `<<` `>>` | left → right |
| 6 | `<` `<=` `>` `>=` | left → right |
| 7 | `==` `!=` | left → right |
| 8 | `&` | left → right |
| 9 | `^` | left → right |
| 10 | `\|` | left → right |
| 11 | `&&` | left → right |
| 12 | `\|\|` | left → right |
| 13 | `?:` | right → left |
| 14 | `=` `+=` `-=` … | right → left |
| 15 | `,` | left → right |

### The four traps

| You wrote | C parsed | Fix |
|---|---|---|
| `a & b == c` | `a & (b == c)` | `(a & b) == c` |
| `1 << 2 + 3` | `1 << (2 + 3)` = 32 | `(1 << 2) + 3` = 7 |
| `!a == b` | `(!a) == b` | `!(a == b)` |
| `*p++` | `*(p++)` | `(*p)++` |

**Bitwise operators bind looser than comparisons.** This is the one to memorise — it is a historical
accident of C's grammar, and it is why `-Wparentheses` exists.

`-Wall -Wextra` warns on the first two but **not** on `a + b % c`, because `%` binding tighter than
`+` surprises nobody.

---

## Part 2: Arithmetic Facts

| Expression | Value |
|---|---|
| `-7 / 2` | `-3` |
| `-7 % 2` | `-1` |
| `7 / -2` | `-3` |
| `7 % -2` | `1` |
| `~5` | `-6` |
| `5 & 3` | `1` |
| `5 \| 3` | `7` |
| `5 ^ 3` | `6` |

**C99 rule:** division **truncates toward zero**; the sign of `a % b` follows **`a`**.

The identity `(a/b)*b + a%b == a` holds in every case.

> **Different from Python.** Python floors: `-7 // 2 == -4`, `-7 % 2 == 1`. If you are taking CS 101
> concurrently, do not carry the intuition across.

---

## Part 3: Bit Manipulation Idioms

```c
enum { FLAG_A = 1u << 0, FLAG_B = 1u << 1, FLAG_C = 1u << 2 };
```

| Operation | Idiom |
|---|---|
| Set | `p \|= FLAG;` |
| Clear | `p &= ~FLAG;` |
| Toggle | `p ^= FLAG;` |
| Test | `(p & FLAG) != 0` |

**Always `1u << n`, never `1 << n`.** For a signed `int`, `1 << 31` sets the sign bit and is
**undefined behaviour** — UBSan reports
`left shift of 1 by 31 places cannot be represented in type 'int'`. An `unsigned int` has no sign
bit and its shifts are defined modulo 2³².

**Test must normalise.** `(p & FLAG) != 0` yields exactly `0` or `1`; `p & FLAG` yields the mask
value, which is `4` for `FLAG_C`, not `1`.

---

## Part 4: The Four Categories of "It Depends"

| Category | Meaning | Example |
|---|---|---|
| **Well defined** | One outcome, guaranteed | `1 + 1` |
| **Unspecified** | Several outcomes allowed, no documentation required | order of `f() + g()` |
| **Implementation-defined** | Several outcomes, but the compiler must document its choice | `-1 >> 1` |
| **Undefined** | **No requirement whatsoever** | `i = i++`, `INT_MAX + 1` |

**Undefined is the dangerous one.** The compiler may assume it never happens and optimise on that
assumption, so the damage can appear far from the offending line.

### Sequence points

Between two sequence points, an object may be modified **at most once**, and may be read only to
compute the value stored.

```c
i = i++;              /* UB: two writes to i          */
printf("%d %d", i++, i++);  /* UB: two writes, and unsequenced */
a[i] = i++;           /* UB: read of i not used to compute the write */
```

`-Wall` includes `-Wsequence-point`:

```
warning: operation on 'i' may be undefined [-Wsequence-point]
```

### What *is* guaranteed

- `&&` and `||` **short-circuit**, left to right, with a sequence point after the left operand
- The `,` operator sequences left before right
- `?:` evaluates the condition, then exactly one branch

---

## Part 5: Control Flow

### `switch`

- Controlling expression must be **integer** type (`int`, `char`, `enum` — not `double`, not a string)
- `case` labels must be **compile-time constants** and distinct
- Execution **falls through** to the next label without `break`

```c
case 1: printf("one "); /* fall through */
case 2: printf("two "); break;
```

**`-Wall -Wextra -Werror` rejects undocumented fallthrough** with
`error: this statement may fall through [-Werror=implicit-fallthrough=]`. The comment
`/* fall through */` (or C23 `[[fallthrough]]`) silences it without changing behaviour.

An empty chain never warns — there is no statement to fall through:

```c
case 'a': case 'e': case 'i': return 1;
```

### Loops

| Form | Test | Runs at least once? |
|---|---|---|
| `while (c) { }` | before | No |
| `do { } while (c);` | after | **Yes** |
| `for (init; c; step)` | before | No |

`for` and `while` are equivalent **except with `continue`**: in a `for` loop `continue` still runs
the step expression, so a hand-translation must place the step before the `continue` target or the
loop will not terminate.

### Common patterns

```c
/* accumulate */         for (int i = 0; i < n; i++) total += a[i];
/* search, early exit */ for (int i = 0; i < n; i++) if (a[i] == key) { found = i; break; }
/* read until EOF */     while ((c = getchar()) != EOF) { ... }
```

**`int c`, never `char c`,** for `getchar()` — `EOF` must be distinguishable from every valid
character value.

---

## Build Line

```
gcc -Wall -Wextra -Werror -pedantic -std=c11 -g
gcc -fsanitize=undefined            # catches signed overflow, bad shifts
```

---

*PROG 101 · Week 2 · Reference · © CSE Department*
