/* dowhile.c — PROG 101 Lab 2, Part 3C: a do-while body runs even when the
 * condition is false on entry.
 */
#include <stdio.h>

int main(void) {
    int k = 100, iter = 0;

    do {
        iter++;
    } while (k < 10);

    printf("%d\n", iter);   /* prints 1: the body ran once before the false test */
    return 0;
}
