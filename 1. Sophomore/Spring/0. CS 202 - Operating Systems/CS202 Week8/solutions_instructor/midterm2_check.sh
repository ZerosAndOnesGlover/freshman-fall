#!/bin/sh
# midterm2_check.sh — every figure on Midterm 2 and in its mark scheme, checked against
# the course's own reference programs and by arithmetic. Run before printing the paper.
#   cd "CS202 Week8/solutions_instructor" && ./midterm2_check.sh
# CS 202 Week 8, Midterm 2.
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

# ---- Q1(b): the Banker's state on the paper (max rows first, then allocation rows)
cat > "$TMP/q1b.txt" <<'STATE'
4 3
1 1 2
3 2 2
6 1 3
3 1 4
4 2 2
1 0 0
5 1 1
2 1 1
0 0 2
request 3 1 1 0
request 1 1 0 2
STATE
out=$("$TMP/banker" < "$TMP/q1b.txt")
check "Q1(b) safe sequence" "state is SAFE; one safe sequence: <P1, P2, P3, P0>" "$(echo "$out" | sed -n 1p)"
check "Q1(b) P3 (1,1,0) refused" "request P3 (1,1,0): DENIED: would be unsafe" "$(echo "$out" | sed -n 2p)"
check "Q1(b) P1 (1,0,2) granted" "request P1 (1,0,2): GRANTED" "$(echo "$out" | sed -n 3p)"
check "Q1(b) available after" "  available now (0,1,0)  state is SAFE; one safe sequence: <P1, P2, P3, P0>" "$(echo "$out" | sed -n 4p)"

# ---- Q4(a),(b): page replacement on the paper's string
printf '7\n0\n1\n2\n0\n3\n0\n4\n2\n3\n0\n3\n' > "$TMP/q4a.txt"
check "Q4(a) FIFO, 3 frames"  "10" "$("$TMP/pagesim" fifo 3 < "$TMP/q4a.txt" | awk 'NR==3{print $2}')"
check "Q4(a) LRU, 3 frames"   "9"  "$("$TMP/pagesim" lru  3 < "$TMP/q4a.txt" | awk 'NR==3{print $2}')"
check "Q4(a) OPT, 3 frames"   "7"  "$("$TMP/pagesim" opt  3 < "$TMP/q4a.txt" | awk 'NR==3{print $2}')"
check "Q4(b) FIFO, 4 frames"  "7"  "$("$TMP/pagesim" fifo 4 < "$TMP/q4a.txt" | awk 'NR==3{print $2}')"
printf '1\n2\n3\n4\n1\n2\n5\n1\n2\n3\n4\n5\n' > "$TMP/q4b.txt"
check "Q4(b) anomaly string, FIFO 3" "9"  "$("$TMP/pagesim" fifo 3 < "$TMP/q4b.txt" | awk 'NR==3{print $2}')"
check "Q4(b) anomaly string, FIFO 4" "10" "$("$TMP/pagesim" fifo 4 < "$TMP/q4b.txt" | awk 'NR==3{print $2}')"

# ---- the arithmetic on the rest of the paper
py=$(python3 - <<'PY'
print("Q2a_pdx", (0x00C03004 >> 22) & 0x3FF)
print("Q2a_ptx", (0x00C03004 >> 12) & 0x3FF)
print("Q2a_off", 0x00C03004 & 0xFFF)
print("Q2b_sparse_pages", 64 + 1)
print("Q2b_sparse_kib", (64 + 1) * 4)
print("Q2b_dense_pages", (1 << 30) // 4096 // 512 + 1)
print("Q2b_dense_kib", ((1 << 30) // 4096 // 512 + 1) * 4)
print("Q2c_reach_4k_mib", 1536 * 4 // 1024)
print("Q2c_reach_2m_gib", 1536 * 2 // 1024)
print("Q2c_eat95", round(0.95 * 1 + 0.05 * 20, 2))
print("Q2c_breakeven", round((20 - 8) / 19, 2))
print("Q3b_faults", (1 << 30) // 4096)
print("Q3b_seconds", round((1 << 30) // 4096 * 2.7e-6, 2))
print("Q3c_total", 1028 + 2 + 1 + 64 + 1)
print("Q3c_userpages", 4210688 // 4096)
print("Q4d_A", round(2 / 3 * (1000 + 0 + 4096 / 12288 * 1000)))
print("Q4d_B", round(2 / 3 * (1000 + 500 + 200 / 12288 * 1000)))
print("Q5a_max", (12 + 128) * 512)
print("Q5a_blocks", -(-20000 // 512) + 1)
print("Q5c_cold", round(10000 * 93.9e-6, 2))
print("Q5c_warm", round(10000 * 1.61e-6, 3))
print("Q5d_each", round(10000 * 3.9e-3, 1))
print("Q5d_batched", round(100 * 3.9e-3, 2))
PY
)
get() { echo "$py" | awk -v k="$1" '$1==k{print $2}'; }
check "Q2(a) directory index"        "3"     "$(get Q2a_pdx)"
check "Q2(a) table index"            "3"     "$(get Q2a_ptx)"
check "Q2(a) offset"                 "4"     "$(get Q2a_off)"
check "Q2(b) sparse pages"           "65"    "$(get Q2b_sparse_pages)"
check "Q2(b) sparse KiB"             "260"   "$(get Q2b_sparse_kib)"
check "Q2(b) dense pages"            "513"   "$(get Q2b_dense_pages)"
check "Q2(b) dense KiB"              "2052"  "$(get Q2b_dense_kib)"
check "Q2(c) 4 KiB reach (MiB)"      "6"     "$(get Q2c_reach_4k_mib)"
check "Q2(c) 2 MiB reach (GiB)"      "3"     "$(get Q2c_reach_2m_gib)"
check "Q2(c) EAT at 95%"             "1.95"  "$(get Q2c_eat95)"
check "Q2(c) break-even hit rate"    "0.63"  "$(get Q2c_breakeven)"
check "Q3(b) COW faults"             "262144" "$(get Q3b_faults)"
check "Q3(b) seconds of faults"      "0.71"  "$(get Q3b_seconds)"
check "Q3(c) fork pages"             "1096"  "$(get Q3c_total)"
check "Q3(c) user pages"             "1028"  "$(get Q3c_userpages)"
check "Q4(d) score A"                "889"   "$(get Q4d_A)"
check "Q4(d) score B"                "1011"  "$(get Q4d_B)"
check "Q5(a) largest file"           "71680" "$(get Q5a_max)"
check "Q5(a) blocks for 20,000"      "41"    "$(get Q5a_blocks)"
check "Q5(c) cold pass (s)"          "0.94"  "$(get Q5c_cold)"
check "Q5(c) warm pass (s)"          "0.016" "$(get Q5c_warm)"
check "Q5(d) fsync per record (s)"   "39.0"  "$(get Q5d_each)"
check "Q5(d) batched (s)"            "0.39"  "$(get Q5d_batched)"

[ $fail -eq 0 ] && echo "ALL CHECKS PASSED" || { echo "SOME CHECKS FAILED"; exit 1; }
