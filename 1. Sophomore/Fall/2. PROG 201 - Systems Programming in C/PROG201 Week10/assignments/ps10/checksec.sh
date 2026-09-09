#!/bin/bash
# A checksec(1) in ten lines -- the real tool is not installed.
# Reports the four mitigations on an ELF binary.
b="${1:?usage: checksec.sh BINARY}"
canary=$(objdump -d "$b" 2>/dev/null | grep -qc stack_chk && echo yes || echo NO)
nx=$(readelf -l "$b" 2>/dev/null | grep -A1 GNU_STACK | grep -q RWE && echo "NO (exec stack)" || echo yes)
pie=$(readelf -h "$b" 2>/dev/null | grep -q 'Type:.*DYN' && echo yes || echo "NO (fixed base)")
relro=$(readelf -l "$b" 2>/dev/null | grep -q GNU_RELRO && { readelf -d "$b" 2>/dev/null | grep -q BIND_NOW && echo full || echo partial; } || echo NO)
printf "%s:\n  Canary : %s\n  NX     : %s\n  PIE    : %s\n  RELRO  : %s\n" "$b" "$canary" "$nx" "$pie" "$relro"
