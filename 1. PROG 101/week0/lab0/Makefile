CC = gcc
CFLAGS = -Wall -Wextra -Werror -g -std=c11

all: hello temperature

hello: hello.c
	$(CC) $(CFLAGS) -o $@ $<

temperature: temperature.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f hello temperature *.o *.i *.s

.PHONY: all clean
