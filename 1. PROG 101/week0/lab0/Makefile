# Makefile for compiling C programs

# CCompiler to use
CC = gcc

# Compiler flags
CFLAGS = -Wall -Wextra -Werror -g -std=c11

# Default target
all: hello temperature

# Build rules for the hello program
hello: hello.c
	$(CC) $(CFLAGS) -o $@ $<

# Build rules for the temperature program
temperature: temperature.c
	$(CC) $(CFLAGS) -o $@ $<

# Clean up build artifacts
clean:
	rm -f hello temperature *.o *.i *.s

# .PHONY target to avoid conflicts with files named 'all' or 'clean'
.PHONY: all clean
