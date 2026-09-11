/* rtsim.c: periodic real-time tasks on one CPU, under rate-monotonic and
 * earliest-deadline-first scheduling. Deadlines equal periods; all tasks are
 * released together at time 0; the simulation runs for one hyperperiod.
 *
 *   gcc -O2 -Wall -Wextra -o rtsim rtsim.c
 *   ./rtsim rm  "2/5 4/7"      tasks as C/P: 2 ms of CPU every 5 ms, 4 every 7
 *   ./rtsim edf "2/5 4/7"
 *
 * CS 202 Week 2, L09 §2.
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXT 8

static long gcd(long a, long b) { while (b) { long t = a % b; a = b; b = t; } return a; }

int main(int argc, char **argv)
{
    if (argc != 3 || (strcmp(argv[1], "rm") && strcmp(argv[1], "edf"))) {
        fprintf(stderr, "usage: %s rm|edf \"C/P C/P ...\"\n", argv[0]);
        return 2;
    }
    int edf = !strcmp(argv[1], "edf");
    int n = 0, C[MAXT], P[MAXT];
    char *spec = strdup(argv[2]);
    for (char *tok = strtok(spec, " "); tok && n < MAXT; tok = strtok(0, " "))
        if (sscanf(tok, "%d/%d", &C[n], &P[n]) == 2) n++;
    long hyper = 1;
    double U = 0;
    for (int i = 0; i < n; i++) { hyper = hyper / gcd(hyper, P[i]) * P[i]; U += (double)C[i] / P[i]; }
    double bound = n * (pow(2.0, 1.0 / n) - 1);
    printf("%s: %d tasks, utilisation %.3f, Liu-Layland RM bound %.3f, hyperperiod %ld ms\n",
           edf ? "EDF" : "RM", n, U, bound, hyper);

    int remaining[MAXT] = {0}, deadline[MAXT] = {0}, misses = 0;
    char line[80];
    int len = 0;
    for (long t = 0; t < hyper; t++) {
        for (int i = 0; i < n; i++) {
            if (t % P[i] == 0) {
                if (remaining[i] > 0) {
                    printf("  t=%ld: task %d missed its deadline with %d ms left\n", t, i + 1, remaining[i]);
                    misses++;
                }
                remaining[i] = C[i];
                deadline[i] = t + P[i];
            }
        }
        int run = -1;
        for (int i = 0; i < n; i++) {
            if (!remaining[i]) continue;
            if (run < 0) { run = i; continue; }
            if (edf ? deadline[i] < deadline[run] || (deadline[i] == deadline[run] && i < run)
                    : P[i] < P[run])
                run = i;
        }
        if (t < 70)
            line[len++] = run < 0 ? '.' : (char)('1' + run);
        if (run >= 0) remaining[run]--;
    }
    line[len] = 0;
    for (int i = 0; i < n; i++)
        if (remaining[i] > 0) { printf("  t=%ld: task %d missed its deadline with %d ms left\n", hyper, i + 1, remaining[i]); misses++; }
    printf("  first %ld ms: %s\n  deadline misses in one hyperperiod: %d\n", hyper < 70 ? hyper : 70, line, misses);
    free(spec);
    return 0;
}
