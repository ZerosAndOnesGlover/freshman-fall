/* PROG 201 -- Lab 8: a plugin host.
 *
 *   make
 *   ./host ./p_double.so ./p_square.so
 *   ./host ./p_double.so ./p_bad.so ./p_missing.so     # the error paths
 *
 * Three plugins are provided: p_double and p_square work, p_bad declares an
 * ABI this host does not support.  You will write a fourth.
 *
 * The skeleton loads nothing yet -- section 1 of the lab sheet starts here.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>
#include <time.h>
#include "plugin.h"

#define MAXP 16
struct loaded { void *handle; struct plugin *p; };
static struct loaded loaded[MAXP];
static int nloaded;

/* `loaded` goes live with TODO 1; this keeps the skeleton warning-free.
 * Delete it once you have filled the table in. */
static void unused_until_todo1(void) { (void) loaded; }

static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+t.tv_nsec/1e9;}

/* TODO 1.  Load one plugin.
 *
 *   dlopen(path, ...)  -- which flags?  L27 section 4 has a table, and the
 *       answer for a plugin host is not RTLD_LAZY|RTLD_GLOBAL.
 *   dlsym(h, "prog201_plugin")  -- and check dlerror(), NOT the return value,
 *       because a symbol's value can legitimately be NULL.  Clear dlerror()
 *       first, or you will report somebody else's error.
 *   check p->abi against PROG201_PLUGIN_ABI BEFORE calling anything through
 *       the struct -- an old plugin has a different layout.
 *   call p->init if there is one; a non-zero return means refuse it.
 *   record the handle and the struct, print a line, return 0.
 *
 * Every failure path must dlclose() what it opened and return -1, and must
 * print something that names the plugin and says what was wrong.
 */
static int load(const char *path)
{
    (void) path;
    fprintf(stderr, "load(): TODO 1\n");
    return -1;
}

int main(int argc, char **argv)
{
    (void) unused_until_todo1;
    long x = 7;
    double t0 = now();
    for (int i = 1; i < argc; i++) load(argv[i]);
    double dt = now() - t0;
    printf("\nloading %d plugin(s) took %.3f ms\n\n", nloaded, dt * 1000);

    /* TODO 3.  Run every loaded plugin's apply() on x and print the result.
     * This is one line once TODO 1 fills the table. */
    (void) x;

    /* TODO 2.  Unload, in the reverse of the order you loaded them: call
     * each plugin's fini (if it has one) and then dlclose its handle. */
    printf("\n");
    return 0;
}
