# clang provides libFuzzer (-fsanitize=fuzzer) and ASan; AFL is not installed.
CC = clang
CFLAGS = -O1 -g

all: fuzz run_one heap fmt

fuzz: fuzz_parser.c parser.c
	$(CC) $(CFLAGS) -fsanitize=fuzzer,address,undefined -o $@ fuzz_parser.c parser.c

run_one: run_one.c parser.c
	$(CC) $(CFLAGS) -fsanitize=address,undefined -o $@ run_one.c parser.c

# the heap-bug and format-string demos from L33
heap: heap.c
	$(CC) $(CFLAGS) -fsanitize=address -o $@ heap.c
	gcc -O0 -o heap_plain heap.c

fmt: fmt.c
	gcc -fno-stack-protector -o $@ fmt.c

# find a crash (a few seconds), then reproduce it under the sanitizer:
find: fuzz
	mkdir -p corpus
	./fuzz -max_total_time=20 -artifact_prefix=./ corpus || true

clean:
	rm -f fuzz run_one heap heap_plain fmt crash-* *.o
	rm -rf corpus

.PHONY: all find clean
