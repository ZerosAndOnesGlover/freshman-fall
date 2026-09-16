/* safeupdate.c — replace a file's contents so that a crash leaves either the old file
 * or the new one, timing each step: write, fsync, rename, fsync the directory.
 *   gcc -O2 -Wall -Wextra -o safeupdate safeupdate.c && ./safeupdate DIR [--no-dirsync]
 * CS 202 Week 7, Lab 7 Part D. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

int main(int argc, char **argv)
{
    const char *dir = argc > 1 ? argv[1] : ".";
    int dirsync = !(argc > 2 && !strcmp(argv[2], "--no-dirsync"));
    char target[512], tmp[512];
    snprintf(target, sizeof target, "%s/data.bin", dir);
    snprintf(tmp, sizeof tmp, "%s/data.tmp", dir);
    char *payload = malloc(1 << 20);
    memset(payload, 0x5a, 1 << 20);

    double t0 = now();
    int fd = open(tmp, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) { perror(tmp); return 1; }
    if (write(fd, payload, 1 << 20) != 1 << 20) perror("write");
    double t1 = now();
    if (fsync(fd)) perror("fsync");
    double t2 = now();
    close(fd);
    if (rename(tmp, target)) perror("rename");
    double t3 = now();
    double t4 = t3;
    if (dirsync) {
        int dfd = open(dir, O_RDONLY);
        if (fsync(dfd)) perror("fsync dir");
        close(dfd);
        t4 = now();
    }
    printf("write %6.2f ms   fsync file %6.2f ms   rename %6.2f ms   fsync dir %6.2f ms   total %6.2f ms%s\n",
           (t1 - t0) * 1e3, (t2 - t1) * 1e3, (t3 - t2) * 1e3, (t4 - t3) * 1e3, (t4 - t0) * 1e3,
           dirsync ? "" : "   (no directory fsync)");
    free(payload);
    return 0;
}
