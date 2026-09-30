/* hello.c — Week 0, Lab 0 (PS 0, Problem 1.4: greeting moved into a macro) */
#include <stdio.h>

#define GREETING "Hello, world"

int main(void) {
    printf(GREETING "!\n");
    printf("I am a C programmer.\n");
    return 0;
}
