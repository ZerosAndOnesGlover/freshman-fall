#!/usr/bin/env python3
"""Register allocation by graph colouring -- Chaitin's algorithm.

The TAC your compiler has been emitting since Week 4 uses an unbounded
supply of temporaries: t0, t1, t2, ... and it never reuses one.  A real
machine has sixteen general-purpose registers, and x86-64 lets you touch
about thirteen of them.  Something has to map the first onto the second.

The reduction is the elegant part, and it is pure graph theory:

    two variables may share a register  <=>  they are never live at the
    same time  <=>  they are not adjacent in the interference graph

so allocating k registers IS k-colouring the interference graph.  Optimal
colouring is NP-complete (Karp 1972), which sounds fatal until you notice
that compilers do not need optimal -- they need good, fast, and always
correct.  Chaitin's 1981 heuristic is all three:

    SIMPLIFY  a node with fewer than k neighbours can ALWAYS be coloured,
              whatever happens to the rest of the graph -- its neighbours
              cannot use up all k colours between them.  So remove it and
              push it on a stack; the graph gets smaller and easier.
    SPILL     if every remaining node has degree >= k, no node is trivially
              safe.  Pick one to keep in memory instead, remove it, carry
              on.  Which one you pick is the whole art.
    SELECT    pop the stack, giving each node a colour its already-coloured
              neighbours are not using.

The removal in SIMPLIFY is why this works: degrees only fall as nodes come
out, so a graph that looks uncolourable often is not.

Requires live.py -- interference is defined by liveness, so an error in the
def/use table becomes a wrong register assignment, which is the single
nastiest class of compiler bug there is.  See L12 section 4.
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tac import compile_fn
from live import defs, uses, check_coverage, liveness, live_points
from loops import find_loops


# --------------------------------------------------------- interference graph
def interference(blocks):
    """Nodes are variables; an edge means "never share a register".

    Built at definition points: when an instruction defines d, d interferes
    with everything still live after it, because that value must survive
    past the write.

    One exception, and it earns its keep.  For a move `x = y`, x and y hold
    the SAME value at that point, so they may share a register even though
    both are live.  Adding the edge anyway is not incorrect -- it just
    wastes a register.  Omitting it is what makes coalescing possible.
    """
    _, OUT, _ = liveness(blocks)
    graph = {}

    def node(v):
        graph.setdefault(v, set())

    for b in blocks:
        pts = live_points(b, OUT[b.name])
        for ins, live_after in zip(b.instrs, pts):
            for v in live_after:
                node(v)
            for d in defs(ins):
                node(d)
                others = set(live_after)
                if ins.op == 'copy':
                    others -= uses(ins)          # the move exception
                for v in others:
                    if v != d:
                        graph[d].add(v)
                        graph[v].add(d)
    return graph


# ------------------------------------------------------------- spill costing
def spill_costs(blocks):
    """How much it hurts to keep each variable in memory instead.

    Every reference costs a load or a store, and a reference inside a loop
    costs that once per iteration.  We do not know the trip count, so we use
    the classical stand-in: weight by 10 ** loop-nesting-depth.  Ten is
    arbitrary and everybody uses it; what matters is that it is much bigger
    than one, so an inner-loop variable is never spilled to save an outer one.

    This is where Week 5's two halves meet: L11's loop finder decides L12's
    register assignment.
    """
    depth = {b.name: 0 for b in blocks}
    loops, _ = find_loops(blocks)
    for l in loops:
        for name in l.names:
            depth[name] += 1

    cost = {}
    for b in blocks:
        w = 10 ** depth[b.name]
        for ins in b.instrs:
            for v in defs(ins) | uses(ins):
                cost[v] = cost.get(v, 0) + w
    return cost, depth


# --------------------------------------------------------- Chaitin's algorithm
def colour(graph, k, cost=None):
    """k-colour `graph`.  Returns (assignment, spilled, trace).

    `assignment` maps variable -> register number in range(k).
    `spilled` is the set that did not fit.
    `trace` records each decision, so the lab can watch it run.
    """
    work = {v: set(ns) for v, ns in graph.items()}
    stack, spilled, trace = [], set(), []

    while work:
        low = [v for v, ns in work.items() if len(ns) < k]
        if low:
            # Deterministic choice, so the trace is reproducible.
            v = sorted(low)[0]
            trace.append(f"simplify {v} (degree {len(work[v])} < {k})")
        else:
            # Every node is "significant".  Spill the one with the best
            # cost-to-degree ratio: cheap to spill, and frees many edges.
            def ratio(v):
                c = (cost or {}).get(v, 1)
                return c / max(len(work[v]), 1)
            v = min(sorted(work), key=ratio)
            spilled.add(v)
            trace.append(f"SPILL    {v} (degree {len(work[v])}, "
                         f"cost {(cost or {}).get(v, 1)}, "
                         f"ratio {ratio(v):.2f})")
        stack.append(v)
        for n in work[v]:
            work[n].discard(v)
        del work[v]

    assignment = {}
    while stack:
        v = stack.pop()
        if v in spilled:
            continue
        taken = {assignment[n] for n in graph[v] if n in assignment}
        free = [c for c in range(k) if c not in taken]
        if not free:
            # A node we optimistically pushed did not fit after all.  Chaitin
            # spills here; Briggs (1989) is the refinement that pushes
            # optimistically precisely so that this happens less often.
            spilled.add(v)
            trace.append(f"select   {v} -> no colour free, actual spill")
            continue
        assignment[v] = free[0]
        trace.append(f"select   {v} -> r{free[0]}")
    return assignment, spilled, trace


def chromatic_lower_bound(graph):
    """max clique is a lower bound on colours needed; we report max degree+1
    as an upper bound and the largest clique we find greedily as a floor."""
    best = 0
    for v in sorted(graph):
        clique = {v}
        for u in sorted(graph[v]):
            if all(u in graph[w] for w in clique):
                clique.add(u)
        best = max(best, len(clique))
    return best


# ------------------------------------------------------------------- driver
def report(src, fname=None, k=4):
    d, code, blocks = compile_fn(src, fname)
    check_coverage(code)
    g = interference(blocks)
    cost, depth = spill_costs(blocks)
    asg, spilled, trace = colour(g, k, cost)
    return d, code, blocks, g, cost, depth, asg, spilled, trace


if __name__ == '__main__':
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    which = sys.argv[2] if len(sys.argv) > 2 else None
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    d, code, blocks, g, cost, depth, asg, spilled, trace = report(src, which, k)

    print(f"; ---- interference graph for {d.name}: "
          f"{len(g)} nodes, {sum(len(v) for v in g.values()) // 2} edges ----")
    for v in sorted(g):
        print(f"  {v:6s} deg {len(g[v]):2d}  cost {cost.get(v,0):4d}  "
              f"| {' '.join(sorted(g[v])) or '-'}")

    lb = chromatic_lower_bound(g)
    maxdeg = max((len(n) for n in g.values()), default=0)
    print(f"\n; largest clique found: {lb}  (so at least {lb} registers)")
    print(f"; max degree: {maxdeg}  (so at most {maxdeg + 1} suffice)")

    print(f"\n; ---- Chaitin with k = {k} ----")
    for t in trace:
        print(f";  {t}")
    print(f"\n; assignment: " +
          (', '.join(f"{v}=r{c}" for v, c in sorted(asg.items())) or '-'))
    print(f"; spilled:    {sorted(spilled) or '-'}")

    print(f"\n; ---- how many registers does {d.name} actually need? ----")
    for kk in range(1, maxdeg + 3):
        a, sp, _ = colour(g, kk, cost)
        print(f";  k={kk:2d}  spilled {len(sp):2d}  {sorted(sp) if sp else ''}")
