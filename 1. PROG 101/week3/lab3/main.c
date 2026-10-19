#include <stdio.h>

#include "mathutil.h"

int main(void) {
    printf("gcd(48,18)=%d gcd(-48,18)=%d gcd(17,5)=%d gcd(0,7)=%d\n",
           gcd(48, 18), gcd(-48, 18), gcd(17, 5), gcd(0, 7));

    printf("factorial:");
    for (int i = 0; i <= 12; i++) {
        printf(" %ld", factorial(i));
    }
    printf("\n");

    printf("primes<30:");
    for (int n = 2; n < 30; n++) {
        if (is_prime(n)) {
            printf(" %d", n);
        }
    }
    printf("\n");

    printf("lcm(2147483646, 2147483647)=%lld\n",
           lcm(2147483646, 2147483647));
    return 0;
}
