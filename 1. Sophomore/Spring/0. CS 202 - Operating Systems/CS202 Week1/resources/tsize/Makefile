# Build a module object against this machine's headers. It is never loaded:
# the sizes are read from the symbol table.
#
#   make && nm -S tsize.o | grep _size

obj-m += tsize.o

all:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(CURDIR) modules

clean:
	$(MAKE) -C /lib/modules/$(shell uname -r)/build M=$(CURDIR) clean
