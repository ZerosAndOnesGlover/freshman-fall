// CS 211 Week 9, Lab 9 Part A.  The store-buffer litmus test.
//
//   Thread 0:  x = 1;  r1 = y;
//   Thread 1:  y = 1;  r2 = x;
//
// Under SEQUENTIAL CONSISTENCY -- the model everyone reasons with by
// default -- the four instructions interleave in some single global order,
// and in every such order at least one thread reads the other's write.  So
// r1 == 0 && r2 == 0 is IMPOSSIBLE.
//
// It happens, on this x86-64 machine, thousands of times a second.
//
// The cause is the store buffer: a write retires into a per-core queue
// before it is visible to other cores, and the load that follows is allowed
// to complete first.  That reordering -- StoreLoad -- is the ONLY one x86
// permits, and it is enough to break the algorithm above.
//
//   gcc -O2 -pthread -o litmus litmus.c
//   ./litmus 200000            # no barrier
//   ./litmus 200000 fence      # full barrier between the store and the load
//
// The threads are created once and synchronised per iteration by a
// sense-reversing barrier.  Creating threads inside the loop would cost far
// more than the effect being measured -- the first version of this file did
// that and ran 20000 iterations in over two minutes.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <stdatomic.h>
#include <time.h>

// Distinct cache lines.  Sharing one makes the coherence traffic serialise
// the two threads and the window vanishes: you would measure zero and
// conclude, wrongly, that x86 is sequentially consistent.
#define PAD _Alignas(64)

static PAD volatile int x;
static PAD volatile int y;
static PAD _Atomic int arrived;
static PAD _Atomic int sense;
static PAD int r1, r2;

static int use_fence;
static long iters;
static long counts[4];          // indexed by (r1<<1)|r2

static void bar_wait(int *local_sense) {
    *local_sense = !*local_sense;
    if (atomic_fetch_add(&arrived, 1) == 1) {
        atomic_store(&arrived, 0);
        atomic_store(&sense, *local_sense);
    } else {
        while (atomic_load(&sense) != *local_sense)
            ;
    }
}

static void *worker(void *arg) {
    long me = (long)arg;
    int ls = 0;
    for (long i = 0; i < iters; i++) {
        bar_wait(&ls);                       // both threads start together
        if (me == 0) {
            x = 1;
            if (use_fence) atomic_thread_fence(memory_order_seq_cst);
            r1 = y;
        } else {
            y = 1;
            if (use_fence) atomic_thread_fence(memory_order_seq_cst);
            r2 = x;
        }
        bar_wait(&ls);                       // both finished
        if (me == 0) {
            counts[((r1 != 0) << 1) | (r2 != 0)]++;
            x = y = 0;                       // reset for the next round
        }
        bar_wait(&ls);                       // reset observed by both
    }
    return NULL;
}

int main(int argc, char **argv) {
    iters = argc > 1 ? atol(argv[1]) : 100000;
    use_fence = argc > 2 && strcmp(argv[2], "fence") == 0;

    struct timespec a, b;
    clock_gettime(CLOCK_MONOTONIC, &a);
    pthread_t p0, p1;
    pthread_create(&p0, NULL, worker, (void *)0);
    pthread_create(&p1, NULL, worker, (void *)1);
    pthread_join(p0, NULL);
    pthread_join(p1, NULL);
    clock_gettime(CLOCK_MONOTONIC, &b);
    double secs = (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9;

    printf("; ---- store-buffer litmus, %ld iterations%s ----\n",
           iters, use_fence ? ", WITH seq_cst fence" : "");
    printf("  r1=0,r2=0   %8ld   <- FORBIDDEN under sequential consistency\n",
           counts[0]);
    printf("  r1=0,r2=1   %8ld\n", counts[1]);
    printf("  r1=1,r2=0   %8ld\n", counts[2]);
    printf("  r1=1,r2=1   %8ld\n", counts[3]);
    printf("  %.3f s   %.0f iters/s   %.4f%% forbidden\n",
           secs, iters / secs, 100.0 * counts[0] / iters);
    return 0;
}
