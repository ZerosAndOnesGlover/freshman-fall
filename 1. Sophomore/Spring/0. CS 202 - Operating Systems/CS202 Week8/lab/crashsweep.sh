#!/bin/sh
# crashsweep.sh — stop a file-system operation after every possible number of block
# writes, then check what the image looks like. With a working journal, every crash
# point must leave either the state before the operation or the state after it.
#   ./crashsweep.sh ./myfsj base.img recover create /d/y
#   ./crashsweep.sh ./myfs  base.img norecover create /d/y
# The checker is always ./myfsj fsck, which detects orphaned inodes and leaked blocks.
# CS 202 Week 8, Lab 8 and PS 8.
[ $# -lt 4 ] && { echo "usage: $0 IMPL BASE_IMAGE recover|norecover COMMAND [ARGS]"; exit 1; }
IMPL=$1; BASE=$2; MODE=$3; shift 3
n=1
while [ $n -le 400 ]; do
  cp "$BASE" probe.img
  "$IMPL" probe.img crash $n "$@" >/dev/null 2>&1
  [ $? -ne 3 ] && break
  n=$((n + 1))
done
W=$n
old=0; new=0; bad=0
n=1
while [ $n -lt $W ]; do
  cp "$BASE" t.img
  "$IMPL" t.img crash $n "$@" >/dev/null 2>&1
  [ "$MODE" = recover ] && "$IMPL" t.img recover >/dev/null 2>&1
  if ./myfsj t.img fsck >/dev/null 2>&1; then
    if "$IMPL" t.img stat "$2" >/dev/null 2>&1; then new=$((new + 1)); else old=$((old + 1)); fi
  else
    bad=$((bad + 1))
    echo "  crash after $n writes: $(./myfsj t.img fsck 2>/dev/null | tail -1)"
  fi
  n=$((n + 1))
done
rm -f probe.img t.img
echo "$W writes to complete; $((W - 1)) crash points: $old before, $new after, $bad inconsistent"
