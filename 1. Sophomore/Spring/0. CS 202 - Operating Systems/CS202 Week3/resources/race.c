/* race.c: several threads increment one shared counter, with no lock.
 *
 *   gcc -O2 -Wall -Wextra -pthread -o race race.c
 *   ./race <threads> <increments per thread>
 *
 * CS 202 Week 3, L10 §1-§2.
 */
#define _GNU_SOURCE
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

static volatile long counter;     /* volatile: the compiler must load, add and store every time */
static long per_thread;

static void *work(void *arg)
{
    (void)arg;
    for (long i = 0; i < per_thread; i++)
        counter++;
    return 0;
}

int main(int argc, char **argv)
{
    int n = argc > 1 ? atoi(argv[1]) : 2;
    per_thread = argc > 2 ? atol(argv[2]) : 10000000;
    pthread_t t[64];
    for (int i = 0; i < n; i++) pthread_create(&t[i], 0, work, 0);
    for (int i = 0; i < n; i++) pthread_join(t[i], 0);
    long expected = n * per_thread;
    printf("%d threads x %ld: counter = %ld, expected %ld, lost %ld (%.1f%%)\n",
           n, per_thread, counter, expected, expected - counter, 100.0 * (expected - counter) / expected);
    return 0;
}
