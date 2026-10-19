/* overflow.c — PROG 101 Lab 2, Part 2B: signed overflow.
 * Deliberately undefined: INT_MAX + 1. UBSan reports it at run time.
 */
#include <stdio.h>
#include <limits.h>

int main(void) {
    int x = INT_MAX;
    printf("%d\n", x + 1);
    return 0;
}
