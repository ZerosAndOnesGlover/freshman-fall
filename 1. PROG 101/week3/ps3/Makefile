CC = gcc
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c11 -g

stats: main.o stats.o
	$(CC) $(CFLAGS) -o $@ main.o stats.o -lm

# Both objects list stats.h as a prerequisite, so touching stats.h
# rebuilds BOTH; touching main.c rebuilds only main.o.
main.o: main.c stats.h
	$(CC) $(CFLAGS) -c main.c -o $@

stats.o: stats.c stats.h
	$(CC) $(CFLAGS) -c stats.c -o $@

clean:
	rm -f stats *.o

.PHONY: clean
