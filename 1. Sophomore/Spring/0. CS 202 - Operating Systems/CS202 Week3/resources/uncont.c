/* uncont.c: fifty million uncontended pthread_mutex lock/unlock pairs.
 *
 *   gcc -O2 -pthread -o uncont uncont.c && strace -f -c ./uncont
 *
 * CS 202 Week 3, L11 §1. */
#include <pthread.h>
#include <stdio.h>
int main(void){ pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER; volatile long c = 0; for (long i = 0; i < 50000000; i++) { pthread_mutex_lock(&m); c++; pthread_mutex_unlock(&m); } printf("%ld\n", c); return 0; }
