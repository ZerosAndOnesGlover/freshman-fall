/* PROG 201 -- Lab 3 Part A.  What will this machine let you do?
 * Provided complete.  Read it, run it, and write the answers down. */
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sched.h>
#include <pthread.h>
#include <sys/resource.h>

int main(void)
{
    struct rlimit rl;
    getrlimit(RLIMIT_RTPRIO, &rl);
    printf("RLIMIT_RTPRIO: soft=%lu hard=%lu\n",
           (unsigned long) rl.rlim_cur, (unsigned long) rl.rlim_max);
    getrlimit(RLIMIT_NICE, &rl);
    printf("RLIMIT_NICE  : soft=%lu hard=%lu\n",
           (unsigned long) rl.rlim_cur, (unsigned long) rl.rlim_max);

    struct sched_param p = { .sched_priority = 10 };
    errno = 0;
    int rc = sched_setscheduler(0, SCHED_FIFO, &p);
    printf("sched_setscheduler(SCHED_FIFO, 10) -> %d, errno=%s\n",
           rc, rc < 0 ? strerror(errno) : "-");

    pthread_mutexattr_t a;
    pthread_mutexattr_init(&a);
    rc = pthread_mutexattr_setprotocol(&a, PTHREAD_PRIO_INHERIT);
    printf("pthread_mutexattr_setprotocol(PRIO_INHERIT) -> %d %s\n",
           rc, rc ? strerror(rc) : "");
    pthread_mutex_t m;
    rc = pthread_mutex_init(&m, &a);
    printf("pthread_mutex_init with that attribute      -> %d %s\n",
           rc, rc ? strerror(rc) : "");
    int got = -1;
    pthread_mutexattr_getprotocol(&a, &got);
    printf("protocol reads back as %d (NONE=%d INHERIT=%d PROTECT=%d)\n",
           got, PTHREAD_PRIO_NONE, PTHREAD_PRIO_INHERIT, PTHREAD_PRIO_PROTECT);
    return 0;
}
