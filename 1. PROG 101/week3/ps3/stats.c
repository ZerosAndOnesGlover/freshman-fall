/* stats.c — running statistics over values fed in one at a time.
 * All state lives in file-level statics: private to this translation unit
 * (internal linkage) and alive for the whole run.
 *
 * Contracts (Problem 4.1):
 *   stats_mean
 *     precondition : count > 0          (at least one value has been added)
 *     postcondition: returns sum / count
 *   invariant between calls
 *     count values have been added since the last reset;
 *     sum   == total of those values;
 *     sum_sq == total of their squares;
 *     count > 0 implies lowest <= mean <= highest.
 */
#include <assert.h>
#include <math.h>

#include "stats.h"

static int    count   = 0;
static double sum     = 0.0;
static double sum_sq  = 0.0;
static double lowest  = 0.0;
static double highest = 0.0;

static double square(double x) {   /* file-private helper */
    return x * x;
}

void stats_reset(void) {
    count   = 0;
    sum     = 0.0;
    sum_sq  = 0.0;
    lowest  = 0.0;
    highest = 0.0;
}

void stats_add(double x) {
    if (count == 0 || x < lowest) {
        lowest = x;
    }
    if (count == 0 || x > highest) {
        highest = x;
    }
    count++;
    sum    += x;
    sum_sq += square(x);
}

int stats_count(void) {
    return count;
}

double stats_mean(void) {
    assert(count > 0);              /* precondition: at least one value */
    return sum / count;
}

double stats_variance(void) {
    assert(count > 1);             /* sample variance needs two values */
    double m = stats_mean();
    return (sum_sq - count * m * m) / (count - 1);
}

double stats_stddev(void) {
    return sqrt(stats_variance());
}

double stats_min(void) {
    assert(count > 0);
    return lowest;
}

double stats_max(void) {
    assert(count > 0);
    return highest;
}
