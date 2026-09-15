/* errchk.c: what three kinds of mutex do when misused.
 *
 *   gcc -O2 -Wall -Wextra -pthread -o errchk errchk.c && ./errchk
 *
 * CS 202 Week 4, L15 §6.
 */
#define _GNU_SOURCE
#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

static pthread_mutex_t rob;
static void *die_holding(void *arg) { (void)arg; pthread_mutex_lock(&rob); return 0; }   /* exits holding it */

int main(void)
{
    pthread_mutexattr_t a;

    pthread_mutex_t def = PTHREAD_MUTEX_INITIALIZER;
    pthread_mutex_lock(&def);
    struct timespec dl;
    clock_gettime(CLOCK_REALTIME, &dl);
    dl.tv_sec += 1;
    int r = pthread_mutex_timedlock(&def, &dl);
    printf("default mutex, locked twice by one thread:        %s (after waiting 1 s)\n", strerrorname_np(r));

    pthread_mutex_t ec;
    pthread_mutexattr_init(&a);
    pthread_mutexattr_settype(&a, PTHREAD_MUTEX_ERRORCHECK);
    pthread_mutex_init(&ec, &a);
    pthread_mutex_lock(&ec);
    r = pthread_mutex_lock(&ec);
    printf("error-checking mutex, locked twice by one thread: %s (at once)\n", strerrorname_np(r));

    pthread_mutexattr_init(&a);
    pthread_mutexattr_setrobust(&a, PTHREAD_MUTEX_ROBUST);
    pthread_mutex_init(&rob, &a);
    pthread_t t;
    pthread_create(&t, 0, die_holding, 0);
    pthread_join(t, 0);
    r = pthread_mutex_lock(&rob);
    printf("robust mutex, owner exited while holding it:      %s\n", strerrorname_np(r));
    if (r == EOWNERDEAD) {
        pthread_mutex_consistent(&rob);
        pthread_mutex_unlock(&rob);
        r = pthread_mutex_lock(&rob);
        printf("  after pthread_mutex_consistent and unlock, lock returns %d\n", r);
    }
    return 0;
}
