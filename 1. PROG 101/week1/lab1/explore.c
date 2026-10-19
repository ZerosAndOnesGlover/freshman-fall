/* explore.c — PROG 101 Lab 1: look at values in GDB */
#include <stdio.h>

int global_counter = 7;

int main(void) {
    signed char   sc  = -42;
    unsigned char uc  = 214;
    short         s   = -1;
    int           i   = 0x12345678;
    int           neg = -2;
    unsigned int  u   = 4294967294u;
    float         f   = 1.0f;
    float         tenth = 0.1f;
    double        d   = 0.1;
    long long     big = 1LL + 2147483647;

    printf("sc=%d uc=%d s=%d i=%d neg=%d u=%u f=%f tenth=%.10f d=%.20f big=%lld\n",
           sc, uc, s, i, neg, u, f, tenth, d, big);
    return 0;
}
