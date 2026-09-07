CFLAGS = -Wall -Wextra -O2 -g -std=c11
LDLIBS = -lpthread

all: rtcheck inversion

rtcheck: rtcheck.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

inversion: inversion.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

# Part B, the baseline.  A few seconds.
baseline: inversion
	./inversion

# Part C, the bug.  ABOUT A HUNDRED SECONDS.  That is the result.
bug: inversion
	./inversion m

# Part D, the fixes.
fixes: inversion
	./inversion m nice0
	./inversion m chunks=100
	./inversion m chunks=1000
	./inversion m nice0 chunks=100

clean:
	rm -f rtcheck inversion

.PHONY: all baseline bug fixes clean
