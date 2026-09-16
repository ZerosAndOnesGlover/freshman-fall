#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"

// bigf.c — how large a file xv6 can hold, and what happens at the limit.
// CS 202 Week 7, L22.
int
main(void)
{
  char buf[512];
  int fd, i, n, total = 0, blocks = 0;

  memset(buf, 'x', sizeof(buf));
  fd = open("big.txt", O_CREATE | O_RDWR);
  if(fd < 0){ printf(1, "open failed\n"); exit(); }
  for(i = 0; ; i++){
    n = write(fd, buf, sizeof(buf));
    if(n != sizeof(buf))
      break;
    total += n;
    blocks++;
  }
  printf(1, "wrote %d bytes = %d blocks, then write returned %d\n", total, blocks, n);
  close(fd);
  unlink("big.txt");
  exit();
}
