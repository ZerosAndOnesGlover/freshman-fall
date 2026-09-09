#!/bin/bash
# PROG 201 -- PS 9: does your optimised version still give the right answers,
# and how much faster is it?
#
#   ./check.sh ./slow ./fast words.txt
set -u
A=${1:-./slow}; B=${2:-./fast}; W=${3:-words.txt}

[ -f "$W" ] || { echo "no $W -- run: ./gen 400000 > words.txt"; exit 2; }

echo "=== correctness ==="
"$A" "$W" 2>/dev/null > /tmp/p201-a.out
"$B" "$W" 2>/dev/null > /tmp/p201-b.out
if diff -q /tmp/p201-a.out /tmp/p201-b.out >/dev/null; then
    echo "  ok    output is identical"
else
    echo "  FAIL  output differs:"
    diff /tmp/p201-a.out /tmp/p201-b.out | head -6
    exit 1
fi

echo "=== speed (best of 5) ==="
best() {
    local prog=$1 b=99999
    for i in 1 2 3 4 5; do
        local t
        t=$( { /usr/bin/env time -f "%e" "$prog" "$W" >/dev/null; } 2>&1 | tail -1 )
        b=$(python3 -c "print(min($b,$t))")
    done
    echo "$b"
}
ta=$(best "$A"); tb=$(best "$B")
printf "  %-20s %8s s\n" "$A" "$ta"
printf "  %-20s %8s s\n" "$B" "$tb"
python3 -c "
a=$ta; b=$tb
print(f'  speedup{chr(58)} {a/b if b>0 else 0:.2f}x')
print('  ' + ('PASSES the 5x requirement' if b>0 and a/b>=5 else 'does NOT yet reach 5x'))"
