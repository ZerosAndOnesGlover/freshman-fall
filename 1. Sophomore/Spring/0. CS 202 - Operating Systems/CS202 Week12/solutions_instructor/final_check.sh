#!/bin/sh
# final_check.sh — every figure on the Final Examination and in its mark scheme,
# checked against the course's own reference programs and by arithmetic.
# Run before printing the paper.
#   cd "CS202 Week12/solutions_instructor" && ./final_check.sh
# CS 202 Week 12, Final Examination.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
CS202=$(cd "$HERE/../.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0
check() { # check DESCRIPTION EXPECTED ACTUAL
  if [ "$2" = "$3" ]; then echo "ok   $1"; else echo "FAIL $1: expected [$2], got [$3]"; fail=1; fi
}

gcc -O2 -w -o "$TMP/banker" "$CS202/CS202 Week4/solutions_instructor/banker reference (do not distribute).c"
gcc -O2 -w -o "$TMP/pagesim" "$CS202/CS202 Week6/solutions_instructor/pagesim reference (do not distribute).c"

# ---- Q2(b),(c): the Banker's state on the paper (available, then all Max, then all Allocation)
cat > "$TMP/q2b.txt" <<'STATE'
4 3
2 1 2
4 2 3
3 3 3
5 1 4
2 2 2
1 0 2
2 1 1
3 0 2
0 1 1
request 0 2 1 0
request 2 2 1 2
STATE
out=$("$TMP/banker" < "$TMP/q2b.txt")
check "Q2(b)2 state is safe" "state is SAFE; one safe sequence: <P2, P3, P0, P1>" "$(echo "$out" | sed -n 1p)"
check "Q2(b)3 P0 (2,1,0) refused" "request P0 (2,1,0): DENIED: would be unsafe" "$(echo "$out" | sed -n 2p)"
check "Q2(c) P2 (2,1,2) granted" "request P2 (2,1,2): GRANTED" "$(echo "$out" | sed -n 3p)"
check "Q2(c) available is (0,0,0) and safe" \
  "  available now (0,0,0)  state is SAFE; one safe sequence: <P2, P3, P0, P1>" "$(echo "$out" | sed -n 4p)"

# ---- Q3(a): page replacement on the paper's string
printf '7\n0\n1\n2\n0\n3\n0\n4\n2\n3\n0\n3\n2\n1\n2\n0\n1\n7\n0\n1\n' > "$TMP/q3a.txt"
check "Q3(a) 20 references, 6 distinct" "20 references, 6 distinct pages" \
  "$("$TMP/pagesim" lru 3 < "$TMP/q3a.txt" | sed -n 1p)"
for alg in fifo lru opt; do
  for fr in 3 4; do
    eval "got_${alg}_${fr}=\$(\"\$TMP/pagesim\" \$alg \$fr < \"\$TMP/q3a.txt\" | awk 'NR==3{print \$2}')"
  done
done
check "Q3(a) FIFO 3 frames" "15" "$got_fifo_3"
check "Q3(a) LRU  3 frames" "12" "$got_lru_3"
check "Q3(a) OPT  3 frames" "9"  "$got_opt_3"
check "Q3(a) FIFO 4 frames" "10" "$got_fifo_4"
check "Q3(a) LRU  4 frames" "8"  "$got_lru_4"
check "Q3(a) OPT  4 frames" "8"  "$got_opt_4"

# ---- Belady's anomaly is NOT on this string, but IS on the one the scheme names
printf '1\n2\n3\n4\n1\n2\n5\n1\n2\n3\n4\n5\n' > "$TMP/belady.txt"
check "Q3(a)3 Belady string, FIFO 3" "9"  "$("$TMP/pagesim" fifo 3 < "$TMP/belady.txt" | awk 'NR==3{print $2}')"
check "Q3(a)3 Belady string, FIFO 4" "10" "$("$TMP/pagesim" fifo 4 < "$TMP/belady.txt" | awk 'NR==3{print $2}')"

# ---- the arithmetic on the rest of the paper
py=$(python3 - <<'PY'
B, PTRS = 512, 128
print("Q1b_calls_1byte", 16 * 1024 * 1024)
print("Q1b_secs_1byte", 16 * 1024 * 1024 // 1000000)
print("Q1b_calls_64k", 16 * 1024 * 1024 // (64 * 1024))
print("Q1b_ratio", (16 * 1024 * 1024) // (16 * 1024 * 1024 // (64 * 1024)))
print("Q3b_reach_4k_mib", 1536 * 4 // 1024)
print("Q3b_reach_2m_gib", 1536 * 2 // 1024)
print("Q4a_xv6_blocks", 12 + PTRS)
print("Q4a_xv6_bytes", (12 + PTRS) * B)
print("Q4a_p2_blocks", 11 + PTRS + PTRS * PTRS)
print("Q4a_p2_bytes", (11 + PTRS + PTRS * PTRS) * B)
print("Q4a_p2_meta", 2 + PTRS)   # indirect + double indirect + 128 second-level
print("Q5a_majority5", 5 // 2 + 1)
print("Q5a_tolerate5", 5 - (5 // 2 + 1))
print("Q5a_majority6", 6 // 2 + 1)
print("Q5a_tolerate6", 6 - (6 // 2 + 1))
PY
)
get() { echo "$py" | awk -v k="$1" '$1==k{print $2}'; }
check "Q1(b)1 system calls, 1 byte"   "16777216" "$(get Q1b_calls_1byte)"
check "Q1(b)1 seconds at 1 us each"   "16"       "$(get Q1b_secs_1byte)"
check "Q1(b)2 system calls, 64 KiB"   "256"      "$(get Q1b_calls_64k)"
check "Q1(b)3 ratio"                  "65536"    "$(get Q1b_ratio)"
check "Q3(b)1 TLB reach, 4 KiB (MiB)" "6"        "$(get Q3b_reach_4k_mib)"
check "Q3(b)1 TLB reach, 2 MiB (GiB)" "3"        "$(get Q3b_reach_2m_gib)"
check "Q4(a)1 xv6 blocks"             "140"      "$(get Q4a_xv6_blocks)"
check "Q4(a)1 xv6 bytes"              "71680"    "$(get Q4a_xv6_bytes)"
check "Q4(a)2 Project 2 blocks"       "16523"    "$(get Q4a_p2_blocks)"
check "Q4(a)2 Project 2 bytes"        "8459776"  "$(get Q4a_p2_bytes)"
check "Q4(a)2 metadata blocks"        "130"      "$(get Q4a_p2_meta)"
check "Q5(a)1 majority of 5"          "3"        "$(get Q5a_majority5)"
check "Q5(a)1 failures tolerated"     "2"        "$(get Q5a_tolerate5)"
check "Q5(a)2 majority of 6"          "4"        "$(get Q5a_majority6)"
check "Q5(a)2 failures tolerated"     "2"        "$(get Q5a_tolerate6)"

# ---- Q5(c)1: the UMIP claim, on the machine the paper was set on
cat > "$TMP/sgdt.c" <<'C'
#include <stdio.h>
int main(void){ unsigned char d[10]; __asm__ volatile("sgdt %0" : "=m"(d));
  unsigned long base=0; for(int i=9;i>=2;i--) base=(base<<8)|d[i];
  printf("%s\n", base ? "leaked" : "zero"); return 0; }
C
if gcc -O2 -w -o "$TMP/sgdt" "$TMP/sgdt.c" 2>/dev/null; then
  check "Q5(c)1 sgdt still leaks on this machine" "leaked" "$("$TMP/sgdt")"
else
  echo "skip Q5(c)1 (not x86)"
fi

echo
if [ "$fail" = 0 ]; then echo "ALL CHECKS PASSED"; else echo "SOME CHECKS FAILED"; exit 1; fi
