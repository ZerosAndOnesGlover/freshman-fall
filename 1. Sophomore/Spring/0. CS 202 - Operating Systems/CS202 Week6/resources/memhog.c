#include "types.h"
#include "stat.h"
#include "user.h"

// memhog.c — grow with sbrk until xv6 refuses, then try to fork. Needs the nfree()
// system call from Week 5's resources/nfree.patch.
//   git apply nfree.patch; add _memhog to UPROGS; make qemu-nox; then: memhog
// CS 202 Week 6, L19 §1.

// memhog.c — grow with sbrk until xv6 refuses, then try to fork.
int
main(int argc, char *argv[])
{
  int pages = 0, pid;
  char *p;

  printf(1, "free pages at start: %d\n", nfree());
  while((p = sbrk(4096)) != (char*)-1){
    p[0] = 1;
    pages++;
  }
  printf(1, "sbrk refused after %d pages; free pages now %d\n", pages, nfree());
  pid = fork();
  printf(1, "fork returned %d\n", pid);
  if(pid == 0)
    exit();
  if(pid > 0)
    wait();
  sbrk(-pages * 4096);
  printf(1, "gave it back: free pages %d\n", nfree());
  exit();
}
