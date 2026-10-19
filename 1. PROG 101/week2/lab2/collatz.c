/* collatz.c — PROG 101 Lab 2, Part 3B: trace the Collatz loop from x = 27. */
#include <stdio.h>

int main(void) {
    int x = 27, steps = 0;

    while (x != 1) {
        x = (x % 2) ? 3 * x + 1 : x / 2;
        steps++;
    }

    printf("steps = %d\n", steps);
    return 0;
}
