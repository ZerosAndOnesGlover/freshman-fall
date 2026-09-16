// ring.c — a character device: writes append to a circular buffer, reads take from it
// and sleep while it is empty. Registered in devsw[RING], so that open/read/write on an
// inode created with mknod("ring", RING, 0) reach this code.
// CS 202 Week 9, PS 9.

#include "types.h"
#include "defs.h"
#include "param.h"
#include "spinlock.h"
#include "sleeplock.h"
#include "fs.h"
#include "file.h"
#include "memlayout.h"
#include "mmu.h"
#include "proc.h"

#define RINGSIZE 512

struct {
  struct spinlock lock;
  char buf[RINGSIZE];
  uint r;                 // next byte to read
  uint w;                 // next byte to write
  int dropped;            // bytes discarded because the buffer was full
} ring;

void
ringinit(void)
{
  // TODO (Q2a): initialise the lock and register this device in devsw[RING].
}

// Read up to n bytes. Sleeps while the buffer is empty, like consoleread.
int
ringread(struct inode *ip, char *dst, int n)
{
  // TODO (Q2b): unlock the inode, take ring.lock, sleep while the buffer is empty,
  // copy out up to n bytes, release, relock the inode, and return the count.
  (void)ip; (void)dst; (void)n;
  return -1;
}

// Write n bytes, discarding any that do not fit, and wake a waiting reader.
int
ringwrite(struct inode *ip, char *src, int n)
{
  // TODO (Q2c): take ring.lock, append what fits, count what does not in ring.dropped,
  // wake any sleeping reader, and return how many bytes were stored.
  (void)ip; (void)src; (void)n;
  return -1;
}
