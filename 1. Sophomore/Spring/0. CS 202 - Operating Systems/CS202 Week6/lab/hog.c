/* hog.c — allocate and fill memory one MiB at a time, reporting every 16 MiB.
 *   gcc -O2 -Wall -Wextra -o hog hog.c && ./hog MIB
 * CS 202 Week 6, Lab 6. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv)
{
    long want = argc > 1 ? atol(argv[1]) : 1024;
    for (long mib = 1; mib <= want; mib++) {
        char *p = malloc(1 << 20);
        if (!p) { printf("malloc refused at %ld MiB\n", mib); return 1; }
        memset(p, (int)(mib & 0x7f) + 1, 1 << 20);
        if (mib % 16 == 0) { printf("%ld MiB\n", mib); fflush(stdout); }
    }
    printf("done: %ld MiB\n", want);
    return 0;
}
