/* link.ld: put the kernel at 1 MB, where Multiboot loaders expect it, and put
 * the Multiboot header first so the loader can find it in the first 8 KB. */
ENTRY(_start)

SECTIONS
{
    . = 1M;
    .text   : { *(.multiboot) *(.text*) }
    .rodata : { *(.rodata*) }
    .data   : { *(.data*) }
    .bss    : { *(COMMON) *(.bss*) }
}
