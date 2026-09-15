#include "types.h"
#include "stat.h"
#include "user.h"

// memx.c — count the physical pages xv6 spends on sbrk and fork, using the nfree()
// system call added by nfree.patch.
//   git apply nfree.patch; add _memx to UPROGS; make qemu-nox; then: memx
// CS 202 Week 5, L16 §5.

int
main(int argc, char *argv[])
{
  int a, b, c, d, pid;
  char *p;

  a = nfree();
  printf(1, "size %d, free pages at start: %d\n", (int)sbrk(0), a);
  p = sbrk(4096);
  b = nfree();
  printf(1, "sbrk(4096): %d fewer, size %d\n", a - b, (int)sbrk(0));
  p[0] = 1;
  sbrk(4*1024*1024);
  c = nfree();
  printf(1, "sbrk(4 MB) more: %d fewer, size %d\n", b - c, (int)sbrk(0));
  pid = fork();
  if(pid == 0){
    d = nfree();
    printf(1, "in child after fork: %d fewer than parent before fork\n", c - d);
    exit();
  }
  wait();
  printf(1, "after child exits: %d (parent had %d)\n", nfree(), c);
  exit();
}
