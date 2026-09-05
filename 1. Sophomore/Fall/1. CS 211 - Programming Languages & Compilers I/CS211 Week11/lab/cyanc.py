#!/usr/bin/env python3
"""cyanc -- the whole compiler, one command.

Eleven weeks of phases, wired together and given a driver:

    0  lexer.py       source     -> tokens
    1  parser.py      tokens     -> AST
    2  typecheck.py   AST        -> typed AST        (+ the first phase that says no)
    3  tac.py         typed AST  -> three-address code
    4  tac.py         TAC        -> control-flow graph
    5  opt.py         CFG        -> optimised CFG
    6  live.py        CFG        -> liveness         (registers, and GC roots)
    7  regalloc.py    liveness   -> register assignment
    8  llvmgen.py     TAC        -> LLVM IR
    9  llc / lli      LLVM IR    -> x86-64, or JIT

Usage:

    python3 cyanc.py FILE.cy                    # compile, report every phase
    python3 cyanc.py FILE.cy --emit=tac         # stop and print one phase
    python3 cyanc.py FILE.cy --run 1071 462     # JIT it with lli and print the result
    python3 cyanc.py FILE.cy -o prog            # native executable via clang
    python3 cyanc.py FILE.cy --opt              # let LLVM optimise, and say what it did

`--emit` takes: tokens, ast, tac, cfg, opt, live, regs, llvm.

**This file adds no compilation of its own.** It is a driver: argument
parsing, phase sequencing, and reporting. That is what a compiler driver is
-- `gcc` is mostly this, and the thing people call "the compiler" is `cc1`.
"""
import argparse
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from lexer import tokenize, LexError
from parser import parse, ParseError
from typecheck import Checker, TypeError_
from tac import TAC, build_cfg, dump, dump_cfg
import live as L
import opt as O
import regalloc as RA
from llvmgen import compile_to_llvm, Unsupported


def rule(t):
    print(f"; ---- {t} ----")


def phase_times():
    return {}


def compile_file(path, want=None, emit=None, verbose=True):
    """Run every phase, reporting as it goes. Returns the LLVM IR."""
    src = open(path).read()
    times = {}

    def timed(name, fn):
        t0 = time.perf_counter()
        r = fn()
        times[name] = time.perf_counter() - t0
        return r

    # 0 -------------------------------------------------------------- lex
    toks = timed('lex', lambda: tokenize(src))
    if emit == 'tokens':
        for t in toks:
            print(f"  {t.kind:<8} {t.text!r}")
        return None, times
    if verbose:
        rule(f"0. lexer: {len(toks)} tokens")

    # 1 ------------------------------------------------------------ parse
    ast = timed('parse', lambda: parse(src))
    fns = [d for d in ast.decls if d.kind == 'Fn']
    if emit == 'ast':
        print(f"  {len(ast.decls)} declarations")
        for d in ast.decls:
            print(f"  {d.kind:<8} {getattr(d, 'name', '?')}")
        return None, times
    if verbose:
        rule(f"1. parser: {len(ast.decls)} declarations, "
             f"{len(fns)} functions")

    # 2 ------------------------------------------------------ type check
    def check():
        c = Checker()
        c.check_program(ast)
        return c
    checker = timed('typecheck', check)
    if verbose:
        rule(f"2. type checker: ok, {len(checker.structs)} struct(s)")

    target = next((f for f in fns if f.name == want), fns[0]) if fns else None
    if target is None:
        raise SystemExit("no functions to compile")

    # 3 -------------------------------------------------------------- TAC
    def gen():
        t = TAC()
        t.gen_fn(target)
        return t.code
    code = timed('tac', gen)
    L.check_coverage(code)
    if emit == 'tac':
        dump(code)
        return None, times
    if verbose:
        rule(f"3. TAC for {target.name}: {len(code)} instructions")

    # 4 -------------------------------------------------------------- CFG
    blocks = timed('cfg', lambda: build_cfg(code))
    if emit == 'cfg':
        dump_cfg(blocks)
        return None, times
    if verbose:
        edges = sum(len(b.succs) for b in blocks)
        rule(f"4. CFG: {len(blocks)} basic blocks, {edges} edges")

    # 5 -------------------------------------------------- our optimiser
    before = len(code)
    # `O.optimise` returns (code, log) -- a TUPLE. An earlier version of this
    # driver bound the pair and reported `len(...)` of it, which is 2, and
    # duly announced "12 -> 2 instructions (83% removed)" for every program
    # in the folder. A plausible number, measuring the arity of a tuple.
    opt_code, opt_log = timed('opt', lambda: O.optimise(list(code)))
    if emit == 'opt':
        dump(opt_code)
        for line in opt_log:
            print(f"; {line}")
        return None, times
    if verbose:
        rule(f"5. our optimiser: {before} -> {len(opt_code)} instructions "
             f"({100 * (before - len(opt_code)) // max(before, 1)}% removed)")

    # 6 --------------------------------------------------------- liveness
    IN, OUT, rounds = timed('live', lambda: L.liveness(blocks))
    if emit == 'live':
        for b in blocks:
            print(f"  {b.name:<10} IN {sorted(IN[b.name])} "
                  f"OUT {sorted(OUT[b.name])}")
        return None, times
    if verbose:
        peak = max((len(s) for s in OUT.values()), default=0)
        rule(f"6. liveness: fixed point in {rounds} rounds, "
             f"peak {peak} simultaneously live")

    # 7 ------------------------------------------------ register allocation
    if verbose or emit == 'regs':
        try:
            g = RA.interference(blocks)
            nodes = len(g)
            edges = sum(len(v) for v in g.values()) // 2
            if emit == 'regs':
                for v in sorted(g):
                    print(f"  {v:<6} interferes with {sorted(g[v])}")
                return None, times
            rule(f"7. interference graph: {nodes} nodes, {edges} edges")
        except Exception as e:
            if emit == 'regs':
                raise
            rule(f"7. register allocation: skipped ({type(e).__name__})")

    # 8 ------------------------------------------------------------- LLVM
    # Pass the AST we already have: otherwise this phase silently
    # re-parses and re-type-checks, and the timing table lies.
    ir = timed('llvm', lambda: compile_to_llvm(src, target.name, ast))
    if emit == 'llvm':
        print(ir)
        return ir, times
    if verbose:
        body = [l for l in ir.split('\n') if l.startswith('  ')]
        rule(f"8. LLVM IR: {len(body)} instructions "
             f"({sum('alloca' in l for l in body)} alloca, "
             f"{sum(l.strip().startswith(('%', 'store')) and ('load' in l or 'store' in l) for l in body)} load/store)")
    return ir, times


def run_llvm(ir, fn, args, native=None, optimise=False):
    """Hand the IR to LLVM: `lli` to JIT it, or `clang` for a binary."""
    with tempfile.TemporaryDirectory() as d:
        ll = os.path.join(d, 'mod.ll')
        open(ll, 'w').write(ir)

        if optimise:
            out = os.path.join(d, 'opt.ll')
            subprocess.run(['opt', '-O2', '-S', ll, '-o', out], check=True)
            before = sum(1 for l in open(ll) if l.startswith('  '))
            after = sum(1 for l in open(out) if l.startswith('  '))
            rule(f"opt -O2: {before} -> {after} instructions "
                 f"({100 * (before - after) // max(before, 1)}% removed)")
            ll = out

        # a `main` that calls the function with the given arguments
        argv = ', '.join(f"i64 {a}" for a in args)
        main = os.path.join(d, 'main.ll')
        open(main, 'w').write(
            f'define i32 @main() {{\n'
            f'  %r = call i64 @{fn}({argv})\n'
            f'  %t = trunc i64 %r to i32\n'
            f'  ret i32 %t\n}}\n')

        combined = os.path.join(d, 'all.ll')
        with open(combined, 'w') as f:
            f.write(open(ll).read())
            f.write(open(main).read())

        if native:
            subprocess.run(['clang', '-O2', combined, '-o', native],
                           check=True)
            rule(f"native executable: {native}")
            r = subprocess.run([os.path.abspath(native)])
            print(f"  exit code {r.returncode}  = {fn}({', '.join(map(str, args))})")
            return r.returncode

        t0 = time.perf_counter()
        r = subprocess.run(['lli', combined])
        dt = time.perf_counter() - t0
        rule(f"lli (JIT): exit code {r.returncode} "
             f"= {fn}({', '.join(map(str, args))})   [{dt * 1000:.0f} ms]")
        return r.returncode


def main(argv):
    ap = argparse.ArgumentParser(prog='cyanc', description=__doc__.split('\n')[0])
    ap.add_argument('file')
    ap.add_argument('args', nargs='*', type=int,
                    help="arguments, if --run or -o is given")
    ap.add_argument('--fn', help="which function to compile (default: first)")
    ap.add_argument('--emit', choices=['tokens', 'ast', 'tac', 'cfg', 'opt',
                                       'live', 'regs', 'llvm'])
    ap.add_argument('--run', action='store_true', help="JIT it with lli")
    ap.add_argument('-o', dest='native', help="build a native executable")
    ap.add_argument('--opt', action='store_true', help="run LLVM's -O2 first")
    ap.add_argument('--times', action='store_true', help="report phase times")
    a = ap.parse_args(argv[1:])

    try:
        ir, times = compile_file(a.file, a.fn, a.emit,
                                 verbose=a.emit is None)
    except (LexError, ParseError, TypeError_) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except Unsupported as e:
        print(f"error: unsupported: {e}", file=sys.stderr)
        return 3

    if a.times:
        rule("phase times")
        total = sum(times.values())
        for k, v in times.items():
            print(f"  {k:<12} {v * 1000:7.2f} ms  {100 * v / total:5.1f}%")
        print(f"  {'total':<12} {total * 1000:7.2f} ms")

    if ir and (a.run or a.native):
        fn = a.fn or 'main'
        # find the emitted function's name from the IR
        for line in ir.split('\n'):
            if line.startswith('define'):
                fn = line.split('@')[1].split('(')[0]
                break
        return run_llvm(ir, fn, a.args, a.native, a.opt)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
