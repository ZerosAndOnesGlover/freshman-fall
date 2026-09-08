/* Open N connections and keep them open.  What does a connection cost? */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>
#include <sys/socket.h>
#include <sys/resource.h>
#include <netinet/in.h>

static long rss_of(int pid)
{
    char path[64]; snprintf(path, sizeof path, "/proc/%d/status", pid);
    FILE *f = fopen(path, "r"); if (!f) return -1;
    char line[256]; long v = -1;
    while (fgets(line, sizeof line, f)) if (!strncmp(line, "VmRSS:", 6)) { sscanf(line+6, "%ld", &v); break; }
    fclose(f); return v;
}

int main(int argc, char **argv)
{
    signal(SIGPIPE, SIG_IGN);
    int port = argc > 1 ? atoi(argv[1]) : 18080;
    int want = argc > 2 ? atoi(argv[2]) : 10000;
    int srv  = argc > 3 ? atoi(argv[3]) : 0;

    struct rlimit rl; getrlimit(RLIMIT_NOFILE, &rl);
    long rss0 = srv ? rss_of(srv) : -1;

    struct sockaddr_in a = { .sin_family = AF_INET, .sin_port = htons(port),
                             .sin_addr.s_addr = htonl(INADDR_LOOPBACK) };
    int *fds = calloc(want, sizeof *fds);
    int n = 0;
    for (; n < want; n++) {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        if (s < 0) { printf("socket failed at %d: %s\n", n, strerror(errno)); break; }
        if (connect(s, (struct sockaddr *) &a, sizeof a) < 0) {
            printf("connect failed at %d: %s\n", n, strerror(errno));
            close(s); break;
        }
        fds[n] = s;
        if (n && n % 2000 == 0 && srv) {
            printf("  %6d connections: server RSS %ld MiB\n", n, rss_of(srv) / 1024);
            fflush(stdout);
        }
    }
    long rss1 = srv ? rss_of(srv) : -1;
    printf("held %d connections\n", n);
    if (srv > 0 && rss0 > 0 && rss1 > 0)
        printf("server RSS %ld -> %ld kB  = %.1f kB per connection\n",
               rss0, rss1, (double)(rss1 - rss0) / (n ? n : 1));
    printf("client RLIMIT_NOFILE %lu\n", (unsigned long) rl.rlim_cur);
    for (int i = 0; i < n; i++) close(fds[i]);
    return 0;
}
