# PROG 201 · Systems Programming in C
## Week 7 · Lecture 1 of 3
### The VFS, and the POSIX Filesystem API

---

**Reading:** APUE Ch. 4 · TLPI Ch. 14–15 · `man 2 statfs`, `man 2 openat`, `man 7 path_resolution` · **Previous:** L21 · **Next:** L23 — inodes, directory entries and links

---

## 1. One API, Many Filesystems

Week 1 said `read` and `write` work on anything. This week is the machinery that makes that true.

`vfs.c` calls `statfs` on six paths:

```
  /                      ext2/3/4   block 4096  blocks 60984407  free 34000468  namelen 255
  /tmp                   ext2/3/4   block 4096  blocks 60984407  free 34000468  namelen 255
  /proc                  proc       block 4096  blocks 0         free 0         namelen 255
  /sys                   sysfs      block 4096  blocks 0         free 0         namelen 255
  /dev/shm               tmpfs      block 4096  blocks 984903    free 945955    namelen 255
  /dev/pts               devpts     block 4096  blocks 0         free 0         namelen 255
```

**Six different implementations, one struct.** Two of them (`proc`, `sysfs`) report **zero blocks**, because they have no storage at all — their files are generated when you read them. One (`tmpfs`) is RAM. One (`devpts`) is a directory of pseudo-terminals, which is where Week 6's `script -qc` sessions came from.

The **Virtual File System** is the kernel layer that makes those the same thing. A filesystem registers a set of function pointers — how to look up a name in a directory, how to read a block of a file, how to allocate an inode — and every system call above it is written once, against the interface. `read()` on `/proc/self/stat` and `read()` on `/etc/hostname` enter the same code, and diverge at one indirect call.

**And the abstraction leaks in a way worth seeing:**

```
  /etc/hostname          size 30    blocks 8    read 30 bytes: adebayo-glover-ThinkPad-T480s
  /proc/self/stat        size 0     blocks 0    read 40 bytes: 1112690 (vfs) R 1112679 ...
```

**`/proc/self/stat` has `st_size` = 0 and `read` returns forty bytes.** There is no file. `stat` on a `procfs` entry is a function that fills in a struct with zeros for the fields that have no meaning, and the content only exists while you are reading it. A program that trusts `st_size` to size a buffer works on `ext4` and silently reads nothing under `/proc` — which is why `read`-until-zero, not `st_size`, is the way to read a file you did not create.

---

## 2. The Four Objects Underneath

The VFS has four in-memory types, and every one of them is a cache of something:

| Object | Represents | Cached because |
| --- | --- | --- |
| **`inode`** | a file — its metadata and where its data is | reading it is a disk access |
| **`dentry`** | *this name in that directory maps to that inode* | path lookup would otherwise be a disk read per component |
| **`file`** | an open file description — offset, flags | this is Week 1's middle table |
| **`superblock`** | a mounted filesystem | one per mount |

**The `file` object is Week 1 L04's open file description**, and it is worth noticing that the diagram you drew in Week 1 was a picture of the VFS. Descriptor table → `file` → `dentry` → `inode`, with the last two being the part Week 1 drew as "the inode".

**The `dentry` cache is the one that matters for performance.** Resolving `/usr/lib/x86_64-linux-gnu/libc.so.6` means looking up five names, each in a directory, each of which without a cache would be a disk read. The dcache makes the second lookup of any path essentially free, and it is why `ls` of a directory you just listed is instant.

---

## 3. Path Resolution Is a Loop

`man 7 path_resolution` is four pages and describes an algorithm you can write down:

```
start at "/" (absolute) or the process's cwd (relative)
for each component:
    the current directory must be a directory and you must have +x on it
    look the component up in it -> an inode
    if that inode is a symlink, replace the component with the link target and restart
    (up to 40 times, then ELOOP)
```

Three consequences worth having:

**`x` on a directory means "may traverse", not "may execute".** A directory with `r` and no `x` can be listed but not entered — you can see the names and cannot `stat` them. It is the permission bit people get wrong most often.

**Symlinks are followed during resolution, not at the end.** So `/a/b/c` where `b` is a symlink resolves `b`'s target and continues — which is why PS 5's path-traversal check had to `realpath` rather than look for `..`.

**`ELOOP` after 40 links** is a limit, not a proof of a cycle. `ln -s a b; ln -s b a` gives `ELOOP`; so does a chain of 41 perfectly acyclic links.

### `openat` and why it exists

```c
int dirfd = open("/some/dir", O_RDONLY | O_DIRECTORY);
int fd    = openat(dirfd, "file.txt", O_RDONLY);
```

Every path-taking call has an `*at` variant: `openat`, `fstatat`, `unlinkat`, `renameat`, `linkat`, `mkdirat`. They exist for two reasons:

- **A race.** Between your `stat("/tmp/x")` and your `open("/tmp/x")`, somebody may replace `/tmp/x` with a symlink to `/etc/shadow`. A descriptor to the *directory* is a stable handle that no rename can invalidate, so `fstatat(dirfd, "x", ...)` and `openat(dirfd, "x", ...)` refer to the same directory even if the path to it changes. This is the TOCTTOU class from Week 1 L05 §5 and PS 5 Q3(a).
- **Threads.** There is one current directory per *process*, so `chdir` in a threaded program changes it for every thread. `openat` lets each thread carry its own "where I am" in a descriptor.

**`AT_FDCWD` as the `dirfd` means "relative to the current directory"**, which is how `openat` implements `open`.

---

## 4. The Calls, Grouped by What They Touch

You have used most of these. The grouping is the point:

**Names** — these change directory entries and never touch file data:

```c
link(old, new)        /* another name for the same inode      */
unlink(path)          /* remove a name; the file may survive  */
rename(old, new)      /* atomically replace one name          */
symlink(target, path) /* a new inode holding a string         */
mkdir / rmdir
```

**Metadata** — these change the inode:

```c
stat / fstat / lstat / fstatat
chmod / chown / utimensat
truncate / ftruncate
```

**Data** — Week 1, unchanged:

```c
open / read / write / lseek / close / pread / pwrite
```

**Directories** — a directory is a file you may not `read`:

```c
opendir / readdir / closedir      /* the portable way   */
getdents64                        /* what they call     */
```

**`read()` on a directory descriptor fails with `EISDIR`** on Linux, deliberately: directory format is filesystem-specific, so the kernel will not hand you the bytes. `readdir` gives you a name, an inode number and sometimes a type:

```
  /etc     .(ino 5505025, DIR)  ..(ino 2, DIR)  hosts(ino 5505418, REG)  subgid(ino 5507855, REG)
```

**`d_type` is `DT_UNKNOWN` on some filesystems**, and code that trusts it without a fallback to `lstat` breaks on exactly the filesystems that matter (older XFS, some network mounts). `readdir` also gives you **no order** — `.` and `..` happen to come first here, and nothing requires it.

---

## 5. `stat`, and What Is Actually In It

```c
struct stat {
    dev_t     st_dev;      /* which filesystem                */
    ino_t     st_ino;      /* which inode on it               */
    mode_t    st_mode;     /* type and permissions            */
    nlink_t   st_nlink;    /* how many names point here       */
    uid_t     st_uid;  gid_t st_gid;
    off_t     st_size;     /* bytes                           */
    blksize_t st_blksize;  /* the preferred I/O size          */
    blkcnt_t  st_blocks;   /* 512-byte units ACTUALLY used    */
    struct timespec st_atim, st_mtim, st_ctim;
};
```

Five things in there that people get wrong:

**`(st_dev, st_ino)` is the identity of a file**, not the path. Two paths naming the same file agree on both; `st_ino` alone does not, because inode numbers are only unique within a filesystem. Any program that de-duplicates files by inode number without the device is wrong across a mount point — and `find -samefile` and `rsync -H` both compare the pair.

**`st_size` and `st_blocks` disagree, in both directions.** A sparse file has more size than blocks (Week 1 L05 §4 measured 1.1 GB in 4 KB); a small file has more blocks than size, because a block is the unit. And `st_blocks` is **always in 512-byte units**, whatever the filesystem's block size — a 1 KiB block shows as 2.

**`st_ctim` is not creation time.** It is the *inode change* time — when the metadata last changed. `chmod` moves it and does not move `mtime`. Creation time exists on ext4 as `crtime` and POSIX has no call for it; Linux added `statx` with `STATX_BTIME` in 2017.

**`st_atime` is probably lying.** Every modern system mounts with `relatime` or `noatime` — **this machine's root is `noatime`** — because updating an access time on every read turns a read-only workload into a write workload. Code that uses `atime` for anything is code from before 2007.

**`st_mode` holds two things**: the type (`S_ISREG`, `S_ISDIR`, `S_ISLNK`, `S_ISFIFO`, `S_ISCHR`, `S_ISBLK`, `S_ISSOCK`) and twelve permission bits. `S_ISLNK` is only ever true through **`lstat`**, because `stat` follows the link — which is why `ls -l` uses `lstat` and `cat` uses `stat`.

---

## 6. Mounts, and Where the Tree Comes From

A filesystem is grafted onto the tree at a mount point, and from then on it is invisible in the path:

```
$ df -T .
/dev/nvme0n1p2 ext4 243937628 107911140 123562312  47% /
```

**Crossing a mount point is the one thing path resolution does that is not a lookup.** The dentry for a mount point holds a pointer to the mounted filesystem's root, and traversal follows it. Two consequences:

- **`..` from a filesystem's root goes to the parent of the mount point**, in the other filesystem. Resolution handles it; the on-disk `..` entry cannot, because it does not know where it was mounted.
- **`rename` cannot cross a filesystem**, and fails with `EXDEV`. `mv` between filesystems is therefore a copy and an unlink, done in userspace, which is why it is slow and why it is not atomic.

**Bind mounts** graft a subtree somewhere else, and **overlay mounts** stack two directories with copy-on-write — which is what every container image is (Week 11).

---

## Summary

- The **VFS** is one interface over many implementations: six filesystem types answered one `statfs`, two of them with **zero blocks** because they have no storage.
- **`/proc/self/stat` has `st_size` = 0 and reads 40 bytes.** Read until zero; do not trust `st_size` on a file you did not create.
- Four cached objects: **`inode`, `dentry`, `file`, `superblock`** — and the `file` object is Week 1's open file description.
- **Path resolution is a loop** with a permission check per component. `x` on a directory means *traverse*; symlinks are followed mid-path; `ELOOP` after 40.
- **`openat` and friends exist** to close a TOCTTOU race and to give threads a per-thread "where I am".
- The calls divide into **names, metadata, data and directories**. A directory cannot be `read`; `readdir` gives no order and `d_type` may be `DT_UNKNOWN`.
- **`(st_dev, st_ino)` identifies a file.** `st_blocks` is always 512-byte units. **`st_ctim` is not creation time**, and `st_atime` is disabled on this machine (`noatime`).
- `rename` across filesystems fails with **`EXDEV`**, which is why `mv` between disks is a copy.

---

## Exercises

1. `statfs` every mount point on your machine (`/proc/self/mounts` lists them). How many distinct `f_type` values are there, and which report zero blocks?
2. Read `/proc/self/maps` with a buffer sized from `st_size`. What do you get? Now fix it and say what the rule is.
3. Make a directory `chmod 600` and try to `stat` a file inside it, then `chmod 500` and list it. Which bit does which?
4. Build a symlink chain 39 links long, then 41. Where exactly does `ELOOP` appear, and does the number depend on the filesystem?
5. Write the TOCTTOU race in §3 as two programs — one that opens `/tmp/x` by path, one that swaps it for a symlink in a loop — and then close it with `openat`. How often did it hit?
6. `stat` and `lstat` the same symlink and print `st_size`, `st_mode` and `st_ino` for both. Explain all three differences.
7. `mv` a large file within one filesystem and across two, with `strace`. How many system calls each, and which `errno` started the difference?

---

*PROG 201 · Week 7 · L22 · © CSE Department*
