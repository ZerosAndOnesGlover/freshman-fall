// CS 211 Week 9, Lab 9 Part C.  The compiler is a source of reordering too.
//
// One thread spins waiting for a flag; another sets it.  The flag is an
// ordinary `int`, which makes this a DATA RACE, which is undefined
// behaviour, which means the compiler may assume it does not happen.
//
// And it does assume that.  At -O2 the load of `ready` is loop-invariant --
// nothing in the loop body writes it, and the compiler is entitled to
// believe no one else does either -- so it is hoisted out and the loop
// becomes `if (!ready) for(;;);`.
//
//   gcc -O0 -pthread -o hoist_O0 hoist.c && timeout 5 ./hoist_O0   # finishes
//   gcc -O2 -pthread -o hoist_O2 hoist.c && timeout 5 ./hoist_O2   # HANGS
//   gcc -O2 -pthread -DATOMIC -o hoist_at hoist.c && ./hoist_at    # finishes
//
// **No processor reordered anything here.** This is entirely the compiler,
// on the most strongly ordered mainstream architecture there is.
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <stdatomic.h>

#ifdef ATOMIC
static _Atomic int ready;
static _Atomic int payload;
#else
static int ready;
static int payload;
#endif

static void *setter(void *a) {
    (void)a;
    usleep(100000);            // let the reader get into its loop first
    payload = 42;
    ready = 1;
    return NULL;
}

static void *reader(void *a) {
    (void)a;
    while (!ready)
        ;                       // spin
    printf("  reader saw ready; payload = %d\n", payload);
    return NULL;
}

int main(void) {
#ifdef ATOMIC
    printf("; ---- flag is _Atomic ----\n");
#else
    printf("; ---- flag is a plain int (data race) ----\n");
#endif
    pthread_t s, r;
    pthread_create(&r, NULL, reader, NULL);
    pthread_create(&s, NULL, setter, NULL);
    pthread_join(s, NULL);
    pthread_join(r, NULL);
    printf("  done\n");
    return 0;
}
