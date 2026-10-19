/* fixed.c — PROG 101, Week 0, Problem Set 0 (Problem 4)
 * The corrected broken.c: all ten planted defects fixed.
 *
 *   gcc -Wall -Wextra -Werror -std=c11 fixed.c -o fixed
 */

#include <stdio.h>

#define VERSION 2

int describe(int code);
void summarise(int code);

int main(void) {
    int status = 3;
    double ratio = 0.75;

    printf("Version: %d\n", VERSION);
    printf("Ratio: %f\n", ratio);
    printf("Status: %d\n", status);

    describe(status);
    summarise(status);

    return 0;
}

int describe(int code) {
    printf("Code %d\n", code);
    if (code == 3) {
        printf("Status is three\n");
    }
    return 0;
}

void summarise(int code) {
    printf("Summary: code %d handled.\n", code);
}
