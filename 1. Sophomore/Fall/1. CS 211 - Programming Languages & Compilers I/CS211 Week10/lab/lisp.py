#!/usr/bin/env python3
"""A Lisp, in order to have macros.

Week 7 established a rule and then measured it: **in a strict language `if`
cannot be an ordinary function**, because a function's arguments are
evaluated before it is entered and a conditional's whole job is to decline to
evaluate one of its branches. `factV` needed `lazyif` and thunks to work
under call-by-value at all.

This file is about the other way out. A **macro** is not a function: it runs
at *expansion* time and receives its arguments as **unevaluated syntax**. So
a macro can be `if`. It can also be `while`, `unless`, `and`, `or`, and any
other control structure you care to invent -- as ordinary library code, with
no change to the language.

The reason it works in Lisp specifically is **homoiconicity**: a Lisp program
*is* a Lisp data structure. `(if a b c)` is a list of four symbols. A macro
is therefore just a function from lists to lists, written in the same
language, using the same list operations you use for everything else.

    python3 lisp.py              # the demonstrations
    python3 lisp.py -            # a REPL
    python3 lisp.py file.lisp

**There is no parser in this file worth the name.** `read` turns text into
nested Python lists in about thirty lines, and that is the entire front end,
because the surface syntax and the data structure are the same thing. Weeks
1 and 2 spent a fortnight on the part Lisp declines to have.
"""
import sys
from itertools import count


class LispError(Exception):
    pass


class Symbol(str):
    """A name. Distinct from a string so that `'foo` and `"foo"` differ."""
    __slots__ = ()


def S(name):
    return Symbol(name)


QUOTE, IF, DEFINE, LAMBDA, DEFMACRO = map(
    S, ('quote', 'if', 'define', 'lambda', 'defmacro'))
QUASI, UNQUOTE, UNQUOTE_SPLICING = map(S, ('quasiquote', 'unquote',
                                           'unquote-splicing'))
BEGIN, SETQ = S('begin'), S('set!')


# ------------------------------------------------------------------ reading
def tokenize(src):
    out, i = [], 0
    while i < len(src):
        c = src[i]
        if c == ';':
            while i < len(src) and src[i] != '\n':
                i += 1
        elif c in '()':
            out.append(c); i += 1
        elif c == "'":
            out.append("'"); i += 1
        elif c == '`':
            out.append('`'); i += 1
        elif c == ',':
            if src[i:i + 2] == ',@':
                out.append(',@'); i += 2
            else:
                out.append(','); i += 1
        elif c == '"':
            j = i + 1
            while j < len(src) and src[j] != '"':
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1]); i = j + 1
        elif c.isspace():
            i += 1
        else:
            j = i
            while j < len(src) and not src[j].isspace() and src[j] not in '()':
                j += 1
            out.append(src[i:j]); i = j
    return out


def atom(tok):
    if tok.startswith('"'):
        return tok[1:-1]
    try:
        return int(tok)
    except ValueError:
        pass
    try:
        return float(tok)
    except ValueError:
        return S(tok)


READER_MACROS = {"'": QUOTE, '`': QUASI, ',': UNQUOTE, ',@': UNQUOTE_SPLICING}


def read_from(toks):
    if not toks:
        raise LispError("unexpected end of input")
    t = toks.pop(0)
    if t in READER_MACROS:
        return [READER_MACROS[t], read_from(toks)]
    if t == '(':
        out = []
        while toks and toks[0] != ')':
            out.append(read_from(toks))
        if not toks:
            raise LispError("missing )")
        toks.pop(0)
        return out
    if t == ')':
        raise LispError("unexpected )")
    return atom(t)


def read(src):
    """Text -> nested Python lists. **This is the whole front end.**"""
    toks = tokenize(src)
    forms = []
    while toks:
        forms.append(read_from(toks))
    return forms


def write(x):
    if isinstance(x, list):
        return '(' + ' '.join(map(write, x)) + ')'
    if x is True:
        return '#t'
    if x is False:
        return '#f'
    if x is None:
        return 'nil'
    if isinstance(x, Symbol):
        return str(x)
    if isinstance(x, str):
        return f'"{x}"'
    if isinstance(x, Lambda):
        return f"<lambda {write(x.params)}>"
    if isinstance(x, Macro):
        return f"<macro {write(x.params)}>"
    if callable(x):
        return f"<builtin {getattr(x, '__name__', '?')}>"
    return str(x)


# -------------------------------------------------------------- environment
class Env(dict):
    """A scope, chained to its parent -- Week 3's `Scope`, in nine lines.

    `params` may end with a REST parameter, written `(a b . rest)`: the name
    after the dot collects everything left over. A macro like `while` needs
    it, because a loop body is an arbitrary number of forms.
    """

    def __init__(self, params=(), args=(), parent=None):
        params, args = list(params), list(args)
        if S('.') in params:
            i = params.index(S('.'))
            fixed, rest = params[:i], params[i + 1]
            if len(args) < len(fixed):
                raise LispError(f"expected at least {len(fixed)} args, "
                                f"got {len(args)}")
            super().__init__(zip(fixed, args))
            self[rest] = args[len(fixed):]
        else:
            if len(params) != len(args):
                raise LispError(f"expected {len(params)} args, "
                                f"got {len(args)}")
            super().__init__(zip(params, args))
        self.parent = parent

    def find(self, name):
        if name in self:
            return self
        if self.parent is None:
            raise LispError(f"unbound symbol: {name}")
        return self.parent.find(name)


class Lambda:
    __slots__ = ('params', 'body', 'env')

    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env


class Macro:
    """Identical to `Lambda` in every respect except **when** it runs and
    whether its arguments were evaluated first. That is the entire
    difference, and it is the subject of this week."""

    __slots__ = ('params', 'body', 'env')

    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env


# ------------------------------------------------------------ macroexpansion
_gensym = count()


def macroexpand_1(form, env):
    """Expand the outermost macro call, once. Returns (form, expanded?)."""
    if not isinstance(form, list) or not form:
        return form, False
    head = form[0]
    if isinstance(head, Symbol):
        try:
            m = env.find(head)[head]
        except LispError:
            return form, False
        if isinstance(m, Macro):
            # THE line. The arguments go in UNEVALUATED -- as the syntax the
            # programmer wrote, not as the values it would produce.
            local = Env(m.params, form[1:], m.env)
            return eval_seq(m.body, local), True
    return form, False


def macroexpand(form, env, limit=200):
    """Expand repeatedly until it is no longer a macro call."""
    for _ in range(limit):
        form, did = macroexpand_1(form, env)
        if not did:
            return form
    raise LispError("macro expansion did not terminate")


def macroexpand_all(form, env):
    """Expand everywhere, recursively. What `python3 lisp.py` prints to show
    that the macro is gone by the time anything runs."""
    form = macroexpand(form, env)
    if isinstance(form, list) and form and form[0] not in (QUOTE,):
        return [form[0]] + [macroexpand_all(x, env) for x in form[1:]] \
            if isinstance(form[0], Symbol) and form[0] in (IF, DEFINE, LAMBDA,
                                                           BEGIN, SETQ) \
            else [macroexpand_all(x, env) for x in form]
    return form


# ------------------------------------------------------------------ eval
def eval_seq(body, env):
    r = None
    for f in body:
        r = leval(f, env)
    return r


def leval(x, env):
    while True:
        if isinstance(x, Symbol):
            return env.find(x)[x]
        if not isinstance(x, list):
            return x                       # numbers, strings, booleans
        if not x:
            return []

        head = x[0]

        if head is QUOTE or head == QUOTE:
            return x[1]
        if head == IF:
            _, test, conseq, *alt = x
            # Only ONE branch is evaluated. This is a special form in the
            # evaluator; section 3 of L21 is about how to get it without one.
            x = conseq if leval(test, env) not in (False, None) \
                else (alt[0] if alt else None)
            continue
        if head == DEFINE:
            _, name, expr = x
            env[name] = leval(expr, env)
            return name
        if head == SETQ:
            _, name, expr = x
            env.find(name)[name] = leval(expr, env)
            return None
        if head == LAMBDA:
            return Lambda(x[1], x[2:], env)
        if head == DEFMACRO:
            _, name, params, *body = x
            env[name] = Macro(params, body, env)
            return name
        if head == BEGIN:
            for f in x[1:-1]:
                leval(f, env)
            x = x[-1]
            continue
        if head == QUASI:
            return quasi(x[1], env)

        # a macro call expands before anything is evaluated
        if isinstance(head, Symbol):
            try:
                maybe = env.find(head)[head]
            except LispError:
                maybe = None
            if isinstance(maybe, Macro):
                x = macroexpand(x, env)
                continue

        fn = leval(head, env)
        args = [leval(a, env) for a in x[1:]]
        if isinstance(fn, Lambda):
            env = Env(fn.params, args, fn.env)
            for f in fn.body[:-1]:
                leval(f, env)
            x = fn.body[-1]
            continue                       # tail call, without growing the stack
        if callable(fn):
            return fn(*args)
        raise LispError(f"not callable: {write(fn)}")


def quasi(x, env):
    """Backquote: build a list, evaluating only the `,` and `,@` parts.

    This is what makes macros readable. Without it a macro body is a pile of
    `(list (quote if) ...)` calls; with it, the macro looks like the code it
    produces, with holes.
    """
    if not isinstance(x, list) or not x:
        return x
    if x[0] == UNQUOTE:
        return leval(x[1], env)
    out = []
    for item in x:
        if isinstance(item, list) and item and item[0] == UNQUOTE_SPLICING:
            out.extend(leval(item[1], env))
        else:
            out.append(quasi(item, env))
    return out


# --------------------------------------------------------------- primitives
def global_env():
    import operator as op
    e = Env()
    e.update({
        S('+'): lambda *a: sum(a),
        S('-'): lambda a, *b: -a if not b else a - sum(b),
        S('*'): lambda *a: __import__('math').prod(a),
        S('/'): op.floordiv, S('%'): op.mod,
        S('='): op.eq, S('<'): op.lt, S('>'): op.gt,
        S('<='): op.le, S('>='): op.ge,
        S('not'): lambda a: a in (False, None),
        S('list'): lambda *a: list(a),
        S('cons'): lambda a, b: [a] + b,
        S('car'): lambda a: a[0],
        S('cdr'): lambda a: a[1:],
        S('null?'): lambda a: a == [],
        S('pair?'): lambda a: isinstance(a, list) and len(a) > 0,
        S('symbol?'): lambda a: isinstance(a, Symbol),
        S('append'): lambda *a: [x for l in a for x in l],
        S('length'): len,
        S('print'): lambda *a: print('  ' + ' '.join(map(write, a))) or None,
        S('gensym'): lambda: S(f"g{next(_gensym)}"),
        S('#t'): True, S('#f'): False, S('nil'): None,
        # Deliberately available so that L21 section 3 can compare a macro
        # against a function on identical inputs.
        S('boom'): lambda *a: (_ for _ in ()).throw(
            LispError("boom was evaluated")),
    })
    return e


def run(src, env=None):
    env = env if env is not None else global_env()
    r = None
    for form in read(src):
        r = leval(form, env)
    return r, env


def main(argv):
    if len(argv) > 1 and argv[1] == '-':
        env = global_env()
        while True:
            try:
                line = input('lisp> ')
            except EOFError:
                return 0
            try:
                print(' ', write(run(line, env)[0]))
            except (LispError, Exception) as e:
                print(f"  error: {e}")
    if len(argv) > 1:
        src = open(argv[1]).read()
        print(write(run(src)[0]))
        return 0

    import demo
    return demo.main()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
