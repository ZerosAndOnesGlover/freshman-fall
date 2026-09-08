/* PROG 201 -- Lab 8: the plugin interface.
 * A plugin is a shared object exporting one symbol, `prog201_plugin`. */
#ifndef PROG201_PLUGIN_H
#define PROG201_PLUGIN_H

#define PROG201_PLUGIN_ABI 1

/* Plugins are compiled -fvisibility=hidden (see the Makefile), so the one
 * symbol the host looks up has to be exported deliberately.  L27 section 7. */
#define PROG201_EXPORT __attribute__((visibility("default")))

struct plugin {
    int         abi;                       /* must be PROG201_PLUGIN_ABI */
    const char *name;
    const char *description;
    int       (*init)(void);               /* 0 on success              */
    long      (*apply)(long x);            /* the actual work           */
    void      (*fini)(void);
};

#endif
