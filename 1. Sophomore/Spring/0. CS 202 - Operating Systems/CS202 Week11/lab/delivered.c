/* delivered.c — a write() to a socket succeeds long after the reader has stopped
 * reading: what "sent" means.  CS 202 Week 11, L34 §3. */
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/wait.h>
#include <fcntl.h>
int main(void)
{
    int srv = socket(AF_INET, SOCK_STREAM, 0), one = 1;
    setsockopt(srv, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    struct sockaddr_in a = { .sin_family = AF_INET, .sin_addr.s_addr = htonl(INADDR_LOOPBACK) };
    bind(srv, (struct sockaddr *)&a, sizeof a);
    socklen_t l = sizeof a; getsockname(srv, (struct sockaddr *)&a, &l);
    listen(srv, 1);
    pid_t p = fork();
    if (p == 0) { int s = accept(srv, 0, 0); pause(); _exit(0); (void)s; }
    int cl = socket(AF_INET, SOCK_STREAM, 0);
    connect(cl, (struct sockaddr *)&a, sizeof a);
    kill(p, SIGSTOP);                       /* the peer will never read again */
    fcntl(cl, F_SETFL, O_NONBLOCK);
    char buf[4096];
    memset(buf, 'x', sizeof buf);
    long total = 0;
    for (;;) {
        ssize_t r = write(cl, buf, sizeof buf);
        if (r <= 0) break;
        total += r;
    }
    printf("write() reported success for %ld bytes the peer never read\n", total);
    printf("and then refused, with the connection still open\n");
    kill(p, SIGKILL); waitpid(p, 0, 0);
    return 0;
}
