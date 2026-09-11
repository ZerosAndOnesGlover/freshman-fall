/* boot.S: everything that has to be assembly.
 *
 * QEMU (acting as a Multiboot loader) finds the header below, loads the ELF at
 * 1 MB and jumps to _start with the CPU in 32-bit protected mode, ring 0,
 * paging off and interrupts off. There is no stack yet, so we make one. */

        .section .note.GNU-stack,"",@progbits

        .set MB_MAGIC,    0x1BADB002
        .set MB_FLAGS,    0
        .set MB_CHECKSUM, -(MB_MAGIC + MB_FLAGS)

        .section .multiboot
        .align 4
        .long MB_MAGIC, MB_FLAGS, MB_CHECKSUM

        .section .bss
        .align 16
stack_bottom:
        .skip 16384
stack_top:

        .section .text
        .globl _start
_start:
        mov  $stack_top, %esp
        call kmain
        /* kmain returned: nothing left to do. Stop the CPU for good. */
        cli
1:      hlt
        jmp  1b

/* void outb(unsigned short port, unsigned char value)
 * The OUT instruction. In ring 3 this is a general-protection fault (L02 §3). */
        .globl outb
outb:
        mov  4(%esp), %edx
        mov  8(%esp), %eax
        outb %al, (%dx)
        ret

/* unsigned get_cs(void): the code segment selector. Its low two bits are the CPL. */
        .globl get_cs
get_cs:
        xor  %eax, %eax
        mov  %cs, %ax
        ret
