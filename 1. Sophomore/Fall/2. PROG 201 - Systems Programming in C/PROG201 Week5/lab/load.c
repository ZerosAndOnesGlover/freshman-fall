/* PROG 201 -- Lab 5: a load generator.
 *
 * C concurrent connections, N requests total.
 * Each request is a fresh connection (HTTP/1.0, Connection: close).
 *   ./load <port> <concurrency> <requests> [threads]
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <time.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/epoll.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <stdatomic.h>

static int PORT, CONC, TOTAL, NTHREADS;
static atomic_int issued, done_ok, done_err;
static double *lat;                       /* one slot per completed request */
static atomic_int lat_n;

static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}

static const char REQ[] = "GET / HTTP/1.0\r\nHost: localhost\r\n\r\n";

struct slot { int fd; int state; double t0; size_t sent; size_t got; };
/* state: 0 free, 1 connecting, 2 writing, 3 reading */

/* TODO 1.  Start one request in slot `s`.
 *
 *   - claim a request from the global budget with atomic_fetch_add(&issued,1);
 *     return 0 if TOTAL is already reached (and put it back)
 *   - make a NON-BLOCKING socket: SOCK_STREAM | SOCK_NONBLOCK
 *   - record s->fd, s->state = 1, s->t0 = now(), s->sent = 0, s->got = 0
 *   - connect().  It will almost always return -1 with errno == EINPROGRESS,
 *     which is NOT an error -- L18 section 4.  Anything else is.
 *   - register the fd with EPOLLOUT and .data.ptr = s, because a connecting
 *     socket becomes WRITABLE when the handshake finishes
 *   - return 1
 */
static int start_one(struct slot *s, int ep)
{
    (void) s; (void) ep;
    return 0;
}

static void finish(struct slot *s, int ep, int ok)
{
    epoll_ctl(ep, EPOLL_CTL_DEL, s->fd, NULL);
    close(s->fd);
    if (ok) {
        int i = atomic_fetch_add(&lat_n, 1);
        if (i < TOTAL) lat[i] = now() - s->t0;
        atomic_fetch_add(&done_ok, 1);
    } else atomic_fetch_add(&done_err, 1);
    s->state = 0;
}

static void *worker(void *arg)
{
    (void) arg;
    int per = CONC / NTHREADS ? CONC / NTHREADS : 1;
    struct slot *slots = calloc(per, sizeof *slots);
    int ep = epoll_create1(0);
    int live = 0;
    for (int i = 0; i < per; i++) live += start_one(&slots[i], ep);

    struct epoll_event out[512];
    while (live > 0) {
        int n = epoll_wait(ep, out, 512, 5000);
        if (n <= 0) break;
        for (int i = 0; i < n; i++) {
            struct slot *s = out[i].data.ptr;
            if (s->state == 1) {
                /* TODO 2.  The socket is writable, which means the handshake
                 * finished -- but it may have finished by failing.  Ask
                 * SO_ERROR whether it worked (L18 section 4); on failure
                 * finish(s, ep, 0) and start another request in this slot.
                 * On success move to state 2. */
                s->state = 2;
            }
            if (s->state == 2) {
                /* TODO 3.  Write the request.  It is 35 bytes so it will
                 * almost always go in one call -- write the loop anyway,
                 * tracking s->sent, because "almost always" is not a
                 * guarantee (L16 section 6).  EAGAIN is not an error.
                 * When the whole request is out, switch to state 3 and
                 * EPOLL_CTL_MOD the registration to EPOLLIN. */
                continue;
            }
            if (s->state == 3) {
                /* TODO 4.  Read until the server closes.  read() > 0 means
                 * more of the response; add it to s->got and wait for the
                 * next event.  read() == 0 is the server's close, which for
                 * HTTP/1.0 is the end of the response -- the request
                 * succeeded if we got any bytes at all.  Anything else is a
                 * failure.  Either way, finish() the slot and start_one()
                 * another request in it, keeping `live` right. */
                finish(s, ep, 0);
                live--;
            }
        }
    }
    close(ep); free(slots);
    return NULL;
}

static int cmp(const void *a, const void *b)
{ double x = *(const double *)a, y = *(const double *)b; return x < y ? -1 : x > y; }

int main(int argc, char **argv)
{
    signal(SIGPIPE, SIG_IGN);
    PORT     = argc > 1 ? atoi(argv[1]) : 8080;
    CONC     = argc > 2 ? atoi(argv[2]) : 50;
    TOTAL    = argc > 3 ? atoi(argv[3]) : 10000;
    NTHREADS = argc > 4 ? atoi(argv[4]) : 4;
    if (NTHREADS > CONC) NTHREADS = CONC;
    lat = calloc(TOTAL, sizeof *lat);
    atomic_store(&issued, 0);
    fprintf(stderr, "%d requests, %d concurrent, %d threads; request is %zu bytes\n",
            TOTAL, CONC, NTHREADS, sizeof REQ - 1);

    pthread_t t[64];
    double t0 = now();
    for (int i = 0; i < NTHREADS; i++) pthread_create(&t[i], NULL, worker, NULL);
    for (int i = 0; i < NTHREADS; i++) pthread_join(t[i], NULL);
    double dt = now() - t0;

    int n = atomic_load(&lat_n); if (n > TOTAL) n = TOTAL;
    qsort(lat, n, sizeof *lat, cmp);
    printf("conc %-5d ok %-7d err %-6d %7.3f s  %9.0f req/s   "
           "p50 %6.2f ms  p99 %7.2f ms  max %7.2f ms\n",
           CONC, atomic_load(&done_ok), atomic_load(&done_err), dt,
           atomic_load(&done_ok) / dt,
           n ? lat[n/2]*1000 : 0.0, n ? lat[(int)(n*0.99)]*1000 : 0.0, n ? lat[n-1]*1000 : 0.0);
    return 0;
}
