// int13.c: an xv6 user program that executes two instructions it may not.
//
// Copy into your xv6 directory, add _int13 to UPROGS in the Makefile, and
// `make qemu-nox`. Then, at the xv6 shell:
//
//   $ int13          executes int $13 — a jump through a kernel-only IDT gate
//   $ int13 cli      executes cli     — a privileged instruction
//
// CS 202 Lab 0, Part D.

#include "types.h"
#include "user.h"

void asm_int13(void);
void asm_cli(void);

__asm__(".globl asm_int13, asm_cli\n"
        "asm_int13: int $13; ret\n"
        "asm_cli:   cli;     ret\n");

int
main(int argc, char *argv[])
{
  if(argc > 1){
    printf(1, "int13: executing cli\n");
    asm_cli();
  } else {
    printf(1, "int13: executing int $13\n");
    asm_int13();
  }
  printf(1, "int13: still running?\n");
  exit();
}
