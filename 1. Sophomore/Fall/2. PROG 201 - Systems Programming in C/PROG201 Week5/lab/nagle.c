/* Nagle's algorithm meets delayed ACK: the 40-millisecond mystery. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <time.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <signal.h>

static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}

#define ROUNDS 20

static void server(int port)
{
    int ls = socket(AF_INET, SOCK_STREAM, 0);
    int one = 1; setsockopt(ls, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(port),
                             .sin_addr.s_addr = htonl(INADDR_LOOPBACK) };
    if (bind(ls, (struct sockaddr *)&a, sizeof a) < 0) { perror("bind"); _exit(1); }
    listen(ls, 8);
    for (int conn = 0; conn < 2; conn++) {
        int c = accept(ls, NULL, NULL);
        setsockopt(c, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);  /* reply at once */
        for (int i = 0; i < ROUNDS; i++) {
            char buf[64]; size_t got = 0;
            while (got < 5) {                       /* header(1) + body(4) */
                ssize_t k = read(c, buf + got, 5 - got);
                if (k <= 0) goto next;
                got += k;
            }
            if (write(c, "ok", 2) != 2) goto next;
        }
    next:
        close(c);
    }
    close(ls);
    _exit(0);
}

static double client(int port, int nodelay)
{
    int s = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(port),
                             .sin_addr.s_addr = htonl(INADDR_LOOPBACK) };
    if (connect(s, (struct sockaddr *)&a, sizeof a) < 0) { perror("connect"); exit(1); }
    if (nodelay) { int one = 1; setsockopt(s, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one); }

    double total = 0;
    for (int i = 0; i < ROUNDS; i++) {
        double t0 = now();
        if (write(s, "H", 1) != 1) break;           /* write 1: the header */
        if (write(s, "body", 4) != 4) break;        /* write 2: the body   */
        char r[8];
        if (read(s, r, sizeof r) <= 0) break;       /* wait for the reply  */
        total += now() - t0;
    }
    close(s);
    return total / ROUNDS * 1000;                   /* ms per round trip */
}

int main(int argc, char **argv)
{
    int port = argc > 1 ? atoi(argv[1]) : 19100;
    pid_t k = fork();
    if (k == 0) server(port);
    usleep(300000);
    double with_nagle = client(port, 0);
    double without    = client(port, 1);
    kill(k, SIGKILL); wait(NULL);
    printf("two small writes then wait for a reply, %d round trips:\n", ROUNDS);
    printf("  Nagle on (default)        : %8.3f ms per round trip\n", with_nagle);
    printf("  TCP_NODELAY               : %8.3f ms per round trip\n", without);
    printf("  ratio                     : %8.1fx\n", with_nagle / without);
    return 0;
}
