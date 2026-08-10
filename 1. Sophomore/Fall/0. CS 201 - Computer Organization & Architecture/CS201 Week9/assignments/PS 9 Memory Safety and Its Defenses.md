# CS 201 · Problem Set 9
## Memory Safety and Its Defenses

---

**Released:** Week 9, Wednesday · **Due:** Week 10, Friday 17:00
**Total: 100 points** · Submit one PDF plus a `.zip` of source, `PS9_{LastName}_{StudentID}.pdf`

> **This is a defensive problem set.** Every program you write or analyse is your own, compiled in a
> sandbox with defenses toggled to study them. **Q3 asks you to *fix* vulnerable code and *prove* the
> fix with a sanitizer — not to attack anything.**
>
> Project 1 was due last Friday; this problem set is lighter to leave room for the marking backlog.

---

### Q1: The Overflow and Its Defenses (24 points)

**(a) [4]** For `void vuln(const char *in){ char buf[16]; strcpy(buf, in); }`, with `buf` at `rbp-0x10`: draw the frame from `rbp-0x10` to `rbp+8` and state how many bytes of input reach the return address.

**(b) [5]** Compile it with today's defaults and quote the **four** canary instructions from the disassembly. Explain what each does, and why the canary is read from `fs:0x28` rather than a local variable.

**(c) [4]** Overflow it and report the result *(expected: stack smashing detected)*. Explain precisely what the check compared and why the attacker cannot simply supply the right value.

**(d) [5]** `readelf -lW` shows `GNU_STACK RW`. Name the attack the missing `E` prevents, and describe the attacker's response to it (name the technique).

**(e) [6]** Run your program five times printing `&main`, then five times under `setarch -R`. Report both. Explain what ASLR denies an attacker, why it does **not** fix the bug, and why the low 12 bits never change.

---

### Q2: The Arms Race (18 points)

**(a) [6]** Complete this table and give, for each row, one sentence on the mechanism:

| Attack | Defense | Attacker's response |
|---|---|---|
| Stack smash, inject code | ? | ? |
| ret2libc, known addresses | ? | ? |
| ROP gadget chain | ? | ? |

**(b) [4]** A gadget is "any useful instruction ending in `ret`". Count the `ret` instructions in `/bin/ls` and in libc on your machine *(reference: 203 and 6123)*. Explain why so many exist, and why the *usable* gadget count can exceed the `ret` count.

**(c) [4]** Explain how a ROP chain executes, in terms of what Week 3 said `ret` does. Why did NX not stop it?

**(d) [4]** `endbr64` appears at the start of every function *(count them in one of your binaries)*. Explain how CET's landing pads and shadow stack defeat the forward and backward edges of control flow respectively — and state how you would check whether the shadow stack is actually **enforced** on a given machine, versus merely compiled in.

---

### Q3: Fix the Bugs (34 points)

Below are four vulnerable functions. For **each**: identify the bug, explain the security consequence, write a corrected version, and **demonstrate the fix** — show the sanitizer or compiler catching the original and passing the fix.

**(a) [8]**
```c
char *dup_upper(const char *s) {
    char buf[64];
    strcpy(buf, s);
    for (char *p = buf; *p; p++) *p = toupper(*p);
    return strdup(buf);
}
```

**(b) [8]**
```c
void *make_array(size_t n) {
    int *a = malloc(n * sizeof(int));    /* n is attacker-controlled */
    for (size_t i = 0; i < n; i++) a[i] = 0;
    return a;
}
```

**(c) [8]**
```c
void log_msg(const char *user_msg) {
    fprintf(logfile, user_msg);
}
```

**(d) [10]**
```c
int *cache;
void set(int i, int v) { cache[i] = v; }     /* i unchecked */
int  get(int i)        { return cache[i]; }
void reset(void) { free(cache); cache = malloc(1024*sizeof(int)); }
/* ... some caller does: reset(); ... get(5); ... reset(); ... get(5); */
```

For (d), name **two** distinct bug classes present, not one.

> **"Demonstrate the fix" means evidence.** For (a) and (d): `-fsanitize=address` reports on the
> original, clean on the fix. For (b): show the wrapped size, and `calloc` or `__builtin_mul_overflow`
> refusing. For (c): the `-Wformat-security` warning, and a `%p` leak on the original.

---

### Q4: The Security Mindset (16 points)

**(a) [4]** State the three principles from L30 §6. For each, give one concrete example from **an earlier week** of the course.

**(b) [4]** A memory-*disclosure* bug (a leak) is as valuable as a memory-*corruption* bug. Explain why, naming the two defenses a leak defeats.

**(c) [4]** Explain a TOCTOU race with a concrete example, and make it atomic. Why is this a *security* bug and not merely a correctness bug?

**(d) [4]** "Every mitigation in Week 9 is compensation for C's permission to write out of bounds." Argue for or against, and name one language design that removes the vulnerability rather than raising its cost.

---

## Marks

| | |
|---|---:|
| Q1 The Overflow and Its Defenses | 24 |
| Q2 The Arms Race | 18 |
| Q3 Fix the Bugs | 34 |
| Q4 The Security Mindset | 16 |
| **Total** | **100** |

---

*CS 201 · Week 9 · Problem Set 9*
