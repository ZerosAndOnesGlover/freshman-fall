/* kernel.c: the whole kernel. CS 202 Lab 0.
 *
 * There is no libc, no printf, no operating system underneath you: you ARE the
 * operating system. The only way to make anything happen is to talk to the
 * (emulated) hardware directly. Five TODOs; do them in order and `make run`
 * after each one. */

#define COM1        0x3F8   /* first serial port: QEMU copies it to your terminal */
#define DEBUG_EXIT  0xF4    /* QEMU's isa-debug-exit device                       */
#define VGA_TEXT    0xB8000 /* 80x25 text-mode screen: one 16-bit cell per char  */

void outb(unsigned short port, unsigned char value);   /* boot.S */
unsigned get_cs(void);                                 /* boot.S */

/* TODO 1: send one character to the serial port. One line. */
static void serial_putc(char c)
{
    (void)c;
}

/* TODO 2: send a NUL-terminated string, using serial_putc. */
static void serial_puts(const char *s)
{
    (void)s;
}

void kmain(void)
{
    /* TODO 3: print "Hello from ring 0" and a newline. */

    /* TODO 4: print "CPL = " followed by the current privilege level as a
     * single digit. get_cs() returns the CS selector; the CPL is its low two
     * bits. You have no printf: convert the digit to a character yourself. */

    /* TODO 5: power the machine off by writing 0 to port DEBUG_EXIT, so that
     * `make run` returns instead of hanging. What status does QEMU exit with? */

    (void)serial_puts;     /* delete these two lines once TODO 3 uses them */
    (void)serial_putc;
}
