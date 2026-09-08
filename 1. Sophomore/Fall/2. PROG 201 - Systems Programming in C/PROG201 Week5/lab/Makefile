CFLAGS = -Wall -Wextra -O2 -g -std=c11
LDLIBS = -lpthread

all: server load hold nagle

nagle: nagle.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

hold: hold.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

server: server.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

load: load.c
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

clean:
	rm -f server load hold nagle

.PHONY: all clean
