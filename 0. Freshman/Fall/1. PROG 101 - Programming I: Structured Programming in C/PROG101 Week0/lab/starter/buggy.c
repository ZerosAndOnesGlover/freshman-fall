/* buggy.c — Intentionally Buggy Program for GDB Lab
 * PROG 101: Programming I — Structured Programming in C
 *
 * This program has an intentional bug.
 * Your job: find it using GDB.
 *
 * Compile with:
 *   gcc -Wall -g -std=c11 -o buggy buggy.c
 * Then:
 *   gdb ./buggy
 */

#include <stdio.h>

/* Function prototype */
int sum_array(int arr[], int n);

int main(void) {
    int numbers[] = {10, 20, 30, 40, 50};

    /* BUG IS HERE — can you find it with GDB before looking? */
    int total = sum_array(numbers, 6);

    printf("Sum of array: %d\n", total);
    printf("Expected sum: %d\n", 10 + 20 + 30 + 40 + 50);
    return 0;
}

int sum_array(int arr[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return sum;
}
