CFLAGS = -Wall -Wextra -O2 -g -std=c11

all: jit

jit: jit.c
	$(CC) $(CFLAGS) -o $@ $<

# Part A and B
run: jit
	./jit

# Part C
wx: jit
	./jit wx

# Part D
bench: jit
	./jit bench

# Disassemble what you emitted -- see section 2 of the lab sheet.
dis: jit
	@echo "run ./jit and paste the hex into: echo <hex> | xxd -r -p > /tmp/code.bin"
	@echo "then: objdump -D -b binary -m i386:x86-64 /tmp/code.bin"

clean:
	rm -f jit

.PHONY: all run wx bench dis clean
