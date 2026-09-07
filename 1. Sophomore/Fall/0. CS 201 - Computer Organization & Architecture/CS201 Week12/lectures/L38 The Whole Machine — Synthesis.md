# CS 201 · Computer Organization & Architecture
## Week 12 · Lecture 2 of 3
### The Whole Machine — Synthesis

---

**Reading:** none — re-read your own [[CS201 Week12/summary|summary]] files · **Previous:** L37, frontiers

---

## 1. One Program, Every Week

Take the most ordinary thing imaginable — a web server reading a value from a file and sending it to a client — and watch every week of this course appear in it. **Nothing below is a stretch; each is literally what happens.**

```c
int handle_request(int sock) {
    char buf[256];
    int fd = open("data.txt", O_RDONLY);       // [7] storage, [6] file→pages
    ssize_t n = read(fd, buf, sizeof buf);      // [6] page cache, maybe [7] a fault
    long total = parse_and_sum(buf, n);         // [1] integers, [2] the compiled loop
    char out[64];
    snprintf(out, sizeof out, "%ld\n", total);  // [9] bounded — not sprintf
    send(sock, out, strlen(out), 0);            // [8] TCP, a round trip
    close(fd);
    return 0;
}
```

| Line | Week(s) | What the machine is doing |
|---|---|---|
| `char buf[256]` | 3, 9 | a stack frame; a bounds check that must not be missing |
| `open` | 6, 7 | a file becomes mappable pages; the device is 10⁵× slower than L1 |
| `read` | 6, 7 | page-cache hit (2.5 μs) or a fault to the SSD (157 μs) |
| `parse_and_sum` | 1, 2, 4, 5 | integer overflow risk; a compiled loop; cache misses; a dependency chain |
| `snprintf` not `sprintf` | 9 | the one-character difference between safe and exploitable |
| `send` | 8 | a byte stream, framed; a 187 ms round trip dwarfing everything above |
| all of it | 10, 11 | across cores it shares state; and you would *profile* before optimising |

**Twelve weeks, one function.** The course was never a list of topics — it was one machine, examined at twelve depths.

---

## 2. The Layers, Top to Bottom, Are the Course

Week 0 drew the abstraction hierarchy and promised the course would descend it. It did:

```
  high-level code        the web server above
     │  [1] what the numbers really are
     C                   the language you profiled
     │  [2] what it compiles to
  assembly / ISA         you can read it now
     │  [3] how a call works
  the stack + ABI        frames, ret, the calling convention
     │  [4-6] where the data lives
  memory hierarchy       caches, virtual memory, the TLB
     │  [7-8] the world outside the chip
  storage + network      the bottom of the latency ladder
     │  [5,10] how it goes fast
  pipeline + cores       ILP, coherence, the roofline
     │  [11] how you make it faster on purpose
  the method             measure, diagnose, bound, fix
     │  [9,12] what it all costs, and what's next
  security + frontiers
```

**Every arrow is a week, and every layer is a contract with costs** — Week 0's thesis, now something you can prove at each level rather than take on faith.

---

## 3. The Latency Ladder — the Course in One Table

Everything the course measured, on one machine, spanning **nine orders of magnitude:**

| Event | Time | Cycles @3.2 GHz | Week |
|---|---:|---:|---|
| L1 cache hit | 1.2 ns | 4 | 4 |
| L2 hit | 3.4 ns | 12 | 4 |
| L3 hit | 12 ns | 41 | 4 |
| DRAM access | 137 ns | 438 | 4 |
| Minor page fault | 1.9 μs | 6 200 | 6 |
| Page-cache hit | 2.5 μs | 8 000 | 7 |
| TCP loopback round trip | 18.6 μs | 60 000 | 8 |
| SSD 4 KiB read | 157 μs | 500 000 | 7 |
| `fsync` | 3.9 ms | 12 500 000 | 7 |
| LAN round trip | 2.4 ms | 7 700 000 | 8 |
| Internet round trip | 187 ms | 600 000 000 | 8 |

**If you internalise one artefact from this course, make it this table.** Every performance decision you will ever make is a question of *which row you are on* — and the whole of Week 11's method is finding out which row a program is actually spending its time in, then moving it up.

---

## 4. The Ideas That Recurred

The course looked like twelve subjects. It was really a handful of ideas, each appearing in disguise week after week:

**Data movement is the bottleneck, not computation.** Week 4's cache lines, Week 7's storage blocks, Week 8's message sizes, Week 10's bouncing cache line, Week 11's memory-bound matmul — **the same lesson five times.** The arithmetic was almost never the problem; getting the data to the arithmetic was.

**A fixed per-operation cost makes operation size the dominant variable.** Cache lines (64 B), storage blocks (18× from 4 KiB to 1 MiB), network messages (64 B → 64 KiB, 6.6 → 2436 MiB/s). Batching is not a micro-optimisation; it is *the* optimisation.

**The compiler runs equivalent code, not your code.** Week 0's deleted loop, Week 2's constant-folded division, Week 5's `cmov`, Week 11's inlined-away profile. "What does the machine do?" is answered by `objdump`, never by reading the C.

**Know your bottleneck before you act.** Week 4's "which cache level?", Week 5's compute-vs-memory, Week 7's "device or cache?", Week 11's roofline. Applying the right fix to the wrong bottleneck measures nothing — which the course demonstrated with null results five separate times.

**Every abstraction is a contract with a cost.** Week 0's thesis, and then: the ISA (Week 2), the calling convention (Week 3), virtual memory (Week 6), TCP (Week 8), the memory model (Week 10). The contracts are what let separately-built things interoperate; their costs are what you spend the rest of your career managing.

---

## 5. Why the Order Was the Order

The course was not arbitrary. **Each week was the prerequisite for the next**, and the security week (9) proved it: you could not understand a buffer overflow without the stack frame (3), ROP without the instruction set (2) and virtual memory (6), a format-string leak without knowing what is on the stack, or ASLR without page tables. **Security was where the whole machine had to be understood at once** — which is why it came late, and why it was so satisfying if the earlier weeks had landed.

**The frontiers week (12) is the same test from the other end:** you can only see why a TPU discards branch predictors and caches because you spent Weeks 4 and 5 learning what those cost and what they buy. **You understand the specialised machines because you understand the general one.**

---

## 6. What You Can Now Do

Not a list of facts — a set of capabilities that did not exist twelve weeks ago:

- **Read any function's disassembly** and say what the machine does with it.
- **Explain why one program is 30× faster than an algorithmically identical one**, and prove it with a profiler.
- **Look at a slow program and know where to look** — which layer, which bottleneck, which measurement.
- **Write code that is not trivially exploitable**, and know which defenses protect the code you cannot fix.
- **Distrust a benchmark** until it survives the checklist.
- **Read the specialised machines** — GPU, TPU, RISC-V — as answers to a question you now understand.

**This is what "a fundamentally better programmer in every language" meant in Week 0.** It was not a slogan; it was the specific set of things above, and you can do them now.

---

## 7. What to Take Away

1. **One ordinary function contains every week of the course.** It was always one machine.
2. **The abstraction hierarchy of Week 0 is the syllabus**, descended layer by layer.
3. **The latency ladder is the single most useful artefact** — nine orders of magnitude, and every performance question is "which row?".
4. **A handful of ideas recurred in disguise**: data movement dominates; operation size matters; the compiler runs equivalent code; know your bottleneck; abstractions cost.
5. **The order was necessary** — security and the frontiers both required the whole machine at once.
6. **You are a better programmer in every language now**, in the specific sense Week 0 promised.

---

## Exercises

1. Take a program you have written and annotate five lines with the week of this course each one touches.
2. From the latency ladder, how many L1 hits fit in one internet round trip? What does that ratio imply for how you design a networked program?
3. Give a *sixth* recurrence of "data movement is the bottleneck" from your own experience or reading, outside the examples in §4.
4. The course put security in Week 9, not Week 2. Argue why that ordering was necessary using two specific dependencies.
5. Pick one specialised machine from L37 and explain, using two specific earlier weeks, why you could not have understood it in Week 1.

---

*Next: L39 — the road ahead, and where this goes in Year 3.*
