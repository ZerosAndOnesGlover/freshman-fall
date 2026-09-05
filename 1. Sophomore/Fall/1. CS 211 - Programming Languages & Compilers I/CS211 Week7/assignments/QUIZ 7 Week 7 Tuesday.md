# CS 211 · Quiz 7

**Sat:** Tuesday of **Week 7**, first 10 minutes of lecture · TH 205
**Covers:** **Week 6** — the heap, reference counting, tracing, root sets, generations, write barriers
**Unmarked.** Recorded in `5. Academic Registry/2. Gradebook/Year2 Sophomore/Fall/_CS 211 Lab and Quiz Record.md`.

**The answer key is printed below the questions.** Do not look at it until you have written something for all six.

> **Midterm 2 is next Tuesday and covers Weeks 4–7.** This quiz is the only one whose material is
> inside that exam and behind you. Treat a wrong answer here as a revision instruction.

---

## Questions

**1.** *(2 min)* A collector finds that an object's reference count is **zero**. What may it conclude?

Now the count is **three**. What may it conclude? Give a heap in which the second conclusion is wrong.

---

**2.** *(2 min)* Where does a tracing collector's **root set** come from?

Name the compiler analysis that produces it, the week you wrote it, and what it was originally for.

---

**3.** *(2 min)* Week 5's `store` instruction reads three variables: the array, the index, and the value. Week 4's `Instr.uses` reported only two of them.

In Week 5, that bug **deleted an instruction**. In Week 6, the same bug does something worse. **What, and why is it worse?**

---

**4.** *(1 min)* A generational collector never scans the old generation during a minor collection.

So what stops it freeing a young object that an old object points to? Name the mechanism and the set it maintains.

---

**5.** *(2 min)* You measure a program under two root policies. **Peak live memory is identical** under both, and one of them retains far more garbage.

Explain how both can be true, and name a measurement that *would* show the difference.

---

**6.** *(1 min)* `-Xlog:gc` reports ZGC's longest pause as **8 ms**. `-Xlog:safepoint` reports it as **115 µs** — seventy times smaller — on the same run of the same program.

Neither tool is broken. **What is the difference between the two numbers?**

---
---

## Answer Key

**1.** A count of **zero** proves the object is **unreachable**, so it is safe to free.

A count of **three** proves nothing. It proves three pointers exist; it does not prove that anything can reach them.

```
        a ---> [b] ---> b ---> [a] ---> a
```

Every object in that cycle has a positive count, held entirely by the other members. Drop every external pointer and all four counts stay positive, and none of the four is reachable from anywhere.

**Reference counting is sound and incomplete.** `cycle.cy leak 5` allocates 25 objects, frees 5, and leaks 20.

*Full credit requires the asymmetry stated correctly. "Three pointers point at it, so it is live" is the error the question is testing.*

---

**2.** From the **compiler**. The collector cannot compute it.

The analysis is **live-variable analysis**, from **Week 5**, written for **register allocation** — to decide when a register may be reused.

Both consumers ask the same question — *what does the future read?* — so the same backward, union dataflow analysis answers both. In a production runtime the emitted table is called a **stack map**.

*Accept "liveness". Do not accept "the runtime scans the stack" without qualification — a **conservative** collector does that, and L14 §5 is about what it costs.*

---

**3.** `uses` never inspects the **`dst`** slot, and `store` keeps the array there. So the array looks dead.

- **Week 5:** the instruction that computed the array is deleted. The program computes a wrong answer.
- **Week 6:** the array is not a root, so the collector **frees it** — and the next instruction writes through the pointer. That is a **use-after-free**.

**Why worse:** an imprecise analysis costs performance; an **unsound** one costs memory safety. A wrong answer is a bug; a use-after-free is an exploitable bug, in a language that was supposed to be memory-safe.

```
$ python3 runtime.py victim.cy victim --gc=mark --threshold=4 --roots=week4
; ---- CRASH ----
  #2 was freed, and the program still has a pointer to it
```

*The phase that consumes an analysis decides what a bug in it costs. The table did not change.*

---

**4.** A **write barrier** — a few instructions on every heap pointer write — which records old-to-young pointers in the **remembered set**. Minor collections treat that set as an additional source of roots.

*Bonus, not required:* there is one old-to-young pointer the barrier cannot catch, because no write creates it — **promotion** turns an existing young-to-young pointer into an old-to-young one. Handling it is `_promote`'s fix-up, and removing that fix-up freed 97 reachable objects while still printing the right answer.

---

**5.** Peak live is set by **whatever triggers a collection** — an object count or a heap size. A collector that retains garbage does not exceed that trigger; it just reaches it *sooner*. So retention shows up as **more frequent collections and more marking work**, never as a higher peak.

The measurement that shows it is **residency** — live bytes immediately *after* a collection — or equivalently the count of objects scanned.

```
roots=live   residency  16 B   17 collections    17 scanned
roots=scope  residency 216 B   22 collections   132 scanned
```

**Peak live was 504 bytes in both.**

*Anyone benchmarking a collector by peak RSS is measuring their own heap-sizing policy.*

---

**6.** `-Xlog:gc` reports the duration of a **collection cycle**. `-Xlog:safepoint` reports the **stop-the-world pauses**.

For Serial and Parallel those are the same thing. **ZGC is concurrent** — nearly all of its cycle runs alongside the program — so its cycle time says almost nothing about how long the application was stopped.

Reading the first number would make you choose G1, whose true worst pause (1637 µs) is **fourteen times longer** than ZGC's (115 µs).

*The general rule: measure the quantity you care about, not the one the tool prints by default — and when comparing tools, check the default means the same thing for each.*

---

## How You Did

**6 correct** — you are ready for Week 7, and for the Week 6 third of Midterm 2.
**4–5** — reread the section you missed **before Tuesday**, not after.
**0–3** — L13 and L14, properly, this week. **Midterm 2 is in seven days and Weeks 4–7 are all on it.**

**Question 2 is the one to check yourself on.** It is the connection the whole of Week 6 was built to make — that a garbage collector's correctness rests on a compiler analysis written five weeks earlier for an unrelated purpose — and it is the kind of link an exam asks about.

---

*CS 211 · Week 7 · Quiz 7 · © CSE Department*
