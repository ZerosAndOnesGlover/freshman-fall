/* kread.c: try to read one byte at an address given in hex.
 *
 *   gcc -O2 -Wall -Wextra -o kread kread.c
 *   ./kread ffffffff81000000
 *
 * CS 202 Week 0, L02 §6. */
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static void on_segv(int sig, siginfo_t *si, void *uc)
{
    (void)sig; (void)uc;
    char buf[160];
    const char *code = si->si_code == SEGV_MAPERR ? "SEGV_MAPERR"
                     : si->si_code == SEGV_ACCERR ? "SEGV_ACCERR" : "other";
    int n = snprintf(buf, sizeof buf, "SIGSEGV at %p, si_code %s\n", si->si_addr, code);
    if (write(1, buf, n) < 0)       /* snprintf is not async-signal-safe in general; */
        _exit(2);                   /* here the process exits immediately after      */
    _exit(0);
}

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s <hex address>\n", argv[0]);
        return 1;
    }
    struct sigaction sa;
    memset(&sa, 0, sizeof sa);
    sa.sa_sigaction = on_segv;
    sa.sa_flags = SA_SIGINFO;
    sigaction(SIGSEGV, &sa, 0);

    unsigned long addr = strtoul(argv[1], 0, 16);
    printf("reading 0x%lx ... ", addr);
    fflush(stdout);
    volatile char c = *(char *)addr;
    printf("got 0x%02x\n", (unsigned char)c);
    return 0;
}
