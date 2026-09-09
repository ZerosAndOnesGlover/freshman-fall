/* PROG 201 Week 12 -- load client for the harness (ab is not installed).
 * Opens C connections in parallel, each firing R sequential GET requests to a
 * path, and reports throughput and mean/p50/p99/max latency.
 *
 *   bench PORT [CONNS] [PER_CONN] [PATH]
 *   bench 8080 50 200            # 50 conns x 200 reqs to "/"
 *   bench 8080 10 4 /slow        # exercise a blocking endpoint
 *
 * Build: make        (warning-clean under -Wall -Wextra)
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

static int PORT, PER;
static const char *PATH = "/";
static double *lat; static int latn;
static pthread_mutex_t lm = PTHREAD_MUTEX_INITIALIZER; static int li = 0;

static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec + t.tv_nsec/1e9; }

static void *client(void *a)
{
    (void)a;
    char req[256];
    int rl = snprintf(req, sizeof req, "GET %s HTTP/1.0\r\n\r\n", PATH);
    for (int r = 0; r < PER; r++) {
        double t0 = now();
        int fd = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in s = {0};
        s.sin_family = AF_INET; s.sin_addr.s_addr = htonl(INADDR_LOOPBACK); s.sin_port = htons(PORT);
        if (connect(fd, (void *)&s, sizeof s) < 0) { close(fd); continue; }
        if (write(fd, req, rl) != rl) { close(fd); continue; }
        char b[512]; while (read(fd, b, sizeof b) > 0) { }
        close(fd);
        double d = now() - t0;
        pthread_mutex_lock(&lm); if (li < latn) lat[li++] = d; pthread_mutex_unlock(&lm);
    }
    return 0;
}

static int cmp(const void *a, const void *b){ double x=*(const double*)a, y=*(const double*)b; return x<y?-1:(x>y?1:0); }

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s PORT [CONNS] [PER_CONN] [PATH]\n", argv[0]); return 2; }
    PORT = atoi(argv[1]);
    int C = argc > 2 ? atoi(argv[2]) : 50;
    PER   = argc > 3 ? atoi(argv[3]) : 200;
    if (argc > 4) PATH = argv[4];

    latn = C * PER; lat = malloc(sizeof(double) * latn);
    pthread_t *th = malloc(sizeof(pthread_t) * C);
    double t0 = now();
    for (int i = 0; i < C; i++) pthread_create(&th[i], 0, client, 0);
    for (int i = 0; i < C; i++) pthread_join(th[i], 0);
    double dt = now() - t0;

    qsort(lat, li, sizeof(double), cmp);
    double sum = 0; for (int i = 0; i < li; i++) sum += lat[i];
    printf("requests=%d  conns=%d  wall=%.3fs  throughput=%.0f req/s\n", li, C, dt, li/dt);
    if (li) printf("latency mean=%.2fms  p50=%.2fms  p99=%.2fms  max=%.2fms\n",
        sum/li*1e3, lat[li/2]*1e3, lat[(int)(li*0.99)]*1e3, lat[li-1]*1e3);
    free(lat); free(th);
    return 0;
}
