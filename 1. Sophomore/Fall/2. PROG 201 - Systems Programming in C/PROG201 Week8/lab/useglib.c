#include <stdio.h>
int greet(int);
int farewell(int);
int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);          /* so LD_DEBUG interleaves */
    fprintf(stderr, ">>> about to call greet the first time\n");
    printf("greet(10)    = %d\n", greet(10));
    fprintf(stderr, ">>> about to call greet the second time\n");
    printf("greet(20)    = %d\n", greet(20));
    fprintf(stderr, ">>> about to call farewell the first time\n");
    printf("farewell(10) = %d\n", farewell(10));
    return 0;
}
