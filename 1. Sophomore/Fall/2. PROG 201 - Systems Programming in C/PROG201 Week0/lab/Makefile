# PROG 201 · Lab 0
# Build with: make          Clean with: make clean
# -Wall -Wextra is not optional in this course, and -g is what makes gdb useful.

CC      = gcc
CFLAGS  = -Wall -Wextra -O2 -g -std=c11

all: supervisor flaky

supervisor: supervisor.c
	$(CC) $(CFLAGS) -o $@ $<

flaky: flaky.c
	$(CC) $(CFLAGS) -o $@ $<

# Part B: a child that crashes and a child that crash-loops.
demo-crash: all
	./supervisor a:crash b:flap

# Part C: start this, then send SIGTERM to the supervisor from another terminal.
demo-stop: all
	./supervisor ok:ok h:hang

clean:
	rm -f supervisor flaky core core.*

.PHONY: all clean demo-crash demo-stop
