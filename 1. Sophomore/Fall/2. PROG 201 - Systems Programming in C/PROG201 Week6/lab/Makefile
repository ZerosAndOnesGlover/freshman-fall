CFLAGS = -Wall -Wextra -O2 -g -std=c11

all: tsh groups ttyctl groupsig

tsh: tsh.c
	$(CC) $(CFLAGS) -o $@ $<

groups: groups.c
	$(CC) $(CFLAGS) -o $@ $<

ttyctl: ttyctl.c
	$(CC) $(CFLAGS) -o $@ $<

groupsig: groupsig.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f tsh groups ttyctl groupsig

.PHONY: all clean
