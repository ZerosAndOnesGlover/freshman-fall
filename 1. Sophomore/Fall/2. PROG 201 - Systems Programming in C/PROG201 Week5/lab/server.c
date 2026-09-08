/* Five ways to serve the same trivial HTTP response. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <netdb.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/epoll.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <netinet/tcp.h>

static const char REPLY[] =
    "HTTP/1.0 200 OK\r\nContent-Length: 13\r\nConnection: close\r\n\r\nHello, world\n";

static int WORK_US;          /* per-request blocking work, microseconds */
static int SPIN_US;          /* per-request cpu work, microseconds       */

static void do_work(void)
{
    if (WORK_US) usleep(WORK_US);
    if (SPIN_US) {
        struct timespec a, b;
        clock_gettime(CLOCK_MONOTONIC, &a);
        volatile unsigned long x = 0;
        for (;;) {
            for (int i = 0; i < 1000; i++) x++;
            clock_gettime(CLOCK_MONOTONIC, &b);
            if ((b.tv_sec - a.tv_sec) * 1e6 + (b.tv_nsec - a.tv_nsec) / 1e3 >= SPIN_US) break;
        }
    }
}

static int listen_on(int port, int backlog)
{
    int s = socket(AF_INET, SOCK_STREAM, 0);
    if (s < 0) { perror("socket"); exit(1); }
    int one = 1;
    setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(port),
                             .sin_addr.s_addr = htonl(INADDR_LOOPBACK) };
    if (bind(s, (struct sockaddr *) &a, sizeof a) < 0) { perror("bind"); exit(1); }
    if (listen(s, backlog) < 0) { perror("listen"); exit(1); }
    return s;
}

/* read the request (we ignore it), write the reply, close */
static void serve(int c)
{
    char buf[2048];
    ssize_t n = read(c, buf, sizeof buf);
    (void) n;
    do_work();
    ssize_t sent = 0, len = sizeof REPLY - 1;
    while (sent < len) {
        ssize_t k = write(c, REPLY + sent, len - sent);
        if (k < 0) { if (errno == EINTR) continue; break; }
        sent += k;
    }
    close(c);
}

static void *thread_body(void *a) { serve((int)(long) a); return NULL; }

/* ---------------------------------------------------------------- pool -- */
#define QCAP 1024
static int qbuf[QCAP], qhead, qtail, qcount;
static pthread_mutex_t qm = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t  qne = PTHREAD_COND_INITIALIZER, qnf = PTHREAD_COND_INITIALIZER;

static void qput(int fd)
{
    pthread_mutex_lock(&qm);
    while (qcount == QCAP) pthread_cond_wait(&qnf, &qm);
    qbuf[qhead] = fd; qhead = (qhead + 1) % QCAP; qcount++;
    pthread_cond_signal(&qne);
    pthread_mutex_unlock(&qm);
}
static int qget(void)
{
    pthread_mutex_lock(&qm);
    while (qcount == 0) pthread_cond_wait(&qne, &qm);
    int fd = qbuf[qtail]; qtail = (qtail + 1) % QCAP; qcount--;
    pthread_cond_signal(&qnf);
    pthread_mutex_unlock(&qm);
    return fd;
}
static void *pool_body(void *a) { (void) a; for (;;) serve(qget()); return NULL; }

/* --------------------------------------------------------------- epoll -- */
static void set_nonblock(int fd)
{
    int f = fcntl(fd, F_GETFL, 0);
    fcntl(fd, F_SETFL, f | O_NONBLOCK);
}

struct conn { int fd; int sent; };

static void run_epoll(int ls)
{
    set_nonblock(ls);
    int ep = epoll_create1(0);
    struct epoll_event ev = { .events = EPOLLIN, .data.fd = ls };
    epoll_ctl(ep, EPOLL_CTL_ADD, ls, &ev);
    struct epoll_event out[256];
    for (;;) {
        int n = epoll_wait(ep, out, 256, -1);
        for (int i = 0; i < n; i++) {
            int fd = out[i].data.fd;
            if (fd == ls) {
                for (;;) {
                    int c = accept(ls, NULL, NULL);
                    if (c < 0) break;                 /* EAGAIN: drained */
                    set_nonblock(c);
                    struct epoll_event e = { .events = EPOLLIN, .data.fd = c };
                    epoll_ctl(ep, EPOLL_CTL_ADD, c, &e);
                }
            } else {
                char buf[2048];
                ssize_t k = read(fd, buf, sizeof buf);
                if (k <= 0 && !(k < 0 && errno == EAGAIN)) {
                    epoll_ctl(ep, EPOLL_CTL_DEL, fd, NULL); close(fd); continue;
                }
                do_work();
                ssize_t len = sizeof REPLY - 1, sent = 0;
                while (sent < len) {
                    ssize_t w = write(fd, REPLY + sent, len - sent);
                    if (w < 0) break;
                    sent += w;
                }
                epoll_ctl(ep, EPOLL_CTL_DEL, fd, NULL);
                close(fd);
            }
        }
    }
}

int main(int argc, char **argv)
{
    signal(SIGPIPE, SIG_IGN);
    signal(SIGCHLD, SIG_IGN);                        /* no zombies */
    const char *mode = argc > 1 ? argv[1] : "iter";
    int port = argc > 2 ? atoi(argv[2]) : 8080;
    int workers = argc > 3 ? atoi(argv[3]) : 8;
    int backlog = argc > 4 ? atoi(argv[4]) : 512;
    WORK_US     = argc > 5 ? atoi(argv[5]) : 0;
    SPIN_US     = argc > 6 ? atoi(argv[6]) : 0;

    int ls = listen_on(port, backlog);
    fprintf(stderr, "%s server on 127.0.0.1:%d (workers %d, backlog %d, block %d us, spin %d us)\n",
            mode, port, workers, backlog, WORK_US, SPIN_US);

    if (!strcmp(mode, "epoll")) { run_epoll(ls); return 0; }

    if (!strcmp(mode, "pool")) {
        for (int i = 0; i < workers; i++) {
            pthread_t t; pthread_create(&t, NULL, pool_body, NULL); pthread_detach(t);
        }
    }

    int accepted = 0;
    for (;;) {
        int c = accept(ls, NULL, NULL);
        if (c < 0) { if (errno == EINTR) continue; perror("accept"); break; }
        accepted++;
        if (!strcmp(mode, "iter"))        serve(c);
        else if (!strcmp(mode, "fork")) { if (fork() == 0) { close(ls); serve(c); _exit(0); } close(c); }
        else if (!strcmp(mode, "thread")) {
            pthread_t t;
            int rc = pthread_create(&t, NULL, thread_body, (void *)(long) c);
            if (rc == 0) pthread_detach(t);
            else {
                static int reported;
                if (!reported++) fprintf(stderr,
                    "pthread_create failed after %d connections: %s\n", accepted, strerror(rc));
                close(c);
            }
        }
        else if (!strcmp(mode, "pool"))   qput(c);
        else { fprintf(stderr, "modes: iter fork thread pool epoll\n"); return 2; }
    }
    return 0;
}
