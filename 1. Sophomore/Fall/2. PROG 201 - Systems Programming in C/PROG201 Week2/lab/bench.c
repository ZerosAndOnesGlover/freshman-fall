/* PROG 201 -- Lab 2: IPC performance benchmark
 *
 * Four mechanisms, two questions:
 *   bulk    -- how fast can it move N MiB in fixed-size chunks?
 *   trip    -- how long does one request/response round trip take?
 *
 * The pipe versions are written for you.  Read them first: every TODO below
 * is the same shape with a different mechanism in the middle.
 *
 *   make
 *   ./bench bulk 256 4096          # 256 MiB in 4 KiB chunks, every mechanism
 *   ./bench trip 100000            # 100,000 one-byte ping-pongs
 *   ./bench slots 256              # Part C: bulk against ring depth
 *
 * Anything a function cannot do yet returns -1 and prints as "--".
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <time.h>
#include <mqueue.h>
#include <semaphore.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/wait.h>

#define FIFO_PATH "/tmp/prog201.bench.fifo"
#define MQ_NAME   "/prog201.bench"
#define SHM_NAME  "/prog201.bench"

#define MAX_SLOTS 64
#define SLOT_SIZE 262144

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec / 1e9;
}

static void die(const char *what) { perror(what); exit(1); }

/* The shared region every shm test uses.  Note that both semaphores are
 * INSIDE it -- see L09 section 1.  Putting a sem_t in a local variable and
 * passing its address to a child gives you two unrelated counters. */
struct ring {
    sem_t    empty, full;
    unsigned head, tail;
    size_t   len;
    char     data[MAX_SLOTS][SLOT_SIZE];
};

static struct ring *ring_make(int slots)
{
    struct ring *r = mmap(NULL, sizeof *r, PROT_READ | PROT_WRITE,
                          MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (r == MAP_FAILED) die("mmap");
    if (sem_init(&r->empty, 1, slots) < 0) die("sem_init");
    if (sem_init(&r->full,  1, 0) < 0) die("sem_init");
    r->head = r->tail = 0;
    return r;
}

static void ring_free(struct ring *r)
{
    sem_destroy(&r->empty);
    sem_destroy(&r->full);
    munmap(r, sizeof *r);
}

/* ===================================================================== bulk */

/* WORKED EXAMPLE.  Parent writes `bytes` in `chunk`-sized pieces; child
 * reads until EOF.  Returns elapsed seconds. */
static double bulk_pipe(long bytes, int chunk)
{
    int fd[2];
    if (pipe(fd) < 0) die("pipe");

    if (fork() == 0) {
        close(fd[1]);                      /* or the child never sees EOF */
        char *sink = malloc(chunk);
        while (read(fd[0], sink, chunk) > 0)
            ;
        _exit(0);
    }
    close(fd[0]);

    char *buf = calloc(chunk, 1);
    double t0 = now();
    for (long sent = 0; sent < bytes; ) {
        ssize_t n = write(fd[1], buf, chunk);
        if (n < 0) die("write");
        sent += n;                         /* a short write is not an error */
    }
    close(fd[1]);                          /* this is what ends the child */
    wait(NULL);
    double dt = now() - t0;
    free(buf);
    return dt;
}

/* TODO 1.  Same as bulk_pipe, through a FIFO at FIFO_PATH.
 *
 * mkfifo() it (unlink first -- it survives a crashed run), then fork.  Both
 * ends open the SAME path: the child O_RDONLY, the parent O_WRONLY.  Remember
 * L07 section 5: a blocking open on a FIFO does not return until the other end
 * opens, so the order you write these two opens in decides whether this
 * function works or hangs forever.  unlink() when you are done. */
static double bulk_fifo(long bytes, int chunk)
{
    (void) bytes; (void) chunk;
    return -1;
}

/* TODO 2.  Same, through a POSIX message queue.
 *
 * mq_open with O_CREAT and a struct mq_attr.  Send bytes/chunk messages of
 * `chunk` bytes; the child mq_receive()s the same number.
 *
 * Two things will bite you, both from L08:
 *   - mq_maxmsg <= 10 and mq_msgsize <= 8192 for an unprivileged process.
 *     Return -1 rather than dying when chunk is too big -- the harness
 *     prints "--" and the table stays readable.
 *   - the receive buffer must be at least mq_msgsize, not the message length.
 *
 * Link with -lrt (the Makefile already does). */
static double bulk_mq(long bytes, int chunk)
{
    (void) bytes; (void) chunk;
    return -1;
}

/* TODO 3.  Same, through shared memory with a ONE-slot ring.
 *
 * ring_make(1) gives you the region.  Producer: sem_wait(empty), memcpy in,
 * sem_post(full).  Consumer: sem_wait(full), memcpy out, sem_post(empty).
 * The consumer must copy the data out -- if it does not, you are timing an
 * empty loop rather than a transfer.
 *
 * Predict the number before you run it.  Write your prediction in the answer
 * sheet BEFORE the first run; Q4 asks for it. */
static double bulk_shm(long bytes, int chunk)
{
    (void) bytes; (void) chunk;
    return -1;
}

/* ================================================================== round trip */

/* WORKED EXAMPLE.  Parent writes one byte and waits for one back, `trips`
 * times.  Two pipes, because one pipe is one direction. */
static double rt_pipe(long trips)
{
    int up[2], down[2];
    if (pipe(up) < 0 || pipe(down) < 0) die("pipe");

    if (fork() == 0) {
        char c;
        for (long i = 0; i < trips; i++) {
            if (read(up[0], &c, 1) != 1) _exit(1);
            if (write(down[1], &c, 1) != 1) _exit(1);
        }
        _exit(0);
    }
    char c = 'x';
    double t0 = now();
    for (long i = 0; i < trips; i++) {
        if (write(up[1], &c, 1) != 1) die("write");
        if (read(down[0], &c, 1) != 1) die("read");
    }
    double dt = now() - t0;
    wait(NULL);
    return dt;
}

/* TODO 4.  The same round trip through shared memory and two semaphores.
 *
 * No data needs to move -- the point is the handoff.  Parent: sem_post(full),
 * sem_wait(empty).  Child: sem_wait(full), sem_post(empty).  That is one
 * trip.  Use ring_make(0) so `empty` starts at zero. */
static double rt_shm(long trips)
{
    struct ring *r = ring_make(0);      /* both semaphores start at zero */
    (void) trips;
    ring_free(r);
    return -1;
}

/* TODO 5 (Part C).  bulk through shared memory with `slots` slots.
 *
 * This is bulk_shm with the ring index arithmetic put back:
 *   head = (head + 1) % slots  in the producer,
 *   tail = (tail + 1) % slots  in the consumer.
 * chunk must be <= SLOT_SIZE. */
static double bulk_slots(long bytes, int chunk, int slots)
{
    (void) bytes; (void) chunk; (void) slots;
    return -1;
}

/* ===================================================================== main */

static void row(const char *name, double dt, long MB)
{
    if (dt < 0) printf("%-24s %10s %12s\n", name, "--", "--");
    else        printf("%-24s %10.3f %12.1f\n", name, dt, MB / dt);
}

static void triprow(const char *name, double dt, long trips)
{
    if (dt < 0) printf("%-24s %10s %12s\n", name, "--", "--");
    else        printf("%-24s %10.3f %12.3f\n", name, dt, dt * 1e6 / trips);
}

int main(int argc, char **argv)
{
    const char *what = argc > 1 ? argv[1] : "bulk";

    if (!strcmp(what, "bulk")) {
        long MB    = argc > 2 ? atol(argv[2]) : 256;
        int  chunk = argc > 3 ? atoi(argv[3]) : 4096;
        long bytes = MB * 1024 * 1024;
        printf("bulk: %ld MiB in %d-byte chunks\n", MB, chunk);
        printf("%-24s %10s %12s\n", "mechanism", "seconds", "MiB/s");
        row("pipe",              bulk_pipe(bytes, chunk), MB);
        row("FIFO",              bulk_fifo(bytes, chunk), MB);
        row("POSIX mq",          bulk_mq(bytes, chunk),   MB);
        row("shm + sem, 1 slot", bulk_shm(bytes, chunk),  MB);
    } else if (!strcmp(what, "trip")) {
        long trips = argc > 2 ? atol(argv[2]) : 100000;
        printf("round trip: %ld one-byte ping-pongs\n", trips);
        printf("%-24s %10s %12s\n", "mechanism", "seconds", "us/trip");
        triprow("pipe",          rt_pipe(trips), trips);
        triprow("shm + sem",     rt_shm(trips),  trips);
    } else if (!strcmp(what, "slots")) {
        long MB    = argc > 2 ? atol(argv[2]) : 256;
        int  chunk = argc > 3 ? atoi(argv[3]) : 4096;
        long bytes = MB * 1024 * 1024;
        int  depth[] = { 1, 2, 4, 8, 16, 32, 64 };
        printf("ring depth: %ld MiB in %d-byte slots\n", MB, chunk);
        printf("%-24s %10s %12s\n", "slots", "seconds", "MiB/s");
        for (unsigned i = 0; i < sizeof depth / sizeof *depth; i++) {
            char label[32];
            snprintf(label, sizeof label, "%d", depth[i]);
            row(label, bulk_slots(bytes, chunk, depth[i]), MB);
        }
    } else {
        fprintf(stderr, "usage: %s [bulk MB chunk | trip TRIPS | slots MB chunk]\n", argv[0]);
        return 2;
    }
    return 0;
}
