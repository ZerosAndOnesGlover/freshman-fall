# CS 211 · Programming Languages & Compilers I
## Week 6 · Lecture 1 of 2
### The Instruction Nothing Frees

---

**Reading:** Dragon §7.4–7.6 · Appel ch. 13.1–13.3 · Jones, Hosking & Moss, *The Garbage Collection Handbook*, ch. 2 and 5 · **Next:** L14, roots, generations, and barriers

---

## 1. Two Weeks of Producing Pointers and Never Consuming One

Week 4 gave your compiler an `alloc` instruction. Week 5 taught liveness to describe it. Neither week ever asked where the memory comes from, and neither asked where it goes.

Ask now. Every occurrence of the word `free` in the compiler:

```
$ grep -rn "free" *.py
```

```
regalloc.py:127:            # cost-to-degree ratio: cheap to spill, and frees many edges.
regalloc.py:147:        free = [c for c in range(k) if c not in taken]
regalloc.py:148:        if not free:
regalloc.py:153:            trace.append(f"select   {v} -> no colour free, actual spill")
regalloc.py:155:        assignment[v] = free[0]
regalloc.py:156:        trace.append(f"select   {v} -> r{free[0]}")
```

**Six hits, all in the register allocator, none of them about memory.**

Look at what that says. Registers are a scarce resource with a fixed budget, and your compiler manages them *exactly*: Week 5 computed the precise lifetime of every value, built an interference graph from it, and reused a register the instant its previous occupant died. Not one register is held a moment longer than it is needed.

The heap gets none of that. Eight phases, 2108 lines, and the only resource whose reclamation the compiler has thought about is the one that lives inside a single function. `alloc` is a token in a table. It has been a promise the whole term, and this is the week it comes due.

The reason nothing has broken is that nothing has run. Every phase so far produced a **representation**: tokens, a tree, a typed tree, three-address code, a smaller version of it, an assignment of variables to registers. A representation cannot leak. So Week 6 opens by building the thing that can.

---

## 2. `runtime.py`: The Phase That Executes

`runtime.py` interprets TAC directly. It keeps a heap of objects, hands out addresses, and — the part that matters for the rest of this week — it can be asked at any instruction which addresses the program can still reach.

```
$ python3 runtime.py churn.cy churn 200 --gc=none
```

```
; ---- churn(200) = 20096 ----
; ---- heap ----
  allocated        202 objects        3256 bytes
  freed              0 objects           0 bytes
  still live       202 objects        3256 bytes
  peak live        202 objects        3256 bytes
  collector   none
```

**Two hundred and two allocated, zero freed.** `churn` holds at most eight objects at a time; it is holding two hundred and two. That is not a bug in `churn`. It is the compiler you have written, running.

Run it with `churn 2000000` and the machine runs out of memory. This is what a language with `new` and no plan looks like.

> **A leak is not a crash, and that is the problem.** The program above returns 20096, which is
> correct. Every test passes. The defect is invisible until the input is large enough, at which
> point it is fatal and looks like a machine problem rather than a language problem.

---

## 3. Stack and Heap: Why One of Them Is Free

Week 5's register allocator handled locals, and CS 201's stack frames handled the ones that spilled. Neither needed a collector. Why not?

**Because a stack frame's lifetime is a property of the program text.** A local is created on entry and destroyed on return; the compiler knows both points statically, and "destroy" is one instruction — add a constant to the stack pointer. Deallocation is free because *deallocation order is forced*: last in, first out, always.

The heap exists for values whose lifetime is *not* nested like that. `new Node` inside a loop, returned from a function, stored into an array that outlives the frame — the moment a value can outlive the frame that made it, the stack discipline cannot express it, and the question "when is this dead?" stops having a syntactic answer.

| | stack | heap |
|---|---|---|
| lifetime known | statically, from the CFG | **dynamically, from the object graph** |
| deallocation | one instruction, LIFO | requires knowing what still points here |
| cost of getting it wrong | impossible | leak, or use-after-free |

**This is the whole subject.** Everything else in this lecture and the next is an answer to "what still points here?"

---

## 4. Manual Memory Management, and Its Two Failure Modes

The obvious answer is to make the programmer say. Add `free(p)` and let them call it.

C does this. It has two failure modes and they are not symmetric.

**Free too late (or never) — a leak.** The program grows. It is slow, then it dies. Bad, but *monotone*: the program's answers are correct right up until it stops.

**Free too early — a use-after-free.** The program keeps a pointer to memory the allocator has handed to someone else. Now two parts of the program disagree about what is at that address.

Our runtime raises on this, which no real runtime does:

```python
class UseAfterFree(Exception):
    """A real runtime does not raise this.  It reads whatever is now at that
    address and carries on, which is why use-after-free is a security bug
    and not a crash."""
```

**A leak wastes memory. A use-after-free hands an attacker a write primitive.** Reading freed memory returns whatever now lives there; writing it corrupts whatever now lives there; and if the attacker controls what gets allocated in between, they control what you write. That is the mechanism behind a large fraction of the CVEs in every C and C++ codebase.

*CS 201 reaches this same failure from the other side in Week 9, and finds that
`-fsanitize=address` names a use-after-free at both the free and the misuse. Worth
remembering when you debug PS 6: the tool exists because the bug is silent.*

> **The asymmetry is the argument for automatic memory management.** Both failure modes come
> from the same question — "is anything still pointing here?" — and a human answering it by hand
> is answering a *global* question with *local* information. The function calling `free` cannot
> see the rest of the program.

---

## 5. Reference Counting

The first automatic answer. Give every object a count of how many pointers refer to it. Increment on every pointer copy, decrement on every pointer destruction, and free when the count reaches zero.

`collect.py`'s `RefCount` implements it against the runtime's six hooks:

```python
def on_var_write(self, old, new):
    self.incref(new)
    self.decref(old)

def on_heap_write(self, obj, old, new):
    self.incref(new)
    self.decref(old)

def on_frame_exit(self, frame):
    for v in list(frame.env.values()):
        self.decref(v)
```

**Increment before decrement, always.** Write those two lines in the other order and `x = x` frees the object between them: the count drops to zero, the object is reclaimed, and then it is incremented back to one — a live object on the free list.

Note the shape of `decref`: it is a *worklist*, not a recursion.

```python
work = [v.addr]
while work:
    a = work.pop()
    ...
```

Freeing an object drops the counts of everything it points at, which may free those too. Dropping the head of a thousand-element list frees all thousand, and a recursive implementation recurses a thousand deep to do it. This is not hypothetical — it is how CPython's deallocator used to overflow the C stack on long lists.

---

## 6. Reference Counting Measured: It Is Very Good

```
$ python3 runtime.py churn.cy churn 200 --gc=rc --threshold=16
$ python3 runtime.py churn.cy churn 200 --gc=mark --threshold=16
```

| | allocated | freed | **peak live** |
|---|---|---|---|
| `--gc=none` | 202 | 0 | 202 objects · 3256 B |
| `--gc=rc` | 202 | **202** | **8 objects · 152 B** |
| `--gc=mark` | 202 | 187 | 16 objects · 280 B |
| `--gc=gen` | 202 | 195 | 31 objects · 520 B |

**Reference counting has the smallest footprint of the four, by a factor of two over mark-sweep and four over generational.** It frees every object, and it frees each one at the instruction where the last pointer to it dies — not at the next collection, because there is no next collection.

That is worth stating plainly, because reference counting is usually introduced as the naive one:

> **Reference counting is the only collector here that is *prompt*.** Peak footprint is not a
> tie-breaker; for a program on a small device it is the whole specification. This is why Swift
> and Objective-C use it, why C++'s `shared_ptr` is it, and why CPython uses it as its primary
> mechanism.

It also has a property none of the others have: **it can tell you when an object died.** Section 7 needs that.

---

## 7. An Aside That Is Not an Aside: Only a Prompt Collector Can Measure a Lifetime

Next lecture's entire argument rests on the claim that most objects die young. Measure it.

```
$ python3 runtime.py churn.cy churn 2000 --gc=mark --threshold=64 --lifetimes
```

```
; ---- age at death, 1983 objects (age = allocations survived) ----
     8 <= age < 16       238   22.3% cum  ######
    16 <= age < 32       487   46.8% cum  ############
    32 <= age < 64       955   95.0% cum  #######################
    64 <= age < 128       99  100.0% cum  ##
  median age 33   mean 33.3   max 84
```

Median age 33, with a threshold of 64. Now the same program under reference counting:

```
$ python3 runtime.py churn.cy churn 2000 --gc=rc --lifetimes
```

```
; ---- age at death, 2002 objects (age = allocations survived) ----
     1 <= age < 2       1713   85.6% cum  #########################################
    16 <= age < 32       284   99.9% cum  #######
   256 <= age              2  100.0% cum  
  median age 1   mean 6.8   max 2001
```

**Median age 1 against median age 33, on the same program.** One of these is wrong, and it is not hard to say which: a tracing collector does not notice a death when it happens, it notices at the next collection. Its histogram has a median of half the threshold because *that is what it is measuring*. It is measuring itself.

The reference-counted numbers describe the program, and they describe it exactly:

- **85.6% die at age 1** — allocated, summed, and dropped on the next iteration.
- **284 die between 16 and 32** — every seventh object is stored into `keep`, which has four slots, so a stored object is overwritten after about 28 further allocations. 28 is in that bucket. The histogram is reporting the program's source code back at us.
- **2 die at age 2001** — `seed` and `keep`, at frame exit.

> **Instrument with the tool that can see the event.** The tracing collector was not lying; it was
> answering a different question, and the fact that both questions produce a number with the word
> "age" on it is exactly how a measurement goes wrong without anybody noticing.

---

## 8. The Thing Reference Counting Cannot Do

A count of zero proves the object is unreachable. **A count above zero does not prove it is reachable.**

Two objects that point at each other hold each other's count at one. Drop every external pointer and both counts stay at one. Neither is reachable from anywhere, and neither will ever be freed.

```
        a ---> [b] ---> b ---> [a] ---> a
        ^                                |
        +--------------------------------+
```

Reference counting is *sound* — it never frees a reachable object — but it is **incomplete**: there is garbage it cannot identify. And the garbage it cannot identify is exactly the shape that doubly-linked lists, parent pointers, observer registrations, and cyclic object graphs all have.

---

## 9. Try to Build One in Cyan. You Cannot.

So write the cycle and measure the leak. Three attempts:

```
$ python3 runtime.py cyc_direct.cy direct
error: line 14 col 11: struct 'Node' is missing field(s): next

$ python3 runtime.py cyc_empty.cy viaEmpty
error: line 18 col 22: cannot infer the type of an empty array literal

$ python3 runtime.py cyc_array.cy viaArray
error: line 13 col 3: cannot assign [[int]] to a target of type [int]
```

**Three attempts, three rejections, three different rules.**

**Attempt 1 — the self-referential field.** `struct Node { val: int; next: Node; }` is a legal declaration. `new Node` must initialise every field, `next` needs a `Node`, and there is no `Node` yet. There never will be: the first one is impossible. The type is *declarable and uninhabitable*, and Cyan's checker discovers this one object at a time rather than by looking at the declaration.

**Attempt 2 — patch the pointers in afterwards.** Build the objects pointing at nothing, then assign. This is exactly how you would do it in Java, with `null`. Cyan has no `null`, so the stand-in is an empty array — and `[]` has no elements to infer an element type from. The annotation on the `let` says what it should be, but `check_expr` never receives it.

**Attempt 3 — forget structs; make an array hold itself.** `r` is `[[int]]`, so `r[0]` is `[int]`. To succeed we would need a type `T` with `T = [T]`. That is an infinite type, and the grammar has no way to write one down. Week 3's Hindley-Milner rejected the same thing and called it the occurs check.

The conclusion is a real property of the language, and it is not a small one:

> **Reference counting is complete for Cyan.** Every heap our front end can build is acyclic, so
> a count of zero and unreachability coincide, and `--gc=rc` frees everything.
>
> **That is a fact about Cyan's type checker, not about reference counting.**

Which is the most useful thing this course can show you about a language guarantee: *the property held, and it held for a reason nobody designed.* Nobody sat down and decided Cyan would be acyclic. It fell out of three unrelated rules — mandatory field initialisation, no null, and no type inference for empty literals — and any one of them relaxing takes it away.

---

## 10. Relaxing One of Them: Eleven Lines

Attempt 2's rejection is the weakest of the three, and it is not even about cycles. `[]` fails because `check_expr` infers bottom-up and never learns what the context wanted. Give it that information:

```python
def check_expr(self, e, scope, expect=None):
```

and in the `Array` case:

```python
if not e.items:
    if expect is None or expect.name != 'array':
        err(e, "cannot infer the type of an empty array literal, "
               "and the context does not say what it should be")
    t = expect          # fall through: `e.ty = t` still has to run
```

then pass the expectation down at the four places that have one — a `let` with an annotation, an assignment (the target's type), a struct field initialiser, and a top-level `let`.

**Six call sites, eleven lines of code.** Checking bottom-up and *also* pushing an expected type downwards is called **bidirectional type checking**, and this is the smallest instance of it that does anything. Every prior week's test program still compiles.

Now:

```
$ python3 runtime.py cycle.cy leak 5 --gc=rc
```

```
; ---- leak(5) = 15 ----
  allocated         25 objects         440 bytes
  freed              5 objects          40 bytes
  still live        20 objects         400 bytes
  freed at rc=0                   5 objects
  still counted                  20 objects  <- unreachable if this is the end of the program
```

```
$ python3 runtime.py cycle.cy leak 5 --gc=mark --threshold=8
```

```
  allocated         25 objects         440 bytes
  freed             20 objects         352 bytes
  still live         5 objects          88 bytes
```

**Eighty per cent of the heap, leaked, by a collector that was complete an hour ago.** Five calls leak twenty objects; five hundred leak two thousand. The leak is linear in the work done, which is the worst kind.

> **A language guarantee is a conjunction, and you rarely know all of its terms.** "Reference
> counting suffices here" was true, and it depended on a rule about *empty array literals*.
> If you cannot enumerate what a guarantee depends on, you cannot predict which change will
> end it — and the change that ended this one was eleven lines that had nothing to do with
> memory.

---

## 11. The Other Answer: Trace

Reference counting asks each object "how many people point at you?" — a local question with a local answer, which is why it is prompt and why it cannot see cycles. A cycle is a *global* structure and no local count reveals it.

So ask the global question instead. **Start from what the program can reach directly, and follow every pointer.** Whatever you do not arrive at is garbage — cyclic or not, because reachability does not care about the shape of the graph.

That is tracing, and it needs one thing reference counting never needed: **the root set**, the addresses the running program holds outside the heap. L14 is largely about where that comes from and what it costs to get it wrong.

**Three colours.**

- **White** — not yet reached.
- **Grey** — reached; children not yet scanned.
- **Black** — reached; children scanned.

Start with the roots grey and everything else white. Repeatedly take a grey object, blacken it, and grey its white children. When no grey remains, **every white object is garbage** — sweep them.

```python
black = set()
grey = list(self.m.roots())
while grey:
    a = grey.pop()
    if a in black:
        continue
    black.add(a)
    obj = self.heap.objs.get(a)
    for c in obj.refs():
        if c not in black:
            grey.append(c)

dead = [a for a in self.heap.objs if a not in black]
```

**The `if a in black: continue` is what makes cycles work.** An object already blackened is not scanned again, so a cycle is traversed once and terminates. Reference counting has no equivalent line because it never traverses anything.

The correctness invariant is: **no black object ever points to a white object.** If that holds when the marking finishes, every white object is unreachable. In a stop-the-world collector it holds for free — the program is not running, so it cannot create such a pointer. L14 §7 is about what it costs to keep it true when the program *is* running.

Note also what tracing does **not** need: `on_var_write`, `on_heap_write`, `on_frame_exit`. `MarkSweep` implements two of the six hooks and ignores four. Reference counting needs all six.

> **That asymmetry is the trade, and it is not mainly about speed.** Reference counting maintains
> an invariant continuously: it pays a little on every pointer write, forever, and can answer "is
> this garbage?" immediately. Tracing reconstructs the answer from scratch: it pays nothing on
> writes, and answers all at once, **at a time the program did not choose**. Everything in L14 —
> generations, barriers, concurrency — is an attempt to have both.

---

## 12. Somebody Else's Runtime Has Exactly This Problem

None of this is a toy. CPython is reference-counted, has precisely the incompleteness of §8, and ships a *second* collector to clean up after the first.

```
$ python3 pycycle.py
```

```
; with gc DISABLED -- reference counting alone
  no cycle               built  200 nodes   refcounting left    0 alive   gc.collect() then freed    0
  cycle                  built  200 nodes   refcounting left  200 alive   gc.collect() then freed  200

; with gc ENABLED -- the cycle collector runs on its own schedule
  10000 cycles built      9998 nodes still alive without an explicit collect
  gc.collect() freed      9998 objects;    0 nodes remain
```

**Two hundred nodes built, two hundred leaked, zero freed** — on the interpreter you have run every program in this course on. Add `b.link = a` and the leak appears; remove it and it does not.

And with the cycle collector enabled, ten thousand cycles are *still* sitting in memory until something triggers a collection. `gc.get_threshold()` reports `(2000, 10, 0)` on this machine: the tracing pass runs after a net two thousand allocations, not when the garbage appears. **Automatic does not mean immediate.**

The lesson generalises past Python. Every reference-counted production runtime either accepts the leak (Swift, Objective-C — where you are expected to break cycles by hand with `weak`) or bolts on a tracer (CPython, PHP). **There is no third option, because §8 is not an implementation detail.**

---

## 13. What to Take From This

1. **`alloc` was a promise for two weeks.** A representation cannot leak; a runtime can.
2. **The stack is free because its lifetimes are nested.** The heap is the case where they are not, and that is the entire reason this subject exists.
3. **Manual `free` has two failure modes and they are not symmetric.** Too late is a leak. Too early is a security bug.
4. **Reference counting is prompt and has the smallest footprint here** — 8 objects peak against mark-sweep's 16. It is not the naive option.
5. **Only a prompt collector can measure a lifetime.** Median age 1 versus median age 33, same program; the tracer was measuring its own threshold.
6. **A count of zero proves unreachability; a positive count proves nothing.** Cycles are the gap, and they are the shape real data structures have.
7. **Cyan could not express a cycle, for three unrelated reasons, none of them designed.** Eleven lines of bidirectional type checking ended it and leaked 80% of the heap.
8. **Tracing answers the global question and does not care about graph shape** — at the cost of needing a root set, and of stopping the program to ask.

**Next:** where roots come from — and the discovery that we already wrote the analysis that produces them, in Week 5, for a completely different reason.

---

*CS 211 · Week 6 · Lecture 13 · © CSE Department*
