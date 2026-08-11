#!/bin/sh
# Lab 1 -- build the flex lexer and diff it against the hand-written one.
set -e
: "${1?usage: ./compare.sh FILE.cy}"

flex -o cyan_lex.c cyan.l
gcc -o cyanlex cyan_lex.c

./cyanlex   < "$1" > flex.out   2>&1 || true
python3 lexer.py "$1" > hand.out 2>&1 || true

if diff -u flex.out hand.out > delta.txt; then
    printf 'IDENTICAL -- %s tokens\n' "$(wc -l < flex.out)"
else
    printf 'DIFFER:\n'
    cat delta.txt
fi
