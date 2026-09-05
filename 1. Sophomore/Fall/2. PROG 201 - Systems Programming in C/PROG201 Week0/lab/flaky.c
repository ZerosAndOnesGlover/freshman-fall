/* flaky.c — a child that fails in the four ways a supervisor has to tell apart.
 *
 *   ./flaky <name> <mode>
 *
 *   ok      run for 30s, then exit 0            (a healthy worker)
 *   exit    run for <1s, then exit 1            (a worker that gives up)
 *   crash   dereference NULL after ~1s          (SIGSEGV)
 *   hang    ignore SIGTERM and loop forever     (needs SIGKILL to stop)
 *   flap    exit 1 immediately, every time      (a crash loop)
 *
 * Build: gcc -Wall -Wextra -O2 -o flaky flaky.c
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc != 3) { fprintf(stderr, "usage: %s <name> <ok|exit|crash|hang|flap>\n", argv[0]); return 2; }
    const char *name = argv[1], *mode = argv[2];

    fprintf(stderr, "[%s] pid %d started in mode '%s'\n", name, getpid(), mode);

    if (!strcmp(mode, "flap"))  return 1;
    if (!strcmp(mode, "hang"))  { signal(SIGTERM, SIG_IGN); for (;;) pause(); }

    sleep(1);
    if (!strcmp(mode, "exit"))  return 1;
    if (!strcmp(mode, "crash")) { volatile int *p = NULL; return *p; }

    sleep(29);
    return 0;
}
