# CS 201 · Lab 9 — Solutions and TA Notes
## Instructor Only

---

> **Unmarked.** Five checkpoints. All figures verified on the lab image. **This is a defensive lab —
> keep the framing throughout: understand the mitigation, then write code that does not need it.**

---

## Before the Session — the Framing Matters

**Open by saying what the lab is and is not.** It is: understanding how the machine's defenses work so you trust them and write safe code. It is not: a how-to for attacking anything. **Every binary is one the student compiled in this directory with defenses toggled to study them.**

**The genuine payoff is Part 4** — the sanitizer that finds the bug before it ships. Parts 1–3 explain the runtime defenses for code you cannot fix; **Part 4 is the one that changes how they write C.** If the session runs short, protect Part 4.

**On ASLR:** the machine has `randomize_va_space = 2` *(verified)*. Students who see identical addresses have probably run under `setarch -R` or a container that disabled it — check.

---

## Timing

| Part | Budget | Reality |
|---|---|---|
| 1 — the canary | 20 min | 15 min |
| 2 — the overwrite (GDB) | 25 min | 25 min |
| 3 — NX and ASLR | 20 min | 15 min |
| 4 — **the sanitizer** | 30 min | **Protect this** |
| 5 — format string | 15 min | 15 min |

---

## Part 1

The four instructions are in the handout and verified. **Answers:**

1. **`fs:0x28` is thread-local storage** — not reachable through a stack overflow and randomised per process, so the attacker cannot read or reproduce it. A local variable would be overwritten by the same overflow.
2. **Just below the return address**, so that any overflow reaching the return address must first cross the canary. Placing it at the bottom of the frame would let an overflow of the buffers-above-it corrupt the return address without touching it.
3. **The epilogue found the canary changed** — the overflow wrote through its slot en route to the return address — so `__stack_chk_fail` aborted. *(Verified: `*** stack smashing detected ***`.)*

**✅ CHECKPOINT 1**

---

## Part 2

*(Verified: with `-fno-stack-protector`, 24 bytes of padding then 8 bytes lands on the return-address slot; GDB shows it become the injected value.)*

**Answers:**

1. `buf` at `rbp-0x10`: 16 (buf) + 8 (saved rbp) = **24** to the return address. Draw checked.
2. **`strcpy` stops at the first zero byte.** Real addresses are mostly high with leading zero bytes, so a `strcpy`-based overflow cannot place them — a genuine constraint that shapes real exploits (and why `read`/`memcpy`-based bugs are more useful to attackers than `strcpy` ones).
3. **The ABI's 16-byte stack alignment (Week 3 §L12).** After `ret` lands on the target, `rsp` is misaligned, and the target's first `movaps` faults. **This is why "the return address changed" and "the exploit works" are very different achievements** — and it is worth connecting explicitly to the segfault they saw in Week 3.

> **Keep this in GDB.** The null-byte problem in (2) is the reason, and it teaches itself when a
> command-line payload silently truncates.

**✅ CHECKPOINT 2**

---

## Part 3

**3.1** `GNU_STACK RW` *(verified)*. The missing `E` prevents **stack code injection**; the attacker's response is **code reuse / ROP** (L29).

**3.2** *(Verified: five distinct addresses; `setarch -R` gives identical ones.)*

1. **ASLR denies the attacker usable addresses. It does not fix the bug.**
2. **The low 12 bits are the page offset** — a page cannot be relocated within itself (Week 6).
3. **Everything in libc moves together**, so one leaked libc address reveals the base and hence every gadget. This is why disclosure bugs are worth so much (L29 §4).

**✅ CHECKPOINT 3**

---

## Part 4 — the important part

### 4.1

*(Verified.)* ASan reports:

```
ERROR: AddressSanitizer: stack-buffer-overflow
WRITE of size 41 ...
  #1 ... in vuln vuln.c:3
  [32, 48) 'buf' (line 3) <== Memory access at offset 48 overflows this variable
```

**It names the buffer, the line and the overflowing offset.** Make the contrast with Part 1 explicit: the canary tells you *at runtime, in production, that something already went wrong*; ASan tells you *in testing, exactly where the bug is*, before anyone ships it.

### 4.2

*(Verified.)* `heap-use-after-free`, reporting **both** the free site and the use site — the two events a heap bug separates in time and space, which is exactly what makes heap bugs hard without the tool.

### 4.3

*(Verified: `bytes = 0`; `malloc` returns a tiny pointer; `calloc` returns NULL.)*

**Answers:**

1. **~2× is a bargain in testing** — you run the suite once and find bugs that would cost far more in production — **and unacceptable in production** because every user pays the 2× forever, and the red-zone memory overhead is large. **Ship without ASan; test with it.**
2. **The canary is a runtime tripwire with no location; ASan is a testing tool with exact location.** The canary protects the shipped binary against an overflow you missed; ASan stops you missing it. **You want both — different jobs.**
3. `int *make_array(size_t n){ size_t b; if(__builtin_mul_overflow(n,sizeof(int),&b)) return NULL; return calloc(n,sizeof(int)); }` *(verified — refuses at `n = 2^62`, works at `n = 8`)*.

> **This is the checkpoint that should change behaviour.** End it by having every student add
> `-fsanitize=address,undefined -Wall -Wextra` to their Project 1 build and re-run their tests.
> Several will find something.

**✅ CHECKPOINT 4**

---

## Part 5

*(Verified: the `bad` path leaks stack words via `%p`; `good` prints literally; `-Wformat-security` warns, and the warning is in `-Wall`.)*

**Answers:**

1. **`printf` reads its "arguments" from where the calling convention says they are** (Week 3) — the argument registers first, then the stack. With no real arguments passed, `%p` consumes whatever is in `rsi`, `rdx`, … and then the stack, disclosing it.
2. **The leaked words can include the canary and libc pointers** — so a "read-only" bug defeats both the canary and ASLR, enabling the corruption bug that follows. Disclosure and corruption are complementary.
3. **`%n` turns it into an arbitrary memory write.**
4. **A shipped format-string bug means a warning was ignored** — so `-Wall -Werror` (warnings as errors) would have made the vulnerability un-shippable. **Turn warnings into build failures.**

**✅ CHECKPOINT 5**

---

## What Success Looks Like

1. Recognise the canary in a disassembly and explain why it is read from `fs:0x28`.
2. Explain, having watched it, why a changed return address is not a working exploit.
3. State what NX and ASLR each deny an attacker, and that neither fixes the bug.
4. **Compile with `-fsanitize=address,undefined` and read its report to the bug.**
5. **Turn on `-Wall -Werror` and understand that a shipped format-string bug is an ignored warning.**

Items 4 and 5 are the ones that make them better engineers rather than better-informed victims.

---

*CS 201 · Week 9 · Lab 9 Solutions · Instructor Only*
