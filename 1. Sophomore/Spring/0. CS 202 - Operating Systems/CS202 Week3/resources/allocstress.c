// allocstress.c: four processes grow their memory by eight pages, fill every
// byte with their own mark, check it, and give the pages back -- 1,000 times.
// If the kernel ever hands the same physical page to two processes at once,
// one of them finds another's mark in its memory.
#include "types.h"
#include "user.h"

#define PAGES 8
#define ITER  1000

static void
child(int k)
{
  char mark = 'A' + k;          // not 0 (fresh pages) and not 1 (kfree's junk)
  int i, j;
  for(i = 0; i < ITER; i++){
    char *p = sbrk(PAGES * 4096);
    if(p == (char*)-1){
      printf(1, "child %d: sbrk failed at iteration %d\n", k, i);
      exit();
    }
    for(j = 0; j < PAGES * 4096; j++)
      p[j] = mark;
    for(j = 0; j < PAGES * 4096; j++)
      if(p[j] != mark){
        printf(1, "child %d: CORRUPTION at iteration %d, byte %d: found %d, wrote %d\n", k, i, j, p[j], mark);
        exit();
      }
    sbrk(-PAGES * 4096);
  }
  printf(1, "child %d: %d iterations clean\n", k, ITER);
  exit();
}

int
main(void)
{
  int k;
  for(k = 0; k < 4; k++)
    if(fork() == 0)
      child(k);
  for(k = 0; k < 4; k++)
    wait();
  printf(1, "allocstress done\n");
  exit();
}
