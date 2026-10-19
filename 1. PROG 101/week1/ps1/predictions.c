/* predictions.c — PROG 101, Week 1, Problem Set 1 (Problem 3)
 * Predict, then run. One straight-line main, five snippets.
 * Each snippet carries a PREDICTION comment written before running.
 *
 *   gcc -Wall -Wextra -std=c11 -o predictions predictions.c
 */

#include <stdio.h>

int main(void) {
    /* Snippet 1 — PREDICTION: b is unsigned, so a is converted to a huge
     * unsigned value; a < b is false -> 0. (This is the -Wsign-compare warning.) */
    int a = -1;
    unsigned int b = 1;
    printf("1: a < b is %d\n", a < b);

    /* Snippet 2 — PREDICTION: char is signed here; 200 does not fit, so it is
     * reinterpreted as 200 - 256 = -56. */
    char c = 200;              /* char may be signed on your system */
    printf("2: %d\n", c);

    /* Snippet 3 — PREDICTION: unsigned arithmetic is modulo 2^32,
     * so 0 - 1 wraps to 4294967295. */
    unsigned int u = 0;
    u = u - 1;
    printf("3: %u\n", u);

    /* Snippet 4 — PREDICTION: the cast truncates toward zero, so
     * 3.9 -> 3 and -3.9 -> -3. */
    int x = (int)3.9;
    int y = (int)-3.9;
    printf("4: %d %d\n", x, y);

    /* Snippet 5 — PREDICTION: integer division truncates toward zero and %
     * takes the sign of the dividend: 3 -3 1 -1. */
    printf("5: %d %d %d %d\n", 7 / 2, -7 / 2, 7 % 3, -7 % 3);

    return 0;
}
