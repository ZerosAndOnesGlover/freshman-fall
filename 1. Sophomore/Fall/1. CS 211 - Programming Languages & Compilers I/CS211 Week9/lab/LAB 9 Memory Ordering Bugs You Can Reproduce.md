# CS 211 · Lab 9
## Memory Ordering Bugs You Can Reproduce

**Friday of Week 9 · 14:00–15:50 · BH 220 · covers Week 9**
**Unmarked and mandatory.** The TA checks you off in the session. [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] costs you a letter grade after a second unexcused absence.

**Bring:** a terminal. Everything is in this folder.

> **The syllabus asks for memory-ordering bugs on a *weakly-ordered* processor. BH 220 does not
> have one** — every machine here is x86-64. Part D is about what that costs you and what to do
> instead, and the gap is not a workaround: **the reorderings you cannot see here are exactly the
> ones that break code when it moves to ARM.**

---

## Setup

```bash
cd "CS211 Week9/lab"
gcc -O2 -pthread -o litmus litmus.c && ./litmus 200000
gcc -O2 -pthread -o orders orders.c
javac Hoist.java
```

If any of those fail, get the TA now rather than at 15:30.

---

## Part A — The Impossible Outcome (25 min)

**Q1.** Before running anything, look at the two threads in `litmus.c`:

```
Thread 0:  x = 1;  r1 = y;
Thread 1:  y = 1;  r2 = x;
```

**On paper**, enumerate the interleavings and convince yourself that `r1 == 0 && r2 == 0` is impossible under sequential consistency. Write the argument in one sentence.

**Q2.** Now run it:

```bash
./litmus 200000
```

- Report all four counts.
- **How many times did the impossible outcome occur?**
- Run it twice more. Is the count stable?

**Q3.** Compute the rate as a percentage. Then answer: **how many test runs would you expect to need before seeing this once?** Say what that implies about catching this defect by testing.

**Q4.** Now add the barrier:

```bash
./litmus 500000 fence
```

- Report the forbidden count. Run three times.
- Find the fence in the source. What does `atomic_thread_fence(memory_order_seq_cst)` compile to?
  ```bash
  gcc -O2 -pthread -S -o - litmus.c | grep -A2 -B2 "mfence\|lock"
  ```
- Explain what that instruction does to the store buffer.

**Q5.** `litmus.c` puts `x` and `y` on separate cache lines.

- **Predict first, and write it down:** removing the padding will make the forbidden outcome *more* or *less* frequent?
- Now do it:
  ```bash
  sed 's/^#define PAD _Alignas(64)/#define PAD/' litmus.c > nopad.c
  gcc -O2 -pthread -o nopad nopad.c && ./nopad 500000
  ```
- **The change is about two orders of magnitude, and most people predict the direction wrongly.** Report both numbers and work out the mechanism: what happens to the shared line, and what does that do to how long the *load* takes?

---

## Part B — The Compiler Did It (30 min)

**Q6.** Three builds of one file:

```bash
gcc -O0 -pthread -o hoist_O0 hoist.c ; timeout 5 ./hoist_O0 ; echo "exit $?"
gcc -O2 -pthread -o hoist_O2 hoist.c ; timeout 5 ./hoist_O2 ; echo "exit $?"
gcc -O2 -pthread -DATOMIC -o hoist_at hoist.c ; timeout 5 ./hoist_at ; echo "exit $?"
```

Report all three. **One of them never finishes.**

**Q7.** Find out why:

```bash
gcc -O2 -pthread -S -o - hoist.c | sed -n '/^reader:/,/^\.LFE/p'
```

- Quote the two instructions that make the loop infinite.
- Now the atomic version:
  ```bash
  gcc -O2 -pthread -DATOMIC -S -o - hoist.c | sed -n '/^reader:/,/^\.LFE/p'
  ```
- **What is the single difference?** State it in terms of where the load is.

**Q8.** **Name the Week 5 optimisation that did this.**

Then answer the harder question: **is this a bug in that optimisation?** Argue it either way, but engage with what the compiler is entitled to assume.

**Q9.** Now `orders.c`, which counts to four million:

```bash
gcc -O2 -pthread -o orders orders.c   && ./orders 4 1000000
gcc -O0 -pthread -o orders_O0 orders.c && ./orders_O0 4 1000000
./orders_O0 4 1000000
```

- The `plain` row is a data race. At `-O2` it gives the **right** answer in **0.000 s**. At `-O0` it loses a large fraction. Report all three runs.
- Find out what `-O2` did:
  ```bash
  gcc -O2 -pthread -S -o - orders.c | sed -n '/^w_plain:/,/ret/p'
  ```
- **The million-iteration loop became one instruction. Quote it.**
- In one sentence: what licensed that?

**Q10.** *(Discussion — out loud with your neighbour.)*

You are debugging a concurrency bug. You build with `-O0` to get better debug info, and the bug appears. Your colleague builds with `-O2` and it does not.

**Who has the bug?** What should you actually conclude, and what should you do next?

---

## Part C — Java, and the Actor Alternative (25 min)

**Q11.** Same bug, memory-safe language:

```bash
java Hoist plain
java Hoist volatile
```

- Report both.
- Open `Hoist.java` and find the `Thread.sleep(300)`. **Change it to 5 and re-run `plain`.** What happens?
- **Explain the difference.** Your answer must mention the JIT.
- What does that imply about a test suite that runs quickly?

**Q12.** C's `volatile` and Java's `volatile` are different keywords with the same spelling.

```bash
sed 's/^static int ready;/static volatile int ready;/' hoist.c > hoist_vol.c
gcc -O2 -pthread -o hoist_vol hoist_vol.c ; timeout 5 ./hoist_vol ; echo "exit $?"
```

- Does it terminate?
- **Does that make the program correct?** These are different questions. Answer both, and say what the C standard actually promises about `volatile` and other threads.

**Q13.** Take the shared state away:

```bash
python3 actors.py 4 20000
```

- Report the three rows.
- The actor version is the slowest. **Find `Counter.on` in the source and say what you are buying.**
- The `shared, no lock` row got the **right answer**. The same algorithm in C lost 44–63% of its increments (Q9). **Why the difference?**
  ```bash
  python3 -c "import sys; print(sys._is_gil_enabled())"
  ```

**Q14.** `actors.py` claims the locking "has not gone away — it has been moved into the mailbox."

**Find the lock.** Then decide whether the claim is fair, and be ready to defend your answer.

---

## Part D — The Machines We Do Not Have (20 min)

**Q15.** Fill in this table from L19 §4:

| reordering | x86-TSO | ARM / POWER |
|---|---|---|
| LoadLoad | | |
| LoadStore | | |
| StoreStore | | |
| StoreLoad | | |

**Q16.** The flag-and-payload handoff:

```c
payload = 42;      /* (1) */
ready = 1;         /* (2) */
```

- Which reordering would let a reader see `ready == 1` and `payload == 0`?
- **Is that possible on x86?** Is it possible on ARM?
- So: a program can be genuinely broken, pass every test on x86 forever, and fail on the first ARM build. **Say what you would do about that**, given that you cannot test on hardware you do not have.

**Q17.** Run the tool that does not need the hardware:

```bash
gcc -O0 -g -pthread -fsanitize=thread -o orders_tsan orders.c
setarch $(uname -m) -R ./orders_tsan 2 20000 2>&1 | head -20
```

**The `setarch $(uname -m) -R` is required on these machines** — without it TSan aborts with `unexpected memory mapping`. Try it without, so you have seen the failure.

- What does TSan report? Quote the file, line and variable.
- Run it on `hoist.c` too.
- Measure the slowdown: time `./orders_O0 4 300000` against the TSan build.

**Q18.** *(Discussion.)* TSan checks **happens-before**, not outcomes. Q3 established that testing cannot find this class of bug.

- Why can TSan find in one run what testing will not find in a year?
- **Name two earlier weeks** where the same move — checking the property instead of sampling the results — was the fix.
- What are TSan's limits? *(It reports races it observes. What does it not do?)*

---

## If You Finish Early

**Q19.** Modify `litmus.c` so that only **one** thread has a fence. Does the forbidden outcome return? What does that tell you about where barriers must go?

**Q20.** In `orders.c`, replace `memory_order_seq_cst` with `memory_order_relaxed` in the counter increment. Is the answer still correct? **Should it be?** Explain why a relaxed counter is one of the few legitimate uses of `relaxed`.

**Q21.** Write the smallest program you can where `relaxed` gives a wrong answer but `acq_rel` does not. *(Hint: you need a flag and a payload, not a counter.)* If you cannot make it fail on x86, say why — and name the architecture where it would.

**Q22.** Run `./litmus` while the machine is loaded (`stress-ng --cpu 8` or just several copies at once). Does the forbidden rate change? What does that suggest about reproducing concurrency bugs in CI versus on a developer laptop?

---

## Before You Leave

Show the TA:

1. Your Q2 forbidden count, and your Q3 estimate of how many test runs would be needed to see it once.
2. Your Q5 prediction — written *before* you ran it — and the actual numbers.
3. Your Q7 quote of the two instructions, and Q9's single instruction.
4. Your Q13 explanation of why the racy Python was right and the racy C was not.

---

*CS 211 · Week 9 · Lab 9 · © CSE Department*
