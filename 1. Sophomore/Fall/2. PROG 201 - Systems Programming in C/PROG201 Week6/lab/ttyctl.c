/* What the terminal does to a background process group. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <termios.h>
#include <sys/wait.h>

static const char *how(int st)
{
    static char b[64];
    if (WIFSTOPPED(st))  snprintf(b, sizeof b, "STOPPED by %s", strsignal(WSTOPSIG(st)));
    else if (WIFSIGNALED(st)) snprintf(b, sizeof b, "killed by %s", strsignal(WTERMSIG(st)));
    else snprintf(b, sizeof b, "exited %d", WEXITSTATUS(st));
    return b;
}

/* run `body` in a child that is in its own, BACKGROUND, process group */
static void background(const char *what, void (*body)(void))
{
    fflush(stdout);
    pid_t k = fork();
    if (k == 0) { setpgid(0, 0); body(); _exit(0); }
    setpgid(k, k);
    int st;
    waitpid(k, &st, WUNTRACED);
    printf("  %-42s %s\n", what, how(st));
    if (WIFSTOPPED(st)) { kill(-k, SIGKILL); kill(-k, SIGCONT); waitpid(k, NULL, 0); }
    fflush(stdout);
}

static void bg_read(void)  { char b[4]; ssize_t n = read(STDIN_FILENO, b, 1);
                             if (n < 0) { fprintf(stderr, "read: %s\n", strerror(errno)); _exit(7); } }
static void bg_write(void) { ssize_t r = write(STDOUT_FILENO, "  (background wrote this)\n", 26);
                             if (r < 0) _exit(8); }
static void bg_tcsetattr(void) { struct termios t; tcgetattr(STDIN_FILENO, &t);
                                 if (tcsetattr(STDIN_FILENO, TCSANOW, &t) < 0) _exit(9); }

int main(void)
{
    setvbuf(stdout, NULL, _IOLBF, 0);
    int tty = open("/dev/tty", O_RDWR);
    printf("foreground group is %d; this process is in %d\n", tcgetpgrp(tty), getpgrp());

    struct termios t; tcgetattr(tty, &t);
    printf("TOSTOP is %s by default\n\n", (t.c_lflag & TOSTOP) ? "SET" : "clear");

    printf("a process group that is NOT the foreground one:\n");
    background("read() from the terminal",        bg_read);
    background("write() to the terminal",         bg_write);
    background("tcsetattr() on the terminal",     bg_tcsetattr);

    t.c_lflag |= TOSTOP;
    tcsetattr(tty, TCSANOW, &t);
    printf("\nnow with TOSTOP set:\n");
    background("write() to the terminal",         bg_write);
    t.c_lflag &= ~TOSTOP;
    tcsetattr(tty, TCSANOW, &t);

    /* and the same three in the FOREGROUND group */
    printf("\nthe same process group, made foreground with tcsetpgrp:\n");
    fflush(stdout);
    pid_t k = fork();
    if (k == 0) {
        setpgid(0, 0);
        signal(SIGTTOU, SIG_IGN);
        tcsetpgrp(tty, getpgrp());                 /* claim the terminal */
        struct termios tt;
        tcgetattr(STDIN_FILENO, &tt);
        tcsetattr(STDIN_FILENO, TCSANOW, &tt);    /* allowed: we are foreground */
        if (write(STDOUT_FILENO, "  wrote, and was not stopped\n", 29) < 0) _exit(10);
        tcsetpgrp(tty, getppid());                 /* hand it back */
        _exit(0);
    }
    setpgid(k, k);
    int st; waitpid(k, &st, WUNTRACED);
    printf("  %-42s %s\n", "foreground group writing", how(st));
    close(tty);
    return 0;
}
