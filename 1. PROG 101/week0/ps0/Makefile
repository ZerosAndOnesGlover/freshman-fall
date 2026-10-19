# Makefile — PROG 101, Week 0, Problem Set 0
# Builds every program in the set with strict flags.
#
#   make        build info, hello, fixed, greet
#   make test   build, then run quick sanity checks
#   make clean  remove all build products

CC      = gcc
CFLAGS  = -Wall -Wextra -Werror -g -std=c11

.PHONY: all clean test

all: info hello fixed greet

info: info.o
	$(CC) $(CFLAGS) $^ -o $@

hello: hello.o
	$(CC) $(CFLAGS) $^ -o $@

fixed: fixed.o
	$(CC) $(CFLAGS) $^ -o $@

greet: main.o greet.o
	$(CC) $(CFLAGS) $^ -o $@

# main.o and greet.o include greet.h, so a header edit must rebuild them.
main.o greet.o: greet.h

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

test: all
	@echo "Testing info..."
	./info
	@echo "Testing greet..."
	./greet
	@echo "All tests passed."

clean:
	rm -f info hello fixed greet *.o *.i *.s
