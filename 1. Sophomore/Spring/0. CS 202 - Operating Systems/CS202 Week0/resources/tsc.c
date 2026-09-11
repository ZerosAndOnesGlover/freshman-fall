/* tsc.c: the kernel decides whether RDTSC is privileged, per process.
 *
 *   gcc -O2 -Wall -Wextra -o tsc tsc.c && ./tsc
 *
 * CS 202 Week 0, L02 §4. */
#include <stdio.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <unistd.h>
#include <x86intrin.h>

static void try(const char *when)
{
    fflush(stdout);
    pid_t p = fork();
    if (p == 0) { unsigned long long t = __rdtsc(); printf("  %s: rdtsc = %llu\n", when, t); fflush(stdout); _exit(0); }
    int st; waitpid(p, &st, 0);
    if (WIFSIGNALED(st)) printf("  %s: killed by signal %d\n", when, WTERMSIG(st));
}

int main(void)
{
    int mode;
    prctl(PR_GET_TSC, &mode);
    printf("PR_GET_TSC = %s\n", mode == PR_TSC_ENABLE ? "PR_TSC_ENABLE" : "PR_TSC_SIGSEGV");
    try("before");
    printf("prctl(PR_SET_TSC, PR_TSC_SIGSEGV) = %d\n", prctl(PR_SET_TSC, PR_TSC_SIGSEGV));
    try("after ");
    return 0;
}
