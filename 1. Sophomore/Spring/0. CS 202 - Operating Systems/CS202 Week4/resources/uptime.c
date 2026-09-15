// uptime.c: ask the kernel for the tick count. CS 202 Week 4, L13 §7.
//
// Copy into xv6 and add _uptime to UPROGS. On its own it prints the tick count.
// L13 §7 first adds a second acquire(&tickslock) to sys_uptime in sysproc.c.
#include "types.h"
#include "user.h"

int
main(void)
{
  printf(1, "uptime: asking the kernel for the tick count\n");
  printf(1, "uptime: %d\n", uptime());
  exit();
}
