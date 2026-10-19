/* info.c — PROG 101, Week 0, Problem Set 0 (Problem 2)
 * A fixed-width student profile card, exactly 52 columns wide.
 *
 *   gcc -Wall -Wextra -Werror -std=c11 -o info info.c
 */

#include <stdio.h>

#define NAME    "Adebayo Glover"
#define ID      "20260001"
#define YEAR    2026
#define COURSE  "PROG 101 - Structured Programming in C"

/* One horizontal rule: a left cap, 50 fill characters, a right cap. */
static void rule(const char *left, const char *fill, const char *right) {
    printf("%s", left);
    for (int i = 0; i < 50; ++i) {
        printf("%s", fill);
    }
    printf("%s\n", right);
}

int main(void) {
    rule("╔", "═", "╗");
    printf("║%*s%s%*s║\n", 13, "", "PROG 101 Student Profile", 13, "");
    rule("╠", "═", "╣");
    printf("║  Name:    %-38s ║\n", NAME);
    printf("║  ID:      %-38s ║\n", ID);
    printf("║  Year:    %-38d ║\n", YEAR);
    printf("║  Course:  %-38s ║\n", COURSE);
    rule("╚", "═", "╝");
    return 0;
}
