/* states.c: put one process in each state the kernel reports, and read them back. */
#define _GNU_SOURCE
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <unistd.h>

static char state_of(pid_t p)
{
    char path[64], buf[512];
    snprintf(path, sizeof path, "/proc/%d/stat", p);
    FILE *f = fopen(path, "r");
    if (!f) return '?';
    size_t n = fread(buf, 1, sizeof buf - 1, f);
    fclose(f);
    buf[n] = 0;
    char *rp = strrchr(buf, ')');      /* comm may contain spaces; state follows the last ')' */
    return rp ? rp[2] : '?';
}

int main(void)
{
    pid_t running = fork();
    if (running == 0) { for (;;) ; }

    pid_t sleeping = fork();
    if (sleeping == 0) { pause(); _exit(0); }

    pid_t stopped = fork();
    if (stopped == 0) { pause(); _exit(0); }

    pid_t zombie = fork();
    if (zombie == 0) _exit(7);

    pid_t traced = fork();
    if (traced == 0) { ptrace(PTRACE_TRACEME, 0, 0, 0); raise(SIGSTOP); pause(); _exit(0); }

    pid_t vforker = fork();
    if (vforker == 0) {
        pid_t c = vfork();
        if (c == 0) { sleep(3); _exit(0); }   /* undefined in strict terms; enough to hold the parent */
        _exit(0);
    }

    usleep(300000);
    kill(stopped, SIGSTOP);
    usleep(300000);

    printf("%-32s %-8s %s\n", "what", "pid", "state");
    printf("%-32s %-8d %c\n", "busy loop", running, state_of(running));
    printf("%-32s %-8d %c\n", "pause()", sleeping, state_of(sleeping));
    printf("%-32s %-8d %c\n", "SIGSTOP", stopped, state_of(stopped));
    printf("%-32s %-8d %c\n", "exited, not reaped", zombie, state_of(zombie));
    printf("%-32s %-8d %c\n", "stopped under ptrace", traced, state_of(traced));
    printf("%-32s %-8d %c\n", "parent waiting in vfork()", vforker, state_of(vforker));
    printf("%-32s %-8d %c\n", "this process, reading /proc", getpid(), state_of(getpid()));

    kill(running, SIGKILL); kill(sleeping, SIGKILL); kill(stopped, SIGKILL);
    kill(traced, SIGKILL);
    sleep(4);
    while (wait(0) > 0) ;
    return 0;
}
