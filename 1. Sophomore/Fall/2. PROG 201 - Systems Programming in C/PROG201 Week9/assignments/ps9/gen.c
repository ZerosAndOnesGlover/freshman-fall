/* PROG 201 -- PS 9: generate the word list.
 *   ./gen 400000 > words.txt
 * Deterministic: the same count always gives the same file, so your
 * before-and-after numbers are comparable and so are everybody else's. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned long s = 88172645463325252UL;
static unsigned long rnd(void){ s^=s<<13; s^=s>>7; s^=s<<17; return s; }

int main(int argc, char **argv)
{
    long n = argc > 1 ? atol(argv[1]) : 400000;
    static const char *common[] = { "the","of","and","to","in","a","is","that","it","for" };
    static char tail[6000][10];
    for (int i = 0; i < 6000; i++) {
        int len = 3 + (int)(rnd() % 7);
        for (int j = 0; j < len; j++) tail[i][j] = 'a' + (char)(rnd() % 26);
        tail[i][len] = 0;
    }
    for (long i = 0; i < n; i++) {
        if (rnd() % 100 < 45) fputs(common[rnd() % 10], stdout);
        else                  fputs(tail[rnd() % 6000], stdout);
        putchar(i + 1 == n ? '\n' : ' ');
    }
    return 0;
}
