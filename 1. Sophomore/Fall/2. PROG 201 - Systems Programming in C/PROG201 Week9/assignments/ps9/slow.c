/* PROG 201 -- PS 9: a slow program.
 *
 * It reads a word list, counts how many times each word occurs, scores each
 * word, and prints a summary.  The answers are correct.  It is much slower
 * than it needs to be, and the reasons are findable with a profiler.
 *
 *   ./slow words.txt
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define MAXWORDS 200000
#define MAXLEN   64

static char  words[MAXWORDS][MAXLEN];
static long  counts[MAXWORDS];
static double scores[MAXWORDS];
static int   nwords;

static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}

/* find a word, or -1 */
static int lookup(const char *w)
{
    for (int i = 0; i < nwords; i++)
        if (strcmp(words[i], w) == 0) return i;
    return -1;
}

static void add_word(const char *w)
{
    int i = lookup(w);
    if (i >= 0) { counts[i]++; return; }
    if (nwords >= MAXWORDS) return;
    strncpy(words[nwords], w, MAXLEN - 1);
    counts[nwords] = 1;
    nwords++;
}

/* normalise a word to lower case, in a freshly allocated buffer */
static char *normalise(const char *w)
{
    char *out = malloc(MAXLEN);
    int j = 0;
    for (int i = 0; i < (int) strlen(w) && j < MAXLEN - 1; i++)
        if (isalpha((unsigned char) w[i])) out[j++] = (char) tolower((unsigned char) w[i]);
    out[j] = 0;
    return out;
}

/* score = count weighted by how many OTHER words share its first letter */
static void compute_scores(void)
{
    for (int i = 0; i < nwords; i++) {
        long share = 0;
        for (int j = 0; j < nwords; j++)
            if (words[j][0] == words[i][0]) share += counts[j];
        scores[i] = share ? (double) counts[i] / share : 0.0;
    }
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s wordlist\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 1; }

    double t0 = now();
    char buf[MAXLEN];
    long total = 0;
    while (fscanf(f, "%63s", buf) == 1) {
        char *n = normalise(buf);
        if (*n) { add_word(n); total++; }
        free(n);
    }
    fclose(f);
    double t_read = now() - t0;

    double t1 = now();
    compute_scores();
    double t_score = now() - t1;

    double best = 0; int bi = 0;
    for (int i = 0; i < nwords; i++) if (scores[i] > best) { best = scores[i]; bi = i; }

    printf("%ld words, %d distinct\n", total, nwords);
    printf("most distinctive: %s  (count %ld, score %.6f)\n", words[bi], counts[bi], best);
    fprintf(stderr, "read+count %.3f s, score %.3f s, total %.3f s\n",
            t_read, t_score, now() - t0);
    return 0;
}
