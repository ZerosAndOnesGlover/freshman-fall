/* sizes.c — PROG 101 Lab 1, Part 1A: sizeof of the basic types */
#include <stdio.h>

int main(void) {
    printf("char        %zu\n", sizeof(char));
    printf("short       %zu\n", sizeof(short));
    printf("int         %zu\n", sizeof(int));
    printf("long        %zu\n", sizeof(long));
    printf("long long   %zu\n", sizeof(long long));
    printf("float       %zu\n", sizeof(float));
    printf("double      %zu\n", sizeof(double));
    printf("long double %zu\n", sizeof(long double));
    return 0;
}
