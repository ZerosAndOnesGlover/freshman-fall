/* overflow.c — PROG 101, Week 1, Problem Set 1 (Problem 5)
 * Unsigned wrap-around (defined) vs signed overflow (undefined behaviour,
 * caught by the UndefinedBehaviorSanitizer).
 *
 *   gcc -Wall -Wextra -std=c11 -fsanitize=undefined -g -o overflow overflow.c
 */

#include <stdio.h>
#include <limits.h>

int main(void) {
    unsigned int u = UINT_MAX;
    int i = INT_MAX;

    printf("unsigned: UINT_MAX + 1 = %u\n", u + 1u);
    printf("signed:   INT_MAX + 1  = %d\n", i + 1);

    return 0;
}
