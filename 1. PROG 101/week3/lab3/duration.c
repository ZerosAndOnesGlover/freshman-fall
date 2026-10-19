#include <stdio.h>

static int counter(void)   { static int n = 0; return ++n; }
static int automatic(void) {        int n = 0; return ++n; }

int main(void) {
    printf("call  counter()  automatic()\n");
    for (int i = 1; i <= 4; i++) {
        int c = counter();
        int a = automatic();
        printf("%4d  %9d  %11d\n", i, c, a);
    }
    return 0;
}
