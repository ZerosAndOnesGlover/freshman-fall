/* Processes, groups, sessions, and the controlling terminal. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <sys/wait.h>

static void line(const char *who)
{
    int tty = open("/dev/tty", O_RDWR);
    pid_t fg = tty >= 0 ? tcgetpgrp(tty) : -1;
    printf("%-22s pid=%-8d ppid=%-8d pgid=%-8d sid=%-8d tcpgrp=%d%s\n",
           who, getpid(), getppid(), getpgrp(), getsid(0), fg,
           (fg == getpgrp()) ? "   <- foreground" : "");
    if (tty >= 0) close(tty);
    fflush(stdout);
}

int main(void)
{
    setvbuf(stdout, NULL, _IOLBF, 0);
    line("the shell's child");

    pid_t a = fork();
    if (a == 0) { line("  fork, nothing else"); _exit(0); }
    waitpid(a, NULL, 0);

    pid_t b = fork();
    if (b == 0) {
        if (setpgid(0, 0) < 0) perror("setpgid");        /* its own group */
        line("  after setpgid(0,0)");
        _exit(0);
    }
    setpgid(b, b);                       /* the parent does it too -- see below */
    waitpid(b, NULL, 0);

    pid_t c = fork();
    if (c == 0) {
        if (setsid() < 0) perror("setsid");              /* its own session */
        line("  after setsid()");
        _exit(0);
    }
    waitpid(c, NULL, 0);

    /* a two-process pipeline in one group, the way a shell builds one */
    pid_t lead = 0;
    for (int i = 0; i < 2; i++) {
        pid_t k = fork();
        if (k == 0) {
            setpgid(0, lead);            /* stage 0 leads; stage 1 joins it */
            char w[32]; snprintf(w, sizeof w, "  pipeline stage %d", i);
            line(w);
            _exit(0);
        }
        if (i == 0) lead = k;
        setpgid(k, lead);
    }
    while (wait(NULL) > 0) ;
    return 0;
}
