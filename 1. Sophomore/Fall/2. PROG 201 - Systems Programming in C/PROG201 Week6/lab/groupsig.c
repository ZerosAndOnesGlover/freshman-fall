/* Ctrl-C goes to a process GROUP, not to a process. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/wait.h>

static void sleeper(const char *tag)
{
    (void) tag;
    for (;;) pause();
}

int main(void)
{
    setvbuf(stdout, NULL, _IOLBF, 0);
    int tty = open("/dev/tty", O_RDWR);
    printf("shell pgid %d, terminal foreground group %d\n\n", getpgrp(), tcgetpgrp(tty));

    /* Group A: three children in ONE group, like a pipeline */
    pid_t lead = 0, kids[3];
    for (int i = 0; i < 3; i++) {
        pid_t k = fork();
        if (k == 0) { setpgid(0, lead); sleeper("a"); _exit(0); }
        if (i == 0) lead = k;
        setpgid(k, lead);
        kids[i] = k;
    }
    /* Group B: one child in its own group -- a "background job" */
    pid_t other = fork();
    if (other == 0) { setpgid(0, 0); sleeper("b"); _exit(0); }
    setpgid(other, other);

    usleep(200000);
    printf("group A = %d (3 processes), group B = %d (1 process)\n", lead, other);

    printf("\nkill(%d, SIGINT)   -- one process by pid:\n", kids[1]);
    kill(kids[1], SIGINT);
    usleep(200000);
    for (int i = 0; i < 3; i++) {
        int st; pid_t r = waitpid(kids[i], &st, WNOHANG);
        printf("  A[%d] pid %d: %s\n", i, kids[i],
               r == 0 ? "still running" : WIFSIGNALED(st) ? strsignal(WTERMSIG(st)) : "gone");
    }

    printf("\nkill(-%d, SIGINT)  -- the whole group (note the minus):\n", lead);
    kill(-lead, SIGINT);
    usleep(200000);
    for (int i = 0; i < 3; i++) {
        int st; pid_t r = waitpid(kids[i], &st, WNOHANG);
        printf("  A[%d] pid %d: %s\n", i, kids[i],
               r == 0 ? "still running" : r < 0 ? "already reaped"
                      : WIFSIGNALED(st) ? strsignal(WTERMSIG(st)) : "gone");
    }
    int st; pid_t r = waitpid(other, &st, WNOHANG);
    printf("  B    pid %d: %s   <- a different group, untouched\n", other,
           r == 0 ? "still running" : "gone");

    kill(-other, SIGKILL);
    while (wait(NULL) > 0) ;
    close(tty);
    return 0;
}
