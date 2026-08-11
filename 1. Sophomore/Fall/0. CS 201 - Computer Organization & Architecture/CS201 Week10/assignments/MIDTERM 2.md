# CS 201 · MIDTERM EXAMINATION 2
## Computer Organization & Architecture

---

**Week 10, Monday · 18:00–19:15 · VNC 100**
**Duration: 75 minutes · Total: 100 points · Weight: 12.5% of the course grade**
**Covers: Weeks 5–9** (pipelining and ILP, virtual memory, storage, networks, security)

---

**Name:** _________________________________ **Student ID:** ___________________

---

> **Permitted:** one handwritten sheet of A4, **one side only**. Student ID on the desk.
> **Not permitted:** calculators, electronic devices, printed material, the textbook.
>
> **Answer all five questions.** Show your working — a correct method with an arithmetic slip earns
> most of the marks; a bare number earns none. "Explain in one sentence" means one sentence.

---

## Q1 — Pipelining and Parallelism (20 points)

**(a) [4]** Distinguish **latency** from **throughput** for a pipeline. Does pipelining improve one, the other, or both?

**(b) [4]** Classify each as RAW, WAR or WAW, and state which is a *true* dependency and what removes the others:

```
mov rax, [rbx]      ; (1)
add rax, rcx        ; (2)
mov rbx, 5          ; (3)
```

**(c) [4]** Four independent accumulator chains summed the same values **4.00×** faster than one chain. Explain, in terms of latency-bound versus throughput-bound execution.

**(d) [4]** The same AVX2 loop measured **4.51×** at 16 KiB per array and **1.07×** at 16 MiB. Explain the difference in one or two sentences.

**(e) [4]** A routine is 40% of a program's runtime and you speed it up by 5×. Using Amdahl's Law, give the overall speedup. Show the arithmetic.

---

## Q2 — Virtual Memory (20 points)

**(a) [4]** Why is the x86-64 page-table index 9 bits? Derive it from the page size and entry size.

**(b) [4]** A load misses the TLB and the page-table pages are not cached. How many memory accesses does the single load take? Break them down.

**(c) [4]** 512 pointers occupying 32 KiB of L1-resident cache lines cost **1.24 ns** each spread over 8 pages and **27.57 ns** each over 8192 pages. The data never left L1. Explain what changed and name the structure responsible.

**(d) [4]** `malloc(512 MiB)` increased resident memory by 136 KiB. Explain, and state what makes the rest of the memory become resident later.

**(e) [4]** A child process writes one byte to each page of a 256 MiB region shared with its parent after `fork`, taking exactly 65 536 minor faults. Name the mechanism and the single PTE bit that implements it.

---

## Q3 — Storage (20 points)

**(a) [4]** Give the three components of a rotating-disk access. For a 4 KiB read, roughly what fraction is spent transferring data, and what does that imply about block sizes?

**(b) [4]** Flash cannot overwrite a page in place. State the rule, name the two units involved, and say what the FTL does instead.

**(c) [4]** Sequential SSD throughput rose from 113 MiB/s at 4 KiB to 2006 MiB/s at 1 MiB — an **18×** rise. What was limiting the small-block case? If the device were the limit, what would the curve look like?

**(d) [4]** Cached 4 KiB reads ran at 2.51 μs; `O_DIRECT` reads at 157.6 μs — **63×**. What is the only difference between the two?

**(e) [4]** A 4 KiB write costs 6 μs; the same write plus `fsync` costs 3876 μs. A database promises 10 000 durable transactions per second. Show why one `fsync` per transaction is impossible, and name the technique that keeps the promise.

---

## Q4 — Networks (20 points)

**(a) [4]** Name the four TCP/IP layers and one protocol at each. Give the total header overhead for a 1-byte payload over TCP/IP/Ethernet.

**(b) [4]** TCP is a byte stream. Two `send` calls of 100 bytes — give two ways the peer's `recv` might observe them, and state what a protocol must therefore do.

**(c) [4]** `TCP_NODELAY` changed one workload by 3% and another by **1350×**, the slow case measuring **41 ms** per round trip. What is 41 ms, and what two mechanisms deadlocked?

**(d) [4]** An HTTPS page load took 589 ms on a 187 ms link. Account for the time, and state how much was the server's own processing.

**(e) [4]** State **Little's Law**. A server on a 187 ms link must sustain 1000 requests/second. How many requests must be in flight, and what does that imply about a one-request-at-a-time server?

---

## Q5 — Security (20 points)

**(a) [4]** A `char buf[16]` sits at `rbp-0x10`. How many bytes of input reach the return address? Draw the frame.

**(b) [4]** The stack canary is read from `fs:0x28`, not an ordinary local. Give two reasons this matters for its security.

**(c) [4]** NX made the stack non-executable, defeating code injection. Name the attacker's response and explain why NX does not stop it. (libc has ~6000 `ret` instructions — why does that matter?)

**(d) [4]** `void *p = malloc(count * size)` with attacker-controlled `count`. Describe the vulnerability and give the fix.

**(e) [4]** A binary contains `endbr64` landing pads, so a colleague concludes CET is protecting it. Why is that conclusion unsafe, and how would you check whether the mitigation is actually enforced?

---

## Marks

| | |
|---|---:|
| Q1 Pipelining and Parallelism | 20 |
| Q2 Virtual Memory | 20 |
| Q3 Storage | 20 |
| Q4 Networks | 20 |
| Q5 Security | 20 |
| **Total** | **100** |

---

*CS 201 · Midterm Examination 2 · Weeks 5–9 · Year 2 Fall*
