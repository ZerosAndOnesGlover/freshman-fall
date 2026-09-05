#!/usr/bin/env python3
"""Hand-written lexer for Cyan. No regex library -- an explicit DFA loop."""
import sys

KEYWORDS = {'fn', 'let', 'if', 'else', 'while', 'return', 'struct', 'new',
            'true', 'false', 'int', 'bool', 'string'}

# Longest first, so maximal munch falls out of the ordering.
OPERATORS = ['==', '!=', '<=', '>=', '&&', '||', '->',
             '+', '-', '*', '/', '%', '<', '>', '!', '=']
PUNCT = list('(){}[],;:.')


class LexError(Exception):
    pass


class Token:
    __slots__ = ('kind', 'text', 'line', 'col')

    def __init__(self, kind, text, line, col):
        self.kind, self.text, self.line, self.col = kind, text, line, col

    def __repr__(self):
        return f"{self.kind}({self.text})"

    def __eq__(self, other):
        return (self.kind, self.text) == (other.kind, other.text)


def is_letter(c):
    return c.isascii() and (c.isalpha() or c == '_')


def is_digit(c):
    return c.isascii() and c.isdigit()


def tokenize(src):
    toks, i, line, col = [], 0, 1, 1
    n = len(src)

    def advance(k):
        nonlocal i, line, col
        for _ in range(k):
            if src[i] == '\n':
                line += 1
                col = 1
            else:
                col += 1
            i += 1

    while i < n:
        c = src[i]

        # --- whitespace ---
        if c in ' \t\r\n':
            advance(1)
            continue

        # --- comments ---
        if src.startswith('//', i):
            while i < n and src[i] != '\n':
                advance(1)
            continue
        if src.startswith('/*', i):
            start_line = line
            advance(2)
            while i < n and not src.startswith('*/', i):
                advance(1)
            if i >= n:
                raise LexError(f"unterminated block comment opened on line {start_line}")
            advance(2)
            continue

        start_line, start_col = line, col

        # --- identifiers and keywords ---
        if is_letter(c):
            j = i
            while j < n and (is_letter(src[j]) or is_digit(src[j])):
                j += 1
            text = src[i:j]
            advance(j - i)
            kind = 'KEYWORD' if text in KEYWORDS else 'IDENT'
            toks.append(Token(kind, text, start_line, start_col))
            continue

        # --- integers ---
        if is_digit(c):
            j = i
            while j < n and is_digit(src[j]):
                j += 1
            # An identifier may not start immediately after a digit: 12abc
            if j < n and is_letter(src[j]):
                raise LexError(f"line {line}: malformed number '{src[i:j+1]}'")
            text = src[i:j]
            advance(j - i)
            toks.append(Token('INT', text, start_line, start_col))
            continue

        # --- strings ---
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                if src[j] == '\n':
                    raise LexError(f"line {line}: newline in string literal")
                j += 2 if src[j] == '\\' else 1
            if j >= n:
                raise LexError(f"line {line}: unterminated string literal")
            text = src[i:j + 1]
            advance(j + 1 - i)
            toks.append(Token('STRING', text, start_line, start_col))
            continue

        # --- operators, maximal munch ---
        for op in OPERATORS:
            if src.startswith(op, i):
                advance(len(op))
                toks.append(Token('OP', op, start_line, start_col))
                break
        else:
            if c in PUNCT:
                advance(1)
                toks.append(Token('PUNCT', c, start_line, start_col))
            else:
                raise LexError(f"line {line} col {col}: unexpected character {c!r}")

    return toks


if __name__ == '__main__':
    src = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
    try:
        for t in tokenize(src):
            print(f"{t.kind}({t.text})")
    except LexError as e:
        print(f"lex error: {e}", file=sys.stderr)
        sys.exit(1)
