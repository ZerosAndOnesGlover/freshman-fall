/* bitlib.h — Bit Manipulation Utilities
 * PROG 101: Programming I — Structured Programming in C
 * Week 1, Lab 1
 *
 * Usage:
 *   #include "bitlib.h"
 *   Link with bitlib.o (compile bitlib.c)
 */

#ifndef BITLIB_H
#define BITLIB_H

#include <stdint.h>

/*
 * bit_set — Set bit n in x (bit 0 = LSB, bit 31 = MSB)
 * Returns the modified value.
 * Example: bit_set(0b1010, 0) = 0b1011
 */
uint32_t bit_set(uint32_t x, int n);

/*
 * bit_clear — Clear bit n in x
 * Returns the modified value.
 * Example: bit_clear(0b1111, 2) = 0b1011
 */
uint32_t bit_clear(uint32_t x, int n);

/*
 * bit_toggle — Flip bit n in x
 * Returns the modified value.
 * Example: bit_toggle(0b1010, 1) = 0b1000
 */
uint32_t bit_toggle(uint32_t x, int n);

/*
 * bit_test — Test whether bit n is set
 * Returns 1 if bit n is 1, 0 if bit n is 0.
 * Example: bit_test(0b1010, 1) = 1
 *          bit_test(0b1010, 0) = 0
 */
int bit_test(uint32_t x, int n);

/*
 * bit_count — Count the number of 1 bits (population count)
 * Returns the number of bits set to 1 in x.
 * Example: bit_count(0b10110101) = 5
 * Bonus challenge: implement without any loops!
 */
int bit_count(uint32_t x);

/*
 * bit_is_power_of_2 — Test if x is a power of 2
 * Returns 1 if x is a power of 2 (1, 2, 4, 8, 16, ...), 0 otherwise.
 * REQUIREMENT: Must be a single expression — no loops, no if statements.
 * Hint: what does a power of 2 look like in binary?
 *       What does (n & (n-1)) compute?
 */
int bit_is_power_of_2(uint32_t x);

/*
 * bit_reverse — Reverse all 32 bits of x
 * Returns x with bit 0 and bit 31 swapped, bit 1 and bit 30 swapped, etc.
 * Example: bit_reverse(0x80000000) = 0x00000001
 *          bit_reverse(0xA0000000) = 0x00000005
 */
uint32_t bit_reverse(uint32_t x);

/*
 * bit_extract — Extract a bitfield
 * Returns the bits of x from position low to position high (inclusive),
 * right-shifted so the lowest bit of the field is at position 0.
 *
 * Example: x = 0b11_1010_1100
 *          bit_extract(x, 7, 4) extracts bits 7,6,5,4 = 0b1010 = 10
 *
 * Precondition: 0 <= low <= high <= 31
 */
uint32_t bit_extract(uint32_t x, int high, int low);

/*
 * bit_set_field — Set a bitfield to a value
 * Sets bits [high..low] of x to value (the low (high-low+1) bits of value).
 * Returns the modified x.
 *
 * Example: bit_set_field(0xFFFFFFFF, 7, 4, 0b1010)
 *          clears bits 7-4 and sets them to 0b1010
 *          Result: 0xFFFFFF_A_F → 0xFFFFFFAF
 *
 * Precondition: 0 <= low <= high <= 31
 */
uint32_t bit_set_field(uint32_t x, int high, int low, uint32_t value);

/*
 * bit_byteswap — Swap byte order (endianness)
 * Reverses the byte order of a 32-bit value.
 * Used to convert between little-endian and big-endian.
 * Example: bit_byteswap(0x12345678) = 0x78563412
 */
uint32_t bit_byteswap(uint32_t x);

#endif /* BITLIB_H */
