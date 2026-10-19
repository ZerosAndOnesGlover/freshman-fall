CC = gcc

# Clean programs: the lab's required flags, including -Werror.
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11 -g

# Demonstrative files whose warnings / undefined behaviour are the POINT of the
# exercise (Parts 1A and 2), so -Werror is deliberately omitted. UBSan catches
# the Part 2B/2C UB at run time.
DEMOFLAGS = -Wall -Wextra -pedantic -std=c11 -g -fsanitize=undefined

PROGRAMS = fallthrough collatz dowhile wordcount
DEMOS    = precedence ub overflow shift

all: $(PROGRAMS)

demos: $(DEMOS)

$(PROGRAMS): %: %.c
	$(CC) $(CFLAGS) -o $@ $<

$(DEMOS): %: %.c
	$(CC) $(DEMOFLAGS) -o $@ $<

clean:
	rm -f $(PROGRAMS) $(DEMOS)

.PHONY: all demos clean
