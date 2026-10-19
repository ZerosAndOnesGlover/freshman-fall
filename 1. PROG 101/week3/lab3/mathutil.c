#include <assert.h>

#include "mathutil.h"

/* File-private helper: visible only in this translation unit (internal linkage). */
static int abs_int(int x) { return x < 0 ? -x : x; }

int gcd(int a, int b) {
    a = abs_int(a);
    b = abs_int(b);
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}

long factorial(int n) {
    assert(n >= 0);          /* programmer error: negative input */
    long r = 1;
    for (int i = 2; i <= n; i++) {
        r *= i;
    }
    return r;
}

int is_prime(int n) {
    if (n < 2) {
        return 0;
    }
    for (int d = 2; d <= n / d; d++) {   /* d <= n/d avoids d*d overflow */
        if (n % d == 0) {
            return 0;
        }
    }
    return 1;
}

long long lcm(int a, int b) {
    if (a == 0 || b == 0) {
        return 0;
    }
    int g = gcd(a, b);
    long long r = ((long long)a / g) * b;   /* divide first: no overflow near INT_MAX */
    return r < 0 ? -r : r;
}
