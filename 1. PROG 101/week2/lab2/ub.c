/* ub.c — PROG 101 Lab 2, Part 2A: the sequence-point classic.
 * Deliberately undefined: i is modified twice with no sequence point.
 * Build without -Werror so the -Wsequence-point warning can be recorded.
 */
#include <stdio.h>

int main(void) {
    int i = 5;
    i = i++;
    printf("%d\n", i);
    return 0;
}
