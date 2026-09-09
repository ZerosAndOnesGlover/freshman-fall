/* the libFuzzer entry point -- one function, and clang provides main(). */
#include <stdint.h>
#include <stddef.h>
int parse(const uint8_t *, size_t);
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    parse(data, size);
    return 0;
}
