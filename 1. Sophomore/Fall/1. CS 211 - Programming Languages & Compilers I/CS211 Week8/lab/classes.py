#!/usr/bin/env python3
"""Type classes, and the translation that makes them disappear.

A type class looks like a new language feature:

    class Eq a where
      eq : a -> a -> Bool

    instance Eq Int  where eq = primEqInt
    instance Eq Bool where eq = primEqBool
    instance Eq a => Eq (List a) where eq = ...   -- needs Eq a

    member : Eq a => a -> List a -> Bool

It is not one. **A class is a record type, an instance is a value of that
record, and a constrained function is a function that takes the record as an
extra argument.** The record is called a *dictionary*, and the translation is
called dictionary passing.

    python3 classes.py

The output is the elaborated program. Read the `member` case: the constraint
`Eq a =>` has become a parameter, and every call site has been given the
right dictionary by the compiler. **Nothing in the elaborated program is a
type class.**

Why this matters beyond Haskell: it is the same trick as a C++ vtable and a
Rust trait object, with one difference that decides everything about how they
perform -- section 8 of L18.
"""
import sys


# ------------------------------------------------------------------ types
class TCon:
    __slots__ = ('name', 'args')

    def __init__(self, name, *args):
        self.name, self.args = name, args

    def __repr__(self):
        return f"{self.name} {' '.join(map(repr, self.args))}" if self.args \
            else self.name

    def __eq__(self, o):
        return (isinstance(o, TCon) and o.name == self.name
                and o.args == self.args)

    def __hash__(self):
        return hash((self.name, self.args))


class TVar:
    __slots__ = ('name',)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, o):
        return isinstance(o, TVar) and o.name == self.name

    def __hash__(self):
        return hash(('v', self.name))


INT, BOOL = TCon('Int'), TCon('Bool')


def LIST(t):
    return TCon('List', t)


def PAIR(a, b):
    return TCon('Pair', a, b)


# ---------------------------------------------------------------- classes
class Class:
    """A class declaration is a **record type**."""

    def __init__(self, name, var, methods, supers=()):
        self.name, self.var, self.methods = name, var, methods
        self.supers = supers

    def dict_type(self):
        sup = [f"super{s}" for s in self.supers]
        return "{ " + ', '.join(sup + list(self.methods)) + " }"


class Instance:
    """An instance declaration is a **value** of that record type.

    `context` is the list of constraints the instance itself needs -- the
    `Eq a =>` in `instance Eq a => Eq (List a)`.  In the elaborated program
    those become *parameters of the dictionary-building function*, which is
    why an instance with a context compiles to a function rather than a
    constant.
    """

    def __init__(self, cls, head, impls, context=()):
        self.cls, self.head, self.impls = cls, head, impls
        self.context = context

    def key(self):
        return (self.cls, self.head.name)


# ------------------------------------------------------------------ program
CLASSES = {
    'Eq': Class('Eq', 'a', {'eq': 'a -> a -> Bool'}),
    'Ord': Class('Ord', 'a', {'le': 'a -> a -> Bool'}, supers=('Eq',)),
    'Show': Class('Show', 'a', {'show': 'a -> String'}),
}

INSTANCES = [
    Instance('Eq', INT, {'eq': 'primEqInt'}),
    Instance('Eq', BOOL, {'eq': 'primEqBool'}),
    Instance('Eq', LIST(TVar('a')), {'eq': 'eqList dEq_a'},
             context=[('Eq', 'a')]),
    Instance('Eq', PAIR(TVar('a'), TVar('b')),
             {'eq': 'eqPair dEq_a dEq_b'},
             context=[('Eq', 'a'), ('Eq', 'b')]),
    Instance('Ord', INT, {'le': 'primLeInt'}),
    Instance('Ord', LIST(TVar('a')), {'le': 'leList dOrd_a'},
             context=[('Ord', 'a')]),
    Instance('Show', INT, {'show': 'primShowInt'}),
    Instance('Show', LIST(TVar('a')), {'show': 'showList dShow_a'},
             context=[('Show', 'a')]),
]


def find(cls, ty):
    """Resolve `cls ty` to an instance, or None.

    **This is where the work happens, and it happens at compile time.** The
    result is a dictionary *expression*, built once, with no run-time search.
    """
    for inst in INSTANCES:
        if inst.cls != cls:
            continue
        if inst.head == ty:
            return inst, {}
        if isinstance(inst.head, TCon) and isinstance(ty, TCon) \
                and inst.head.name == ty.name \
                and len(inst.head.args) == len(ty.args):
            sub = {}
            ok = True
            for pat, act in zip(inst.head.args, ty.args):
                if isinstance(pat, TVar):
                    sub[pat.name] = act
                elif pat != act:
                    ok = False
            if ok:
                return inst, sub
    return None, None


def resolve(cls, ty, depth=0):
    """Build the dictionary expression for `cls ty`, recursively.

    Returns (expression, trace-lines) or raises. The recursion is why
    `eq [[1],[2]]` works without anyone writing an instance for
    lists-of-lists-of-Int: the compiler *constructs* one.
    """
    inst, sub = find(cls, ty)
    if inst is None:
        raise TypeError(f"no instance for {cls} {ty!r}")
    pad = '  ' * depth
    lines = [f"{pad}{cls} {ty!r}  ->  instance {cls} {inst.head!r}"]
    args = []
    for (c, v) in inst.context:
        arg_ty = sub.get(v)
        if arg_ty is None:
            raise TypeError(f"cannot resolve {c} {v} for {cls} {ty!r}")
        e, sub_lines = resolve(c, arg_ty, depth + 1)
        lines += sub_lines
        args.append(e)
    name = f"d{cls}_{_tyname(ty)}"
    expr = name if not args else f"({name} {' '.join(args)})"
    return expr, lines


def _tyname(t):
    if isinstance(t, TVar):
        return t.name
    # `.capitalize()` would lowercase the rest, turning ListInt into Listint
    # one nesting level down. Upper-case the first character only.
    def cap(s):
        return s[:1].upper() + s[1:]
    return t.name + ''.join(cap(_tyname(a)) for a in t.args)


# -------------------------------------------------------------------- main
def rule(t):
    print(f"\n; ---- {t} ----")


def main():
    print("; ---- a class is a record type ----")
    for name, c in CLASSES.items():
        sup = f"  (superclass: {', '.join(c.supers)})" if c.supers else ""
        print(f"  class {name} {c.var}   =>   type Dict{name} {c.var} = "
              f"{c.dict_type()}{sup}")

    rule("an instance is a value of that record")
    for inst in INSTANCES:
        ctx = ''
        if inst.context:
            ctx = ('(' + ', '.join(f"{c} {v}" for c, v in inst.context)
                   + ') => ')
        target = f"d{inst.cls}_{_tyname(inst.head)}"
        params = ' '.join(f"d{c}_{v}" for c, v in inst.context)
        lhs = f"{target} {params}".strip()
        body = ', '.join(f"{k} = {v}" for k, v in inst.impls.items())
        print(f"  instance {ctx}{inst.cls} {inst.head!r}")
        print(f"      {lhs} = {{ {body} }}")

    rule("resolution happens at COMPILE time, and it recurses")
    for cls, ty in [('Eq', INT), ('Eq', LIST(INT)), ('Eq', LIST(LIST(INT))),
                    ('Eq', PAIR(INT, LIST(BOOL))), ('Ord', LIST(INT)),
                    ('Show', LIST(LIST(INT)))]:
        expr, lines = resolve(cls, ty)
        print(f"  {cls} {ty!r}")
        for l in lines[1:]:
            print(f"      {l}")
        print(f"      => {expr}")

    rule("what a constrained function becomes")
    print("  source:")
    print("      member : Eq a => a -> List a -> Bool")
    print("      member x xs = ...  uses  eq x y")
    print()
    print("  elaborated:")
    print("      member : DictEq a -> a -> List a -> Bool")
    print("      member dEq_a x xs = ...  uses  (eq dEq_a) x y")
    print()
    print("  call site `member 3 [1,2,3]`  becomes  `member dEq_Int 3 [1,2,3]`")
    expr, _ = resolve('Eq', LIST(INT))
    print(f"  call site `member [1] [[1],[2]]`  becomes  "
          f"`member {expr} [1] [[1],[2]]`")

    rule("what fails, and when")
    for cls, ty in [('Show', BOOL), ('Ord', BOOL), ('Eq', TCon('Tree', INT))]:
        try:
            resolve(cls, ty)
            print(f"  {cls} {ty!r}: resolved")
        except TypeError as e:
            print(f"  {cls} {ty!r:<12} COMPILE-TIME ERROR -- {e}")
    print()
    print("  Note WHEN those failed: at elaboration, before anything ran.")
    print("  A missing instance is a type error, not a method-not-found.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
