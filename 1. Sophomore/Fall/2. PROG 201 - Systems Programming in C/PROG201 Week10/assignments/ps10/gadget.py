#!/usr/bin/env python3
"""A minimal ROP gadget finder. ROPgadget is not installed; this is ~40 lines
and finds the short sequences ending in RET (0xc3) that a chain needs."""
import subprocess, sys, re

def gadgets(binary, want):
    # disassemble the executable text with objdump
    out = subprocess.run(["objdump","-d","-M","intel",binary],
                         capture_output=True, text=True).stdout
    # collect (address, mnemonic) for .text
    insns = []
    for line in out.splitlines():
        m = re.match(r"\s+([0-9a-f]+):\t[0-9a-f ]+\t(.*)", line)
        if m:
            addr = int(m.group(1),16)
            mnem = re.sub(r"\s+"," ",m.group(2).split("#")[0].strip())
            insns.append((addr, mnem))
    # a gadget: a `ret` preceded by up to `depth` simple instructions
    found = {}
    for i,(addr,mn) in enumerate(insns):
        if mn == "ret":
            for depth in range(1,4):
                if i-depth < 0: break
                seq = [insns[i-depth+k][1] for k in range(depth)] + ["ret"]
                # reject anything with a call/jmp/leave in the middle
                if any(x.split()[0] in ("call","jmp","leave","je","jne") for x in seq[:-1]):
                    continue
                text = " ; ".join(seq)
                start = insns[i-depth][0]
                if want in text and text not in found:
                    found[text] = start
    return found

if __name__ == "__main__":
    b = sys.argv[1]; pat = sys.argv[2] if len(sys.argv)>2 else ""
    for text,addr in sorted(gadgets(b,pat).items(), key=lambda kv: kv[1]):
        print(f"0x{addr:016x}  {text}")
