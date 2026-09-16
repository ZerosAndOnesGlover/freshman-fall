#include "types.h"
#include "stat.h"
#include "user.h"

// lazytest.c — sbrk should cost nothing until the pages are touched.
// CS 202 Project 2 Part A reference.
int
main(void)
{
  int before, after_sbrk, after_touch, i;
  char *p;

  before = nfree();
  p = sbrk(4 * 1024 * 1024);
  after_sbrk = nfree();
  for(i = 0; i < 16; i++)
    p[i * 4096] = 1;
  after_touch = nfree();
  printf(1, "free %d -> %d after sbrk(4 MB) (%d pages), -> %d after touching 16 pages (%d pages)\n",
         before, after_sbrk, before - after_sbrk, after_touch, after_sbrk - after_touch);
  printf(1, "reading an untouched page inside the region gives %d\n", p[1023 * 4096]);
  exit();
}
