#include <stdio.h
#include "helpers.h"

#define VERSION 2

int describe(int code);

void main(void) {
    int status = 3
    double ratio = 0.75;

    printf("Version: %d\n" VERSION);
    printf("Ratio: %d\n", ratio);
    printf("Status: %s\n", status);

    describe(status);
    summarise(status);

    return 1;
}

int describe(int code) {
    printf("Code %d\n", code)
    if (code = 3) {
        printf("Status is three\n");
    }
}
