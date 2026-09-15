#include "types.h"
#include "stat.h"
#include "user.h"
#include "mmu.h"

// pgfault.c — write one byte where this process has no business writing, and see
// what xv6's trap handler does about it.
//   add _pgfault to UPROGS, make qemu-nox, then:  pgfault past | guard | kernel | text
// CS 202 Week 5, L18 §2.
int
main(int argc, char *argv[])
{
  char *p;
  uint sz = (uint)sbrk(0);

  if(argc < 2){
    printf(1, "usage: pgfault past|guard|kernel|text\n");
    exit();
  }
  if(argv[1][0] == 'p')
    p = (char*)sz;                              // the first byte past the process's memory
  else if(argv[1][0] == 'g')
    p = (char*)(PGROUNDDOWN((uint)&p) - 1);     // the last byte of the guard page below the stack
  else if(argv[1][0] == 'k')
    p = (char*)0x80100000;                      // the kernel's text
  else
    p = (char*)main;                            // this program's own code
  printf(1, "size 0x%x; writing to 0x%x\n", sz, (uint)p);
  *p = 1;
  printf(1, "wrote it\n");
  exit();
}
