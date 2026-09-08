#!/bin/bash
# usage: ./bench.sh <mode> <port> <conc> <total> [workers] [block_us] [spin_us]
# Starts the server, runs the load generator against it, and stops the server.
MODE=$1; PORT=$2; CONC=$3; TOTAL=$4; W=${5:-8}; B=${6:-0}; S=${7:-0}
./server "$MODE" "$PORT" "$W" 512 "$B" "$S" 2>/dev/null &
SRV=$!
sleep 0.4
printf "%-8s " "$MODE"
./load "$PORT" "$CONC" "$TOTAL" 4
kill $SRV 2>/dev/null; wait $SRV 2>/dev/null
sleep 0.2
