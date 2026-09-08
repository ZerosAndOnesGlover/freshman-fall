CFLAGS = -Wall -Wextra -O2 -g -std=c11
PLUGIN_CFLAGS = $(CFLAGS) -fPIC -shared -fvisibility=hidden
LDLIBS = -ldl

PLUGINS = p_double.so p_square.so p_bad.so

all: host $(PLUGINS)

host: host.c plugin.h
	$(CC) $(CFLAGS) -o $@ host.c $(LDLIBS)

%.so: %.c plugin.h
	$(CC) $(PLUGIN_CFLAGS) -o $@ $<

run: all
	./host ./p_double.so ./p_square.so

errors: all
	./host ./p_double.so ./p_bad.so ./p_missing.so

clean:
	rm -f host *.so

.PHONY: all run errors clean
