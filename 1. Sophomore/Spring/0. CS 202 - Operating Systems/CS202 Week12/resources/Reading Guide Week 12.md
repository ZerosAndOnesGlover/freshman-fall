# CS 202 · Reading Guide · Week 12
## Security, and What the Course Was

---

**Three lectures, one problem set, one lab, and the final.** The reading this week is short because **the revision guide in this folder is the other half of it.**

---

## Required

### OSTEP, chapters 53–54 — *Introduction to Security*, *Authentication*

**Read 53 properly and skim 54.** OSTEP's security chapters are the weakest in the book — they were added late and cover ground the rest of the book does not connect to. **Read 53 for the vocabulary** (subject, object, principal, policy against mechanism) and **ignore its treatment of access control lists**, which the lectures replace with what this machine actually does.

**What to take from it:** the distinction between **policy** (what should be allowed) and **mechanism** (what enforces it). L37 assumes you have it.

---

### Saltzer & Schroeder (1975), *The Protection of Information in Computer Systems* — **section I only**

**Eleven pages, and still the best thing written on the subject.** Section I gives the eight design principles. **Read them slowly and try each against the machine in front of you:**

| Principle | Ask |
|---|---|
| Economy of mechanism | how many lines are in this machine's TCB? |
| Fail-safe defaults | what happens when the seccomp filter does not match? |
| **Complete mediation** | which checks are in silicon, and which are in a program that might be skipped? |
| Open design | which of this course's defences depends on secrecy? *(none)* |
| Separation of privilege | why does `sudo` ask for a password it already knows you can supply? |
| **Least privilege** | **this is L38, in full** |
| Least common mechanism | what does the page cache share between users? |
| Psychological acceptability | why is `setarch -R` available to everyone? |

**Skip sections II and III** unless you are interested — they describe descriptor-based hardware that did not survive.

---

### `man 2 seccomp`, `man 7 capabilities`, `man 2 prctl`

**These are the reading for PS 12** and there is no substitute. Read:

- **`seccomp(2)`** — all of it, including **"Caveats"**, which explains why the filter cannot dereference a pointer.
- **`capabilities(7)`** — the list of 41, then the five sets (permitted, inheritable, effective, bounding, ambient). **Read the `CAP_SYS_ADMIN` entry and count what it governs.**
- **`prctl(2)`** — `PR_SET_NO_NEW_PRIVS` only.

---

## Recommended

### Anderson (1972), *Computer Security Technology Planning Study* — the reference monitor

**Two pages of it matter**: the three requirements (complete mediation, tamper-proof, verifiable). **Everything since is a negotiation over the third.**

### Thompson (1984), *Reflections on Trusting Trust* — three pages

**Read this once in your life and this is the week.** It is the Turing Award lecture, and it ends by demonstrating that **you cannot trust code you did not write yourself — and that includes the compiler that compiled the compiler.** It is the reason "the toolchain" is in L37's TCB table.

### Klein et al. (2009), *seL4: Formal Verification of an OS Kernel*

**Read the abstract and section 2.** It is what satisfying the reference monitor's third requirement actually costs: **about 200,000 lines of proof for 8,700 lines of C**, and a design in which drivers and file systems are outside the kernel entirely.

### The vulnerability directory, as a reading

```bash
grep . /sys/devices/system/cpu/vulnerabilities/* | sed 's|.*/||'
```

**Pick the one line that says `Vulnerable` and read about that flaw.** It is more instructive than any survey, because it is about the machine you are typing on.

---

## Not Required, But Worth An Evening

- **Lipp et al., *Meltdown*, and Kocher et al., *Spectre*.** The introductions alone explain why every system call in this course cost 840 ns instead of 80.
- **Corbet, *Some seccomp philosophy*, LWN.** Why a syscall filter is not a security boundary on its own.
- **`Documentation/userspace-api/seccomp_filter.rst`** in the Linux tree — the authors explaining their own design.

---

## Before the Final

**Read `Final Revision Guide.md` in this folder.** It is one page: **per week, the one idea and the one number.** If you can reconstruct the reasoning behind each line of it, you are prepared.

**Then re-read your own reports.** Twelve problem sets and eleven labs of your own measurements are a better revision text than any of the above, **because you know what you had to fix to get each number.**

---

*CS 202 · Week 12 · Reading Guide · © CSE Department*
