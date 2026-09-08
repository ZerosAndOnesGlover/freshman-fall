#include <stdio.h>
#include "plugin.h"
static int  init(void)      { fprintf(stderr, "  [double] init\n"); return 0; }
static long apply(long x)   { return x * 2; }
static void fini(void)      { fprintf(stderr, "  [double] fini\n"); }
PROG201_EXPORT struct plugin prog201_plugin = { PROG201_PLUGIN_ABI, "double", "multiply by two", init, apply, fini };
