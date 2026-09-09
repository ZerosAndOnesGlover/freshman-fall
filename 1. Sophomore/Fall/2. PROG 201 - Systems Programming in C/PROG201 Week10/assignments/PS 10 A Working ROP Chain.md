# PROG 201 · Problem Set 10
## A Working ROP Chain (Sandboxed)

---

**Released:** Week 10, Wednesday · **Due:** Week 11, Friday 17:00
**Total: 100 points** · Submit one PDF, `PS10_{LastName}_{StudentID}.pdf`, and your code as `PS10_{LastName}.tar.gz`

> **This is a sandboxed exercise on a binary the course gives you.** The target `vuln` is compiled
> with protections removed on purpose and is run under `setarch -R`, which turns off address
> randomisation **for that one process only** — you never change the machine-wide setting, and
> nothing here applies to a program you were not handed. The point of building the exploit is
> stated in every lecture this week: **you cannot reason about a mitigation you have not watched
> fail.** Part D is where you turn each one back on and watch it work.
>
> **Run every attack under `setarch -R ./vuln`.** An exploit that "does not work" is very often one
> you forgot to run in the sandbox.
>
> Everything you submit must build clean; the exploit script is Python 3 and needs no libraries.

---

### The Target

```bash
cd ps10
make                       # builds vuln (non-PIE, no canary, NX on), vuln_pie, vuln_canary
./checksec.sh vuln
./gadget.py vuln           # the course's 40-line gadget finder (ROPgadget is not installed)
echo hello | setarch -R ./vuln
```

`vuln` reads a line with `gets` into a 64-byte buffer. It contains a function `unlock(long key)` that spawns a shell **only if called with `key == 0xc0ffee`** — so a plain jump to it is not enough; you must control the argument register. Two gadgets to do that are present in the binary (a real target would borrow them from libc; the build record explains why a hardened libc has too few).

---

### Q1: Find the Offset (16 points)

**(a) [10]** Find the distance from the start of the buffer to the saved return address, and show your working — the marker method (L31 §2), a cyclic pattern, or gdb. Report the offset and how you confirmed it.

**(b) [6]** Explain what the eight bytes at that offset are, and what the eight bytes *before* them are. Why is the offset larger than the buffer size?

---

### Q2: ret2win, and Why It Is Not Enough (18 points)

**(a) [8]** Overwrite the return address with the address of `unlock` and run it. Report what happens. It will reach `unlock` and then **crash** — capture the crash and identify, from a debugger, the exact instruction it died on.

**(b) [6]** That crash is a stack-alignment problem. Explain it: which instruction faults, why the ABI requires what it requires, and which single gadget fixes it. *(L32 §3.)*

**(c) [4]** Even fixed, jumping to `unlock` prints the *wrong-key* branch. Explain why — what is in `%rdi` when you arrive by a plain overwrite, and why is it not `0xc0ffee`?

---

### Q3: The Chain (34 points)

**(a) [20]** Build `exploit.py`: a ROP chain that calls `unlock(0xc0ffee)` and gives you a shell. It must use the alignment gadget **and** a register-control gadget — a genuine chain, not ret2win.

Submit the script and a transcript showing the shell running a command (`id`, or anything that proves execution).

**(b) [8]** Annotate your chain. For each 8-byte word from the offset onward, say what it is (padding, a gadget address, data a gadget consumes, or the target) and what the CPU does when the preceding `ret` lands on it. A table is fine.

**(c) [6]** Your chain reused `pop rdi ; ret` and a bare `ret`. Find both with `./gadget.py`, give their addresses, and explain **why every byte the CPU executed satisfied NX** even though you injected a payload. *(This is the whole point of ROP — say it precisely.)*

---

### Q4: Turn the Defences Back On (24 points)

For each mitigation: rebuild or re-run so it is active, run your **unchanged** exploit, and report what happens and why.

**(a) [6] Stack canary.** Run against `vuln_canary`. Report the exact message and exit code, and say what the canary is, where it is read from, and why your overflow cannot avoid it.

**(b) [6] ASLR, without PIE.** Run your exploit against `vuln` **without** `setarch -R` (ASLR on). It probably still works. Explain why — which regions does ASLR randomise, and why are your gadget and `unlock` addresses unaffected? *(L31 §5. This surprises people.)*

**(c) [6] PIE.** Run against `vuln_pie` (with ASLR on). Now it fails. Explain what changed, and what an attacker would need to make the exploit work again.

**(d) [6] NX.** You did not need to defeat NX — explain why not, i.e. why a ROP chain is NX-clean. Then describe what the exploit would have looked like on a pre-NX executable stack, and confirm with `./checksec.sh` what `vuln`'s stack permission actually is.

---

### Q5: The Hardware Question (8 points)

**(a) [4]** Count the `endbr64` instructions in `vuln` (`objdump -d vuln | grep -c endbr64`). What are they for, and check `/proc/cpuinfo` for `shstk` — is anything on this machine enforcing them?

**(b) [4]** A **shadow stack** would stop your exploit where a canary does not. Explain the difference: what does each protect, and why can a ROP chain get past one but not the other? Then say, in one sentence, why this machine's CPU does not stop you.

---

## Marks

| Q | Topic | Points |
|---|---|---:|
| 1 | Find the offset | 16 |
| 2 | ret2win, and why it is not enough | 18 |
| 3 | The chain | 34 |
| 4 | Turn the defences back on | 24 |
| 5 | The hardware question | 8 |
| | **Total** | **100** |

**Late work:** [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] applies. The lowest problem set of the term is dropped.

**A note on conduct.** This exercise is why the department can teach exploitation at all: it is bounded to a binary we wrote, in a sandbox you control, for the purpose of understanding the defences. Using these techniques against any system you were not given is a violation of [[Year2 - Sophomore/COURSE POLICIES|COURSE POLICIES]] and of the law, and it is not what the marks are for.

---

*PROG 201 · Week 10 · PS 10 · © CSE Department*
