# PROG 201 · Lab 8
## A Plugin System with `dlopen`
### Covers Week 8 · sat **Monday of Week 9**, 15:00–16:50, BH 215 · **unmarked, checked off in the session**

---

> **This lab covers Week 8 and is sat in Week 9.** Lab *N* is sat on the Monday of Week *N+1*.
>
> **Project 1 is due at 17:00 on the Friday of this week, and so is PS 8.** Two deadlines, one day.
> Neither needs this lab, but plan the week accordingly — [[PROG 201 Scheduling Notes]] records it.
>
> **Midterm 2 was last Monday.** Marked papers are returned in Tuesday's lecture.
>
> **Unmarked.** The TA checks your work off in the session.

**What you are building:** the mechanism behind every plugin architecture you have used — `dlopen`, an ABI number, and a struct of function pointers.

You will also read a binary. **Part A is twenty minutes with `objdump` and `LD_DEBUG` finding, in a real file, the GOT slot that holds its own PLT stub's address** — which is the trick that makes lazy binding work, and which you cannot really believe until you have seen the bytes.

---

## 0. Setup (5 minutes)

```bash
mkdir -p "$PROG201/week8/lab8"        # $PROG201 is set in ~/.bashrc -- see Lab 0
cd "$PROG201/week8/lab8"
cp "$ACADEMICS/1. Sophomore/Fall/2. PROG 201 - Systems Programming in C/PROG201 Week8/lab/"{host.c,plugin.h,p_double.c,p_square.c,p_bad.c,libgreet.c,useglib.c,faketime.c,usetime.c,Makefile} .

make
./host ./p_double.so ./p_square.so
```

The skeleton builds clean and loads nothing:

```
load(): TODO 1
load(): TODO 1

loading 0 plugin(s) took 0.009 ms
```

**Three plugins are provided.** `p_double` and `p_square` work; `p_bad` declares ABI 0, which this host does not support. Read `plugin.h` first — it is twenty lines and it is the whole interface.

---

## 1. Part A — Read a Binary (25 min)

Build the example from L25 and L26 and look at what the linker produced.

```bash
gcc -O2 -fPIC -shared -o libgreet.so libgreet.c
gcc -O2 -o useglib      useglib.c -L. -lgreet -Wl,-rpath,'$ORIGIN'
gcc -O2 -o useglib_lazy useglib.c -L. -lgreet -Wl,-rpath,'$ORIGIN' \
        -Wl,-z,lazy -Wl,-z,norelro
```

**(a) What does the binary need, and who provides it?**

```bash
readelf -l useglib | grep -A1 INTERP
readelf -d useglib | head -4
ldd useglib
objdump -R useglib | grep JUMP_SLOT
```

Write down: the interpreter, the `NEEDED` libraries, and — Q1 — **which entry `ldd` prints that is not a file on disk.**

**(b) The PLT and the GOT.**

```bash
objdump -d -j .plt -j .plt.sec useglib | grep -A3 "greet@plt"
```

You should see a single `jmp *offset(%rip)`, and `objdump` helpfully names the GOT slot it jumps through.

Now the lazy build, which has a bigger PLT:

```bash
objdump -d -j .plt useglib_lazy | head -20
readelf -x .got.plt useglib_lazy | head -6
objdump -R useglib_lazy | grep JUMP_SLOT
```

**Match the numbers up.** The `.got.plt` dump contains small values like `30100000`, which little-endian is `0x1030` — and `0x1030` is an address in the PLT you just disassembled. **Q2 asks which one and why.**

**(c) When does binding happen?**

```bash
LD_DEBUG=bindings ./useglib_lazy 2>&1 | grep -E "about to|symbol .greet|symbol .farewell|= [0-9]"
LD_DEBUG=bindings ./useglib      2>&1 | grep -E "about to|symbol .greet|symbol .farewell|= [0-9]"
```

**The two outputs are in a different order and that is the entire point.** Q3.

```bash
readelf -d useglib | grep -E "BIND_NOW|FLAGS"
```

---

## 2. Part B — The Plugin Host (40 min)

**TODO 1 — `load`.** `dlopen`, `dlsym`, check the ABI, call `init`, record it.

Four things to get right, and the lab sheet will not tell you the flags:

- **Which `dlopen` flags?** L27 §4 has the table. One of the two choices turns "a broken plugin crashes the host later" into "the plugin does not load", and the other stops two plugins sharing a symbol by accident.
- **Check `dlerror()`, not `dlsym`'s return value** — and clear it first. Q4.
- **Check the ABI before you call anything through the struct.** A plugin built against a different layout has your `apply` pointer somewhere else entirely.
- Every failure path `dlclose`s and says what was wrong.

**TODO 3 — run them.** One line: `apply(x)` for each loaded plugin.

**TODO 2 — unload.** `fini` then `dlclose`, **in reverse order**.

```bash
make run
make errors
```

Expected:

```
  [double] init
  [square] init
loaded double    multiply by two
loaded square    x squared

loading 2 plugin(s) took 0.211 ms

  double   apply(7) = 14
  square   apply(7) = 49

  [square] fini
  [double] fini
```

and, with the bad ones:

```
./p_bad.so: ABI 0, this host wants 1 -- refusing
dlopen ./p_missing.so: ./p_missing.so: cannot open shared object file: No such file or directory
```

**Then write a fourth plugin.** `p_negate.c`, or anything with a different `apply`. Add it to the Makefile's `PLUGINS` and load it alongside the others.

**Check what your plugin exports:**

```bash
nm -D --defined-only p_negate.so
```

**It should be exactly one line.** The Makefile compiles plugins `-fvisibility=hidden` and `plugin.h` defines `PROG201_EXPORT` for the one symbol that must be visible. Q5.

---

## 3. Part C — Interposition (25 min)

**(a)** Build the twelve-line `time()` replacement and use it:

```bash
gcc -O2 -fPIC -shared -o faketime.so faketime.c
gcc -O2 -o usetime usetime.c

./usetime
LD_PRELOAD=$PWD/faketime.so ./usetime
FAKE_TIME=0 LD_PRELOAD=$PWD/faketime.so ./usetime
```

Then confirm where the call went:

```bash
LD_DEBUG=bindings LD_PRELOAD=$PWD/faketime.so ./usetime 2>&1 | grep "symbol .time'"
```

**(b) Now try it on a program you did not write:**

```bash
LD_PRELOAD=$PWD/faketime.so date
```

**It prints the real time.** Q6 — and the answer is not that `LD_PRELOAD` failed.

**(c) Find out which programs run destructors.** Build a two-line probe:

```c
#include <unistd.h>
__attribute__((constructor)) static void c(void){ if(write(2,"[probe] ctor\n",13)<0){} }
__attribute__((destructor))  static void d(void){ if(write(2,"[probe] dtor\n",13)<0){} }
```

```bash
gcc -O2 -fPIC -shared -o probe.so probe.c
for p in /usr/bin/true /usr/bin/ls /usr/bin/grep "python3 -c pass"; do
    echo "== $p"; LD_PRELOAD=$PWD/probe.so $p /etc >/dev/null 2>&1 </dev/null
    LD_PRELOAD=$PWD/probe.so $p /etc 2>&1 >/dev/null
done
```

**Two of those four run the destructor and two do not.** Confirm with `LD_DEBUG=all ... | grep "calling fini"`. Q7, and it matters for PS 8, which is due Friday.

---

## 4. Questions

Answer in the answer sheet. Three or four sentences each unless stated.

**Q1.** `ldd useglib` printed three lines and one of them is not a file. Name it, say who put it in your address space, and give one function that lives there and why that makes it fast.

**Q2.** In `useglib_lazy`, the GOT slot for `greet` initially contains an address **inside the PLT**. Say which instruction it points at and walk through what happens on the first call and on the second. *(Four or five sentences — this is the mechanism.)*

**Q3.** The two `LD_DEBUG=bindings` runs put the binding lines in different places relative to the program's output. Explain both, name the linker flag that causes the difference, and say **why it is the default**.

**Q4.** Why is `if (!dlsym(h, "x"))` the wrong way to check for a missing symbol, and why must you call `dlerror()` before the `dlsym` as well as after?

**Q5.** `nm -D --defined-only` on your plugin shows one symbol. Say what makes that happen, and give two reasons it is better than exporting everything.

**Q6.** `LD_PRELOAD` replaced `time()` in your program and did nothing to `date`. Explain. *(The answer involves a different function and a thing that is not a library.)*

**Q7.** Report which of the four programs ran the destructor. Then say what that means for a `LD_PRELOAD` tool that prints its report from a destructor, and give one way to write such a tool that does not have the problem.

**Q8.** *(One sentence.)* Your host uses `RTLD_LOCAL`. Describe what could go wrong if two plugins were loaded `RTLD_GLOBAL` and both happened to define a function called `helper`.

---

## 5. Checkoff

Show the TA:

- [ ] `make run` and `make errors`, with the ABI refusal and the missing-file error both readable.
- [ ] Your own fourth plugin loading and working, and `nm -D` showing one exported symbol.
- [ ] The `.got.plt` bytes matching a PLT address, and Q2 explained out loud.
- [ ] Your written answers to **Q3, Q6 and Q7**.

**If you finish early:** make the host reload a plugin — `dlclose` it and `dlopen` it again — while the program keeps running, and edit the plugin's source in between. That is hot reloading, it is how a game engine and a web server both do it, and the thing that will surprise you is what `dlclose` does *not* do.

**Take with you:** **PS 8 is due Friday** and is a `LD_PRELOAD` `malloc` profiler — Part C(c) is its Q4. **Project 1 is due the same day.** Week 10's return-oriented programming is L26 §4's writable GOT, used by somebody else.

---

*PROG 201 · Week 8 · Lab 8 · © CSE Department*
