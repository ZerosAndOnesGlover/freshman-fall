/* limits.c — PROG 101, Week 1, Problem Set 1 (Problem 1)
 * One row per integer type: sizeof plus <limits.h> min and max,
 * then sizeof for float and double. Columns are field-width aligned.
 *
 *   gcc -Wall -Wextra -std=c11 -o limits limits.c
 */

#include <stdio.h>
#include <limits.h>

int main(void) {
    printf("%-15s %6s %22s %22s\n", "type", "bytes", "min", "max");

    printf("%-15s %6zu %22d %22d\n", "signed char",
           sizeof(signed char), SCHAR_MIN, SCHAR_MAX);
    printf("%-15s %6zu %22d %22u\n", "unsigned char",
           sizeof(unsigned char), 0, (unsigned)UCHAR_MAX);
    printf("%-15s %6zu %22d %22d\n", "short",
           sizeof(short), SHRT_MIN, SHRT_MAX);
    printf("%-15s %6zu %22d %22u\n", "unsigned short",
           sizeof(unsigned short), 0, (unsigned)USHRT_MAX);
    printf("%-15s %6zu %22d %22d\n", "int",
           sizeof(int), INT_MIN, INT_MAX);
    printf("%-15s %6zu %22u %22u\n", "unsigned int",
           sizeof(unsigned int), 0u, UINT_MAX);
    printf("%-15s %6zu %22ld %22ld\n", "long",
           sizeof(long), LONG_MIN, LONG_MAX);
    printf("%-15s %6zu %22lld %22lld\n", "long long",
           sizeof(long long), LLONG_MIN, LLONG_MAX);

    printf("%-15s %6zu\n", "float", sizeof(float));
    printf("%-15s %6zu\n", "double", sizeof(double));

    return 0;
}
