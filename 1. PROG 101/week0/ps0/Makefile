# Makefile for PS 0: builds info, hello, fixed and greet.
# broken.c is deliberately not built: it is the Problem 4 exhibit.

CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

.PHONY: all clean test

all: info hello fixed greet

# Single-file programs: $@ is the target, $< the first prerequisite.
info: info.c
	$(CC) $(CFLAGS) -o $@ $<

hello: hello.c
	$(CC) $(CFLAGS) -o $@ $<

fixed: fixed.c
	$(CC) $(CFLAGS) -o $@ $<

# Problem 5: link greet from both objects; $^ is all prerequisites.
greet: main.o greet.o
	$(CC) $(CFLAGS) -o $@ $^

# Each object depends on its .c AND on greet.h, so a header change
# rebuilds both (see make_report.md, 5.3).
main.o: main.c greet.h
	$(CC) $(CFLAGS) -c -o $@ $<

greet.o: greet.c greet.h
	$(CC) $(CFLAGS) -c -o $@ $<

test: all
	@echo "Testing info..."
	./info
	@echo "Testing hello..."
	./hello
	@echo "Testing fixed..."
	./fixed
	@echo "Testing greet..."
	./greet
	@echo "All tests passed."

clean:
	rm -f info hello fixed greet *.o *.i *.s
