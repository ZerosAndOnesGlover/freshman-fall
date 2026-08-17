#!/usr/bin/env python3
"""Live-variable analysis, and the dead-code elimination it makes honest.

Week 4's `dead_code` in opt.py scanned backwards through the flat instruction
list and kept anything whose destination it had already seen read.  That is
not liveness.  It is a guess that happens to be right on straight-line code,
and Week 5 opens by showing you what it costs when the code is not straight.

Two things are wrong with it, and both trace to `Instr.uses()`:

  1.  `store` and `setfield` READ their `dst` -- `a[i] = v` reads the array
      `a` in order to write into it.  `uses()` reports only `a` and `b`, so
      the array operand looks dead and the instruction that computed it gets
      deleted.  This is unsafe: it removes code that is needed.
  2.  `getfield`, `setfield` and `alloc` carry a field or type NAME in an
      operand slot.  `uses()` decides what is a variable by asking whether
      the string is an identifier, so `p.x` reports a use of a variable `x`
      that does not exist.  This is merely conservative for DCE -- but it
      invents interference edges in Week 5's register allocator, and there
      it costs you registers.

The fix is not a cleverer heuristic.  It is to stop guessing from the SHAPE
of an operand and write down, per opcode, which slots are defs and which are
uses.  That is DEFS/USES below, and everything in this file and in
regalloc.py reads it.
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tac import Instr, compile_fn, build_cfg, dump


# --------------------------------------------------------------- def and use
#
# For each opcode: (defs, uses) as tuples of slot names.  A slot holds a
# variable only if it is listed here; anything else in that slot is a
# literal, a label, an operator, a field name or a type name.
#
#   'dst', 'a', 'b'  -- the slot holds one operand
#   'b*'             -- the slot holds a LIST of operands (call arguments,
#                       phi arguments)
#
SLOTS = {
    'label':    ((),      ()),
    'goto':     ((),      ()),
    'const':    (('dst',), ()),
    'copy':     (('dst',), ('a',)),
    'unary':    (('dst',), ('b',)),        # `a` is the operator, not a var
    'call':     (('dst',), ('b*',)),       # `a` is the callee name
    'ret':      ((),      ('a',)),
    'ifz':      ((),      ('a',)),
    'iftrue':   ((),      ('a',)),
    'load':     (('dst',), ('a', 'b')),
    'store':    ((),      ('dst', 'a', 'b')),   # writes THROUGH dst, reads it
    'getfield': (('dst',), ('a',)),        # `b` is the field name
    'setfield': ((),      ('dst', 'b')),   # `a` is the field name
    'alloc':    (('dst',), ()),            # `a` is the type name
    'newarr':   (('dst',), ()),            # `a` is the length
    'phi':      (('dst',), ('b*',)),
}

# Binary arithmetic and comparison all share one shape.
for _op in ('+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!='):
    SLOTS[_op] = (('dst',), ('a', 'b'))


def _slot(ins, name):
    """Yield the variable names held in one slot, or nothing if it holds a
    literal.  A variable is a str; ints, bools and None are literals."""
    if name.endswith('*'):
        val = getattr(ins, name[:-1])
        if isinstance(val, list):
            for x in val:
                if isinstance(x, str):
                    yield x
        return
    val = getattr(ins, name)
    if isinstance(val, str):
        yield val


def defs(ins):
    """The set of variables this instruction writes."""
    d, _ = SLOTS.get(ins.op, ((), ()))
    return {x for n in d for x in _slot(ins, n)}


def uses(ins):
    """The set of variables this instruction reads."""
    _, u = SLOTS.get(ins.op, ((), ()))
    return {x for n in u for x in _slot(ins, n)}


def check_coverage(code):
    """Every opcode in `code` must appear in SLOTS.

    An unknown opcode would silently get empty def and use sets, which makes
    liveness under-approximate and DCE unsafe.  Fail loudly instead.
    """
    unknown = {ins.op for ins in code} - set(SLOTS)
    if unknown:
        raise KeyError(f"no def/use entry for opcode(s): {sorted(unknown)}")


# ------------------------------------------------------------ block liveness
#
# Backward, may-analysis.  "May" because a variable is live if there EXISTS
# some path to a use, so the merge over successors is union -- Week 4's L10
# section 7 in the general form, instantiated here.
#
#     OUT[B] = union of IN[S] for every successor S
#     IN[B]  = use[B] union (OUT[B] - def[B])
#
def block_use_def(b):
    """use[B] = read before any write in B.  def[B] = written anywhere in B."""
    used, defd = set(), set()
    for ins in b.instrs:
        used |= uses(ins) - defd
        defd |= defs(ins)
    return used, defd


def liveness(blocks):
    """Iterate IN/OUT to a fixed point.  Returns (IN, OUT, rounds)."""
    IN = {b.name: set() for b in blocks}
    OUT = {b.name: set() for b in blocks}
    ud = {b.name: block_use_def(b) for b in blocks}

    rounds = 0
    while True:
        rounds += 1
        changed = False
        # Backward analyses converge faster over reverse order, exactly as
        # forward ones do over forward order.  Correctness does not depend
        # on the order; only the round count does.
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
            return IN, OUT, rounds


def live_points(b, out_set):
    """Live-OUT at every instruction of block `b`, given live-OUT of `b`.

    Returns a list parallel to b.instrs.  Walk backwards, applying the same
    transfer function one instruction at a time:  live = use U (live - def).
    """
    live = set(out_set)
    points = [None] * len(b.instrs)
    for i in range(len(b.instrs) - 1, -1, -1):
        points[i] = set(live)
        ins = b.instrs[i]
        live = uses(ins) | (live - defs(ins))
    return points


# ---------------------------------------------------------- dead-code, again
SIDE_EFFECTS = {'call', 'store', 'setfield', 'ret', 'goto', 'ifz', 'iftrue',
                'label', 'alloc', 'newarr'}


def dce_live(blocks, params=(), keep_named=False):
    """Delete any instruction whose destination is not live afterwards.

    Unlike Week 4's version this needs no rule about names beginning with
    `t`.  Liveness tells us whether a named local is read on any path out;
    if it is not, the assignment goes.  `keep_named=True` restores the old
    timid behaviour so the lab can measure the difference.
    """
    _, OUT = liveness(blocks)[:2]
    removed = 0
    for b in blocks:
        pts = live_points(b, OUT[b.name])
        keep = []
        for ins, live_after in zip(b.instrs, pts):
            if ins.op in SIDE_EFFECTS:
                keep.append(ins); continue
            d = defs(ins)
            if keep_named and any(not x.startswith('t') for x in d):
                keep.append(ins); continue
            if d and not (d & live_after):
                removed += 1
                continue
            keep.append(ins)
        b.instrs = keep
    return removed


def flatten(blocks):
    return [ins for b in blocks for ins in b.instrs]


# ------------------------------------------------------------------- driver
def analyse(src, fname=None):
    d, code, blocks = compile_fn(src, fname)
    check_coverage(code)
    return d, code, blocks


if __name__ == '__main__':
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    which = sys.argv[2] if len(sys.argv) > 2 else None
    d, code, blocks = analyse(src, which)

    IN, OUT, rounds = liveness(blocks)
    print(f"; ---- liveness for {d.name}: fixed point after {rounds} rounds ----")
    for b in blocks:
        print(f"{b.name:10s} IN {sorted(IN[b.name])!s:34s} OUT {sorted(OUT[b.name])}")

    n = len(code)
    removed = dce_live(blocks)
    print(f"\n; ---- dce: {n} -> {n - removed} instructions "
          f"({removed} removed) ----")
    dump(flatten(blocks))
