"""Week 3 verification: Hindley-Milner type inference by unification.

A minimal HM implementation over a small lambda language, used to produce the
worked traces in L07/L08 and to check the PS 3 answers. Deliberately small --
the point is that the whole algorithm is about 120 lines.
"""
from itertools import count

_fresh = count()


# ---------------------------------------------------------------- types
class TVar:
    def __init__(self):
        self.id = next(_fresh)
        self.ref = None          # set when unified

    def __repr__(self):
        return repr(prune(self)) if self.ref else f"t{self.id}"


class TCon:
    def __init__(self, name, args=()):
        self.name, self.args = name, tuple(args)

    def __repr__(self):
        if self.name == '->':
            a, b = self.args
            astr = f"({a!r})" if isinstance(prune(a), TCon) and prune(a).name == '->' else repr(a)
            return f"{astr} -> {b!r}"
        if not self.args:
            return self.name
        return f"{self.name}[{', '.join(map(repr, self.args))}]"


def fn(a, b):
    return TCon('->', (a, b))


INT, BOOL = TCon('int'), TCon('bool')


def prune(t):
    """Follow unification links to the representative type."""
    if isinstance(t, TVar) and t.ref is not None:
        t.ref = prune(t.ref)
        return t.ref
    return t


def occurs(v, t):
    t = prune(t)
    if t is v:
        return True
    if isinstance(t, TCon):
        return any(occurs(v, a) for a in t.args)
    return False


class TypeError_(Exception):
    pass


def unify(a, b, trace=None):
    a, b = prune(a), prune(b)
    if trace is not None:
        trace.append(f"unify({a!r}, {b!r})")
    if isinstance(a, TVar):
        if a is not b:
            if occurs(a, b):
                raise TypeError_(f"occurs check: cannot construct infinite type {a!r} = {b!r}")
            a.ref = b
        return
    if isinstance(b, TVar):
        return unify(b, a, trace)
    if a.name != b.name or len(a.args) != len(b.args):
        raise TypeError_(f"cannot unify {a!r} with {b!r}")
    for x, y in zip(a.args, b.args):
        unify(x, y, trace)


# ------------------------------------------------------------ expressions
# ('var', name) | ('lam', x, body) | ('app', f, arg)
# ('let', x, val, body) | ('int', n) | ('bool', b)
# ('if', c, t, e) | ('add', l, r) | ('leq', l, r)

class Scheme:
    """A polymorphic type: forall qs . t"""
    def __init__(self, qs, t):
        self.qs, self.t = qs, t


def free_vars(t, acc=None):
    acc = set() if acc is None else acc
    t = prune(t)
    if isinstance(t, TVar):
        acc.add(t)
    else:
        for a in t.args:
            free_vars(a, acc)
    return acc


def instantiate(s):
    if not s.qs:
        return s.t
    mapping = {q: TVar() for q in s.qs}

    def go(t):
        t = prune(t)
        if isinstance(t, TVar):
            return mapping.get(t, t)
        return TCon(t.name, [go(a) for a in t.args])
    return go(s.t)


def generalise(env, t):
    env_free = set()
    for s in env.values():
        env_free |= free_vars(s.t) - set(s.qs)
    return Scheme(list(free_vars(t) - env_free), t)


def infer(e, env, trace=None):
    kind = e[0]
    if kind == 'int':
        return INT
    if kind == 'bool':
        return BOOL
    if kind == 'var':
        if e[1] not in env:
            raise TypeError_(f"unbound variable '{e[1]}'")
        return instantiate(env[e[1]])
    if kind == 'lam':
        _, x, body = e
        tv = TVar()
        if trace is not None:
            trace.append(f"assign {x} : {tv!r}")
        return fn(tv, infer(body, {**env, x: Scheme([], tv)}, trace))
    if kind == 'app':
        _, f, a = e
        tf, ta = infer(f, env, trace), infer(a, env, trace)
        tr = TVar()
        unify(tf, fn(ta, tr), trace)
        return tr
    if kind == 'let':
        _, x, val, body = e
        tv = infer(val, env, trace)
        return infer(body, {**env, x: generalise(env, tv)}, trace)
    if kind == 'if':
        _, c, t, f = e
        unify(infer(c, env, trace), BOOL, trace)
        tt, tf = infer(t, env, trace), infer(f, env, trace)
        unify(tt, tf, trace)
        return tt
    if kind == 'add':
        _, l, r = e
        unify(infer(l, env, trace), INT, trace)
        unify(infer(r, env, trace), INT, trace)
        return INT
    if kind == 'leq':
        _, l, r = e
        unify(infer(l, env, trace), INT, trace)
        unify(infer(r, env, trace), INT, trace)
        return BOOL
    raise TypeError_(f"unknown node {kind}")


def show(label, e, env=None, with_trace=False):
    global _fresh
    _fresh = count()
    tr = [] if with_trace else None
    try:
        t = infer(e, env or {}, tr)
        print(f"  {label:<34} : {t!r}")
    except TypeError_ as ex:
        print(f"  {label:<34} : TYPE ERROR -- {ex}")
    if with_trace:
        for line in tr:
            print(f"        {line}")


print("=== inferred types, no annotations anywhere ===")
show("\\x -> x", ('lam', 'x', ('var', 'x')))
show("\\x -> x + 1", ('lam', 'x', ('add', ('var', 'x'), ('int', 1))))
show("\\f -> \\x -> f (f x)",
     ('lam', 'f', ('lam', 'x', ('app', ('var', 'f'), ('app', ('var', 'f'), ('var', 'x'))))))
show("\\x -> \\y -> x", ('lam', 'x', ('lam', 'y', ('var', 'x'))))
show("\\f -> \\g -> \\x -> f (g x)",
     ('lam', 'f', ('lam', 'g', ('lam', 'x',
      ('app', ('var', 'f'), ('app', ('var', 'g'), ('var', 'x')))))))
show("\\x -> if x <= 0 then 1 else x",
     ('lam', 'x', ('if', ('leq', ('var', 'x'), ('int', 0)), ('int', 1), ('var', 'x'))))

print("\n=== let-polymorphism ===")
# f must be used at TWO DIFFERENT types for the effect to show. Here it is
# bool->bool in the condition and int->int in the branch.
_body = ('if', ('app', ('var', 'f'), ('bool', True)),
               ('app', ('var', 'f'), ('int', 1)),
               ('int', 2))
show("let f = \\x->x in if f true then f 1 else 2",
     ('let', 'f', ('lam', 'x', ('var', 'x')), _body))
show("(\\f -> if f true then f 1 else 2) (\\x->x)",
     ('app', ('lam', 'f', _body), ('lam', 'x', ('var', 'x'))))

# The classic example is a TRAP: both forms accept it, because both uses of
# id are at int->int and no polymorphism is needed.
show("let id = \\x->x in id (id 1)   [both OK]",
     ('let', 'id', ('lam', 'x', ('var', 'x')),
      ('app', ('var', 'id'), ('app', ('var', 'id'), ('int', 1)))))
show("(\\id -> id (id 1)) (\\x->x)     [both OK]",
     ('app', ('lam', 'id', ('app', ('var', 'id'),
                            ('app', ('var', 'id'), ('int', 1)))),
      ('lam', 'x', ('var', 'x'))))

print("\n=== errors ===")
show("1 + true", ('add', ('int', 1), ('bool', True)))
show("\\x -> x x", ('lam', 'x', ('app', ('var', 'x'), ('var', 'x'))))
show("if 1 then 1 else 2", ('if', ('int', 1), ('int', 1), ('int', 2)))
show("if true then 1 else false", ('if', ('bool', True), ('int', 1), ('bool', False)))

print("\n=== the trace for \\x -> x + 1 ===")
show("\\x -> x + 1", ('lam', 'x', ('add', ('var', 'x'), ('int', 1))), with_trace=True)
