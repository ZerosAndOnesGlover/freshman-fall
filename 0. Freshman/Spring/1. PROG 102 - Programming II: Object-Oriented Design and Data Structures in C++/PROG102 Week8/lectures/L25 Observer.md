# PROG 102 · Lecture 25
## Observer

*“Wherever there is modularity there is the potential for misunderstanding: Hiding information implies a need to check communication.”* — Alan Perlis, "Epigrams on Programming" (1982), #20

**Week 8 · Tuesday · 50 minutes**
**Reading:** Gang of Four Ch. 5, *Observer* · **Assumes:** Week 4, Week 5 (`weak_ptr`), Week 7

**Date:** Tuesday 16 March 2027 · 10:00–10:50 · Week 8

**Coursework:** 📊 **Quiz 8** today 10:00–10:15 · 📝 **PS 7** due Fri 19 Mar 17:00 · 📝 **PS 8** released Fri 19 Mar 10:00, due Fri 26 Mar 17:00 · 🔬 **Lab 8** Mon 22 Mar 15:00–16:50

---

## 1. Intent

> **Define a one-to-many dependency between objects so that when one object changes state, all its
> dependents are notified and updated automatically.**

The **subject** holds state and a list of observers. When the state changes, it calls each observer.
**The subject does not know what the observers are** — only that they satisfy an interface.

You have used this more than any other pattern in the book, in every program you have ever used:

- a **button** notifying its click handlers;
- a **spreadsheet cell** notifying the cells whose formulas depend on it;
- a **file watcher** notifying a build system;
- every "reactive" or "event-driven" framework, which is Observer with better marketing.

---

## 2. The Structure

```cpp
struct Observer {
    virtual ~Observer() = default;
    virtual void notify(int value) = 0;
};

class Subject {
    std::vector<Observer*> observers;
public:
    void attach(Observer* o) { observers.push_back(o); }
    void set(int v)          { for (auto* o : observers) o->notify(v); }
};
```

Twelve lines. **The coupling runs one way**: observers know about the subject's interface, and the
subject knows nothing about any concrete observer. Adding a new kind of observer requires no change to
`Subject` at all — which is the **Open/Closed Principle** (L26 §2.2) in its clearest form.

---

## 3. And It Is Broken

```cpp
Subject s;
{
    Printer temp("temp");
    s.attach(&temp);
}                            // temp is destroyed here
s.set(42);                   // and the subject still has its address
```

```
ERROR: AddressSanitizer: stack-use-after-scope
    ... in Subject::set(int)  observer.cpp:14
```

**The subject is holding a pointer to an object that no longer exists.**

This is not a contrived example. It is the single most common bug in Observer implementations, and it
happens because the pattern as usually drawn has **no answer to the question of lifetime**:

- The subject does not own the observers — it should not, since an observer usually outlives or
  underlives it independently.
- The observers do not own the subject.
- So **nobody is responsible** for removing an observer when it dies.

### 3.1 The Usual "Fix", and Why It Is Not One

```cpp
class Observer { ~Observer() { subject->detach(this); } };     // deregister in the destructor
```

This works, and it costs you:

- **the observer must know its subject**, which reverses the dependency the pattern existed to avoid;
- **it must know *all* its subjects**, if it observes more than one;
- **the order of destruction now matters** — if the subject dies first, `detach` is a use-after-free
  in the *other* direction;
- and it is easy to get wrong in exactly the way that produces intermittent crashes at shutdown.

**Week 5 gave you a better tool.**

---

## 4. `weak_ptr` Observers

> **Just enough capture and `std::function` for Weeks 8–10.** Week 3 gave you empty-bracket lambdas.
> This week's code puts names inside the brackets, and stores lambdas in variables:
>
> ```cpp
> int k = 10;
> auto add_k   = [k](int x) { return x + k; };     // [k]  : a COPY of k, taken now
> auto bump_k  = [&k]() { ++k; };                   // [&k] : a REFERENCE to k — k must outlive the lambda
> std::function<int(int)> f = add_k;                // #include <functional>: holds ANY callable
> f(5);                                             //   taking int, returning int  -> 15
> ```
>
> - The **capture list** names the outside variables the lambda uses: `[k]` copies, `[&k]` refers.
> - `std::function<R(Args...)>` can hold a lambda, a function object or a function pointer with that
>   signature, which is what lets different callables sit in one container.
> - Only capture by reference what you are **sure** outlives the lambda.
>
> What a lambda compiles to, what capture costs, why a dangling capture is the classic bug, and how
> `std::function` works inside are all **Week 11**.

```cpp
class Subject {
    std::vector<std::weak_ptr<Observer>> observers;
public:
    void attach(std::shared_ptr<Observer> o) { observers.push_back(o); }

    void set(int v) {
        observers.erase(std::remove_if(observers.begin(), observers.end(),
            [v](std::weak_ptr<Observer>& w) {
                if (auto s = w.lock()) { s->notify(v); return false; }   // alive: notify, keep
                return true;                                             // expired: drop
            }), observers.end());
    }
    std::size_t count() const { return observers.size(); }
};
```

Measured, with an observer that dies mid-way:

```
observers registered: 2
temp saw 1
alive saw 1
after temp dies, registered: 2
alive saw 42
after notify (pruned):     1
```

**Sanitizer-clean.** Three things happened, and each is worth naming.

**The dead observer was not notified.** `lock()` returned null and it was skipped — no crash, no
special case.

**The list self-cleans.** The expired entry was removed during notification. Nobody had to call
`detach`, and the observer's destructor knows nothing about any subject.

**The count is stale until the next notification** — 2 after `temp` dies, 1 after `set`. That is
correct and worth stating: `weak_ptr` does not remove itself; it just knows it is dead. **If you need
an accurate live count, `count()` must lock each entry** rather than return `observers.size()`.

### 4.1 What It Costs

The subject now requires observers to be held by `shared_ptr`, which is a real constraint — a stack
object cannot be an observer. That is the price of the pattern being safe, and it is usually worth it.

**Note the interaction with L17 §5**: `weak_ptr` here is not breaking a *cycle*, it is expressing
*non-ownership*. Same tool, different reason, and both are in the two lines of L17 §7's preference
list.

> **The Week 5 alternative would be `shared_ptr` observers** — the subject co-owns them, so they cannot
> die while registered. **Do not do this.** It means a subject keeps its observers alive, so a window
> keeps its closed dialogs alive, and a leak becomes a design feature.

---

## 5. Push or Pull

Two variants, and the choice matters more than it looks:

```cpp
virtual void notify(int value);        // PUSH: the subject sends the data
virtual void notify(const Subject&);   // PULL: the observer asks for what it wants
```

| | Push | Pull |
| --- | --- | --- |
| Subject knows what observers need | yes — it sends it | no |
| Observers can want different things | badly | naturally |
| Coupling | looser on lifetime, tighter on data | the reverse |
| Cost when observers ignore the data | computed anyway | not computed |

**Push is simpler and right when every observer wants the same small thing.** Pull is right when
observers want different subsets, or when computing the data is expensive and some observers will not
use it.

The Gang of Four note that pull "emphasises the subject's ignorance of its observers" — which is the
pattern's whole point, so pull is the more orthodox choice. **Push is the more common one in practice**
because it is easier and usually adequate.

---

## 6. The Problems the Pattern Does Not Solve

Worth knowing, because they will bite you and the book is quiet about most of them.

- **Notification order is unspecified.** If observer A's handler depends on observer B having already
  run, you have a bug that will appear when someone reorders a registration.
- **Re-entrancy.** If `notify` causes an observer to `attach` or `detach`, you are mutating the vector
  you are iterating — **Week 3 §L11 §6's invalidation, in its nastiest form.** The `remove_if` version
  above is *not* safe against this. A common fix is to notify over a copy of the list.
- **An observer that throws** aborts the notification, and the remaining observers never hear about it.
  **Week 9** is where this becomes the whole question.
- **Cascades.** A notifies B, which updates C, which notifies A. Nothing in the pattern prevents an
  infinite loop, and spreadsheets have to detect this explicitly.
- **Threads.** If the subject is notified from one thread and observers register from another, the
  vector is a shared mutable structure. **Week 10.**

> **The pattern solves coupling. It does not solve ordering, re-entrancy, exceptions, cycles or
> concurrency**, and every real event system has had to answer all five.

---

## 7. Summary

| Idea | The point |
| --- | --- |
| Intent | One-to-many; the subject knows nothing about concrete observers |
| Open/Closed | New observers need no change to the subject |
| The naive version is **broken** | `stack-use-after-scope`, verified |
| Deregister-in-destructor | Works, and reverses the dependency the pattern avoided |
| **`weak_ptr` observers** | Dead ones are skipped and pruned; nobody calls `detach` |
| The count is stale | Until the next notification |
| Do **not** use `shared_ptr` | The subject would keep its observers alive |
| Push vs pull | Push if everyone wants the same thing; pull otherwise |
| Not solved | Order, re-entrancy, exceptions, cycles, threads |

---

## 8. Exercises

**1.** Implement the naive raw-pointer Observer and reproduce the `stack-use-after-scope`. **Paste the
report** and name the line.

**2.** Rewrite it with `weak_ptr`. Show a dead observer being skipped and the list being pruned.
**Report the count before and after notification** and explain the staleness.

**3.** Write `count()` two ways: `observers.size()`, and a version that locks each entry. **Give a
situation where the difference matters.**

**4.** Implement both push and pull for the same subject. **Give one concrete observer that is much
better served by pull**, and say why.

**5.** Make an observer `attach` a new observer from inside its `notify`. **Run it under
`-fsanitize=address`.** Then fix it by notifying over a copy, and say what that costs.

**6.** Make one observer throw from `notify`. **Report which observers were notified and which were
not.** Do not fix it — Week 9 does.

**7.** Build a two-subject cycle where A's observer updates B and B's observer updates A. **What
happens?** Then add the smallest change that stops it.

---

## 9. Next

**Lecture 26** covers three patterns that all answer the same question — *how do you make a piece of
behaviour a parameter?* — and measures four different ways of doing it, one of which is much slower
than everybody expects.

---

*PROG 102 · Week 8 · Lecture 25 · © CSE Department*
