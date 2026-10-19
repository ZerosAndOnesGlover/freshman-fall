/* hello.c — PROG 101, Week 0, Problem Set 0 (Problem 1)
 * Started from the Lab 0 hello.c; GREETING added for Problem 1.4.
 *
 *   gcc -Wall -Wextra -Werror -std=c11 -o hello hello.c
 */

#include <stdio.h>

#define GREETING "Hello, world"

int main(void) {
    printf("%s!\n", GREETING);
    printf("I am a C programmer.\n");
    return 0;
}
