#!/usr/bin/env python3
"""Constant folding, copy propagation, and dead-code elimination on TAC.

Each pass is a fixed-point iteration -- keep applying until nothing changes.
That is the same shape as epsilon-closure in Week 1 and FIRST/FOLLOW in
Week 2, and it is the shape of every dataflow analysis in Week 5.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tac import Instr, TAC, compile_fn, dump, build_cfg

FOLDABLE = {'+': lambda a, b: a + b, '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: int(a / b) if b else None,
            '%': lambda a, b: a - int(a / b) * b if b else None,
            '<': lambda a, b: a < b, '<=': lambda a, b: a <= b,
            '>': lambda a, b: a > b, '>=': lambda a, b: a >= b,
            '==': lambda a, b: a == b, '!=': lambda a, b: a != b}


def const_fold(code):
    """Replace `t = 2 + 3` with `t = 5`, propagating known constants."""
    known = {}
    changed = False
    out = []
    for ins in code:
        if ins.op == 'label':
            known.clear()               # a label may be a join point
            out.append(ins); continue
        if ins.op == 'const':
            known[ins.dst] = ins.a
            out.append(ins); continue

        a = known.get(ins.a, ins.a) if isinstance(ins.a, str) else ins.a
        b = known.get(ins.b, ins.b) if isinstance(ins.b, str) else ins.b

        if ins.op in FOLDABLE and isinstance(a, (int, bool)) \
                and isinstance(b, (int, bool)):
            v = FOLDABLE[ins.op](a, b)
            if v is not None:
                known[ins.dst] = v
                out.append(Instr('const', dst=ins.dst, a=v))
                changed = True
                continue
        # Cyan has no negative literals -- L03 section 3 -- so `-7` is unary
        # minus over 7. Without this case, nothing containing a negative
        # constant folds at all.
        if ins.op == 'unary' and isinstance(b, (int, bool)):
            v = (-b) if a == '-' else (not b)
            known[ins.dst] = v
            out.append(Instr('const', dst=ins.dst, a=v))
            changed = True
            continue
        if ins.op == 'copy' and isinstance(a, (int, bool)):
            known[ins.dst] = a
            out.append(Instr('const', dst=ins.dst, a=a))
            changed = True
            continue
        if ins.dst is not None:
            known.pop(ins.dst, None)
        out.append(ins)
    return out, changed


def copy_prop(code):
    """Replace uses of x with y after `x = y`."""
    alias, out, changed = {}, [], False
    for ins in code:
        if ins.op == 'label':
            alias.clear(); out.append(ins); continue
        a = alias.get(ins.a, ins.a) if isinstance(ins.a, str) else ins.a
        b = alias.get(ins.b, ins.b) if isinstance(ins.b, str) else ins.b
        if ins.op == 'call' and isinstance(ins.b, list):
            b = [alias.get(x, x) if isinstance(x, str) else x for x in ins.b]
        if (a, b) != (ins.a, ins.b):
            changed = True
        ni = Instr(ins.op, dst=ins.dst, a=a, b=b, label=ins.label)
        if ins.op == 'copy' and isinstance(a, str):
            alias[ins.dst] = a
        elif ins.dst is not None:
            alias.pop(ins.dst, None)
            alias = {k: v for k, v in alias.items() if v != ins.dst}
        out.append(ni)
    return out, changed


def dead_code(code):
    """Remove assignments whose destination is never read.

    Backwards pass: a temp is live if some later instruction reads it.
    Named variables are kept -- without full liveness we cannot prove a
    named local is dead, and Week 5 is where that becomes possible.
    """
    live, keep, changed = set(), [], False
    SIDE_EFFECTS = {'call', 'store', 'setfield', 'ret', 'goto', 'ifz',
                    'iftrue', 'label', 'alloc', 'newarr'}
    for ins in reversed(code):
        needed = ins.op in SIDE_EFFECTS or ins.dst is None \
            or ins.dst in live or not ins.dst.startswith('t')
        if needed:
            if ins.dst is not None:
                live.discard(ins.dst)
            for u in ins.uses():
                live.add(u)
            if ins.op == 'call' and isinstance(ins.b, list):
                live.update(x for x in ins.b if isinstance(x, str))
            keep.append(ins)
        else:
            changed = True
    return list(reversed(keep)), changed


def optimise(code, rounds=10):
    """Run the passes to a fixed point."""
    log = []
    for i in range(rounds):
        any_change = False
        for name, fn in (('fold', const_fold), ('copy', copy_prop),
                         ('dce', dead_code)):
            code, ch = fn(code)
            if ch:
                any_change = True
                log.append(f"round {i+1}: {name} changed the code")
        if not any_change:
            log.append(f"fixed point after {i+1} round(s)")
            break
    return code, log


if __name__ == '__main__':
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    which = sys.argv[2] if len(sys.argv) > 2 else None
    d, code, _ = compile_fn(src, which)
    print(f"; ---- before: {len(code)} instructions ----")
    dump(code)
    opt, log = optimise(code)
    print(f"\n; ---- after: {len(opt)} instructions ----")
    dump(opt)
    print("\n; ---- log ----")
    for l in log:
        print(f";  {l}")
