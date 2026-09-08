#!/bin/bash
# PROG 201 -- Lab 7: is the filesystem still what it should be?
# Checks structure with e2fsck and contents with debugfs.  No mounting.
IMG=${1:-disk.img}
fail=0

check() {   # check <description> <command...>
    local what="$1"; shift
    if "$@" >/dev/null 2>&1; then
        printf '  ok    %s\n' "$what"
    else
        printf '  FAIL  %s\n' "$what"; fail=$((fail+1))
    fi
}

echo "=== structure ==="
e2fsck -fn "$IMG" >/tmp/p201-fsck.out 2>&1
rc=$?
case $rc in
  0) echo "  ok    e2fsck: clean" ;;
  4) echo "  FAIL  e2fsck: errors left uncorrected (rc=4)"; fail=$((fail+1)) ;;
  8) echo "  FAIL  e2fsck: could not open the filesystem (rc=8)"; fail=$((fail+1)) ;;
  *) echo "  ??    e2fsck returned $rc" ;;
esac
grep -E '^(Inode|Entry|Block|Free|Padding|Unattached|Pass)' /tmp/p201-fsck.out |
    grep -v '^Pass' | sed 's/^/        /' | head -8

echo "=== contents ==="
check "/docs/note.txt exists"  bash -c "debugfs -R 'stat /docs/note.txt' '$IMG' 2>/dev/null | grep -q 'Type: regular'"
check "/alias.txt exists"      bash -c "debugfs -R 'stat /alias.txt' '$IMG' 2>/dev/null | grep -q 'Type: regular'"
check "they are the same inode" bash -c "
    a=\$(debugfs -R 'stat /docs/note.txt' '$IMG' 2>/dev/null | head -1 | awk '{print \$2}')
    b=\$(debugfs -R 'stat /alias.txt'    '$IMG' 2>/dev/null | head -1 | awk '{print \$2}')
    [ -n \"\$a\" ] && [ \"\$a\" = \"\$b\" ]"
check "link count is 2"        bash -c "debugfs -R 'stat /alias.txt' '$IMG' 2>/dev/null | grep -q 'Links: 2'"
check "/link.txt is a symlink" bash -c "debugfs -R 'stat /link.txt' '$IMG' 2>/dev/null | grep -q 'Fast link dest'"
check "/big.bin is 200000 B"   bash -c "debugfs -R 'stat /big.bin' '$IMG' 2>/dev/null | grep -q 'Size: 200000'"
check "/huge.bin is 5000000 B" bash -c "debugfs -R 'stat /huge.bin' '$IMG' 2>/dev/null | grep -q 'Size: 5000000'"
check "/huge.bin reads back"   bash -c "debugfs -R 'dump /huge.bin /tmp/p201-out.bin' '$IMG' 2>/dev/null && [ \$(stat -c%s /tmp/p201-out.bin) = 5000000 ]"
rm -f /tmp/p201-out.bin

echo
if [ $fail -eq 0 ]; then echo "all checks passed"; else echo "$fail check(s) failed"; fi
exit $fail
