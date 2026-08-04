# PROG 102 · Lecture 27
## State, MVC, and What C++11 Obsoleted

**Week 8 · Friday · 50 minutes**
**Reading:** Gang of Four Ch. 5 — State · **Assumes:** L25, L26

---

## 1. State

> **Allow an object to alter its behaviour when its internal state changes. The object will appear to
> change its class.**

The problem it replaces is a `switch` in every method:

```cpp
void Door::open() {
    switch (state) {
        case CLOSED: state = OPENED; break;
        case OPENED: /* already open */ break;
        case LOCKED: throw std::logic_error("locked"); break;
    }
}
void Door::close() { switch (state) { /* the same three cases again */ } }
void Door::lock()  { switch (state) { /* and again */ } }
```

**Three methods × three states = nine cases**, and adding a state means finding and editing every
`switch`. This is the Week 4 type-switch problem in temporal clothing.

State makes each state a class:

```cpp
struct DoorState {
    virtual ~DoorState() = default;
    virtual void open(Door&)  = 0;
    virtual void close(Door&) = 0;
    virtual const char* name() const = 0;
};

struct Closed : DoorState {
    void open(Door& d) override { std::puts("opening"); d.set(std::make_unique<Opened>()); }
    void close(Door&)  override { std::puts("already closed"); }
};
```

The `Door` holds a `unique_ptr<DoorState>` and forwards. **A transition is an assignment.**

```
state=closed
opening
state=opened
already open
closing
state=closed
```

### 1.1 What It Buys, and What It Costs

**Buys:** each state's behaviour is in one place; adding a state adds a class and edits nothing; the
transitions are explicit in code rather than implicit in a nest of conditions.

**Costs:** a class per state, and — the real one — **the transitions are now scattered**. To know
everything that can lead to `Locked`, you must read every state class. The `switch` version had all
transitions in one visible table.

> **The trade is: behaviour localised, transitions distributed.** For a machine with many states and
> simple behaviour, a **transition table** (a `map` from state and event to state) is often clearer
> than either. **State is right when each state does something substantially different**, and
> over-applied when the states differ only in which one comes next.

**Note State's structural identity with Strategy** — both delegate to a swappable object. The
difference is entirely in intent: a Strategy is chosen *by the client* and stays put; a State changes
*itself*, in response to events. Same code, different story, and the Gang of Four list them separately
for that reason alone.

---

## 2. Model-View-Controller

Not one of the 23. **MVC is an architectural pattern** — it organises a whole program rather than a
handful of classes.

| Part | Holds | Knows about |
| --- | --- | --- |
| **Model** | the data and the rules | nothing |
| **View** | the presentation | the model |
| **Controller** | input handling | the model and the view |

**The Model knows nothing about the other two**, which is the entire point: the same model can drive a
GUI, a web page and a test harness.

**And the mechanism that lets the View track the Model is Observer.** MVC is largely Observer plus a
convention about who is allowed to know what — which is why it is taught here rather than as its own
topic.

> **A warning worth giving.** MVC is the most argued-about acronym in software, and the reason is that
> nobody agrees where the controller stops. MVP, MVVM and a dozen framework-specific variants exist
> because the original description is ambiguous about it. **Do not learn a definition and defend it.**
> Learn the invariant — *the model does not know about the presentation* — which every variant keeps,
> and treat the rest as local convention.

---

## 3. The Week's Argument

You have now implemented five behavioural patterns. **Two of them are largely obsolete in modern C++**,
and the reason is worth more than the patterns.

### 3.1 The Claim

**A design pattern is a workaround for something the language cannot say.**

In 1994, C++ had no way to pass *behaviour with attached state* as a value. Your options were:

- a **function pointer** — no state;
- an object with a **virtual method** — state, at the cost of a class, an interface, and a heap
  allocation.

**Strategy and Command are both that second option**, given names. They are what a closure looks like
in a language without closures.

C++11 added closures.

### 3.2 Command, Both Ways

The 1994 version — an interface, a concrete command class, a history:

```cpp
struct Command { virtual ~Command()=default; virtual void execute()=0; virtual void undo()=0; };
class AppendCmd : public Command { Document& d; std::string s; /* ctor, execute, undo */ };
class History { std::vector<std::unique_ptr<Command>> done; /* run, undo */ };
```

The modern version:

```cpp
struct Action { std::function<void()> doit, undoit; };
class History {
    std::vector<Action> done;
public:
    void run(Action a) { a.doit(); done.push_back(std::move(a)); }
    bool undo() { if (done.empty()) return false; done.back().undoit(); done.pop_back(); return true; }
};
```

with commands built inline:

```cpp
auto append = [&doc](std::string s) {
    return Action{ [&doc,s]{ doc += s; },
                   [&doc,s]{ doc.resize(doc.size() - s.size()); } };
};
h.run(append("Hello"));
```

Both produce identical behaviour. Counted:

| | non-blank lines | types |
| --- | --- | --- |
| 1994 style | **20** | **4** |
| modern | **8** | **2** |

**And the modern version needs no new class per action.** Adding a "delete" command is one more lambda
pair, not one more class.

### 3.3 Strategy, Both Ways

```cpp
struct Compare { virtual bool less(int,int) const = 0; };      // + a class per ordering
struct Ascending : Compare { bool less(int a,int b) const override { return a<b; } };
```

against

```cpp
auto asc = [](int a, int b) { return a < b; };
int k = 10;
auto shifted = [k](int x) { return x + k; };      // captures state -- a function pointer cannot
```

**And it is faster.** From L26 §3: the lambda is 159.9–160.9 ms where the virtual Strategy is
165.7–167.6 ms and `std::function` is 287.5–304.1 ms.

**Fewer lines, fewer types, and quicker.** There is no axis on which the 1994 Strategy wins for the
common case of "pass a comparison".

### 3.4 What C++11 Did *Not* Obsolete

This is the important half, and the reason §3.1's claim is a scalpel rather than a hammer.

- **Observer is untouched.** Its problem is *lifetime and notification*, not "how do I pass a
  function". `weak_ptr` improved the implementation; the pattern is the same shape.
- **State is untouched.** Each state has several methods and its own identity. A lambda cannot be a
  state machine.
- **Template Method is untouched.** It is about a class hierarchy's structure, not about passing
  behaviour.
- **Strategy survives when it has state, several methods, or a lifetime** — a policy object rather than
  a function.
- **Command survives when the action must be inspected** — serialised, logged, sent over a network,
  shown in a UI as "Undo *Rename*". **A `std::function` cannot tell you what it does**; a `Command`
  object can carry a name and parameters.

> **So the honest statement is narrower than "patterns are obsolete":**
>
> **The patterns that existed only to package a callable have been absorbed into the language. The
> patterns that were about structure, lifetime or identity have not.**

### 3.5 Why This Matters Beyond C++

The Gang of Four wrote down what worked in 1994 in C++ and Smalltalk. **Every pattern in the book is,
in part, a description of what those languages could not express**, and later languages absorbed the
most useful ones:

- C++11 lambdas absorbed Strategy and Command.
- Java 8's streams absorbed much of Iterator.
- Languages with first-class functions never needed either.
- `std::variant` and pattern matching are eating Visitor.

**That is not a failure of the book. It is the book working**: a pattern that recurs often enough
eventually becomes a feature. **Recognising which of today's patterns are tomorrow's language features
is the skill**, and it is why L22 §6.3 warned that being in the catalogue is not an endorsement.

---

## 4. Summary

| Idea | The point |
| --- | --- |
| **State** | A class per state; transitions are assignments |
| State's cost | Behaviour localised, **transitions distributed** |
| State vs Strategy | Structurally identical; differ only in intent |
| **MVC** | Architectural; the model knows nothing. Built on Observer |
| MVC's variants | Learn the invariant, not a definition |
| **The argument** | A pattern is a workaround for what the language cannot say |
| Command, 1994 vs modern | **20 lines / 4 types** → **8 lines / 2 types** |
| Strategy, 1994 vs modern | Fewer lines, fewer types, **and faster** |
| **Not obsoleted** | Observer, State, Template Method; Strategy/Command with state or identity |
| The general form | Patterns that packaged a callable were absorbed. Structural ones were not |

---

## 5. Exercises

**1.** Implement the `Door` state machine with three states — closed, opened, locked — using State.
Then implement it with a `switch` in each method. **Count the cases in each.**

**2.** For your State version, answer: **what must you read to know every way of reaching `Locked`?**
Then say what a transition table would have given you.

**3.** Implement Command 1994-style and lambda-style for the same three actions. **Report non-blank
lines and type counts for both.**

**4.** Add **redo** to both versions from exercise 3. **Which was easier, and by how much?**

**5.** Give a concrete case where the 1994 Command is **better** than the lambda version. *(§3.4 gives
you the category; you supply a specific example.)*

**6.** §3.1 claims a pattern is a workaround for a missing language feature. **Find a counterexample
in the catalogue** — a pattern that would still be needed in a language with every feature you can
think of. Defend it in three sentences.

**7.** Pick any pattern from Weeks 7–8 and argue that a *future* C++ feature could absorb it. Name the
feature.

---

## 6. Next

**Week 9** is exception safety — the three guarantees, `noexcept`, and why RAII is the only thing that
makes any of it tractable. It also answers the question L25 §6 left open: **what happens when an
observer throws halfway through a notification?**

**Project 1 is due Friday.**

---

*PROG 102 · Week 8 · Lecture 27 · © CSE Department*
