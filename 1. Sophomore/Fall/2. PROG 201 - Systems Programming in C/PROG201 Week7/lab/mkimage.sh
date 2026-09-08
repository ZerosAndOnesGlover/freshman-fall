#!/bin/bash
# PROG 201 -- Lab 7: build a small ext4 filesystem in a file.
#
# No root and no mounting: mke2fs, debugfs, dumpe2fs and e2fsck all work on
# an ordinary file.  Only mount(8) needs privileges, and we never mount.
set -e
IMG=${1:-disk.img}
MB=${2:-64}

rm -f "$IMG"
dd if=/dev/zero of="$IMG" bs=1M count="$MB" status=none
# 1 KiB blocks so that indirect blocks and extents are visible at small sizes
mke2fs -q -t ext4 -b 1024 -F "$IMG"

printf 'hello from a file\n'      > /tmp/p201-note.txt
head -c 200000 /dev/urandom       > /tmp/p201-big.bin
head -c 5000000 /dev/urandom      > /tmp/p201-huge.bin

debugfs -w -f /dev/stdin "$IMG" >/dev/null 2>&1 <<EOF
mkdir /docs
cd /docs
write /tmp/p201-note.txt note.txt
cd /
write /tmp/p201-big.bin big.bin
write /tmp/p201-huge.bin huge.bin
ln /docs/note.txt /alias.txt
symlink /link.txt /docs/note.txt
symlink /longlink.txt /a/very/long/target/path/that/will/not/fit/inside/the/inode/at/all/xxxxxxxx
quit
EOF

rm -f /tmp/p201-note.txt /tmp/p201-big.bin /tmp/p201-huge.bin

# debugfs's `ln` does not update the link count.  Fix it now so that the image
# starts clean -- Part A is about noticing that it did not.
e2fsck -fy "$IMG" >/dev/null 2>&1 || true

echo "built $IMG (${MB} MiB, 1 KiB blocks)"
echo
echo "  /docs/note.txt   and  /alias.txt   are the same inode  (a hard link)"
echo "  /link.txt        is a short symlink   (fits in the inode)"
echo "  /longlink.txt    is a long symlink    (needs a block)"
echo "  /big.bin         200,000 bytes"
echo "  /huge.bin        5,000,000 bytes"
