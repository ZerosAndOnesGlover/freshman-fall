/* PROJECT 2 -- Production HTTP Daemon (STARTER SCAFFOLD).
 *
 * As given, this is a single-threaded, un-hardened server that answers GET /
 * with "hello\n". It compiles and runs. Your job (see PROJECT 2) is to turn it
 * into a daemon that runs unattended -- reusing your Week 5-6 concurrent server
 * for the pool, and adding the production concerns marked TODO below.
 *
 * Build:  make            Run:  ./httpd 8080 4            Test: ../../lab/harness/bench 8080 50 200
 *
 * Do NOT commit the compiled binary.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>
#include <sys/socket.h>
#include <netinet/in.h>

/* TODO (Part 2): a self-pipe, a SIGTERM/SIGINT handler that writes one byte to
 * it, and signal(SIGPIPE, SIG_IGN). The main loop should poll() the listening
 * socket AND the pipe, and break out to drain on the pipe wakeup.            */

/* TODO (Part 1): a bounded connection queue (cond vars notempty/notfull) and a
 * fixed pool of worker threads that pop fds and call serve(). Reuse your
 * Week 5-6 server. Accept must apply backpressure when the queue is full.    */

/* TODO (Part 5): drop_privileges() -- setgroups(0,NULL); setgid(); setuid();
 * IN THAT ORDER. Only meaningful when started as root to bind a low port.    */

static void serve(int cfd)
{
    char buf[4096];
    ssize_t n = read(cfd, buf, sizeof buf - 1);       /* TODO (Part 4): bound and validate */
    if (n <= 0) { close(cfd); return; }
    buf[n] = 0;
    const char *body = "hello\n";
    char resp[256];
    int rl = snprintf(resp, sizeof resp,
        "HTTP/1.0 200 OK\r\nContent-Length: %zu\r\nConnection: close\r\n\r\n%s",
        strlen(body), body);
    ssize_t w = write(cfd, resp, rl);                  /* may EPIPE -- see Part 2 */
    if (w < 0 && errno == EPIPE) fprintf(stderr, "[worker] client gone (EPIPE)\n");
    close(cfd);
}

int main(int argc, char **argv)
{
    int port = argc > 1 ? atoi(argv[1]) : 8080;
    /* int nworkers = argc > 2 ? atoi(argv[2]) : 4;   -- wire up in Part 1 */

    int lfd = socket(AF_INET, SOCK_STREAM, 0);
    int one = 1; setsockopt(lfd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    struct sockaddr_in addr = {0};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);     /* TODO: INADDR_ANY once you drop privilege */
    addr.sin_port = htons(port);
    if (bind(lfd, (void *)&addr, sizeof addr) < 0) { fprintf(stderr, "bind :%d: %s\n", port, strerror(errno)); return 1; }
    if (listen(lfd, 128) < 0) { perror("listen"); return 1; }
    fprintf(stderr, "[httpd] pid %d listening on 127.0.0.1:%d (STARTER: single-threaded)\n", getpid(), port);

    /* STARTER accept loop: serve one connection at a time, no signals, no drain.
     * Replace with the poll()+pool+drain design from Parts 1 and 2. */
    for (;;) {
        int cfd = accept(lfd, 0, 0);
        if (cfd < 0) { if (errno == EINTR) continue; perror("accept"); continue; }
        serve(cfd);
    }
    return 0;
}
