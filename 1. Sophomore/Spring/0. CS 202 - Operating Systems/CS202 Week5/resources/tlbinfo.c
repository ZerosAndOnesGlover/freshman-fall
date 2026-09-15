/* tlbinfo.c — the TLB descriptor bytes from cpuid leaf 2. Decode them with the
 * Intel SDM, Vol. 2A, Table 3-12.
 *   gcc -O2 -Wall -Wextra -o tlbinfo tlbinfo.c && ./tlbinfo
 * CS 202 Week 5, L17 §2. */
#include <stdio.h>
#include <cpuid.h>
int main(void)
{
    unsigned a, b, c, d;
    __cpuid(2, a, b, c, d);
    unsigned r[4] = { a, b, c, d };
    printf("cpuid leaf 2 descriptor bytes:");
    for (int i = 0; i < 4; i++) {
        if (r[i] & 0x80000000u) continue;
        for (int k = (i == 0 ? 1 : 0); k < 4; k++) { unsigned x = r[i] >> (8 * k) & 0xff; if (x) printf(" %02x", x); }
    }
    printf("\n");
    return 0;
}
