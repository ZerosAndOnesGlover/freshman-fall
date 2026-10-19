/* asrt.c — demonstrates assert(n >= 0) firing inside factorial.
 *
 * Build with assertions active (default):
 *     gcc -Wall -Wextra -Werror -pedantic -std=c11 -g asrt.c mathutil.c -o asrt
 * Build with assertions compiled out:
 *     gcc -DNDEBUG -Wall -Wextra -Werror -pedantic -std=c11 -g asrt.c mathutil.c -o asrt_ndebug
 */
#include <stdio.h>

#include "mathutil.h"

int main(void) {
    printf("%ld\n", factorial(-1));
    return 0;
}
