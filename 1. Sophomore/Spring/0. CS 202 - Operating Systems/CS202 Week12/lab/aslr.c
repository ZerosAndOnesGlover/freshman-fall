/* aslr.c -- where the pieces of an address space landed.  Week 12, L37 §5. */
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

int global;

int main(void)
{
	int local;
	void *heap = malloc(16);
	void *map = mmap(NULL, 4096, PROT_READ, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

	printf("%p %p %p %p %p\n", (void *)main, (void *)&global, heap, map, (void *)&local);
	return 0;
}
