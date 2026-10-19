/* bad.c — declares abs_int itself and calls it.
 *
 * This translation unit compiles cleanly: a declaration is a promise, and
 * that is all the compiler needs to emit a call. The failure happens later,
 * at link time, because mathutil.c's abs_int has internal linkage (it is
 * `static`) and so is not exported for bad.o to resolve against.
 */
int abs_int(int x);   /* declaration only — no visible definition */

int main(void) {
    return abs_int(-7);
}
