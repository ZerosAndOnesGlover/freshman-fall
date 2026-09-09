/* run the parser on one input file -- for reproducing a saved crash under
 * the sanitizer once the fuzzer has found it. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int parse(const uint8_t *, size_t);
int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: %s crashfile\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror(argv[1]); return 1; }
    static uint8_t buf[65536];
    size_t n = fread(buf, 1, sizeof buf, f);
    fclose(f);
    /* copy into an exact-sized heap block so ASan's bounds are tight */
    uint8_t *h = malloc(n ? n : 1);
    for (size_t i = 0; i < n; i++) h[i] = buf[i];
    int r = parse(h, n);
    printf("parse returned %d\n", r);
    free(h);
    return 0;
}
