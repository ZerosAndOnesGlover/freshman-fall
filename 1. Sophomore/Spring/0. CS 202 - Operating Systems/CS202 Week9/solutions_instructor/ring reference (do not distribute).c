// ring.c — a character device: writes append to a circular buffer, reads take from it
// and sleep while it is empty. Registered in devsw[RING], so that open/read/write on an
// inode created with mknod("ring", RING, 0) reach this code.
// CS 202 Week 9, PS 9 reference.

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
  initlock(&ring.lock, "ring");
  devsw[RING].read = ringread;
  devsw[RING].write = ringwrite;
}

// Read up to n bytes. Sleeps while the buffer is empty, like consoleread.
int
ringread(struct inode *ip, char *dst, int n)
{
  int got = 0;

  iunlock(ip);
  acquire(&ring.lock);
  while(ring.r == ring.w){
    if(myproc()->killed){
      release(&ring.lock);
      ilock(ip);
      return -1;
    }
    sleep(&ring.r, &ring.lock);
  }
  while(got < n && ring.r != ring.w){
    dst[got++] = ring.buf[ring.r++ % RINGSIZE];
  }
  release(&ring.lock);
  ilock(ip);
  return got;
}

// Write n bytes, discarding any that do not fit, and wake a waiting reader.
int
ringwrite(struct inode *ip, char *src, int n)
{
  int i;

  iunlock(ip);
  acquire(&ring.lock);
  for(i = 0; i < n; i++){
    if(ring.w - ring.r >= RINGSIZE){
      ring.dropped += n - i;
      break;
    }
    ring.buf[ring.w++ % RINGSIZE] = src[i];
  }
  wakeup(&ring.r);
  release(&ring.lock);
  ilock(ip);
  return i;
}
