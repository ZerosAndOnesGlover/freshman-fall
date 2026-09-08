/* One API, many filesystems.  The VFS, seen from userspace. */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <dirent.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/statfs.h>
#include <sys/vfs.h>

static const char *fsname(long t)
{
    switch (t) {
    case 0xEF53:     return "ext2/3/4";
    case 0x01021994: return "tmpfs";
    case 0x9FA0:     return "proc";
    case 0x62656572: return "sysfs";
    case 0x1CD1:     return "devpts";
    case 0x6969:     return "nfs";
    case 0x9123683E: return "btrfs";
    case 0x58465342: return "xfs";
    case 0x27E0EB:   return "cgroup";
    case 0x63677270: return "cgroup2";
    default:         return "?";
    }
}

static void probe(const char *path)
{
    struct statfs s;
    if (statfs(path, &s) < 0) { printf("  %-22s %s\n", path, strerror(errno)); return; }
    printf("  %-22s %-10s block %-6ld  blocks %-12llu free %-12llu  namelen %ld\n",
           path, fsname((long) s.f_type), (long) s.f_bsize,
           (unsigned long long) s.f_blocks, (unsigned long long) s.f_bfree,
           (long) s.f_namelen);
}

static void readdir_demo(const char *path)
{
    DIR *d = opendir(path);
    if (!d) { printf("  %s: %s\n", path, strerror(errno)); return; }
    struct dirent *e;
    int n = 0;
    printf("  %-22s ", path);
    while ((e = readdir(d)) && n < 4) {
        const char *t = e->d_type == DT_DIR ? "DIR" : e->d_type == DT_REG ? "REG" :
                        e->d_type == DT_LNK ? "LNK" : e->d_type == DT_UNKNOWN ? "UNKNOWN" : "other";
        printf("%s(ino %llu, %s)  ", e->d_name, (unsigned long long) e->d_ino, t);
        n++;
    }
    printf("\n");
    closedir(d);
}

int main(void)
{
    printf("statfs: the same struct for every filesystem\n");
    probe("/");
    probe("/tmp");
    probe("/proc");
    probe("/sys");
    probe("/dev/shm");
    probe("/dev/pts");

    printf("\nopen/read/stat work on all of them:\n");
    struct stat st;
    const char *paths[] = { "/etc/hostname", "/proc/self/stat", "/sys/kernel/ostype" };
    for (unsigned i = 0; i < 3; i++) {
        if (stat(paths[i], &st) == 0)
            printf("  %-22s size %-8lld blocks %-6lld  (st_size is a lie for one of these)\n",
                   paths[i], (long long) st.st_size, (long long) st.st_blocks);
    }
    for (unsigned i = 0; i < 3; i++) {
        int fd = open(paths[i], O_RDONLY);
        char b[128]; ssize_t n = read(fd, b, 40);
        if (n > 0) { b[n] = 0; for (char *p = b; *p; p++) if (*p == '\n') *p = ' ';
                     printf("  %-22s read %2zd bytes: %.40s\n", paths[i], n, b); }
        close(fd);
    }

    printf("\nreaddir gives a name, an inode number, and sometimes a type:\n");
    readdir_demo("/etc");
    readdir_demo("/proc");
    return 0;
}
