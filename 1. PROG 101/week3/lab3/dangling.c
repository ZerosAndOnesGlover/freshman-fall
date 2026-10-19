/* dangling.c — two versions of the same "return a pointer to a local" bug.
 *
 * Version 1 (the default) warns all by itself:
 *     gcc -std=c11 -g dangling.c -o dangling
 *
 * Version 2 launders the address through identity() and is silent even under
 * the full warning set:
 *     gcc -Wall -Wextra -pedantic -std=c11 -g -DVERSION2 dangling.c -o dangling2
 *
 * Under AddressSanitizer the silent version is still caught at run time:
 *     gcc -Wall -Wextra -pedantic -std=c11 -g -DVERSION2 -fsanitize=address \
 *         dangling.c -o dangling2_asan
 */
#include <stdio.h>

#ifdef VERSION2
/* version 2 — one function further away */
static int *identity(int *p) { return p; }
static int *make2(void) { int x = 42; return identity(&x); }
#else
/* version 1 — direct */
static int *make(void) { int x = 42; return &x; }
#endif

int main(void) {
#ifdef VERSION2
    int *p = make2();
#else
    int *p = make();
#endif
    printf("%d\n", *p);   /* dereference the dangling pointer */
    return 0;
}
