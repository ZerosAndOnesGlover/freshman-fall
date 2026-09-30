/* info.c — PS 0, Problem 2: Personal Info Printer
 * PROG 101: Programming I — Structured Programming in C
 *
 * Prints a student profile card inside a 52-character-wide box.
 *
 * Layout: each row is  ║ + 50 characters + ║.  Field values are printed with
 * a left-aligned width (%-39s / %-39d) so the right border always lands in the
 * same column.  printf counts BYTES, not characters, so the values must be
 * plain ASCII; the box-drawing characters (3 bytes each in UTF-8) sit in the
 * literal parts of the format strings, where no width is applied.
 *
 * Compile with:
 *   gcc -Wall -Wextra -Werror -g -std=c11 -o info info.c
 */

#include <stdio.h>

#define STUDENT_NAME "Adebayo Glover"
#define STUDENT_ID   "20260001"        /* TODO: replace with my real student ID */
#define GRAD_YEAR    2030              /* TODO: replace with my graduation year */
#define COURSE       "PROG 101 - Structured Programming in C"

int main(void) {
    printf("╔══════════════════════════════════════════════════╗\n");
    printf("║             PROG 101 Student Profile             ║\n");
    printf("╠══════════════════════════════════════════════════╣\n");
    printf("║  Name:    %-39s║\n", STUDENT_NAME);
    printf("║  ID:      %-39s║\n", STUDENT_ID);
    printf("║  Year:    %-39d║\n", GRAD_YEAR);
    printf("║  Course:  %-39s║\n", COURSE);
    printf("╚══════════════════════════════════════════════════╝\n");
    return 0;
}
