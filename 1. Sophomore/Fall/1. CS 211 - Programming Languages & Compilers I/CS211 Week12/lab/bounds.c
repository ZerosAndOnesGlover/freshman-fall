// CS 211 Week 12, Lab 12 Part A.  One question, four answers.
//
// Every language in this folder is asked the same thing: read past the end
// of an array. The four answers are the safety axis of L25, measured.
//
//   gcc -O2 -o bounds_c bounds.c && ./bounds_c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int a[4] = {10, 20, 30, 40};
    int idx = 7;                       // deliberately out of range

    printf("; ---- C ----\n");
    printf("  a[3] = %d\n", a[3]);
    // Undefined behaviour. Not "returns garbage" -- the standard imposes
    // NO requirement on this program at all, which is Week 9's point about
    // data races arriving in a different disguise.
    printf("  a[7] = %d   <- undefined behaviour, no diagnostic\n", a[idx]);
    printf("  (the program continued)\n");
    return 0;
}
