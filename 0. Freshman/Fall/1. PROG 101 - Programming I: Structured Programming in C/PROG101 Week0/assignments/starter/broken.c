/* broken.c — Problem Set 0, Problem 4
 * PROG 101: Programming I — Structured Programming in C
 *
 * This file contains exactly 10 deliberate errors.
 * DO NOT fix anything here.
 * 
 * Your task:
 *   1. Identify all 10 errors in error_log.md
 *   2. Create fixed.c with all errors corrected
 *
 * Categories of errors you may find:
 *   - Preprocessor errors
 *   - Compiler errors  
 *   - Linker errors
 *   - Logic errors
 *   - Undefined behavior
 */

#include <stdio.h
#include <stdlib.h>

#define MAX_SIZE 10
#define SQUARE(x) x * x

int compute_sum(int arr, int n);

int main(void) {
    int numbers[MAX_SIZE] = {1, 2, 3, 4, 5};
    int total = compute_sum(numbers, 5)
    double pi = 3.14159;

    printf("Sum: %d\n" total);
    printf("Pi: %d\n", pi);
    printf("Square of 3+1: %d\n", SQUARE(3+1));

    int *ptr = malloc(sizeof(int) * 5);
    free(ptr);
    free(ptr);

    return;
}

int compute_sum(int *arr, int n) {
    int sum = 0
    for (int i = 0; i <= n; i++) {
        sum += arr[i];
    }
    return sum;
}
