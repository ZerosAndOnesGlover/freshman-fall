// spin.c: burn CPU forever, so that procdump has something running.
//
// Copy into xv6, add _spin to UPROGS, run `spin &` at the shell, then press
// Ctrl-P for a process listing.
//
// CS 202 Week 1: L04 §3, Lab 1 Part E.
#include "types.h"
#include "user.h"

int
main(void)
{
  volatile unsigned int x = 0;
  for(;;)
    x++;
}
