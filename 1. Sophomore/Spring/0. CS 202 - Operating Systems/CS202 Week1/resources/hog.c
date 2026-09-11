/* hog vs sleeper on one CPU: who gets switched out voluntarily, and who involuntarily? */
#define _GNU_SOURCE
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
static void show(const char *who, pid_t p)
{
    char path[64], line[128];
    snprintf(path, sizeof path, "/proc/%d/status", p);
    FILE *f = fopen(path, "r");
    while (fgets(line, sizeof line, f))
        if (strstr(line, "ctxt_switches")) printf("%-8s %s", who, line);
    fclose(f);
}
int main(void)
{
    cpu_set_t s; CPU_ZERO(&s); CPU_SET(5, &s); sched_setaffinity(0, sizeof s, &s);
    pid_t hog = fork();
    if (hog == 0) { volatile unsigned long x = 0; for (;;) x++; }
    pid_t sleeper = fork();
    if (sleeper == 0) { for (;;) usleep(1000); }
    sleep(5);
    show("hog", hog); show("sleeper", sleeper);
    kill(hog, SIGKILL); kill(sleeper, SIGKILL);
    while (wait(0) > 0) ;
    return 0;
}
