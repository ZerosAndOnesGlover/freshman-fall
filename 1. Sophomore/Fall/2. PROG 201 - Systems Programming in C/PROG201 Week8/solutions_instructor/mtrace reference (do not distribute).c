/* LD_PRELOAD malloc profiler.  The reference for PS 8. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dlfcn.h>
#include <stdatomic.h>

static void *(*real_malloc)(size_t);
static void  (*real_free)(void *);
static void *(*real_calloc)(size_t, size_t);
static void *(*real_realloc)(void *, size_t);

static atomic_long n_malloc, n_free, n_calloc, n_realloc;
static atomic_long bytes_total, live, peak;
static __thread int inside;                 /* stop recursion through dlsym */

/* dlsym itself calls calloc on the first call, before real_calloc is set.
 * A tiny bootstrap arena breaks that circle. */
static char boot[65536];
static size_t boot_used;
static int is_boot(void *p) { return (char *) p >= boot && (char *) p < boot + sizeof boot; }

static void *boot_alloc(size_t n)
{
    n = (n + 15) & ~(size_t) 15;
    if (boot_used + n > sizeof boot) return NULL;
    void *p = boot + boot_used;
    boot_used += n;
    return p;
}

static void init(void)
{
    static int done;
    if (done) return;
    done = 1;                                /* set BEFORE dlsym, not after */
    real_malloc  = dlsym(RTLD_NEXT, "malloc");
    real_calloc  = dlsym(RTLD_NEXT, "calloc");
    real_realloc = dlsym(RTLD_NEXT, "realloc");
    real_free    = dlsym(RTLD_NEXT, "free");
}

static void bump(long n)
{
    long l = atomic_fetch_add(&live, n) + n;
    long p = atomic_load(&peak);
    while (l > p && !atomic_compare_exchange_weak(&peak, &p, l)) ;
}

void *malloc(size_t n)
{
    if (!real_malloc) { if (inside) return boot_alloc(n); inside = 1; init(); inside = 0; }
    if (!real_malloc) return boot_alloc(n);
    void *p = real_malloc(n);
    if (p) { atomic_fetch_add(&n_malloc, 1);
             atomic_fetch_add(&bytes_total, (long) n); bump((long) n); }
    return p;
}

void *calloc(size_t a, size_t b)
{
    if (!real_calloc) { if (inside) { void *p = boot_alloc(a * b); if (p) memset(p, 0, a * b); return p; }
                        inside = 1; init(); inside = 0; }
    if (!real_calloc) { void *p = boot_alloc(a * b); if (p) memset(p, 0, a * b); return p; }
    void *p = real_calloc(a, b);
    if (p) { atomic_fetch_add(&n_calloc, 1);
             atomic_fetch_add(&bytes_total, (long)(a * b)); bump((long)(a * b)); }
    return p;
}

void *realloc(void *old, size_t n)
{
    if (!real_realloc) { inside = 1; init(); inside = 0; }
    if (is_boot(old)) { void *p = real_malloc ? real_malloc(n) : boot_alloc(n);
                        if (p && old) memcpy(p, old, n); return p; }
    void *p = real_realloc(old, n);
    if (p) atomic_fetch_add(&n_realloc, 1);
    return p;
}

void free(void *p)
{
    if (!p || is_boot(p)) return;            /* never free the bootstrap arena */
    if (!real_free) { inside = 1; init(); inside = 0; }
    atomic_fetch_add(&n_free, 1);
    real_free(p);
}

static atomic_int reported;

static void report(void)
{
    if (atomic_exchange(&reported, 1)) return;      /* at most once */
    char buf[512];
    int n = snprintf(buf, sizeof buf,
        "\n[mtrace] malloc %ld  calloc %ld  realloc %ld  free %ld\n"
        "[mtrace] total allocated %ld bytes, peak live %ld bytes\n"
        "[mtrace] %ld allocation(s) never freed\n",
        atomic_load(&n_malloc), atomic_load(&n_calloc), atomic_load(&n_realloc),
        atomic_load(&n_free), atomic_load(&bytes_total), atomic_load(&peak),
        atomic_load(&n_malloc) + atomic_load(&n_calloc) - atomic_load(&n_free));
    ssize_t w = write(2, buf, n); (void) w;   /* write, not printf: async-safe-ish */
}

__attribute__((destructor)) static void on_dtor(void) { report(); }

/* A destructor only runs if the program leaves through exit().  ls(1) and
 * grep(1) do not -- they call _exit.  So interpose both. */
void _exit(int status)
{
    report();
    void (*real)(int) = dlsym(RTLD_NEXT, "_exit");
    real(status);
    __builtin_unreachable();
}

void _Exit(int status)
{
    report();
    void (*real)(int) = dlsym(RTLD_NEXT, "_Exit");
    real(status);
    __builtin_unreachable();
}
