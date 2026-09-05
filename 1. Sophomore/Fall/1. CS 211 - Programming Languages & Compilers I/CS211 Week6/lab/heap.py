#!/usr/bin/env python3
"""The object model: pointers, objects, and the heap they live in.

Three files share this week's runtime, and this is the one they agree on:

    heap.py     what an object is, what a pointer is, and the counters
    runtime.py  the interpreter, and where the roots come from
    collect.py  the three collectors

**Why this is its own module and not the top of runtime.py.**  `Ref` is
identified by `isinstance`, so every part of the system must mean the *same
class* by it.  Run `python3 runtime.py` and Python imports that file twice --
once as `__main__`, once as `runtime` when collect.py imports it -- producing
two unrelated `Ref` classes, one of which fails every isinstance check.  The
symptom is a reference counter that counts nothing, frees nothing, and
reports no error.  Putting the object model in a module that neither of the
others can be entry point for makes the question impossible to get wrong.

That is not a Python curiosity you can file away.  It is object identity
across compilation units, which is the same problem C++ solves with the
one-definition rule and Java solves with classloader identity -- and which,
in a garbage collector, decides whether a word is a pointer.
"""

WORD = 8            # bytes, matching CS 201's x86-64


class Ref:
    """A pointer.

    Distinguishable from an int by its type, which is the whole point: a
    *precise* collector never has to guess whether a word is an address.
    A conservative collector -- Boehm's, and every collector for a language
    that compiles to untyped machine words -- does have to guess, and L14
    section 6 measures what the guess costs.
    """

    __slots__ = ('addr',)

    def __init__(self, addr):
        self.addr = addr

    def __repr__(self):
        return f"#{self.addr}"

    def __eq__(self, o):
        return isinstance(o, Ref) and o.addr == self.addr

    def __hash__(self):
        return hash(('ref', self.addr))


class Obj:
    """One heap object.

    `slots` maps field name -> value for a struct and index -> value for an
    array.  Both are dicts, so a collector walks either one the same way and
    never needs to know which it has.

    `words` is the size in machine words: one header plus one per slot.  The
    header is where a real runtime puts the type pointer, the mark bit, and
    the generation -- here they are Python attributes, but the space is
    counted honestly, because "how much did we save" is a question about
    bytes and PS 6 Part D asks it.
    """

    __slots__ = ('addr', 'kind', 'tyname', 'slots', 'words', 'born', 'gen',
                 'survived', 'marked')

    def __init__(self, addr, kind, tyname, slots, words, born):
        self.addr, self.kind, self.tyname = addr, kind, tyname
        self.slots, self.words, self.born = slots, words, born
        self.gen = 0
        self.survived = 0
        self.marked = False

    @property
    def nbytes(self):
        return self.words * WORD

    def refs(self):
        """Every address this object points at.  The collector's only view
        into an object -- note it never looks at the ints."""
        for v in self.slots.values():
            if isinstance(v, Ref):
                yield v.addr

    def __repr__(self):
        body = ', '.join(f"{k}={v!r}" for k, v in self.slots.items())
        return f"#{self.addr} {self.tyname}{{{body}}}"


class UseAfterFree(Exception):
    """Raised when the program dereferences an address the collector freed.

    A real runtime does not raise this.  It reads whatever is now at that
    address and carries on, which is why use-after-free is a security bug
    and not a crash.  We raise, because a course in which the collector's
    mistakes are silent would teach the wrong lesson twice.
    """

    def __init__(self, addr):
        super().__init__(f"#{addr} was freed, and the program still has a "
                         f"pointer to it")
        self.addr = addr


class Heap:
    """Addresses, objects, and every counter this week's measurements read."""

    def __init__(self):
        self.objs = {}
        self.next_addr = 1
        self.clock = 0              # allocation sequence number
        self.total_allocs = 0
        self.total_bytes = 0
        self.freed_objs = 0
        self.freed_bytes = 0
        self.peak_objs = 0
        self.peak_bytes = 0
        self.lifetimes = []         # (bytes allocated between birth and death)

    @property
    def live_objs(self):
        return len(self.objs)

    @property
    def live_bytes(self):
        return sum(o.nbytes for o in self.objs.values())

    def alloc(self, kind, tyname, slots, words):
        a = self.next_addr
        self.next_addr += 1
        self.clock += 1
        self.objs[a] = Obj(a, kind, tyname, slots, words, self.clock)
        self.total_allocs += 1
        self.total_bytes += words * WORD
        self.peak_objs = max(self.peak_objs, len(self.objs))
        self.peak_bytes = max(self.peak_bytes, self.live_bytes)
        return Ref(a)

    def free(self, addr):
        o = self.objs.pop(addr)
        self.freed_objs += 1
        self.freed_bytes += o.nbytes
        # Age is measured in allocations, not seconds.  "Most objects die
        # young" is a claim about how much *allocation* happens in an
        # object's lifetime, and that is the number a collector can act on.
        self.lifetimes.append(self.clock - o.born)
        return o

    def get(self, addr):
        o = self.objs.get(addr)
        if o is None:
            raise UseAfterFree(addr)
        return o

    def survivors(self):
        """Objects still live, oldest first.  Used by the lifetime report."""
        return sorted(self.objs.values(), key=lambda o: o.born)
