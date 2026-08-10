# CS 201 · Computer Organization & Architecture
## Week 9 · Lecture 3 of 3
### Integer Overflows, Format Strings, and the Security Mindset

---

**Reading:** CS:APP §2.3 (revisited), §3.10 · **Previous:** L29, ROP and CFI

---

## 1. Not Every Bug Is on the Stack

L28 and L29 were about the stack. But the most valuable bugs today are elsewhere — in **integer arithmetic**, in **format strings**, and on the **heap** — and several of them let the attacker *read* memory, which L29 showed is worth as much as writing it.

**Every one of these is a bug you have already met in this course**, wearing a security consequence.

---

## 2. The Integer Overflow That Corrupts the Heap

This is Week 1 §L04 — undefined and wrapping arithmetic — as a vulnerability.

```c
void *bad_alloc(size_t count, size_t size) {
    size_t bytes = count * size;        /* can overflow */
    return malloc(bytes);
}
```

If an attacker controls `count`, they can make the multiplication wrap:

```
count=2305843009213693952 size=16 -> bytes=0 (want 2^65)
malloc returned 0x5819248532b0 — a tiny buffer for a huge request
```

*(Verified — $2^{61} \times 16 = 2^{65}$, which wraps to 0 in a 64-bit `size_t`.)*

**`malloc(0)` returns a valid, tiny pointer.** The caller believes it has an enormous buffer and copies enormous data into it — a **heap overflow**, and the check that should have caught it (`if (bytes >= needed)`) may itself have been computed from the wrapped value and passed.

**The fix is exactly Week 1's.** Use a checked multiply, or a checked allocator:

```
calloc(count, size) correctly returned (nil)   /* NULL = refused */
```

*(Verified — `calloc` detects the overflow internally and returns NULL rather than a small buffer.)* And `__builtin_mul_overflow(count, size, &bytes)` returns true on overflow, so you can refuse before allocating.

> **Week 1 warned that undefined signed overflow lets the compiler delete your check. This is the
> other half:** even defined, wrapping *unsigned* overflow silently produces a small number where you
> expected a large one, and the allocation sized from it is the vulnerability. **`malloc(a * b)` is a
> bug pattern**, and every serious codebase has a checked-multiply helper for exactly this.

---

## 3. The Format String That Reads the Stack

This is Week 8's data-versus-format confusion, and Week 3's stack, combined.

```c
void bad(const char *user)  { printf(user); }              /* user string AS format */
void good(const char *user) { printf("%s", user); }        /* the fix */
```

**If the user string contains format specifiers, `printf` acts on them** — and its arguments, when there are no real ones, are read straight off the stack:

```
$ ./prog '%p %p %p %p %p'
BAD  (printf(user)):  0x7ffc225cdbc0 (nil) (nil) 0x729342a03b20 (nil)
GOOD (printf(%s,user)): %p %p %p %p %p
```

*(Verified.)* **The `%p` specifiers printed stack contents the program never meant to disclose** — and among the things on the stack are saved registers, pointers into libc, and the **stack canary**. This is a **memory-disclosure** bug, and L28 §4–§5 and L29 §4 all said the same thing: **a leak defeats the canary and defeats ASLR.**

**`%n` is worse still** — it *writes* the number of bytes printed so far to a pointer argument, turning a format string into an arbitrary memory *write*.

**The bug is trivial and the fix is trivial:** the format string must be a literal you control, never data. **And the compiler tells you:**

```
$ gcc -Wformat-security -c prog.c
warning: format not a string literal and no format arguments [-Wformat-security]
```

*(Verified.)* **This warning is on in `-Wall`.** A format-string vulnerability in shipped code means a warning was ignored.

---

## 4. Use-After-Free and the Heap

The heap has its own family of bugs, and they are harder to see than a stack overflow because the corruption and the crash can be far apart in time.

| Bug | What happens |
|---|---|
| **Use-after-free** | Memory is used after `free`. The allocator may have handed that block to someone else — so a read leaks their data and a write corrupts it |
| **Double-free** | `free` called twice corrupts the allocator's own bookkeeping, which lives *in* the freed blocks |
| **Heap overflow** | Writing past a heap allocation overwrites the *metadata* of the next block — sizes and free-list pointers the allocator trusts |

**The theme is that the allocator's control data lives in the same memory as your data.** A heap overflow does not overwrite a return address; it overwrites the allocator's idea of how big the next block is, and the exploit unfolds on the *next* allocation. **This decoupling of cause and effect is what makes heap bugs hard to debug and valuable to attack.**

**The tools:** `-fsanitize=address` (AddressSanitizer) catches use-after-free, double-free and heap overflow at the moment they happen, with both the allocation and the misuse stack traces. **It is the single most effective thing you can do**, and it costs about 2× runtime — free in testing.

---

## 5. Data Races Are a Security Bug

Week 5 and PROG 201's concurrency material has a security face. A **time-of-check-to-time-of-use** (TOCTOU) race:

```c
if (access(path, W_OK) == 0) {     /* check: may I write it? */
    /* attacker swaps `path` for a symlink to /etc/passwd here */
    fd = open(path, O_WRONLY);     /* use: opens the swapped target */
}
```

**Between the check and the use, the world changed.** The permission check passed for one file and the open acted on another. **Any security decision followed by an action on the same named resource is a potential TOCTOU**, and the fix is to make check-and-use atomic — here, `open` first and check the *descriptor*, not the path.

---

## 6. The Security Mindset

The specific bugs matter less than the habit of thought behind them. Three principles:

**Trust no input.** Every byte from outside the program — arguments, files, the network from Week 8, the environment — is chosen by an adversary until proven otherwise. **A length field is a claim, not a fact. A format string is code. A filename can change under you.**

**Think about what the code *can* do, not what it is *meant* to do.** `strcpy` is meant to copy a string; it *can* write past a buffer. `printf(user)` is meant to print; it *can* read the stack. **The attacker reads the second column.**

**Defence in depth.** No single mitigation is sufficient — L29's ladder proves it — so systems layer canaries, NX, ASLR, CFI and sanitizers, and assume each will sometimes fail. **The goal is not to make attack impossible but to make it require defeating several independent mechanisms at once.**

> **This is why the course spent eight weeks on how the machine really works before this one.** You
> cannot reason about a buffer overflow without the stack frame (Week 3), about ROP without the
> instruction set (Week 2) and virtual memory (Week 6), about a format-string leak without knowing
> what is on the stack, or about ASLR without page tables. **Security is not a topic bolted on at the
> end; it is what the whole machine looks like to someone who wants to misuse it.**

---

## 7. What to Take Away

1. **The valuable bugs are often not on the stack** — integer arithmetic, format strings, the heap.
2. **`malloc(a * b)` can wrap to a tiny buffer.** Use `calloc` or a checked multiply.
3. **`printf(user)` reads the stack** via `%p` and writes it via `%n`. The format string must be a literal.
4. **The compiler warns** about format bugs — `-Wformat-security`, on in `-Wall`.
5. **Heap bugs corrupt allocator metadata**, decoupling cause from crash. AddressSanitizer finds them.
6. **A TOCTOU race is a security bug.** Make check-and-use atomic.
7. **Trust no input; read what code *can* do; layer defenses.**

---

## Exercises

1. `size_t bytes = count * size` wraps to a small value. Rewrite it with `__builtin_mul_overflow` so the allocation is refused, and say what `calloc` does internally.
2. `printf(user)` with `user = "%p %p %p"` prints three stack words. Explain where `printf` gets those "arguments" from, using the calling convention from Week 3.
3. Why is a memory-*disclosure* bug (a leak) as valuable to an attacker as a memory-*corruption* bug? Connect to L28 §5 and L29 §4.
4. `%n` writes to memory. Given a format string and a controlled pointer on the stack, sketch how it becomes an arbitrary write.
5. A use-after-free crashes "randomly", far from the free. Explain why, in terms of what the allocator does with a freed block.
6. Give a TOCTOU race other than the `access`/`open` example, and make it atomic.
7. Name, for each of the three attacks in this lecture, the earlier week whose material it reuses.

---

*Next week: multi-core and the GPU — and Midterm 2, covering Weeks 5–9.*
