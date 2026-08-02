/* bitlib.c — Bit Manipulation Utilities — IMPLEMENTATION
 * PROG 101: Programming I — Structured Programming in C
 * Week 1, Lab 1
 *
 * Fill in each function. Document the bit trick you use.
 */

#include "bitlib.h"

/*
 * bit_set: Set bit n using the OR operator with a mask.
 * A mask with only bit n set is: (1u << n)
 * OR-ing x with this mask forces bit n to 1.
 */
uint32_t bit_set(uint32_t x, int n) {
    /* TODO: Implement using |= and a shift */
    (void)x; (void)n;   /* Remove these when you implement */
    return 0;
}

uint32_t bit_clear(uint32_t x, int n) {
    /* TODO: Implement. Hint: ~(1u << n) gives a mask with all bits set EXCEPT bit n */
    (void)x; (void)n;
    return 0;
}

uint32_t bit_toggle(uint32_t x, int n) {
    /* TODO: Implement using XOR */
    (void)x; (void)n;
    return 0;
}

int bit_test(uint32_t x, int n) {
    /* TODO: Implement. Result must be exactly 0 or 1, not just any non-zero value */
    (void)x; (void)n;
    return 0;
}

int bit_count(uint32_t x) {
    /* TODO: Implement. A simple loop works.
     * Bonus: Brian Kernighan's algorithm: x &= (x-1) clears the lowest set bit.
     *        Count how many times you can do this before x becomes 0.
     */
    (void)x;
    return 0;
}

int bit_is_power_of_2(uint32_t x) {
    /* TODO: MUST be a single expression — no if, no loop.
     * Hint: A power of 2 has exactly one bit set.
     *       What does (x & (x-1)) produce for a power of 2?
     *       Remember: 0 is NOT a power of 2.
     */
    (void)x;
    return 0;
}

uint32_t bit_reverse(uint32_t x) {
    /* TODO: Reverse all 32 bits.
     * One approach: loop 32 times, extracting the LSB of x each time
     * and placing it into the appropriate position of the result.
     */
    (void)x;
    return 0;
}

uint32_t bit_extract(uint32_t x, int high, int low) {
    /* TODO:
     * 1. Create a mask of (high - low + 1) ones: ((1u << (high-low+1)) - 1)
     * 2. Shift x right by low
     * 3. AND with mask to extract only the desired bits
     */
    (void)x; (void)high; (void)low;
    return 0;
}

uint32_t bit_set_field(uint32_t x, int high, int low, uint32_t value) {
    /* TODO:
     * 1. Create the field mask
     * 2. Clear the field in x: x &= ~(mask << low)
     * 3. Mask and shift value: value = (value & mask) << low
     * 4. OR in the new value
     */
    (void)x; (void)high; (void)low; (void)value;
    return 0;
}

uint32_t bit_byteswap(uint32_t x) {
    /* TODO:
     * Extract each byte and reassemble in reverse order.
     * Byte 0 (bits 7-0)   → goes to bits 31-24
     * Byte 1 (bits 15-8)  → goes to bits 23-16
     * Byte 2 (bits 23-16) → goes to bits 15-8
     * Byte 3 (bits 31-24) → goes to bits 7-0
     *
     * Hint: use (x & 0xFF) to extract byte 0, (x >> 8) & 0xFF for byte 1, etc.
     */
    (void)x;
    return 0;
}
