# Builds cs202ring.ko against the running kernel's headers.
#   make          build
#   make clean    remove the build products
# CS 202 Week 9, PS 9.
obj-m += cs202ring.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
