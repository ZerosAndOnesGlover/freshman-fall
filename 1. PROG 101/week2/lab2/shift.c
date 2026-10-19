/* shift.c — PROG 101 Lab 2, Part 2C: shifting into the sign bit.
 * Deliberately undefined: 1 << 31 on a signed int. UBSan reports it.
 * The one-character fix is 1u << 31.
 */
#include <stdio.h>

int main(void) {
    int s = 1;
    printf("%d\n", s << 31);
    return 0;
}
