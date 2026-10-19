/* flags.c — PROG 101, Week 2, Problem Set 2 (Problem 1)
 * A file-permission set in one unsigned int: set / clear / toggle bits,
 * test membership as exactly 0 or 1, count set bits, render as rwx.
 *
 *   gcc -Wall -Wextra -Werror -pedantic -std=c11 -o flags flags.c
 */

#include <stdio.h>

#define PERM_READ  (1u << 0)
#define PERM_WRITE (1u << 1)
#define PERM_EXEC  (1u << 2)

int main(void) {
    unsigned p = 0;

    p = p | PERM_READ;                 /* set READ   */
    printf("set READ     -> %u\n", p);
    p = p | PERM_EXEC;                 /* set EXEC   */
    printf("set EXEC     -> %u\n", p);
    p = p & ~PERM_READ;                /* clear READ */
    printf("clear READ   -> %u\n", p);
    p = p ^ PERM_WRITE;                /* toggle WRITE */
    printf("toggle WRITE -> %u\n", p);

    printf("test WRITE   -> %d\n", (p & PERM_WRITE) != 0);  /* exactly 0 or 1 */
    printf("test READ    -> %d\n", (p & PERM_READ) != 0);

    int count = 0;                     /* count set bits */
    for (unsigned rest = p; rest != 0; rest = rest >> 1) {
        count += (int)(rest & 1u);
    }
    printf("bits set     -> %d\n", count);

    printf("as rwx       -> %c%c%c\n",
           (p & PERM_READ)  ? 'r' : '-',
           (p & PERM_WRITE) ? 'w' : '-',
           (p & PERM_EXEC)  ? 'x' : '-');

    return 0;
}
