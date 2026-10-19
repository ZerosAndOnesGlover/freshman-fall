/* main.c — feeds the sample data into the running-statistics library
 * one value at a time (no arrays yet) and prints every statistic to six
 * decimal places.
 */
#include <stdio.h>

#include "stats.h"

int main(void) {
    stats_reset();
    stats_add(2.0);
    stats_add(4.0);
    stats_add(4.0);
    stats_add(4.0);
    stats_add(5.0);
    stats_add(5.0);
    stats_add(7.0);
    stats_add(9.0);

    printf("count    %d\n",   stats_count());
    printf("mean     %.6f\n", stats_mean());
    printf("variance %.6f\n", stats_variance());
    printf("stddev   %.6f\n", stats_stddev());
    printf("min      %.6f\n", stats_min());
    printf("max      %.6f\n", stats_max());
    return 0;
}
