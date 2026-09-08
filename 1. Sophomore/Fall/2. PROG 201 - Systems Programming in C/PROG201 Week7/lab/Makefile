CFLAGS = -Wall -Wextra -O2 -g -std=c11

all: links vfs durable durable2

links: links.c
	$(CC) $(CFLAGS) -o $@ $<
vfs: vfs.c
	$(CC) $(CFLAGS) -o $@ $<
durable: durable.c
	$(CC) $(CFLAGS) -o $@ $<
durable2: durable2.c
	$(CC) $(CFLAGS) -o $@ $<

image: 
	./mkimage.sh disk.img 64

clean:
	rm -f links vfs durable durable2 t.dat t2.dat cfg.txt cfg.tmp a.txt b.txt s.txt

clean-images:
	rm -f disk.img *.img

.PHONY: all image clean clean-images
