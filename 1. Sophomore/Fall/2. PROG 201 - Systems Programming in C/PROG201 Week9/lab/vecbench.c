#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}
#define KEEP(x) __asm__ volatile("" :: "r,m"(x) : "memory")
int sumi(const int *a, long n){ int s=0; for(long i=0;i<n;i++) s+=a[i]; return s; }
int main(int argc, char **argv){
    long n = argc>1 ? atol(argv[1]) : (16L<<20);      /* default 64 MiB of int */
    int *a = aligned_alloc(64, n*sizeof *a);
    for(long i=0;i<n;i++) a[i]=1;
    double best=1e9;
    for(int r=0;r<7;r++){ double t0=now(); int s=sumi(a,n); double d=now()-t0; KEEP(s); if(d<best) best=d; }
    printf("%8ld ints (%5ld KiB): %8.3f ms  %8.2f GB/s\n", n, n*4/1024, best*1000, n*4.0/best/1e9);
    free(a); return 0;
}
