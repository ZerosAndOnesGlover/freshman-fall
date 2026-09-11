/* xsave.c: how much register state does this CPU have beyond the 16 GPRs? */
#include <cpuid.h>
#include <stdio.h>
#include <sys/auxv.h>
int main(void)
{
    unsigned a, b, c, d;
    __cpuid_count(0xD, 0, a, b, c, d);
    printf("XSAVE area: %u bytes for the features enabled in XCR0, %u bytes if all supported were enabled\n", b, c);
    printf("XCR0-supported feature bits (EDX:EAX) = 0x%08x%08x\n", d, a);
    __cpuid_count(0xD, 1, a, b, c, d);
    printf("CPUID(0xD,1).EAX = 0x%x  (bit0 XSAVEOPT, bit1 XSAVEC, bit3 XSAVES)\n", a);
    printf("AT_MINSIGSTKSZ = %lu\n", getauxval(AT_MINSIGSTKSZ));
    return 0;
}
