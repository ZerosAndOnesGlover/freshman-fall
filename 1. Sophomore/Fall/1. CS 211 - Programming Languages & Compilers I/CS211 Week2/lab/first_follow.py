"""Week 2 verification: FIRST/FOLLOW sets, LL(1) tables, and conflict detection."""
EPS = 'ε'


def first_sets(g, terminals):
    first = {nt: set() for nt in g}
    changed = True
    while changed:
        changed = False
        for nt, prods in g.items():
            for prod in prods:
                if not prod:                       # A -> ε
                    if EPS not in first[nt]:
                        first[nt].add(EPS); changed = True
                    continue
                for sym in prod:
                    if sym in terminals:
                        if sym not in first[nt]:
                            first[nt].add(sym); changed = True
                        break
                    add = first[sym] - {EPS}
                    if not add <= first[nt]:
                        first[nt] |= add; changed = True
                    if EPS not in first[sym]:
                        break
                else:                              # every symbol nullable
                    if EPS not in first[nt]:
                        first[nt].add(EPS); changed = True
    return first


def first_of_seq(seq, first, terminals):
    out = set()
    for sym in seq:
        if sym in terminals:
            out.add(sym); return out
        out |= first[sym] - {EPS}
        if EPS not in first[sym]:
            return out
    out.add(EPS)
    return out


def follow_sets(g, start, first, terminals):
    follow = {nt: set() for nt in g}
    follow[start].add('$')
    changed = True
    while changed:
        changed = False
        for nt, prods in g.items():
            for prod in prods:
                for i, sym in enumerate(prod):
                    if sym in terminals:
                        continue
                    rest = prod[i + 1:]
                    add = first_of_seq(rest, first, terminals) if rest else {EPS}
                    if EPS in add:
                        add = (add - {EPS}) | follow[nt]
                    if not add <= follow[sym]:
                        follow[sym] |= add; changed = True
    return follow


def ll1_table(g, start, terminals):
    first = first_sets(g, terminals)
    follow = follow_sets(g, start, first, terminals)
    table, conflicts = {}, []
    for nt, prods in g.items():
        for prod in prods:
            f = first_of_seq(prod, first, terminals) if prod else {EPS}
            targets = set(f - {EPS})
            if EPS in f:
                targets |= follow[nt]
            for t in targets:
                key = (nt, t)
                if key in table and table[key] != prod:
                    conflicts.append((nt, t, table[key], prod))
                else:
                    table[key] = prod
    return first, follow, table, conflicts


def show(name, g, start, terminals):
    first, follow, table, conflicts = ll1_table(g, start, terminals)
    print(f"\n=== {name} ===")
    for nt in g:
        f = ', '.join(sorted(first[nt]))
        fo = ', '.join(sorted(follow[nt]))
        print(f"  FIRST({nt:<3}) = {{ {f} }}".ljust(46) + f"FOLLOW({nt:<3}) = {{ {fo} }}")
    if conflicts:
        print(f"  --> NOT LL(1): {len(conflicts)} conflict(s)")
        for nt, t, a, b in conflicts:
            print(f"      {nt} on '{t}': {a or ('ε',)}  vs  {b or ('ε',)}")
    else:
        print(f"  --> LL(1). Table has {len(table)} entries.")
    return conflicts


TERM = set('+-*/()n')

# The natural left-recursive expression grammar -- NOT LL(1)
left_rec = {
    'E': [('E', '+', 'T'), ('T',)],
    'T': [('T', '*', 'F'), ('F',)],
    'F': [('n',), ('(', 'E', ')')],
}
show("Left-recursive E ::= E + T | T", left_rec, 'E', TERM)

# After eliminating left recursion -- IS LL(1)
no_left_rec = {
    'E':  [('T', "E'")],
    "E'": [('+', 'T', "E'"), ()],
    'T':  [('F', "T'")],
    "T'": [('*', 'F', "T'"), ()],
    'F':  [('n',), ('(', 'E', ')')],
}
show("After left-recursion elimination", no_left_rec, 'E', TERM)

# Needing left factoring
TERM2 = set(['if', 'e', 's', 'else', '$'])
unfactored = {
    'S': [('if', 'e', 'S'), ('if', 'e', 'S', 'else', 'S'), ('s',)],
}
show("Dangling else (unfactored)", unfactored, 'S', TERM2)

factored = {
    'S':  [('if', 'e', 'S', "S'"), ('s',)],
    "S'": [('else', 'S'), ()],
}
show("Dangling else (left-factored)", factored, 'S', TERM2)
