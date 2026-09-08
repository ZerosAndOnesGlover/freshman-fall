/* Interposition: replace a libc function without touching the program. */
#define _GNU_SOURCE
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
time_t time(time_t *t)
{
    time_t fixed = 1000000000;                 /* 2001-09-09 */
    const char *e = getenv("FAKE_TIME");
    if (e) fixed = (time_t) atoll(e);
    if (t) *t = fixed;
    return fixed;
}
