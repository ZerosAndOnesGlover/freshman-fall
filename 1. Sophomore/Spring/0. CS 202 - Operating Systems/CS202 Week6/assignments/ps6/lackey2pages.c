/* lackey2pages.c — turn valgrind --tool=lackey --trace-mem=yes output into a page
 * reference string: one hex virtual page number per line, consecutive repeats removed.
 *   valgrind --tool=lackey --trace-mem=yes --log-file=trace.log PROGRAM ARGS
 *   ./lackey2pages [-d] < trace.log > PROGRAM.pages       (-d: data accesses only)
 * CS 202 Week 6, PS 6. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv)
{
    int data_only = argc > 1 && !strcmp(argv[1], "-d");
    char line[256];
    unsigned long last = ~0UL, events = 0, refs = 0;
    while (fgets(line, sizeof line, stdin)) {
        char kind;
        unsigned long addr;
        if (line[0] == '=') continue;
        if (line[0] == 'I') { if (data_only) continue; kind = 'I'; }
        else if (line[0] == ' ' && (line[1] == 'L' || line[1] == 'S' || line[1] == 'M')) kind = line[1];
        else continue;
        if (sscanf(line + 2, " %lx", &addr) != 1) continue;
        events++;
        unsigned long vpn = addr >> 12;
        if (vpn != last) { printf("%lx\n", vpn); refs++; last = vpn; }
        (void)kind;
    }
    fprintf(stderr, "%lu accesses, %lu page references after removing repeats\n", events, refs);
    return 0;
}
