/* rss.c: address space is not memory. Map 256 MiB, then touch it a quarter at a time. */
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
static void show(const char *when)
{
    FILE *f = fopen("/proc/self/status", "r"); char line[128];
    printf("%-24s", when);
    while (fgets(line, sizeof line, f))
        if (!strncmp(line, "VmSize", 6) || !strncmp(line, "VmRSS", 5)) { line[strlen(line)-1] = 0; printf("  %s", line); }
    printf("\n"); fclose(f);
}
int main(void)
{
    size_t len = 256UL << 20;
    show("start");
    char *p = mmap(0, len, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    show("after mmap 256 MiB");
    for (int q = 1; q <= 4; q++) {
        memset(p + (q - 1) * (len / 4), 1, len / 4);
        char label[32]; snprintf(label, sizeof label, "after touching %d/4", q);
        show(label);
    }
    munmap(p, len);
    show("after munmap");
    return 0;
}
