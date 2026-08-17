#!/usr/bin/env python3
"""Dominators, natural loops, loop-invariant code motion, induction variables.

Nothing here knows what a `while` statement is.  The front end threw that
away in Week 4 -- by the time the optimiser runs there are only blocks and
edges, and a loop is a property of the GRAPH:

    a back edge is an edge n -> h where h dominates n,
    and the loop it heads is every node that can reach n without passing h.

That definition finds loops written with `goto`, loops the parser never saw
as loops, and loops produced by earlier optimisation passes.  A pass that
matched on the AST's `While` node would find none of them.

Fixed-point iteration, for the fourth time this term: epsilon-closure in
Week 1, FIRST/FOLLOW in Week 2, the folder in Week 4, and now dominators.
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tac import Instr, compile_fn, build_cfg, dump
from live import defs, uses, check_coverage, liveness, flatten


# ----------------------------------------------------------------- dominance
def dominators(blocks):
    """DOM[B] = {B} U (intersection of DOM[P] over predecessors P).

    The entry block is dominated only by itself.  Every other block starts
    at "dominated by everything" and shrinks -- a MUST analysis, so the
    merge is intersection and the initial value is the universe.  Compare
    liveness, which is a MAY analysis and therefore starts empty and grows.
    """
    names = [b.name for b in blocks]
    universe = set(names)
    entry = blocks[0]
    dom = {b.name: set(universe) for b in blocks}
    dom[entry.name] = {entry.name}

    rounds = 0
    while True:
        rounds += 1
        changed = False
        for b in blocks[1:]:
            new = set(universe)
            for p in b.preds:
                new &= dom[p.name]
            new.add(b.name)
            if new != dom[b.name]:
                dom[b.name] = new
                changed = True
        if not changed:
            return dom, rounds


def back_edges(blocks, dom):
    """Edges n -> h with h in DOM[n].  Each one heads a natural loop."""
    out = []
    for b in blocks:
        for s in b.succs:
            if s.name in dom[b.name]:
                out.append((b, s))
    return out


def natural_loop(tail, header):
    """{header} plus every node reaching `tail` without going through header."""
    body = {header.name, tail.name}
    stack = [tail] if tail is not header else []
    while stack:
        n = stack.pop()
        for p in n.preds:
            if p.name not in body:
                body.add(p.name)
                stack.append(p)
    return body


class Loop:
    def __init__(self, blocks, tail, header):
        by = {b.name: b for b in blocks}
        self.header = header
        self.tail = tail
        self.names = natural_loop(tail, header)
        self.blocks = [b for b in blocks if b.name in self.names]
        # An exit is a block IN the loop with a successor OUTSIDE it.
        self.exits = [b for b in self.blocks
                      if any(s.name not in self.names for s in b.succs)]

    def __repr__(self):
        return (f"<loop header={self.header.name} "
                f"body={sorted(self.names)} "
                f"exits={[b.name for b in self.exits]}>")


def find_loops(blocks):
    dom, _ = dominators(blocks)
    return [Loop(blocks, t, h) for t, h in back_edges(blocks, dom)], dom


# ------------------------------------------------------ loop-invariant motion
#
# An instruction is invariant in loop L when every variable it reads either
#   (a) has no definition inside L at all, or
#   (b) has exactly one definition inside L, and that definition is itself
#       already known invariant.
# Iterate to a fixed point, because (b) is recursive.
#
# Being invariant is NOT sufficient to hoist it.  See MOVABLE below.

# Opcodes that may be hoisted at all.  Everything omitted either has an
# effect the loop count is part of (`call`, `store`, `setfield`), reads
# memory that the loop may write (`load`, `getfield`), or is control flow.
#
# `/` and `%` are omitted DELIBERATELY and the reason is section 6 of L11:
# they can trap.  Hoisting `a / b` out of a loop that runs zero times
# executes a division the source program never performs, and if b is 0 the
# optimised program dies where the original returned.  An optimisation that
# turns a working program into a crashing one is not an optimisation.
MOVABLE = {'const', 'copy', 'unary', '+', '-', '*',
           '<', '<=', '>', '>=', '==', '!='}


def invariant_instrs(loop):
    """The instructions of `loop` that compute the same value every time."""
    defs_in_loop = {}
    for b in loop.blocks:
        for ins in b.instrs:
            for d in defs(ins):
                defs_in_loop.setdefault(d, []).append(ins)

    inv = set()          # ids of instructions proved invariant
    while True:
        changed = False
        for b in loop.blocks:
            for ins in b.instrs:
                if id(ins) in inv or ins.op not in MOVABLE:
                    continue
                ok = True
                for u in uses(ins):
                    ds = defs_in_loop.get(u, [])
                    if not ds:
                        continue                     # (a) defined outside
                    if len(ds) == 1 and id(ds[0]) in inv:
                        continue                     # (b) invariant already
                    ok = False
                    break
                if ok:
                    inv.add(id(ins))
                    changed = True
        if not changed:
            return inv, defs_in_loop


def hoistable(loop, inv, defs_in_loop, live_out):
    """Filter invariant instructions down to the ones it is SAFE to move.

    Dragon section 9.5.3, with the trap condition of L11 section 6 added:

      1. the instruction's block dominates every exit of the loop -- so the
         hoisted code runs exactly when the original would have.  If the
         loop can exit before reaching it, hoisting makes it run when the
         source says it should not.
      2. its destination has exactly one definition in the loop -- otherwise
         which of them is "the" value is undefined.
      3. it cannot trap -- enforced by MOVABLE, above.

    Condition 1 can be relaxed when the destination is dead after the loop,
    since then nobody can observe the extra execution.  We do not relax it:
    see PS 5 Part C, which asks you to, and asks what breaks.
    """
    dom = loop._dom
    out = []
    for b in loop.blocks:
        for ins in b.instrs:
            if id(ins) not in inv:
                continue
            if not all(b.name in dom[e.name] for e in loop.exits):
                continue                                        # (1)
            d = defs(ins)
            if len(d) != 1:
                continue
            (dst,) = tuple(d)
            if len(defs_in_loop.get(dst, [])) != 1:
                continue                                        # (2)
            out.append((b, ins))
    return out


def licm(blocks, code):
    """Hoist what is safe into a preheader.  Returns (new_code, log).

    The preheader is the point immediately before the header's `label`.
    That works because the back edge targets the LABEL, so it re-enters the
    loop below the hoisted code, while the entry path falls through it
    exactly once.  This holds for every loop `tac.py` generates; a loop with
    two entry edges from outside would need a real preheader block, and the
    assert below is what tells you when you have met one.
    """
    loops, dom = find_loops(blocks)
    log, hoisted = [], []
    for loop in loops:
        loop._dom = dom
        inv, dmap = invariant_instrs(loop)
        cand = hoistable(loop, inv, dmap, None)
        outside_preds = [p for p in loop.header.preds
                         if p.name not in loop.names]
        assert len(outside_preds) <= 1, \
            f"loop {loop.header.name} has {len(outside_preds)} entry edges; " \
            "it needs a real preheader block"
        log.append(f"{loop.header.name}: body={sorted(loop.names)} "
                   f"invariant={len(inv)} hoistable={len(cand)}")
        for b, ins in cand:
            log.append(f"  hoist  {repr(ins).strip()}")
            hoisted.append((loop.header.name, ins))

    if not hoisted:
        return code, log

    move = {id(i) for _, i in hoisted}
    out = []
    for ins in code:
        if ins.op == 'label':
            for hdr, hi in hoisted:
                if hdr == ins.label:
                    out.append(hi)
            out.append(ins)
            continue
        if id(ins) in move:
            continue
        out.append(ins)
    return out, log


# ------------------------------------------------------- induction variables
def basic_ivs(loop):
    """Variables updated by `i = i + c` (or `i - c`) exactly once per pass.

    Returns {name: step}.  These are the variables whose value is an affine
    function of the iteration number, which is what makes both strength
    reduction and Week 11's bounds-check elimination possible.
    """
    counts, cands = {}, {}
    for b in loop.blocks:
        for ins in b.instrs:
            for d in defs(ins):
                counts[d] = counts.get(d, 0) + 1

    # `i = i + 1` is never one instruction in our TAC.  gen_stmt lowers it to
    #     t11 = i + t10
    #     i   = t11
    # because the right-hand side is generated before the assignment knows
    # where it is going.  So the update we are looking for is a binary op
    # whose result is copied straight back into one of its own operands, and
    # the detector has to see through that copy.  A version that matched only
    # `i = i + c` finds no induction variable in ANY loop this compiler emits
    # -- which is what the first draft of this function did.
    writeback = {}          # temp -> variable it is copied into, inside L
    for b in loop.blocks:
        for ins in b.instrs:
            if ins.op == 'copy' and isinstance(ins.a, str):
                writeback[ins.a] = ins.dst

    for b in loop.blocks:
        for ins in b.instrs:
            if ins.op not in ('+', '-') or ins.dst is None:
                continue
            var = writeback.get(ins.dst)
            if var is None or counts.get(var) != 1 or counts.get(ins.dst) != 1:
                continue
            for operand, amt in ((ins.a, ins.b), (ins.b, ins.a)):
                if operand != var or not isinstance(amt, str):
                    continue
                k = _const_in(loop, amt)
                if k is None:
                    continue
                if ins.op == '-' and operand is ins.b:
                    continue        # `c - i` is not an induction update
                cands[var] = k if ins.op == '+' else -k
    return cands


def _const_in(loop, name):
    """The value of `name` if it is set by a single `const` in the loop."""
    found = None
    for b in loop.blocks:
        for ins in b.instrs:
            if ins.op == 'const' and ins.dst == name:
                if found is not None:
                    return None
                found = ins.a
    return found if isinstance(found, int) and not isinstance(found, bool) \
        else None


# ------------------------------------------------------------------- driver
if __name__ == '__main__':
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    which = sys.argv[2] if len(sys.argv) > 2 else None
    d, code, blocks = compile_fn(src, which)
    check_coverage(code)

    dom, rounds = dominators(blocks)
    print(f"; ---- dominators for {d.name} (fixed point after {rounds}) ----")
    for b in blocks:
        print(f"{b.name:10s} dom by {sorted(dom[b.name])}")

    loops, _ = find_loops(blocks)
    print(f"\n; ---- {len(loops)} natural loop(s) ----")
    for l in loops:
        print(f"  {l}")
        ivs = basic_ivs(l)
        print(f"    basic induction variables: {ivs or '-'}")

    new, log = licm(blocks, code)
    print(f"\n; ---- licm: {len(code)} -> {len(new)} in loop body ----")
    for l in log:
        print(f";  {l}")
    print()
    dump(new)
