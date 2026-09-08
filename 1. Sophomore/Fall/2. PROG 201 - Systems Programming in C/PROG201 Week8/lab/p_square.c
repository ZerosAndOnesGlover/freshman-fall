#include <stdio.h>
#include "plugin.h"
static int  init(void)      { fprintf(stderr, "  [square] init\n"); return 0; }
static long apply(long x)   { return x * x; }
static void fini(void)      { fprintf(stderr, "  [square] fini\n"); }
PROG201_EXPORT struct plugin prog201_plugin = { PROG201_PLUGIN_ABI, "square", "x squared", init, apply, fini };
