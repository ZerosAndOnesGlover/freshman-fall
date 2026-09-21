/* buggy.c — Intentionally Buggy Program for GDB Lab
 * PROG 101: Programming I — Structured Programming in C
 *
 * This program has one intentional bug: a variable is read before it is
 * given a value (Lecture 03, "Common Beginner Errors").
 * Your job: find it with the compiler's warnings and with GDB.
 *
 * Compile with:
 *   gcc -Wall -g -std=c11 -o buggy buggy.c
 * Then:
 *   gdb ./buggy
 */

#include <stdio.h>

int add_three(int a, int b, int c);

int main(void) {
    int total;                 /* BUG IS HERE — can you find it with GDB before looking? */
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
