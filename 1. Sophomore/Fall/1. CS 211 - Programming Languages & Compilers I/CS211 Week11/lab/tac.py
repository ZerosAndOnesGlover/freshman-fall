#!/usr/bin/env python3
"""Three-address code generation, control-flow graphs, and SSA for Cyan.

Phase 5 of the eight. Reads the typed AST from typecheck.py and lowers it to
a flat list of instructions, each with at most three operands -- hence
"three-address". Then splits that into basic blocks and builds the CFG.
"""
import sys, os
from itertools import count

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lexer import LexError
from parser import parse, ParseError
from typecheck import Checker, TypeError_, INT, BOOL, STR


class Instr:
    """One three-address instruction: dst = a op b, or a control transfer."""

    def __init__(self, op, dst=None, a=None, b=None, label=None):
        self.op, self.dst, self.a, self.b, self.label = op, dst, a, b, label

    def __repr__(self):
        o = self.op
        if o == 'label':
            return f"{self.label}:"
        if o == 'goto':
            return f"    goto {self.label}"
        if o == 'ifz':
            return f"    ifz {self.a} goto {self.label}"
        if o == 'iftrue':
            return f"    if {self.a} goto {self.label}"
        if o == 'copy':
            return f"    {self.dst} = {self.a}"
        if o == 'const':
            return f"    {self.dst} = {self.a!r}"
        if o == 'unary':
            return f"    {self.dst} = {self.a}{self.b}"
        if o == 'call':
            args = ', '.join(map(str, self.b))
            return f"    {self.dst} = call {self.a}({args})" if self.dst \
                else f"    call {self.a}({args})"
        if o == 'ret':
            return f"    ret {self.a}" if self.a is not None else "    ret"
        if o == 'phi':
            args = ', '.join(f"{v}" for v in self.b)
            return f"    {self.dst} = phi({args})"
        # Week 5 fix.  These six fell through to the generic binary form
        # below, which printed `store` as `t2 = t3 store t0` -- reading as
        # though it DEFINED t2, when in fact it writes through it.  The
        # syllabus says you debug a compiler by dumping representations;
        # a dump that misreports a def is worse than no dump.
        if o == 'load':
            return f"    {self.dst} = {self.a}[{self.b}]"
        if o == 'store':
            return f"    {self.dst}[{self.a}] = {self.b}"
        if o == 'getfield':
            return f"    {self.dst} = {self.a}.{self.b}"
        if o == 'setfield':
            return f"    {self.dst}.{self.a} = {self.b}"
        if o == 'alloc':
            return f"    {self.dst} = alloc {self.a}"
        if o == 'newarr':
            return f"    {self.dst} = newarr {self.a}"
        return f"    {self.dst} = {self.a} {self.op} {self.b}"

    @property
    def is_terminator(self):
        return self.op in ('goto', 'ifz', 'iftrue', 'ret')

    def uses(self):
        """Variables read by this instruction.

        UNSAFE -- superseded by live.py's SLOTS table in Week 5, and kept
        only so that Lab 5 can measure what it gets wrong.  It decides what
        is a variable by the SHAPE of the operand, which misses that `store`
        and `setfield` read their `dst`, and which mistakes field and type
        names for variables.  Do not use it in new code.
        """
        out = []
        for x in (self.a, self.b):
            if isinstance(x, str) and (x.startswith('t') or x.startswith('%')
                                       or x.isidentifier()):
                if self.op != 'call' or x is not self.a:
                    out.append(x)
        if self.op == 'call' and isinstance(self.b, list):
            out = [x for x in self.b if isinstance(x, str)]
        if self.op == 'phi':
            out = list(self.b)
        return out


class TAC:
    def __init__(self):
        self.code = []
        self.temps = count()
        self.labels = count()

    def temp(self):
        return f"t{next(self.temps)}"

    def label(self):
        return f"L{next(self.labels)}"

    def emit(self, *a, **kw):
        self.code.append(Instr(*a, **kw))
        return self.code[-1]

    # ----------------------------------------------------------- program
    def gen_fn(self, d):
        self.emit('label', label=f"fn_{d.name}")
        self.gen_block(d.body)
        if not (self.code and self.code[-1].op == 'ret'):
            self.emit('ret')
        return self.code

    def gen_block(self, b):
        for s in b.stmts:
            self.gen_stmt(s)

    def gen_stmt(self, s):
        k = s.kind
        if k == 'Let':
            v = self.gen_expr(s.value)
            self.emit('copy', dst=s.name, a=v)
        elif k == 'Assign':
            v = self.gen_expr(s.value)
            if s.target.kind == 'Var':
                self.emit('copy', dst=s.target.name, a=v)
            elif s.target.kind == 'Index':
                arr = self.gen_expr(s.target.arr)
                idx = self.gen_expr(s.target.index)
                self.emit('store', dst=arr, a=idx, b=v)
            else:
                obj = self.gen_expr(s.target.obj)
                self.emit('setfield', dst=obj, a=s.target.name, b=v)
        elif k == 'If':
            c = self.gen_expr(s.cond)
            lelse, lend = self.label(), self.label()
            self.emit('ifz', a=c, label=lelse if s.els else lend)
            self.gen_block(s.then)
            if s.els:
                self.emit('goto', label=lend)
                self.emit('label', label=lelse)
                if s.els.kind == 'Block':
                    self.gen_block(s.els)
                else:
                    self.gen_stmt(s.els)
            self.emit('label', label=lend)
        elif k == 'While':
            ltop, lend = self.label(), self.label()
            self.emit('label', label=ltop)
            c = self.gen_expr(s.cond)
            self.emit('ifz', a=c, label=lend)
            self.gen_block(s.body)
            self.emit('goto', label=ltop)
            self.emit('label', label=lend)
        elif k == 'Return':
            self.emit('ret', a=self.gen_expr(s.value) if s.value else None)
        elif k == 'ExprStmt':
            self.gen_expr(s.expr)
        else:
            raise NotImplementedError(k)

    def gen_expr(self, e):
        k = e.kind
        if k == 'Int':
            t = self.temp(); self.emit('const', dst=t, a=e.value); return t
        if k == 'Bool':
            t = self.temp(); self.emit('const', dst=t, a=e.value); return t
        if k == 'Str':
            t = self.temp(); self.emit('const', dst=t, a=e.value); return t
        if k == 'Var':
            return e.name
        if k == 'Unary':
            o = self.gen_expr(e.operand)
            t = self.temp(); self.emit('unary', dst=t, a=e.op, b=o); return t
        if k == 'Binary':
            if e.op in ('&&', '||'):
                return self.gen_shortcircuit(e)
            l = self.gen_expr(e.lhs)
            r = self.gen_expr(e.rhs)
            t = self.temp()
            self.emit(e.op, dst=t, a=l, b=r)
            return t
        if k == 'Call':
            fname = e.fn.name if e.fn.kind == 'Var' else self.gen_expr(e.fn)
            args = [self.gen_expr(a) for a in e.args]
            t = self.temp()
            self.emit('call', dst=t, a=fname, b=args)
            return t
        if k == 'Index':
            a = self.gen_expr(e.arr); i = self.gen_expr(e.index)
            t = self.temp(); self.emit('load', dst=t, a=a, b=i); return t
        if k == 'Field':
            o = self.gen_expr(e.obj)
            t = self.temp(); self.emit('getfield', dst=t, a=o, b=e.name); return t
        if k == 'New':
            t = self.temp()
            self.emit('alloc', dst=t, a=e.name)
            for f, v in e.inits:
                val = self.gen_expr(v)
                self.emit('setfield', dst=t, a=f, b=val)
            return t
        if k == 'Array':
            t = self.temp()
            self.emit('newarr', dst=t, a=len(e.items))
            for i, x in enumerate(e.items):
                v = self.gen_expr(x)
                self.emit('store', dst=t, a=i, b=v)
            return t
        raise NotImplementedError(k)

    def gen_shortcircuit(self, e):
        """&& and || must not evaluate the right operand unconditionally."""
        t = self.temp()
        lend = self.label()
        l = self.gen_expr(e.lhs)
        self.emit('copy', dst=t, a=l)
        if e.op == '&&':
            self.emit('ifz', a=t, label=lend)
        else:
            self.emit('iftrue', a=t, label=lend)
        r = self.gen_expr(e.rhs)
        self.emit('copy', dst=t, a=r)
        self.emit('label', label=lend)
        return t


# ------------------------------------------------------------- basic blocks
class Block:
    def __init__(self, name):
        self.name, self.instrs = name, []
        self.succs, self.preds = [], []

    def __repr__(self):
        return f"<{self.name}: {len(self.instrs)} instr>"


def build_cfg(code):
    """Split a flat instruction list into basic blocks and link them.

    A leader is: the first instruction, any label, and any instruction
    following a terminator. -- Dragon section 8.4
    """
    leaders = {0}
    for i, ins in enumerate(code):
        if ins.op == 'label':
            leaders.add(i)
        if ins.is_terminator and i + 1 < len(code):
            leaders.add(i + 1)

    starts = sorted(leaders)
    blocks, by_label = [], {}
    for n, s in enumerate(starts):
        end = starts[n + 1] if n + 1 < len(starts) else len(code)
        name = code[s].label if code[s].op == 'label' else f"B{n}"
        b = Block(name)
        b.instrs = code[s:end]
        blocks.append(b)
        if code[s].op == 'label':
            by_label[code[s].label] = b

    for n, b in enumerate(blocks):
        last = b.instrs[-1] if b.instrs else None
        if last is None:
            continue
        if last.op == 'goto':
            tgt = by_label.get(last.label)
            if tgt:
                b.succs.append(tgt)
        elif last.op in ('ifz', 'iftrue'):
            tgt = by_label.get(last.label)
            if tgt:
                b.succs.append(tgt)
            if n + 1 < len(blocks):
                b.succs.append(blocks[n + 1])
        elif last.op == 'ret':
            pass
        elif n + 1 < len(blocks):
            b.succs.append(blocks[n + 1])
    for b in blocks:
        for s in b.succs:
            s.preds.append(b)
    return blocks


def compile_fn(src, fname=None):
    ast = parse(src)
    c = Checker()
    c.check_program(ast)
    fns = [d for d in ast.decls if d.kind == 'Fn']
    d = next((f for f in fns if f.name == fname), fns[0]) if fns else None
    t = TAC()
    t.gen_fn(d)
    return d, t.code, build_cfg(t.code)


def dump(code):
    for ins in code:
        print(ins)


def dump_cfg(blocks):
    for b in blocks:
        succ = ', '.join(x.name for x in b.succs) or '-'
        pred = ', '.join(x.name for x in b.preds) or '-'
        print(f"{b.name}  (preds: {pred})  ->  {succ}")
        for ins in b.instrs:
            if ins.op != 'label':
                print(f"  {ins!r}")


if __name__ == '__main__':
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    which = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        d, code, blocks = compile_fn(src, which)
        print(f"; ---- three-address code for {d.name} ----")
        dump(code)
        print(f"\n; ---- CFG: {len(blocks)} basic blocks ----")
        dump_cfg(blocks)
    except (LexError, ParseError, TypeError_) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
