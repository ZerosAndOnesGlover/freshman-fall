# PROG 201 · Lab 1
CC     = gcc
CFLAGS = -Wall -Wextra -O2 -g -std=c11

all: pipeline

pipeline: pipeline.c
	$(CC) $(CFLAGS) -o $@ $<

# Part A: two stages.
demo2: pipeline
	./pipeline ls -1 /etc : wc -l

# Part B: three stages, against the shell's own answer.
demo3: pipeline
	./compare.sh

clean:
	rm -f pipeline

.PHONY: all clean demo2 demo3
