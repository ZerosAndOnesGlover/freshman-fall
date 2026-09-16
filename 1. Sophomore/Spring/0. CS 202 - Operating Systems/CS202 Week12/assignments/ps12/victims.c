/* victims.c -- things for a jail to stop.  Week 12, PS 12 test material.
   Build: gcc -O2 -Wall -Wextra -o victim victims.c
   Run:   victim spin | grab | open | fork | socket | quiet */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/socket.h>

int main(int argc, char **argv)
{
	const char *what = argc > 1 ? argv[1] : "quiet";

	if (!strcmp(what, "spin")) {
		volatile double x = 1.0;
		for (;;) x = x * 1.0000001 + 1.0;
	}
	if (!strcmp(what, "grab")) {
		size_t total = 0;
		for (;;) {
			char *p = malloc(1 << 20);
			if (!p) {
				printf("malloc failed after %zu MiB\n", total);
				return 1;
			}
			memset(p, 1, 1 << 20);
			total++;
			if (total > 4096) {
				printf("took 4 GiB without complaint\n");
				return 0;
			}
		}
	}
	if (!strcmp(what, "open")) {
		int n = 0;
		for (;;) {
			if (open("/dev/null", O_RDONLY) < 0) {
				printf("open failed after %d descriptors: %s\n", n, strerror(errno));
				return 1;
			}
			n++;
			if (n > 100000) { printf("opened 100000\n"); return 0; }
		}
	}
	if (!strcmp(what, "fork")) {
		int n = 0;
		for (;;) {
			pid_t p = fork();
			if (p == 0) { sleep(30); _exit(0); }
			if (p < 0) {
				printf("fork failed after %d children: %s\n", n, strerror(errno));
				return 1;
			}
			n++;
			if (n > 200) { printf("forked 200\n"); return 0; }
		}
	}
	if (!strcmp(what, "socket")) {
		int s = socket(AF_INET, SOCK_DGRAM, 0);
		printf("socket() = %d%s%s\n", s, s < 0 ? ": " : "", s < 0 ? strerror(errno) : "");
		return s < 0;
	}
	printf("nothing to see here\n");
	return 0;
}
