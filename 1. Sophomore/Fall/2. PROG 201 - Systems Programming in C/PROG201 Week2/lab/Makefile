CFLAGS = -Wall -Wextra -O2 -g -std=c11
LDLIBS = -lrt -lpthread

all: bench

bench: bench.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

# The three runs the lab asks for.
bulk: bench
	./bench bulk 256 4096

trip: bench
	./bench trip 100000

slots: bench
	./bench slots 256 4096

# Leftover IPC objects from a crashed run.  See L08 section 4.
clean-ipc:
	-rm -f /dev/shm/prog201* /dev/shm/sem.prog201* /dev/mqueue/prog201* /tmp/prog201.*

clean: clean-ipc
	rm -f bench

.PHONY: all bulk trip slots clean clean-ipc
