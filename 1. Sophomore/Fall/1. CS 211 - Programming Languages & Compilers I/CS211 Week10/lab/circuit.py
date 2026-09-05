#!/usr/bin/env python3
"""A circuit DSL, twice: internal and external.

PS 10 asks for a DSL for describing circuits with a simulator behind it.
This file is the starting point and the argument, not the answer -- it
implements enough of both styles to make the trade-off concrete.

**Internal DSL** (`Circuit` below): a little language embedded in Python,
using operator overloading. Costs nothing to build, gets Python's tooling
for free, and is limited to what Python's grammar already permits.

**External DSL** (`parse_netlist`): its own syntax, its own parser, built
with the combinators from `combinators.py`. Says exactly what you want it
to say, and you now own a language.

    python3 circuit.py

The simulator is deliberately simple -- levelised evaluation over a DAG --
because the interesting part of this week is the *language*, not the
physics. PS 10 Part C asks you to add sequential logic, which is where the
DAG assumption stops holding.
"""
import sys
from itertools import product

from combinators import (Parser, regex, lit, seq, alt, many, lazy, Ok, Err)


# ------------------------------------------------------------ the netlist
class Node:
    """One wire. Built by the internal DSL's operators."""

    _n = 0

    def __init__(self, op, *inputs, name=None):
        self.op, self.inputs = op, inputs
        Node._n += 1
        self.name = name or f"n{Node._n}"

    # The internal DSL is these five lines.
    def __and__(self, o):
        return Node('and', self, o)

    def __or__(self, o):
        return Node('or', self, o)

    def __xor__(self, o):
        return Node('xor', self, o)

    def __invert__(self):
        return Node('not', self)

    def __repr__(self):
        if self.op == 'input':
            return self.name
        return f"({self.op} {' '.join(map(repr, self.inputs))})"


def inputs(names):
    return [Node('input', name=n) for n in names.split()]


GATES = {
    'and': lambda *a: all(a),
    'or': lambda *a: any(a),
    'xor': lambda *a: sum(a) % 2 == 1,
    'not': lambda a: not a,
    'nand': lambda *a: not all(a),
    'nor': lambda *a: not any(a),
}


# -------------------------------------------------------------- simulator
def evaluate(node, env, memo=None):
    """Evaluate one output under an assignment to the inputs.

    Memoised, which matters: a shared subexpression is a real wire, and
    without the memo a diamond-shaped circuit is evaluated exponentially.
    """
    memo = {} if memo is None else memo
    if id(node) in memo:
        return memo[id(node)]
    if node.op == 'input':
        v = env[node.name]
    else:
        v = GATES[node.op](*(evaluate(i, env, memo) for i in node.inputs))
    memo[id(node)] = v
    return v


def gate_count(*nodes, seen=None):
    """Distinct gates across ALL the given outputs, shared wires once.

    The `seen` set must be shared between outputs, not reset per output.
    A full adder's `sum` and `cout` both use `xor(a, b)` -- that is ONE
    gate with two consumers, and counting it twice reports 6 where the
    textbook says 5. Sharing is the whole reason the memo in `evaluate`
    exists, so the counter has to agree with it.
    """
    seen = set() if seen is None else seen
    total = 0
    for node in nodes:
        if id(node) in seen or node.op == 'input':
            continue
        seen.add(id(node))
        total += 1 + gate_count(*node.inputs, seen=seen)
    return total


def truth_table(outputs, ins):
    names = [n.name for n in ins]
    rows = []
    for bits in product([False, True], repeat=len(ins)):
        env = dict(zip(names, bits))
        rows.append((bits, tuple(evaluate(o, env) for o in outputs)))
    return names, rows


def show_table(label, outputs, ins, out_names):
    names, rows = truth_table(outputs, ins)
    print(f"\n  {label}")
    print(f"    {' '.join(f'{n:>3}' for n in names)} | "
          f"{' '.join(f'{n:>4}' for n in out_names)}")
    for bits, outs in rows:
        print(f"    {' '.join(f'{int(b):>3}' for b in bits)} | "
              f"{' '.join(f'{int(o):>4}' for o in outs)}")


# ----------------------------------------------------- the external DSL
#
#   netlist := decl+
#   decl    := 'in' NAME+ | NAME '=' gexpr
#   gexpr   := NAME | GATE '(' gexpr (',' gexpr)* ')'
#
NAME = regex(r'[A-Za-z_][A-Za-z_0-9]*', 'name')
GATE = alt(*[lit(g) for g in GATES])


def parse_netlist(src):
    """Text -> {name: Node}. An external DSL: its own syntax, its own parser.

    Note what this buys over the internal version: `nand(a, b)` is spelled
    the way an engineer would spell it, rather than `~(a & b)`. And note
    what it costs -- everything below this line.
    """
    env = {}

    def gexpr():
        call = (seq(GATE, lit('('), sep_args, lit(')'))
                >> (lambda v: Node(v[0], *v[2])))
        ref = NAME >> (lambda n: env[n] if n in env
                       else _undefined(n))
        return call | ref

    def _undefined(n):
        raise SyntaxError(f"undefined wire: {n}")

    sep_args = lazy(lambda: (seq(lazy(gexpr),
                                 many(seq(lit(','), lazy(gexpr))
                                      >> (lambda v: v[1])))
                             >> (lambda v: [v[0]] + v[1])))

    for line in src.strip().split('\n'):
        line = line.split('#')[0].strip()
        if not line:
            continue
        if line.startswith('in '):
            for n in line[3:].replace(',', ' ').split():
                env[n] = Node('input', name=n)
        else:
            lhs, _, rhs = line.partition('=')
            lhs = lhs.strip()
            node = gexpr().parse(rhs)
            node.name = lhs
            env[lhs] = node
    return env


# -------------------------------------------------------------------- main
def main():
    print("; ---- internal DSL: operator overloading ----")
    a, b, cin = inputs("a b cin")
    s1 = a ^ b
    total = s1 ^ cin
    carry = (a & b) | (s1 & cin)
    print(f"  sum   = {total!r}")
    print(f"  carry = {carry!r}")
    print(f"  gates, shared wires counted once: {gate_count(total, carry)}"
          f"   (2 xor + 2 and + 1 or; the first xor feeds both outputs)")
    show_table("full adder", [total, carry], [a, b, cin], ["sum", "cout"])

    print("\n  Five lines of Python built that language:")
    print("    __and__  __or__  __xor__  __invert__  and a Node class.")
    print("  No parser, no grammar, no new file format.")

    print("\n; ---- external DSL: its own syntax ----")
    src = """
      in a b cin
      s1   = xor(a, b)
      sum  = xor(s1, cin)
      c1   = and(a, b)
      c2   = and(s1, cin)
      cout = or(c1, c2)
    """
    print("  " + src.strip().replace('\n', '\n  '))
    net = parse_netlist(src)
    show_table("full adder, from the netlist",
               [net['sum'], net['cout']],
               [net['a'], net['b'], net['cin']], ["sum", "cout"])

    print("\n; ---- do they agree? ----")
    ins = [net['a'], net['b'], net['cin']]
    _, r1 = truth_table([total, carry], [a, b, cin])
    _, r2 = truth_table([net['sum'], net['cout']], ins)
    same = [x[1] for x in r1] == [x[1] for x in r2]
    print(f"  internal and external produce identical truth tables: {same}")

    print("\n; ---- what each one cost ----")
    print("  internal   5 operator methods, 0 lines of parser")
    print("  external   a grammar, a parser, and error messages you own")
    print("  internal   `nand(a,b)` must be spelled `~(a & b)`")
    print("  external   `nand(a, b)` is spelled the way it is spoken")
    print("  internal   Python's syntax errors, line numbers and debugger")
    print("  external   whatever diagnostics you are prepared to write")
    return 0 if same else 1


if __name__ == '__main__':
    sys.exit(main())
