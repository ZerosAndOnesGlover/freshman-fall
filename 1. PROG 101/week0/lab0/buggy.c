/* buggy.c — Fixed and documented, Week 0, Lab 0 (GDB exercise)
 *
 * THE BUG (now fixed):
 *   `total` was declared but never given a value, then read on the right-hand
 *   side of `total = total + add_three(a, b, c);`. A local of automatic storage
 *   duration is not zero-initialised: it holds whatever bytes happen to be in
 *   that stack slot, so the result was garbage and changed between runs.
 *
 *   gcc -Wall -g reported: warning: 'total' may be used uninitialized
 *
 * THE FIX:
 *   Initialise it — `int total = 0;` — so the accumulator starts from a known
 *   value. Compiling warning-free and running now prints Total: 60.
 *
 * Build:  gcc -Wall -Wextra -Werror -g -std=c11 -o buggy buggy.c
 */

#include <stdio.h>

int add_three(int a, int b, int c);

int main(void) {
    int total = 0;             /* FIX: was `int total;` — read before assignment */
    int a = 10;
    int b = 20;
    int c = 30;

    total = total + add_three(a, b, c);

    printf("Total:    %d\n", total);
    printf("Expected: %d\n", 10 + 20 + 30);
    return 0;
}

int add_three(int a, int b, int c) {
    return a + b + c;
}
