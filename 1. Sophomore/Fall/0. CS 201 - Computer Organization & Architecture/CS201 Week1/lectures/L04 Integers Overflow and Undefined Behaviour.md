# CS 201 · Computer Organization & Architecture
## Week 1 · Lecture 1 of 3
### Integers, Overflow, and Undefined Behaviour

*“Make no mistake about it: Computers process numbers - not symbols. We measure our understanding (and control) by the extent to which we can arithmetize an activity.”* — Alan Perlis, "Epigrams on Programming" (1982), #65

---

**Reading:** CS:APP §2.2–2.3 · **Previous:** L03, the shape of x86-64

**Coursework:** 📊 **Quiz 1** today · 📝 **PS 1** released Wed this week, due Fri of Week 2 17:00

---

## 1. What ECE 110 Already Gave You

You built a two's complement adder out of gates. You know that:

- An $n$-bit two's complement value spans $-2^{n-1}$ to $2^{n-1}-1$.
- Negation is invert-and-add-one.
- There is **one** zero, which is why the range is asymmetric.
- Subtraction reuses the adder, which is why two's complement won.
- **Carry-out and signed overflow are different flags**, and all four combinations occur.

**None of that is re-taught.** This lecture is about the consequence that ECE 110 could not show you: at the gate level, overflow is a *flag*. In C, signed overflow is **undefined behaviour**, and that is a much stranger thing.

---

## 2. The Hardware Does Not Trap

$-128$ in 8-bit two's complement negated is $-128$:

$$\texttt{10000000} \xrightarrow{\text{invert}} \texttt{01111111} \xrightarrow{+1} \texttt{10000000}$$

**The hardware sets OF and carries on.** It does not fault, does not stop, does not tell anyone. If nobody reads OF, the wrong value simply propagates.

C, on x86-64, never reads it. There is no code in a normal C program that checks the overflow flag after an `add`. So at the machine level, signed overflow **wraps silently**, exactly as unsigned does.

**This is where most people stop, and it is where the actual problem starts.**

---

## 3. Undefined Behaviour Is Not "Whatever The Hardware Does"

The C standard says signed overflow is *undefined behaviour*: the standard imposes no requirement at all. Most students read this as "so you get the wrapped value, which is machine-dependent but harmless."

That is wrong, and here is the proof.

```c
int  always_true(int x)      { return x + 1 > x; }   /* signed   */
unsigned uns(unsigned x)     { return x + 1 > x; }   /* unsigned */
```

Mathematically these look identical. Compile at `-O2` and look:

```
0000000000001190 <always_true>:
    1190:  endbr64
    1194:  mov    eax,0x1
    1199:  ret
```

```
00000000000011a0 <uns>:
    11a0:  endbr64
    11a4:  xor    eax,eax
    11a6:  cmp    edi,0xffffffff
    11a9:  setne  al
    11ac:  ret
```

*(Verified — GCC 13.3.0, `-O2`.)*

**`always_true` does not compute anything.** It returns the constant 1. There is no addition, no comparison. The function **cannot** return 0 for any input, including `INT_MAX`.

**`uns` really does compare.** It checks `x != 0xffffffff`, because unsigned wraparound is *defined* to be modular, so `UINT_MAX + 1 == 0`, and `0 > UINT_MAX` is genuinely false. GCC is obliged to get that case right.

Confirming at run time:

```
signed   always_true(INT_MAX) = 1
unsigned uns(UINT_MAX)        = 0
```

*(Verified at both `-O0` and `-O2`.)*

> **The reasoning GCC used.** "Signed overflow is undefined. A program with undefined behaviour has
> no meaning, so I may assume it never happens. If `x + 1` never overflows, then `x + 1 > x` is
> always true. Return 1."
>
> **This is not a compiler bug and it is not malice.** It is the compiler using a licence the
> standard granted it, and that licence is worth real performance — it is what lets loop bounds be
> proven monotonic and induction variables be widened to 64 bits. **You cannot have both the
> optimisation and the wraparound.**

---

## 4. Why This Is a Security Topic, Not a Pedantry Topic

The classic form:

```c
char *buf = malloc(n + 1);        /* n is int, attacker-controlled */
if (len < n) memcpy(buf, src, len);
```

If `n` is `INT_MAX`, then `n + 1` overflows. The compiler is entitled to assume it did not — so a check written to guard against it may be **deleted as provably redundant**. The allocation is tiny; the copy is not.

**The bug is not that the value wrapped. The bug is that your check disappeared.**

Real instances of exactly this pattern have produced remote code execution in widely deployed software. Week 9 returns to it once you can see the stack.

---

## 5. Writing It Correctly

| Want | Do |
|---|---|
| Wraparound arithmetic | Use `unsigned`. It is defined to be modulo $2^n$ |
| Detect overflow | `__builtin_add_overflow(a, b, &r)` — returns true on overflow, compiles to one `add` plus a `jo` |
| Guarantee wrapping on signed | `gcc -fwrapv`. Defines the behaviour, and costs some optimisation |
| Find it in existing code | `gcc -fsanitize=undefined`, which traps at run time and prints the line |

**`-fsanitize=undefined` is the one to remember.** It is how you discover that code you inherited has been relying on undefined behaviour for years. You will use it in Lab 1 and in PS 1.

---

## 6. Signed and Unsigned Do Not Mix

C's *usual arithmetic conversions* say that when a signed and an unsigned operand of the same rank meet, **the signed one is converted to unsigned.**

```c
int  a = -1;
unsigned b = 1;
if (a < b) puts("as expected");
else       puts("surprise");
```

This prints `surprise`. `-1` converts to `4294967295`, which is not less than 1.

The classic loop bug:

```c
for (int i = 0; i < strlen(s) - 1; i++)  /* strlen returns size_t (unsigned) */
```

For an **empty string**, `strlen(s) - 1` is not $-1$; it is `SIZE_MAX`. The loop runs about $1.8 \times 10^{19}$ times and reads far off the end of the buffer.

> **The rule to carry:** the moment an expression mixes signedness, stop and work out which conversion
> happens. C's answer is rarely the intuitive one, and the compiler warns about only some of these
> (`-Wsign-compare`, which is *not* in `-Wall` for C).

---

## 7. What to Take Away

1. **The hardware sets a flag and continues.** Nothing traps.
2. **Undefined behaviour is a licence to assume, not a promise to wrap.** `x + 1 > x` compiled to `mov eax,0x1`.
3. **Unsigned overflow is defined**; the same expression compiled to a real comparison.
4. **Deleted overflow checks are a real exploit class**, not a curiosity.
5. **Mixed signed/unsigned converts toward unsigned**, and `strlen(s) - 1` on an empty string is enormous.

---

## Exercises

1. `always_true` returns 1 unconditionally at `-O2`. At `-O0` it performs the addition and comparison. Is the `-O0` build *more correct*? Argue both sides, then say what the standard makes of the question.
2. Compile `always_true` with `-O2 -fwrapv` and disassemble. Predict the output first.
3. Why is `unsigned` wraparound defined by the standard when signed wraparound is not? *(Hint: what did signed representation look like in 1989, and how many schemes were in use?)*
4. Rewrite the `malloc(n + 1)` fragment so that it is correct for every `int` value of `n`, using `__builtin_add_overflow`.
5. For `int i` and `size_t n`, `i < n` triggers `-Wsign-compare`. Give a value of `i` and `n` for which the comparison gives the mathematically wrong answer, and one for which it is fine.

---

*Next: L05 — how a float is actually laid out, and why 0.1 is not 0.1.*
