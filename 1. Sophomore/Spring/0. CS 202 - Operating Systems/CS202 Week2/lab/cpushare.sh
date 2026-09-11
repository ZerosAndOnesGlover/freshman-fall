#!/bin/bash
# cpushare.sh: how much CPU did each of these processes get over the next few seconds?
#
#   ./cpushare.sh 4 <pid> <pid> ...      measure for 4 seconds
#
# Reads utime + stime (fields 14 and 15 of /proc/<pid>/stat, in clock ticks)
# before and after, and prints each process's share of the total.
# CS 202 Lab 2.
secs=$1; shift
declare -A before
for p in "$@"; do before[$p]=$(awk '{print $14 + $15}' /proc/$p/stat); done
sleep "$secs"
total=0
declare -A used
for p in "$@"; do
    used[$p]=$(( $(awk '{print $14 + $15}' /proc/$p/stat) - ${before[$p]} ))
    total=$(( total + ${used[$p]} ))
done
for p in "$@"; do
    printf "pid %-8s nice %3s  policy %-6s  %4d ticks  %5.1f%%\n" "$p" \
        "$(awk '{print $19}' /proc/$p/stat)" "$(chrt -p $p | head -1 | awk '{print $NF}')" \
        "${used[$p]}" "$(echo "scale=1; 100 * ${used[$p]} / ($total + 0.0001)" | bc)"
done
