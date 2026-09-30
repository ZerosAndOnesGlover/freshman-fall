/* fixed.c — PS 0, Problem 4: broken.c with every error corrected
 * PROG 101: Programming I — Structured Programming in C
 *
 * Each fix is marked with the matching entry number from error_log.md.
 *
 * Compile with:
 *   gcc -Wall -Wextra -Werror -g -std=c11 -o fixed fixed.c
 */

#include <stdio.h>                        /* E1: closing > added */
                                          /* E2: #include "helpers.h" removed */
#define VERSION 2

int describe(int code);
void summarise(int code);                 /* E8: declared here ... */

int main(void) {                          /* E3: main returns int */
    int status = 3;                       /* E4: missing ; */
    double ratio = 0.75;

    printf("Version: %d\n", VERSION);     /* E5: missing comma */
    printf("Ratio: %.2f\n", ratio);       /* E6: %f for a double */
    printf("Status: %d\n", status);       /* E7: %d for an int */

    describe(status);
    summarise(status);

    return 0;                             /* E3: 0 = success */
}

int describe(int code) {
    printf("Code %d\n", code);            /* E9: missing ; */
    if (code == 3) {                      /* E10: compare, not assign */
        printf("Status is three\n");
    }
    return 0;                             /* E11: int function must return */
}

void summarise(int code) {                /* E8: ... and defined here */
    printf("Summary: status %d\n", code);
}
