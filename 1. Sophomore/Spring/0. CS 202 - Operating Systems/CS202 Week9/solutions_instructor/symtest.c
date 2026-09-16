#include "types.h"
#include "stat.h"
#include "user.h"
#include "fcntl.h"

// symtest.c — symbolic links: following one, not following one, and a loop.
// CS 202 Project 2 Part C reference.
int
main(void)
{
  int fd, n, r;
  char buf[64];
  struct stat st;

  unlink("a"); unlink("b"); unlink("l1"); unlink("l2");

  fd = open("a", O_CREATE | O_RDWR);
  printf(1, "open(a, O_CREATE) = %d\n", fd);
  write(fd, "hello through a link\n", 21);
  close(fd);

  r = symlink("a", "b");
  printf(1, "symlink(a, b) = %d\n", r);

  fd = open("b", O_RDONLY | O_NOFOLLOW);
  printf(1, "open(b, O_NOFOLLOW) = %d\n", fd);
  if(fd >= 0){
    if(fstat(fd, &st) == 0)
      printf(1, "  the link inode: type %d, size %d\n", st.type, st.size);
    n = read(fd, buf, sizeof(buf) - 1);
    buf[n > 0 ? n : 0] = 0;
    printf(1, "  it contains %d bytes: \"%s\"\n", n, buf);
    close(fd);
  }

  fd = open("b", O_RDONLY);
  printf(1, "open(b) following the link = %d\n", fd);
  if(fd >= 0){
    n = read(fd, buf, sizeof(buf) - 1);
    buf[n > 0 ? n : 0] = 0;
    printf(1, "  read %d bytes: %s", n, buf);
    close(fd);
  }

  symlink("l2", "l1");
  symlink("l1", "l2");
  fd = open("l1", O_RDONLY);
  printf(1, "open of a symlink loop = %d (should be -1)\n", fd);

  unlink("a"); unlink("b"); unlink("l1"); unlink("l2");
  exit();
}
