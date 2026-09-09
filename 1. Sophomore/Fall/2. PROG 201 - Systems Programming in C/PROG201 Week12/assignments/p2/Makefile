# PROJECT 2 -- production build (prod) and sanitizer build (asan). No warnings.
# Do NOT commit the binaries.
CC      = cc
CFLAGS  = -Wall -Wextra -Werror -O2 -std=gnu11 -pthread \
          -fstack-protector-strong -D_FORTIFY_SOURCE=2
SAN     = -fsanitize=address,undefined -g -O1

httpd: httpd.c
	$(CC) $(CFLAGS) -o $@ $<

# sanitizer build for Part 4 -- run your own traffic through this
httpd-asan: httpd.c
	$(CC) -Wall -Wextra -std=gnu11 -pthread $(SAN) -o $@ $<

# fuzz target for Part 4 (clang; supply your parser + fuzz_parser.c)
# fuzz: fuzz_parser.c parser.c
# 	clang -fsanitize=fuzzer,address -g -o $@ fuzz_parser.c parser.c

clean:
	rm -f httpd httpd-asan fuzz

.PHONY: clean
