/* fsync against fdatasync when the size does NOT change, and the
 * directory fsync everybody forgets. */
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

/* overwrite in place: the file size never changes, so fdatasync has nothing
 * to write about the metadata */
static void inplace(const char *what, int datasync)
{
    int fd = open("t2.dat", O_WRONLY | O_CREAT, 0644);
    char *buf = malloc(REC); memset(buf, 'y', REC);
    if (ftruncate(fd, (off_t) N * REC) < 0) perror("ftruncate");
    fsync(fd);
    double t0 = now();
    for (int i = 0; i < N; i++) {
        if (pwrite(fd, buf, REC, (off_t) i * REC) != REC) perror("pwrite");
        if (datasync ? fdatasync(fd) : fsync(fd)) perror("sync");
    }
    double dt = now() - t0;
    printf("  %-40s %8.3f s   %8.2f ms each\n", what, dt, dt * 1000 / N);
    close(fd); free(buf);
}

/* the safe-write pattern: temp file, fsync it, rename, fsync the DIRECTORY */
static void safe_write(const char *what, int sync_dir)
{
    double t0 = now();
    for (int i = 0; i < 50; i++) {
        int fd = open("cfg.tmp", O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (write(fd, "config data\n", 12) != 12) perror("write");
        fsync(fd);                       /* the file's contents are durable */
        close(fd);
        if (rename("cfg.tmp", "cfg.txt") < 0) perror("rename");
        if (sync_dir) {
            int d = open(".", O_RDONLY | O_DIRECTORY);
            fsync(d);                    /* ...and now so is the NAME */
            close(d);
        }
    }
    double dt = now() - t0;
    printf("  %-40s %8.3f s   %8.2f ms each\n", what, dt, dt * 1000 / 50);
}

int main(void)
{
    printf("overwrite in place, %d records of %d bytes (size never changes)\n", N, REC);
    inplace("fsync every record",     0);
    inplace("fdatasync every record", 1);

    printf("\nthe safe-write pattern, 50 times\n");
    safe_write("write, fsync, rename",                       0);
    safe_write("write, fsync, rename, fsync the directory",   1);

    unlink("t2.dat"); unlink("cfg.txt"); unlink("cfg.tmp");
    return 0;
}
