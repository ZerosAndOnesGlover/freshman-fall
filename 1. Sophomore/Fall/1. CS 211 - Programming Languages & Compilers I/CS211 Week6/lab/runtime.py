#!/usr/bin/env python3
"""A runtime for Cyan: an interpreter with a real heap.

Phase 8 of the eight, and the first one that is not a compiler phase at all.

Everything before this week produced a *representation*.  The lexer produced
tokens, the parser a tree, the checker a typed tree, tac.py three-address
code, opt.py a smaller version of it, regalloc.py an assignment of variables
to registers.  Nothing ever ran.  That was fine while the questions were
about form -- but `alloc` is not a question about form.  It is a request for
memory, and until something executes it there is no memory to ask about.

So this file executes TAC.  It keeps a heap of objects, hands out addresses,
and -- crucially -- it can be asked, at any instruction, "which addresses can
this program still reach?"  That question is the root set, and answering it
is what collect.py needs from us.  The object model itself lives in heap.py;
read that file's docstring for why it is not the top of this one.

Three root policies ship here, because which one you pick is not a detail:

    'scope'  -- every value in every frame.  Always safe, always keeps more
                than it must.  This is what a naive interpreter does.
    'live'   -- Week 5's liveness at the current instruction.  Precise.
                Frees more, and needs the SLOTS table to be right.
    'week4'  -- liveness computed from Week 4's `Instr.uses()`.  Included so
                that Lab 6 can watch a reachable object get collected.

The third one is not a straw man.  It is the same def/use bug you fixed in
Week 5, moved one phase later, and its symptom changes from "the optimiser
deletes an instruction" to "the collector frees an object the program is
still holding".  Same cause.  Much worse failure.
"""
import sys, os, time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lexer import LexError
from parser import parse, ParseError
from typecheck import Checker, TypeError_
from tac import TAC, Instr, build_cfg
from heap import WORD, Ref, Obj, Heap, UseAfterFree
import live as L


# --------------------------------------------------------------- liveness
#
# live.py computes liveness with the SLOTS table.  Week 4 computed def/use
# from the shape of the operand.  Both are wanted here, so the analysis is
# written once over an injected model.
#
def _defs4(ins):
    return {ins.dst} if isinstance(ins.dst, str) else set()


def _uses4(ins):
    return set(ins.uses())


MODELS = {
    'live':  (L.defs, L.uses),
    'week4': (_defs4, _uses4),
}


def liveness_with(blocks, model):
    """live.py's fixed point, parameterised by the def/use model."""
    defs, uses = model
    IN = {b.name: set() for b in blocks}
    OUT = {b.name: set() for b in blocks}

    ud = {}
    for b in blocks:
        used, defd = set(), set()
        for ins in b.instrs:
            used |= uses(ins) - defd
            defd |= defs(ins)
        ud[b.name] = (used, defd)

    while True:
        changed = False
        for b in reversed(blocks):
            out = set()
            for s in b.succs:
                out |= IN[s.name]
            use, dfn = ud[b.name]
            inn = use | (out - dfn)
            if out != OUT[b.name] or inn != IN[b.name]:
                OUT[b.name], IN[b.name] = out, inn
                changed = True
        if not changed:
            return IN, OUT


def live_after_map(blocks, model):
    """id(instruction) -> the set of variables live immediately AFTER it.

    That is the set a collector must treat as roots if it stops at that
    instruction: what is live *after* the current instruction is what the
    rest of the program can still read.
    """
    defs, uses = model
    _, OUT = liveness_with(blocks, model)
    m = {}
    for b in blocks:
        live = set(OUT[b.name])
        for ins in reversed(b.instrs):
            m[id(ins)] = set(live)
            live = uses(ins) | (live - defs(ins))
    return m


# ---------------------------------------------------------------- program
class Fn:
    def __init__(self, decl, code, blocks):
        self.decl, self.code, self.blocks = decl, code, blocks
        self.name = decl.name
        self.params = [p for p, _ in decl.params]
        self.labels = {ins.label: i for i, ins in enumerate(code)
                       if ins.op == 'label'}
        self.live = {}          # policy -> id(instr) -> live set

    def live_map(self, policy):
        if policy not in self.live:
            self.live[policy] = live_after_map(self.blocks, MODELS[policy])
        return self.live[policy]


class Program:
    def __init__(self, fns, structs):
        self.fns, self.structs = fns, structs


def compile_program(src):
    """Every function, not just one.  tac.py's `compile_fn` picks a single
    function because Weeks 4 and 5 only ever looked at one; a runtime has to
    be able to call the others."""
    ast = parse(src)
    c = Checker()
    c.check_program(ast)
    fns = {}
    for d in ast.decls:
        if d.kind == 'Fn':
            t = TAC()
            t.gen_fn(d)
            L.check_coverage(t.code)
            fns[d.name] = Fn(d, t.code, build_cfg(t.code))
    return Program(fns, c.structs)


# ------------------------------------------------------------------ frames
class Frame:
    __slots__ = ('fn', 'env', 'pc', 'call_site')

    def __init__(self, fn, args):
        self.fn = fn
        self.env = dict(zip(fn.params, args))
        self.pc = 0
        self.call_site = None


class Machine:
    """The interpreter.

    `collector` is anything with the six hooks in collect.py's Collector.  Pass
    None to run with no collector at all, which is what the compiler has
    been doing for two weeks: allocate, never free, and see how far you get.
    """

    def __init__(self, prog, collector=None, roots='live', trace=False,
                 max_steps=20_000_000):
        self.prog = prog
        self.gc = collector
        self.roots_policy = roots
        self.trace = trace
        self.heap = Heap()
        self.frames = []
        self.steps = 0
        self.max_steps = max_steps
        self.gc_events = []
        if collector is not None:
            collector.attach(self)

    # ------------------------------------------------------------- roots
    def root_names(self, f):
        """The variables of frame `f` that are roots at its current pc.

        Names, not addresses -- because a *moving* collector has to write the
        new address back into the frame, and it cannot do that with an
        address alone.  This is the concrete form of L14 section 5's point:
        being able to identify a pointer is what lets you relocate it, and
        being able to find where the pointer is *stored* is the other half.
        """
        if self.roots_policy == 'scope':
            return set(f.env)
        ins = f.fn.code[f.pc] if f.pc < len(f.fn.code) else None
        if ins is None:
            return set()
        return set(f.fn.live_map(self.roots_policy).get(id(ins), ()))

    def roots(self):
        """Every heap address the running program can still reach directly.

        Reachability *through* the heap is the collector's job.  This is only
        the boundary: the addresses held in frames.
        """
        out = set()
        for f in self.frames:
            for n in self.root_names(f):
                v = f.env.get(n)
                if isinstance(v, Ref):
                    out.add(v.addr)
        return out

    def each_root_slot(self):
        """(frame, name, address) for every root, so a moving collector can
        assign a new address back into `frame.env[name]`."""
        for f in self.frames:
            for n in self.root_names(f):
                v = f.env.get(n)
                if isinstance(v, Ref):
                    yield f, n, v.addr

    # ------------------------------------------------------------ values
    def val(self, f, x):
        """Resolve an operand.  A str is a variable name; anything else is a
        literal that tac.py put directly in the slot (an array index, an
        array length, a constant)."""
        if isinstance(x, str):
            if x not in f.env:
                raise KeyError(f"{f.fn.name}: read of undefined '{x}'")
            return f.env[x]
        return x

    def setvar(self, f, name, value):
        """Every write to a variable goes through here, so that a reference
        counter can see it.  A tracing collector does not care."""
        if self.gc is not None:
            self.gc.on_var_write(f.env.get(name), value)
        f.env[name] = value

    def write_slot(self, obj, key, value):
        """Every write into the heap goes through here, so that a reference
        counter can adjust counts and a generational collector can run its
        write barrier."""
        if self.gc is not None:
            self.gc.on_heap_write(obj, obj.slots.get(key), value)
        obj.slots[key] = value

    # --------------------------------------------------------------- run
    def run(self, entry, args=()):
        fn = self.prog.fns[entry]
        self.frames.append(Frame(fn, list(args)))
        result = None
        while self.frames:
            f = self.frames[-1]
            if f.pc >= len(f.fn.code):
                result = self.pop_frame(None)
                continue
            ins = f.fn.code[f.pc]
            self.steps += 1
            if self.steps > self.max_steps:
                raise RuntimeError("step limit exceeded")
            if self.trace:
                print(f"  [{f.fn.name}:{f.pc}] {ins!r}", file=sys.stderr)
            r = self.step(f, ins)
            if r is not None:
                result = r
        return result

    def pop_frame(self, value):
        f = self.frames.pop()
        if self.gc is not None:
            self.gc.on_frame_exit(f)
        if self.frames:
            caller = self.frames[-1]
            site = caller.fn.code[caller.pc]
            if site.dst is not None:
                self.setvar(caller, site.dst, value)
            caller.pc += 1
            return None
        return value

    def step(self, f, ins):
        op = ins.op
        if op == 'label':
            f.pc += 1
        elif op == 'const':
            self.setvar(f, ins.dst, ins.a)
            f.pc += 1
        elif op == 'copy':
            self.setvar(f, ins.dst, self.val(f, ins.a))
            f.pc += 1
        elif op == 'unary':
            v = self.val(f, ins.b)
            self.setvar(f, ins.dst, -v if ins.a == '-' else (not v))
            f.pc += 1
        elif op == 'goto':
            f.pc = f.fn.labels[ins.label]
        elif op == 'ifz':
            f.pc = (f.fn.labels[ins.label] if not self.val(f, ins.a)
                    else f.pc + 1)
        elif op == 'iftrue':
            f.pc = (f.fn.labels[ins.label] if self.val(f, ins.a)
                    else f.pc + 1)
        elif op == 'ret':
            return self.pop_frame(self.val(f, ins.a)
                                  if ins.a is not None else None)
        elif op == 'call':
            callee = self.prog.fns.get(ins.a)
            if callee is None:
                raise RuntimeError(f"no such function: {ins.a}")
            args = [self.val(f, x) for x in ins.b]
            self.frames.append(Frame(callee, args))
        elif op == 'alloc':
            fields = self.prog.structs[ins.a]
            slots = {name: None for name in fields}
            r = self.allocate('struct', ins.a, slots, 1 + len(fields))
            self.setvar(f, ins.dst, r)
            f.pc += 1
        elif op == 'newarr':
            n = ins.a
            r = self.allocate('array', f"[{n}]", {i: None for i in range(n)},
                              1 + n)
            self.setvar(f, ins.dst, r)
            f.pc += 1
        elif op == 'getfield':
            o = self.deref(self.val(f, ins.a))
            self.setvar(f, ins.dst, o.slots[ins.b])
            f.pc += 1
        elif op == 'setfield':
            o = self.deref(self.val(f, ins.dst))
            self.write_slot(o, ins.a, self.val(f, ins.b))
            f.pc += 1
        elif op == 'load':
            o = self.deref(self.val(f, ins.a))
            i = self.val(f, ins.b)
            if i not in o.slots:
                raise RuntimeError(f"index {i} out of range for {o.tyname}")
            self.setvar(f, ins.dst, o.slots[i])
            f.pc += 1
        elif op == 'store':
            o = self.deref(self.val(f, ins.dst))
            i = self.val(f, ins.a)
            if i not in o.slots:
                raise RuntimeError(f"index {i} out of range for {o.tyname}")
            self.write_slot(o, i, self.val(f, ins.b))
            f.pc += 1
        elif op == 'phi':
            raise RuntimeError("phi is not executable -- it is a note to the "
                               "compiler, and must be destroyed before "
                               "codegen (L10 section 5)")
        else:
            a, b = self.val(f, ins.a), self.val(f, ins.b)
            self.setvar(f, ins.dst, ARITH[op](a, b))
            f.pc += 1
        return None

    def deref(self, r):
        if not isinstance(r, Ref):
            raise RuntimeError(f"not a pointer: {r!r}")
        return self.heap.get(r.addr)

    def allocate(self, kind, tyname, slots, words):
        if self.gc is not None:
            self.gc.before_alloc(words * WORD)
        r = self.heap.alloc(kind, tyname, slots, words)
        if self.gc is not None:
            self.gc.after_alloc(self.heap.objs[r.addr])
        return r


def _div(a, b):
    """Truncating division, as in C and as in Week 4's folder -- NOT Python's
    floor division.  Quiz 5 question 6 is about this exact line."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


ARITH = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': _div,
    '%': lambda a, b: a - _div(a, b) * b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
}


# ----------------------------------------------------------------- report
def lifetime_report(m, buckets=(1, 2, 4, 8, 16, 32, 64, 128, 256)):
    """How old were objects when they died, in allocations?

    The generational hypothesis is the claim that this histogram is
    front-loaded -- that most objects are young at death.  It is an empirical
    claim about programs, not a theorem, and it is the entire justification
    for a collector that looks at some objects more often than others.  So
    measure it rather than quoting it.

    Age is counted in ALLOCATIONS, not seconds and not instructions.  That is
    the clock a collector actually runs on: a minor collection happens after
    so many bytes have been handed out, so "how much allocation did this
    object survive" is the number that decides whether it gets scanned again.
    """
    ages = m.heap.lifetimes
    if not ages:
        print("; ---- no object was ever freed; nothing to measure ----")
        return
    print(f"; ---- age at death, {len(ages)} objects "
          f"(age = allocations survived) ----")
    prev = 0
    cum = 0
    for b in buckets:
        n = sum(1 for a in ages if prev <= a < b)
        cum += n
        if n or prev == 0:
            bar = '#' * min(48, round(48 * n / len(ages)))
            print(f"  {prev:>4} <= age < {b:<5} {n:>6}  "
                  f"{100 * cum / len(ages):>5.1f}% cum  {bar}")
        prev = b
    n = sum(1 for a in ages if a >= prev)
    if n:
        bar = '#' * min(48, round(48 * n / len(ages)))
        print(f"  {prev:>4} <= age        {n:>6}  100.0% cum  {bar}")
    ages_sorted = sorted(ages)
    med = ages_sorted[len(ages_sorted) // 2]
    print(f"  median age {med}   mean {sum(ages) / len(ages):.1f}   "
          f"max {max(ages)}")


def report(m, label=""):
    h = m.heap
    print(f"; ---- heap{' ' + label if label else ''} ----")
    print(f"  allocated   {h.total_allocs:>8} objects   "
          f"{h.total_bytes:>9} bytes")
    print(f"  freed       {h.freed_objs:>8} objects   "
          f"{h.freed_bytes:>9} bytes")
    print(f"  still live  {h.live_objs:>8} objects   "
          f"{h.live_bytes:>9} bytes")
    print(f"  peak live   {h.peak_objs:>8} objects   "
          f"{h.peak_bytes:>9} bytes")
    if m.gc is not None:
        m.gc.report()


def main(argv):
    if len(argv) < 2:
        print("usage: runtime.py FILE.cy [FN] [ARGS...] "
              "[--gc=none|rc|mark|gen] [--roots=live|scope|week4] "
              "[--threshold=N] [--lifetimes] [--no-fixup] [--trace]",
              file=sys.stderr)
        return 2
    opts = {a.split('=')[0]: a.split('=', 1)[-1]
            for a in argv if a.startswith('--')}
    pos = [a for a in argv[1:] if not a.startswith('--')]

    try:
        src = open(pos[0]).read()
    except OSError as e:
        print(f"error: cannot read {pos[0]}: {e.strerror}", file=sys.stderr)
        return 2
    entry = pos[1] if len(pos) > 1 else None
    try:
        args = [int(x) for x in pos[2:]]
    except ValueError:
        print(f"error: arguments must be integers, got {pos[2:]}", file=sys.stderr)
        return 2

    prog = compile_program(src)
    if entry is None:
        entry = next(iter(prog.fns))
    if entry not in prog.fns:
        print(f"error: no function '{entry}' in {pos[0]}; "
              f"choose from {', '.join(prog.fns)}", file=sys.stderr)
        return 2

    import collect
    coll = collect.make(opts.get('--gc', 'none'),
                        threshold=int(opts.get('--threshold', 16)),
                        fixup='--no-fixup' not in opts)
    m = Machine(prog, coll, roots=opts.get('--roots', 'live'),
                trace='--trace' in opts)
    try:
        r = m.run(entry, args)
    except UseAfterFree as e:
        print(f"; ---- CRASH ----\n  {e}", file=sys.stderr)
        report(m, "at the crash")
        return 3
    print(f"; ---- {entry}({', '.join(map(str, args))}) = {r!r} ----")
    report(m)
    if '--lifetimes' in opts:
        lifetime_report(m)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except (LexError, ParseError, TypeError_) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
