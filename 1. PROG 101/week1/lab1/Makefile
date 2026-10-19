CC = gcc
CFLAGS = -Wall -Wextra -g -O0 -std=c11

PROGRAMS = explore sizes

all: $(PROGRAMS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS)

.PHONY: all clean
