/* A name is not a file.  An inode is a file. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

static void show(const char *path)
{
    struct stat st;
    if (lstat(path, &st) < 0) { printf("  %-12s %s\n", path, strerror(errno)); return; }
    char kind = S_ISLNK(st.st_mode) ? 'l' : S_ISDIR(st.st_mode) ? 'd' : '-';
    printf("  %-12s %c inode %-9llu links %-3lu size %-7lld",
           path, kind, (unsigned long long) st.st_ino,
           (unsigned long) st.st_nlink, (long long) st.st_size);
    if (S_ISLNK(st.st_mode)) {
        char buf[256]; ssize_t n = readlink(path, buf, sizeof buf - 1);
        if (n > 0) { buf[n] = 0; printf("  -> %s", buf); }
        struct stat t;
        if (stat(path, &t) < 0) printf("   (DANGLING)");
    }
    printf("\n");
}

int main(void)
{
    unlink("a.txt"); unlink("b.txt"); unlink("s.txt"); unlink("gone.txt");

    int fd = open("a.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (write(fd, "the data\n", 9) != 9) return 1;
    close(fd);

    if (link("a.txt", "b.txt") < 0) perror("link");        /* hard link */
    if (symlink("a.txt", "s.txt") < 0) perror("symlink");  /* soft link */

    printf("1. one file, three names:\n");
    show("a.txt"); show("b.txt"); show("s.txt");

    printf("\n2. remove the ORIGINAL name:\n");
    unlink("a.txt");
    show("a.txt"); show("b.txt"); show("s.txt");
    printf("   the hard link still has the data; the symlink points at nothing.\n");

    printf("\n3. the data is still there, through the other name:\n");
    fd = open("b.txt", O_RDONLY);
    char buf[32]; ssize_t n = read(fd, buf, sizeof buf - 1);
    if (n > 0) { buf[n] = 0; printf("   cat b.txt -> %s", buf); }
    close(fd);

    printf("\n4. open, then unlink the last name:\n");
    fd = open("b.txt", O_RDONLY);
    unlink("b.txt");
    show("b.txt");
    n = pread(fd, buf, sizeof buf - 1, 0);
    if (n > 0) { buf[n] = 0; printf("   still readable through the descriptor: %s", buf); }
    printf("   /proc/self/fd/%d -> ", fd);
    fflush(stdout);
    char lbuf[256]; ssize_t k = readlink("/proc/self/fd/3", lbuf, sizeof lbuf - 1);
    if (k > 0) { lbuf[k] = 0; printf("%s\n", lbuf); }
    close(fd);                                    /* NOW the blocks are freed */

    printf("\n5. what you may and may not hard-link:\n");
    errno = 0;
    printf("   link to a directory : %s\n",
           link(".", "dirlink") < 0 ? strerror(errno) : "allowed"); 
    errno = 0;
    printf("   symlink to a directory: %s\n",
           symlink(".", "dirsym") < 0 ? strerror(errno) : "allowed");
    unlink("dirsym"); unlink("dirlink");
    unlink("s.txt");
    return 0;
}
