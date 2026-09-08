#include <stdio.h>
#include <time.h>
int main(void)
{
    time_t t = time(NULL);
    printf("time() = %ld -> %s", (long) t, ctime(&t));
    return 0;
}
