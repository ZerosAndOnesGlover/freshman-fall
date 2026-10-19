#include <stdio.h>

static void try_modify(int x) {
    printf("  inside: &x=%p x=%d -> ", (void*)&x, x);
    x = 999;
    printf("%d\n", x);
}

int main(void) {
    int v = 42;
    printf("before: &v=%p v=%d\n", (void*)&v, v);
    try_modify(v);
    printf("after : &v=%p v=%d\n", (void*)&v, v);
    return 0;
}
