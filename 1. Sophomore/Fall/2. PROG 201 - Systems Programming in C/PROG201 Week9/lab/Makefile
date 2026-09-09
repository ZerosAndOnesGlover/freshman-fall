CFLAGS = -Wall -Wextra -O2 -g

all: roof cache target vecbench

roof: roof.c
	$(CC) $(CFLAGS) -march=native -o $@ $< -lm

cache: cache.c
	$(CC) $(CFLAGS) -o $@ $<

# the sampling profiler from L28, and a target to point it at
target: target.c sprof.c
	$(CC) $(CFLAGS) -rdynamic -o $@ target.c sprof.c -ldl

# the same loop at -O2 and -O3, for section 5
vecbench: vecbench.c
	$(CC) -Wall -Wextra -O2 -g -o vb_O2 vecbench.c
	$(CC) -Wall -Wextra -O3 -g -o vb_O3 vecbench.c
	@touch vecbench

clean:
	rm -f roof cache target vb_O2 vb_O3 vecbench

.PHONY: all clean
