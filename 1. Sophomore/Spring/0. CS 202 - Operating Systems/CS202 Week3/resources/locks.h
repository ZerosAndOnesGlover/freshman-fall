/* locks.h: five ways to protect a critical section, all with one interface.
 * CS 202 Week 3. */
#pragma once
#define _GNU_SOURCE
#include <linux/futex.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdatomic.h>
#include <sys/syscall.h>
#include <unistd.h>

static inline void cpu_relax(void) { __asm__("pause"); }

/* 1. Test-and-set spinlock: atomic_flag is a boolean with an atomic set-and-return-old. */
typedef struct { atomic_flag f; } tas_lock;
static inline void tas_acquire(tas_lock *l) { while (atomic_flag_test_and_set(&l->f)) cpu_relax(); }
static inline void tas_release(tas_lock *l) { atomic_flag_clear(&l->f); }

/* 1b. Test-and-TEST-and-set: look first, and only write when the lock looks free.
 *     A failed xchg still writes, and every write drags the cache line to this CPU. */
typedef struct { atomic_int v; } ttas_lock;
static inline void ttas_acquire(ttas_lock *l)
{
    for (;;) {
        if (atomic_load_explicit(&l->v, memory_order_relaxed) == 0 && atomic_exchange(&l->v, 1) == 0)
            return;
        cpu_relax();
    }
}
static inline void ttas_release(ttas_lock *l) { atomic_store(&l->v, 0); }

/* 2. Compare-and-swap spinlock: "if it is 0, make it 1" as one instruction. */
typedef struct { atomic_int v; } cas_lock;
static inline void cas_acquire(cas_lock *l)
{
    for (;;) {
        int expected = 0;
        if (atomic_compare_exchange_weak(&l->v, &expected, 1)) return;
        cpu_relax();
    }
}
static inline void cas_release(cas_lock *l) { atomic_store(&l->v, 0); }

/* 3. Futex mutex, after Drepper's "Futexes Are Tricky": 0 = unlocked,
 *    1 = locked, 2 = locked and someone may be waiting. The kernel is entered
 *    only to sleep (state 2) and only to wake someone (was 2 on unlock). */
typedef struct { atomic_int v; } futex_lock;
static inline long sys_futex(atomic_int *addr, int op, int val)
{
    return syscall(SYS_futex, addr, op, val, 0, 0, 0);
}
static inline void futex_acquire(futex_lock *l)
{
    int c = 0;
    if (atomic_compare_exchange_strong(&l->v, &c, 1)) return;       /* fast path: no system call */
    if (c != 2) c = atomic_exchange(&l->v, 2);
    while (c != 0) {
        sys_futex(&l->v, FUTEX_WAIT_PRIVATE, 2);                    /* sleep only if still 2 */
        c = atomic_exchange(&l->v, 2);
    }
}
static inline void futex_release(futex_lock *l)
{
    if (atomic_exchange(&l->v, 0) == 2)
        sys_futex(&l->v, FUTEX_WAKE_PRIVATE, 1);                    /* someone may be asleep */
}
