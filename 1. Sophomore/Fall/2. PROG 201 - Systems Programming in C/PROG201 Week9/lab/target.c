#include <stdio.h>
#include <stdlib.h>
void sprof_start(long); void sprof_report(int);

/* Not static, and each takes a value the compiler cannot fold away --
 * otherwise gcc computes the answer once and the profile is four samples. */
__attribute__((noinline)) double slow(long n, double k)
{ double s = 0; for (long i = 1; i <= n; i++) s += k / i; return s; }

__attribute__((noinline)) double medium(long n, double k)
{ double s = 0; for (long i = 1; i <= n; i++) s += i * k; return s; }

__attribute__((noinline)) double quick(long n, double k)
{ double s = 0; for (long i = 1; i <= n; i++) s += i + k; return s; }

int main(void)
{
    sprof_start(1000);                       /* one sample per ms of CPU */
    double s = 0;
    for (int r = 0; r < 40; r++) {
        s += slow(3000000, 1.0 + r);
        s += medium(1000000, 0.5 + r);
        s += quick(200000, r);
    }
    printf("%f\n", s);
    sprof_report(8);
    return 0;
}
