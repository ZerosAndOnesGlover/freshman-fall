/* devcost.c — what reaching a device costs from user space: the same read() to
 * /dev/null, /dev/zero, /dev/urandom and a file, plus an ioctl and a poll, so that
 * the dispatch through the kernel's file-operations table can be separated from the
 * work the device actually does.
 *   gcc -O2 -Wall -Wextra -o devcost devcost.c && taskset -c 2 ./devcost
 * CS 202 Week 9, L28. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <poll.h>
#include <sys/ioctl.h>
#include <termios.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

static double per_op(const char *path, int flags, size_t len, int n)
{
    int fd = open(path, flags);
    if (fd < 0) { perror(path); return -1; }
    char *buf = malloc(len);
    double t0 = now();
    for (int i = 0; i < n; i++) {
        ssize_t r = (flags & O_WRONLY) ? write(fd, buf, len) : read(fd, buf, len);
        if (r < 0) { perror(path); break; }
        if ((flags & O_RDONLY) == O_RDONLY && r == 0) lseek(fd, 0, SEEK_SET);
    }
    double t1 = now();
    free(buf);
    close(fd);
    return (t1 - t0) * 1e9 / n;
}

int main(void)
{
    int n = 200000;
    printf("%-22s %10s %10s\n", "device", "4 B", "4 KiB");
    const char *paths[] = { "/dev/null", "/dev/zero", "/dev/urandom" };
    for (int i = 0; i < 3; i++) {
        int flags = i == 0 ? O_WRONLY : O_RDONLY;
        printf("%-22s %8.0f ns %8.0f ns\n", paths[i], per_op(paths[i], flags, 4, n), per_op(paths[i], flags, 4096, n / 10));
    }
    /* a regular file, warm in the page cache, for comparison */
    int fd = open("devcost.tmp", O_RDWR | O_CREAT | O_TRUNC, 0644);
    char *b = calloc(1, 4096);
    if (write(fd, b, 4096) != 4096) perror("write");
    close(fd);
    printf("%-22s %8.0f ns %8.0f ns\n", "a cached file", per_op("devcost.tmp", O_RDONLY, 4, n), per_op("devcost.tmp", O_RDONLY, 4096, n / 10));
    unlink("devcost.tmp");
    free(b);

    /* an ioctl, and a poll that finds data ready */
    fd = open("/dev/zero", O_RDONLY);
    struct winsize ws;
    double t0 = now();
    int fails = 0;
    for (int i = 0; i < n; i++) if (ioctl(fd, TIOCGWINSZ, &ws) < 0) fails++;
    double t1 = now();
    printf("%-22s %8.0f ns   (%d of %d returned an error, as a non-tty must)\n", "ioctl TIOCGWINSZ", (t1 - t0) * 1e9 / n, fails, n);
    struct pollfd p = { .fd = fd, .events = POLLIN };
    t0 = now();
    for (int i = 0; i < n; i++) if (poll(&p, 1, 0) < 0) perror("poll");
    t1 = now();
    printf("%-22s %8.0f ns\n", "poll, ready", (t1 - t0) * 1e9 / n);
    close(fd);
    return 0;
}
