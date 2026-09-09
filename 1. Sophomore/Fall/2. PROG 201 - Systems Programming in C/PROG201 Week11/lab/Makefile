# LAB 11 -- containers from primitives. `make` builds all four; none needs root.
CC     = cc
CFLAGS = -Wall -Wextra -O2 -std=gnu11

BINS = minic hog sec cost

all: $(BINS)

minic: minic.c
	$(CC) $(CFLAGS) -o $@ $<
hog: hog.c
	$(CC) $(CFLAGS) -o $@ $<
sec: sec.c
	$(CC) $(CFLAGS) -o $@ $<
cost: cost.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(BINS)

.PHONY: all clean
