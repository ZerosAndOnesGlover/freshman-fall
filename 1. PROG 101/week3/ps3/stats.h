/* stats.h — a running-statistics library (values fed in one at a time).
 * The include guard is essential: without it, a translation unit that
 * includes this header twice (directly and via another header) would see
 * duplicate declarations — and, worse, duplicate *definitions* when there
 * are any — producing "redefinition" errors.
 */
#ifndef STATS_H
#define STATS_H

void   stats_reset(void);
void   stats_add(double x);
int    stats_count(void);
double stats_mean(void);
double stats_variance(void);   /* sample variance, denominator n - 1 */
double stats_stddev(void);
double stats_min(void);
double stats_max(void);

#endif /* STATS_H */
