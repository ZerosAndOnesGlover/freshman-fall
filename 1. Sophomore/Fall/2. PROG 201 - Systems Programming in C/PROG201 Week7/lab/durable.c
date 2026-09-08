/* What does making a write durable cost? */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <sys/stat.h>

static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}

#define N 200
#define REC 4096

static double run(const char *what, int flags, int sync_each, int datasync)
{
    unlink("t.dat");
    int fd = open("t.dat", O_WRONLY | O_CREAT | O_TRUNC | flags, 0644);
    if (fd < 0) { perror("open"); exit(1); }
    char *buf = malloc(REC);
    memset(buf, 'x', REC);
    double t0 = now();
    for (int i = 0; i < N; i++) {
        if (write(fd, buf, REC) != REC) { perror("write"); exit(1); }
        if (sync_each) { if (datasync ? fdatasync(fd) : fsync(fd)) perror("sync"); }
    }
    if (!sync_each) fsync(fd);
    double dt = now() - t0;
    close(fd); free(buf);
    printf("  %-40s %8.3f s   %8.2f ms per record   %7.0f rec/s\n",
           what, dt, dt * 1000 / N, N / dt);
    return dt;
}

int main(void)
{
    printf("%d records of %d bytes\n", N, REC);
    run("write only, one fsync at the end",        0, 0, 0);
    run("write + fdatasync every record",          0, 1, 1);
    run("write + fsync every record",              0, 1, 0);
    run("O_SYNC, no explicit sync",           O_SYNC, 0, 0);
    run("O_DSYNC, no explicit sync",         O_DSYNC, 0, 0);
    unlink("t.dat");
    return 0;
}
