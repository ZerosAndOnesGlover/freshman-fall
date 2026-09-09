/* A sampling profiler in one file.  No privileges, no perf events.
 *
 * setitimer(ITIMER_PROF) delivers SIGPROF every `interval` of CPU time;
 * the handler reads the interrupted instruction pointer out of the
 * ucontext and records it.  That is what a sampling profiler is.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <dlfcn.h>
#include <ucontext.h>
#include <sys/time.h>

#define MAXSAMP 200000
static void *samples[MAXSAMP];
static volatile long nsamp;
static volatile long lost;

static void on_prof(int sig, siginfo_t *si, void *uc)
{
    (void) sig; (void) si;
    ucontext_t *c = uc;
    void *ip = (void *) c->uc_mcontext.gregs[REG_RIP];   /* x86-64 */
    if (nsamp < MAXSAMP) samples[nsamp++] = ip;
    else lost++;
}

void sprof_start(long usec)
{
    struct sigaction sa;
    memset(&sa, 0, sizeof sa);
    sa.sa_sigaction = on_prof;
    sa.sa_flags = SA_SIGINFO | SA_RESTART;
    sigemptyset(&sa.sa_mask);
    if (sigaction(SIGPROF, &sa, NULL) < 0) { perror("sigaction"); return; }

    struct itimerval it = { { 0, usec }, { 0, usec } };
    if (setitimer(ITIMER_PROF, &it, NULL) < 0) perror("setitimer");
}

struct bucket { void *base; const char *name; long n; };

void sprof_report(int topn)
{
    struct itimerval off = { { 0, 0 }, { 0, 0 } };
    setitimer(ITIMER_PROF, &off, NULL);

    static struct bucket b[512];
    int nb = 0;
    for (long i = 0; i < nsamp; i++) {
        Dl_info info;
        void *base = NULL; const char *name = "??";
        if (dladdr(samples[i], &info) && info.dli_sname) {
            base = info.dli_saddr; name = info.dli_sname;
        } else if (dladdr(samples[i], &info)) {
            base = info.dli_fbase; name = info.dli_fname ? info.dli_fname : "??";
        }
        int k;
        for (k = 0; k < nb; k++) if (b[k].base == base && !strcmp(b[k].name, name)) break;
        if (k == nb && nb < 512) { b[nb].base = base; b[nb].name = name; b[nb].n = 0; nb++; }
        if (k < 512) b[k].n++;
    }
    for (int i = 0; i < nb; i++)
        for (int j = i + 1; j < nb; j++)
            if (b[j].n > b[i].n) { struct bucket t = b[i]; b[i] = b[j]; b[j] = t; }

    fprintf(stderr, "\n[sprof] %ld samples", nsamp);
    if (lost) fprintf(stderr, " (%ld lost -- buffer full)", lost);
    fprintf(stderr, "\n[sprof] %-7s %-8s %s\n", "samples", "percent", "function");
    for (int i = 0; i < nb && i < topn; i++)
        fprintf(stderr, "[sprof] %7ld %7.2f%%  %s\n",
                b[i].n, 100.0 * b[i].n / (nsamp ? nsamp : 1), b[i].name);
}
