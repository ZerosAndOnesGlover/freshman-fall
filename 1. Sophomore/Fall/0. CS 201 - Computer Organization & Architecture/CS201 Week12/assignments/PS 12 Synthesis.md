# CS 201 · Problem Set 12
## Synthesis — Domain-Specific Architectures and the Whole Machine

---

**Released:** Week 12, Wednesday · **Due:** Week 12, Friday 17:00 *(last teaching week)*
**Total: 100 points** · Submit one PDF, `PS12_{LastName}_{StudentID}.pdf`

> **The final problem set is synthesis, not new mechanics.** It asks you to connect the frontiers to
> the machine you now understand, and to trace the whole course through one program. **Project 2 is
> due the same day — this set is deliberately short.**

---

### Q1: RISC-V and CISC (16 points)

**(a) [4]** The loop `for(i) s += a[i]` compiles on x86-64 to a body containing `add eax, DWORD PTR [rdi]` — a single instruction that loads memory and adds. Write the equivalent RISC-V (two instructions), and explain what a RISC design forbids that forces the split.

**(b) [4]** RISC-V uses *more* instructions for the same work and considers this a good trade. Give three reasons, each connected to a specific earlier week (fixed-length decode, pipelining, hardware simplicity).

**(c) [4]** RISC-V's defining feature is being an **open** standard. Explain why that is an *architectural* advantage, not merely a licensing one — what did it enable that a proprietary ISA cannot?

**(d) [4]** x86-64 is "CISC on the outside, RISC on the inside" (Week 3 §L03). Reconcile this with RISC-V's bet: if modern x86 chips already translate to RISC-like micro-ops, why build a RISC ISA at all?

---

### Q2: Domain-Specific Architectures (20 points)

**(a) [6]** Place CPU, GPU, TPU, FPGA and ASIC on the **generality-vs-efficiency** axis. For each, give one workload for which it is the right choice, and state what it spends its transistors on.

**(b) [5]** A TPU discards the large caches and branch predictors a CPU spends heavily on. **Which specific Week-4 and Week-5 features is it throwing away, and why can it?** What property of neural-network computation makes those features useless?

**(c) [4]** The TPU is cited at 15–30× the performance-per-watt of a contemporary GPU on inference. Explain, in terms of the generality-efficiency trade, how it achieves that without being "cleverer".

**(d) [5]** "The architecture reflects the workload" is offered as the whole frontier in one sentence. Defend or challenge it, using **two** of the specialised machines and **one** general principle from Week 0.

---

### Q3: Two Different Machines (14 points)

**(a) [5]** A quantum computer is described as "not faster, but different". Name a problem it can help with and one it cannot, and state the property that distinguishes the two classes. Why is it not simply "a faster CPU"?

**(b) [5]** Neuromorphic chips co-locate compute and memory. **Which bottleneck from Weeks 0 and 4 does that attack?** Explain why co-location helps, and why it helps only certain workloads.

**(c) [4]** Both quantum and neuromorphic are described as "decades out" and "honest bets". What would have to be true — about the workload or the engineering — for each to become mainstream, and why is that uncertain?

---

### Q4: The Whole Machine (30 points)

Consider this function (the synthesis example from L38):

```c
int handle_request(int sock) {
    char buf[256];
    int fd = open("data.txt", O_RDONLY);
    ssize_t n = read(fd, buf, sizeof buf);
    long total = parse_and_sum(buf, n);
    char out[64];
    snprintf(out, sizeof out, "%ld\n", total);
    send(sock, out, strlen(out), 0);
    close(fd);
    return 0;
}
```

**(a) [12]** For **each** of the six numbered operations, name the week(s) of the course it touches and state, in one sentence, what the machine is actually doing. (Twelve sentences total; two per line where two weeks apply.)

**(b) [6]** `snprintf` is used, not `sprintf`. Explain the security significance in terms of the stack frame (Week 3) and Week 9, and what an attacker could do with the `sprintf` version.

**(c) [6]** Order the six operations by their likely **latency**, using the course's ladder, and identify which single operation probably dominates the whole function's runtime. Justify with numbers.

**(d) [6]** Suppose profiling shows `parse_and_sum` is 80% of the CPU time (excluding I/O waits). Apply the Week-11 method: what would you measure next, what are the two things it might be bound by, and what is the Amdahl ceiling on optimising it?

---

### Q5: What You Keep (20 points)

**(a) [6]** The course's latency ladder spans nine orders of magnitude. State the **ratios** (not the absolute numbers) between: L1 and DRAM; DRAM and an SSD read; an SSD read and an internet round trip. Explain why the ratios are more worth remembering than the numbers.

**(b) [6]** Five ideas recurred across the course (L38 §4). State three of them, and for each give **two** distinct weeks where it appeared.

**(c) [4]** "The compiler runs equivalent code, not your code." Give two specific instances from the course where this mattered, and state the general consequence for how you answer "what does the machine do?".

**(d) [4]** The course argues two things will not change: the speed of light, and that data movement costs more than computation. **Pick one** and argue why it is permanent, and what it implies for how you will design systems throughout your career.

---

## Marks

| | |
|---|---:|
| Q1 RISC-V and CISC | 16 |
| Q2 Domain-Specific Architectures | 20 |
| Q3 Two Different Machines | 14 |
| Q4 The Whole Machine | 30 |
| Q5 What You Keep | 20 |
| **Total** | **100** |

---

*CS 201 · Week 12 · Problem Set 12 — the last*
