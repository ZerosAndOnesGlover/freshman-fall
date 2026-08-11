# CS 201 · Computer Organization & Architecture
## Course Retrospective
### Read this **after** the final exam

---

> **This is not revision.** If the exam has not happened, close it — the revision guide in this folder
> is where your time should go.
>
> **Afterwards, it is worth fifteen minutes.**

---

## 1. What You Actually Learned

**Twelve weeks, and at no point did anything appear that did not rest on something earlier.**

| week | you learned to | out of |
|---|---|---|
| 0 | see the machine under the code | nothing |
| 1 | distrust the numbers | bits |
| 2 | read what the compiler emits | the ISA |
| 3 | trace a function call | the stack |
| 4 | explain why memory is slow | the cache |
| 5 | explain how it goes fast | the pipeline |
| 6 | see the addresses aren't real | page tables |
| 7 | reach the bottom of the ladder | storage |
| 8 | cross the ocean | the network |
| 9 | **attack the whole thing** | Weeks 2, 3, 6 |
| 10 | make many cores cooperate | the cache line |
| 11 | **make it faster on purpose** | all of it |
| 12 | see where the field is going | the general machine |

**Read the "out of" column.** Weeks 9 and 11 were built out of *the whole course* — which is why they came late, and why they were the two weeks where everything had to be understood at once. **You could not have done them in Week 3.** That you could do them by Week 11 is the measure of what the course was.

---

## 2. The Numbers You Measured, Not Memorised

Every headline result in this course was a number you produced on a real machine and checked against a model. **That is the difference between knowing and being told:**

- 0.1 + 0.2 ≠ 0.3, and the absorption index was $2^{21}$ **by derivation and by measurement.**
- The cache cliffs at 32 KiB / 256 KiB / 6 MiB — found with a stopwatch, matching `lscpu`.
- 30× from swapping two loop lines; 7.45× from swapping two loop indices.
- `malloc(512 MiB)` cost 136 KiB; 131 071 faults for 131 072 pages.
- `fsync` at 645× a write; the page cache at 63× the device.
- An internet round trip at 187 ms — 600 million cycles.
- A shared counter that got *slower* on two cores; false sharing at 1.45×.
- A benchmark that reported 0.0000 s because the loop was deleted.

**You will forget the exact figures. You will not forget that you measured them** — and that several of your first attempts measured nothing, until you made them honest.

---

## 3. The Reflex That Is the Real Product

The course had one habit underneath all the content, and it is the thing worth keeping:

> **When you want to know what the machine does, you look. You do not guess.**

`objdump` for the instructions. `gdb` for the stack. `perf`, `strace`, `/proc`, cachegrind for the behaviour. A stopwatch and a model for the truth. **Every "verified" in these notes was one small exercise of that reflex**, and it is what separates an engineer who reasons about performance from one who superstitions about it.

You were reliably wrong about where the time went, which fix would help, and what your benchmark measured. **Knowing that — and knowing to check — is not a weakness the course exposed. It is the professionalism the course built.**

---

## 4. What Was Left Out, and Honestly So

No course fits in twelve weeks, and this one made deliberate omissions you should know about:

- **`perf` was unavailable** on the lab machines, so you used gprof and cachegrind. On a machine you own, learn `perf` — it is the industry tool.
- **No GPU and one NUMA node**, so Weeks 10 and 12's GPU and NUMA material were conceptual with cited figures. **You can read a GPU reduction; you have not run one.** CS 331 will change that.
- **Out-of-order execution, superscalar issue, and real DRAM timing** were sketched, not modelled. ECE 311 is where they become the subject.
- **The formal memory model** — acquire/release, the C11 orderings — was named but not developed. CS 211 and PROG 202 do it properly.

**None of these gaps was hidden.** Knowing the boundary of what you were taught is part of being taught well.

---

## 5. Where It Goes

You are, as Year 2 keeps saying, learning to think in systems. **CS 201 was the layer everything else stands on**, and the courses that assume it are specific: CS 202 implements it, ECE 311 builds the hardware, CS 341 attacks it, CS 302 extends the network, CS 321 the storage, CS 331 the GPU, MATH 341 the floating point. **You will meet this course again, from the inside, in almost everything ahead.**

---

## 6. The Last Word

Week 0 promised that understanding what the computer actually does would make you a fundamentally better programmer in every language. That was not a slogan. It was the specific set of things you can now do — read the disassembly, find the bottleneck, write code that is not trivially exploitable, distrust a benchmark, and see the specialised machines as answers to a question you understand.

**The machine is no longer a mystery to you.** You know the layers, the costs, and the reflex to look when you are unsure. That knowledge does not belong to one language or one job. It is the ground the whole field stands on, and it is yours.

Now go build something fast.

---

*CS 201 · Course Retrospective · read after the final*
