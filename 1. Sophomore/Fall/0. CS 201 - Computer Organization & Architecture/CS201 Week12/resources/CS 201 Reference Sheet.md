# CS 201 · Reference Sheet
## The whole course on one page

> Everything worth keeping, in one place. **The numbers are from this machine (i5-8250U) and change
> per generation; the ratios and the methods do not.**

---

## The Latency Ladder — the single most useful artefact

| Event | Time | ≈ cycles @3.2 GHz | Ratio to L1 |
|---|---:|---:|---:|
| L1 cache hit | 1.2 ns | 4 | 1× |
| L2 hit | 3.4 ns | 12 | 3× |
| L3 hit | 12 ns | 41 | 10× |
| DRAM access | 137 ns | 438 | **~100×** |
| Minor page fault | 1.9 μs | 6 200 | 1 500× |
| Page-cache hit | 2.5 μs | 8 000 | 2 000× |
| TCP loopback RTT | 18.6 μs | 60 000 | 15 000× |
| SSD 4 KiB read | 157 μs | 500 000 | **~130 000×** |
| `fsync` | 3.9 ms | 12.5 M | 3 M× |
| Internet RTT | 187 ms | 600 M | **~10⁸×** |

**Every performance question is "which row?"**

---

## Formulas

| | |
|---|---|
| **Amdahl's Law** | $S = \dfrac{1}{(1-p) + p/s}$;  max = $\dfrac{1}{1-p}$ |
| **Cache capacity** | $S \times E \times B$ (sets × ways × line bytes) |
| **Address split** | offset $= \log_2 B$; index $= \log_2 S$; tag = rest |
| **Same-set stride** | $S \times B$ bytes |
| **Page-table index** | $\log_2(\text{page}/\text{entry}) = \log_2(4096/8) = 9$ bits |
| **TLB reach** | entries × page size |
| **Arithmetic intensity** | flops / bytes moved |
| **Little's Law** | concurrency = throughput × latency |
| **Rotational latency** | $\tfrac12 \times 60/\text{rpm}$ |

---

## x86-64 quick reference

**Argument registers:** `rdi rsi rdx rcx r8 r9`, then the stack. Return in `rax`.
**Caller-saved:** `rax rcx rdx rsi rdi r8–r11`. **Callee-saved:** `rbx rbp r12–r15 rsp`.
**Alignment:** `rsp` ≡ 0 (mod 16) before `call`, ≡ 8 on entry; **each push flips parity**.
**Frame:** from a `buf[N]` at `rbp-X`, the return address is $X+8$ bytes away.
**32-bit write zeroes the upper 32; 8/16-bit writes do not.**
**`cmp`/`test` write no register** — only flags (ZF SF CF OF).
**Signed jumps** `jl jle jg jge`; **unsigned** `jb jbe ja jae`.
**`lea` computes, does not load.**

**Addressing:** `[base + index×scale + disp]`, scale ∈ {1,2,4,8}.

---

## IEEE 754 (single)

`1 sign | 8 exponent (bias 127) | 23 mantissa`, implicit leading 1 → **24 bits precision**.
$e=0$: zero (mantissa 0) or denormal. $e=255$: ±∞ (mantissa 0) or NaN.
**`float` stops counting at $2^{24}$; `double` at $2^{53}$.** Addition is **not associative**.

---

## The cache miss triad

| Miss | Cause | Fix |
|---|---|---|
| Compulsory | first touch | none (prefetch to hide) |
| Capacity | working set > cache | **blocking** |
| Conflict | too many hot lines → one set | **padding** / stride change |

**Optimise the level that is missing** — D1 miss served by L2 (~12 cyc) vs DRAM (~438) are 36× apart and counted the same.

---

## The roofline

**Compute-bound** (flat roof): reduce flops / vectorise. **Memory-bound** (slanted roof): reduce bytes moved / improve locality. **The ridge** is where they meet. Vector add ≈ 0.04 flop/byte (memory-bound); matmul ~ $n/12$ (compute-bound for large $n$).

---

## Multi-core

**MESI:** M/E writable, S needs invalidate, I needs fetch. **A shared write is a broadcast.**
**False sharing:** the 64-byte line, not the variable, is the unit — pad to `alignas(64)`.
**Coherence ≠ consistency.** x86 = TSO (permits store-load reordering).
**Physical cores, not threads, deliver compute throughput.**

---

## Security

**Overflow** ← unbounded copy. **Canary** (`fs:0x28`) detects it. **NX** (`RW` stack) stops injection → **ROP** reuses code → **CFI/CET** (compiled ≠ enforced). **ASLR** hides addresses; a leak defeats it. **`malloc(a*b)`** overflows → `calloc`/`__builtin_mul_overflow`. **`printf(user)`** leaks (`%p`) and writes (`%n`). **Fix in testing: `-Wall -Werror -fsanitize=address,undefined`.**

---

## The method (Week 11)

**Measure → Profile → Diagnose → Bound → Fix → Re-measure.** Never skip diagnose (which resource?) or bound (Amdahl — is it worth it?).

**Benchmark checklist:** Did the compiler delete it? Is the result consumed? Which layer? Did it exercise the effect? Is the bottleneck what I changed? Warm-up + repeats + variance? **Does it match a model?**

---

## The six recurring ideas

1. **Data movement is the bottleneck, not computation.**
2. **A fixed per-operation cost makes operation size dominant.**
3. **The compiler runs equivalent code, not your code.**
4. **Know your bottleneck before you act.**
5. **Every abstraction is a contract with a cost.**
6. **A benchmark is wrong until it survives the checklist.**

---

## The tools

| Question | Tool |
|---|---|
| What instructions? | `objdump -d -M intel` |
| What's on the stack? | `gdb`: `x/gx $rbp+8`, `info frame` |
| Which cache level? | `valgrind --tool=cachegrind` |
| Where's the time? | `gprof` / `perf` / `callgrind` |
| Address space, faults? | `/proc/PID/maps`, `/proc/PID/statm`, `getrusage` |
| Sockets, syscalls? | `ss`, `strace` |
| Storage, device vs cache? | `O_DIRECT`, `lsblk`, `fsync` |
| Cache/CPU geometry? | `lscpu -C`, `getconf PAGESIZE` |

---

*CS 201 · Reference Sheet · Weeks 0–12*
