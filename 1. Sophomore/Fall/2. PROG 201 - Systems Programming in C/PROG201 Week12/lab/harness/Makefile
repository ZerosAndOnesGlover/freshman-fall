# PROG 201 Week 12 -- test harness. Provided; build with `make`.
CC     = cc
CFLAGS = -Wall -Wextra -O2 -std=gnu11 -pthread

all: bench rudeclient

bench: bench.c
	$(CC) $(CFLAGS) -o $@ $<
rudeclient: rudeclient.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f bench rudeclient

.PHONY: all clean
