/* fallthrough.c — PROG 101 Lab 2, Part 3A: deliberate fall-through.
 * Each falling-through arm carries a "fall through" comment (recognised by
 * gcc's -Wimplicit-fallthrough), declaring the intent. This builds clean
 * under -Werror -pedantic without changing the output.
 */
#include <stdio.h>

int main(void) {
    for (int n = 1; n <= 5; n++) {
        printf("n=%d: ", n);
        switch (n) {
            case 1: printf("one ");   /* fall through */
            case 2: printf("two ");   /* fall through */
            case 3: printf("three "); break;
            case 4: printf("four "); break;
            default: printf("other ");
        }
        printf("\n");
    }
    return 0;
}
