/* buggy.c — Intentionally Buggy Program for GDB Lab
 * PROG 101: Programming I — Structured Programming in C
 *
 * This program had one intentional bug: a variable is read before it is
 * given a value (Lecture 03, "Common Beginner Errors").
 *
 * BUG (found and fixed, Lab 0 Part 6):
 *   `int total;` was declared without a value, so line 24 of the starter,
 *   `total = total + add_three(a, b, c);`, read garbage.
 *   - gcc -Wall reported: 'total' is used uninitialized [-Wuninitialized]
 *   - GDB (break 24, print total) showed total = 32767 before the line ran,
 *     so Total printed 32827 instead of 60. Outside GDB the value changed
 *     from run to run (32824, 32825, 32826): it is whatever was left on the
 *     stack by code that ran before main.
 * FIX: initialise it - `int total = 0;`. Output is now 60 and -Wall is clean.
 * Also added `d` so the expected value is computed from a, b and c instead
 * of repeating the literals 10 + 20 + 30.
 *
 * Compile with:
 *   gcc -Wall -g -std=c11 -o buggy buggy.c
 * Then:
 *   gdb ./buggy
 */

#include <stdio.h>

int add_three(int a, int b, int c);

int main(void) {
    int total = 0;             /* FIX: was uninitialised, so it started as garbage */
    int a = 10;
    int b = 20;
    int c = 30;
    int d = a + b + c;

    total = total + add_three(a, b, c);

    printf("Total:    %d\n", total);
    printf("Expected: %d\n", d);
    return 0;
}

int add_three(int a, int b, int c) {
    return a + b + c;
}
