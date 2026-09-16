/* durable.c — what a write costs when it only reaches the page cache, and what it costs
 * when it has to reach the disk: buffered writes, fsync, fdatasync, O_SYNC and O_DIRECT.
 *   gcc -O2 -Wall -Wextra -o durable durable.c && ./durable DIR
 * CS 202 Week 7, L23. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <errno.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

static long meminfo(const char *key)
{
    FILE *f = fopen("/proc/meminfo", "r"); char l[256]; long v = -1;
    while (fgets(l, sizeof l, f)) if (!strncmp(l, key, strlen(key))) v = atol(l + strlen(key));
    fclose(f); return v;
}

int main(int argc, char **argv)
{
    const char *dir = argc > 1 ? argv[1] : ".";
    char path[512];
    char *buf;
    if (posix_memalign((void **)&buf, 4096, 1 << 20)) return 1;
    memset(buf, 0xA5, 1 << 20);

    /* 1. buffered writes of 64 MiB, then fsync */
    snprintf(path, sizeof path, "%s/w1.bin", dir);
    int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    long d0 = meminfo("Dirty:");
    double t0 = now();
    for (int i = 0; i < 64; i++) if (write(fd, buf, 1 << 20) != 1 << 20) perror("write");
    double t1 = now();
    long d1 = meminfo("Dirty:");
    if (fsync(fd)) perror("fsync");
    double t2 = now();
    printf("64 MiB buffered write: %6.3f s = %5.0f MB/s, then fsync %6.3f s   Dirty %ld -> %ld kB\n",
           t1 - t0, 67.1 / (t1 - t0), t2 - t1, d0, d1);
    close(fd);

    /* 2. one 4 KiB write, repeated, with different durability */
    struct { const char *name; int flags; int sync; } modes[] = {
        { "buffered, no sync",  O_WRONLY | O_CREAT | O_TRUNC, 0 },
        { "fsync every write",  O_WRONLY | O_CREAT | O_TRUNC, 1 },
        { "fdatasync every write", O_WRONLY | O_CREAT | O_TRUNC, 2 },
        { "O_SYNC",             O_WRONLY | O_CREAT | O_TRUNC | O_SYNC, 0 },
        { "O_DIRECT, no sync",  O_WRONLY | O_CREAT | O_TRUNC | O_DIRECT, 0 },
        { "O_DIRECT + fdatasync", O_WRONLY | O_CREAT | O_TRUNC | O_DIRECT, 2 },
    };
    for (unsigned m = 0; m < sizeof modes / sizeof modes[0]; m++) {
        snprintf(path, sizeof path, "%s/w2_%u.bin", dir, m);
        fd = open(path, modes[m].flags, 0644);
        if (fd < 0) { printf("%-24s open failed: %s\n", modes[m].name, strerror(errno)); continue; }
        int n = modes[m].sync || (modes[m].flags & O_SYNC) ? 200 : 2000;
        t0 = now();
        for (int i = 0; i < n; i++) {
            if (write(fd, buf, 4096) != 4096) { perror("write"); break; }
            if (modes[m].sync == 1) fsync(fd);
            if (modes[m].sync == 2) fdatasync(fd);
        }
        t1 = now();
        printf("4 KiB writes, %-22s %8.1f us each = %8.0f writes/s\n", modes[m].name, (t1 - t0) * 1e6 / n, n / (t1 - t0));
        close(fd);
        unlink(path);
    }
    snprintf(path, sizeof path, "%s/w1.bin", dir);
    unlink(path);
    free(buf);
    return 0;
}
