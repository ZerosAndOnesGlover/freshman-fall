#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int scale(int *a, int n, int k);
int main(void){
    int n = 20000000; int *a = malloc(n*sizeof(int));
    for (int i=0;i<n;i++) a[i] = i & 1023;
    struct timespec t0,t1; long best = 1L<<62; int s=0;
    for (int r=0;r<5;r++){
        clock_gettime(CLOCK_MONOTONIC,&t0);
        s = scale(a,n,3);
        clock_gettime(CLOCK_MONOTONIC,&t1);
        long ns=(t1.tv_sec-t0.tv_sec)*1000000000L+(t1.tv_nsec-t0.tv_nsec);
        if(ns<best) best=ns;
    }
    printf("%ld ms  (checksum %d)\n", best/1000000, s);
    return 0;
}
