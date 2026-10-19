CC     = gcc
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11 -g

# Built by `make all`. bad.c and dangling.c are deliberately broken, so they
# are not part of the default build (see the targets below).
PROGRAMS = stack pbv duration prog

all: $(PROGRAMS)

# --- single-file programs -------------------------------------------
stack:    stack.c
	$(CC) $(CFLAGS) -o $@ $<
pbv:      pbv.c
	$(CC) $(CFLAGS) -o $@ $<
duration: duration.c
	$(CC) $(CFLAGS) -o $@ $<

# --- multi-file program: separate compilation -----------------------
prog: main.o mathutil.o
	$(CC) $(CFLAGS) -o $@ main.o mathutil.o

main.o:     main.c     mathutil.h
	$(CC) $(CFLAGS) -c main.c -o main.o

mathutil.o: mathutil.c mathutil.h
	$(CC) $(CFLAGS) -c mathutil.c -o mathutil.o

# --- Part 4A: assertion demo (assertions active and compiled out) ---
asrt: asrt.c mathutil.c mathutil.h
	$(CC) $(CFLAGS) -o $@ asrt.c mathutil.c

asrt_ndebug: asrt.c mathutil.c mathutil.h
	$(CC) $(CFLAGS) -DNDEBUG -o $@ asrt.c mathutil.c

clean:
	rm -f $(PROGRAMS) asrt asrt_ndebug *.o

.PHONY: all clean
