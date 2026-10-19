CC = gcc
CFLAGS = -Wall -Wextra -g -std=c11

PROGRAMS = limits predictions floats overflow

all: $(PROGRAMS)

floats: floats.c
	$(CC) $(CFLAGS) -o $@ $< -lm

overflow: overflow.c
	$(CC) $(CFLAGS) -fsanitize=undefined -o $@ $<

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS)

.PHONY: all clean
