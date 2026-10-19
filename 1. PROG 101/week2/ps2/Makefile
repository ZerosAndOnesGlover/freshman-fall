CC = gcc
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11

PROGRAMS = flags

all: $(PROGRAMS)

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS)

.PHONY: all clean
