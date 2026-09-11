/* readsize.c: read one file with a given buffer size, and time it.
 *
 *   head -c 16M /dev/urandom > data16m
 *   gcc -O2 -Wall -Wextra -o readsize readsize.c
 *   ./readsize data16m 1; ./readsize data16m 65536
 *
 * CS 202 Week 0, L03 §4. */
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
int main(int argc, char **argv)
{
    if (argc != 3) {
        fprintf(stderr, "usage: %s <file> <buffer size>\n", argv[0]);
        return 1;
    }
    size_t bs = strtoul(argv[2], 0, 10);
    char *buf = malloc(bs);
    long calls = 0, total = 0;
    struct timespec a, b;
    int fd = open(argv[1], O_RDONLY);
    clock_gettime(CLOCK_MONOTONIC, &a);
    for (ssize_t n; (n = read(fd, buf, bs)) > 0; calls++) total += n;
    calls++;  /* the read that returned 0 */
    clock_gettime(CLOCK_MONOTONIC, &b);
    double s = (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) * 1e-9;
    printf("bs=%7zu  read() calls=%9ld  bytes=%ld  time=%.4f s  per call=%.0f ns\n", bs, calls, total, s, s / calls * 1e9);
    return 0;
}
