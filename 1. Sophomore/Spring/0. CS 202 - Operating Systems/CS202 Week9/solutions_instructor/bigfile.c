#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"

// bigfile.c — how large a file xv6 can hold once bmap has a double indirect block.
// CS 202 Project 2 Part B reference.
int
main(void)
{
  char buf[512];
  int fd, i, n, blocks = 0;

  memset(buf, 'z', sizeof(buf));
  unlink("big");
  fd = open("big", O_CREATE | O_RDWR);
  if(fd < 0){ printf(1, "open failed\n"); exit(); }
  for(i = 0; ; i++){
    n = write(fd, buf, sizeof(buf));
    if(n != sizeof(buf))
      break;
    blocks++;
    if(blocks % 2000 == 0)
      printf(1, "  %d blocks\n", blocks);
  }
  printf(1, "wrote %d blocks = %d bytes, then write returned %d\n", blocks, blocks * 512, n);
  close(fd);
  fd = open("big", O_RDONLY);
  for(i = 0; i < blocks; i++){
    if(read(fd, buf, sizeof(buf)) != sizeof(buf) || buf[0] != 'z'){
      printf(1, "read back wrong at block %d\n", i);
      break;
    }
  }
  printf(1, "read %d blocks back correctly\n", i);
  close(fd);
  unlink("big");
  exit();
}
