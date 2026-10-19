/* floats.c — PROG 101, Week 1, Problem Set 1 (Problem 4)
 * Floating point: rounding error, epsilon, precision limit, overflow,
 * NaN and negative zero. Link with -lm.
 *
 *   gcc -Wall -Wextra -std=c11 -o floats floats.c -lm
 */

#include <stdio.h>
#include <float.h>
#include <math.h>

int main(void) {
    double sum = 0.1 + 0.2;

    printf("0.1 + 0.2       = %.17g\n", sum);
    printf("== 0.3?           %d\n", sum == 0.3);
    printf("|sum - 0.3| < 1e-9? %d\n", fabs(sum - 0.3) < 1e-9);

    printf("DBL_EPSILON     = %g\n", DBL_EPSILON);
    printf("FLT_EPSILON     = %g\n", FLT_EPSILON);

    printf("16777216f + 1   = %.1f\n", (double)(16777216.0f + 1.0f));

    printf("DBL_MAX * 2     = %g\n", DBL_MAX * 2.0);

    double zero = 0.0;
    double nan  = zero / zero;
    printf("0.0 / 0.0       = %f; nan == nan is %d; isnan is %d\n",
           nan, nan == nan, isnan(nan));

    printf("-0.0 == 0.0 is %d, printed as %f, 1/-0.0 = %f\n",
           -0.0 == 0.0, -0.0, 1.0 / -0.0);

    return 0;
}
