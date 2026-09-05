#!/usr/bin/env python3
"""Recursive descent parser for Cyan. Consumes tokens from lexer.py, produces an AST.

One function per non-terminal, exactly as the grammar reads -- except where the
grammar is left-recursive, which recursive descent cannot handle directly. Those
become loops; see parse_add_expr.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lexer import tokenize, Token, LexError


class ParseError(Exception):
    pass


# ---------------------------------------------------------------- AST nodes
class Node:
    """An AST node. `line` and `col` come from the token that started the
    construct -- Week 3's type checker needs them, and they cannot be
    recovered later."""

    def __init__(self, kind, line=0, col=0, **kw):
        self.kind = kind
        self.line = line
        self.col = col
        self.__dict__.update(kw)

    def __repr__(self):
        fields = {k: v for k, v in self.__dict__.items()
                  if k not in ('kind', 'line', 'col')}
        inner = ', '.join(f"{k}={v!r}" for k, v in fields.items())
        return f"{self.kind}({inner})"


class Parser:
    def __init__(self, tokens):
        self.toks = tokens
        self.i = 0

    # -------------------------------------------------------- token helpers
    def pos(self):
        """Line and column of the current token, for attaching to a node."""
        t = self.peek()
        if t is None and self.toks:
            t = self.toks[-1]
        return (t.line, t.col) if t else (0, 0)

    def peek(self, ahead=0):
        j = self.i + ahead
        return self.toks[j] if j < len(self.toks) else None

    def at(self, kind, text=None):
        t = self.peek()
        return t is not None and t.kind == kind and (text is None or t.text == text)

    def eat(self, kind, text=None):
        if not self.at(kind, text):
            got = self.peek()
            want = f"{kind}" + (f" '{text}'" if text else "")
            where = f"line {got.line} col {got.col}" if got else "end of input"
            found = f"{got.kind} '{got.text}'" if got else "end of input"
            raise ParseError(f"{where}: expected {want}, found {found}")
        t = self.toks[self.i]
        self.i += 1
        return t

    def accept(self, kind, text=None):
        if self.at(kind, text):
            self.i += 1
            return True
        return False

    # ------------------------------------------------------------ program
    def parse_program(self):
        decls = []
        while self.peek() is not None:
            decls.append(self.parse_decl())
        return Node('Program', decls=decls)

    def parse_decl(self):
        if self.at('KEYWORD', 'fn'):
            return self.parse_fn_decl()
        if self.at('KEYWORD', 'struct'):
            return self.parse_struct_decl()
        if self.at('KEYWORD', 'let'):
            return self.parse_let()
        t = self.peek()
        raise ParseError(f"line {t.line}: expected a declaration, found '{t.text}'")

    def parse_fn_decl(self):
        ln, cl = self.pos()
        self.eat('KEYWORD', 'fn')
        name = self.eat('IDENT').text
        self.eat('PUNCT', '(')
        params = [] if self.at('PUNCT', ')') else self.parse_params()
        self.eat('PUNCT', ')')
        ret = None
        if self.accept('OP', '->'):
            ret = self.parse_type()
        body = self.parse_block()
        return Node('Fn', line=ln, col=cl, name=name, params=params, ret=ret, body=body)

    def parse_struct_decl(self):
        ln, cl = self.pos()
        self.eat('KEYWORD', 'struct')
        name = self.eat('IDENT').text
        self.eat('PUNCT', '{')
        fields = []
        while not self.at('PUNCT', '}'):
            fname = self.eat('IDENT').text
            self.eat('PUNCT', ':')
            fields.append((fname, self.parse_type()))
            self.eat('PUNCT', ';')
        self.eat('PUNCT', '}')
        return Node('Struct', line=ln, col=cl, name=name, fields=fields)

    def parse_params(self):
        params = [self.parse_param()]
        while self.accept('PUNCT', ','):
            params.append(self.parse_param())
        return params

    def parse_param(self):
        name = self.eat('IDENT').text
        self.eat('PUNCT', ':')
        return (name, self.parse_type())

    # -------------------------------------------------------------- types
    def parse_type(self):
        for prim in ('int', 'bool', 'string'):
            if self.accept('KEYWORD', prim):
                return Node('TyPrim', name=prim)
        if self.accept('PUNCT', '['):
            inner = self.parse_type()
            self.eat('PUNCT', ']')
            return Node('TyArray', of=inner)
        if self.accept('KEYWORD', 'fn'):
            self.eat('PUNCT', '(')
            args = []
            if not self.at('PUNCT', ')'):
                args.append(self.parse_type())
                while self.accept('PUNCT', ','):
                    args.append(self.parse_type())
            self.eat('PUNCT', ')')
            self.eat('OP', '->')
            return Node('TyFn', args=args, ret=self.parse_type())
        if self.at('IDENT'):
            return Node('TyName', name=self.eat('IDENT').text)
        t = self.peek()
        raise ParseError(f"line {t.line}: expected a type, found '{t.text}'")

    # --------------------------------------------------------- statements
    def parse_block(self):
        ln, cl = self.pos()
        self.eat('PUNCT', '{')
        stmts = []
        while not self.at('PUNCT', '}'):
            if self.peek() is None:
                raise ParseError("unexpected end of input inside a block")
            stmts.append(self.parse_stmt())
        self.eat('PUNCT', '}')
        return Node('Block', line=ln, col=cl, stmts=stmts)

    def parse_stmt(self):
        ln, cl = self.pos()
        if self.at('KEYWORD', 'let'):
            return self.parse_let()
        if self.at('KEYWORD', 'if'):
            return self.parse_if()
        if self.at('KEYWORD', 'while'):
            return self.parse_while()
        if self.at('KEYWORD', 'return'):
            return self.parse_return()

        # assign_stmt vs expr_stmt: parse an expression, then look for '='.
        # An lvalue is a subset of postfix, so we check the shape afterwards.
        start = self.i
        e = self.parse_expr()
        if self.at('OP', '='):
            if not self.is_lvalue(e):
                t = self.toks[start]
                raise ParseError(
                    f"line {t.line}: left-hand side of '=' is not assignable")
            self.eat('OP', '=')
            rhs = self.parse_expr()
            self.eat('PUNCT', ';')
            return Node('Assign', line=ln, col=cl, target=e, value=rhs)
        self.eat('PUNCT', ';')
        return Node('ExprStmt', line=ln, col=cl, expr=e)

    @staticmethod
    def is_lvalue(node):
        if node.kind == 'Var':
            return True
        if node.kind == 'Index':
            return Parser.is_lvalue(node.arr)
        if node.kind == 'Field':
            return Parser.is_lvalue(node.obj)
        return False

    def parse_let(self):
        ln, cl = self.pos()
        self.eat('KEYWORD', 'let')
        name = self.eat('IDENT').text
        ty = self.parse_type() if self.accept('PUNCT', ':') else None
        self.eat('OP', '=')
        val = self.parse_expr()
        self.eat('PUNCT', ';')
        return Node('Let', line=ln, col=cl, name=name, ty=ty, value=val)

    def parse_if(self):
        ln, cl = self.pos()
        self.eat('KEYWORD', 'if')
        cond = self.parse_expr()
        then = self.parse_block()
        els = None
        if self.accept('KEYWORD', 'else'):
            els = self.parse_if() if self.at('KEYWORD', 'if') else self.parse_block()
        return Node('If', line=ln, col=cl, cond=cond, then=then, els=els)

    def parse_while(self):
        ln, cl = self.pos()
        self.eat('KEYWORD', 'while')
        cond = self.parse_expr()
        return Node('While', line=ln, col=cl, cond=cond, body=self.parse_block())

    def parse_return(self):
        ln, cl = self.pos()
        self.eat('KEYWORD', 'return')
        if self.accept('PUNCT', ';'):
            return Node('Return', line=ln, col=cl, value=None)
        v = self.parse_expr()
        self.eat('PUNCT', ';')
        return Node('Return', line=ln, col=cl, value=v)

    # -------------------------------------------------------- expressions
    # The grammar is left-recursive at every binary level. Recursive descent
    # cannot call itself first, so each left-recursive rule becomes a loop --
    # which is exactly what left-recursion elimination produces, folded back
    # into iteration. Looping left-to-right gives left associativity.
    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        node = self.parse_and()
        while self.at('OP', '||'):
            ln, cl = self.pos()
            self.eat('OP', '||')
            node = Node('Binary', line=ln, col=cl, op='||', lhs=node,
                        rhs=self.parse_and())
        return node

    def parse_and(self):
        node = self.parse_cmp()
        while self.at('OP', '&&'):
            ln, cl = self.pos()
            self.eat('OP', '&&')
            node = Node('Binary', line=ln, col=cl, op='&&', lhs=node,
                        rhs=self.parse_cmp())
        return node

    CMP = {'==', '!=', '<', '<=', '>', '>='}

    def parse_cmp(self):
        node = self.parse_add()
        if self.peek() and self.peek().kind == 'OP' and self.peek().text in self.CMP:
            ln, cl = self.pos()
            op = self.eat('OP').text
            rhs = self.parse_add()
            node = Node('Binary', line=ln, col=cl, op=op, lhs=node, rhs=rhs)
            # non-associative: a second comparison is a syntax error
            if self.peek() and self.peek().kind == 'OP' and self.peek().text in self.CMP:
                t = self.peek()
                raise ParseError(
                    f"line {t.line}: comparison is non-associative; "
                    f"write 'a {op} b && b {t.text} c'")
        return node

    def parse_add(self):
        node = self.parse_mul()
        while self.peek() and self.peek().kind == 'OP' and self.peek().text in ('+', '-'):
            ln, cl = self.pos()
            op = self.eat('OP').text
            node = Node('Binary', line=ln, col=cl, op=op, lhs=node,
                        rhs=self.parse_mul())
        return node

    def parse_mul(self):
        node = self.parse_unary()
        while self.peek() and self.peek().kind == 'OP' and self.peek().text in ('*', '/', '%'):
            ln, cl = self.pos()
            op = self.eat('OP').text
            node = Node('Binary', line=ln, col=cl, op=op, lhs=node,
                        rhs=self.parse_unary())
        return node

    def parse_unary(self):
        if self.peek() and self.peek().kind == 'OP' and self.peek().text in ('-', '!'):
            ln, cl = self.pos()
            op = self.eat('OP').text
            return Node('Unary', line=ln, col=cl, op=op,
                        operand=self.parse_unary())
        return self.parse_postfix()

    def parse_postfix(self):
        node = self.parse_primary()
        while True:
            ln, cl = self.pos()
            if self.at('PUNCT', '('):
                self.eat('PUNCT', '(')
                args = []
                if not self.at('PUNCT', ')'):
                    args.append(self.parse_expr())
                    while self.accept('PUNCT', ','):
                        args.append(self.parse_expr())
                self.eat('PUNCT', ')')
                node = Node('Call', line=ln, col=cl, fn=node, args=args)
            elif self.at('PUNCT', '['):
                self.eat('PUNCT', '[')
                idx = self.parse_expr()
                self.eat('PUNCT', ']')
                node = Node('Index', line=ln, col=cl, arr=node, index=idx)
            elif self.at('PUNCT', '.'):
                self.eat('PUNCT', '.')
                node = Node('Field', line=ln, col=cl, obj=node, name=self.eat('IDENT').text)
            else:
                return node

    def parse_primary(self):
        ln, cl = self.pos()
        t = self.peek()
        if t is None:
            raise ParseError("unexpected end of input in an expression")
        if t.kind == 'INT':
            self.i += 1
            return Node('Int', line=ln, col=cl, value=int(t.text))
        if t.kind == 'STRING':
            self.i += 1
            return Node('Str', line=ln, col=cl, value=t.text)
        if t.kind == 'IDENT':
            self.i += 1
            return Node('Var', line=ln, col=cl, name=t.text)
        if self.at('KEYWORD', 'true') or self.at('KEYWORD', 'false'):
            self.i += 1
            return Node('Bool', line=ln, col=cl, value=(t.text == 'true'))
        if self.accept('PUNCT', '('):
            e = self.parse_expr()
            self.eat('PUNCT', ')')
            return e                       # no Paren node -- L01 section 4
        if self.at('PUNCT', '['):
            self.eat('PUNCT', '[')
            items = []
            if not self.at('PUNCT', ']'):
                items.append(self.parse_expr())
                while self.accept('PUNCT', ','):
                    items.append(self.parse_expr())
            self.eat('PUNCT', ']')
            return Node('Array', line=ln, col=cl, items=items)
        if self.at('KEYWORD', 'new'):
            self.eat('KEYWORD', 'new')
            name = self.eat('IDENT').text
            self.eat('PUNCT', '{')
            inits = []
            if not self.at('PUNCT', '}'):
                while True:
                    f = self.eat('IDENT').text
                    self.eat('PUNCT', ':')
                    inits.append((f, self.parse_expr()))
                    if not self.accept('PUNCT', ','):
                        break
            self.eat('PUNCT', '}')
            return Node('New', line=ln, col=cl, name=name, inits=inits)
        if self.at('KEYWORD', 'fn'):
            self.eat('KEYWORD', 'fn')
            self.eat('PUNCT', '(')
            params = [] if self.at('PUNCT', ')') else self.parse_params()
            self.eat('PUNCT', ')')
            ret = self.parse_type() if self.accept('OP', '->') else None
            return Node('Lambda', line=ln, col=cl, params=params, ret=ret, body=self.parse_block())
        raise ParseError(f"line {t.line} col {t.col}: unexpected '{t.text}'")


def parse(src):
    return Parser(tokenize(src)).parse_program()


def dump(node, indent=0):
    pad = '  ' * indent
    if isinstance(node, Node):
        fields = {k: v for k, v in node.__dict__.items()
                  if k not in ('kind', 'line', 'col')}
        simple = {k: v for k, v in fields.items()
                  if not isinstance(v, (Node, list)) or not v}
        print(f"{pad}{node.kind}" + (f" {simple}" if simple else ""))
        for k, v in fields.items():
            if isinstance(v, Node):
                print(f"{pad}  .{k}:"); dump(v, indent + 2)
            elif isinstance(v, list) and v:
                print(f"{pad}  .{k}:")
                for item in v:
                    if isinstance(item, Node):
                        dump(item, indent + 2)
                    elif isinstance(item, tuple):
                        print(f"{pad}    {item[0]}:")
                        if isinstance(item[1], Node):
                            dump(item[1], indent + 3)


if __name__ == '__main__':
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    try:
        dump(parse(src))
    except (LexError, ParseError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
