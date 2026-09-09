/* PROG 201 -- Lab 10: the parser to fuzz.  It decodes a toy "record" format
 * and has three planted bugs.  Your job is to make the fuzzer find them and
 * then say which line each crash points to.  Do NOT read too hard first --
 * finding them by fuzzing is the exercise. */
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>

/* record: [len:1][tag:1][count:1][kind:1][payload...] */
int parse(const uint8_t *d, size_t n)
{
    if (n < 4) return 0;

    uint8_t len   = d[0];
    uint8_t tag   = d[1];
    uint8_t count = d[2];
    uint8_t kind  = d[3];

    char name[16];
    if (tag == 'C')
        memcpy(name, d + 4, len);          /* copy `len` bytes of payload */

    if (kind == 'D')
        return 100 / count;                /* divide by the count field */

    if (kind == 'R')
        return d[4 + len];                 /* read one byte at an offset */

    (void) name;
    return 1;
}
