/* sgdt.c -- the Week 0 claim, re-run in Week 12.
   CS 202 Week 12, Lab 12 Part A, and L39 §3.
   Build: gcc -O2 -Wall -Wextra -o sgdt sgdt.c

   SGDT stores the Global Descriptor Table register -- a kernel address -- and
   it is not a privileged instruction on a CPU without UMIP.  This kernel is
   built with CONFIG_X86_UMIP=y.  Run it and see what that is worth. */
#include <stdio.h>

int main(void)
{
	unsigned char d[10];
	unsigned long base = 0;

	__asm__ volatile ("sgdt %0" : "=m"(d));
	for (int i = 9; i >= 2; i--)
		base = (base << 8) | d[i];
	printf("sgdt from user mode succeeded: GDT base %#lx limit %u\n",
	    base, d[0] | (d[1] << 8));
	return 0;
}
