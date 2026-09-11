// fpu.c: two processes each add 0.5 to a double, 20 million times, and check
// the answer forty times along the way.
//
// Copy into xv6, add _fpu to UPROGS, and boot with ONE CPU:
//   make qemu-nox CPUS=1
//   $ fpu
//
// CS 202 Week 1: L05 §6, Lab 1 Part E, PS 1 Q4.
#include "types.h"
#include "user.h"

static void
work(char *who)
{
  double x = 0.0;
  int i, j, bad = 0;
  for(j = 0; j < 40; j++){
    for(i = 0; i < 500000; i++)
      x = x + 0.5;
    if(x != 0.5 * 500000 * (j + 1))
      bad++;
  }
  printf(1, "%s: %d of 40 checkpoints wrong, final x*2 = %d (expected 20000000)\n", who, bad, (int)(x * 2));
}

int
main(void)
{
  if(fork() == 0){
    work("child ");
    exit();
  }
  work("parent");
  wait();
  exit();
}
