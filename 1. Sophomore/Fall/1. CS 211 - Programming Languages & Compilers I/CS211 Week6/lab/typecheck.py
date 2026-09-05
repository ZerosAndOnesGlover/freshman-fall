#!/usr/bin/env python3
"""Type checker and scope analyser for Cyan.

Phase 4 of the eight. Walks the AST from parser.py, builds a symbol table,
resolves every name, and annotates each expression node with a type.

Cyan is NOT Hindley-Milner: parameters and return types are annotated, so
inference is local -- a `let` takes the type of its initialiser and nothing
else needs solving. Week 3's lectures use HM for the general case; this is
the pragmatic version, and the difference is the point of PS 3 Q4.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lexer import tokenize, LexError
from parser import parse, Node, ParseError


class TypeError_(Exception):
    pass


def err(node, msg):
    """Raise a type error located at `node`. Every message in this phase goes
    through here, so every message carries a position -- which is only
    possible because parser.py put line/col on the node."""
    where = f"line {node.line}" if getattr(node, 'line', 0) else "?"
    if getattr(node, 'col', 0):
        where += f" col {node.col}"
    raise TypeError_(f"{where}: {msg}")


# ------------------------------------------------------------------ types
class Ty:
    def __init__(self, name, args=(), fields=None):
        self.name, self.args, self.fields = name, tuple(args), fields

    def __eq__(self, o):
        return isinstance(o, Ty) and self.name == o.name and self.args == o.args

    def __hash__(self):
        return hash((self.name, self.args))

    def __repr__(self):
        if self.name == 'fn':
            *a, r = self.args
            return f"fn({', '.join(map(repr, a))}) -> {r!r}"
        if self.name == 'array':
            return f"[{self.args[0]!r}]"
        return self.name


INT, BOOL, STR, VOID = Ty('int'), Ty('bool'), Ty('string'), Ty('void')


# ----------------------------------------------------------- symbol table
class Scope:
    """A lexical scope. Chained to its parent -- L07 section 3."""

    def __init__(self, parent=None):
        self.names = {}
        self.parent = parent

    def declare(self, name, ty, line):
        if name in self.names:
            raise TypeError_(f"line {line}: '{name}' is already declared in this scope")
        self.names[name] = ty
        return ty

    def lookup(self, name):
        s = self
        while s is not None:
            if name in s.names:
                return s.names[name]
            s = s.parent
        return None

    def depth(self):
        return 0 if self.parent is None else 1 + self.parent.depth()


class Checker:
    def __init__(self):
        self.structs = {}          # name -> {field: Ty}
        self.globals = Scope()
        self.ret_stack = []
        self.trace = []            # (event, name, depth) for --dump-scopes

    # ------------------------------------------------------------ types
    def resolve_type(self, node, line=0):
        if node is None:
            return VOID
        if node.kind == 'TyPrim':
            return {'int': INT, 'bool': BOOL, 'string': STR}[node.name]
        if node.kind == 'TyArray':
            return Ty('array', (self.resolve_type(node.of, line),))
        if node.kind == 'TyFn':
            return Ty('fn', tuple(self.resolve_type(a, line) for a in node.args)
                      + (self.resolve_type(node.ret, line),))
        if node.kind == 'TyName':
            if node.name not in self.structs:
                raise TypeError_(f"line {line}: unknown type '{node.name}'")
            return Ty(node.name)
        raise TypeError_(f"line {line}: bad type node {node.kind}")

    # ---------------------------------------------------------- program
    def check_program(self, prog):
        # Pass 1: struct declarations, so types can refer to them.
        for d in prog.decls:
            if d.kind == 'Struct':
                if d.name in self.structs:
                    raise TypeError_(f"struct '{d.name}' declared twice")
                self.structs[d.name] = {}
        for d in prog.decls:
            if d.kind == 'Struct':
                self.structs[d.name] = {f: self.resolve_type(t) for f, t in d.fields}

        # Pass 2: function signatures, so calls may precede declarations.
        for d in prog.decls:
            if d.kind == 'Fn':
                sig = Ty('fn', tuple(self.resolve_type(t) for _, t in d.params)
                         + (self.resolve_type(d.ret),))
                self.globals.declare(d.name, sig, 0)

        # Pass 3: bodies, and top-level lets in order.
        for d in prog.decls:
            if d.kind == 'Fn':
                self.check_fn(d)
            elif d.kind == 'Let':
                want = self.resolve_type(d.ty) if d.ty is not None else None
                t = self.check_expr(d.value, self.globals, want)
                if d.ty is not None:
                    if t != want:
                        raise TypeError_(f"'{d.name}' declared {want!r} but initialised {t!r}")
                self.globals.declare(d.name, t, 0)

    def check_fn(self, d):
        scope = Scope(self.globals)
        for pname, pty in d.params:
            scope.declare(pname, self.resolve_type(pty), 0)
            self.trace.append(('declare', pname, scope.depth()))
        ret = self.resolve_type(d.ret)
        self.ret_stack.append(ret)
        self.check_block(d.body, scope)
        self.ret_stack.pop()

    # -------------------------------------------------------- statements
    def check_block(self, block, parent):
        scope = Scope(parent)                      # a block opens a scope
        self.trace.append(('enter', '', scope.depth()))
        for s in block.stmts:
            self.check_stmt(s, scope)
        self.trace.append(('exit', '', scope.depth()))

    def check_stmt(self, s, scope):
        k = s.kind
        if k == 'Let':
            want = self.resolve_type(s.ty) if s.ty is not None else None
            t = self.check_expr(s.value, scope, want)
            if s.ty is not None:
                if t != want:
                    err(s, f"'{s.name}' is declared {want!r} but "
                           f"initialised with {t!r}")
                t = want
            scope.declare(s.name, t, s.line)
            self.trace.append(('declare', s.name, scope.depth()))
        elif k == 'Assign':
            tt = self.check_expr(s.target, scope)
            tv = self.check_expr(s.value, scope, tt)
            if tt != tv:
                err(s, f"cannot assign {tv!r} to a target of type {tt!r}")
        elif k == 'If':
            c = self.check_expr(s.cond, scope)
            if c != BOOL:
                err(s.cond, f"if condition must be bool, found {c!r}")
            self.check_block(s.then, scope)
            if s.els is not None:
                if s.els.kind == 'Block':
                    self.check_block(s.els, scope)
                else:
                    self.check_stmt(s.els, scope)
        elif k == 'While':
            c = self.check_expr(s.cond, scope)
            if c != BOOL:
                err(s.cond, f"while condition must be bool, found {c!r}")
            self.check_block(s.body, scope)
        elif k == 'Return':
            want = self.ret_stack[-1]
            got = VOID if s.value is None else self.check_expr(s.value, scope)
            if got != want:
                err(s, f"function returns {want!r} but this returns {got!r}")
        elif k == 'ExprStmt':
            self.check_expr(s.expr, scope)
        else:
            raise TypeError_(f"unknown statement {k}")

    # ------------------------------------------------------- expressions
    ARITH = {'+', '-', '*', '/', '%'}
    ORDER = {'<', '<=', '>', '>='}
    EQ = {'==', '!='}

    def check_expr(self, e, scope, expect=None):
        """Type of `e`.

        Week 6 adds `expect`: the type the surrounding context requires, or
        None where there is no such requirement.  Everything in the language
        infers its own type bottom-up and ignores it -- except the empty
        array literal, which has nothing to infer from.  Passing the
        expectation down instead of only checking against it on the way back
        up is called *bidirectional* type checking, and this is the smallest
        possible instance of it.

        The reason it is in Week 6 and not Week 3 is that it is what makes a
        heap cycle constructible, and therefore what makes reference counting
        incomplete.  L13 section 10.
        """
        k = e.kind
        if k == 'Int':
            t = INT
        elif k == 'Bool':
            t = BOOL
        elif k == 'Str':
            t = STR
        elif k == 'Var':
            t = scope.lookup(e.name)
            if t is None:
                err(e, f"undefined variable '{e.name}'")
        elif k == 'Unary':
            o = self.check_expr(e.operand, scope)
            if e.op == '-':
                if o != INT:
                    err(e, f"unary '-' needs int, found {o!r}")
                t = INT
            else:
                if o != BOOL:
                    err(e, f"'!' needs bool, found {o!r}")
                t = BOOL
        elif k == 'Binary':
            t = self.check_binary(e, scope)
        elif k == 'Call':
            ft = self.check_expr(e.fn, scope)
            if ft.name != 'fn':
                err(e, f"cannot call a value of type {ft!r}")
            *params, ret = ft.args
            if len(params) != len(e.args):
                err(e, f"expected {len(params)} argument(s), "
                       f"found {len(e.args)}")
            for i, (a, want) in enumerate(zip(e.args, params)):
                got = self.check_expr(a, scope)
                if got != want:
                    err(a, f"argument {i+1} should be {want!r}, found {got!r}")
            t = ret
        elif k == 'Index':
            at = self.check_expr(e.arr, scope)
            it = self.check_expr(e.index, scope)
            if at.name != 'array':
                err(e, f"cannot index a value of type {at!r}")
            if it != INT:
                err(e.index, f"array index must be int, found {it!r}")
            t = at.args[0]
        elif k == 'Field':
            ot = self.check_expr(e.obj, scope)
            if ot.name not in self.structs:
                err(e, f"type {ot!r} has no fields")
            fields = self.structs[ot.name]
            if e.name not in fields:
                err(e, f"struct '{ot.name}' has no field '{e.name}'")
            t = fields[e.name]
        elif k == 'Array':
            if not e.items:
                if expect is None or expect.name != 'array':
                    err(e, "cannot infer the type of an empty array literal, "
                           "and the context does not say what it should be")
                t = expect          # fall through: `e.ty = t` still has to run
            else:
                ts = [self.check_expr(x, scope) for x in e.items]
                if any(x != ts[0] for x in ts):
                    err(e, f"array elements have differing types: {ts[0]!r} "
                           f"and {next(x for x in ts if x != ts[0])!r}")
                t = Ty('array', (ts[0],))
        elif k == 'New':
            if e.name not in self.structs:
                err(e, f"unknown struct '{e.name}'")
            fields = self.structs[e.name]
            given = {f for f, _ in e.inits}
            missing = set(fields) - given
            extra = given - set(fields)
            if missing:
                err(e, f"struct '{e.name}' is missing field(s): "
                       f"{', '.join(sorted(missing))}")
            if extra:
                err(e, f"struct '{e.name}' has no field(s): "
                       f"{', '.join(sorted(extra))}")
            for f, v in e.inits:
                got = self.check_expr(v, scope, fields[f])
                if got != fields[f]:
                    err(v, f"field '{f}' should be {fields[f]!r}, found {got!r}")
            t = Ty(e.name)
        elif k == 'Lambda':
            s2 = Scope(scope)
            for pn, pt in e.params:
                s2.declare(pn, self.resolve_type(pt), 0)
            ret = self.resolve_type(e.ret)
            self.ret_stack.append(ret)
            self.check_block(e.body, s2)
            self.ret_stack.pop()
            t = Ty('fn', tuple(self.resolve_type(pt) for _, pt in e.params) + (ret,))
        else:
            raise TypeError_(f"unknown expression {k}")
        e.ty = t                       # annotate -- this is the phase's output
        return t

    def check_binary(self, e, scope):  # noqa: C901
        lt = self.check_expr(e.lhs, scope)
        rt = self.check_expr(e.rhs, scope)
        op = e.op
        if op in self.ARITH:
            if op == '+' and lt == STR and rt == STR:
                return STR
            if lt != INT or rt != INT:
                err(e, f"'{op}' needs int operands, found {lt!r} and {rt!r}")
            return INT
        if op in self.ORDER:
            if lt != INT or rt != INT:
                err(e, f"'{op}' needs int operands, found {lt!r} and {rt!r}")
            return BOOL
        if op in self.EQ:
            if lt != rt:
                err(e, f"cannot compare {lt!r} with {rt!r}")
            return BOOL
        if op in ('&&', '||'):
            if lt != BOOL or rt != BOOL:
                err(e, f"'{op}' needs bool operands, found {lt!r} and {rt!r}")
            return BOOL
        raise TypeError_(f"unknown operator '{op}'")


def check(src):
    ast = parse(src)
    c = Checker()
    c.check_program(ast)
    return ast, c


if __name__ == '__main__':
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    try:
        ast, c = check(src)
        print("type check passed")
        for name, ty in c.globals.names.items():
            print(f"  {name:<12} : {ty!r}")
    except (LexError, ParseError, TypeError_) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
