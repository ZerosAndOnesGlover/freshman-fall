/* myfs reference — a small Unix-like file system on an image file, in the shape of
 * xv6's: a superblock, an inode table, a free-block bitmap, and data blocks reached
 * through twelve direct addresses and one indirect block.
 *   gcc -O2 -Wall -Wextra -o myfs myfs.c
 *   ./myfs IMAGE COMMAND [ARGS]        (the image is created by `format`)
 *
 * Commands:
 *   format [BLOCKS]        make a new file system (default 2048 blocks of 512 bytes)
 *   mkdir PATH             create a directory
 *   create PATH            create an empty file
 *   write PATH SIZE BYTE   replace PATH's contents with SIZE copies of BYTE (hex)
 *   append PATH SIZE BYTE  add SIZE copies of BYTE to the end
 *   read PATH OFF LEN      print LEN bytes from offset OFF as a summary of runs
 *   ls PATH                list a directory
 *   stat PATH              inode number, type, links, size, blocks
 *   link OLD NEW           a second name for one file
 *   rm PATH                remove a name, and the file if it was the last
 *   df                     blocks and inodes in use
 *   dump                   the layout, and the first blocks of the bitmap
 *   fsck                   check the bitmap against what the inodes reach
 * CS 202 Week 7, PS 7. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define BSIZE     512
#define NDIRECT   12
#define NINDIRECT (BSIZE / sizeof(uint32_t))
#define MAXFILE   (NDIRECT + NINDIRECT)
#define DIRSIZ    14
#define ROOTINO   1
#define MAGIC     0x4d594653u                 /* "MYFS" */

#define T_FREE 0
#define T_DIR  1
#define T_FILE 2

struct superblock {
    uint32_t magic;
    uint32_t size;                            /* blocks in the image */
    uint32_t ninodes;
    uint32_t inodestart;
    uint32_t bmapstart;
    uint32_t datastart;
};

struct dinode {
    uint16_t type;
    uint16_t nlink;
    uint32_t size;
    uint32_t addrs[NDIRECT + 1];
};

struct dirent {
    uint16_t inum;
    char name[DIRSIZ];
};

#define IPB (BSIZE / sizeof(struct dinode))
#define BPB (BSIZE * 8)

/* ---------------------------------------------------------------- provided: the image */

static FILE *img;
static struct superblock sb;

static void die(const char *msg)
{
    fprintf(stderr, "myfs: %s\n", msg);
    exit(1);
}

static void bread(uint32_t b, void *buf)
{
    if (fseek(img, (long)b * BSIZE, SEEK_SET) || fread(buf, BSIZE, 1, img) != 1) die("read failed");
}

static void bwrite(uint32_t b, const void *buf)
{
    if (fseek(img, (long)b * BSIZE, SEEK_SET) || fwrite(buf, BSIZE, 1, img) != 1) die("write failed");
}

static void iread(uint32_t inum, struct dinode *ip)
{
    char blk[BSIZE];
    if (inum == 0 || inum >= sb.ninodes) die("bad inode number");
    bread(sb.inodestart + inum / IPB, blk);
    memcpy(ip, blk + (inum % IPB) * sizeof *ip, sizeof *ip);
}

static void iwrite(uint32_t inum, const struct dinode *ip)
{
    char blk[BSIZE];
    if (inum == 0 || inum >= sb.ninodes) die("bad inode number");
    bread(sb.inodestart + inum / IPB, blk);
    memcpy(blk + (inum % IPB) * sizeof *ip, ip, sizeof *ip);
    bwrite(sb.inodestart + inum / IPB, blk);
}

/* ---------------------------------------------------------------- Q1: blocks and inodes */

/* Find a free data block in the bitmap, mark it used, zero it, and return its number. */
static uint32_t balloc(void)
{
    char blk[BSIZE];
    for (uint32_t b = 0; b < sb.size; b += BPB) {
        bread(sb.bmapstart + b / BPB, blk);
        for (uint32_t bi = 0; bi < BPB && b + bi < sb.size; bi++) {
            int m = 1 << (bi % 8);
            if (!(blk[bi / 8] & m)) {
                blk[bi / 8] |= m;
                bwrite(sb.bmapstart + b / BPB, blk);
                char zero[BSIZE] = { 0 };
                bwrite(b + bi, zero);
                return b + bi;
            }
        }
    }
    die("out of blocks");
    return 0;
}

/* Mark block B free. */
static void bfree(uint32_t b)
{
    char blk[BSIZE];
    bread(sb.bmapstart + b / BPB, blk);
    uint32_t bi = b % BPB;
    if (!(blk[bi / 8] & 1 << (bi % 8))) die("freeing a free block");
    blk[bi / 8] &= ~(1 << (bi % 8));
    bwrite(sb.bmapstart + b / BPB, blk);
}

/* Find a free inode, give it TYPE and one link, and return its number. */
static uint32_t ialloc(uint16_t type)
{
    struct dinode di;
    for (uint32_t i = ROOTINO; i < sb.ninodes; i++) {
        iread(i, &di);
        if (di.type == T_FREE) {
            memset(&di, 0, sizeof di);
            di.type = type;
            di.nlink = 1;
            iwrite(i, &di);
            return i;
        }
    }
    die("out of inodes");
    return 0;
}

/* The disk block holding block BN of the file, allocating it — and the indirect block
 * if needed — when ALLOC is set. Returns 0 for a hole when ALLOC is clear. */
static uint32_t bmap(uint32_t inum, struct dinode *ip, uint32_t bn, int alloc)
{
    if (bn >= MAXFILE) die("file too large");
    if (bn < NDIRECT) {
        if (!ip->addrs[bn] && alloc) {
            ip->addrs[bn] = balloc();
            iwrite(inum, ip);
        }
        return ip->addrs[bn];
    }
    bn -= NDIRECT;
    if (!ip->addrs[NDIRECT]) {
        if (!alloc) return 0;
        ip->addrs[NDIRECT] = balloc();
        iwrite(inum, ip);
    }
    uint32_t ind[NINDIRECT];
    bread(ip->addrs[NDIRECT], ind);
    if (!ind[bn] && alloc) {
        ind[bn] = balloc();
        bwrite(ip->addrs[NDIRECT], ind);
    }
    return ind[bn];
}

/* Free every block of the file and set its size to 0. */
static void itruncate(uint32_t inum, struct dinode *ip)
{
    for (int i = 0; i < NDIRECT; i++)
        if (ip->addrs[i]) { bfree(ip->addrs[i]); ip->addrs[i] = 0; }
    if (ip->addrs[NDIRECT]) {
        uint32_t ind[NINDIRECT];
        bread(ip->addrs[NDIRECT], ind);
        for (uint32_t i = 0; i < NINDIRECT; i++) if (ind[i]) bfree(ind[i]);
        bfree(ip->addrs[NDIRECT]);
        ip->addrs[NDIRECT] = 0;
    }
    ip->size = 0;
    iwrite(inum, ip);
}

/* ---------------------------------------------------------------- Q2: reading and writing */

/* Read N bytes from OFF of the file into BUF; returns how many were read. */
static uint32_t iread_data(uint32_t inum, struct dinode *ip, uint32_t off, uint32_t n, char *buf)
{
    if (off > ip->size) return 0;
    if (off + n > ip->size) n = ip->size - off;
    uint32_t done = 0;
    while (done < n) {
        uint32_t b = bmap(inum, ip, (off + done) / BSIZE, 0);
        uint32_t in_block = BSIZE - (off + done) % BSIZE;
        uint32_t take = n - done < in_block ? n - done : in_block;
        if (b == 0) memset(buf + done, 0, take);          /* a hole reads as zeros */
        else {
            char blk[BSIZE];
            bread(b, blk);
            memcpy(buf + done, blk + (off + done) % BSIZE, take);
        }
        done += take;
    }
    return done;
}

/* Write N bytes from BUF at OFF, growing the file if needed. */
static uint32_t iwrite_data(uint32_t inum, struct dinode *ip, uint32_t off, uint32_t n, const char *buf)
{
    if (off + n > MAXFILE * BSIZE) die("file too large");
    uint32_t done = 0;
    while (done < n) {
        uint32_t b = bmap(inum, ip, (off + done) / BSIZE, 1);
        uint32_t in_block = BSIZE - (off + done) % BSIZE;
        uint32_t take = n - done < in_block ? n - done : in_block;
        char blk[BSIZE];
        bread(b, blk);
        memcpy(blk + (off + done) % BSIZE, buf + done, take);
        bwrite(b, blk);
        done += take;
    }
    if (off + n > ip->size) {
        ip->size = off + n;
        iwrite(inum, ip);
    }
    return done;
}

/* ---------------------------------------------------------------- Q3: directories and paths */

/* The inode number of NAME in directory DP, or 0. */
static uint32_t dirlookup(uint32_t dinum, struct dinode *dp, const char *name)
{
    struct dirent de;
    for (uint32_t off = 0; off < dp->size; off += sizeof de) {
        if (iread_data(dinum, dp, off, sizeof de, (char *)&de) != sizeof de) die("short directory read");
        if (de.inum && !strncmp(de.name, name, DIRSIZ)) return de.inum;
    }
    return 0;
}

/* Add NAME -> INUM to directory DP, reusing a free slot if there is one. */
static void dirlink(uint32_t dinum, struct dinode *dp, const char *name, uint32_t inum)
{
    if (strlen(name) >= DIRSIZ) die("name too long");
    if (dirlookup(dinum, dp, name)) die("name exists");
    struct dirent de;
    uint32_t off;
    for (off = 0; off < dp->size; off += sizeof de) {
        iread_data(dinum, dp, off, sizeof de, (char *)&de);
        if (de.inum == 0) break;
    }
    memset(&de, 0, sizeof de);
    de.inum = (uint16_t)inum;
    memcpy(de.name, name, strlen(name));          /* names shorter than DIRSIZ keep the zero padding */
    iwrite_data(dinum, dp, off, sizeof de, (const char *)&de);
}

/* Remove NAME from directory DP; returns the inode it named. */
static uint32_t dirunlink(uint32_t dinum, struct dinode *dp, const char *name)
{
    struct dirent de;
    for (uint32_t off = 0; off < dp->size; off += sizeof de) {
        iread_data(dinum, dp, off, sizeof de, (char *)&de);
        if (de.inum && !strncmp(de.name, name, DIRSIZ)) {
            uint32_t inum = de.inum;
            memset(&de, 0, sizeof de);
            iwrite_data(dinum, dp, off, sizeof de, (const char *)&de);
            return inum;
        }
    }
    return 0;
}

/* Resolve PATH. With PARENT set, stop at the last element and copy it into NAME,
 * returning the containing directory's inode number. */
static uint32_t namei(const char *path, int parent, char *name, struct dinode *ip)
{
    if (path[0] != '/') die("paths must be absolute");
    uint32_t inum = ROOTINO;
    iread(inum, ip);
    const char *p = path + 1;
    while (*p) {
        const char *slash = strchr(p, '/');
        size_t len = slash ? (size_t)(slash - p) : strlen(p);
        if (len == 0 || len >= DIRSIZ) die("bad path element");
        char elem[DIRSIZ + 1];
        memcpy(elem, p, len);
        elem[len] = 0;
        int last = !slash || !slash[1];
        if (parent && last) {
            memcpy(name, elem, len + 1);
            return inum;
        }
        if (ip->type != T_DIR) die("not a directory");
        uint32_t next = dirlookup(inum, ip, elem);
        if (!next) return 0;
        inum = next;
        iread(inum, ip);
        p = slash ? slash + 1 : p + len;
    }
    return inum;
}

/* ---------------------------------------------------------------- provided: the commands */

static void put_sb(void)
{
    char blk[BSIZE] = { 0 };
    memcpy(blk, &sb, sizeof sb);
    bwrite(1, blk);
}

static void format(uint32_t blocks)
{
    if (blocks < 64) die("too few blocks");
    char zero[BSIZE] = { 0 };
    for (uint32_t b = 0; b < blocks; b++) bwrite(b, zero);
    uint32_t ninodes = 128;
    uint32_t inodeblocks = (ninodes + IPB - 1) / IPB;
    uint32_t bitmapblocks = (blocks + BPB - 1) / BPB;
    sb.magic = MAGIC;
    sb.size = blocks;
    sb.ninodes = ninodes;
    sb.inodestart = 2;
    sb.bmapstart = sb.inodestart + inodeblocks;
    sb.datastart = sb.bmapstart + bitmapblocks;
    put_sb();
    for (uint32_t b = 0; b < sb.datastart; b++) {            /* metadata blocks are in use */
        char blk[BSIZE];
        bread(sb.bmapstart + b / BPB, blk);
        blk[(b % BPB) / 8] |= 1 << (b % 8);
        bwrite(sb.bmapstart + b / BPB, blk);
    }
    struct dinode root;
    uint32_t inum = ialloc(T_DIR);
    if (inum != ROOTINO) die("root is not inode 1");
    iread(inum, &root);
    dirlink(inum, &root, ".", inum);
    dirlink(inum, &root, "..", inum);
    iread(inum, &root);
    root.nlink = 2;
    iwrite(inum, &root);
    printf("formatted %u blocks of %d bytes: superblock 1, inodes %u-%u, bitmap %u-%u, data %u-%u\n",
           blocks, BSIZE, sb.inodestart, sb.bmapstart - 1, sb.bmapstart, sb.datastart - 1, sb.datastart, blocks - 1);
    printf("%u inodes, %u data blocks, max file %lu bytes\n", ninodes, blocks - sb.datastart, MAXFILE * (unsigned long)BSIZE);
}

static void load_sb(void)
{
    char blk[BSIZE];
    bread(1, blk);
    memcpy(&sb, blk, sizeof sb);
    if (sb.magic != MAGIC) die("not a myfs image (run format first)");
}

static uint32_t used_blocks(void)
{
    uint32_t n = 0;
    char blk[BSIZE];
    for (uint32_t b = 0; b < sb.size; b++) {
        if (b % BPB == 0) bread(sb.bmapstart + b / BPB, blk);
        if (blk[(b % BPB) / 8] & 1 << (b % 8)) n++;
    }
    return n;
}

/* Mark in SEEN every block the file at INUM reaches. Returns blocks counted. */
static uint32_t walk_file(uint32_t inum, unsigned char *seen)
{
    struct dinode di;
    iread(inum, &di);
    uint32_t n = 0;
    for (int i = 0; i < NDIRECT; i++) if (di.addrs[i]) { seen[di.addrs[i]]++; n++; }
    if (di.addrs[NDIRECT]) {
        seen[di.addrs[NDIRECT]]++;
        n++;
        uint32_t ind[NINDIRECT];
        bread(di.addrs[NDIRECT], ind);
        for (uint32_t i = 0; i < NINDIRECT; i++) if (ind[i]) { seen[ind[i]]++; n++; }
    }
    return n;
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr, "usage: %s IMAGE COMMAND [ARGS]\n", argv[0]);
        return 1;
    }
    const char *path = argv[1], *cmd = argv[2];
    img = fopen(path, strcmp(cmd, "format") ? "r+b" : "w+b");
    if (!img) { perror(path); return 1; }

    struct dinode ip, dp;
    char name[DIRSIZ + 1];
    uint32_t inum, dinum;

    if (!strcmp(cmd, "format")) {
        format(argc > 3 ? (uint32_t)strtoul(argv[3], 0, 10) : 2048);
    } else if (load_sb(), !strcmp(cmd, "mkdir") || !strcmp(cmd, "create")) {
        if (argc < 4) die("usage: mkdir|create PATH");
        int isdir = cmd[0] == 'm';
        dinum = namei(argv[3], 1, name, &dp);
        if (!dinum) die("no such directory");
        if (dirlookup(dinum, &dp, name)) die("already exists");
        inum = ialloc(isdir ? T_DIR : T_FILE);
        dirlink(dinum, &dp, name, inum);
        if (isdir) {
            iread(inum, &ip);
            dirlink(inum, &ip, ".", inum);
            dirlink(inum, &ip, "..", dinum);
            iread(inum, &ip);
            ip.nlink = 2;
            iwrite(inum, &ip);
            iread(dinum, &dp);
            dp.nlink++;
            iwrite(dinum, &dp);
        }
        printf("%s %s: inode %u\n", isdir ? "mkdir" : "create", argv[3], inum);
    } else if (!strcmp(cmd, "write") || !strcmp(cmd, "append")) {
        if (argc < 6) die("usage: write|append PATH SIZE BYTE");
        inum = namei(argv[3], 0, name, &ip);
        if (!inum) die("no such file");
        uint32_t n = (uint32_t)strtoul(argv[4], 0, 10);
        int byte = (int)strtoul(argv[5], 0, 16);
        uint32_t off = cmd[0] == 'a' ? ip.size : 0;
        if (cmd[0] == 'w') itruncate(inum, &ip);
        char buf[BSIZE];
        memset(buf, byte, sizeof buf);
        uint32_t done = 0;
        while (done < n) {
            uint32_t take = n - done < BSIZE ? n - done : BSIZE;
            iwrite_data(inum, &ip, off + done, take, buf);
            done += take;
        }
        iread(inum, &ip);
        printf("%s %s: %u bytes at %u, size now %u, %u blocks\n", cmd, argv[3], n, off, ip.size,
               (ip.size + BSIZE - 1) / BSIZE);
    } else if (!strcmp(cmd, "read")) {
        if (argc < 6) die("usage: read PATH OFF LEN");
        inum = namei(argv[3], 0, name, &ip);
        if (!inum) die("no such file");
        uint32_t off = (uint32_t)strtoul(argv[4], 0, 10), n = (uint32_t)strtoul(argv[5], 0, 10);
        char *buf = malloc(n ? n : 1);
        uint32_t got = iread_data(inum, &ip, off, n, buf);
        printf("read %s %u+%u: %u bytes", argv[3], off, n, got);
        for (uint32_t i = 0; i < got;) {                        /* summarise as runs */
            uint32_t j = i;
            while (j < got && buf[j] == buf[i]) j++;
            printf("  %02x x%u", (unsigned char)buf[i], j - i);
            i = j;
        }
        printf("\n");
        free(buf);
    } else if (!strcmp(cmd, "ls")) {
        if (argc < 4) die("usage: ls PATH");
        inum = namei(argv[3], 0, name, &ip);
        if (!inum) die("no such directory");
        if (ip.type != T_DIR) die("not a directory");
        printf("ls %s\n", argv[3]);
        struct dirent de;
        for (uint32_t off = 0; off < ip.size; off += sizeof de) {
            iread_data(inum, &ip, off, sizeof de, (char *)&de);
            if (!de.inum) continue;
            struct dinode e;
            iread(de.inum, &e);
            printf("  %-14.14s inode %3u %-4s links %u size %u\n", de.name, de.inum,
                   e.type == T_DIR ? "dir" : "file", e.nlink, e.size);
        }
    } else if (!strcmp(cmd, "stat")) {
        if (argc < 4) die("usage: stat PATH");
        inum = namei(argv[3], 0, name, &ip);
        if (!inum) die("no such file");
        unsigned char *seen = calloc(sb.size, 1);
        uint32_t blocks = walk_file(inum, seen);
        free(seen);
        printf("stat %s: inode %u %s links %u size %u blocks %u\n", argv[3], inum,
               ip.type == T_DIR ? "dir" : "file", ip.nlink, ip.size, blocks);
    } else if (!strcmp(cmd, "link")) {
        if (argc < 5) die("usage: link OLD NEW");
        inum = namei(argv[3], 0, name, &ip);
        if (!inum) die("no such file");
        if (ip.type == T_DIR) die("cannot link a directory");
        dinum = namei(argv[4], 1, name, &dp);
        if (!dinum) die("no such directory");
        dirlink(dinum, &dp, name, inum);
        iread(inum, &ip);
        ip.nlink++;
        iwrite(inum, &ip);
        printf("link %s %s: inode %u links %u\n", argv[3], argv[4], inum, ip.nlink);
    } else if (!strcmp(cmd, "rm")) {
        if (argc < 4) die("usage: rm PATH");
        dinum = namei(argv[3], 1, name, &dp);
        if (!dinum) die("no such directory");
        inum = dirlookup(dinum, &dp, name);
        if (!inum) die("no such file");
        iread(inum, &ip);
        if (ip.type == T_DIR) die("cannot remove a directory");
        dirunlink(dinum, &dp, name);
        ip.nlink--;
        iwrite(inum, &ip);
        if (ip.nlink == 0) {
            itruncate(inum, &ip);
            ip.type = T_FREE;
            iwrite(inum, &ip);
            printf("rm %s: inode %u freed\n", argv[3], inum);
        } else {
            printf("rm %s: inode %u still has %u links\n", argv[3], inum, ip.nlink);
        }
    } else if (!strcmp(cmd, "df")) {
        uint32_t used = used_blocks(), ninuse = 0;
        for (uint32_t i = ROOTINO; i < sb.ninodes; i++) { iread(i, &ip); if (ip.type != T_FREE) ninuse++; }
        printf("df: %u of %u blocks used (%u free), %u of %u inodes used\n", used, sb.size, sb.size - used,
               ninuse, sb.ninodes - 1);
    } else if (!strcmp(cmd, "dump")) {
        printf("dump: size %u ninodes %u inodestart %u bmapstart %u datastart %u\n",
               sb.size, sb.ninodes, sb.inodestart, sb.bmapstart, sb.datastart);
        char blk[BSIZE];
        bread(sb.bmapstart, blk);
        printf("bitmap:");
        for (int i = 0; i < 8; i++) printf(" %02x", (unsigned char)blk[i]);
        printf("  (blocks 0-63)\n");
    } else if (!strcmp(cmd, "fsck")) {
        unsigned char *seen = calloc(sb.size, 1);
        for (uint32_t b = 0; b < sb.datastart; b++) seen[b]++;
        uint32_t files = 0;
        for (uint32_t i = ROOTINO; i < sb.ninodes; i++) {
            iread(i, &ip);
            if (ip.type == T_FREE) continue;
            files++;
            walk_file(i, seen);
        }
        uint32_t marked = 0, reached = 0, lost = 0, dbl = 0, phantom = 0;
        char blk[BSIZE];
        for (uint32_t b = 0; b < sb.size; b++) {
            if (b % BPB == 0) bread(sb.bmapstart + b / BPB, blk);
            int inmap = (blk[(b % BPB) / 8] & 1 << (b % 8)) != 0;
            marked += inmap;
            reached += seen[b] > 0;
            if (seen[b] > 1) dbl++;
            if (seen[b] && !inmap) phantom++;
            if (!seen[b] && inmap) lost++;
        }
        free(seen);
        printf("fsck: %u inodes in use, %u blocks marked, %u blocks reachable, "
               "%u leaked, %u used twice, %u used but not marked\n", files, marked, reached, lost, dbl, phantom);
    } else {
        die("unknown command");
    }
    fclose(img);
    return 0;
}
