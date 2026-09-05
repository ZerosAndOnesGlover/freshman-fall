#!/usr/bin/env python3
"""Three garbage collectors for the Cyan runtime.

    RefCount     -- count the pointers to each object; free at zero.
    MarkSweep    -- trace from the roots; free everything not reached.
    Generational -- trace the young objects only, most of the time.

They share one interface, which runtime.py calls at six points:

    attach(machine)                   once, at construction
    before_alloc(nbytes)              may collect; the only place we do
    after_alloc(obj)                  object exists, nothing points to it yet
    on_var_write(old, new)            a variable was rebound
    on_heap_write(obj, old, new)      a field or element was written
    on_frame_exit(frame)              a call returned; its locals are gone

Note which collectors need which hooks.  **MarkSweep implements two of the
six and ignores the rest.**  Reference counting needs every single one,
because it maintains an invariant continuously; tracing needs almost none,
because it reconstructs the answer from scratch at a point of its choosing.

That asymmetry is the whole trade, and it is not primarily about speed:

    reference counting  pays a little on every pointer write, forever,
                        and answers "is this garbage?" immediately.
    tracing             pays nothing on writes, and answers the question
                        all at once, at a time the program did not choose.

Everything else in this file -- generations, barriers, promotion -- is an
attempt to have both.

**A name that matters.** This module is called `collect`, not `gc`.  Naming
it `gc.py` would put it ahead of CPython's own `gc` module on `sys.path`,
and Lab 6 Part C measures CPython's cycle collector.  Shadowing it would
make that measurement quietly impossible.
"""
import time
from heap import Ref, WORD


class Collector:
    """The no-op collector.  Also the base class, and also exactly what the
    compiler has had since Week 4: allocation with no reclamation."""

    name = 'none'

    def attach(self, machine):
        self.m = machine
        self.heap = machine.heap
        self.collections = 0
        self.pauses = []            # seconds, one per collection
        self.scanned = 0            # objects visited by a trace
        self.barrier_hits = 0       # write-barrier invocations
        self.barrier_records = 0    # of those, the ones that recorded
        # Live bytes immediately AFTER each collection.  "Residency" is the
        # honest footprint number: peak live is capped by whatever triggers a
        # collection, so a collector that retains garbage does not show up in
        # the peak -- it shows up here, and in how often it has to run.
        self.residency = []

    def before_alloc(self, nbytes):
        pass

    def after_alloc(self, obj):
        pass

    def on_var_write(self, old, new):
        pass

    def on_heap_write(self, obj, old, new):
        pass

    def on_frame_exit(self, frame):
        pass

    # ------------------------------------------------------------ reports
    def report(self):
        print(f"  collector   {self.name}")
        if self.collections:
            tot = sum(self.pauses)
            print(f"  collections {self.collections:>8}          "
                  f"{tot * 1e3:>8.2f} ms total")
            print(f"  longest     {max(self.pauses) * 1e6:>8.1f} us"
                  f"          {self.scanned:>7} objects scanned")
        if self.residency:
            print(f"  residency   {sum(self.residency) / len(self.residency):>8.0f} bytes mean"
                  f"     {max(self.residency):>7} bytes worst")
        if self.barrier_hits:
            print(f"  barrier     {self.barrier_hits:>8} writes    "
                  f"{self.barrier_records:>7} recorded")


# ------------------------------------------------------------- refcounting
class RefCount(Collector):
    """Immediate reclamation, and the one collector that can be wrong.

    The count on an object is the number of pointers to it: from variables
    and from other objects' fields.  When it reaches zero nothing can reach
    the object, so it is freed -- and freeing it drops the counts of
    everything it pointed at, which may free those too.

    "Nothing can reach it" is where this goes wrong.  A count of zero proves
    unreachability.  **A count above zero does not prove reachability.**  Two
    objects that point at each other hold each other's count at one, and
    neither is reachable from anywhere.  L13 section 8.
    """

    name = 'refcount'

    def attach(self, machine):
        super().attach(machine)
        self.count = {}
        self.freed_by_zero = 0

    def after_alloc(self, obj):
        # Zero, not one.  The `alloc` instruction stores the result into a
        # variable immediately afterwards, and that store is what takes the
        # first reference.  Starting at one would leak every object by
        # exactly one count.
        self.count[obj.addr] = 0

    def incref(self, v):
        if isinstance(v, Ref):
            self.count[v.addr] = self.count.get(v.addr, 0) + 1

    def decref(self, v):
        """Drop one reference, and free transitively if that was the last.

        The worklist is not decoration.  Dropping the head of a
        thousand-element list frees all thousand, and a recursive
        implementation would recurse a thousand deep to do it -- which is
        how CPython's deallocator used to overflow the C stack on long
        lists.
        """
        if not isinstance(v, Ref):
            return
        work = [v.addr]
        while work:
            a = work.pop()
            n = self.count.get(a, 0) - 1
            self.count[a] = n
            if n > 0:
                continue
            if a not in self.heap.objs:
                continue
            obj = self.heap.objs[a]
            for child in list(obj.slots.values()):
                if isinstance(child, Ref):
                    work.append(child.addr)
            self.heap.free(a)
            self.count.pop(a, None)
            self.freed_by_zero += 1

    # Increment before decrement, always.  `x = x` must not free the object
    # between the two operations.
    def on_var_write(self, old, new):
        self.incref(new)
        self.decref(old)

    def on_heap_write(self, obj, old, new):
        self.incref(new)
        self.decref(old)

    def on_frame_exit(self, frame):
        for v in list(frame.env.values()):
            self.decref(v)

    def report(self):
        super().report()
        print(f"  freed at rc=0            {self.freed_by_zero:>8} objects")
        stuck = [a for a, n in self.count.items()
                 if n > 0 and a in self.heap.objs]
        if stuck:
            print(f"  still counted            {len(stuck):>8} objects  "
                  f"<- unreachable if this is the end of the program")


# -------------------------------------------------------------- mark-sweep
class MarkSweep(Collector):
    """Tracing.  Two phases, three colours.

    White -- not yet reached.  Grey -- reached, children not yet scanned.
    Black -- reached, children scanned.  Start with the roots grey and
    everything else white; repeatedly take a grey object, blacken it, and
    grey its white children; when no grey objects remain, every white object
    is garbage.

    The invariant that makes this correct is: **no black object ever points
    to a white object.**  In a stop-the-world collector it holds for free,
    because the program is not running and cannot create such a pointer.
    L14 section 7 is about what it costs to keep it true when the program
    *is* running.
    """

    name = 'mark-sweep'

    def __init__(self, threshold=16):
        self.threshold = threshold

    def before_alloc(self, nbytes):
        if self.heap.live_objs >= self.threshold:
            self.collect()

    def collect(self):
        t0 = time.perf_counter()
        black = set()
        grey = list(self.m.roots())
        scanned = 0
        while grey:
            a = grey.pop()
            if a in black:
                continue
            black.add(a)
            scanned += 1
            obj = self.heap.objs.get(a)
            if obj is None:
                continue                    # a root into freed memory
            for c in obj.refs():
                if c not in black:
                    grey.append(c)

        dead = [a for a in self.heap.objs if a not in black]
        for a in dead:
            self.heap.free(a)

        self.collections += 1
        self.scanned += scanned
        self.residency.append(self.heap.live_bytes)
        self.pauses.append(time.perf_counter() - t0)
        return len(dead)


# ------------------------------------------------------------ generational
class Generational(Collector):
    """Two generations, a write barrier, and a remembered set.

    The bet: most objects die young.  If that is true, a collection that
    looks only at young objects finds almost all of the garbage for a
    fraction of the work.

    The cost of the bet is the barrier.  A minor collection must not free a
    young object that an *old* object points to -- and it never scans old
    objects, so it would not see the pointer.  So every heap write is
    inspected, and every old->young pointer is recorded.  The remembered set
    is then treated as an extra source of roots.

    **The subtle case is promotion, not writes.**  A young object that
    points to another young object creates no barrier record -- correctly,
    since both are scanned.  Promote the parent and that pointer becomes an
    unrecorded old->young pointer.  `_promote` handles it, and getting this
    wrong produces a collector that works on every small test and frees live
    objects under load.
    """

    name = 'generational'

    def __init__(self, threshold=16, promote_after=2, major_every=8,
                 fixup=True):
        self.threshold = threshold
        self.promote_after = promote_after
        self.major_every = major_every
        # Set False to remove the promotion fix-up in `_promote` and nothing
        # else.  The collector still passes every small test.  L14 section 8
        # and Lab 6 Part D.
        self.fixup = fixup

    def attach(self, machine):
        super().attach(machine)
        self.remembered = set()
        self.minors = 0
        self.majors = 0
        self.promoted = 0
        self.minor_pauses = []
        self.major_pauses = []

    def before_alloc(self, nbytes):
        young = sum(1 for o in self.heap.objs.values() if o.gen == 0)
        if young >= self.threshold:
            if self.minors and self.minors % self.major_every == 0:
                self.major()
            else:
                self.minor()

    # --------------------------------------------------------- the barrier
    def on_heap_write(self, obj, old, new):
        self.barrier_hits += 1
        if obj.gen == 1 and isinstance(new, Ref):
            child = self.heap.objs.get(new.addr)
            if child is not None and child.gen == 0:
                self.remembered.add(obj.addr)
                self.barrier_records += 1

    # ------------------------------------------------------------ minor GC
    def minor(self):
        t0 = time.perf_counter()
        black, scanned = set(), 0

        grey = [a for a in self.m.roots()
                if a in self.heap.objs and self.heap.objs[a].gen == 0]
        # The remembered set contributes its young children as roots.  Note
        # we do not scan the old object itself -- only the pointers out of
        # it that the barrier told us about.
        stale = set()
        for a in self.remembered:
            o = self.heap.objs.get(a)
            if o is None:
                stale.add(a)
                continue
            kids = [c for c in o.refs()
                    if c in self.heap.objs and self.heap.objs[c].gen == 0]
            if not kids:
                stale.add(a)
            grey.extend(kids)
        self.remembered -= stale

        while grey:
            a = grey.pop()
            if a in black:
                continue
            black.add(a)
            scanned += 1
            o = self.heap.objs.get(a)
            if o is None:
                continue
            for c in o.refs():
                # Traversal stops at the old generation.  That is the entire
                # saving, and the entire reason the barrier has to exist.
                oc = self.heap.objs.get(c)
                if oc is not None and oc.gen == 0 and c not in black:
                    grey.append(c)

        dead = [a for a, o in self.heap.objs.items()
                if o.gen == 0 and a not in black]
        for a in dead:
            self.heap.free(a)
        self.remembered -= set(dead)

        for a in black:
            o = self.heap.objs.get(a)
            if o is None or o.gen != 0:
                continue
            o.survived += 1
            if o.survived >= self.promote_after:
                self._promote(o)

        self.minors += 1
        self.collections += 1
        self.scanned += scanned
        self.residency.append(self.heap.live_bytes)
        dt = time.perf_counter() - t0
        self.pauses.append(dt)
        self.minor_pauses.append(dt)
        return len(dead)

    def _promote(self, o):
        o.gen = 1
        self.promoted += 1
        # See the class docstring.  This object's young children were never
        # barriered, because when the pointers were written both ends were
        # young.  They are old->young pointers now.
        if not self.fixup:
            return
        if any(self.heap.objs[c].gen == 0
               for c in o.refs() if c in self.heap.objs):
            self.remembered.add(o.addr)

    # ------------------------------------------------------------ major GC
    def major(self):
        t0 = time.perf_counter()
        black, scanned = set(), 0
        grey = list(self.m.roots())
        while grey:
            a = grey.pop()
            if a in black:
                continue
            black.add(a)
            scanned += 1
            o = self.heap.objs.get(a)
            if o is None:
                continue
            grey.extend(c for c in o.refs() if c not in black)

        dead = [a for a in self.heap.objs if a not in black]
        for a in dead:
            self.heap.free(a)
        self.remembered -= set(dead)

        self.majors += 1
        self.collections += 1
        self.scanned += scanned
        self.residency.append(self.heap.live_bytes)
        dt = time.perf_counter() - t0
        self.pauses.append(dt)
        self.major_pauses.append(dt)
        return len(dead)

    def report(self):
        super().report()
        print(f"  minor       {self.minors:>8}          "
              f"{sum(self.minor_pauses) * 1e3:>8.2f} ms")
        print(f"  major       {self.majors:>8}          "
              f"{sum(self.major_pauses) * 1e3:>8.2f} ms")
        if self.minor_pauses:
            print(f"  mean minor  {sum(self.minor_pauses) / len(self.minor_pauses) * 1e6:>8.1f} us"
                  f"          {self.promoted:>7} promoted")
        if self.major_pauses:
            print(f"  mean major  {sum(self.major_pauses) / len(self.major_pauses) * 1e6:>8.1f} us"
                  f"          {len(self.remembered):>7} remembered at exit")


COLLECTORS = {
    'none': Collector,
    'rc': RefCount,
    'mark': MarkSweep,
    'gen': Generational,
}


def make(kind, threshold=16, fixup=True):
    cls = COLLECTORS.get(kind)
    if cls is None:
        raise SystemExit(f"unknown collector '{kind}'; "
                         f"choose from {', '.join(COLLECTORS)}")
    if cls is Generational:
        return cls(threshold=threshold, fixup=fixup)
    if cls is MarkSweep:
        return cls(threshold=threshold)
    return cls()
