#ifndef MATHUTIL_H
#define MATHUTIL_H

int  gcd(int a, int b);
long factorial(int n);
int  is_prime(int n);

/* Bonus: least common multiple, computed without overflowing for
 * inputs near INT_MAX (divide before multiplying). */
long long lcm(int a, int b);

#endif /* MATHUTIL_H */
