# PROG 201 · Lab 10
## Fuzzing a Parser — Finding Bugs You Did Not Write a Test For
### Covers Week 10 · sat **Monday of Week 11**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 10 and is sat in Week 11.** Lab *N* is sat on the Monday of Week *N+1*.
>
> **PS 10 (the ROP exploit) is due this Friday.** It uses the sandbox described in the lectures;
> this lab does not — fuzzing needs no special privileges. **Marked Midterm 2 scripts came back in
> Week 9**; if yours raised questions, the TA has office hours before Friday.
>
> **Unmarked.** The TA checks your work off in the session.

**What you are building:** the loop that finds the bug before an attacker does.

You are given a small parser with three bugs planted in it. You will fuzz it, watch a coverage-guided fuzzer find its way past a magic-byte check that random input never would, and reproduce each crash under a sanitizer that points at the exact line. Then you will do the same to the heap and format-string bugs from the lectures, and see what they do **without** the sanitizer — which is nothing visible, which is why they ship.

---

## 0. Setup (5 minutes)

```bash
mkdir -p "$PROG201/week10/lab10"        # $PROG201 is set in ~/.bashrc -- see Lab 0
cd "$PROG201/week10/lab10"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week10/lab/"{parser.c,fuzz_parser.c,run_one.c,heap.c,fmt.c,Makefile} .

make
```

**AFL is not installed** and a student account cannot add it, so this lab uses **libFuzzer**, which is built into clang (`-fsanitize=fuzzer`). It is coverage-guided in the same way AFL is, and the ideas transfer exactly.

Read `parser.c` — but not too closely. **Finding the bugs by fuzzing is the exercise**; reading the source first is like reading the answer key.

---

## 1. Part A — Fuzz It (25 min)

```bash
mkdir -p corpus
./fuzz -artifact_prefix=./ corpus
```

libFuzzer runs until it crashes, then saves the crashing input as `crash-<hash>` and stops. It should take **seconds**:

```
==ERROR: AddressSanitizer: heap-buffer-overflow
    READ of size 1 ... in parse
SUMMARY: AddressSanitizer: heap-buffer-overflow parser.c:NN in parse
```

**Reproduce the crash under the sanitizer** so you get the full report deterministically:

```bash
./run_one crash-<hash>
```

Q1: report the crash type, the **exact source line** libFuzzer named, and the crashing input (`xxd crash-<hash>`). It will be short — often under 16 bytes.

**Then find the other two.** libFuzzer stops at the first crash, so move the one you found aside and run again:

```bash
mkdir -p found && mv crash-* found/
./fuzz -artifact_prefix=./ corpus
```

There are **three** bugs: an overflow, an out-of-bounds read, and one that is not a memory error at all. Q2 wants all three, each with its line and a one-line explanation of the input that triggers it.

---

## 2. Part B — Why Coverage Guidance Matters (20 min)

The parser has a check like `if (d[3] == 'R')`. Random bytes pass it one time in 256; two such checks in a row, one time in 65,536.

**(a)** Run with the pointer-coverage counter on and watch it discover structure:

```bash
./fuzz -print_pcs=1 -artifact_prefix=./ corpus 2>&1 | grep -c "NEW"
```

Each `NEW` is an input that reached code no previous input did. Q3: roughly how many executions until the first crash, and how many distinct coverage points did it find on the way?

**(b)** Write a **dumb** fuzzer in ten lines — random bytes, no feedback — and give it the same time budget:

```bash
cat > dumb.sh <<'EOF'
#!/bin/bash
for i in $(seq 1000000); do
    head -c $((RANDOM % 40)) /dev/urandom > t.in
    ./run_one t.in >/dev/null 2>&1 || { echo "crash after $i inputs:"; xxd t.in | head -1; break; }
done
EOF
chmod +x dumb.sh && timeout 60 ./dumb.sh
```

Q4: did the dumb fuzzer find anything in a minute? Compare with libFuzzer's seconds, and explain the difference in terms of the magic-byte checks. *(This is the single idea that made fuzzing practical.)*

---

## 3. Part C — What the Sanitizer Buys (20 min)

The heap bugs from L33, with and without ASan:

```bash
./heap u ; echo "asan uaf rc=$?"          # AddressSanitizer build
./heap d ; echo "asan double-free rc=$?"
./heap_plain u ; echo "plain uaf rc=$?"   # ordinary gcc build
./heap_plain d ; echo "plain double-free rc=$?"
```

Q5: what does each of the four do? The two plain runs are the point — **report their exit codes and whether anything went wrong that a test suite would notice.**

The format-string bug:

```bash
./fmt 'hello'                              # harmless
./fmt 'AAAA %p %p %p %p %p %p'             # the read primitive
./fmt "$(python3 -c "print('%p '*12)")"    # find your own input in the leak
./fmt 'AAAAAAAA%7$n' ; echo "rc=$?"        # the write primitive
```

Q6: from the `%p` leak, which word is your input string, and how do you know? What does the `%n` run do, and why is it a *write* and not a crash-by-accident?

---

## 4. Part D — Fix One (10 min)

Pick the out-of-bounds read in `parser.c` and fix it — a bounds check before the access. Rebuild and re-fuzz:

```bash
make && ./fuzz -max_total_time=30 -artifact_prefix=./ corpus
```

Q7: does the fuzzer still crash on that bug? Does it now find one of the *others* faster, having got past the first? Report what changed. *(A fixed bug often unblocks the fuzzer to reach deeper code — this is why you re-fuzz after every fix, not once at the end.)*

---

## 5. Questions

Answer in the answer sheet. Three or four sentences each unless stated.

**Q1.** Your first crash: the type, the source line libFuzzer named, and the crashing input as hex. How many bytes was it?

**Q2.** All three bugs, each with its line and the input that triggers it. Which one is not a memory-safety error, and what is it instead?

**Q3.** Roughly how many executions to the first crash, and how many coverage points on the way? What does "coverage-guided" mean in one sentence?

**Q4.** Did your dumb fuzzer find anything in a minute? Explain the gap using the parser's magic-byte checks and a probability.

**Q5.** The four heap runs. **The two plain ones are the question:** what exit code, and would a normal test suite have caught either? What does that say about why use-after-free bugs ship?

**Q6.** The `%p` leak and the `%n` write. Which leaked word is your input, and how would `%p` help defeat ASLR (L31 §5)? Why is `%n` a write primitive rather than an accident?

**Q7.** After you fixed one bug, what did re-fuzzing do? Why is "re-fuzz after every fix" the rule rather than "fuzz once at the end"?

---

## 6. Checkoff

Show the TA:

- [ ] All three crashes found by fuzzing, each reproduced under `run_one` with its source line.
- [ ] Your dumb fuzzer's result next to libFuzzer's, and Q4 explained out loud.
- [ ] The two plain heap runs exiting cleanly, and why that is the danger.
- [ ] Your written answers to **Q3, Q5 and Q6**.

**If you finish early:** take a real parser from a small GitHub C project, write a `LLVMFuzzerTestOneInput` for it, and fuzz it under ASan for five minutes. If you find something, that is a real bug — report it to the maintainers, not anywhere else.

**Take with you:** **PS 10 is due Friday** — the ROP exploit, in the sandbox. Fuzzing (this lab) is how you *find* the bug; ROP (PS 10) is what an attacker does with it once found; and the mitigations from the lectures are what stand between the two. Week 11 is containers — the isolation you put a program in when you cannot trust it not to have all of these.

---

*PROG 201 · Week 10 · Lab 10 · © CSE Department*
