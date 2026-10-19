/* wordcount.c — PROG 101 Lab 2, Part 4: a two-state word counter.
 * Reads stdin char by char; counts words on the transition into IN_WORD.
 * `int c`, not `char c`, so EOF is distinguishable from every character.
 */
#include <stdio.h>

#define OUT_OF_WORD 0
#define IN_WORD     1

int main(void) {
    int st = OUT_OF_WORD;
    long words = 0, chars = 0, lines = 0;
    int c;

    while ((c = getchar()) != EOF) {
        chars++;
        if (c == '\n') lines++;

        switch (st) {
            case OUT_OF_WORD:
                if (!(c == ' ' || c == '\t' || c == '\n')) {
                    st = IN_WORD;
                    words++;                 /* count on transition only */
                }
                break;
            case IN_WORD:
                if (c == ' ' || c == '\t' || c == '\n') {
                    st = OUT_OF_WORD;
                }
                break;
        }
    }

    printf("%ld %ld %ld\n", lines, words, chars);
    return 0;
}
