/* precedence.c — PROG 101 Lab 2, Part 1A: the parenthesis gallery.
 * Predictions were written before running (see answers.md).
 * NOTE: lines 1 and 3 draw -Wparentheses by design, so this file is
 * built without -Werror (see Makefile, `make demos`).
 */
#include <stdio.h>

int main(void) {
    int a = 6, b = 3, c = 2;

    printf("%d\n", a & b == c);      /* 1: predicted 0 (parsed a & (b==c))        */
    printf("%d\n", (a & b) == c);    /* 2: predicted 1 ((6&3)==2 -> 2==2)         */
    printf("%d\n", 1 << 2 + 3);      /* 3: predicted 32 (parsed 1 << (2+3))       */
    printf("%d\n", (1 << 2) + 3);    /* 4: predicted 7 (4+3)                      */
    printf("%d\n", a + b % c);       /* 5: predicted 7 (a + (b%c) = 6+1)          */
    printf("%d\n", ~5);              /* 6: predicted -6 (~x == -x-1)              */
    printf("%d\n", 5 ^ 3);           /* 7: predicted 6 (0101 ^ 0011)              */

    return 0;
}
