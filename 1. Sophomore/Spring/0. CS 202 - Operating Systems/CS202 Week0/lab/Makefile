# CS 202 · Lab 0 · a kernel that prints Hello
#
#   make          build hello.elf
#   make run      boot it in QEMU; output appears in this terminal
#   make clean
#
# QEMU is the machine. -kernel loads a Multiboot ELF directly, so there is no
# bootloader to write. isa-debug-exit is a fake device: when the kernel writes a
# byte v to port 0xf4, QEMU exits with status (v << 1) | 1.

CC      = gcc
CFLAGS  = -m32 -ffreestanding -fno-pic -fno-stack-protector -nostdlib -O2 -Wall -Wextra
LDFLAGS = -m elf_i386 -T link.ld -z noexecstack --no-warn-rwx-segments
QEMU    = qemu-system-i386
QEMUOPTS = -kernel hello.elf -display none -monitor none -serial stdio -no-reboot \
           -device isa-debug-exit,iobase=0xf4,iosize=0x04

hello.elf: boot.o kernel.o link.ld
	ld $(LDFLAGS) -o $@ boot.o kernel.o

%.o: %.S
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

run: hello.elf
	@echo "--- booting (Ctrl-C quits if your kernel never powers off) ---"
	@$(QEMU) $(QEMUOPTS); echo "--- QEMU exited with status $$? ---"

clean:
	rm -f *.o hello.elf

.PHONY: run clean
