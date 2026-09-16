/* smash.c -- a buffer that is too small, and the canary that notices.
   CS 202 Week 12, L37 §4. */
#include <stdio.h>
#include <string.h>

static void copy_name(const char *src)
{
	char name[16];
	strcpy(name, src);		/* no bound: this is the bug */
	printf("hello, %s\n", name);
}

int main(int argc, char **argv)
{
	copy_name(argc > 1 ? argv[1] : "student");
	printf("returned from copy_name\n");
	return 0;
}
