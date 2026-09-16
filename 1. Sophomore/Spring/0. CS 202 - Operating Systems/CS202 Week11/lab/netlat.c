/* netlat.c — the latency ladder: a function call, a system call, a pipe between two
 * processes, and a message over loopback TCP and UDP, all on one machine — so that the
 * cost of talking to another machine can be put beside them.
 *   gcc -O2 -Wall -Wextra -o netlat netlat.c && taskset -c 2 ./netlat
 * CS 202 Week 11, L34 §2. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

static volatile long sink;
static long __attribute__((noinline)) fn(long x) { return x + 1; }

static double pipe_rtt(int n)
{
    int a[2], b[2];
    if (pipe(a) || pipe(b)) return -1;
    pid_t p = fork();
    if (p == 0) {
        char c;
        for (int i = 0; i < n; i++) { if (read(a[0], &c, 1) != 1) _exit(1); if (write(b[1], &c, 1) != 1) _exit(1); }
        _exit(0);
    }
    char c = 'x';
    double t0 = now();
    for (int i = 0; i < n; i++) { if (write(a[1], &c, 1) != 1) break; if (read(b[0], &c, 1) != 1) break; }
    double t1 = now();
    waitpid(p, 0, 0);
    close(a[0]); close(a[1]); close(b[0]); close(b[1]);
    return (t1 - t0) * 1e6 / n;
}

static double sock_rtt(int type, int n)
{
    int srv = socket(AF_INET, type, 0);
    int one = 1;
    setsockopt(srv, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    struct sockaddr_in addr = { .sin_family = AF_INET, .sin_port = 0, .sin_addr.s_addr = htonl(INADDR_LOOPBACK) };
    if (bind(srv, (struct sockaddr *)&addr, sizeof addr)) { perror("bind"); return -1; }
    socklen_t len = sizeof addr;
    getsockname(srv, (struct sockaddr *)&addr, &len);
    if (type == SOCK_STREAM) listen(srv, 1);

    pid_t p = fork();
    if (p == 0) {
        char c;
        if (type == SOCK_STREAM) {
            int s = accept(srv, 0, 0);
            setsockopt(s, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);
            for (int i = 0; i < n; i++) { if (read(s, &c, 1) != 1) break; if (write(s, &c, 1) != 1) break; }
            close(s);
        } else {
            struct sockaddr_in from; socklen_t fl = sizeof from;
            for (int i = 0; i < n; i++) {
                if (recvfrom(srv, &c, 1, 0, (struct sockaddr *)&from, &fl) != 1) break;
                sendto(srv, &c, 1, 0, (struct sockaddr *)&from, fl);
            }
        }
        _exit(0);
    }
    int cl = socket(AF_INET, type, 0);
    if (connect(cl, (struct sockaddr *)&addr, sizeof addr)) { perror("connect"); return -1; }
    if (type == SOCK_STREAM) setsockopt(cl, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);
    char c = 'x';
    double t0 = now();
    for (int i = 0; i < n; i++) { if (write(cl, &c, 1) != 1) break; if (read(cl, &c, 1) != 1) break; }
    double t1 = now();
    close(cl); close(srv);
    waitpid(p, 0, 0);
    return (t1 - t0) * 1e6 / n;
}

int main(void)
{
    int n = 20000;
    double t0 = now();
    for (int i = 0; i < 1000000; i++) sink = fn(i);
    double t1 = now();
    printf("%-34s %9.4f us\n", "a function call", (t1 - t0) * 1e6 / 1000000);
    t0 = now();
    for (int i = 0; i < 200000; i++) sink = getppid();
    t1 = now();
    printf("%-34s %9.4f us\n", "a system call (getppid)", (t1 - t0) * 1e6 / 200000);
    printf("%-34s %9.4f us\n", "a pipe round trip, two processes", pipe_rtt(n));
    printf("%-34s %9.4f us\n", "loopback UDP round trip", sock_rtt(SOCK_DGRAM, n));
    printf("%-34s %9.4f us\n", "loopback TCP round trip", sock_rtt(SOCK_STREAM, n));
    return 0;
}
