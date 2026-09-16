/* pcache.c — what the page cache holds, how much of a file one read brings in, and
 * what a read costs cold and warm. Uses mincore() to ask which of a file's pages are
 * resident and posix_fadvise(POSIX_FADV_DONTNEED) to drop them again — both available
 * to any user, unlike /proc/sys/vm/drop_caches.
 *   gcc -O2 -Wall -Wextra -o pcache pcache.c && ./pcache FILE
 * CS 202 Week 7. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

static long cached_kb(void)
{
    FILE *f = fopen("/proc/meminfo", "r"); char l[256]; long v = -1;
    while (fgets(l, sizeof l, f)) if (!strncmp(l, "Cached:", 7)) v = atol(l + 7);
    fclose(f); return v;
}

/* How many of the file's pages are in the page cache, and the first run of resident pages. */
static void residency(int fd, size_t size, const char *what, int show_first_run)
{
    void *m = mmap(0, size, PROT_READ, MAP_SHARED, fd, 0);
    if (m == MAP_FAILED) { perror("mmap"); return; }
    size_t pages = (size + 4095) / 4096;
    unsigned char *vec = malloc(pages);
    if (mincore(m, size, vec)) perror("mincore");
    size_t n = 0, run = 0;
    for (size_t i = 0; i < pages; i++) n += vec[i] & 1;
    if (show_first_run) { while (run < pages && (vec[run] & 1)) run++; }
    printf("%-34s %6zu of %zu pages resident (%4.1f%%)", what, n, pages, 100.0 * n / pages);
    if (show_first_run) printf("   first run: %zu pages = %zu KiB", run, run * 4);
    printf("\n");
    free(vec);
    munmap(m, size);
}

int main(int argc, char **argv)
{
    const char *path = argc > 1 ? argv[1] : "big.bin";
    int fd = open(path, O_RDONLY);
    struct stat st;
    if (fd < 0 || fstat(fd, &st)) { perror(path); return 1; }
    size_t size = (size_t)st.st_size;
    printf("%s: %zu MiB\n", path, size >> 20);

    posix_fadvise(fd, 0, 0, POSIX_FADV_DONTNEED);
    sync();
    posix_fadvise(fd, 0, 0, POSIX_FADV_DONTNEED);
    residency(fd, size, "after POSIX_FADV_DONTNEED", 0);

    char buf[4096];
    long c0 = cached_kb();
    double t0 = now();
    if (pread(fd, buf, 1, 0) != 1) perror("pread");
    double t1 = now();
    printf("%-34s %8.1f us   Cached +%ld kB\n", "one 1-byte read, cold", (t1 - t0) * 1e6, cached_kb() - c0);
    residency(fd, size, "after that one read", 1);

    /* sequential read of the whole file, cold */
    posix_fadvise(fd, 0, 0, POSIX_FADV_DONTNEED);
    residency(fd, size, "dropped again", 0);
    char *big = malloc(1 << 20);
    t0 = now();
    lseek(fd, 0, SEEK_SET);
    ssize_t r, total = 0;
    while ((r = read(fd, big, 1 << 20)) > 0) total += r;
    t1 = now();
    printf("%-34s %8.3f s = %6.0f MB/s\n", "sequential read, cold", t1 - t0, total / (t1 - t0) / 1e6);
    residency(fd, size, "after reading it all", 0);

    t0 = now();
    lseek(fd, 0, SEEK_SET);
    total = 0;
    while ((r = read(fd, big, 1 << 20)) > 0) total += r;
    t1 = now();
    printf("%-34s %8.3f s = %6.0f MB/s\n", "sequential read, warm", t1 - t0, total / (t1 - t0) / 1e6);

    /* how the readahead window grows: read one page at a time from a cold file */
    posix_fadvise(fd, 0, 0, POSIX_FADV_DONTNEED);
    {
        void *m = mmap(0, size, PROT_READ, MAP_SHARED, fd, 0);
        unsigned char *vec = malloc((size + 4095) / 4096);
        printf("%-34s", "readahead, page by page");
        for (int i = 0; i < 12; i++) {
            if (pread(fd, buf, 1, (off_t)i * 4096) != 1) perror("pread");
            if (mincore(m, size, vec)) perror("mincore");
            size_t n = 0;
            while (n < (size + 4095) / 4096 && (vec[n] & 1)) n++;
            printf(" %zu", n);
        }
        printf("  pages resident after reading page 0, 1, 2, ...\n");
        free(vec);
        munmap(m, size);
    }

    /* random 4 KiB reads: cold, then with the whole file in cache */
    for (int warm = 0; warm < 2; warm++) {
        if (!warm) posix_fadvise(fd, 0, 0, POSIX_FADV_DONTNEED);
        else {
            lseek(fd, 0, SEEK_SET);
            while ((r = read(fd, big, 1 << 20)) > 0) ;          /* warm the whole file */
            residency(fd, size, "warmed for the next test", 0);
        }
        unsigned long x = 88172645463325252UL;
        int n = warm ? 200000 : 2000;
        t0 = now();
        for (int i = 0; i < n; i++) {
            x ^= x << 13; x ^= x >> 7; x ^= x << 17;
            if (pread(fd, buf, 4096, (off_t)((x % (size / 4096)) * 4096)) < 0) perror("pread");
        }
        t1 = now();
        printf("%-34s %8.2f us each = %8.0f reads/s\n", warm ? "random 4 KiB reads, warm" : "random 4 KiB reads, cold",
               (t1 - t0) * 1e6 / n, n / (t1 - t0));
    }
    free(big);
    return 0;
}
