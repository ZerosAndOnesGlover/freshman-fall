/* supervisor.c — PROG 201 Lab 0 skeleton.
 *
 *   ./supervisor <name>:<mode> ...        e.g.  ./supervisor web:ok db:crash
 *
 * Starts one ./flaky per argument and keeps it running. Your job is the six
 * TODOs below; everything else is here so that the lab is about processes and
 * signals rather than about argument parsing.
 *
 * It compiles and runs as given. It starts nothing, notices nothing, and exits
 * immediately — which is the baseline you are improving on.
 *
 * Build: make
 */
#define _GNU_SOURCE
#include <errno.h>
#include <poll.h>
#include <signal.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/wait.h>

#define MAX_CHILDREN 16
#define MAX_RESTARTS 5          /* restarts allowed ... */
#define WINDOW       10.0       /* ... inside this many seconds */
#define GRACE        2.0        /* seconds between SIGTERM and SIGKILL */

struct child {
    char        *name;
    char        *mode;
    pid_t        pid;           /* 0 = not running */
    int          restarts;      /* inside the current window */
    double       window_start;
    int          gave_up;
};

static struct child kids[MAX_CHILDREN];
static int          nkids;
static sigset_t     orig_mask;  /* the mask we had before blocking anything */

/* --- given: logging and small helpers ------------------------------------- */

static double now(void)
{
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + 1e-9 * t.tv_nsec;
}

/* NOT async-signal-safe. Call it from the main loop, never from a handler. */
static void logf_(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    fprintf(stderr, "[sup %8.3f] ", now());
    vfprintf(stderr, fmt, ap);
    va_end(ap);
    fflush(stderr);
}

static struct child *by_pid(pid_t p)
{
    for (int i = 0; i < nkids; i++) if (kids[i].pid == p) return &kids[i];
    return NULL;
}

static int all_gone(void)
{
    for (int i = 0; i < nkids; i++) if (kids[i].pid > 0) return 0;
    return 1;
}

/* --- TODO 1: the handlers -------------------------------------------------
 * Two flags, two handlers. A handler sets a flag and returns; it does not
 * reap, restart, or print. Read L03 §5 before you write these, and be careful
 * about the type of the flags.
 */

/* static volatile ??? child_died = 0; */
/* static volatile ??? stop_now   = 0; */

/* --- TODO 2: start one child ----------------------------------------------
 * fork(), and in the child exec ./flaky with argv[] = { "./flaky", name, mode }.
 *   - What must you do to stdio before forking?          (L01 §6)
 *   - What must the child do about the signal mask?      (L01 §7 — this one
 *     costs you Part C if you miss it, and the symptom is a child that will
 *     not stop)
 *   - What should the child do if exec fails?
 * Record the pid in c->pid and log the start.
 */
static void start(struct child *c)
{
    (void) c;
}

/* --- TODO 3: reap ---------------------------------------------------------
 * Reap every child that is ready — not one, every one; SIGCHLD does not queue
 * and one delivery can mean several deaths (L03 §3).
 *
 * For each: find it with by_pid(), clear its pid, and report how it died using
 * the W* macros (L02 §3 — check WIFEXITED before WEXITSTATUS).
 *
 * If restart is nonzero, apply the policy:
 *   - if more than WINDOW seconds have passed since window_start, reset the
 *     window and the counter;
 *   - if this child has now died more than MAX_RESTARTS times inside the
 *     window, set gave_up and log it instead of restarting;
 *   - otherwise start() it again.
 *
 * Return the number of children reaped.
 */
static int reap(int restart)
{
    (void) restart;
    return 0;
}

/* --- main ----------------------------------------------------------------- */

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s <name>:<mode> ...\n", argv[0]); return 2; }

    for (int i = 1; i < argc && nkids < MAX_CHILDREN; i++) {
        char *colon = strchr(argv[i], ':');
        if (!colon) { fprintf(stderr, "bad spec '%s'\n", argv[i]); return 2; }
        *colon = '\0';
        kids[nkids].name = argv[i];
        kids[nkids].mode = colon + 1;
        kids[nkids].window_start = now();
        nkids++;
    }

    /* --- TODO 4: block, then install -------------------------------------
     * Block SIGCHLD, SIGTERM and SIGINT and keep the old mask in orig_mask.
     * Then install the handlers with sigaction() — not signal() (L03 §2).
     *
     * Blocking BEFORE installing is not tidiness. A child can die between the
     * first start() and the first sigsuspend(), and if SIGCHLD is unblocked in
     * that window the delivery is gone.
     */

    for (int i = 0; i < nkids; i++) start(&kids[i]);

    /* --- TODO 5: the supervise loop ---------------------------------------
     * While no stop has been requested:
     *   - if child_died is set, clear it and reap(1);
     *   - if every child has either been given up on or exited, log and break;
     *   - otherwise wait for something to happen.
     *
     * "Wait for something to happen" is the interesting line. while (1) {} and
     * sleep(1) are both wrong, for different reasons; L03 §7 has the right
     * call and explains the race that rules out pause().
     */
    while (0) {
    }

    /* --- TODO 6: shut down ------------------------------------------------
     * On SIGTERM/SIGINT:
     *   - send SIGTERM to every running child;
     *   - give them GRACE seconds, reaping as they go — ppoll() with the old
     *     mask is a convenient way to sleep and stay interruptible;
     *   - SIGKILL anything still alive, then reap it. SIGKILL cannot be caught,
     *     so this reap may block.
     * Log every step: a supervisor whose shutdown is silent is a supervisor you
     * cannot debug.
     */

    logf_("supervisor exiting\n");
    return 0;
}
