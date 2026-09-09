# PS 11 -- must build warning-clean; do NOT commit the binary.
CC     = cc
CFLAGS = -Wall -Wextra -O2 -std=gnu11

container: container.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f container

.PHONY: clean
