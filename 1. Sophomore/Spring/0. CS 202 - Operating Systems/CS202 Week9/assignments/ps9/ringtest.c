#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"

// ringtest.c — exercise the ring character device: a child writes, the parent reads,
// and the reader blocks until data arrives.
// CS 202 Week 9, PS 9 reference.
#define RING 2

int
main(int argc, char *argv[])
{
  int fd, i, n, total = 0, last = 0;
  char buf[64];
  int rounds = argc > 1 ? atoi(argv[1]) : 200;

  unlink("ring");
  if(mknod("ring", RING, 0) < 0){
    printf(1, "mknod failed\n");
    exit();
  }

  if(fork() == 0){
    sleep(20);                       // let the parent block in read() first
    fd = open("ring", O_WRONLY);
    for(i = 0; i < rounds; i++){
      buf[0] = 'a' + (i % 26);
      if(write(fd, buf, 1) != 1){
        printf(1, "write failed at %d\n", i);
        break;
      }
    }
    close(fd);
    exit();
  }

  fd = open("ring", O_RDONLY);
  printf(1, "parent: reading (this blocks until the child writes)\n");
  while(total < rounds){
    n = read(fd, buf, sizeof(buf));
    if(n <= 0)
      break;
    total += n;
    last = buf[n - 1];
  }
  printf(1, "parent: read %d bytes of %d; the last byte was '%c', which is byte %d\n",
         total, rounds, last, rounds - 1);
  close(fd);
  wait();
  exit();
}
